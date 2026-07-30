#!/usr/bin/env python3
"""Validate, claim, and finalize one sealed TigerKit preparation."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator


SCHEMA = "tigerkit.prep/v1"
STATUSES = {"ready", "active", "completed", "invalid", "failed"}
TOP_KEYS = {
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
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class StateError(ValueError):
    """The preparation state cannot authorize the requested transition."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(text: str, label: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except (json.JSONDecodeError, StateError) as error:
        raise StateError(f"{label}: invalid strict JSON: {error}") from error


def _object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise StateError(f"{label}: expected object")
    actual = set(value)
    if actual != keys:
        raise StateError(
            f"{label}: missing={sorted(keys - actual)} extra={sorted(actual - keys)}"
        )
    return value


def _string(value: Any, label: str) -> str:
    if type(value) is not str or not value:
        raise StateError(f"{label}: expected non-empty string")
    return value


def _strings(
    value: Any, label: str, *, allow_empty: bool = False
) -> list[str]:
    if type(value) is not list or (not value and not allow_empty):
        raise StateError(f"{label}: expected string array")
    if any(type(item) is not str or not item for item in value):
        raise StateError(f"{label}: expected string array")
    if len(value) != len(set(value)):
        raise StateError(f"{label}: duplicate item")
    return sorted(value)


def _timestamp(value: Any, label: str, *, optional: bool = False):
    if optional and value is None:
        return None
    text = _string(value, label)
    try:
        parsed = datetime.strptime(text, TIMESTAMP_FORMAT)
    except ValueError as error:
        raise StateError(f"{label}: invalid UTC RFC3339 timestamp") from error
    if parsed.strftime(TIMESTAMP_FORMAT) != text:
        raise StateError(f"{label}: invalid UTC RFC3339 timestamp")
    return parsed


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def validate_header(value: Any) -> dict[str, Any]:
    header = _object(value, TOP_KEYS, "manifest")
    if header["schema_version"] != SCHEMA:
        raise StateError("manifest.schema_version: unsupported schema")
    if type(header["prep_id"]) is not str or not PREP_ID.fullmatch(
        header["prep_id"]
    ):
        raise StateError("manifest.prep_id: invalid identity")

    task = _object(header["task"], {"id", "anchors"}, "manifest.task")
    _string(task["id"], "manifest.task.id")
    anchors = _strings(task["anchors"], "manifest.task.anchors")
    if anchors != task["anchors"]:
        raise StateError("manifest.task.anchors: expected canonical order")

    repository = _object(
        header["repository"],
        {"root", "worktree", "branch", "base_head"},
        "manifest.repository",
    )
    for key in ("root", "worktree", "branch"):
        _string(repository[key], f"manifest.repository.{key}")
    for key in ("root", "worktree"):
        if not Path(repository[key]).is_absolute():
            raise StateError(f"manifest.repository.{key}: expected absolute path")
    try:
        Path(repository["worktree"]).relative_to(Path(repository["root"]))
    except ValueError as error:
        raise StateError("manifest.repository.worktree: outside root") from error
    if type(repository["base_head"]) is not str or not HEX_40.fullmatch(
        repository["base_head"]
    ):
        raise StateError("manifest.repository.base_head: expected 40 hex")

    digests = _object(header["digests"], DIGEST_KEYS, "manifest.digests")
    for key, value_digest in digests.items():
        if type(value_digest) is not str or not HEX_64.fullmatch(value_digest):
            raise StateError(f"manifest.digests.{key}: expected sha256")
    if type(header["ticket_mode"]) is not str or header["ticket_mode"] not in {
        "tickets",
        "no-ticket",
    }:
        raise StateError("manifest.ticket_mode: unsupported mode")
    if type(header["status"]) is not str or header["status"] not in STATUSES:
        raise StateError("manifest.status: unsupported state")

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
    expected_id = f"prep-{_digest(_canonical_json(identity))[:16]}"
    if header["prep_id"] != expected_id:
        raise StateError("manifest.prep_id: canonical identity mismatch")

    claim = _object(header["claim"], {"actor", "id"}, "manifest.claim")
    actor = claim["actor"]
    claim_id = claim["id"]
    for key, item in (("actor", actor), ("id", claim_id)):
        if item is not None:
            _string(item, f"manifest.claim.{key}")
    if (actor is None) != (claim_id is None):
        raise StateError("manifest.claim: actor and id must change together")

    timestamps = _object(
        header["timestamps"],
        {"created_at", "claimed_at", "finished_at"},
        "manifest.timestamps",
    )
    created_at = _timestamp(
        timestamps["created_at"], "manifest.timestamps.created_at"
    )
    claimed_at = _timestamp(
        timestamps["claimed_at"],
        "manifest.timestamps.claimed_at",
        optional=True,
    )
    finished_at = _timestamp(
        timestamps["finished_at"],
        "manifest.timestamps.finished_at",
        optional=True,
    )
    if claimed_at is not None and claimed_at < created_at:
        raise StateError("manifest.timestamps: claimed_at precedes created_at")
    if finished_at is not None:
        lower_bound = claimed_at if claimed_at is not None else created_at
        if finished_at < lower_bound:
            raise StateError("manifest.timestamps: finished_at precedes run")

    has_claim = actor is not None
    if has_claim != (claimed_at is not None):
        raise StateError("manifest: claim and claimed_at must change together")
    status = header["status"]
    if status == "ready" and (has_claim or finished_at is not None):
        raise StateError("manifest: ready contains run data")
    if status == "active" and (not has_claim or finished_at is not None):
        raise StateError("manifest: active requires claim data only")
    if status in {"completed", "failed"} and not has_claim:
        raise StateError(f"manifest: {status} requires a claim")
    if status in {"completed", "invalid", "failed"} and finished_at is None:
        raise StateError("manifest: terminal state requires finished_at")
    return header


