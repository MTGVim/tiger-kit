#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
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
LOOP_SPEC_REQUIRED_TOP_LEVEL_KEYS = {"schemaVersion", "specId", "task", "context", "readiness", "scope", "guards", "steps", "verifiers"}
LOOP_SPEC_TOP_LEVEL_KEYS = LOOP_SPEC_REQUIRED_TOP_LEVEL_KEYS | {"blockers", "execution"}
LOOP_SPEC_SCOPE_KEYS = {"modify", "create", "delete", "exclude", "globSemantics", "fingerprintAlgorithm"}
LOOP_SPEC_EXECUTION_KEYS = {"executorRecommendation", "budget", "successConditions", "stopConditions", "escalationConditions"}
LOOP_SPEC_BUDGET_KEYS = {"maxIterations", "maxMinutes"}
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
    motif, applicability, readiness_value, blockers, fit, confidence = select_recommendation(task_type, scan, args.motif)
    readiness = "complete" if readiness_value == "complete" else "blocked"
    spec_id = next_loop_spec_id(args.name)
    context = context_fingerprint(repo_root, scan)
    _, budget, _, forbids = motif_defaults(motif)
    command_ref, command_resolution = targeted_command_ref(task_type, scan)
    verifier_command = scan.get("commands", {}).get(command_ref.rsplit(".", 1)[-1], {}).get("run") or "python3 -m json.tool evals/evals.json >/dev/null"
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    branch = git("branch", "--show-current", cwd=repo_root) or "detached-or-workspace"
    spec: dict[str, Any] = {
        "schemaVersion": "tigerkit.loop-spec/v2",
        "specId": spec_id,
        "task": {"title": task, "type": task_type, "description": task},
        "context": {"repoKey": repo_key_value, "scopeKey": scope_key_value, "branch": branch, "headSha": context["headSha"], "fingerprint": context["fingerprint"]["value"]},
        "readiness": readiness,
        "blockers": [{"id": item, "reason": item} for item in blockers],
        "scope": {"modify": ["**"], "create": [], "delete": [], "exclude": [".git/**", ".env", "**/*.pem", "**/*.key"], "globSemantics": "tigerkit-glob/v1", "fingerprintAlgorithm": "sha256-path-content-v1"},
        "guards": [{"id": f"guard-{i+1}", "rule": f"No {item}"} for i, item in enumerate(forbids)],
        "steps": [
            {"id": "inspect", "summary": "Inspect the current public surface and choose the smallest safe change."},
            {"id": "patch", "summary": "Edit only declared scope paths."},
            {"id": "verify", "summary": "Run required verifier commands and preserve exact result."}
        ],
        "verifiers": [{"id": "required-validation", "command": verifier_command, "required": True}],
    }
    if readiness == "complete":
        spec["execution"] = {
            "executorRecommendation": "reasoning" if task_type in {"refactor", "flaky-test"} else "fast",
            "budget": {"maxIterations": int(budget.get("maxIterations", 4)), "maxMinutes": 30},
            "successConditions": ["required-verifiers-passed", "scope-clean"],
            "stopConditions": ["same-failure-limit-reached", "budget-exhausted"],
            "escalationConditions": ["scope-expansion-required", "plan-deviation-required", "required-verifier-unresolved", command_resolution],
        }
    path = None if args.no_write else loop_spec_dir(repo_root, spec_id) / "spec.yaml"
    return spec, path


def render_loop_spec_summary(spec: dict[str, Any], path: Path | None) -> str:
    execution = spec.get("execution") or {}
    executor = execution.get("executorRecommendation", "NONE")
    readiness = spec["readiness"]
    lines = [
        f"LoopSpec: {spec['specId']}",
        f"Readiness: {readiness}",
        f"Executor: {executor}",
        f"Worktree: {spec['context'].get('branch', 'workspace')}",
    ]
    if spec.get("blockers"):
        lines += ["", "Blockers"]
        for blocker in spec["blockers"]:
            lines.append(f"  - {blocker['id']}: {blocker['reason']}")
    lines += ["", "Guards"]
    for guard in spec["guards"]:
        lines.append(f"  - {guard['rule']}")
    lines += ["", "Saved"]
    lines.append(f"  {path if path else 'NONE (--no-write)'}")
    lines += ["", "Write receipt", f"  changed: {path if path else 'NONE'}", "  source tree changed: no"]
    if readiness == "complete":
        lines += ["", "Next"]
        lines.append(f"  legacy execute helper: execute {path if path else spec['specId']}")
    return "\n".join(lines)


def update_loop_branch_state(repo_root: Path, spec: dict[str, Any], path: Path) -> None:
    branch_state_path = state_root() / "repos" / repo_key(repo_root) / "branches" / scope_key(repo_root) / "branch-state.json"
    branch_state = load_json(branch_state_path, {})
    branch_state.update({
        "repoKey": repo_key(repo_root),
        "scopeKey": scope_key(repo_root),
        "lastLoopSpecId": spec["specId"],
        "lastLoopSpecPath": str(path),
        "updatedAt": now_iso(),
    })
    atomic_write_json(branch_state_path, branch_state)


