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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
