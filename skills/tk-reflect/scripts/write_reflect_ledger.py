#!/usr/bin/env python3
"""Atomically persist the bounded tk-reflect ledger."""

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


MAX_LEDGER_BYTES = 131072
FORBIDDEN_MARKERS = (
    b"diff --git ",
    b"-----BEGIN PRIVATE KEY-----",
    b"Authorization: Bearer ",
    b"Cookie: ",
)


class LedgerError(RuntimeError):
    pass


def _run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )


def _assert_inside(root: Path, target: Path, label: str) -> None:
    resolved = target.resolve(strict=False)
    if resolved == root or root not in resolved.parents:
        raise LedgerError(f"{label} escapes the repository")


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
            raise LedgerError(f"{label} does not exist") from exc
        if stat.S_ISLNK(current_stat.st_mode):
            raise LedgerError(f"{label} contains a symlink")
        target_stat = current_stat
    if target_stat is None:
        raise LedgerError(f"{label} is invalid")
    return target_stat


def _exact_repository(repository: Path) -> Path:
    raw = repository
    repository = repository.resolve(strict=True)
    if not raw.is_absolute() or raw.absolute() != repository:
        raise LedgerError("repository must be an exact absolute non-symlink path")
    top = _run(["git", "rev-parse", "--show-toplevel"], cwd=repository)
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != repository:
        raise LedgerError("repository is not the exact Git worktree root")
    return repository


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, content: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
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


def write_ledger(*, repository: Path, source: Path) -> dict[str, str]:
    repository = _exact_repository(repository)
    scratch = repository / ".tigerkit"
    if scratch.exists():
        scratch_stat = _assert_no_symlink_chain(repository, scratch, "TigerKit scratch")
        if not stat.S_ISDIR(scratch_stat.st_mode):
            raise LedgerError("TigerKit scratch is not a directory")
    else:
        scratch.mkdir(mode=0o700)
        _fsync_directory(repository)
    os.chmod(scratch, 0o700)

    raw_source = source
    source = source.resolve(strict=True)
    if not raw_source.is_absolute() or raw_source.absolute() != source:
        raise LedgerError("source must be an exact absolute non-symlink path")
    source_stat = _assert_no_symlink_chain(repository, source, "ledger source")
    if not stat.S_ISREG(source_stat.st_mode) or scratch not in source.parents:
        raise LedgerError("ledger source must be a regular file inside .tigerkit")

    target = scratch / "reflect.md"
    if source == target:
        raise LedgerError("ledger source and target must be different files")
    if target.exists():
        target_stat = _assert_no_symlink_chain(repository, target, "reflection ledger")
        if not stat.S_ISREG(target_stat.st_mode):
            raise LedgerError("reflection ledger is not a regular file")

    content = source.read_bytes()
    if not content or len(content) > MAX_LEDGER_BYTES:
        raise LedgerError("ledger must be non-empty and at most 131072 bytes")
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LedgerError("ledger must be UTF-8") from exc
    if not text.startswith("# Reflection ledger\n"):
        raise LedgerError("ledger must start with '# Reflection ledger'")
    if any(marker in content for marker in FORBIDDEN_MARKERS):
        raise LedgerError("ledger contains forbidden raw or sensitive material")

    _atomic_write(target, content)
    if target.read_bytes() != content:
        raise LedgerError("reflection ledger reread mismatch")
    digest = hashlib.sha256(content).hexdigest()
    return {
        "status": "written",
        "path": ".tigerkit/reflect.md",
        "sha256": digest,
    }


def parse_args(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    return parser.parse_args(arguments)


def main(arguments: list[str]) -> int:
    try:
        options = parse_args(arguments)
        result = write_ledger(repository=options.repo, source=options.source)
    except (LedgerError, OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
