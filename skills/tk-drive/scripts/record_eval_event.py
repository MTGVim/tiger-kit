#!/usr/bin/env python3
"""Append one strict tk-drive phase event to an evaluation-owned JSONL log."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


PHASES = {
    "tk-implement",
    "tk-reflect",
}
SUCCESS_STATES = {"Pass"}


def _event(arguments: list[str]) -> dict[str, str]:
    if len(arguments) == 2 and arguments[0] == "phase_invocation":
        event_type, phase = arguments
        if phase not in PHASES:
            raise ValueError(f"unsupported phase: {phase}")
        return {"type": event_type, "phase": phase}
    if len(arguments) == 4 and arguments[0] == "phase_receipt":
        event_type, phase, state, transition = arguments
        if phase not in PHASES:
            raise ValueError(f"unsupported phase: {phase}")
        if state not in SUCCESS_STATES:
            raise ValueError(f"unsupported success state: {state}")
        if not transition.strip() or len(transition) > 1000:
            raise ValueError("transition must contain 1-1000 non-whitespace characters")
        return {
            "type": event_type,
            "phase": phase,
            "state": state,
            "transition": transition,
        }
    raise ValueError(
        "usage: record_eval_event.py phase_invocation <phase> | "
        "phase_receipt <phase> <Pass> <transition>"
    )


def main(arguments: list[str]) -> int:
    try:
        event = _event(arguments)
        raw_path = os.environ.get("TK_DRIVE_EVENT_LOG", "")
        path = Path(raw_path)
        if not raw_path or not path.is_absolute() or not path.parent.is_dir():
            raise ValueError(
                "TK_DRIVE_EVENT_LOG must name an absolute path in an existing directory"
            )
        payload = (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
            "utf-8"
        )
        flags = os.O_APPEND | os.O_CREAT | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags, 0o600)
        try:
            os.fchmod(descriptor, 0o600)
            written = os.write(descriptor, payload)
            if written != len(payload):
                raise OSError("short write while recording evaluation event")
        finally:
            os.close(descriptor)
    except (OSError, ValueError) as exc:
        print(f"record_eval_event.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
