#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value or "workspace"


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def state_root() -> Path:
    custom = os.environ.get("TIGERKIT_STATE_ROOT")
    if custom:
        return Path(custom).expanduser()
    return Path.home() / ".tigerkit"


def abs_dir(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def git(*args: str, cwd: Path) -> str | None:
    result = subprocess.run(["git", *args], cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def resolve_repo_root(start: str | None) -> Path:
    cwd = abs_dir(start or os.getcwd())
    repo = git("rev-parse", "--show-toplevel", cwd=cwd)
    return abs_dir(repo) if repo else cwd


def repo_key(repo_root: Path) -> str:
    return f"{slugify(repo_root.name)}--{sha8(str(repo_root))}"


def scope_key(repo_root: Path) -> str:
    branch = git("branch", "--show-current", cwd=repo_root)
    if branch:
        return slugify(branch)
    return f"workspace-{slugify(repo_root.name)}--{sha8(str(repo_root))}"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent), prefix=".tmp-") as tmp:
        tmp.write(text)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    Path(temp_name).replace(path)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def next_gap_id() -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rand = hashlib.sha256(f"{stamp}-{os.getpid()}-{os.urandom(8).hex()}".encode()).hexdigest()[:4].upper()
    return f"GAP-{stamp}-{rand}"


