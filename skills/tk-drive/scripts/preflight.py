#!/usr/bin/env python3
"""Write and inspect the compact TigerKit drive preflight."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any
from urllib.parse import urlsplit


TOP_KEYS = {"task", "repository", "execution", "browser", "sources"}
TASK_KEYS = {"goal", "included_scope", "excluded_scope", "confirmed_decisions"}
REPOSITORY_KEYS = {
    "root",
    "worktree",
    "branch",
    "baseline_head",
    "dirty_paths",
}
EXECUTION_KEYS = {"procedure_graph", "verification_profile"}
PROFILE_KEYS = {"signals", "obligations"}
BROWSER_KEYS = {
    "decision",
    "environment_url",
    "account_role_or_tenant_class",
    "opaque_profile_hint",
    "authentication_expectation",
    "ask_identity_on_cold_start",
}
SOURCE_KEYS = {"spec", "tickets"}
RESUME_KEYS = {
    "material_decisions_unresolved",
    "ready_spec",
    "multiple_units",
    "valid_tickets",
    "incomplete_units",
    "implementation_changed",
    "aggregate_complete",
    "required_work_complete",
}
FORBIDDEN_KEYS = {
    "status",
    "claim",
    "claim_id",
    "actor",
    "lock",
    "phase_cursor",
    "cursor",
    "receipt",
    "transition",
    "transition_debt",
    "finalization_event",
    "credential",
    "credentials",
    "cookie",
    "cookies",
    "token",
    "tokens",
    "otp",
    "password",
    "exact_identity",
}
SECRET_PATTERN = re.compile(
    r"(?i)(?:bearer\s+[a-z0-9._~-]+|password\s*[:=]|token\s*[:=]|cookie\s*[:=]|otp\s*[:=])"
)
HEAD = re.compile(r"^[0-9a-f]{40}$")
OPAQUE_HINT = re.compile(r"^opaque:[A-Za-z0-9._-]{1,64}$")
SAFE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._:/-]{0,199}$")
AUTH_EXPECTATIONS = {"pre-authenticated", "interactive-login-required", "no-auth"}
BROWSER_DECISIONS = {"required", "optional", "N/A"}


class PreflightError(ValueError):
    pass


def _object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise PreflightError(f"{label}: expected exactly {', '.join(sorted(keys))}")
    return value


def _strings(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() and len(item) <= 500 for item in value
    ):
        raise PreflightError(f"{label}: expected bounded non-empty string list")
    if not allow_empty and not value:
        raise PreflightError(f"{label}: list must not be empty")
    return value


def _reject_forbidden(value: Any, label: str = "preflight") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or key.casefold() in FORBIDDEN_KEYS:
                raise PreflightError(f"{label}: prohibited field {key!r}")
            _reject_forbidden(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_forbidden(child, f"{label}[{index}]")
    elif isinstance(value, str) and SECRET_PATTERN.search(value):
        raise PreflightError(f"{label}: secret-like value is prohibited")


def _safe_environment(value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 500:
        raise PreflightError("browser.environment_url: expected bounded string")
    if "://" not in value:
        if not SAFE_LABEL.fullmatch(value):
            raise PreflightError("browser.environment_url: unsafe environment label")
        return value
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise PreflightError("browser.environment_url: URL must not carry identity or secrets")
    return value


def validate_preflight(value: Any) -> dict[str, Any]:
    _reject_forbidden(value)
    root = _object(value, TOP_KEYS, "preflight")
    task = _object(root["task"], TASK_KEYS, "task")
    repository = _object(root["repository"], REPOSITORY_KEYS, "repository")
    execution = _object(root["execution"], EXECUTION_KEYS, "execution")
    profile = _object(
        execution["verification_profile"], PROFILE_KEYS, "verification_profile"
    )
    browser = _object(root["browser"], BROWSER_KEYS, "browser")
    sources = _object(root["sources"], SOURCE_KEYS, "sources")

    if not isinstance(task["goal"], str) or not task["goal"].strip():
        raise PreflightError("task.goal: expected non-empty string")
    for key in ("included_scope", "excluded_scope", "confirmed_decisions"):
        _strings(task[key], f"task.{key}")

    repository_root = Path(str(repository["root"]))
    worktree = Path(str(repository["worktree"]))
    if not repository_root.is_absolute() or not worktree.is_absolute():
        raise PreflightError("repository paths must be absolute")
    resolved_root = repository_root.resolve()
    resolved_worktree = worktree.resolve()
    try:
        resolved_worktree.relative_to(resolved_root)
    except ValueError as exc:
        raise PreflightError("repository.worktree must be contained by repository.root") from exc
    if not isinstance(repository["branch"], str) or not repository["branch"].strip():
        raise PreflightError("repository.branch: expected non-empty string")
    if not isinstance(repository["baseline_head"], str) or not HEAD.fullmatch(
        repository["baseline_head"]
    ):
        raise PreflightError("repository.baseline_head: expected lowercase 40-hex")
    _strings(repository["dirty_paths"], "repository.dirty_paths")

    _strings(execution["procedure_graph"], "execution.procedure_graph", allow_empty=False)
    _strings(profile["signals"], "verification_profile.signals")
    _strings(profile["obligations"], "verification_profile.obligations")

    decision = browser["decision"]
    if decision not in BROWSER_DECISIONS:
        raise PreflightError("browser.decision: expected required, optional, or N/A")
    runtime_keys = (
        "environment_url",
        "account_role_or_tenant_class",
        "opaque_profile_hint",
        "authentication_expectation",
        "ask_identity_on_cold_start",
    )
    if decision == "required":
        _safe_environment(browser["environment_url"])
        role = browser["account_role_or_tenant_class"]
        if not isinstance(role, str) or not SAFE_LABEL.fullmatch(role) or "@" in role:
            raise PreflightError("browser account role must be a non-identifying label")
        hint = browser["opaque_profile_hint"]
        if hint is not None and (
            not isinstance(hint, str) or not OPAQUE_HINT.fullmatch(hint)
        ):
            raise PreflightError("browser opaque profile hint must use opaque:<id>")
        if browser["authentication_expectation"] not in AUTH_EXPECTATIONS:
            raise PreflightError("browser authentication expectation is unsupported")
        if not isinstance(browser["ask_identity_on_cold_start"], bool):
            raise PreflightError("browser cold-start identity flag must be boolean")
    elif any(browser[key] is not None for key in runtime_keys):
        raise PreflightError("browser runtime fields are allowed only when required")

    if sources["spec"] not in {None, ".tigerkit/spec.md"}:
        raise PreflightError("sources.spec: unsupported reference")
    if sources["tickets"] not in {None, ".tigerkit/tickets.md"}:
        raise PreflightError("sources.tickets: unsupported reference")
    return root


def render_preflight(value: Any) -> bytes:
    validated = validate_preflight(value)
    payload = json.dumps(
        validated, ensure_ascii=False, indent=2, sort_keys=True
    )
    return f"# TigerKit preflight\n\n```json\n{payload}\n```\n".encode("utf-8")


def parse_preflight(content: bytes) -> dict[str, Any]:
    text = content.decode("utf-8")
    prefix = "# TigerKit preflight\n\n```json\n"
    suffix = "\n```\n"
    if not text.startswith(prefix) or not text.endswith(suffix):
        raise PreflightError("preflight document shape is invalid")
    try:
        value = json.loads(text[len(prefix) : -len(suffix)])
    except json.JSONDecodeError as exc:
        raise PreflightError(f"preflight JSON is invalid: {exc}") from exc
    return validate_preflight(value)


def _validate_output_path(path: Path, worktree: Path) -> tuple[Path, Path]:
    if not worktree.is_absolute() or worktree.is_symlink():
        raise PreflightError("worktree must be an absolute non-symlink path")
    resolved_worktree = worktree.resolve()
    expected = resolved_worktree / ".tigerkit" / "prep.md"
    if path.is_symlink() or path.parent.is_symlink():
        raise PreflightError("preflight output must not use a symlink")
    if path.absolute() != expected or path.resolve(strict=False) != expected:
        raise PreflightError("preflight output must be <worktree>/.tigerkit/prep.md")
    return expected, resolved_worktree


def write_preflight(path: Path, worktree: Path, value: Any) -> dict[str, Any]:
    expected, _ = _validate_output_path(path, worktree)
    payload = render_preflight(value)
    expected.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if expected.parent.is_symlink():
        raise PreflightError("preflight directory must not be a symlink")
    temporary: Path | None = None
    try:
        descriptor, raw = tempfile.mkstemp(prefix=".prep.", dir=expected.parent)
        temporary = Path(raw)
        with os.fdopen(descriptor, "wb") as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, expected)
        temporary = None
        directory_fd = os.open(expected.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    reread = expected.read_bytes()
    if reread != payload:
        raise PreflightError("preflight strict reread mismatch")
    return parse_preflight(reread)


def choose_resume_action(value: Any) -> str:
    evidence = _object(value, RESUME_KEYS, "resume evidence")
    if not all(isinstance(evidence[key], bool) for key in RESUME_KEYS):
        raise PreflightError("resume evidence values must be booleans")
    if evidence["material_decisions_unresolved"]:
        return "tk-grill-me"
    if not evidence["ready_spec"]:
        return "tk-to-spec"
    if evidence["multiple_units"] and not evidence["valid_tickets"]:
        return "tk-to-tickets"
    if evidence["incomplete_units"]:
        return "tk-implement"
    if evidence["implementation_changed"] and not evidence["aggregate_complete"]:
        return "aggregate verification"
    if evidence["required_work_complete"] and evidence["aggregate_complete"]:
        return "tk-drive finalization"
    raise PreflightError("resume evidence is incomplete or contradictory")


def browser_identity_action(preflight: Any, *, cold_start: bool) -> str:
    browser = validate_preflight(preflight)["browser"]
    if browser["decision"] != "required":
        return "not-applicable"
    if (
        cold_start
        and browser["ask_identity_on_cold_start"]
        and browser["opaque_profile_hint"] is None
    ):
        return "ask-once"
    return "ready"


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("write")
    write.add_argument("path")
    write.add_argument("--worktree", required=True)
    write.add_argument("--input", required=True)
    resume = commands.add_parser("resume")
    resume.add_argument("--evidence", required=True)
    parsed = parser.parse_args(arguments)
    try:
        if parsed.command == "write":
            value = json.loads(Path(parsed.input).read_text(encoding="utf-8"))
            result = write_preflight(
                Path(parsed.path), Path(parsed.worktree), value
            )
            print(json.dumps({"written": True, "fields": sorted(result)}))
        else:
            value = json.loads(Path(parsed.evidence).read_text(encoding="utf-8"))
            print(json.dumps({"next_action": choose_resume_action(value)}))
    except (OSError, json.JSONDecodeError, PreflightError) as exc:
        print(f"preflight.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
