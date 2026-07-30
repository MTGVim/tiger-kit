#!/usr/bin/env python3
"""Create and strictly parse a sealed TigerKit preparation manifest."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "tigerkit.prep/v1"
STATUSES = {"ready", "active", "completed", "invalid", "failed"}
TERMINAL_STATUSES = {"completed", "invalid", "failed"}
TOP_LEVEL_KEYS = {
    "schema_version",
    "prep_id",
    "task",
    "repository",
    "digests",
    "ticket_mode",
    "status",
    "claim",
    "timestamps",
}
DIGEST_KEYS = {
    "source",
    "dirty_inventory",
    "instructions",
    "spec",
    "tickets",
    "verification_profile",
}
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
PREP_ID = re.compile(r"^prep-[0-9a-f]{16}$")
RFC3339_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class ManifestError(ValueError):
    """The preparation document or its inputs violate the public contract."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(value: str, label: str) -> Any:
    try:
        return json.loads(value, object_pairs_hook=_strict_object)
    except (json.JSONDecodeError, ManifestError) as error:
        raise ManifestError(f"{label}: invalid strict JSON: {error}") from error


def _require_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise ManifestError(f"{label}: expected object")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ManifestError(f"{label}: missing={missing} extra={extra}")
    return value


def _require_string(value: Any, label: str) -> str:
    if type(value) is not str or not value:
        raise ManifestError(f"{label}: expected non-empty string")
    return value


def _require_string_list(
    value: Any, label: str, *, allow_empty: bool = False
) -> list[str]:
    if type(value) is not list or (not value and not allow_empty):
        qualifier = "" if allow_empty else "non-empty "
        raise ManifestError(f"{label}: expected {qualifier}string array")
    if any(type(item) is not str or not item for item in value):
        raise ManifestError(f"{label}: expected non-empty string array")
    if len(set(value)) != len(value):
        raise ManifestError(f"{label}: duplicate item")
    return value


def _require_optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _require_string(value, label)


def _require_timestamp(
    value: Any, label: str, optional: bool = False
) -> datetime | None:
    if optional and value is None:
        return None
    text = _require_string(value, label)
    if not RFC3339_UTC.fullmatch(text):
        raise ManifestError(f"{label}: expected UTC RFC3339 timestamp")
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise ManifestError(f"{label}: invalid UTC RFC3339 timestamp") from error


def validate_header(value: Any) -> dict[str, Any]:
    header = _require_keys(value, TOP_LEVEL_KEYS, "manifest")
    if header["schema_version"] != SCHEMA_VERSION:
        raise ManifestError("manifest.schema_version: unsupported schema")
    if type(header["prep_id"]) is not str or not PREP_ID.fullmatch(
        header["prep_id"]
    ):
        raise ManifestError("manifest.prep_id: invalid preparation identity")

    task = _require_keys(header["task"], {"id", "anchors"}, "manifest.task")
    _require_string(task["id"], "manifest.task.id")
    anchors = _require_string_list(task["anchors"], "manifest.task.anchors")
    if anchors != sorted(anchors):
        raise ManifestError("manifest.task.anchors: expected canonical order")

    repository = _require_keys(
        header["repository"],
        {"root", "worktree", "branch", "base_head"},
        "manifest.repository",
    )
    for key in ("root", "worktree", "branch"):
        _require_string(repository[key], f"manifest.repository.{key}")
    for key in ("root", "worktree"):
        if not Path(repository[key]).is_absolute():
            raise ManifestError(f"manifest.repository.{key}: expected absolute path")
    try:
        Path(repository["worktree"]).relative_to(Path(repository["root"]))
    except ValueError as error:
        raise ManifestError(
            "manifest.repository.worktree: must be inside repository root"
        ) from error
    if type(repository["base_head"]) is not str or not HEX_40.fullmatch(
        repository["base_head"]
    ):
        raise ManifestError("manifest.repository.base_head: expected 40 hex characters")

    digests = _require_keys(header["digests"], DIGEST_KEYS, "manifest.digests")
    for key, digest in digests.items():
        if type(digest) is not str or not HEX_64.fullmatch(digest):
            raise ManifestError(f"manifest.digests.{key}: expected sha256")

    if type(header["ticket_mode"]) is not str or header["ticket_mode"] not in {
        "tickets",
        "no-ticket",
    }:
        raise ManifestError("manifest.ticket_mode: unsupported mode")
    if type(header["status"]) is not str or header["status"] not in STATUSES:
        raise ManifestError("manifest.status: unsupported state")

    claim = _require_keys(header["claim"], {"actor", "id"}, "manifest.claim")
    actor = _require_optional_string(claim["actor"], "manifest.claim.actor")
    claim_id = _require_optional_string(claim["id"], "manifest.claim.id")
    if (actor is None) != (claim_id is None):
        raise ManifestError("manifest.claim: actor and id must change together")

    timestamps = _require_keys(
        header["timestamps"],
        {"created_at", "claimed_at", "finished_at"},
        "manifest.timestamps",
    )
    created_at = _require_timestamp(
        timestamps["created_at"], "manifest.timestamps.created_at"
    )
    claimed_at = _require_timestamp(
        timestamps["claimed_at"], "manifest.timestamps.claimed_at", optional=True
    )
    finished_at = _require_timestamp(
        timestamps["finished_at"], "manifest.timestamps.finished_at", optional=True
    )
    if claimed_at is not None and claimed_at < created_at:
        raise ManifestError("manifest.timestamps: claimed_at precedes created_at")
    if finished_at is not None:
        lower_bound = claimed_at if claimed_at is not None else created_at
        if finished_at < lower_bound:
            raise ManifestError("manifest.timestamps: finished_at precedes run start")

    identity = {
        key: header[key]
        for key in (
            "schema_version",
            "task",
            "repository",
            "digests",
            "ticket_mode",
        )
    }
    expected_prep_id = f"prep-{_digest(_canonical_json(identity))[:16]}"
    if header["prep_id"] != expected_prep_id:
        raise ManifestError("manifest.prep_id: does not match canonical identity")

    status = header["status"]
    has_claim = actor is not None
    if has_claim != (claimed_at is not None):
        raise ManifestError("manifest: claim identity and claimed_at must change together")
    if status == "ready" and (
        has_claim or finished_at is not None
    ):
        raise ManifestError("manifest: ready state cannot contain claim or finish data")
    if status == "active" and (
        not has_claim or finished_at is not None
    ):
        raise ManifestError("manifest: active state requires claim data only")
    if status in {"completed", "failed"} and not has_claim:
        raise ManifestError(f"manifest: {status} state requires claim data")
    if status in TERMINAL_STATUSES and finished_at is None:
        raise ManifestError("manifest: terminal state requires finished_at")
    return header


