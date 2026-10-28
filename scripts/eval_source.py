"""Narrow source identity for opt-in evaluation provenance (no paths or logs saved)."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True).stdout


def source_snapshot(root: Path) -> dict[str, str]:
    digest = hashlib.sha256()
    for entry in sorted(git(root, "ls-files", "--stage", "-z").split(b"\0")):
        if not entry:
            continue
        metadata, filename = entry.split(b"\t", 1)
        mode, _, stage = metadata.split()
        if stage != b"0" or mode not in {b"100644", b"100755", b"120000"}:
            raise ValueError("unmerged or unsupported eval source")
        path = root / os.fsdecode(filename)
        data = os.fsencode(os.readlink(path)) if mode == b"120000" else path.read_bytes()
        if mode != b"120000":
            mode = b"100755" if path.stat().st_mode & 0o111 else b"100644"
        digest.update(mode + b"\0" + filename + b"\0" + hashlib.sha256(data).digest())
    return {"commit": git(root, "rev-parse", "HEAD").decode().strip(),
            "tree": git(root, "rev-parse", "HEAD^{tree}").decode().strip(),
            "files_sha256": digest.hexdigest()}


def checkout_id(root: Path) -> str:
    return hashlib.sha256(os.fsencode(root.resolve())).hexdigest()
