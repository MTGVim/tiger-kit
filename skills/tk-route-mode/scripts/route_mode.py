#!/usr/bin/env python3
"""단일 위임 대응표 도우미.

모델 추천 판단과 호스트 설정의 적용·검증은 SKILL.md의 대화형 절차가 담당한다.
"""
import argparse
import copy
import json
import os
import re
import stat
import tempfile
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DEFAULTS = HERE / "references" / "route-defaults.json"
TIERS = ("light", "standard", "top")


def config_path():
    if os.environ.get("ROUTE_MODE_CONFIG"):
        return Path(os.environ["ROUTE_MODE_CONFIG"])
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "route-mode" / "routes.json"


def safe_path(path):
    p = Path(path).expanduser().absolute()
    if ".." in p.parts:
        raise ValueError("상위 디렉터리 경로는 사용할 수 없습니다")
    for part in (p, *p.parents):
        if part.is_symlink():
            raise ValueError("심볼릭 링크 경로는 사용할 수 없습니다")
    if p.exists() and (not p.is_file() or p.stat().st_uid != os.getuid() or p.stat().st_nlink != 1):
        raise ValueError("사용자 소유 일반 파일만 사용할 수 있습니다")
    return p


def read_json(path):
    p = safe_path(path)
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValueError("중복 JSON 키")
            out[k] = v
        return out
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=unique)