def cmd_gap_paths(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    root = state_root()
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "gapDir": str(gap_dir),
        "currentPath": str(gap_dir / "current.md"),
        "branchStatePath": str(root / "repos" / repo_key_value / "branches" / scope_key_value / "branch-state.json"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_write_gap(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    root = state_root()
    content = Path(args.report_file).read_text(encoding="utf-8") if args.report_file else sys.stdin.read()
    if not content.strip():
        raise SystemExit("write-gap requires non-empty report content")
    gap_id = args.gap_id or next_gap_id()
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    report_path = gap_dir / f"{gap_id}.md"
    current_path = gap_dir / "current.md"
    branch_state_path = root / "repos" / repo_key_value / "branches" / scope_key_value / "branch-state.json"
    atomic_write(report_path, content)
    atomic_write(current_path, content)
    branch_state = load_json(branch_state_path, {})
    branch_state.update({
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "lastGapRunId": gap_id,
        "lastGapRunPath": str(report_path),
        "updatedAt": now_iso(),
    })
    atomic_write_json(branch_state_path, branch_state)
    print(json.dumps({
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "gapId": gap_id,
        "reportPath": str(report_path),
        "currentPath": str(current_path),
        "branchStatePath": str(branch_state_path),
    }, ensure_ascii=False, indent=2))
    return 0


# ---- loop-spec helpers -------------------------------------------------
LOOP_MOTIFS = {
    "bugfix": "reproduce-diagnose-patch-verify",
    "refactor": "inventory-batch-transform-verify",
    "flaky-test": "repeat-trace-classify-patch-stress",
}
VALID_LOOP_TYPES = {"bugfix", "refactor", "flaky-test", "unknown"}
VALID_MOTIFS = set(LOOP_MOTIFS.values())
SECRET_NAME_RE = re.compile(r"(^|[._/-])(env|secret|secrets|credential|credentials|token|tokens|key|keys|passwd|password)([._/-]|$)", re.I)
MAX_HASH_BYTES = 256_000
SECRET_VALUE_RE = re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd)\s*[:=]\s*([^\s]+)")


def git_bytes(*args: str, cwd: Path) -> bytes | None:
    result = subprocess.run(["git", *args], cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def git_lines_z(*args: str, cwd: Path) -> list[str]:
    data = git_bytes(*args, cwd=cwd)
    if data is None:
        return []
    return [item.decode("utf-8", "replace") for item in data.split(b"\0") if item]


def next_loop_spec_id(name: str | None = None) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rand = hashlib.sha256(f"loop-{stamp}-{os.getpid()}-{os.urandom(8).hex()}".encode()).hexdigest()[:4].upper()
    prefix = slugify(name) if name else "loop-spec"
    return f"{prefix}-{stamp}-{rand}"


def loop_spec_dir(repo_root: Path, spec_id: str | None = None) -> Path:
    base = state_root() / "repos" / repo_key(repo_root) / "branches" / scope_key(repo_root) / "loop-specs"
    return base / spec_id if spec_id else base


def ensure_state_root_outside_repo(repo_root: Path) -> None:
    root = state_root().expanduser().resolve()
    try:
        root.relative_to(repo_root.resolve())
    except ValueError:
        return
    raise SystemExit("loop-spec state root must be outside the project repository")


def sanitize_task_text(task: str) -> str:
    return SECRET_VALUE_RE.sub(lambda m: f"{m.group(1)}=<redacted>", task)


def is_secretish(path: str) -> bool:
    lowered = path.lower()
    return bool(SECRET_NAME_RE.search(lowered)) or lowered.endswith((".pem", ".p12", ".pfx", ".key"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def safe_file_hash(path: Path) -> tuple[str | None, str | None]:
    try:
        if not path.is_file() or path.is_symlink():
            return None, "unsupported-file-type"
        if is_secretish(str(path)):
            return None, "secret-path"
        size = path.stat().st_size
        if size > MAX_HASH_BYTES:
            return None, "size-limit"
        return sha256_bytes(path.read_bytes()), None
    except Exception:
        return None, "read-error"


def collect_changed_paths(repo_root: Path) -> tuple[list[dict[str, Any]], bool]:
    partial = False
    records: dict[str, dict[str, Any]] = {}
    for item in git_lines_z("diff", "--no-ext-diff", "--name-status", "-z", "HEAD", cwd=repo_root):
        # NUL name-status output alternates status/path for simple changes. Rename records may be imperfect;
        # this scanner records metadata only and never raw diff content.
        if item and not re.match(r"^[A-Z][0-9]*$", item):
            records[item] = {"path": item, "status": "changed"}
    numstat_data = git_bytes("diff", "--no-ext-diff", "--numstat", "-z", "HEAD", cwd=repo_root)
    if numstat_data:
        for raw in numstat_data.split(b"\0"):
            if not raw:
                continue
            parts = raw.decode("utf-8", "replace").split("\t")
            if len(parts) >= 3:
                added, deleted, path = parts[0], parts[1], parts[2]
                rec = records.setdefault(path, {"path": path, "status": "changed"})
                rec["added"] = added
                rec["deleted"] = deleted
    for path in git_lines_z("ls-files", "--others", "--exclude-standard", "-z", cwd=repo_root):
        records.setdefault(path, {"path": path, "status": "untracked"})
    for rel, rec in list(records.items()):
        digest, reason = safe_file_hash(repo_root / rel)
        if digest:
            rec["contentHash"] = digest
        elif reason:
            rec["hashExcludedReason"] = reason
            partial = True
    return [records[k] for k in sorted(records)], partial


def scan_capabilities(repo_root: Path, task: str = "") -> dict[str, Any]:
    package_json = repo_root / "package.json"
    scripts: dict[str, str] = {}
    deps: dict[str, str] = {}
    package_manager = "yarn" if package_json.exists() else "unknown"
    if (repo_root / "yarn.lock").exists():
        package_manager = "yarn"
    elif (repo_root / "pnpm-lock.yaml").exists():
        package_manager = "pnpm"
    elif (repo_root / "package-lock.json").exists():
        package_manager = "npm"
    if package_json.exists():
        try:
            pkg = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = {k: str(v) for k, v in (pkg.get("scripts") or {}).items()}
            for field in ("dependencies", "devDependencies", "peerDependencies"):
                deps.update({k: str(v) for k, v in (pkg.get(field) or {}).items()})
            pm = pkg.get("packageManager")
            if isinstance(pm, str):
                package_manager = pm.split("@")[0]
        except Exception:
            pass
    def has_dep(name: str) -> bool:
        return name in deps or any(name in s for s in scripts.values())
    commands: dict[str, Any] = {}
    def add_cmd(key: str, script_name: str | None, run: str | None):
        commands[key] = {
            "run": run,
            "discovery": {"status": "verified" if run else "unresolved", "source": f"package.json#scripts.{script_name}" if run and script_name else "repository-scan"},
            "execution": {"status": "unprobed" if run else "not-applicable", "reason": "default-mode-is-read-only" if run else "command-not-resolved"},
        }
    type_script = next((s for s in ("type-check", "typecheck", "tsc") if s in scripts), None)
    test_script = next((s for s in ("test", "vitest", "jest") if s in scripts), None)
    lint_script = next((s for s in ("lint", "eslint") if s in scripts), None)
    build_script = "build" if "build" in scripts else None
    runner = package_manager if package_manager in {"yarn", "pnpm", "npm"} else "yarn"
    add_cmd("typecheck", type_script, f"{runner} {type_script}" if type_script else None)
    add_cmd("unit", test_script, f"{runner} {test_script}" if test_script else None)
    add_cmd("lint", lint_script, f"{runner} {lint_script}" if lint_script else None)
    add_cmd("build", build_script, f"{runner} {build_script}" if build_script else None)
    e2e_script = next((s for s in scripts if any(w in s.lower() for w in ("e2e", "playwright", "cypress"))), None)
    add_cmd("targetedE2E", e2e_script, f"{runner} {e2e_script}" if e2e_script else None)
    related_tests = []
    for test_dir in ("test", "tests", "spec", "e2e", "playwright", "cypress"):
        p = repo_root / test_dir
        if p.exists():
            related_tests.append(test_dir)
    return {
        "packageManager": package_manager,
        "framework": "nextjs" if has_dep("next") else "vite" if has_dep("vite") else "react" if has_dep("react") else "unknown",
        "scripts": sorted(scripts.keys()),
        "capabilities": {
            "typescript": (repo_root / "tsconfig.json").exists(),
            "vitest": has_dep("vitest"),
            "jest": has_dep("jest"),
            "playwright": has_dep("@playwright/test") or has_dep("playwright"),
            "cypress": has_dep("cypress"),
            "ci": any((repo_root / p).exists() for p in (".github/workflows", ".gitlab-ci.yml")),
        },
        "commands": commands,
        "relatedTests": related_tests,
    }


def classify_task(task: str, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    t = task.lower()
    if any(w in t for w in ("flaky", "flake", "race", "간헐", "불안정", "타이밍")):
        return "flaky-test"
    if any(w in t for w in ("refactor", "rename", "migration", "migrate", "mechanical", "리팩", "마이그레이션", "일괄")):
        return "refactor"
    if any(w in t for w in ("bug", "fix", "error", "fail", "broken", "버그", "수정", "실패", "오류", "안됨")):
        return "bugfix"
    return "unknown"


def command_resolved(scan: dict[str, Any], key: str) -> bool:
    return bool(scan.get("commands", {}).get(key, {}).get("run"))


def select_recommendation(task_type: str, scan: dict[str, Any], forced_motif: str | None = None) -> tuple[str, str, str, list[str], int, str]:
    unit = command_resolved(scan, "unit")
    typecheck = command_resolved(scan, "typecheck")
    targeted = command_resolved(scan, "targetedE2E") or unit
    blockers: list[str] = []
    if forced_motif:
        if forced_motif not in VALID_MOTIFS:
            raise SystemExit(f"unsupported motif: {forced_motif}")
        motif = forced_motif
    elif task_type in LOOP_MOTIFS:
        motif = LOOP_MOTIFS[task_type]
    else:
        return "not-recommended", "not-recommended", "manual", ["task-type-unknown-or-manual"], 20, "low"
    if task_type == "flaky-test" and not unit:
        blockers.append("repeat-command-unresolved")
    if task_type == "refactor" and not (unit or typecheck):
        blockers.append("regression-verifier-unresolved")
    if task_type == "bugfix" and not targeted:
        blockers.append("targeted-verifier-unresolved")
    if blockers:
        return motif, "conditional", "incomplete", blockers, 55, "medium"
    return motif, "recommended", "complete", [], 87, "medium"


def targeted_command_ref(task_type: str, scan: dict[str, Any]) -> tuple[str, str]:
    if task_type == "bugfix" and command_resolved(scan, "targetedE2E"):
        return "repository.commands.targetedE2E", "resolved"
    if task_type in {"bugfix", "refactor", "flaky-test"} and command_resolved(scan, "unit"):
        return "repository.commands.unit", "resolved"
    if command_resolved(scan, "typecheck"):
        return "repository.commands.typecheck", "resolved"
    return "repository.commands.targetedE2E", "unresolved"


def context_fingerprint(repo_root: Path, scan: dict[str, Any]) -> dict[str, Any]:
    head = git("rev-parse", "HEAD", cwd=repo_root) or "unknown"
    changed, partial = collect_changed_paths(repo_root)
    inputs: list[dict[str, Any]] = [{"headSha": head}, {"changed": changed}]
    for rel in ("package.json", "tsconfig.json", ".github/workflows"):
        p = repo_root / rel
        if p.is_file():
            digest, reason = safe_file_hash(p)
            inputs.append({"path": rel, "contentHash": digest, "hashExcludedReason": reason})
            if reason:
                partial = True
        elif p.is_dir():
            for child in sorted(x for x in p.rglob("*") if x.is_file())[:50]:
                rel_child = str(child.relative_to(repo_root))
                digest, reason = safe_file_hash(child)
                inputs.append({"path": rel_child, "contentHash": digest, "hashExcludedReason": reason})
                if reason:
                    partial = True
    payload = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "headSha": head,
        "dirty": bool(git("status", "--porcelain", cwd=repo_root)),
        "fingerprint": {
            "algorithm": "tigerkit-worktree-v1",
            "value": sha256_bytes(payload),
            "coverage": "partial" if partial else "full",
        },
        "scannedAt": now_iso(),
        "inputs": changed,
    }


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text or any(c in text for c in ":#{}[]&,*?|-<>=!%@`\n") or text.lower() in {"null", "true", "false"}:
        return json.dumps(text, ensure_ascii=False)
    return text


def dump_yaml(value: Any, indent: int = 0) -> str:
    sp = " " * indent
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.append(dump_yaml(v, indent + 2))
            else:
                lines.append(f"{sp}{k}: {yaml_scalar(v)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{sp}[]"
        lines = []
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{sp}-")
                lines.append(dump_yaml(item, indent + 2))
            elif isinstance(item, list):
                lines.append(f"{sp}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{sp}- {yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{sp}{yaml_scalar(value)}"


def motif_defaults(motif: str) -> tuple[str, dict[str, Any], dict[str, Any], list[str]]:
    if motif == "inventory-batch-transform-verify":
        return "fresh-per-batch", {"maxBatches": 12, "sameFailureLimit": 2}, {"batchSize": 5, "fullVerificationEveryBatches": 3}, ["public-export-change", "dependency-change", "snapshot-update", "inventory-query-weakening", "unrelated-change"]
    if motif == "repeat-trace-classify-patch-stress":
        return "retain-until-failure-class-changes", {"maxIterations": 4, "sameFailureLimit": 2}, {"initialRepeatCount": 20, "stressRepeatCount": 50}, ["retry-increase", "timeout-increase", "fixed-sleep", "test-skip", "assertion-or-selector-weakening"]
    return "retain-until-hypothesis-reset", {"maxIterations": 4, "sameFailureLimit": 2}, {}, ["snapshot-update", "dependency-change", "test-skip", "assertion-weakening", "fixed-sleep", "unrelated-change"]


def build_loop_spec(repo_root: Path, task: str, args: argparse.Namespace) -> tuple[dict[str, Any], Path | None]:
    ensure_state_root_outside_repo(repo_root)
    task = sanitize_task_text(task)
    task_type = classify_task(task, args.type)
    if args.motif and task_type != "unknown" and args.motif != LOOP_MOTIFS.get(task_type):
        raise SystemExit("--type and --motif are incompatible")
    scan = scan_capabilities(repo_root, task)
    motif, applicability, readiness, blockers, fit, confidence = select_recommendation(task_type, scan, args.motif)
    spec_id = next_loop_spec_id(args.name)
    context = context_fingerprint(repo_root, scan)
    context_policy, budget, params, forbids = motif_defaults(motif)
    command_ref, command_resolution = targeted_command_ref(task_type, scan)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    reasons = [
        {"value": f"task-type-{task_type}", "provenance": "declared" if args.type else "assumed", "source": "--type" if args.type else "task-classifier"},
        {"value": f"package-manager-{scan['packageManager']}", "provenance": "verified", "source": "package.json-or-lockfile"},
    ]
    if scan.get("relatedTests"):
        reasons.append({"value": "test-directories-detected", "provenance": "verified", "source": ",".join(scan["relatedTests"])})
    spec = {
        "apiVersion": "tigerkit.dev/v1alpha1",
        "kind": "LoopSpec",
        "metadata": {
            "id": spec_id,
            "name": args.name or spec_id,
            "generatedAt": now_iso(),
            "tigerkitVersion": "0.x",
            "schemaVersion": "v1alpha1",
            "motifCatalogVersion": "v1",
        },
        "source": {"task": task, "origin": "slash-command"},
        "worktree": {"repositoryId": repo_key_value, "scopeId": scope_key_value, "branch": git("branch", "--show-current", cwd=repo_root) or "detached-or-workspace"},
        "context": context,
        "task": {"type": task_type, "risk": "medium", "properties": {"reproducibility": "medium", "oracleStrength": "high" if scan.get("commands", {}).get("unit", {}).get("run") else "unresolved", "expectedScope": "local", "humanJudgmentDependency": "low"}},
        "recommendation": {"motif": motif, "applicability": applicability, "fitScore": fit, "confidence": confidence, "reasons": reasons, "alternatives": []},
        "readiness": {"status": readiness, "blockers": blockers},
        "repository": {"packageManager": scan["packageManager"], "framework": scan["framework"], "capabilities": scan["capabilities"], "commands": scan["commands"]},
        "loop": {"contextPolicy": context_policy, "parameters": params, "steps": [
            {"id": "reproduce" if motif != "inventory-batch-transform-verify" else "inventory", "type": "agent", "objective": "Confirm the working set or failing reproduction."},
            {"id": "patch" if motif != "inventory-batch-transform-verify" else "transform", "type": "agent", "objective": "Apply the smallest safe change for the selected batch or hypothesis."},
            {"id": "targeted-verification", "type": "command", "commandRef": command_ref, "required": True, "resolution": command_resolution},
            {"id": "regression-verification", "type": "command", "commandRefs": ["repository.commands.typecheck", "repository.commands.unit"]},
            {"id": "review", "type": "manual-checkpoint", "checks": ["no-test-weakening", "no-unrelated-changes", "root-cause-addressed"]},
        ]},
        "guards": {"maxChangedFiles": 5, "forbid": forbids},
        "budget": budget,
        "success": {"all": ["targeted-verification-passed", "regression-verification-passed", "diff-review-passed"]},
        "escalate": {"any": ["reproduction-not-obtained", "public-api-change-required", "same-failure-limit-reached", "required-verifier-unresolved"]},
        "evidence": {"required": ["root-cause", "before-after-proof", "changed-files", "verification-log"]},
    }
    path = None if args.no_write else loop_spec_dir(repo_root, spec_id) / "spec.yaml"
    return spec, path


def render_loop_spec_summary(spec: dict[str, Any], path: Path | None) -> str:
    rec = spec["recommendation"]
    readiness = spec["readiness"]
    lines = [
        f"Loop strategy: {rec['motif']}",
        f"Applicability: {rec['applicability']}",
        f"Readiness: {readiness['status']}",
        f"Fit score: {rec['fitScore']}/100",
        f"Confidence: {rec['confidence']}",
        f"Worktree: {spec['worktree']['branch']}",
        "",
        "Why",
    ]
    for reason in rec.get("reasons", []):
        lines.append(f"  - {reason['value']} ({reason['provenance']})")
    lines += ["", "Blockers"]
    for blocker in readiness.get("blockers") or ["NONE"]:
        lines.append(f"  - {blocker}")
    lines += ["", "Guards"]
    for guard in spec["guards"]["forbid"]:
        lines.append(f"  - No {guard}")
    lines += ["", "Saved"]
    lines.append(f"  {path if path else 'NONE (--no-write)'}")
    lines += ["", "Write receipt", f"  changed: {path if path else 'NONE'}", "  source tree changed: no"]
    return "\n".join(lines)


def update_loop_branch_state(repo_root: Path, spec: dict[str, Any], path: Path) -> None:
    branch_state_path = state_root() / "repos" / repo_key(repo_root) / "branches" / scope_key(repo_root) / "branch-state.json"
    branch_state = load_json(branch_state_path, {})
    branch_state.update({
        "repoKey": repo_key(repo_root),
        "scopeKey": scope_key(repo_root),
        "lastLoopSpecId": spec["metadata"]["id"],
        "lastLoopSpecPath": str(path),
        "updatedAt": now_iso(),
    })
    atomic_write_json(branch_state_path, branch_state)


def cmd_loop_spec(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    task_args = list(args.task or [])
    if task_args and task_args[0] == "validate":
        if len(task_args) != 2:
            raise SystemExit("Usage: loop-spec validate <spec-id-or-path>")
        args.spec = task_args[1]
        return cmd_loop_spec_validate(args, repo_root)
    task = " ".join(task_args).strip()
    if not task:
        raise SystemExit("/tk:loop-spec generate requires a task. Usage: loop-spec '<task>'")
    spec, path = build_loop_spec(repo_root, task, args)
    if path:
        atomic_write(path, dump_yaml(spec) + "\n")
        update_loop_branch_state(repo_root, spec, path)
    print(render_loop_spec_summary(spec, path))
    if args.explain:
        print("\nExplain")
        print(f"  context fingerprint coverage: {spec['context']['fingerprint']['coverage']}")
        print("  selector mode: rules")
        print("  command discovery is separated from execution status")
    return 0


def resolve_loop_spec_path(repo_root: Path, spec_id_or_path: str) -> Path:
    p = Path(spec_id_or_path).expanduser()
    if p.exists() or p.is_absolute() or "/" in spec_id_or_path:
        return p.resolve()
    return loop_spec_dir(repo_root, spec_id_or_path) / "spec.yaml"


def read_yamlish_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        raise SystemExit(f"cannot read LoopSpec: {path}: {exc}") from exc


def extract_yaml_string(text: str, key: str) -> str | None:
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    if not m:
        return None
    raw = m.group(1).strip()
    if raw.startswith('"') and raw.endswith('"'):
        try:
            return json.loads(raw)
        except Exception:
            return raw.strip('"')
    return None if raw == "null" else raw


def cmd_loop_spec_validate(args: argparse.Namespace, repo_root: Path) -> int:
    path = resolve_loop_spec_path(repo_root, args.spec)
    text = read_yamlish_text(path)
    required_tokens = ["apiVersion:", "kind: LoopSpec", "metadata:", "recommendation:", "readiness:", "context:", "fingerprint:"]
    missing = [tok for tok in required_tokens if tok not in text]
    schema = "invalid" if missing else "valid"
    stored_head = extract_yaml_string(text, "headSha")
    current_head = git("rev-parse", "HEAD", cwd=repo_root)
    context = "unknown"
    if stored_head and current_head:
        context = "current" if stored_head == current_head else "stale"
    print(f"LoopSpec: {path}")
    print(f"Schema: {schema}")
    print(f"Context: {context}")
    if missing:
        print("Missing")
        for item in missing:
            print(f"  - {item}")
    if context == "stale":
        print("Recommendation")
        print("  Regenerate with /tk:loop-spec <task>")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TigerKit generated state helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    p_paths = sub.add_parser("gap-paths", help="Print active gap state paths")
    p_paths.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_paths.set_defaults(func=cmd_gap_paths)

    p_write = sub.add_parser("write-gap", help="Write a gap report into ~/.tigerkit")
    p_write.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_write.add_argument("--gap-id", help="Explicit GAP id", default=None)
    p_write.add_argument("--report-file", help="Read report content from file instead of stdin", default=None)
    p_write.set_defaults(func=cmd_write_gap)

    p_loop = sub.add_parser("loop-spec", help="Generate or validate a worktree-scoped LoopSpec")
    p_loop.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_loop.add_argument("--explain", action="store_true", help="Include expanded explanation in command output")
    p_loop.add_argument("--type", choices=["bugfix", "refactor", "flaky-test"], default=None, help="Override deterministic task classifier")
    p_loop.add_argument("--motif", choices=sorted(VALID_MOTIFS), default=None, help="Force a motif when policy allows it")
    p_loop.add_argument("--name", default=None, help="Human-friendly spec name")
    p_loop.add_argument("--no-write", action="store_true", help="Render recommendation without writing an artifact")
    p_loop.add_argument("task", nargs="*", help="Task description, or: validate <spec-id-or-path>")
    p_loop.set_defaults(func=cmd_loop_spec)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
