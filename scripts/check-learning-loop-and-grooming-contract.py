#!/usr/bin/env python3
"""Validate TigerKit learn/reflect/grooming stage-2 contract needles."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = ROOT / "evals" / "evals.json"

REQUIRED_TEXT_FILES = {
    "README.md": [
        "RED → GREEN → REFACTOR",
        "pos3 / neg2 / owner",
        "guidanceBudgetBytes",
        "compact evidence pointer",
    ],
    ".tigerkit/docs/usage.md": [
        "RED → GREEN → REFACTOR",
        "pos3 / neg2 / owner",
        "guidanceBudgetBytes",
        "compact evidence pointer",
    ],
    "commands/learn.md": [
        "RED → GREEN → REFACTOR",
        "positive 3 / negative 2 / owner",
        "evals/evals.json",
    ],
    "commands/reflect.md": [
        "Failure-type classification",
        "failure_type",
        "evidence_pointer",
        "hit: YYYY-MM-DD",
    ],
    "docs/reflect-file-policy.md": [
        "failure_type",
        "evidence_pointer",
        "hit: YYYY-MM-DD",
    ],
    "commands/grooming.md": [
        "guidanceBudgetBytes",
        "32768",
        "~/.claude/rules-archive/",
        "usage-summary",
        "사용자 승인 없이 강등/삭제",
    ],
    ".tigerkit/docs/output-contract.md": [
        "RED | GREEN | REFACTOR evidence summary",
        "pos3 / neg2 / owner registered | pending",
        "Failure type:",
        "guidanceBudgetBytes or default 32768",
        "rules-archive candidate | /tk:learn handoff | approval required",
    ],
}

REQUIRED_EVAL_NEEDLES = [
    '"name": "learn-skill-tdd-red-green-refactor-loop"',
    '"name": "learn-generates-pos3-neg2-owner-eval-coverage"',
    '"name": "reflect-classifies-failure-type-and-keeps-reason-compact"',
    '"name": "grooming-guidance-budget-and-approval-gates"',
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"learn/grooming contract check failed: {message}")


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {relative_path}")


def require_contains(text: str, needle: str, path_label: str) -> None:
    if needle not in text:
        fail(f"{path_label} must mention {needle!r}")


def main() -> int:
    for relative_path, needles in REQUIRED_TEXT_FILES.items():
        text = read_text(relative_path)
        for needle in needles:
            require_contains(text, needle, relative_path)

    evals_text = read_text(str(EVALS_PATH.relative_to(ROOT)))
    for needle in REQUIRED_EVAL_NEEDLES:
        require_contains(evals_text, needle, str(EVALS_PATH.relative_to(ROOT)))

    print("learn/grooming contract ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
