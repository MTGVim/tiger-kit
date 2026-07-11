#!/usr/bin/env python3
"""Validate the maintained promotion-status registry and its result artifacts."""
from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / ".tigerkit" / "docs" / "promotion-statuses.md"
REGISTRY_PATH = ROOT / "evals" / "contracts" / "promotion-status-registry.json"
EVALS_PATH = ROOT / "evals" / "evals.json"
README_PATH = ROOT / "README.md"
FULL_PILOTS_DOC = ROOT / ".tigerkit" / "docs" / "full-eval-pilots.md"
EXPECTED_IDS = {
    "initial-command-wording",
    "reflect-repo-local-safety",
    "gap-stale-sot-precedence",
    "evidence-helper-operator-handoffs",
}
ALLOWED_STATUS_TIERS = {
    ("micro-validated", "micro-real-agent"),
    ("full-validated", "full-real-agent"),
}
REQUIRED_DOC_NEEDLES = [
    "draft",
    "micro-validated",
    "full-validated",
    "shipped",
    "contract eval",
    "behavior correctness",
    "canonical owner",
    "Update rule",
    "FULL pilot by itself does not mean shipped",
    "evals/contracts/promotion-status-registry.json",
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
    "evals/contracts/promotion-status-registry.json",
    "maintained canonical registry",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"promotion status check failed: {message}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required {label}: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(loaded, dict):
        fail(f"top-level json object required in {path.relative_to(ROOT)}")
    return cast(dict[str, Any], loaded)


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"{label} must mention {needle!r}")


def safe_result_path(raw_path: Any, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        fail(f"{label} must be a non-empty string")
    if raw_path != raw_path.strip() or "\x00" in raw_path or "\\" in raw_path:
        fail(f"{label} must be a normalized POSIX repo-relative path")
    posix_path = PurePosixPath(raw_path)
    if (
        posix_path.is_absolute()
        or PureWindowsPath(raw_path).is_absolute()
        or PureWindowsPath(raw_path).drive
        or posix_path.as_posix() != raw_path
        or any(part in {"", ".", ".."} for part in posix_path.parts)
    ):
        fail(f"{label} must be a normalized POSIX repo-relative path")

    candidate = ROOT.joinpath(*posix_path.parts)
    current = ROOT
    for part in posix_path.parts:
        current /= part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            fail(f"{label} does not name an existing regular file: {raw_path}")
        if stat.S_ISLNK(mode):
            fail(f"{label} must not traverse symlinks: {raw_path}")

    try:
        mode = os.lstat(candidate).st_mode
    except FileNotFoundError:
        fail(f"{label} does not name an existing regular file: {raw_path}")
    if not stat.S_ISREG(mode):
        fail(f"{label} must name a regular file: {raw_path}")
    return candidate


def validate_entry(index: int, entry: Any) -> None:
    label = f"registry entry #{index}"
    if not isinstance(entry, dict):
        fail(f"{label} must be an object")
    for field in ["id", "subject", "status", "evidence_tier", "artifacts", "note"]:
        if field not in entry:
            fail(f"{label} missing field {field!r}")
    if not isinstance(entry["id"], str) or not entry["id"].strip():
        fail(f"{label}.id must be a non-empty string")
    if not isinstance(entry["subject"], str) or not entry["subject"].strip():
        fail(f"{label}.subject must be a non-empty string")

    status = entry["status"]
    evidence_tier = entry["evidence_tier"]
    if (status, evidence_tier) not in ALLOWED_STATUS_TIERS:
        fail(f"{label} has unsupported status/evidence_tier pair: {(status, evidence_tier)!r}")

    artifacts = entry["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        fail(f"{label}.artifacts must contain exactly one result artifact")
    artifact_path = safe_result_path(artifacts[0], f"{label}.artifacts[0]")
    result = load_json(artifact_path, f"result artifact for {entry['id']!r}")
    for field in ["pilot_id", "status", "evidence_tier"]:
        if result.get(field) != entry[field if field != "pilot_id" else "id"]:
            fail(
                f"{label} does not match result artifact {artifact_path.relative_to(ROOT)}"
                f" for {field}: registry={entry.get(field if field != 'pilot_id' else 'id')!r},"
                f" result={result.get(field)!r}"
            )
    if (result.get("status"), result.get("evidence_tier")) not in ALLOWED_STATUS_TIERS:
        fail(f"{label} result artifact has unsupported status/evidence_tier pair")


def validate_registry() -> None:
    registry = load_json(REGISTRY_PATH, "canonical promotion status registry")
    if registry.get("schemaVersion") != "tigerkit.promotion-status-registry/v1":
        fail("registry schemaVersion must be 'tigerkit.promotion-status-registry/v1'")
    entries = registry.get("entries")
    if not isinstance(entries, list) or len(entries) != len(EXPECTED_IDS):
        fail(f"registry entries must contain exactly {len(EXPECTED_IDS)} entries")

    ids: list[str] = []
    for index, entry in enumerate(entries, start=1):
        validate_entry(index, entry)
        ids.append(cast(dict[str, Any], entry)["id"])
    if len(ids) != len(set(ids)):
        fail("registry entry IDs must not contain duplicates")
    if set(ids) != EXPECTED_IDS:
        fail(f"registry IDs must be exactly {sorted(EXPECTED_IDS)!r}; got {sorted(ids)!r}")


def main() -> int:
    readme_text = read_text(README_PATH)
    require_contains(readme_text, "promotion-statuses.md", str(README_PATH.relative_to(ROOT)))

    doc_text = read_text(DOC_PATH)
    for needle in REQUIRED_DOC_NEEDLES:
        require_contains(doc_text, needle, str(DOC_PATH.relative_to(ROOT)))

    full_pilots_text = read_text(FULL_PILOTS_DOC)
    for needle in REQUIRED_FULL_PILOTS_NEEDLES:
        require_contains(needle=needle, text=full_pilots_text, label=str(FULL_PILOTS_DOC.relative_to(ROOT)))

    validate_registry()

    evals_text = read_text(EVALS_PATH)
    for needle in REQUIRED_EVAL_NEEDLES:
        require_contains(evals_text, needle, str(EVALS_PATH.relative_to(ROOT)))

    print(f"promotion status ok: {REGISTRY_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
