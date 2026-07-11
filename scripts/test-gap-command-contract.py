#!/usr/bin/env python3
"""Deterministic regression tests for the canonical /tk:gap command contract."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND_PATH = ROOT / "commands" / "gap.md"

REQUIRED_PLAN_ONLY_RULE = (
    "### Plan/generated Current classification rule",
    "When the SoT requirement is accessible, clear, and non-conflicting",
    "the explicitly scoped/inspected Current set contains only implementation plans and/or generated artifacts",
    "there is no direct implementation/runtime/command/rendered/diff evidence",
    "classify the requested behavior as `missing` in Current, not `ambiguous`",
    "Any uncertainty that uninspected implementation might exist belongs in `⚠️ Ambiguities / Missing Evidence:`",
    "does not replace the primary `missing` classification for this scoped comparison",
    "Do not overclaim global repository absence",
    "Preserve `ambiguous` for source conflict, unresolved owner/source priority, inaccessible required sources, or a genuinely indeterminate requirement",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def test_plan_only_current_classification_rule_is_canonical() -> None:
    text = COMMAND_PATH.read_text(encoding="utf-8")
    policy_start = text.index("## Analysis policy")
    priority_start = text.index("## Priority")
    policy = text[policy_start:priority_start]

    for marker in REQUIRED_PLAN_ONLY_RULE:
        if marker not in policy:
            fail(f"commands/gap.md is missing canonical plan-only rule marker: {marker!r}")

    if policy.index("classify the requested behavior as `missing` in Current, not `ambiguous`") > policy.index(
        "Preserve `ambiguous`"
    ):
        fail("the plan-only missing rule must be evaluated before the ambiguous-preservation rule")


def main() -> int:
    test_plan_only_current_classification_rule_is_canonical()
    print("gap command contract tests ok: plan-only Current classification rule")
    return 0


if __name__ == "__main__":
    sys.exit(main())
