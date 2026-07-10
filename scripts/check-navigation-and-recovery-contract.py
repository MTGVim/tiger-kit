#!/usr/bin/env python3
"""Validate TigerKit navigation/recovery command surfaces and opt-in precompact hook."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / 'evals' / 'evals.json'
STATE_HELPER = ROOT / 'scripts' / 'tigerkit_state.py'
INSTALL_HOOK = ROOT / 'scripts' / 'install-precompact-hook.sh'
PRECOMPACT_HOOK = ROOT / 'hooks' / 'precompact-handoff.py'
HELP_MAP = ROOT / 'docs' / 'help-map.json'

REQUIRED_TEXT_FILES = {
    'README.md': ['/tk:help', '/tk:next', '/tk:quiz', '/tk:wayfinder', 'install-precompact-hook.sh'],
    '.tigerkit/docs/usage.md': ['/tk:help', '/tk:next', '/tk:quiz', '/tk:wayfinder'],
    '.tigerkit/docs/output-contract.md': ['## `/tk:help` Output Contract', '## `/tk:next` Output Contract', '## `/tk:quiz` Output Contract', '## `/tk:wayfinder` Output Contract'],
    'commands/help.md': ['docs/help-map.json', 'generated', '/tk:route', '/tk:next'],
    'commands/next.md': ['usage-summary', 'exactly one', '/tk:quiz'],
    'commands/quiz.md': ['ledger/current.md', 'quiz/current.md', 'clean-diff-rejected'],
    'commands/wayfinder.md': ['wayfinder/current.md', 'shared map', 'reopen hints'],
    'commands/to-prd.md': ['## Interview mode', '## Reference slot'],
    'commands/to-issues.md': ['blocking-edge', 'blocked-by'],
    'commands/prototype.md': ['radically different', 'floating switcher', 'portable pure logic'],
    'scripts/install-precompact-hook.sh': ['PreCompact', 'precompact-handoff.py'],
    'hooks/precompact-handoff.py': ['draft-paths', 'handoffs', 'wayfinder'],
}

REQUIRED_EVAL_NEEDLES = [
    '"name": "help-uses-generated-help-map-navigation-surface"',
    '"name": "next-picks-exactly-one-command-from-usage-summary-or-task"',
    '"name": "quiz-uses-diff-and-ledger-for-comprehension-gate"',
    '"name": "wayfinder-persists-current-first-work-map"',
    '"name": "to-prd-interview-reference-slot-and-to-issues-blocking-edges"',
    '"name": "prototype-wayfinder-and-precompact-opt-in-boundary"',
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"navigation/recovery check failed: {message}")


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        fail(f'missing required file: {relative_path}')


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=str(cwd or ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    for relative_path, needles in REQUIRED_TEXT_FILES.items():
        text = read_text(relative_path)
        for needle in needles:
            if needle not in text:
                fail(f"{relative_path} must mention {needle!r}")

    evals_text = read_text(str(EVALS_PATH.relative_to(ROOT)))
    for needle in REQUIRED_EVAL_NEEDLES:
        if needle not in evals_text:
            fail(f"{EVALS_PATH.relative_to(ROOT)} must mention {needle!r}")

    for kind in ('ledger', 'quiz', 'wayfinder'):
        result = run('python3', str(STATE_HELPER), 'draft-paths', '--repo-root', str(ROOT), '--kind', kind)
        if result.returncode != 0:
            fail(f'draft-paths failed for {kind}: {result.stderr.strip() or result.stdout.strip()}')
        payload = json.loads(result.stdout)
        if payload.get('kind') != kind or 'currentPath' not in payload:
            fail(f'draft-paths payload malformed for {kind}')

    usage = run('python3', str(STATE_HELPER), 'usage-summary', '--repo-root', str(ROOT))
    if usage.returncode != 0:
        fail(f'usage-summary failed: {usage.stderr.strip() or usage.stdout.strip()}')
    usage_payload = json.loads(usage.stdout)
    summary = usage_payload.get('summary', {})
    for required_key in ('ledger', 'quiz', 'wayfinder'):
        if required_key not in summary:
            fail(f'usage-summary missing key {required_key!r}')

    generate = run('python3', str(ROOT / 'scripts' / 'generate-help-map.py'))
    if generate.returncode != 0:
        fail(f'generate-help-map failed: {generate.stderr.strip() or generate.stdout.strip()}')
    help_map = json.loads(HELP_MAP.read_text(encoding='utf-8'))
    commands = {entry['command'] for entry in help_map.get('commands', []) if isinstance(entry, dict) and 'command' in entry}
    for cmd in ('/tk:help', '/tk:next', '/tk:quiz', '/tk:wayfinder'):
        if cmd not in commands:
            fail(f'help-map missing {cmd}')

    with tempfile.TemporaryDirectory() as tmpdir:
        settings = Path(tmpdir) / 'settings.json'
        settings.write_text('{}\n', encoding='utf-8')
        install = run(str(INSTALL_HOOK), str(settings))
        if install.returncode != 0:
            fail(f'install-precompact-hook.sh failed: {install.stderr.strip() or install.stdout.strip()}')
        installed = json.loads(settings.read_text(encoding='utf-8'))
        entries = installed.get('hooks', {}).get('PreCompact', [])
        if not entries:
            fail('PreCompact hook entry missing after install')
        commands_list = [hook.get('command', '') for entry in entries if isinstance(entry, dict) for hook in entry.get('hooks', []) if isinstance(hook, dict)]
        if not any('precompact-handoff.py' in command for command in commands_list):
            fail('installed PreCompact hook does not point at precompact-handoff.py')

    hook_run = run('python3', str(PRECOMPACT_HOOK), cwd=ROOT)
    if hook_run.returncode != 0:
        fail(f'precompact hook failed: {hook_run.stderr.strip() or hook_run.stdout.strip()}')
    hook_payload = json.loads(hook_run.stdout)
    for field in ('handoffPath', 'wayfinderPath', 'repoRoot'):
        if field not in hook_payload:
            fail(f'precompact hook payload missing {field!r}')

    print('navigation/recovery contract ok')
    return 0


if __name__ == '__main__':
    sys.exit(main())
