#!/usr/bin/env python3
"""Safely apply one reflection candidate to an existing local rule file."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile


class GuardError(RuntimeError):
    """A pre-write eligibility or containment check failed."""


class PostWriteError(RuntimeError):
    """A post-write invariant or validator failed."""


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def _normalized_relative(value: str) -> Path:
    if not value or "\x00" in value or any(character in value for character in "*?[]"):
        raise GuardError("repo target must be one exact non-glob repository-relative path")
    path = Path(value)
    if path.is_absolute() or path.as_posix() != value or any(part == ".." for part in path.parts):
        raise GuardError("repo target must be one normalized repository-relative path")
    return path


def _exact_absolute(value: str, label: str) -> Path:
    if not value or "\x00" in value or any(character in value for character in "*?[]"):
        raise GuardError(f"{label} must be one exact non-glob absolute path")
    path = Path(value)
    if not path.is_absolute() or path.absolute() != path:
        raise GuardError(f"{label} must be one exact absolute path")
    return path


def _assert_inside(root: Path, target: Path, label: str) -> None:
    resolved = target.resolve(strict=False)
    if resolved == root or root not in resolved.parents:
        raise GuardError(f"{label} escapes its allowed root")


def _assert_outside(root: Path, target: Path, label: str) -> None:
    resolved = target.resolve(strict=False)
    if resolved == root or root in resolved.parents:
        raise GuardError(f"{label} is repository-local and must use repo scope")


def _assert_no_symlink_chain(root: Path, target: Path, label: str) -> os.stat_result:
    _assert_inside(root, target, label)
    relative = target.relative_to(root)
    current = root
    target_stat: os.stat_result | None = None
    for part in relative.parts:
        current = current / part
        try:
            current_stat = current.lstat()
        except FileNotFoundError as exc:
            raise GuardError(f"{label} does not exist") from exc
        if stat.S_ISLNK(current_stat.st_mode):
            raise GuardError(f"{label} contains a symlink")
        target_stat = current_stat
    if target_stat is None:
        raise GuardError(f"{label} is not a file")
    return target_stat


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, content: bytes, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        view = memoryview(content)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def _secure_backup_root(repository: Path) -> Path:
    scratch = repository / ".tigerkit"
    if scratch.exists():
        scratch_stat = _assert_no_symlink_chain(
            repository, scratch, "TigerKit scratch directory"
        )
        if not stat.S_ISDIR(scratch_stat.st_mode):
            raise GuardError("TigerKit scratch path is not a directory")
    else:
        scratch.mkdir(mode=0o700)
    backup = scratch / "reflect-backup"
    if backup.exists():
        backup_stat = _assert_no_symlink_chain(repository, backup, "reflection backup")
        if not stat.S_ISDIR(backup_stat.st_mode):
            raise GuardError("reflection backup path is not a directory")
    else:
        backup.mkdir(mode=0o700)
    os.chmod(backup, 0o700)
    return backup


def _validator_commands(values: list[str]) -> list[list[str]]:
    commands: list[list[str]] = []
    for value in values:
        try:
            command = json.loads(value)
        except json.JSONDecodeError as exc:
            raise GuardError("validator command must be a JSON string array") from exc
        if (
            not isinstance(command, list)
            or not command
            or not all(
                isinstance(argument, str) and argument and "\x00" not in argument
                for argument in command
            )
        ):
            raise GuardError("validator command must be a non-empty JSON string array")
        commands.append(command)
    if not commands:
        raise GuardError("at least one post-write validator command is required")
    return commands


def _exact_repository(repository: Path) -> Path:
    raw_repository = repository
    repository = repository.resolve(strict=True)
    if not raw_repository.is_absolute() or raw_repository.absolute() != repository:
        raise GuardError("repository must be an exact absolute non-symlink path")
    top = _run(["git", "rev-parse", "--show-toplevel"], cwd=repository)
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != repository:
        raise GuardError("repository is not the exact Git worktree root")
    return repository


def _git_error(command: str, completed: subprocess.CompletedProcess[str]) -> GuardError:
    detail = completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"
    return GuardError(f"unable to determine target Git state with {command}: {detail}")


def _classify_repo_git(repository: Path, relative: Path) -> dict[str, str | None]:
    relative_text = relative.as_posix()
    tracked = _run(
        ["git", "ls-files", "--error-unmatch", "--", relative_text],
        cwd=repository,
    )
    if tracked.returncode == 0:
        raise GuardError("tracked targets are outside local auto-apply authority")
    if tracked.returncode != 1:
        raise _git_error("git ls-files", tracked)

    ignored = _run(
        ["git", "check-ignore", "-v", "--no-index", "--", relative_text],
        cwd=repository,
    )
    if ignored.returncode == 0:
        git_state = "untracked-ignored"
        first = next((line for line in ignored.stdout.splitlines() if line.strip()), "")
        ignore_source = first.split("\t", 1)[0] or None
    elif ignored.returncode == 1:
        git_state = "untracked-visible"
        ignore_source = None
    else:
        raise _git_error("git check-ignore", ignored)

    status_result = _run(
        [
            "git",
            "status",
            "--porcelain=v1",
            "--ignored",
            "--untracked-files=all",
            "--",
            relative_text,
        ],
        cwd=repository,
    )
    if status_result.returncode != 0:
        raise _git_error("git status", status_result)
    status_lines = [line for line in status_result.stdout.splitlines() if line.strip()]
    expected_prefix = "!!" if git_state == "untracked-ignored" else "??"
    if not any(line.startswith(expected_prefix) for line in status_lines):
        raise GuardError("target Git state is inconsistent across deterministic checks")
    return {
        "git_state": git_state,
        "ignore_source": ignore_source,
    }


def _resolve_target(
    *,
    repository: Path,
    scope: str,
    target_value: str,
) -> tuple[Path, str, dict[str, str | None]]:
    if scope == "repo":
        relative = _normalized_relative(target_value)
        target = repository / relative
        target_stat = _assert_no_symlink_chain(repository, target, "target")
        if not stat.S_ISREG(target_stat.st_mode):
            raise GuardError("target is not a regular file")
        state = _classify_repo_git(repository, relative)
        return target, relative.as_posix(), state

    target = _exact_absolute(target_value, "user target")
    user_root = Path.home().resolve(strict=True)
    _assert_inside(user_root, target, "user target")
    _assert_outside(repository, target, "user target")
    target_stat = _assert_no_symlink_chain(user_root, target, "user target")
    if not stat.S_ISREG(target_stat.st_mode):
        raise GuardError("user target is not a regular file")
    return target, str(target), {"git_state": "not-applicable", "ignore_source": None}


def apply_safe_rule(
    *,
    repository: Path,
    scope: str,
    target_value: str,
    baseline_sha256: str,
    candidate: Path,
    validators: list[list[str]],
    user_managed: bool,
) -> dict[str, str | None]:
    if not user_managed:
        raise GuardError("verified user-managed ownership assertion is required")
    repository = _exact_repository(repository)
    target, display_target, initial_state = _resolve_target(
        repository=repository,
        scope=scope,
        target_value=target_value,
    )
    target_stat = target.lstat()

    raw_candidate = candidate
    candidate = candidate.resolve(strict=True)
    if not raw_candidate.is_absolute() or raw_candidate.absolute() != candidate:
        raise GuardError("candidate must be an exact absolute non-symlink path")
    candidate_stat = _assert_no_symlink_chain(repository, candidate, "candidate")
    scratch = repository / ".tigerkit"
    if not stat.S_ISREG(candidate_stat.st_mode) or scratch not in candidate.parents:
        raise GuardError("candidate must be a regular file inside .tigerkit")
    if candidate == target:
        raise GuardError("candidate and target must be different files")

    if (
        len(baseline_sha256) != 64
        or any(character not in "0123456789abcdef" for character in baseline_sha256)
    ):
        raise GuardError("baseline SHA-256 must be 64 lowercase hexadecimal characters")
    before = target.read_bytes()
    if sha256_bytes(before) != baseline_sha256:
        raise GuardError("target changed since the reflection baseline")
    after = candidate.read_bytes()
    if after == before:
        return {
            "status": "no-op",
            "scope": scope,
            "target": display_target,
            "git_state": str(initial_state["git_state"]),
            "ignore_source": initial_state["ignore_source"],
            "before_sha256": baseline_sha256,
            "after_sha256": baseline_sha256,
        }

    backup_root = _secure_backup_root(repository)
    backup = backup_root / "before.bin"
    metadata = backup_root / "metadata.json"
    _atomic_write(backup, before, 0o600)
    metadata_content = (
        json.dumps(
            {
                "scope": scope,
                "target": display_target,
                "git_state": initial_state["git_state"],
                "ignore_source": initial_state["ignore_source"],
                "before_sha256": baseline_sha256,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    _atomic_write(metadata, metadata_content, 0o600)
    if sha256_bytes(backup.read_bytes()) != baseline_sha256:
        raise GuardError("secure backup verification failed before target mutation")

    original_mode = stat.S_IMODE(target_stat.st_mode)
    mutated = False
    try:
        _atomic_write(target, after, original_mode)
        mutated = True
        current_target, _, current_state = _resolve_target(
            repository=repository,
            scope=scope,
            target_value=target_value,
        )
        if current_target != target:
            raise PostWriteError("target identity changed after write")
        after_sha256 = sha256_bytes(after)
        if sha256_bytes(target.read_bytes()) != after_sha256:
            raise PostWriteError("post-write target hash mismatch")
        if current_state != initial_state:
            raise PostWriteError("target state changed during reflection apply")
        for index, command in enumerate(validators, 1):
            completed = _run(command, cwd=repository)
            if completed.returncode != 0:
                raise PostWriteError(
                    f"post-write validator {index} failed with exit {completed.returncode}"
                )
        return {
            "status": "applied",
            "scope": scope,
            "target": display_target,
            "git_state": str(initial_state["git_state"]),
            "ignore_source": initial_state["ignore_source"],
            "before_sha256": baseline_sha256,
            "after_sha256": after_sha256,
            "backup": str(backup.relative_to(repository)),
        }
    except (GuardError, OSError, PostWriteError, subprocess.TimeoutExpired) as exc:
        if not mutated:
            raise
        try:
            _atomic_write(target, before, original_mode)
            restored = sha256_bytes(target.read_bytes()) == baseline_sha256
        except OSError:
            restored = False
        if not restored:
            raise PostWriteError("post-write failure and exact rollback was not verified") from exc
        raise PostWriteError(f"{exc}; exact rollback verified") from exc


def parse_args(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--scope", required=True, choices=("repo", "user"))
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--baseline-sha256", required=True)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--user-managed", action="store_true")
    parser.add_argument(
        "--validate-json",
        action="append",
        default=[],
        help="repeatable JSON string array executed without a shell",
    )
    return parser.parse_args(arguments)


def main(arguments: list[str]) -> int:
    try:
        options = parse_args(arguments)
        result = apply_safe_rule(
            repository=options.repo,
            scope=options.scope,
            target_value=options.target,
            baseline_sha256=options.baseline_sha256,
            candidate=options.candidate,
            validators=_validator_commands(options.validate_json),
            user_managed=options.user_managed,
        )
    except GuardError as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}))
        return 2
    except PostWriteError as exc:
        status = (
            "rollback-unverified"
            if "rollback was not verified" in str(exc)
            else "rolled-back"
        )
        print(json.dumps({"status": status, "error": str(exc)}))
        return 4 if status == "rollback-unverified" else 3
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