def render_document(header: dict[str, Any], body: str) -> str:
    payload = json.dumps(
        header, ensure_ascii=False, indent=2, sort_keys=True
    )
    return f"```json\n{payload}\n```\n\n{body.rstrip()}\n"


def parse_document(document: str) -> tuple[dict[str, Any], str]:
    if not document.startswith("```json\n"):
        raise StateError("manifest: strict JSON fence must start at byte zero")
    marker = "\n```\n"
    end = document.find(marker, len("```json\n"))
    if end < 0:
        raise StateError("manifest: missing JSON fence terminator")
    body = document[end + len(marker) :]
    if not body.startswith("\n# TigerKit preparation\n") or "```" in body:
        raise StateError("manifest: invalid Markdown reference body")
    header = _load_json(document[len("```json\n") : end], "manifest")
    return validate_header(header), body.lstrip("\n")


def _reference(body: str, label: str) -> str:
    prefix = f"- {label}: "
    matches = [line[len(prefix) :] for line in body.splitlines() if line.startswith(prefix)]
    if len(matches) != 1:
        raise StateError(f"manifest body: expected one {label} reference")
    return matches[0]


def _inline_code(value: str, label: str) -> str:
    if len(value) < 2 or not value.startswith("`") or not value.endswith("`"):
        raise StateError(f"manifest body: invalid {label} reference")
    result = value[1:-1]
    if not result or "`" in result:
        raise StateError(f"manifest body: invalid {label} reference")
    return result