def atomic_write(path, data, mode=0o600):
    p = safe_path(path)
    p.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if p.exists():
        mode = stat.S_IMODE(p.stat().st_mode)
    fd, name = tempfile.mkstemp(prefix=".route-mode-", dir=p.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        safe_path(p)
        os.replace(name, p)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return p


def save(data, path=None):
    p = safe_path(path or config_path())
    return atomic_write(p, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())


def backup_config(path):
    from datetime import datetime, timezone
    p = safe_path(path or config_path())
    if p.exists():
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        atomic_write(p.parent / "backups" / ts / p.name, p.read_bytes())


def _default():
    return read_json(DEFAULTS)


def _legacy_source(path):
    p = safe_path(path or config_path())
    old = safe_path(p.parent / "modes.json")
    return p if p.exists() and read_json(p).get("version") == 1 else old


def resolve_legacy(old, name, seen=()):
    """기존 extends를 펼친 실효 대응표를 변경 없이 계산한다."""
    if name not in old.get("modes", {}):
        raise ValueError(f"기존 모드를 찾을 수 없습니다: {name}")
    if name in seen:
        raise ValueError("기존 모드 extends 순환")
    mode = old["modes"][name]
    out = resolve_legacy(old, mode["extends"], seen + (name,)) if mode.get("extends") else {}
    for provider, tiers in mode.get("providers", {}).items():
        for tier, cell in tiers.items():
            out.setdefault(provider, {})[tier] = copy.deepcopy(cell)
    return out


def legacy_preview(old, selected=None):
    """활성 모드의 실효값을 가져오고, 기본값과 다른 칸 및 수동 override를 보존한다."""
    name = selected or old.get("active")
    resolved = resolve_legacy(old, name)
    new = _default()
    new["tiers"] = copy.deepcopy(old.get("tiers", new["tiers"]))
    new["efforts"] = copy.deepcopy(old.get("efforts", new["efforts"]))
    new["providers"] = copy.deepcopy(resolved)
    marked = {}
    def mark_chain(mode_name):
        mode = old["modes"][mode_name]
        if mode.get("extends"):
            mark_chain(mode["extends"])
        marked.update(mode.get("overrides", {}))
    mark_chain(name)
    bundle = _default()["providers"]
    for provider, tiers in resolved.items():
        for tier, cell in tiers.items():
            key = f"{provider}.{tier}"
            if cell != bundle.get(provider, {}).get(tier) or key in marked:
                new["overrides"][key] = copy.deepcopy(cell)
    return new


def load_config(path=None):
    """(유효한 v2 또는 읽기 전용 v1 미리보기, 출처 정보). 파일은 생성하지 않는다."""
    p = safe_path(path or config_path())
    if p.exists():
        raw = read_json(p)
        if raw.get("version") == 2:
            return raw, {"source": str(p), "legacy": False, "missing": False}
        if raw.get("version") == 1:
            return legacy_preview(raw), {"source": str(p), "legacy": True, "missing": False,
                                         "active": raw.get("active"), "modes": list(raw.get("modes", {}))}
        raise ValueError("지원하지 않는 대응표 버전")
    old = safe_path(p.parent / "modes.json")
    if old.exists():
        raw = read_json(old)
        if raw.get("version") != 1:
            raise ValueError("기존 파일이 v1 모드 형식이 아닙니다")
        return legacy_preview(raw), {"source": str(old), "legacy": True, "missing": False,
                                     "active": raw.get("active"), "modes": list(raw.get("modes", {}))}
    return _default(), {"source": str(DEFAULTS), "legacy": False, "missing": True}


def validate(data):
    errors, warnings = [], []
    if data.get("version") != 2 or "modes" in data or "active" in data:
        errors.append("단일 대응표 v2만 허용합니다")
    providers = data.get("providers")
    if not isinstance(providers, dict) or not providers:
        errors.append("providers가 없거나 비어 있습니다")
        return errors, warnings
    efforts = data.get("efforts", {})
    if not isinstance(efforts, dict):
        errors.append("efforts 형식 오류")
        return errors, warnings
    overrides = data.get("overrides", {})
    if not isinstance(overrides, dict):
        errors.append("overrides 형식 오류")
        return errors, warnings
    for provider, tiers in providers.items():
        if provider not in efforts or not isinstance(efforts[provider], list):
            errors.append(f"{provider}: effort 목록 없음")
            continue
        if not isinstance(tiers, dict):
            errors.append(f"{provider}: 티어 형식 오류")
            continue
        for tier in TIERS:
            cell = tiers.get(tier)
            if not isinstance(cell, dict) or not isinstance(cell.get("model"), str) or not cell["model"].strip() or not isinstance(cell.get("effort"), str):
                errors.append(f"{provider}.{tier}: 모델·effort 누락")
                continue
            if cell["effort"] not in efforts[provider]:
                errors.append(f"{provider}.{tier}: 지원 effort 목록과 불일치")
            if provider == "openai" and cell["model"] in ("luna", "terra", "sol"):
                warnings.append(f"{provider}.{tier}: 과거 별칭 {cell['model']} (카탈로그 대조 전 치환 금지)")
        for tier in set(tiers) - set(TIERS):
            errors.append(f"{provider}.{tier}: 알 수 없는 티어")
    for key, cell in overrides.items():
        provider, dot, tier = key.partition(".")
        if not dot or tier not in TIERS or provider not in providers or providers[provider].get(tier) != cell:
            errors.append(f"override와 실효값 불일치: {key}")
    return errors, warnings


def plan(data, provider):
    table = data.get("providers", {}).get(provider)
    if not table:
        raise ValueError(f"공급자 대응표 없음: {provider}")
    defaults = _default().get("providers", {}).get(provider, {})
    rows = ["| 티어 | 맡는 일 | 스킬 기본값 | 실효 모델 / effort | 출처 |",
            "|---|---|---|---|---|"]
    for tier in TIERS:
        cell = table[tier]
        base = defaults.get(tier)
        base_text = f"{base['model']} / {base['effort']}" if base else "없음"
        key = f"{provider}.{tier}"
        origin = "사용자 override" if key in data.get("overrides", {}) else ("기본값" if base == cell else "저장된 사용자 값")
        rows.append(f"| {tier} | {data['tiers'][tier]} | {base_text} | {cell['model']} / {cell['effort']} | {origin} |")
    return "\n".join(rows)


def edit(data, sets, unsets):
    if not sets and not unsets:
        raise ValueError("변경할 칸을 지정해야 합니다")
    updated = copy.deepcopy(data)
    touched = set()
    for item in sets:
        key, sep, value = item.partition("=")
        provider, dot, tier = key.partition(".")
        model, colon, effort = value.rpartition(":")
        if not sep or not dot or provider not in updated["providers"] or tier not in TIERS or not colon or not model.strip() or effort not in updated["efforts"][provider] or key in touched:
            raise ValueError(f"잘못되거나 중복된 --set: {item}")
        if provider == "openai" and model in ("luna", "terra", "sol"):
            raise ValueError("확인되지 않은 Codex 별칭을 새 설정에 저장할 수 없습니다")
        touched.add(key)
        cell = {"model": model, "effort": effort}
        updated["providers"][provider][tier] = cell
        updated["overrides"][key] = cell
    for key in unsets:
        provider, dot, tier = key.partition(".")
        base = _default()["providers"].get(provider, {}).get(tier)
        if not dot or tier not in TIERS or key in touched or key not in updated["overrides"] or not base:
            raise ValueError(f"해제할 override가 없거나 기본값을 찾지 못함: {key}")
        touched.add(key)
        del updated["overrides"][key]
        updated["providers"][provider][tier] = copy.deepcopy(base)
    return updated


BEGIN, END = "<!-- route-mode:begin -->", "<!-- route-mode:end -->"


def rule_block(prefix="tier-"):
    n = {t: f"`{prefix}{t}`" for t in TIERS}
    return (f"{BEGIN}\n하위 에이전트에 위임할 때는 {n['light']}(좁은 사실 수집, 탐색·분류, 기계적 검사), "
            f"{n['standard']}(구현, 독립 리뷰), {n['top']}(아키텍처, 미지 문제 탐사·연구) 중에서 고르고, "
            f"호출할 때 모델·effort 인자를 따로 넘기지 않는다.\n"
            f"예외: 현재 실행이 명시적으로 Ralphex 세션(TK_RALPH_SESSION=1)임을 확인했다면 "
            f"위 티어 대상 선택을 생략하고 자식에게 부모 모델 상속을 요청한다. "
            f"실행기 표식을 확인할 수 없다면 Ralph 세션이라고 추측하지 않는다.\n{END}\n")


def rule_span(text):
    """블록 위치 (시작, 끝) 또는 None. 표시가 깨졌거나 여러 개면 ValueError."""
    b, e = text.count(BEGIN), text.count(END)
    if b == e == 0:
        return None
    if b != 1 or e != 1 or text.index(BEGIN) > text.index(END):
        raise ValueError(f"route-mode 표시가 깨졌거나 여러 개임 (begin {b}, end {e})")
    end = text.index(END) + len(END)
    return text.index(BEGIN), end + (1 if text[end:end + 1] == "\n" else 0)


def rule_apply(path, action, host, prefix="tier-", config=None):
    """지침 파일에 위임 규칙 블록을 넣거나 뺀다. 바꾸기 전에 백업하고 적용 기록에 남긴다."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", host) or prefix not in ("tier-", ""):
        raise ValueError("잘못된 호스트 이름 또는 접두어")
    path = safe_path(path)
    original = path.read_bytes() if path.exists() else b""
    text = original.decode("utf-8")
    span = rule_span(text)
    if action == "status":
        return "on" if span else "off"
    if action == "on":
        block = rule_block(prefix)
        new = text[:span[0]] + block + text[span[1]:] if span else \
            text + ("" if not text or text.endswith("\n") else "\n") + block
    else:
        new = text[:span[0]] + text[span[1]:] if span else text

    if new == text:
        return "unchanged"
    root = safe_path(config or config_path()).parent
    journal = safe_path(root / "applied" / f"{host}.json")
    rec = read_json(journal) if journal.exists() else {}
    if not isinstance(rec, dict) or not isinstance(rec.get("rule", []), list):
        raise ValueError("적용 기록 형식 오류")
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    if action == "off" and span and span[0] == len(new) and new.endswith("\n"):
        for entry in reversed(rec.get("rule", [])):
            if entry.get("file") == str(path) and entry.get("action") == "on":
                if entry.get("before_sha256") == hashlib.sha256(new[:-1].encode()).hexdigest():
                    new = new[:-1]
                break
    backup = None
    if path.exists():
        backup = root / "backups" / ts / path.name
        atomic_write(backup, original)
    if (path.read_bytes() if path.exists() else b"") != original:
        raise ValueError("조회 이후 파일이 변경되었습니다")
    rec.setdefault("rule", []).append({"at": ts, "file": str(path), "action": action,
                                      "backup": str(backup) if backup else None,
                                      "before_sha256": hashlib.sha256(original).hexdigest(),
                                      "after_sha256": hashlib.sha256(new.encode()).hexdigest(), "status": "pending"})
    atomic_write(journal, (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode())
    atomic_write(path, new.encode())
    rec["rule"][-1]["status"] = "applied"
    atomic_write(journal, (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode())
    return action


def main(argv=None):
    ap = argparse.ArgumentParser(prog="route_mode", description="단일 위임 대응표 조회·검증·승인된 설정 변경")
    ap.add_argument("--config", help="단일 대응표 (기본: $ROUTE_MODE_CONFIG 또는 ~/.config/route-mode/routes.json)")
    sub = ap.add_subparsers(dest="cmd")
    status = sub.add_parser("status", help="기본값과 실효값, 출처 조회 (읽기 전용)")
    status.add_argument("--provider")
    status.add_argument("--host")
    status.add_argument("--rule-file")
    sub.add_parser("path", help="설정 및 레거시 파일 위치 확인")
    sub.add_parser("validate", help="단일 대응표와 별칭 검사 (읽기 전용)")
    p = sub.add_parser("plan", help="공급자별 단일 대응표 비교")
    p.add_argument("--provider", required=True)
    a = sub.add_parser("apply", help="승인된 모델·effort 변경만 저장 (호스트 파일 미변경)")
    a.add_argument("--set", action="append", default=[], metavar="PROVIDER.TIER=MODEL:EFFORT")
    a.add_argument("--unset", action="append", default=[], metavar="PROVIDER.TIER")
    m = sub.add_parser("migrate", help="기존 활성 모드에서 단일 대응표로 읽기 전용 미리보기 또는 승인 후 이전")
    m.add_argument("--source", help="기존 modes.json의 정확한 경로")
    m.add_argument("--select-mode", help="활성 모드 외의 모드를 명시적으로 선택할 때만 지정")
    m.add_argument("--save", action="store_true", help="승인 후 새 파일에 저장")
    m.add_argument("--accept-inactive-modes", action="store_true", help="사용하지 않는 과거 모드의 미이전 승인")
    r = sub.add_parser("rule", help="사용자 지침의 위임 규칙 블록 관리")
    r.add_argument("action", choices=["on", "off", "status"])
    r.add_argument("--file", required=True)
    r.add_argument("--host", default="unknown")
    r.add_argument("--prefix", default="tier-")
    args = ap.parse_args(argv)
    if args.cmd is None:
        args.cmd = "status"
        args.provider = args.host = args.rule_file = None
    if args.cmd == "rule":
        print(rule_apply(args.file, args.action, args.host, args.prefix, args.config))
        return 0
    pth = safe_path(args.config or config_path())
    if args.cmd == "migrate":
        source = safe_path(args.source or _legacy_source(pth))
        if not source.exists():
            raise ValueError("기존 modes.json을 찾을 수 없습니다")
        raw = read_json(source)
        if raw.get("version") != 1:
            raise ValueError("v1 모드 설정만 이전할 수 있습니다")
        name = args.select_mode or raw.get("active")
        candidate = legacy_preview(raw, name)
        errors, warnings = validate(candidate)
        print(f"source: {source}\nselected legacy mode: {name}")
        print("legacy modes (only selected mode will be migrated):", ", ".join(raw["modes"]))
        for provider in candidate["providers"]:
            print("\n" + provider + "\n" + plan(candidate, provider))
        for message in errors + warnings:
            print(("ERROR " if message in errors else "WARN ") + message)
        if errors:
            return 1
        if args.save:
            if not args.accept_inactive_modes and any(mode != name for mode in raw["modes"]):
                raise ValueError("사용하지 않는 기존 모드가 있습니다. 이전 대상과 미이전 범위를 승인받아야 합니다")
            if pth.exists():
                raise ValueError("새 단일 대응표 파일이 이미 있습니다. 덮어쓰지 않습니다")
            # 원본은 그대로 보존하며 별도 지속 백업도 생성합니다.
            from datetime import datetime, timezone
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
            backup_name = source.parent / "backups" / f"legacy-modes-{stamp}.json"
            original = source.read_bytes()
            atomic_write(backup_name, original)
            if pth.exists() or source.read_bytes() != original:
                raise ValueError("이전 시작 이후 원본이나 대상이 변경되었습니다")
            print("saved:", save(candidate, pth))
        return 0
    data, meta = load_config(pth)
    errors, warnings = validate(data)
    if args.cmd in ("status", "path", "validate"):
        print(f"config: {meta['source']}")
        print("state:", "legacy preview - migration required" if meta["legacy"] else ("bundled defaults" if meta["missing"] else "saved single mapping"))
        if meta["legacy"]:
            print("legacy active:", meta["active"], "| unused:", ", ".join(m for m in meta["modes"] if m != meta["active"]))
    for message in errors + warnings:
        print(("ERROR " if message in errors else "WARN ") + message)
    if errors:
        return 1
    if args.cmd == "status":
        providers = [args.provider] if args.provider else data["providers"]
        for provider in providers:
            print("\nprovider:", provider, "\n" + plan(data, provider))
        if args.host:
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.host):
                raise ValueError("잘못된 호스트")
            rec = safe_path(pth.parent / "applied" / f"{args.host}.json")
            print("application record:", "present" if rec.exists() else "absent")
        if args.rule_file:
            print("managed rule marker:", rule_apply(args.rule_file, "status", args.host or "unknown"))
        print("profile files: unverified\nprofile load: unverified\nselection rule: unverified")
        for tier in TIERS:
            print(f"{tier} effective model/effort: unverified")
    elif args.cmd == "path":
        print("destination:", pth)
    elif args.cmd == "validate":
        print("OK" if not meta["legacy"] else "MIGRATION REQUIRED")
        return 1 if meta["legacy"] else 0
    elif args.cmd == "plan":
        print(plan(data, args.provider))
    elif args.cmd == "apply":
        if meta["legacy"]:
            raise ValueError("기존 사용자 설정 이전 승인이 필요합니다. migrate를 먼저 사용하세요")
        updated = edit(data, args.set, args.unset)
        errs, warns = validate(updated)
        if errs:
            raise ValueError("; ".join(errs))
        for w in warns:
            print("WARN", w)
        before = pth.read_bytes() if pth.exists() else None
        backup_config(pth)
        if (pth.read_bytes() if pth.exists() else None) != before:
            raise ValueError("조회 이후 사용자 설정이 변경되었습니다")
        print("saved:", save(updated, pth))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, TypeError, KeyError, AttributeError, json.JSONDecodeError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        sys.exit(1)
