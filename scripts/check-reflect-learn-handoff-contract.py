#!/usr/bin/env python3
"""Validate the tracked reflect→learn evidence-handoff contract artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SOURCE_PATH = ROOT / "evals" / "contracts" / "reflect-learn-candidate-source.example.json"
EVALS_PATH = ROOT / "evals" / "evals.json"
REQUIRED_TEXT_FILES = {
    "README.md": [
        "reflect ledger",
        "same-session + same-ledger",
    ],
    "commands/reflect.md": [
        "same-session + same-ledger",
        "source of truth",
        "read-reflect-candidate",
    ],
    "commands/learn.md": [
        "same-session + same-ledger",
        "source of truth",
        "read-reflect-candidate",
    ],
    "skills/reflect/SKILL.md": [
        "same session/ledger candidate",
        "/tk:learn",
    ],
    "skills/learn/SKILL.md": [
        "reflect candidate",
        "ledger",
    ],
    "docs/reflect-file-policy.md": [
        "candidate_id",
        "source of truth",
    ],
    ".tigerkit/docs/output-contract.md": [
        "same-session + same-ledger",
        "source of truth",
        "read-reflect-candidate",
    ],
    ".tigerkit/docs/reflect-learn-evidence-handoff.md": [
        "tigerkit.reflect-learn-source/v1",
        "candidate_id",
        "read-reflect-candidate",
        "source of truth",
    ],
    "scripts/tigerkit_state.py": [
        "read-reflect-candidate",
        "current.yaml",
        "candidate_id",
    ],
}
REQUIRED_SOURCE_FIELDS = {
    "schemaVersion",
    "source_mode",
    "ledger_path",
    "candidate_id",
    "same_session_required",
    "same_ledger_required",
    "source_of_truth",
    "candidate",
    "created_at",
}
REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "target",
    "action",
    "reason",
    "evidence",
}
REQUIRED_EVAL_NEEDLES = [
    '"name": "learn-uses-reflect-ledger-candidate-source-of-truth"',
    "States /tk:learn reads reflect ledger candidate as source of truth",
    "States same-session same-ledger boundary remains in force",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"reflect→learn handoff check failed: {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required contract sample: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(loaded, dict):
        fail(f"top-level json object required in {path.relative_to(ROOT)}")
    return cast(dict[str, Any], loaded)


def require_contains(text: str, needle: str, path_label: str) -> None:
    if needle not in text:
        fail(f"{path_label} must mention {needle!r}")


def main() -> int:
    for relative_path, needles in REQUIRED_TEXT_FILES.items():
        path = ROOT / relative_path
        text = read_text(path)
        for needle in needles:
            require_contains(text, needle, relative_path)

    sample = load_json(SAMPLE_SOURCE_PATH)
    missing = REQUIRED_SOURCE_FIELDS - sample.keys()
    if missing:
        fail(f"sample source missing top-level fields: {sorted(missing)!r}")
    if sample.get("schemaVersion") != "tigerkit.reflect-learn-source/v1":
        fail("sample source schemaVersion must be 'tigerkit.reflect-learn-source/v1'")
    if sample.get("source_mode") != "reflect-candidate":
        fail("sample source source_mode must be 'reflect-candidate'")
    if sample.get("same_session_required") is not True:
        fail("sample source same_session_required must be true")
    if sample.get("same_ledger_required") is not True:
        fail("sample source same_ledger_required must be true")
    if sample.get("source_of_truth") != "reflect-ledger":
        fail("sample source source_of_truth must be 'reflect-ledger'")

    candidate = sample.get("candidate")
    if not isinstance(candidate, dict):
        fail("sample source candidate must be an object")
    candidate_missing = REQUIRED_CANDIDATE_FIELDS - candidate.keys()
    if candidate_missing:
        fail(f"sample source candidate missing fields: {sorted(candidate_missing)!r}")

    evals_text = read_text(EVALS_PATH)
    for needle in REQUIRED_EVAL_NEEDLES:
        require_contains(evals_text, needle, str(EVALS_PATH.relative_to(ROOT)))

    print(f"reflect→learn handoff ok: {SAMPLE_SOURCE_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