def _current_digests(
    header: dict[str, Any],
    body: str,
    arguments: argparse.Namespace,
    evidence: dict[str, Any],
) -> dict[str, str]:
    worktree = Path(arguments.worktree).resolve()
    source = _inline_code(_reference(body, "Source"), "Source")
    spec_ref = _inline_code(_reference(body, "Spec"), "Spec")
    if spec_ref != ".tigerkit/spec.md":
        raise StateError("manifest body: unsupported Spec reference")
    spec_path = worktree / spec_ref
    try:
        spec_content = spec_path.read_bytes()
    except OSError as error:
        raise StateError(f"spec drift: {error}") from error

    ticket_reference = _reference(body, "Tickets")
    if header["ticket_mode"] == "tickets":
        ticket_ref = _inline_code(ticket_reference, "Tickets")
        if ticket_ref != ".tigerkit/tickets.md":
            raise StateError("manifest body: unsupported Tickets reference")
        try:
            ticket_value = (worktree / ticket_ref).read_bytes()
        except OSError as error:
            raise StateError(f"tickets drift: {error}") from error
    else:
        if ticket_reference != "no-ticket single slice":
            raise StateError("manifest body: no-ticket reference mismatch")
        ticket_value = b'{"mode":"no-ticket"}'

    return {
        "source": _digest(source.encode("utf-8")),
        "dirty_inventory": _digest(_canonical_json(evidence["dirty"])),
        "instructions": _digest(_canonical_json(evidence["instructions"])),
        "spec": _digest(spec_content),
        "tickets": _digest(ticket_value),
        "verification_profile": _digest(_canonical_json(evidence["profile"])),
    }


@contextmanager
def _locked_directory(path: Path) -> Iterator[int]:
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise StateError("manifest: another state mutation is active") from error
        yield descriptor
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _atomic_write(
    path: Path,
    header: dict[str, Any],
    body: str,
    directory_fd: int,
) -> dict[str, Any]:
    document = render_document(header, body)
    validate_header(header)
    temporary_path: Path | None = None
    committed = False
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".prep-state.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(document)
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, path)
        committed = True
        os.fsync(directory_fd)
        verified, _ = parse_document(path.read_text(encoding="utf-8"))
        return verified
    except BaseException as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        if not committed:
            raise
        try:
            verified, _ = _read_path(path)
            transition_visible = verified == header
        except (OSError, StateError):
            transition_visible = False
        outcome = "committed" if transition_visible else "uncertain"
        raise StateError(
            f"manifest: transition {outcome} but durability verification failed; "
            f"inspect {path} before recovery"
        ) from error


def _read_path(path: Path) -> tuple[dict[str, Any], str]:
    if path.is_symlink():
        raise StateError("manifest: symbolic links are prohibited")
    try:
        document = path.read_text(encoding="utf-8")
    except OSError as error:
        raise StateError(f"manifest: cannot read {path}: {error}") from error
    return parse_document(document)


def _validate_claim_path(path: Path, worktree: Path) -> None:
    expected = worktree.resolve() / ".tigerkit" / "prep.md"
    if path.resolve() != expected:
        raise StateError("manifest: expected <worktree>/.tigerkit/prep.md")


def _claim_evidence(arguments: argparse.Namespace) -> dict[str, Any]:
    _string(arguments.actor, "actor")
    _string(arguments.claim_id, "claim id")
    _timestamp(arguments.claimed_at, "claimed at")
    _string(arguments.branch, "branch")
    if type(arguments.head) is not str or not HEX_40.fullmatch(arguments.head):
        raise StateError("head: expected 40 lowercase hex characters")
    repository_root = Path(arguments.repository_root)
    worktree = Path(arguments.worktree)
    if not repository_root.is_absolute() or not worktree.is_absolute():
        raise StateError("claim repository paths must be absolute")
    dirty = _strings(
        _load_json(arguments.dirty_inventory_json, "dirty inventory"),
        "dirty inventory",
        allow_empty=True,
    )
    instructions = _strings(
        _load_json(arguments.instruction_inventory_json, "instruction inventory"),
        "instruction inventory",
        allow_empty=True,
    )
    profile = _object(
        _load_json(arguments.verification_profile_json, "verification profile"),
        {"obligations", "signals"},
        "verification profile",
    )
    return {
        "dirty": dirty,
        "instructions": instructions,
        "profile": {
            "obligations": _strings(
                profile["obligations"], "verification profile obligations"
            ),
            "signals": _strings(
                profile["signals"], "verification profile signals"
            ),
        },
    }


