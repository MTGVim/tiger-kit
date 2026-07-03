#!/usr/bin/env python3
"""Check TigerKit active command surface drift and banned token regressions."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / ".claude-plugin" / "plugin.json"
README_PATH = ROOT / "README.md"
USAGE_PATH = ROOT / ".tigerkit" / "docs" / "usage.md"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
OUTPUT_CONTRACT_PATH = ROOT / ".tigerkit" / "docs" / "output-contract.md"

EXPECTED_ACTIVE_COMMANDS = {
    "./commands/gap.md",
    "./commands/route.md",
    "./commands/reflect.md",
    "./commands/ui-diff.md",
    "./commands/grill.md",
    "./commands/prototype.md",
    "./commands/arch-review.md",
    "./commands/merge-conflict.md",
    "./commands/handoff.md",
    "./commands/to-prd.md",
    "./commands/to-issues.md",
}

README_COMMANDS = {
    "/tk:gap",
    "/tk:route",
    "/tk:reflect",
    "/tk:ui-diff",
    "/tk:grill",
    "/tk:prototype",
    "/tk:arch-review",
    "/tk:merge-conflict",
    "/tk:handoff",
    "/tk:to-prd",
    "/tk:to-issues",
}

STRICT_BANNED_TOKENS = [
    "/tk:" + "".join(["l", "a", "u", "n", "c", "h"]),
    "/tk:" + "".join(["e", "x", "e", "c", "u", "t", "e"]),
    "/tk:" + "-".join(["loop", "spec"]),
    "_".join(["GAP", "READY"]),
    "_".join(["GAP", "AUTO", "LAUNCHED"]),
]

CHECKED_PUBLIC_FILES = [
    README_PATH,
    USAGE_PATH,
    MARKETPLACE_PATH,
    OUTPUT_CONTRACT_PATH,
]


def fail(message: str) -> None:
    raise SystemExit(f"command surface drift check failed: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        raise SystemExit(f"invalid json: {path}: {exc}") from exc


def check_plugin_manifest() -> None:
    plugin = load_json(PLUGIN_PATH)
    raw_commands_obj: object = plugin.get("commands")
    if not isinstance(raw_commands_obj, list):
        fail(".claude-plugin/plugin.json commands must be a list")
    raw_commands = cast(list[object], raw_commands_obj)
    if not all(isinstance(command, str) for command in raw_commands):
        fail(".claude-plugin/plugin.json commands must contain only strings")
    commands = [command for command in raw_commands if isinstance(command, str)]
    command_set = set(commands)
    if command_set != EXPECTED_ACTIVE_COMMANDS:
        fail(
            f"plugin command set mismatch: expected {sorted(EXPECTED_ACTIVE_COMMANDS)!r}, "
            f"got {sorted(command_set)!r}"
        )


def check_readme_commands() -> None:
    text = README_PATH.read_text()
    for command in sorted(README_COMMANDS):
        if command not in text:
            fail(f"README.md missing active command {command}")


def check_banned_tokens() -> None:
    for path in CHECKED_PUBLIC_FILES:
        text = path.read_text()
        for token in STRICT_BANNED_TOKENS:
            if token in text:
                fail(f"public surface file {path.relative_to(ROOT)} still exposes banned token {token!r}")


def main() -> int:
    check_plugin_manifest()
    check_readme_commands()
    check_banned_tokens()
    print("command surface drift ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
