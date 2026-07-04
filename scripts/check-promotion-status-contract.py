#!/usr/bin/env python3
"""Validate wording-promotion status docs and sample registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / ".tigerkit" / "docs" / "promotion-statuses.md"
REGISTRY_PATH = ROOT / "evals" / "contracts" / "promotion-status-registry.example.json"
EVALS_PATH = ROOT / "evals" / "evals.json"
README_PATH = ROOT / "README.md"
FULL_PILOTS_DOC = ROOT / ".tigerkit" / "docs" / "full-eval-pilots.md"
VALID_STATUSES = {"draft", "micro-validated", "full-validated", "shipped"}
REQUIRED_DOC_NEEDLES = [
    "draft",
    "micro-validated",
    "full-validated",
    "shipped",
    "contract eval",
    "behavior correctness",
    "Do not promote",
]
REQUIRED_FULL_PILOTS_NEEDLES = [
    "full-validated",
    "shipped",
    "FULL pilot by itself does not mean shipped",
]
REQUIRED_EVAL_NEEDLES = [
    '"name": "promotion-status-distinguishes-draft-micro-full-and-shipped"',
    "States promotion status vocabulary draft micro-validated full-validated shipped",
    "States contract eval and full behavior eval are different evidence tiers",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"promotion status check failed: {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required registry sample: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(loaded, dict):
        fail(f"top-level json object required in {path.relative_to(ROOT)}")
    return cast(dict[str, Any], loaded)


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"{label} must mention {needle!r}")


def main() -> int:
    readme_text = read_text(README_PATH)
    require_contains(readme_text, "promotion-statuses.md", str(README_PATH.relative_to(ROOT)))

    doc_text = read_text(DOC_PATH)
    for needle in REQUIRED_DOC_NEEDLES:
        require_contains(doc_text, needle, str(DOC_PATH.relative_to(ROOT)))

    full_pilots_text = read_text(FULL_PILOTS_DOC)
    for needle in REQUIRED_FULL_PILOTS_NEEDLES:
        require_contains(full_pilots_text, needle, str(FULL_PILOTS_DOC.relative_to(ROOT)))

    registry = load_json(REGISTRY_PATH)
    if registry.get("schemaVersion") != "tigerkit.promotion-status-registry/v1":
        fail("registry schemaVersion must be 'tigerkit.promotion-status-registry/v1'")
    entries = registry.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("registry entries must be a non-empty list")

    statuses_seen: set[str] = set()
    command_surface_seen = False
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            fail(f"registry entry #{index} must be an object")
        for field in ["id", "subject", "status", "evidence_tier", "artifacts", "note"]:
            if field not in entry:
                fail(f"registry entry #{index} missing field {field!r}")
        status = entry["status"]
        if not isinstance(status, str) or status not in VALID_STATUSES:
            fail(f"registry entry #{index} has invalid status {status!r}")
        statuses_seen.add(status)
        subject = entry["subject"]
        if isinstance(subject, str) and subject.startswith("/tk:"):
            command_surface_seen = True
        artifacts = entry["artifacts"]
        if not isinstance(artifacts, list) or not artifacts or not all(isinstance(item, str) and item.strip() for item in artifacts):
            fail(f"registry entry #{index} artifacts must be a non-empty list of strings")

    if not command_surface_seen:
        fail("registry must include at least one /tk:* command surface example")
    if VALID_STATUSES - statuses_seen:
        fail(f"registry must show all statuses at least once; missing {sorted(VALID_STATUSES - statuses_seen)!r}")

    evals_text = read_text(EVALS_PATH)
    for needle in REQUIRED_EVAL_NEEDLES:
        require_contains(evals_text, needle, str(EVALS_PATH.relative_to(ROOT)))

    print(f"promotion status ok: {REGISTRY_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