def claim(arguments: argparse.Namespace) -> dict[str, Any]:
    path = Path(arguments.path)
    worktree = Path(arguments.worktree).resolve()
    evidence = _claim_evidence(arguments)
    _validate_claim_path(path, worktree)
    with _locked_directory(path) as directory_fd:
        header, body = _read_path(path)
        if header["status"] != "ready":
            raise StateError(
                f"manifest: claim requires ready, found {header['status']}"
            )

        drift: list[str] = []
        repository = header["repository"]
        expected_repository = {
            "root": str(Path(arguments.repository_root).resolve()),
            "worktree": str(worktree),
            "branch": arguments.branch,
            "base_head": arguments.head,
        }
        labels = {
            "root": "repository root drift",
            "worktree": "worktree drift",
            "branch": "branch drift",
            "base_head": "base HEAD drift",
        }
        for key, current in expected_repository.items():
            if repository[key] != current:
                drift.append(labels[key])
        try:
            current_digests = _current_digests(
                header, body, arguments, evidence
            )
        except StateError as error:
            drift.append(str(error))
            current_digests = {}
        for key, current in current_digests.items():
            if header["digests"][key] != current:
                drift.append(f"{key.replace('_', ' ')} drift")

        if drift:
            invalid = {
                **header,
                "status": "invalid",
                "timestamps": {
                    **header["timestamps"],
                    "finished_at": arguments.claimed_at,
                },
            }
            _atomic_write(path, invalid, body, directory_fd)
            raise StateError("; ".join(drift))

        active = {
            **header,
            "status": "active",
            "claim": {"actor": arguments.actor, "id": arguments.claim_id},
            "timestamps": {
                **header["timestamps"],
                "claimed_at": arguments.claimed_at,
            },
        }
        return _atomic_write(path, active, body, directory_fd)


def finalize(arguments: argparse.Namespace) -> dict[str, Any]:
    path = Path(arguments.path)
    with _locked_directory(path) as directory_fd:
        header, body = _read_path(path)
        expected = (
            Path(header["repository"]["worktree"]) / ".tigerkit" / "prep.md"
        )
        if path.resolve() != expected:
            raise StateError("manifest: finalize path does not match worktree")
        if header["status"] != "active":
            raise StateError(
                f"manifest: finalize requires active, found {header['status']}"
            )
        if header["claim"]["id"] != arguments.claim_id:
            raise StateError("manifest: claim identity mismatch")
        terminal = {
            **header,
            "status": arguments.status,
            "timestamps": {
                **header["timestamps"],
                "finished_at": arguments.finished_at,
            },
        }
        return _atomic_write(path, terminal, body, directory_fd)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("path")
    claim_parser = subparsers.add_parser("claim")
    claim_parser.add_argument("path")
    claim_parser.add_argument("--actor", required=True)
    claim_parser.add_argument("--claim-id", required=True)
    claim_parser.add_argument("--claimed-at", required=True)
    claim_parser.add_argument("--repository-root", required=True)
    claim_parser.add_argument("--worktree", required=True)
    claim_parser.add_argument("--branch", required=True)
    claim_parser.add_argument("--head", required=True)
    claim_parser.add_argument("--dirty-inventory-json", required=True)
    claim_parser.add_argument("--instruction-inventory-json", required=True)
    claim_parser.add_argument("--verification-profile-json", required=True)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("path")
    finalize_parser.add_argument("--claim-id", required=True)
    finalize_parser.add_argument(
        "--status", choices=("completed", "invalid", "failed"), required=True
    )
    finalize_parser.add_argument("--finished-at", required=True)
    return parser.parse_args(argv)


def main() -> int:
    arguments = parse_args()
    try:
        if arguments.command == "validate":
            header, _ = _read_path(Path(arguments.path))
        elif arguments.command == "claim":
            header = claim(arguments)
        else:
            header = finalize(arguments)
    except (OSError, StateError) as error:
        print(f"prep state error: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "path": arguments.path,
                "prep_id": header["prep_id"],
                "status": header["status"],
                "claim_id": header["claim"]["id"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
