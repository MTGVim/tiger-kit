#!/usr/bin/env python3
"""Validate the tracked gap→route evidence-packet contract artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PACKET_PATH = ROOT / "evals" / "contracts" / "gap-route-evidence-packet.example.json"
EVALS_PATH = ROOT / "evals" / "evals.json"
REQUIRED_TEXT_FILES = {
    "README.md": [
        "current.packet.json",
        "gap packet",
    ],
    "commands/gap.md": [
        "current.packet.json",
        "tigerkit.gap-packet/v1",
        "write-gap-packet",
    ],
    "commands/route.md": [
        "gap packet",
        "same repo/scope",
    ],
    "skills/route/SKILL.md": [
        "gap packet",
        "same repo/scope",
    ],
    ".tigerkit/docs/output-contract.md": [
        "gap packet",
        "same repo/scope",
    ],
    ".tigerkit/docs/storage-boundary.md": [
        "current.packet.json",
    ],
    ".tigerkit/docs/gap-route-evidence-packets.md": [
        "tigerkit.gap-packet/v1",
        "source_refs",
        "precedence",
        "unresolved_questions",
        "read-gap-packet",
    ],
    "scripts/tigerkit_state.py": [
        "gap-packet-paths",
        "read-gap-packet",
        "write-gap-packet",
        "current.packet.json",
    ],
}
REQUIRED_PACKET_FIELDS = {
    "schemaVersion",
    "invocation_id",
    "gap_id",
    "repo_root",
    "repo_key",
    "scope_key",
    "source_refs",
    "precedence",
    "findings",
    "unresolved_questions",
    "report_path",
    "created_at",
}
REQUIRED_PRECEDENCE_FIELDS = {"status", "resolved_order", "conflicts", "note"}
REQUIRED_FINDING_FIELDS = {
    "finding_id",
    "gap_type",
    "title",
    "sot_refs",
    "current_evidence",
    "route",
}
REQUIRED_EVAL_NEEDLES = [
    '"name": "route-reuses-gap-packet-when-available"',
    "States /tk:route can reuse same repo/scope gap packet",
    "States /tk:route falls back when packet missing or stale",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"gap packet contract check failed: {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required packet sample: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(loaded, dict):
        fail(f"top-level json object required in {path.relative_to(ROOT)}")
    return cast(dict[str, Any], loaded)


def require_contains(path_text: str, needle: str, path_label: str) -> None:
    if needle not in path_text:
        fail(f"{path_label} must mention {needle!r}")


def main() -> int:
    for relative_path, needles in REQUIRED_TEXT_FILES.items():
        path = ROOT / relative_path
        text = read_text(path)
        for needle in needles:
            require_contains(text, needle, relative_path)

    packet = load_json(SAMPLE_PACKET_PATH)
    missing_fields = REQUIRED_PACKET_FIELDS - packet.keys()
    if missing_fields:
        fail(f"sample packet missing top-level fields: {sorted(missing_fields)!r}")
    if packet.get("schemaVersion") != "tigerkit.gap-packet/v1":
        fail("sample packet schemaVersion must be 'tigerkit.gap-packet/v1'")

    source_refs = packet.get("source_refs")
    if not isinstance(source_refs, list) or not source_refs:
        fail("sample packet source_refs must be a non-empty list")
    if not all(isinstance(item, dict) for item in source_refs):
        fail("sample packet source_refs entries must be objects")

    precedence = packet.get("precedence")
    if not isinstance(precedence, dict):
        fail("sample packet precedence must be an object")
    precedence_missing = REQUIRED_PRECEDENCE_FIELDS - precedence.keys()
    if precedence_missing:
        fail(f"sample packet precedence missing fields: {sorted(precedence_missing)!r}")

    findings = packet.get("findings")
    if not isinstance(findings, list) or not findings:
        fail("sample packet findings must be a non-empty list")
    first_finding = findings[0]
    if not isinstance(first_finding, dict):
        fail("sample packet findings entries must be objects")
    finding_missing = REQUIRED_FINDING_FIELDS - first_finding.keys()
    if finding_missing:
        fail(f"sample packet finding missing fields: {sorted(finding_missing)!r}")

    unresolved = packet.get("unresolved_questions")
    if not isinstance(unresolved, list):
        fail("sample packet unresolved_questions must be a list")

    evals_text = read_text(EVALS_PATH)
    for needle in REQUIRED_EVAL_NEEDLES:
        require_contains(evals_text, needle, str(EVALS_PATH.relative_to(ROOT)))

    print(f"gap packet contract ok: {SAMPLE_PACKET_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
