#!/usr/bin/env python3
"""Check TigerKit active command surface drift and banned token regressions."""
from __future__ import annotations

import json
import re
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
    "./commands/learn.md",
    "./commands/browser-verify.md",
    "./commands/grill.md",
    "./commands/grooming.md",
    "./commands/prototype.md",
    "./commands/arch-review.md",
    "./commands/merge-conflict.md",
    "./commands/handoff.md",
    "./commands/handon.md",
    "./commands/to-prd.md",
    "./commands/to-issues.md",
}

README_COMMANDS = {
    "/tk:gap",
    "/tk:route",
    "/tk:reflect",
    "/tk:learn",
    "/tk:browser-verify",
    "/tk:grill",
    "/tk:grooming",
    "/tk:prototype",
    "/tk:arch-review",
    "/tk:merge-conflict",
    "/tk:handoff",
    "/tk:handon",
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

COMMAND_OUTPUT_PATHS = {
    "gap": ROOT / "commands" / "gap.md",
    "route": ROOT / "commands" / "route.md",
    "reflect": ROOT / "commands" / "reflect.md",
    "learn": ROOT / "commands" / "learn.md",
    "browser-verify": ROOT / "commands" / "browser-verify.md",
    "grill": ROOT / "commands" / "grill.md",
    "grooming": ROOT / "commands" / "grooming.md",
    "prototype": ROOT / "commands" / "prototype.md",
    "arch-review": ROOT / "commands" / "arch-review.md",
    "merge-conflict": ROOT / "commands" / "merge-conflict.md",
    "handoff": ROOT / "commands" / "handoff.md",
    "handon": ROOT / "commands" / "handon.md",
    "to-prd": ROOT / "commands" / "to-prd.md",
    "to-issues": ROOT / "commands" / "to-issues.md",
}

OUTPUT_SYNC_TARGETS = {
    "gap": "## `/tk:gap` Output Contract",
    "route": "## `/tk:route` Output Contract",
    "reflect": "## `/tk:reflect` Output Contract",
    "learn": "## `/tk:learn` Output Contract",
    "browser-verify": "## `/tk:browser-verify` Output Contract",
    "grill": "## `/tk:grill` Output Contract",
    "grooming": "## `/tk:grooming` Output Contract",
    "prototype": "## `/tk:prototype` Output Contract",
    "arch-review": "## `/tk:arch-review` Output Contract",
    "merge-conflict": "## `/tk:merge-conflict` Output Contract",
    "handoff": "## `/tk:handoff` Output Contract",
    "handon": "## `/tk:handon` Output Contract",
    "to-prd": "## `/tk:to-prd` Output Contract",
    "to-issues": "## `/tk:to-issues` Output Contract",
}

TEXT_OUTPUT_COMMANDS_NO_NONE = {
    "route",
    "learn",
    "browser-verify",
    "grill",
    "grooming",
    "prototype",
    "arch-review",
    "merge-conflict",
    "handoff",
    "handon",
    "to-prd",
    "to-issues",
    "browser-verify",
}

LEGACY_LABELS_WITHOUT_COLON = {
    "Why",
    "Tradeoffs",
    "Needs first",
    "First step",
    "Goal command",
    "다음 행동",
}

SECTION_LABEL_RE = re.compile(r"^\[?[A-Za-z가-힣][A-Za-z가-힣0-9 /-]*:\s*$")


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


def extract_first_fenced_block_after_heading(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start_index = next(index for index, line in enumerate(lines) if line.strip() == heading)
    except StopIteration as exc:
        fail(f"missing heading {heading!r} in output contract helper")
        raise AssertionError from exc

    fence_start = None
    for index in range(start_index + 1, len(lines)):
        if lines[index].strip().startswith("```"):
            fence_start = index
            break
    if fence_start is None:
        fail(f"missing fenced code block after heading {heading!r}")
        raise AssertionError

    fence_start_index = fence_start
    block_lines: list[str] = []
    for index in range(fence_start_index + 1, len(lines)):
        if lines[index].strip().startswith("```"):
            return "\n".join(block_lines).strip()
        block_lines.append(lines[index].rstrip())
    fail(f"unterminated fenced code block after heading {heading!r}")
    raise AssertionError


def extract_command_output_block(path: Path) -> str:
    text = path.read_text()
    lines = text.splitlines()
    for heading in ("## Output contract", "## Output"):
        for index, line in enumerate(lines):
            if line.strip() != heading:
                continue
            for fence_index in range(index + 1, len(lines)):
                if lines[fence_index].strip().startswith("```"):
                    block_lines: list[str] = []
                    for end_index in range(fence_index + 1, len(lines)):
                        if lines[end_index].strip().startswith("```"):
                            return "\n".join(block_lines).strip()
                        block_lines.append(lines[end_index].rstrip())
                    fail(f"unterminated fenced output block in {path.relative_to(ROOT)}")

    fail(f"missing output block in {path.relative_to(ROOT)}")
    raise AssertionError


def normalize_block(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def check_command_output_block_shape() -> None:
    for command_name, path in COMMAND_OUTPUT_PATHS.items():
        block = extract_command_output_block(path)
        if "다음 행동" in block:
            fail(f"{path.relative_to(ROOT)} output block still uses legacy label '다음 행동'")
        if command_name in TEXT_OUTPUT_COMMANDS_NO_NONE and "NONE" in block:
            fail(f"{path.relative_to(ROOT)} output block must omit NONE placeholders outside reflect receipts")

        lines = block.splitlines()
        for index, raw_line in enumerate(lines[:-1]):
            stripped = raw_line.strip()
            if stripped in LEGACY_LABELS_WITHOUT_COLON:
                fail(f"{path.relative_to(ROOT)} output block has legacy label without colon: {stripped!r}")
            if SECTION_LABEL_RE.match(stripped):
                if lines[index + 1].strip() == "":
                    fail(
                        f"{path.relative_to(ROOT)} output block leaves a blank line after section label {stripped!r}"
                    )


def check_output_contract_helper_sync() -> None:
    helper_text = OUTPUT_CONTRACT_PATH.read_text()
    for command_name, heading in OUTPUT_SYNC_TARGETS.items():
        helper_block = extract_first_fenced_block_after_heading(helper_text, heading)
        command_block = extract_command_output_block(COMMAND_OUTPUT_PATHS[command_name])
        if normalize_block(helper_block) != normalize_block(command_block):
            fail(
                f"output contract helper drift for {command_name}: "
                f"{OUTPUT_CONTRACT_PATH.relative_to(ROOT)} does not match {COMMAND_OUTPUT_PATHS[command_name].relative_to(ROOT)}"
            )


def main() -> int:
    check_plugin_manifest()
    check_readme_commands()
    check_banned_tokens()
    check_command_output_block_shape()
    check_output_contract_helper_sync()
    print("command surface drift ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
