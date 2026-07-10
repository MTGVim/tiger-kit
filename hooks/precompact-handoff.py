#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_HELPER = ROOT / 'scripts' / 'tigerkit_state.py'


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(['git', *args], cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.stdout.strip() if result.returncode == 0 else ''


def resolve_repo_root(cwd: Path) -> Path:
    top = git(['rev-parse', '--show-toplevel'], cwd)
    return Path(top).resolve() if top else cwd.resolve()


def draft_path(repo_root: Path, kind: str) -> Path:
    result = subprocess.run(['python3', str(STATE_HELPER), 'draft-paths', '--repo-root', str(repo_root), '--kind', kind], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f'failed to resolve {kind} path')
    payload = json.loads(result.stdout)
    return Path(payload['currentPath']).expanduser().resolve()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    cwd = Path(os.getcwd())
    repo_root = resolve_repo_root(cwd)
    branch = git(['branch', '--show-current'], repo_root) or '(detached)'
    handoff_path = draft_path(repo_root, 'handoffs')
    wayfinder_path = draft_path(repo_root, 'wayfinder')
    title = repo_root.name
    content = f'''# Auto PreCompact Handoff\n\n- generated_at: {now_iso()}\n- repo_root: {repo_root}\n- branch: {branch}\n- cwd: {cwd.resolve()}\n\n## Current state\n- This draft was auto-generated before compaction.\n- Re-run `/tk:handoff` or `/tk:wayfinder` for a richer human-curated summary if needed.\n\n## Resume hint\n- Read this file first after compaction, then inspect the latest diff and current TigerKit artifacts.\n'''
    write_text(handoff_path, content)
    if not wayfinder_path.exists():
        write_text(wayfinder_path, f'# Wayfinder map\n\n- generated_at: {now_iso()}\n- current_goal: resume after compaction\n- next_step: inspect handoff/current.md and continue from the last staged milestone\n')
    print(json.dumps({'handoffPath': str(handoff_path), 'wayfinderPath': str(wayfinder_path), 'repoRoot': str(repo_root)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
