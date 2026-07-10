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


def common_git_dir(repo_root: Path) -> Path:
    raw = git("rev-parse", "--git-common-dir", cwd=repo_root)
    if not raw:
        return abs_dir(repo_root / ".git")
    path = Path(raw)
    if not path.is_absolute():
        path = repo_root / path
    return abs_dir(path)


def repo_key(repo_root: Path) -> str:
    common_dir = common_git_dir(repo_root)
    return f"{slugify(common_dir.parent.name)}--{sha8(str(common_dir))}"


def worktree_key(repo_root: Path) -> str:
    return f"{slugify(repo_root.name)}--{sha8(str(repo_root))}"


def scope_key(repo_root: Path) -> str:
    branch = git("branch", "--show-current", cwd=repo_root)
    if branch:
        return slugify(branch)
    return f"workspace-{slugify(repo_root.name)}--{sha8(str(repo_root))}"


def draft_dir(repo_root: Path, kind: str) -> Path:
    root = state_root()
    return root / "repos" / repo_key(repo_root) / "worktrees" / worktree_key(repo_root) / kind


def browser_verify_dir(repo_root: Path) -> Path:
    root = state_root()
    return root / "repos" / repo_key(repo_root) / "browser-verify"


def legacy_ui_diff_dir(repo_root: Path) -> Path:
    root = state_root()
    return root / "repos" / repo_key(repo_root) / "ui-diff"


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


