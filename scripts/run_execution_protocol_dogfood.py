#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    "tk-prep:behavior:prep-direct-no-seed-red-green",
    "tk-pr-respond:behavior:pr-respond-sdd-faithful-controller",
    "tk-pr-respond:behavior:pr-respond-sdd-round-five-breaker",
    "tk-pr-respond:behavior:pr-respond-reviewer-rejects-passing-underprotected-change",
    "tk-browser-verify:behavior:browser-rereads-evidence-before-rerun",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run live Codex/Claude dogfood for TigerKit's shared SDD/TDD execution protocol."
    )
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--host", action="append", choices=("claude-code", "codex", "hermes-agent"))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--adapter-command", required=True)
    parser.add_argument("--grader-command", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    hosts = args.host or ["claude-code", "codex"]
    command = [
        sys.executable,
        "scripts/run_skill_evals.py",
        "--baseline",
        args.baseline,
        "--candidate",
        args.candidate,
        "--runs",
        str(args.runs),
        "--adapter-command",
        args.adapter_command,
        "--grader-command",
        args.grader_command,
        "--output",
        args.output,
    ]
    for host in hosts:
        command.extend(["--host", host])
    for case in CASES:
        command.extend(["--case", case])
    completed = subprocess.run(command, cwd=ROOT, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
