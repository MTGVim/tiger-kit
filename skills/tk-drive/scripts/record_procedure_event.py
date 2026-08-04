#!/usr/bin/env python3
"""Append one evaluation-only procedure invocation event."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys


PHASES = {
    "aggregate verification",
    "remote-publish",
    "tk-drive finalization",
    "tk-grill-me",
    "tk-pr-rebase",
    "tk-pr-respond",
    "tk-pr-sweep",
    "tk-pr-triage",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-prototype",
    "tk-implement",
    "tk-browser-verify",
    "tk-merge-conflict",
}


def main(arguments: list[str]) -> int:
    try:
        if len(arguments) != 1 or arguments[0] not in PHASES:
            raise ValueError("usage: record_procedure_event.py <canonical-phase>")
        raw_path = os.environ.get("TK_DRIVE_PROCEDURE_LOG", "")
        path = Path(raw_path)
        if not raw_path or not path.is_absolute() or not path.parent.is_dir():
            raise ValueError(
                "TK_DRIVE_PROCEDURE_LOG must name an absolute path in an existing directory"
            )
        payload = (
            json.dumps(
                {"type": "phase_invocation", "phase": arguments[0]},
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
        flags = os.O_APPEND | os.O_CREAT | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags, 0o600)
        try:
            os.fchmod(descriptor, 0o600)
            if os.write(descriptor, payload) != len(payload):
                raise OSError("short write while recording procedure event")
        finally:
            os.close(descriptor)
    except (OSError, ValueError) as exc:
        print(f"record_procedure_event.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