def render_document(header: dict[str, Any], body: str) -> str:
    payload = json.dumps(
        header,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    normalized_body = body.rstrip() + "\n"
    return f"```json\n{payload}\n```\n\n{normalized_body}"


def parse_document(document: str) -> tuple[dict[str, Any], str]:
    if not document.startswith("```json\n"):
        raise ManifestError("manifest: strict JSON fence must be the first bytes")
    marker = "\n```\n"
    marker_index = document.find(marker, len("```json\n"))
    if marker_index < 0:
        raise ManifestError("manifest: missing JSON fence terminator")
    payload = document[len("```json\n") : marker_index]
    body = document[marker_index + len(marker) :]
    if not body.startswith("\n# TigerKit preparation\n"):
        raise ManifestError("manifest: Markdown reference body is missing")
    header = _load_json(payload, "manifest")
    return validate_header(header), body.lstrip("\n")


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _relative_reference(path: Path, worktree: Path, label: str) -> str:
    try:
        return path.resolve().relative_to(worktree.resolve()).as_posix()
    except ValueError as error:
        raise ManifestError(f"{label}: must be inside the worktree") from error


def _read_ready(path: Path, status: str, label: str) -> bytes:
    try:
        content = path.read_bytes()
    except OSError as error:
        raise ManifestError(f"{label}: cannot read {path}: {error}") from error
    if status.encode("utf-8") not in content.splitlines():
        raise ManifestError(f"{label}: required {status}")
    return content


def _single_line(value: str, label: str) -> str:
    _require_string(value, label)
    if "\n" in value or "\r" in value or "`" in value:
        raise ManifestError(f"{label}: expected one backtick-free line")
    return value


def build_ready_document(arguments: argparse.Namespace) -> str:
    worktree = Path(arguments.worktree).resolve()
    repository_root = Path(arguments.repository_root).resolve()
    output = Path(arguments.output).resolve()
    expected_output = worktree / ".tigerkit" / "prep.md"
    if output != expected_output:
        raise ManifestError("output: expected <worktree>/.tigerkit/prep.md")
    if not worktree.is_dir() or not repository_root.is_dir():
        raise ManifestError("repository identity: root and worktree must exist")
    try:
        worktree.relative_to(repository_root)
    except ValueError as error:
        raise ManifestError("repository identity: worktree must be inside root") from error

    source = _single_line(arguments.source, "source")
    prior_art_ref = _single_line(arguments.prior_art_ref, "prior-art-ref")
    task_anchors = sorted(
        _require_string_list(arguments.task_anchor, "task anchors")
    )
    dirty_inventory = _load_json(
        arguments.dirty_inventory_json, "dirty inventory"
    )
    instruction_inventory = _load_json(
        arguments.instruction_inventory_json, "instruction inventory"
    )
    profile = _require_keys(
        _load_json(arguments.verification_profile_json, "verification profile"),
        {"obligations", "signals"},
        "verification profile",
    )
    dirty_inventory = sorted(
        _require_string_list(
            dirty_inventory, "dirty inventory", allow_empty=True
        )
    )
    instruction_inventory = sorted(
        _require_string_list(
            instruction_inventory, "instruction inventory", allow_empty=True
        )
    )
    verification_profile = {
        "obligations": sorted(
            _require_string_list(
                profile["obligations"], "verification profile obligations"
            )
        ),
        "signals": sorted(
            _require_string_list(profile["signals"], "verification profile signals")
        ),
    }

    spec_path = Path(arguments.spec).resolve()
    spec_content = _read_ready(spec_path, "Status: Ready", "spec")
    spec_ref = _relative_reference(spec_path, worktree, "spec")

    if arguments.ticket_mode == "tickets":
        if arguments.tickets is None:
            raise ManifestError("tickets: required in tickets mode")
        tickets_path = Path(arguments.tickets).resolve()
        tickets_content = _read_ready(tickets_path, "Status: Pass", "tickets")
        tickets_ref = f"`{_relative_reference(tickets_path, worktree, 'tickets')}`"
        tickets_digest = _digest(tickets_content)
    else:
        if arguments.tickets is not None:
            raise ManifestError("tickets: prohibited in no-ticket mode")
        tickets_ref = "no-ticket single slice"
        tickets_digest = _digest(b'{"mode":"no-ticket"}')

    digests = {
        "source": _digest(source.encode("utf-8")),
        "dirty_inventory": _digest(_canonical_json(dirty_inventory)),
        "instructions": _digest(_canonical_json(instruction_inventory)),
        "spec": _digest(spec_content),
        "tickets": tickets_digest,
        "verification_profile": _digest(_canonical_json(verification_profile)),
    }
    identity = {
        "schema_version": SCHEMA_VERSION,
        "task": {"id": arguments.task_id, "anchors": task_anchors},
        "repository": {
            "root": str(repository_root),
            "worktree": str(worktree),
            "branch": arguments.branch,
            "base_head": arguments.base_head,
        },
        "digests": digests,
        "ticket_mode": arguments.ticket_mode,
    }
    prep_id = f"prep-{_digest(_canonical_json(identity))[:16]}"
    header = {
        **identity,
        "prep_id": prep_id,
        "status": "ready",
        "claim": {"actor": None, "id": None},
        "timestamps": {
            "created_at": arguments.created_at,
            "claimed_at": None,
            "finished_at": None,
        },
    }
    validate_header(header)
    body = "\n".join(
        (
            "# TigerKit preparation",
            "",
            "## References",
            "",
            f"- Task: `{arguments.task_id}`",
            f"- Source: `{source}`",
            f"- Spec: `{spec_ref}`",
            f"- Tickets: {tickets_ref}",
            "- Verification profile: `digests.verification_profile`",
            f"- Prior-art disposition: {prior_art_ref}",
        )
    )
    document = render_document(header, body)
    parsed, _ = parse_document(document)
    if parsed != header:
        raise ManifestError("manifest: generated document failed strict reread")
    return document


def create_ready_manifest(arguments: argparse.Namespace) -> dict[str, Any]:
    document = build_ready_document(arguments)
    output = Path(arguments.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    directory_fd = os.open(output.parent, os.O_RDONLY)
    temporary_path: Path | None = None
    try:
        try:
            fcntl.flock(directory_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ManifestError("manifest: another prep state mutation is active") from error
        if output.exists():
            current, _ = parse_document(output.read_text(encoding="utf-8"))
            if current["status"] == "active":
                raise ManifestError("manifest: active prep cannot be replaced")
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output.parent,
            prefix=".prep.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(document)
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, output)
        os.fsync(directory_fd)
        verified_header, _ = parse_document(output.read_text(encoding="utf-8"))
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    finally:
        fcntl.flock(directory_fd, fcntl.LOCK_UN)
        os.close(directory_fd)
    return verified_header


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument("--output", required=True)
    create.add_argument("--task-id", required=True)
    create.add_argument("--task-anchor", action="append", required=True)
    create.add_argument("--repository-root", required=True)
    create.add_argument("--worktree", required=True)
    create.add_argument("--branch", required=True)
    create.add_argument("--base-head", required=True)
    create.add_argument("--source", required=True)
    create.add_argument("--dirty-inventory-json", required=True)
    create.add_argument("--instruction-inventory-json", required=True)
    create.add_argument("--spec", required=True)
    create.add_argument(
        "--ticket-mode", choices=("tickets", "no-ticket"), required=True
    )
    create.add_argument("--tickets")
    create.add_argument("--verification-profile-json", required=True)
    create.add_argument("--prior-art-ref", required=True)
    create.add_argument("--created-at", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("path")
    return parser.parse_args(argv)


def main() -> int:
    arguments = parse_args()
    try:
        if arguments.command == "create":
            header = create_ready_manifest(arguments)
        else:
            path = Path(arguments.path)
            header, _ = parse_document(path.read_text(encoding="utf-8"))
    except (ManifestError, OSError) as error:
        print(f"prep manifest error: {error}", file=os.sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "path": str(
                    Path(arguments.output if arguments.command == "create" else arguments.path)
                ),
                "prep_id": header["prep_id"],
                "status": header["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
