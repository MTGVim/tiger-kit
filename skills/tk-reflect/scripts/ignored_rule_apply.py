#!/usr/bin/env python3
"""Compatibility wrapper for the former ignored-only repository rule executor."""

from __future__ import annotations

import sys

from safe_rule_apply import main as safe_main


def main(arguments: list[str]) -> int:
    if not arguments:
        return safe_main(arguments)
    return safe_main(
        [
            arguments[0],
            "--scope",
            "repo",
            "--user-managed",
            *arguments[1:],
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