def render_loop_spec_usage() -> str:
    return "\n".join([
        "사용법: loop-spec <task>  # legacy helper, active /tk command 아님",
        "또는: loop-spec validate <spec-id-or-path>",
        "",
        "예:",
        '  loop-spec "Fix payment modal scroll bug"',
        "  loop-spec validate <spec-id-or-path>",
    ])


def cmd_loop_spec(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    task_args = list(args.task or [])
    if not task_args:
        print(render_loop_spec_usage())
        return 0
    if task_args and task_args[0] == "validate":
        if len(task_args) != 2:
            print(render_loop_spec_usage())
            return 0
        args.spec = task_args[1]
        return cmd_loop_spec_validate(args, repo_root)
    task = " ".join(task_args).strip()
    if not task:
        print(render_loop_spec_usage())
        return 0
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
    if raw.startswith("'") and raw.endswith("'"):
        return raw.strip("'")
    return None if raw == "null" else raw


def cmd_loop_spec_validate(args: argparse.Namespace, repo_root: Path) -> int:
    path = resolve_loop_spec_path(repo_root, args.spec)
    text = read_yamlish_text(path)
    errors = loop_spec_structure_errors(text)
    schema_version = extract_yaml_string(text, "schemaVersion")
    if schema_version != "tigerkit.loop-spec/v2":
        errors.append("schemaVersion must be tigerkit.loop-spec/v2")
    readiness = extract_yaml_string(text, "readiness")
    if readiness == "complete" and not has_top_level_key(text, "execution"):
        errors.append("missing top-level key: execution")
    if readiness == "blocked" and "executorRecommendation:" in text:
        errors.append("blocked spec must not include executorRecommendation")
    schema = "invalid" if errors else "valid"
    stored_head = extract_yaml_string(text, "headSha")
    current_head = git("rev-parse", "HEAD", cwd=repo_root)
    context = "unknown"
    if stored_head and current_head:
        context = "current" if stored_head == current_head else "stale"
    print(f"LoopSpec: {path}")
    print(f"Schema: {schema}")
    print(f"Context: {context}")
    if errors:
        print("Invalid")
        for item in errors:
            print(f"  - {item}")
    if context == "stale":
        print("Recommendation")
        print("  Re-prepare the spec with a legacy helper or external producer.")
    return 0


def execution_dir(repo_root: Path) -> Path:
    return state_root() / "repos" / repo_key(repo_root) / "branches" / scope_key(repo_root) / "executions"


def next_execution_id() -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"exec-{stamp}-{uuid.uuid4().hex[:8]}"


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def platform_key() -> str:
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform == "darwin":
        return "darwin"
    if sys.platform.startswith("win"):
        return "windows"
    return "unknown"


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def yaml_section(text: str, key: str) -> list[str]:
    m = re.search(rf"^(?P<indent>\s*){re.escape(key)}:\s*$", text, re.M)
    if not m:
        return []
    indent = len(m.group("indent"))
    lines = text[m.end():].splitlines()
    out: list[str] = []
    for line in lines:
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        out.append(line)
    return out


def has_top_level_key(text: str, key: str) -> bool:
    return bool(re.search(rf"^{re.escape(key)}:\s*", text, re.M))


def top_level_keys(text: str) -> set[str]:
    return set(re.findall(r"^([A-Za-z0-9_.-]+):\s*", text, re.M))


def direct_section_keys(lines: list[str]) -> set[str]:
    found: list[tuple[int, str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+):\s*(?:.*)$", stripped)
        if m:
            found.append((len(line) - len(line.lstrip(" ")), m.group(1)))
    if not found:
        return set()
    base = min(indent for indent, _ in found)
    return {key for indent, key in found if indent == base}


def section_has_key(lines: list[str], key: str) -> bool:
    return any(re.match(rf"^{re.escape(key)}:\s*(?:.*)$", line.strip()) for line in lines)


def parse_yaml_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw in {"true", "false"}:
        return raw == "true"
    if raw == "null":
        return None
    if raw.startswith('"') and raw.endswith('"'):
        try:
            return json.loads(raw)
        except Exception:
            return raw.strip('"')
    if raw.startswith("'") and raw.endswith("'"):
        return raw.strip("'")
    if re.fullmatch(r"-?[0-9]+", raw):
        return int(raw)
    return raw


def scalar_from_section(lines: list[str], key: str) -> Any:
    for line in lines:
        m = re.match(rf"^{re.escape(key)}:\s*(.+?)\s*$", line.strip())
        if m:
            return parse_yaml_scalar(m.group(1))
    return None


def scalar_list_from_section(lines: list[str], key: str) -> list[str]:
    result: list[str] = []
    active_indent: int | None = None
    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if re.match(rf"^{re.escape(key)}:\s*$", stripped):
            active_indent = indent
            continue
        if active_indent is None:
            continue
        if stripped and indent <= active_indent:
            break
        item = re.match(r"^-\s+(.+?)\s*$", stripped)
        if item:
            raw = item.group(1)
            try:
                result.append(str(json.loads(raw)) if raw.startswith('"') else raw)
            except Exception:
                result.append(raw.strip("'\""))
    return sorted(set(result))


def object_list_from_section(lines: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in lines:
        stripped = line.strip()
        if stripped == "-":
            if current is not None:
                items.append(current)
            current = {}
            continue
        if current is None:
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.+?)\s*$", stripped)
        if not m:
            continue
        key, raw = m.group(1), m.group(2)
        if raw in {"true", "false"}:
            value: Any = raw == "true"
        elif raw == "null":
            value = None
        elif raw.startswith('"') and raw.endswith('"'):
            try:
                value = json.loads(raw)
            except Exception:
                value = raw.strip('"')
        else:
            value = raw.strip("'")
        current[key] = value
    if current is not None:
        items.append(current)
    return items


def valid_object_list(lines: list[str], required_keys: set[str]) -> bool:
    items = object_list_from_section(lines)
    return bool(items) and all(set(item) == required_keys and all(isinstance(item.get(key), str) and item.get(key) for key in required_keys) for item in items)


def loop_spec_structure_errors(text: str) -> list[str]:
    errors: list[str] = []
    present = top_level_keys(text)
    for key in sorted(present - LOOP_SPEC_TOP_LEVEL_KEYS):
        errors.append(f"unknown top-level key: {key}")
    for key in sorted(LOOP_SPEC_REQUIRED_TOP_LEVEL_KEYS - present):
        errors.append(f"missing top-level key: {key}")
    scope_lines = yaml_section(text, "scope")
    scope_keys = direct_section_keys(scope_lines)
    for key in sorted(scope_keys - LOOP_SPEC_SCOPE_KEYS):
        errors.append(f"unknown scope key: {key}")
    if "scope" in present:
        for key in ("modify", "create", "delete", "exclude"):
            if key not in scope_keys:
                errors.append(f"missing scope key: {key}")
    if "execution" in present:
        execution_lines = yaml_section(text, "execution")
        execution_keys = direct_section_keys(execution_lines)
        for key in sorted(execution_keys - LOOP_SPEC_EXECUTION_KEYS):
            errors.append(f"unknown execution key: {key}")
        budget_lines = yaml_section("\n".join(execution_lines), "budget")
        for key in sorted(direct_section_keys(budget_lines) - LOOP_SPEC_BUDGET_KEYS):
            errors.append(f"unknown budget key: {key}")
    if "guards" in present and not valid_object_list(yaml_section(text, "guards"), {"id", "rule"}):
        errors.append("invalid guards")
    if "steps" in present and not valid_object_list(yaml_section(text, "steps"), {"id", "summary"}):
        errors.append("invalid steps")
    return errors


def has_glob(value: str) -> bool:
    return any(ch in value for ch in "*?[")


def path_matches(path: str, patterns: list[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatch(path, pattern) for pattern in patterns)


def validate_scope(scope: dict[str, list[str]]) -> None:
    for rel in scope["create"] + scope["delete"]:
        if has_glob(rel):
            raise ValueError("invalid_scope_pattern")
        if path_matches(rel, scope["exclude"]):
            raise ValueError("invalid_create_delete_state")


def parse_loop_spec_for_execute(path: Path, repo_root: Path) -> dict[str, Any]:
    text = read_yamlish_text(path)
    if loop_spec_structure_errors(text):
        raise ValueError("invalid_loop_spec")

    def req(key: str) -> str:
        value = extract_yaml_string(text, key)
        if value is None:
            raise ValueError("invalid_loop_spec")
        return value

    schema = req("schemaVersion")
    if schema != "tigerkit.loop-spec/v2":
        raise ValueError("unsupported_loop_spec_schema")
    readiness = req("readiness")
    if readiness == "blocked":
        raise ValueError("blocked_loop_spec")
    if readiness != "complete" or not has_top_level_key(text, "execution"):
        raise ValueError("invalid_loop_spec")
    execution_lines = yaml_section(text, "execution")
    if not section_has_key(execution_lines, "executorRecommendation"):
        raise ValueError("missing_executor_recommendation")
    executor = scalar_from_section(execution_lines, "executorRecommendation")
    if executor not in {"fast", "reasoning"}:
        raise ValueError("invalid_loop_spec")
    for key in ("budget", "successConditions", "stopConditions", "escalationConditions"):
        if not section_has_key(execution_lines, key):
            raise ValueError("invalid_loop_spec")
    budget: dict[str, Any] = {}
    for key in ("maxIterations", "maxMinutes"):
        value = scalar_from_section(yaml_section("\n".join(execution_lines), "budget"), key)
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError("invalid_loop_spec")
            budget[key] = value
    parsed = {
        "path": path,
        "text": text,
        "specId": req("specId"),
        "executor": executor,
        "repoKey": req("repoKey"),
        "scopeKey": req("scopeKey"),
        "headSha": req("headSha"),
        "fingerprint": req("fingerprint"),
        "scope": {"modify": [], "create": [], "delete": [], "exclude": []},
        "verifiers": [],
        "execution": {
            "budget": budget,
            "successConditions": scalar_list_from_section(execution_lines, "successConditions"),
            "stopConditions": scalar_list_from_section(execution_lines, "stopConditions"),
            "escalationConditions": scalar_list_from_section(execution_lines, "escalationConditions"),
        },
    }
    scope_lines = yaml_section(text, "scope")
    if not all(section_has_key(scope_lines, key) for key in ("modify", "create", "delete", "exclude")):
        raise ValueError("invalid_loop_spec")
    parsed["scope"] = {key: scalar_list_from_section(scope_lines, key) for key in ("modify", "create", "delete", "exclude")}
    validate_scope(parsed["scope"])
    parsed["verifiers"] = object_list_from_section(yaml_section(text, "verifiers"))
    if not parsed["verifiers"]:
        raise ValueError("invalid_loop_spec")
    for verifier in parsed["verifiers"]:
        if set(verifier) != {"id", "command", "required"} or not isinstance(verifier.get("id"), str) or not verifier.get("id") or not isinstance(verifier.get("command"), str) or not verifier.get("command") or not isinstance(verifier.get("required"), bool):
            raise ValueError("invalid_loop_spec")
    if parsed["repoKey"] != repo_key(repo_root):
        raise ValueError("repository_identity_mismatch")
    if parsed["scopeKey"] != scope_key(repo_root):
        raise ValueError("worktree_identity_mismatch")
    return parsed


def sorted_dirty_paths(repo_root: Path) -> list[str]:
    out = git("status", "--porcelain", cwd=repo_root)
    if not out:
        return []
    paths = []
    for line in out.splitlines():
        if len(line) > 3:
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            paths.append(path)
    return sorted(set(paths))


def file_signature(path: Path) -> dict[str, Any]:
    try:
        if path.is_symlink():
            return {"kind": "symlink", "target": os.readlink(path)}
        if path.is_file():
            st = path.stat()
            return {"kind": "file", "mode": oct(st.st_mode & 0o777), "sha256": sha256_file(path)}
    except Exception:
        return {"kind": "unreadable"}
    return {"kind": "absent"}


def repo_file_state(repo_root: Path) -> dict[str, dict[str, Any]]:
    paths = set(git_lines_z("ls-files", "-z", cwd=repo_root))
    paths.update(git_lines_z("ls-files", "--others", "--exclude-standard", "-z", cwd=repo_root))
    return {rel: file_signature(repo_root / rel) for rel in sorted(paths)}


def changed_since_baseline(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> tuple[list[str], dict[str, str]]:
    changed: list[str] = []
    operations: dict[str, str] = {}
    for rel in sorted(set(before) | set(after)):
        old = before.get(rel, {"kind": "absent"})
        new = after.get(rel, {"kind": "absent"})
        if old == new:
            continue
        changed.append(rel)
        if old.get("kind") == "absent" and new.get("kind") != "absent":
            operations[rel] = "create"
        elif old.get("kind") != "absent" and new.get("kind") == "absent":
            operations[rel] = "delete"
        else:
            operations[rel] = "modify"
    return changed, operations


def scope_violations(paths: list[str], operations: dict[str, str], scope: dict[str, list[str]]) -> list[dict[str, str]]:
    order = {"create": 0, "modify": 1, "delete": 2}
    violations: list[dict[str, str]] = []
    for rel in paths:
        op = operations[rel]
        violation = None
        if path_matches(rel, scope["exclude"]):
            violation = "excluded"
        elif op == "modify" and not path_matches(rel, scope["modify"]):
            violation = "outside_modify_scope"
        elif op == "create" and rel not in scope["create"]:
            violation = "undeclared_create"
        elif op == "delete" and rel not in scope["delete"]:
            violation = "undeclared_delete"
        if violation:
            violations.append({"path": rel, "operation": op, "violation": violation})
    return sorted(violations, key=lambda item: (item["path"].encode("utf-8"), order[item["operation"]]))


def baseline_capture(repo_root: Path) -> dict[str, Any]:
    return {"headSha": git("rev-parse", "HEAD", cwd=repo_root) or "unknown", "dirtyPaths": sorted_dirty_paths(repo_root)}


def verifier_reason(status: str, exit_code: int | None, reason_code: str | None) -> str:
    if reason_code == "timeout_exceeded" or status == "timed_out":
        return "verifier_timed_out"
    if reason_code == "not_attempted_due_to_budget":
        return "budget_exhausted"
    if reason_code == "not_attempted_due_to_unavailable_tool" or exit_code == 127:
        return "required_verifier_unavailable"
    if status == "error":
        return "verifier_error"
    return "verifier_failed"


def run_verifier(repo_root: Path, verifier: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    command = str(verifier.get("command") or "")
    result = {"id": str(verifier.get("id") or "verifier"), "command": command, "status": "not_run", "exitCode": None}
    if not command:
        result.update({"reasonCode": "not_attempted_due_to_unavailable_tool", "message": "Verifier command is empty."})
        return result
    try:
        proc = subprocess.run(command, cwd=str(repo_root), shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired:
        result.update({"status": "timed_out", "reasonCode": "timeout_exceeded", "message": "Verifier timed out."})
        return result
    except Exception as exc:
        result.update({"status": "error", "reasonCode": "process_start_error", "message": str(exc)})
        return result
    result["exitCode"] = proc.returncode
    if proc.returncode == 127:
        result.update({"status": "not_run", "reasonCode": "not_attempted_due_to_unavailable_tool"})
    else:
        result["status"] = "passed" if proc.returncode == 0 else "failed"
    return result


CLAIMED_REASON_CODES = {"plan_deviation_required", "scope_expansion_required", "executor_capability_mismatch", "scope_violation", "excluded_path_modified", "unapproved_path_created", "unapproved_path_deleted", "claimed_observed_mismatch", "executor_error", "required_tool_unavailable", "verifier_failed", "verifier_error", "verifier_timed_out", "budget_exhausted", "success_condition_not_met", "transient_runtime_failure"}
CLAIMED_VERIFIER_REASON_CODES = {"process_start_error", "environment_error", "harness_error", "timeout_exceeded", "not_attempted_due_to_escalation", "not_attempted_due_to_prior_failure", "not_attempted_due_to_budget", "not_attempted_due_to_unavailable_tool", "not_attempted_due_to_invalid_final_state"}


def is_unique_string_list(value: Any, allowed_values: set[str] | None = None) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and (allowed_values is None or item in allowed_values) for item in value) and len(value) == len(set(value))


def valid_claimed_verifier(item: Any) -> bool:
    if not isinstance(item, dict) or not {"id", "status", "exitCode"} <= set(item) or set(item) - {"id", "status", "exitCode", "reasonCode", "message"}:
        return False
    status = item.get("status")
    if not isinstance(item.get("id"), str) or not item.get("id") or status not in {"passed", "failed", "error", "timed_out", "not_run"}:
        return False
    if item.get("exitCode") is not None and (not isinstance(item.get("exitCode"), int) or isinstance(item.get("exitCode"), bool)):
        return False
    if status in {"passed", "failed"} and "reasonCode" in item:
        return False
    if status in {"error", "timed_out", "not_run"} and item.get("reasonCode") not in CLAIMED_VERIFIER_REASON_CODES:
        return False
    if "message" in item and (not isinstance(item.get("message"), str) or not item.get("message")):
        return False
    return True


def valid_reason_detail(item: Any) -> bool:
    if not isinstance(item, dict) or "code" not in item or set(item) - {"code", "message", "verifierId"}:
        return False
    if item.get("code") not in CLAIMED_REASON_CODES:
        return False
    if "message" in item and (not isinstance(item.get("message"), str) or not item.get("message")):
        return False
    if "verifierId" in item and (not isinstance(item.get("verifierId"), str) or not item.get("verifierId")):
        return False
    return True


def claimed_schema_error(claimed: dict[str, Any], expected_execution_id: str, expected_spec_id: str, expected_executor: str, declared_verifier_ids: set[str] | None = None) -> str | None:
    allowed = {"schemaVersion", "executionId", "specId", "executor", "outcome", "changedPaths", "verifierResults", "reasonCodes", "reasonDetails", "safeToRetry", "cleanupRequired"}
    if set(claimed) - allowed:
        return "unknown field"
    required = allowed
    if not required <= set(claimed):
        return "missing field"
    if claimed.get("schemaVersion") != "tigerkit.executor-claimed-result/v1" or claimed.get("executionId") != expected_execution_id or claimed.get("specId") != expected_spec_id or claimed.get("executor") != expected_executor:
        return "identity mismatch"
    if claimed.get("outcome") not in {"completed", "escalated", "failed"}:
        return "invalid outcome"
    if not is_unique_string_list(claimed.get("changedPaths")):
        return "invalid changedPaths"
    if not isinstance(claimed.get("verifierResults"), list) or not all(valid_claimed_verifier(item) for item in claimed.get("verifierResults")):
        return "invalid verifierResults"
    verifier_ids = [item["id"] for item in claimed.get("verifierResults")]
    if len(verifier_ids) != len(set(verifier_ids)):
        return "invalid verifierResults"
    if declared_verifier_ids is not None and any(verifier_id not in declared_verifier_ids for verifier_id in verifier_ids):
        return "invalid verifierResults"
    if not is_unique_string_list(claimed.get("reasonCodes"), CLAIMED_REASON_CODES):
        return "invalid reasonCodes"
    if not isinstance(claimed.get("reasonDetails"), list) or not all(valid_reason_detail(item) for item in claimed.get("reasonDetails")):
        return "invalid reasonDetails"
    if not isinstance(claimed.get("safeToRetry"), bool) or not isinstance(claimed.get("cleanupRequired"), bool):
        return "invalid retry cleanup flags"
    return None


def parse_claimed_result(text: str, execution_id: str, spec_id: str, executor: str, declared_verifier_ids: set[str] | None = None) -> tuple[dict[str, Any] | None, str | None]:
    candidates: list[str] = []
    stripped = text.strip()
    if stripped.startswith("{"):
        candidates.append(stripped)
    match = re.search(r"\{.*\}", stripped, re.S)
    if match:
        candidates.append(match.group(0))
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except Exception:
            continue
        if isinstance(value, dict):
            error = claimed_schema_error(value, execution_id, spec_id, executor, declared_verifier_ids)
            return (value, None) if error is None else (None, error)
    return None, "missing or malformed claimed-result envelope"


def claimed_verifier_map(claimed: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not claimed:
        return {}
    result = {}
    for item in claimed.get("verifierResults") or []:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result[item["id"]] = item
    return result


def classify_claimed_observed_mismatch(claimed: dict[str, Any] | None, changed_paths: list[str], postflight: list[dict[str, Any]]) -> bool:
    if not claimed:
        return False
    if sorted(set(str(x) for x in claimed.get("changedPaths") or [])) != changed_paths:
        return True
    nonpassed = [v for v in postflight if v.get("status") != "passed"]
    if claimed.get("outcome") == "completed" and nonpassed:
        return True
    if claimed.get("outcome") in {"failed", "escalated"} and not nonpassed:
        return True
    claimed_by_id = claimed_verifier_map(claimed)
    for observed in postflight:
        claimed_v = claimed_by_id.get(observed.get("id"))
        if not claimed_v:
            continue
        claimed_passed = claimed_v.get("status") == "passed"
        observed_passed = observed.get("status") == "passed"
        if claimed_passed != observed_passed:
            return True
    return False


def unique_reason_details(codes: list[str], existing: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    seen: set[tuple[str, str | None]] = set()
    code_set = set(codes)
    for detail in existing or []:
        if not isinstance(detail, dict) or detail.get("code") not in code_set:
            continue
        key = (detail["code"], detail.get("verifierId"))
        if key not in seen:
            seen.add(key)
            details.append({k: v for k, v in detail.items() if k in {"code", "message", "verifierId"}})
    for code in codes:
        key = (code, None)
        if key not in seen:
            seen.add(key)
            details.append({"code": code})
    return details


def recommended_actions(result: str, reasons: list[str], safe_to_retry: bool, cleanup_required: bool, changed_paths: list[str]) -> list[str]:
    mapping = {
        "hard_enforcement_unavailable": "inspect_enforcement_failure",
        "scope_violation": "inspect_scope_violation",
        "excluded_path_modified": "inspect_scope_violation",
        "unapproved_path_created": "inspect_scope_violation",
        "unapproved_path_deleted": "inspect_scope_violation",
        "claimed_observed_mismatch": "review_partial_changes",
        "baseline_dirty_path_modified": "review_partial_changes",
        "executor_error": "retry_execute",
        "required_verifier_unavailable": "restore_required_tool",
        "required_tool_unavailable": "restore_required_tool",
        "verifier_failed": "review_partial_changes",
        "verifier_error": "retry_execute",
        "verifier_timed_out": "retry_execute",
        "budget_exhausted": "retry_execute",
    }
    actions = []
    for reason in reasons:
        action = mapping.get(reason)
        if action and action not in actions:
            actions.append(action)
    if not safe_to_retry or cleanup_required or changed_paths:
        actions = [action for action in actions if action != "retry_execute"]
    if not actions and result != "completed":
        actions.append("review_partial_changes")
    return actions


def final_receipt(repo_root: Path, parsed: dict[str, Any], execution_id: str, baseline: dict[str, Any], claimed: dict[str, Any] | None, claim_error: str | None, changed_paths: list[str], violations: list[dict[str, str]], baseline_dirty_modified: list[str], postflight: list[dict[str, Any]]) -> dict[str, Any]:
    safety_reasons = []
    violation_reason = {"excluded": "excluded_path_modified", "outside_modify_scope": "scope_violation", "undeclared_create": "unapproved_path_created", "undeclared_delete": "unapproved_path_deleted"}
    for item in violations:
        reason = violation_reason[item["violation"]]
        if reason not in safety_reasons:
            safety_reasons.append(reason)
    if baseline_dirty_modified:
        safety_reasons.append("baseline_dirty_path_modified")
    if claimed:
        for reason in claimed.get("reasonCodes") or []:
            if reason in {"plan_deviation_required", "scope_expansion_required", "executor_capability_mismatch"} and reason not in safety_reasons:
                safety_reasons.append(reason)
    mismatch = classify_claimed_observed_mismatch(claimed, changed_paths, postflight)
    technical_reasons = []
    if claim_error:
        technical_reasons.append("executor_error")
    for verifier in postflight:
        if verifier.get("status") != "passed":
            reason = verifier_reason(str(verifier.get("status")), verifier.get("exitCode"), verifier.get("reasonCode"))
            if reason not in technical_reasons:
                technical_reasons.append(reason)
    if safety_reasons or mismatch:
        result = "escalated"
        reasons = list(safety_reasons)
        if mismatch and "claimed_observed_mismatch" not in reasons:
            reasons.append("claimed_observed_mismatch")
        for reason in technical_reasons:
            if reason not in reasons:
                reasons.append(reason)
    elif technical_reasons:
        result = "failed"
        reasons = technical_reasons
    else:
        result = "completed"
        reasons = []
    observed_cleanup_required = bool(violations or changed_paths)
    cleanup_required = observed_cleanup_required or bool(claimed.get("cleanupRequired")) if claimed else observed_cleanup_required
    safe_to_retry = (bool(claimed.get("safeToRetry")) if claimed else result != "completed") and not observed_cleanup_required
    receipt: dict[str, Any] = {
        "schemaVersion": "tigerkit.execution-receipt/v1",
        "executionId": execution_id,
        "specId": parsed["specId"],
        "executor": parsed["executor"],
        "result": result,
        "boundaryEnforcement": "hard",
        "reasonCodes": reasons,
        "reasonDetails": unique_reason_details(reasons, claimed.get("reasonDetails") if claimed else None),
        "baseline": baseline,
        "observed": {"changedPaths": changed_paths, "scopeViolations": violations, "baselineDirtyPathsModified": baseline_dirty_modified, "claimedObservedMismatch": mismatch},
        "postflightVerifiers": postflight,
        "safeToRetry": safe_to_retry,
        "cleanupRequired": cleanup_required,
        "recommendedActions": recommended_actions(result, reasons, safe_to_retry, cleanup_required, changed_paths),
    }
    if claimed:
        receipt["claimed"] = {"outcome": claimed["outcome"], "changedPaths": claimed["changedPaths"], "verifierResults": claimed["verifierResults"], "reasonCodes": claimed["reasonCodes"], "reasonDetails": claimed["reasonDetails"]}
    return receipt


def persist_receipt(repo_root: Path, receipt: dict[str, Any]) -> Path:
    path = execution_dir(repo_root) / f"{receipt['executionId']}.yaml"
    if path.exists():
        raise SystemExit(f"receipt already exists: {path}")
    atomic_write(path, dump_yaml(receipt) + "\n")
    return path


def rejected_receipt(spec_id: str, execution_id: str, reason: str, message: str) -> dict[str, Any]:
    return {
        "schemaVersion": "tigerkit.execution-receipt/v1",
        "executionId": execution_id,
        "specId": spec_id,
        "result": "rejected",
        "boundaryEnforcement": "detection_only",
        "reasonCodes": [reason],
        "reasonDetails": [{"code": reason, "message": message}],
        "observed": {
            "changedPaths": [],
            "scopeViolations": [],
            "baselineDirtyPathsModified": [],
            "claimedObservedMismatch": False,
        },
        "postflightVerifiers": [],
        "safeToRetry": False,
        "cleanupRequired": False,
        "recommendedActions": ["inspect_enforcement_failure"] if reason == "hard_enforcement_unavailable" else ["inspect_loop_spec"],
    }

def render_execute_usage() -> str:
    return "\n".join(["사용법: execute <spec-id-or-path>  # legacy helper, active /tk command 아님", "예: execute fix-payment-modal-scroll-20260622-120000-ABCD"])


def render_execute_receipt(receipt: dict[str, Any], path: Path | None, executor: str | None = None) -> str:
    total = len(receipt.get("postflightVerifiers") or [])
    passed = len([v for v in receipt.get("postflightVerifiers") or [] if v.get("status") == "passed"])
    lines = [
        f"Execute: {receipt['result']}",
        f"Spec: {receipt['specId']}",
        f"Executor: {executor or receipt.get('executor', 'NONE')}",
        f"Receipt: {path if path else 'NONE'}",
        f"Changed paths: {len(receipt.get('observed', {}).get('changedPaths') or [])}",
        f"Verifiers: {passed}/{total} passed",
    ]
    if receipt.get("reasonCodes"):
        lines.append(f"Primary reason: {receipt['reasonCodes'][0]}")
    if receipt.get("recommendedActions"):
        lines.append(f"Required action: {receipt['recommendedActions'][0]}")
    return "\n".join(lines)


def run_executor(repo_root: Path, parsed: dict[str, Any], execution_id: str) -> tuple[dict[str, Any] | None, str | None]:
    schema_path = plugin_root() / "schemas" / "executor-claimed-result.schema.json"
    prompt = "\n".join([
        "TigerKit legacy execute helper assigned exactly one LoopSpec.",
        f"executionId: {execution_id}",
        f"specId: {parsed['specId']}",
        f"executor: {parsed['executor']}",
        "Return only valid JSON matching tigerkit.executor-claimed-result/v1.",
        "LoopSpec:",
        parsed["text"],
    ])
    boundary_payload = {"repoRoot": str(repo_root), **parsed["scope"]}
    with NamedTemporaryFile("w", encoding="utf-8", delete=False, prefix="tigerkit-execute-boundary-", suffix=".json") as tmp:
        json.dump(boundary_payload, tmp, ensure_ascii=False)
        boundary_path = tmp.name
    env = os.environ.copy()
    env["TIGERKIT_EXECUTE_BOUNDARY_FILE"] = boundary_path
    try:
        proc = subprocess.run([
            "claude", "-p", "--agent", f"tk-executor-{parsed['executor']}", "--json-schema", schema_path.read_text(encoding="utf-8"), prompt
        ], cwd=str(repo_root), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    except Exception as exc:
        return None, str(exc)
    finally:
        try:
            Path(boundary_path).unlink()
        except Exception:
            pass
    if proc.returncode != 0:
        return None, "executor process failed"
    declared_verifier_ids = {str(verifier["id"]) for verifier in parsed["verifiers"]}
    return parse_claimed_result(proc.stdout, execution_id, parsed["specId"], parsed["executor"], declared_verifier_ids)


def cmd_execute(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    spec_args = list(args.spec or [])
    if len(spec_args) != 1:
        print(render_execute_usage())
        return 0
    execution_id = next_execution_id()
    spec_path = resolve_loop_spec_path(repo_root, spec_args[0])
    spec_id = spec_args[0]
    executor = None
    try:
        parsed = parse_loop_spec_for_execute(spec_path, repo_root)
        spec_id = parsed["specId"]
        executor = parsed["executor"]
        current_head = git("rev-parse", "HEAD", cwd=repo_root)
        if current_head and current_head != parsed["headSha"]:
            receipt = rejected_receipt(spec_id, execution_id, "stale_base_revision", "Current HEAD differs from LoopSpec context headSha.")
            path = persist_receipt(repo_root, receipt)
            print(render_execute_receipt(receipt, path, executor))
            return 1
        current_context = context_fingerprint(repo_root, scan_capabilities(repo_root))
        if current_context["fingerprint"]["value"] != parsed["fingerprint"]:
            receipt = rejected_receipt(spec_id, execution_id, "stale_fingerprint", "Current repository fingerprint differs from LoopSpec context fingerprint.")
            path = persist_receipt(repo_root, receipt)
            print(render_execute_receipt(receipt, path, executor))
            return 1
    except SystemExit as exc:
        if not str(exc).startswith("cannot read LoopSpec:"):
            raise
        receipt = rejected_receipt(spec_id, execution_id, "spec_not_found", f"LoopSpec not found or unreadable: {spec_path}")
        path = persist_receipt(repo_root, receipt)
        print(render_execute_receipt(receipt, path, executor))
        return 1
    except FileNotFoundError:
        receipt = rejected_receipt(spec_id, execution_id, "spec_not_found", f"LoopSpec not found: {spec_path}")
        path = persist_receipt(repo_root, receipt)
        print(render_execute_receipt(receipt, path, executor))
        return 1
    except ValueError as exc:
        reason = str(exc)
        receipt = rejected_receipt(spec_id, execution_id, reason, f"LoopSpec rejected: {reason}")
        path = persist_receipt(repo_root, receipt)
        print(render_execute_receipt(receipt, path, executor))
        return 1
    baseline = baseline_capture(repo_root)
    before = repo_file_state(repo_root)
    claimed, claim_error = run_executor(repo_root, parsed, execution_id)
    after = repo_file_state(repo_root)
    changed_paths, operations = changed_since_baseline(before, after)
    violations = scope_violations(changed_paths, operations, parsed["scope"])
    timeout = int(((parsed.get("execution") or {}).get("budget") or {}).get("maxMinutes") or 30) * 60
    postflight = [run_verifier(repo_root, verifier, timeout) for verifier in parsed["verifiers"] if verifier.get("required") is True]
    baseline_dirty_modified = sorted(set(baseline["dirtyPaths"]) & set(changed_paths))
    receipt = final_receipt(repo_root, parsed, execution_id, baseline, claimed, claim_error, changed_paths, violations, baseline_dirty_modified, postflight)
    path = persist_receipt(repo_root, receipt)
    print(render_execute_receipt(receipt, path, executor))
    return 0 if receipt["result"] == "completed" else 1


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

    p_loop = sub.add_parser("loop-spec", help="Legacy helper: generate or validate a worktree-scoped LoopSpec")
    p_loop.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_loop.add_argument("--explain", action="store_true", help="Include expanded explanation in command output")
    p_loop.add_argument("--type", choices=["bugfix", "refactor", "flaky-test"], default=None, help="Override deterministic task classifier")
    p_loop.add_argument("--motif", choices=sorted(VALID_MOTIFS), default=None, help="Force a motif when policy allows it")
    p_loop.add_argument("--name", default=None, help="Human-friendly spec name")
    p_loop.add_argument("--no-write", action="store_true", help="Render recommendation without writing an artifact")
    p_loop.add_argument("task", nargs="*", help="Task description, or: validate <spec-id-or-path>")
    p_loop.set_defaults(func=cmd_loop_spec)

    p_execute = sub.add_parser("execute", help="Legacy helper: validate and execute a LoopSpec v2")
    p_execute.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_execute.add_argument("spec", nargs="*", help="Spec id or path")
    p_execute.set_defaults(func=cmd_execute)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