def load_gap_packet_content(packet_file: str | None) -> dict[str, Any]:
    raw = Path(packet_file).read_text(encoding="utf-8") if packet_file else sys.stdin.read()
    if not raw.strip():
        raise SystemExit("write-gap-packet requires non-empty packet content")
    try:
        payload = json.loads(raw)
    except Exception as exc:
        raise SystemExit(f"write-gap-packet requires valid json packet content: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("write-gap-packet requires a top-level json object")
    return payload


def cmd_gap_paths(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "gapDir": str(gap_dir),
        "currentPath": str(gap_dir / "current.md"),
        "currentPacketPath": str(gap_dir / "current.packet.json"),
        "branchStatePath": str(root / "repos" / repo_key_value / "branches" / scope_key_value / "branch-state.json"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_gap_packet_paths(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "gapDir": str(gap_dir),
        "currentPacketPath": str(gap_dir / "current.packet.json"),
        "branchStatePath": str(root / "repos" / repo_key_value / "branches" / scope_key_value / "branch-state.json"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_read_gap_packet(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    current_packet_path = gap_dir / "current.packet.json"
    if not current_packet_path.is_file():
        print(json.dumps({
            "found": False,
            "repoRoot": str(repo_root),
            "commonGitDir": str(common_git_dir_value),
            "repoKey": repo_key_value,
            "worktreeKey": worktree_key_value,
            "scopeKey": scope_key_value,
            "currentPacketPath": str(current_packet_path),
        }, ensure_ascii=False, indent=2))
        return 0

    packet = load_json(current_packet_path, None)
    if not isinstance(packet, dict):
        raise SystemExit(f"read-gap-packet found invalid json at {current_packet_path}")

    print(json.dumps({
        "found": True,
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "currentPacketPath": str(current_packet_path),
        "packet": packet,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_read_reflect_candidate(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    current_ledger_path = root / "repos" / repo_key_value / "branches" / scope_key_value / "reflect" / "current.yaml"
    if not current_ledger_path.is_file():
        print(json.dumps({
            "found": False,
            "repoRoot": str(repo_root),
            "commonGitDir": str(common_git_dir_value),
            "repoKey": repo_key_value,
            "worktreeKey": worktree_key_value,
            "scopeKey": scope_key_value,
            "ledgerPath": str(current_ledger_path),
            "candidateId": args.candidate_id,
            "same_session_required": True,
            "same_ledger_required": True,
            "source_of_truth": "reflect-ledger",
        }, ensure_ascii=False, indent=2))
        return 0

    ledger = load_json(current_ledger_path, None)
    if not isinstance(ledger, dict):
        raise SystemExit(f"read-reflect-candidate found invalid ledger json at {current_ledger_path}")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list):
        raise SystemExit(f"read-reflect-candidate expected candidates[] in {current_ledger_path}")

    matched = None
    for item in candidates:
        if isinstance(item, dict) and item.get("candidate_id") == args.candidate_id:
            matched = item
            break

    print(json.dumps({
        "found": matched is not None,
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "ledgerPath": str(current_ledger_path),
        "candidateId": args.candidate_id,
        "same_session_required": True,
        "same_ledger_required": True,
        "source_of_truth": "reflect-ledger",
        "candidate": matched,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_draft_paths(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    draft_root = root / "repos" / repo_key_value / "worktrees" / worktree_key_value
    draft_path = draft_root / args.kind / "current.md"
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "worktreeKey": worktree_key_value,
        "kind": args.kind,
        "draftRoot": str(draft_root),
        "currentPath": str(draft_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_browser_verify_paths(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    profile_dir = browser_verify_dir(repo_root)
    legacy_profile_dir = legacy_ui_diff_dir(repo_root)
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "worktreeKey": worktree_key_value,
        "profileDir": str(profile_dir),
        "legacyProfileDir": str(legacy_profile_dir),
        "legacyDetected": legacy_profile_dir.exists(),
        "envPath": str(profile_dir / "env.md"),
        "loginPath": str(profile_dir / "login.md"),
        "loginLocalPath": str(profile_dir / "login.local.md"),
        "screensDir": str(profile_dir / "screens"),
        "screensReadmePath": str(profile_dir / "screens" / "README.md"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_usage_summary(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    draft_root = root / "repos" / repo_key_value / "worktrees" / worktree_key_value
    kinds = ["handoffs", "prd", "issues", "ledger", "quiz"]
    summary: dict[str, Any] = {}
    for kind in kinds:
        current_path = draft_root / kind / "current.md"
        summary[kind] = {
            "currentPath": str(current_path),
            "exists": current_path.is_file(),
            "mtime": current_path.stat().st_mtime if current_path.is_file() else None,
        }
    profile_dir = browser_verify_dir(repo_root)
    summary["browser-verify-profile"] = {
        "profileDir": str(profile_dir),
        "exists": profile_dir.exists(),
        "envPath": str(profile_dir / "env.md"),
    }
    payload = {
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "worktreeKey": worktree_key_value,
        "summary": summary,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_write_gap(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
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
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "gapId": gap_id,
        "reportPath": str(report_path),
        "currentPath": str(current_path),
        "branchStatePath": str(branch_state_path),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_write_gap_packet(args: argparse.Namespace) -> int:
    repo_root = resolve_repo_root(args.repo_root)
    repo_key_value = repo_key(repo_root)
    scope_key_value = scope_key(repo_root)
    worktree_key_value = worktree_key(repo_root)
    common_git_dir_value = common_git_dir(repo_root)
    root = state_root()
    packet = load_gap_packet_content(args.packet_file)
    gap_id = str(packet.get("gap_id") or args.gap_id or next_gap_id())
    packet.setdefault("gap_id", gap_id)
    packet.setdefault("repo_root", str(repo_root))
    packet.setdefault("repo_key", repo_key_value)
    packet.setdefault("scope_key", scope_key_value)
    packet.setdefault("created_at", now_iso())
    gap_dir = root / "repos" / repo_key_value / "branches" / scope_key_value / "gap"
    packet_path = gap_dir / f"{gap_id}.packet.json"
    current_packet_path = gap_dir / "current.packet.json"
    branch_state_path = root / "repos" / repo_key_value / "branches" / scope_key_value / "branch-state.json"
    normalized = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    atomic_write(packet_path, normalized)
    atomic_write(current_packet_path, normalized)
    branch_state = load_json(branch_state_path, {})
    branch_state.update({
        "repoKey": repo_key_value,
        "scopeKey": scope_key_value,
        "lastGapPacketId": gap_id,
        "lastGapPacketPath": str(packet_path),
        "updatedAt": now_iso(),
    })
    atomic_write_json(branch_state_path, branch_state)
    print(json.dumps({
        "stateRoot": str(root),
        "repoRoot": str(repo_root),
        "commonGitDir": str(common_git_dir_value),
        "repoKey": repo_key_value,
        "worktreeKey": worktree_key_value,
        "scopeKey": scope_key_value,
        "gapId": gap_id,
        "packetPath": str(packet_path),
        "currentPacketPath": str(current_packet_path),
        "branchStatePath": str(branch_state_path),
        "contentSha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
    }, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TigerKit active generated-state helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    p_paths = sub.add_parser("gap-paths", help="Print active gap state paths")
    p_paths.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_paths.set_defaults(func=cmd_gap_paths)

    p_packet_paths = sub.add_parser("gap-packet-paths", help="Print active gap packet state paths")
    p_packet_paths.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_packet_paths.set_defaults(func=cmd_gap_packet_paths)

    p_read_packet = sub.add_parser("read-gap-packet", help="Read current gap packet for the repo/scope")
    p_read_packet.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_read_packet.set_defaults(func=cmd_read_gap_packet)

    p_read_reflect = sub.add_parser("read-reflect-candidate", help="Read one candidate from the current reflect ledger")
    p_read_reflect.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_read_reflect.add_argument("--candidate-id", help="Candidate id to read from current.yaml", required=True)
    p_read_reflect.set_defaults(func=cmd_read_reflect_candidate)

    p_draft_paths = sub.add_parser("draft-paths", help="Print current-first draft artifact paths under ~/.tigerkit")
    p_draft_paths.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_draft_paths.add_argument("--kind", choices=["handoffs", "prd", "issues", "ledger", "quiz"], required=True)
    p_draft_paths.set_defaults(func=cmd_draft_paths)

    p_usage_summary = sub.add_parser("usage-summary", help="Print worktree-scoped current artifact usage summary")
    p_usage_summary.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_usage_summary.set_defaults(func=cmd_usage_summary)

    p_browser_verify_paths = sub.add_parser("browser-verify-paths", help="Print repo-scoped browser-verify profile paths under ~/.tigerkit")
    p_browser_verify_paths.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_browser_verify_paths.set_defaults(func=cmd_browser_verify_paths)

    p_write = sub.add_parser("write-gap", help="Write a gap report into ~/.tigerkit")
    p_write.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_write.add_argument("--gap-id", help="Explicit GAP id", default=None)
    p_write.add_argument("--report-file", help="Read report content from file instead of stdin", default=None)
    p_write.set_defaults(func=cmd_write_gap)

    p_write_packet = sub.add_parser("write-gap-packet", help="Write a gap packet into ~/.tigerkit")
    p_write_packet.add_argument("--repo-root", help="Repo root or working directory", default=None)
    p_write_packet.add_argument("--gap-id", help="Explicit GAP id", default=None)
    p_write_packet.add_argument("--packet-file", help="Read packet json from file instead of stdin", default=None)
    p_write_packet.set_defaults(func=cmd_write_gap_packet)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
