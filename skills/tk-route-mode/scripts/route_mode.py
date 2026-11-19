#!/usr/bin/env python3
"""route-mode 대응표 도구: 검사, 계획 출력, 모드 전환·추가, 벤치마크로 기본 모드 도출.

호스트 설정은 건드리지 않는다. 적용과 확인은 SKILL.md 절차대로 에이전트가 한다.
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
DEFAULTS = HERE / "references" / "default-modes.json"
BENCH = HERE / "references" / "benchmarks.json"
TIERS = ("light", "standard", "top")


def config_path():
    if os.environ.get("ROUTE_MODE_CONFIG"):
        return Path(os.environ["ROUTE_MODE_CONFIG"])
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "route-mode" / "modes.json"


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


def load(path=None):
    p = safe_path(path or config_path())
    return read_json(p if p.exists() else DEFAULTS)


def save(data, path=None):
    p = safe_path(path or config_path())
    return atomic_write(p, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())


def backup_config(path):
    from datetime import datetime, timezone
    p = safe_path(path or config_path())
    if p.exists():
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        atomic_write(p.parent / "backups" / ts / p.name, p.read_bytes())


def update_mode(data, name, sets, unsets, description, bench):
    if name not in data["modes"]:
        raise ValueError(f"없는 모드: {name}")
    new = copy.deepcopy(data)
    mode = new["modes"][name]
    overrides = mode.setdefault("overrides", {})
    providers = mode.setdefault("providers", {})
    def key_parts(key):
        prov, sep, tier = key.partition(".")
        if not sep or prov not in new["efforts"] or tier not in TIERS:
            raise ValueError(f"잘못된 칸: {key}")
        return prov, tier

    touched = set()
    for item in sets:
        key, sep, value = item.partition("=")
        prov, tier = key_parts(key)
        model, colon, effort = value.rpartition(":")
        if not sep or not colon or not model.strip() or effort not in new["efforts"][prov] or key in touched:
            raise ValueError(f"잘못되거나 중복된 --set: {item}")
        touched.add(key)
        cell = {"model": model, "effort": effort}
        providers.setdefault(prov, {})[tier] = cell
        overrides[key] = cell
    for key in unsets:
        prov, tier = key_parts(key)
        if key in touched or key not in overrides:
            raise ValueError(f"해제할 사용자 override가 없거나 중복됨: {key}")
        touched.add(key)
        del overrides[key]
        # 기본 모드는 도출값으로 복원하고, 파생 모드는 부모의 값을 상속한다.
        if name in ("standard", "economy") and bench:
            providers.setdefault(prov, {})[tier] = derive(new, bench)[name]["providers"][prov][tier]
        elif mode.get("extends"):
            providers.get(prov, {}).pop(tier, None)
            if not providers.get(prov):
                providers.pop(prov, None)
        else:
            raise ValueError(f"복원할 기본값 없음: {key}")
    if description is not None:
        mode["description"] = description
    if not touched and description is None:
        raise ValueError("변경할 칸 또는 설명을 지정해야 합니다")
    return new


def resolve(data, mode, seen=()):
    """extends를 펼친 모드의 providers 표를 돌려준다."""
    if mode not in data["modes"]:
        raise ValueError(f"없는 모드: {mode}")
    if mode in seen:
        raise ValueError(f"extends 순환: {' -> '.join(seen + (mode,))}")
    m = data["modes"][mode]
    out = copy.deepcopy(resolve(data, m["extends"], seen + (mode,))) if m.get("extends") else {}
    for prov, tiers in m.get("providers", {}).items():
        for tier, cell in tiers.items():
            out.setdefault(prov, {})[tier] = cell
    return out


def dominated(bench, prov, model, effort):
    """같은 공급자 안에서 비용이 같거나 싸고 점수가 같거나 높은 칸 중 점수가 가장 높은 칸."""
    table = bench["providers"].get(prov, {})
    me = table.get(model, {}).get(effort)
    if not me:
        return None
    best = None
    for m, levels in table.items():
        for e, (c, s) in levels.items():
            if (m, e) != (model, effort) and c <= me[0] and s >= me[1] and (c < me[0] or s > me[1]) and (not best or (s, -c) > (best[2], -best[3])):
                best = (m, e, s, c)
    return best


def bench_path(config=None):
    """사용자가 갱신한 벤치마크가 대응표 옆에 있으면 그것을, 없으면 번들 값을 쓴다."""
    user = (Path(config) if config else config_path()).parent / "benchmarks.json"
    return safe_path(user) if user.exists() or user.is_symlink() else BENCH


# 과거 사용자 벤치마크의 짧은 이름을 그 당시의 정확한 모델 ID로 해석한다.
# 버전을 알 수 없는 임의의 별칭은 최신 버전으로 추측하지 않는다.
LEGACY_BENCHMARK_IDS = {"luna": "gpt-6-luna", "terra": "gpt-6.1-terra"}


def canonicalize_benchmark(bench):
    normalized = copy.deepcopy(bench)
    if "openai" not in normalized.get("providers", {}):
        return normalized
    mapping = dict(LEGACY_BENCHMARK_IDS)
    if "sol" in normalized["providers"]["openai"] or "sol" in normalized.get("tiers", {}).get("openai", []):
        if "GPT-6.1 Sol" not in normalized.get("source", ""):
            raise ValueError("sol 벤치마크 별칭의 버전을 확인할 수 없습니다. 원본 출처와 버전을 명시하세요")
        mapping["sol"] = "gpt-6.1-sol"
    models = normalized["providers"]["openai"]
    for alias, full in mapping.items():
        if alias not in models:
            continue
        if full in models:
            raise ValueError(f"동일 모델 ID 중복: {alias} / {full}")
        models[full] = models.pop(alias)
    if "openai" in normalized.get("tiers", {}):
        normalized["tiers"]["openai"] = [mapping.get(m, m) for m in normalized["tiers"]["openai"]]
    return normalized


def _versioned_family(model):
    """명시적인 모델 ID만 비교한다. 미확인 별칭은 버전을 추측하지 않는다."""
    match = re.fullmatch(r"gpt-(\d+)(?:\.(\d+))?-(sol|terra|luna)", model)
    if not match:
        return None
    return (match.group(3), int(match.group(1)), int(match.group(2) or 0))


def _prefer_newer_release(candidate, preferred):
    """번들 릴리스가 레거시 벤치마크 후보보다 새 버전이면 보존한다."""
    old, new = _versioned_family(candidate["model"]), _versioned_family(preferred["model"])
    if old and new and old[0] == new[0] and new[1:] > old[1:]:
        return copy.deepcopy(preferred)
    return candidate


def derive(data, bench):
    """벤치마크에서 standard·economy 모드를 도출한다.

    standard: light는 경량 모델 low, top은 최상위 모델 medium, standard는 상위 모델 medium.
              칸이 경계선 밖이면 같은 모델 effort를 high까지 올려 보고, 그래도 밖이면 대체 칸을 쓴다.
    economy:  standard 티어만 한 단계 낮춘다(같은 모델 effort 한 단계 아래, 경계선 밖이면 대체 칸).
    """
    bench = canonicalize_benchmark(bench)
    modes = {"standard": {"providers": {}}, "economy": {"providers": {}}}
    for prov, (light, mid, top) in bench["tiers"].items():
        order = data["efforts"][prov]

        def on_frontier(model, effort):
            if not bench["providers"].get(prov, {}).get(model, {}).get(effort):
                raise ValueError("벤치마크에 필요한 모델 및 effort 칸이 없습니다")
            d = dominated(bench, prov, model, effort)
            return {"model": d[0], "effort": d[1]} if d else {"model": model, "effort": effort}

        std = None
        for e in order[order.index("medium"):order.index("high") + 1]:
            if bench["providers"].get(prov, {}).get(mid, {}).get(e) and not dominated(bench, prov, mid, e):
                std = {"model": mid, "effort": e}
                break
        std = std or on_frontier(mid, "medium")
        lower = order[max(order.index(std["effort"]) - 1, 0)]
        base = {"light": on_frontier(light, "low"), "top": on_frontier(top, "medium")}
        # 오래된 벤치마크로 최신 안정 버전을 하향하지 않는다.
        # 실제 호스트 적용 가능성과 사용자 승인은 스킬에서 확인한다.
        release_default = load(DEFAULTS)["modes"]["standard"]["providers"].get(prov, {}).get("top")
        current = data.get("modes", {}).get("standard", {}).get("providers", {}).get(prov, {}).get("top")
        for preferred in (release_default, current):
            if preferred:
                base["top"] = _prefer_newer_release(base["top"], preferred)
        modes["standard"]["providers"][prov] = {**base, "standard": std}
        modes["economy"]["providers"][prov] = {**base, "standard": on_frontier(std["model"], lower)}
    for name, mode in modes.items():
        for tier, cell in mode["providers"].get("openai", {}).items():
            if cell["model"] in LEGACY_BENCHMARK_IDS or cell["model"] == "sol":
                raise ValueError(f"{name}.openai.{tier}: 짧은 모델 별칭이 다시 생성됐습니다")
    return modes


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


def validate(data, bench=None):
    errors, warnings = [], []
    if data.get("active") not in data.get("modes", {}):
        errors.append(f"active 모드가 modes에 없음: {data.get('active')}")
    for mode in data.get("modes", {}):
        try:
            table = resolve(data, mode)
        except ValueError as e:
            errors.append(str(e))
            continue
        if not table:
            errors.append(f"{mode}: providers가 비어 있음")
        for prov, tiers in table.items():
            allowed = data.get("efforts", {}).get(prov)
            for tier in TIERS:
                cell = tiers.get(tier)
                if not cell or not cell.get("model") or not cell.get("effort"):
                    errors.append(f"{mode}.{prov}.{tier}: model·effort 누락")
                    continue
                if allowed and cell["effort"] not in allowed:
                    errors.append(f"{mode}.{prov}.{tier}: 허용되지 않은 effort {cell['effort']}")
                if mode in ("standard", "economy") and prov == "openai" and cell["model"] in ("luna", "terra", "sol"):
                    warnings.append(f"{mode}.{prov}.{tier}: 과거의 짧은 별칭 {cell['model']} (Codex 모델 ID 대조 및 전환 필요)")
                d = bench and dominated(bench, prov, cell["model"], cell["effort"])
                if d:
                    warnings.append(
                        f"{mode}.{prov}.{tier}: {cell['model']} {cell['effort']}는 경계선 밖 "
                        f"({d[0]} {d[1]}가 같거나 싸고 점수 {d[2]}로 같거나 높음)")
            extra = set(tiers) - set(TIERS)
            if extra:
                errors.append(f"{mode}.{prov}: 알 수 없는 티어 {sorted(extra)}")
    return errors, warnings


def plan(data, mode, prov):
    table = resolve(data, mode).get(prov)
    if not table:
        raise ValueError(f"{mode} 모드에 {prov} 대응표가 없음")
    rows = ["| 티어 | 맡는 일 | 모델 | effort |", "|---|---|---|---|"]
    for t in TIERS:
        rows.append(f"| {t} | {data['tiers'][t]} | {table[t]['model']} | {table[t]['effort']} |")
    return "\n".join(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="route_mode", formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="예시:\n  route_mode list\n  route_mode plan --provider anthropic\n  route_mode update economy --set anthropic.standard=sonnet:high\n  route_mode derive --save")
    ap.add_argument("--config", help="대응표 경로 (기본: $ROUTE_MODE_CONFIG 또는 ~/.config/route-mode/modes.json)")
    ap.add_argument("--bench", help="비교할 벤치마크 후보 파일 경로")
    sub = ap.add_subparsers(dest="cmd")
    status = sub.add_parser("status", help="활성 모드와 목표 대응표 확인 (읽기 전용)")
    status.add_argument("--provider")
    status.add_argument("--host")
    status.add_argument("--rule-file")
    sub.add_parser("path", help="대응표 경로 확인")
    sub.add_parser("validate", help="대응표 검사")
    p = sub.add_parser("plan", help="공급자별 목표 대응표 확인")
    p.add_argument("--provider", required=True)
    p.add_argument("--mode")
    sub.add_parser("list", help="모드 목록과 활성 모드 확인")
    u = sub.add_parser("use", help="활성 모드 변경 (승인 필요)")
    u.add_argument("mode")
    a = sub.add_parser("add", help="사용자 모드 추가 (승인 필요)")
    a.add_argument("name")
    a.add_argument("--extends", required=True)
    a.add_argument("--description", default="")
    a.add_argument("--set", action="append", default=[], metavar="PROVIDER.TIER=MODEL:EFFORT")
    u2 = sub.add_parser("update", help="기존 모드의 지정 칸·설명 변경 (승인 필요)")
    u2.add_argument("mode")
    u2.add_argument("--set", action="append", default=[], metavar="PROVIDER.TIER=MODEL:EFFORT")
    u2.add_argument("--unset", action="append", default=[], metavar="PROVIDER.TIER")
    u2.add_argument("--description")
    d = sub.add_parser("derive", help="벤치마크로 기본 모드 비교 (--save 승인 필요)")
    d.add_argument("--save", action="store_true", help="도출한 두 모드를 대응표에 저장")
    r = sub.add_parser("rule", help="사용자 지침 파일의 위임 규칙 블록 관리 (on/off 승인 필요)")
    r.add_argument("action", choices=["on", "off", "status"])
    r.add_argument("--file", required=True, help="호스트의 사용자 수준 지침 파일")
    r.add_argument("--host", default="unknown", help="적용 기록 이름 (예: claude-code)")
    r.add_argument("--prefix", default="tier-", help="위임 대상 이름 접두어 (Hermes 선택지는 빈 문자열)")
    args = ap.parse_args(argv)
    if args.cmd is None:
        args.cmd = "status"
        args.provider = args.host = args.rule_file = None

    if args.bench and (args.cmd != "derive" or args.save):
        ap.error("--bench는 읽기 전용 derive 후보 비교에만 사용할 수 있습니다")

    if args.cmd == "rule":
        try:
            print(rule_apply(args.file, args.action, args.host, args.prefix, args.config))
        except ValueError as e:
            print("ERROR", e, file=sys.stderr)
            return 1
        return 0

    data = load(args.config)
    bp = safe_path(args.bench) if args.bench else bench_path(args.config)
    bench = canonicalize_benchmark(read_json(bp)) if bp.exists() else None

    if args.cmd == "derive":
        if not bench or "tiers" not in bench:
            print("ERROR 벤치마크 파일에 tiers가 없음", file=sys.stderr)
            return 1
        derived = derive(data, bench)
        print(f"벤치마크: {bp}\n출처: {bench.get('source', '?')}")
        changed = False
        for mode, m in derived.items():
            for prov, tiers in m["providers"].items():
                for t in TIERS:
                    new = tiers[t]
                    old = data["modes"].get(mode, {}).get("providers", {}).get(prov, {}).get(t)
                    mark = "" if old == new else f"  (현재 {old['model']} {old['effort']})" if old else "  (새 칸)"
                    if f"{prov}.{t}" in data["modes"].get(mode, {}).get("overrides", {}):
                        mark += "  (사용자 override 보존)"
                    changed |= old != new
                    print(f"{mode:9} {prov:10} {t:9} {new['model']} {new['effort']}{mark}")
        if not changed:
            print("현재 대응표와 같음")
        if args.save:
            new = copy.deepcopy(data)
            for mode, m in derived.items():
                target = new["modes"].setdefault(mode, {"description": ""})
                for prov, tiers in m["providers"].items():
                    for tier, cell in tiers.items():
                        if f"{prov}.{tier}" not in target.get("overrides", {}):
                            target.setdefault("providers", {}).setdefault(prov, {})[tier] = cell
            errors, _ = validate(new, bench)
            if errors:
                for e in errors:
                    print("ERROR", e)
                return 1
            backup_config(args.config)
            print("saved", save(new, args.config))
        return 0

    if args.cmd == "status":
        print(f"active: {data['active']}")
        errors, warnings = validate(data, bench)
        print("mapping:", "invalid" if errors else "valid")
        for message in errors + warnings:
            print(message)
        if errors:
            return 1
        providers = resolve(data, data["active"])
        for provider in ([args.provider] if args.provider else providers):
            print(f"\nprovider: {provider}\n{plan(data, data['active'], provider)}")
        if args.host:
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.host):
                raise ValueError("잘못된 호스트 이름")
            record = safe_path(safe_path(args.config or config_path()).parent / "applied" / f"{args.host}.json")
            print("application record:", "present" if record.exists() else "absent")
        if args.rule_file:
            print("managed rule marker:", rule_apply(args.rule_file, "status", args.host or "unknown"))
        print("profile files: unverified\nprofile load: unverified\nselection rule: unverified")
        for tier in TIERS:
            print(f"{tier} effective model/effort: unverified")
        return 0
    elif args.cmd == "path":
        p = Path(args.config) if args.config else config_path()
        print(f"{p} ({'있음' if p.exists() else '없음, 기본 대응표 사용'})")
    elif args.cmd == "list":
        for name, m in data["modes"].items():
            mark = "*" if name == data["active"] else " "
            ext = f" (extends {m['extends']})" if m.get("extends") else ""
            print(f"{mark} {name}{ext}: {m.get('description', '')}")
    elif args.cmd == "validate":
        errors, warnings = validate(data, bench)
        for w in warnings:
            print("WARN", w)
        for e in errors:
            print("ERROR", e)
        print("OK" if not errors else f"FAIL {len(errors)}")
        return 1 if errors else 0
    elif args.cmd == "plan":
        print(plan(data, args.mode or data["active"], args.provider))
    elif args.cmd in ("use", "add", "update"):
        new = copy.deepcopy(data)
        if args.cmd == "use":
            if args.mode not in new["modes"]:
                print(f"ERROR 없는 모드: {args.mode}", file=sys.stderr)
                return 1
            new["active"] = args.mode
        elif args.cmd == "update":
            new = update_mode(data, args.mode, args.set, args.unset, args.description, bench)
        else:
            if args.name in new["modes"]:
                print(f"ERROR 이미 있는 모드: {args.name}", file=sys.stderr)
                return 1
            mode = {"extends": args.extends, "description": args.description, "providers": {}}
            for s in args.set:
                key, _, val = s.partition("=")
                prov, _, tier = key.partition(".")
                model, _, effort = val.partition(":")
                if not (prov and tier and model and effort):
                    print(f"ERROR --set 형식은 PROVIDER.TIER=MODEL:EFFORT: {s}", file=sys.stderr)
                    return 1
                mode["providers"].setdefault(prov, {})[tier] = {"model": model, "effort": effort}
            new["modes"][args.name] = mode
        errors, warnings = validate(new, bench)
        for w in warnings:
            print("WARN", w)
        if errors:
            for e in errors:
                print("ERROR", e)
            return 1
        if args.cmd in ("use", "add", "update"):
            backup_config(args.config)
        print("saved", save(new, args.config))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, TypeError, KeyError, AttributeError):
        print("ERROR 설정 또는 경로를 안전하게 처리하지 못했습니다", file=sys.stderr)
        sys.exit(1)
