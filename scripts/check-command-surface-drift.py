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
    "./commands/help.md",
    "./commands/route.md",
    "./commands/next.md",
    "./commands/quiz.md",
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
    "/tk:help",
    "/tk:gap",
    "/tk:route",
    "/tk:next",
    "/tk:quiz",
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
    "help": ROOT / "commands" / "help.md",
    "gap": ROOT / "commands" / "gap.md",
    "route": ROOT / "commands" / "route.md",
    "next": ROOT / "commands" / "next.md",
    "reflect": ROOT / "commands" / "reflect.md",
    "learn": ROOT / "commands" / "learn.md",
    "quiz": ROOT / "commands" / "quiz.md",
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

DESCRIPTION_BUDGET = 932

INLINE_BOOTSTRAP_TOKENS = [
    "python3 - <<'PY'",
    ".claude/plugins/cache/tiger-kit/tk",
    'TIGERKIT_STATE_SCRIPT="$({',
]

RELATIVE_HELPER_EXAMPLES = [
    "python3 scripts/resolve_tigerkit_state.py",
    "python3 scripts/tigerkit_state.py",
]

INSTALLED_HELPER_DOC_TARGETS = [
    ROOT / "commands" / "gap.md",
    ROOT / "commands" / "handon.md",
    ROOT / "commands" / "learn.md",
]

INSTALLED_HELPER_UPDATE_GUARD = "claude plugin marketplace update tiger-kit"

NO_NON_GOALS_COMMANDS = [
    ROOT / "commands" / "arch-review.md",
    ROOT / "commands" / "browser-verify.md",
    ROOT / "commands" / "grill.md",
    ROOT / "commands" / "grooming.md",
    ROOT / "commands" / "handoff.md",
    ROOT / "commands" / "handon.md",
    ROOT / "commands" / "learn.md",
    ROOT / "commands" / "merge-conflict.md",
    ROOT / "commands" / "prototype.md",
    ROOT / "commands" / "route.md",
    ROOT / "commands" / "to-issues.md",
    ROOT / "commands" / "to-prd.md",
]

SHARED_BOUNDARY_MARKER = "Shared command boundaries"

REHOMED_BOUNDARY_GUARDS = {
    ROOT / "commands" / "prototype.md": ["commit/push/merge 금지"],
    ROOT / "commands" / "merge-conflict.md": ["unrelated refactor 금지", "formatting-only churn 금지"],
    ROOT / "commands" / "grooming.md": ["신규 guidance를 임의 추가하지 않음", "reflect/learn 역할 대체 금지"],
}

WRAPPER_SKILL_COMMAND_OWNERS = {
    ROOT / "skills" / "arch-review" / "SKILL.md": "commands/arch-review.md",
    ROOT / "skills" / "gap" / "SKILL.md": "commands/gap.md",
    ROOT / "skills" / "grill" / "SKILL.md": "commands/grill.md",
    ROOT / "skills" / "grooming" / "SKILL.md": "commands/grooming.md",
    ROOT / "skills" / "handoff" / "SKILL.md": "commands/handoff.md",
    ROOT / "skills" / "handon" / "SKILL.md": "commands/handon.md",
    ROOT / "skills" / "learn" / "SKILL.md": "commands/learn.md",
    ROOT / "skills" / "merge-conflict" / "SKILL.md": "commands/merge-conflict.md",
    ROOT / "skills" / "prototype" / "SKILL.md": "commands/prototype.md",
    ROOT / "skills" / "reflect" / "SKILL.md": "commands/reflect.md",
    ROOT / "skills" / "route" / "SKILL.md": "commands/route.md",
    ROOT / "skills" / "to-issues" / "SKILL.md": "commands/to-issues.md",
    ROOT / "skills" / "to-prd" / "SKILL.md": "commands/to-prd.md",
}

WRAPPER_SKILL_TOTAL_BUDGET = 11000
WRAPPER_DISABLE_MODEL_INVOCATION_LINE = "disable-model-invocation: true"
BROWSER_VERIFY_ENTRY_SKILL_PATH = ROOT / "skills" / "browser-verify" / "SKILL.md"
BROWSER_VERIFY_ENTRY_BUDGET = 2048
BROWSER_VERIFY_CANONICAL_POLICY_PATH = ROOT / "commands" / "browser-verify.md"
BROWSER_VERIFY_REFERENCE_OWNERS = {
    ROOT / "skills" / "browser-verify" / "references" / "modes" / "env-diff.md": [
        "commands/browser-verify.md",
        "driver-agnostic 규칙",
    ],
    ROOT / "skills" / "browser-verify" / "references" / "modes" / "behavior-verify.md": [
        "commands/browser-verify.md",
        "Behavior 판정 규칙",
        "Mutation 안전",
    ],
    ROOT / "skills" / "browser-verify" / "references" / "drivers" / "cdp-direct.md": [
        "commands/browser-verify.md",
        "canonical policy",
    ],
}

OUTPUT_SYNC_TARGETS = {
    "help": "## `/tk:help` Output Contract",
    "gap": "## `/tk:gap` Output Contract",
    "route": "## `/tk:route` Output Contract",
    "next": "## `/tk:next` Output Contract",
    "reflect": "## `/tk:reflect` Output Contract",
    "learn": "## `/tk:learn` Output Contract",
    "quiz": "## `/tk:quiz` Output Contract",
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
    "help",
    "route",
    "next",
    "learn",
    "quiz",
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


def extract_frontmatter_description(path: Path) -> str:
    match = re.search(r"^description:\s*(.*)$", path.read_text(), re.M)
    return match.group(1).strip() if match else ""


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


def check_description_budget() -> None:
    total = 0
    for path in sorted((ROOT / "commands").glob("*.md")):
        total += len(extract_frontmatter_description(path))
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        total += len(extract_frontmatter_description(path))
    if total > DESCRIPTION_BUDGET:
        fail(f"command+skill description budget exceeded: {total} > {DESCRIPTION_BUDGET}")


def check_no_inline_state_bootstrap() -> None:
    for path in sorted((ROOT / "commands").glob("*.md")):
        text = path.read_text()
        for token in INLINE_BOOTSTRAP_TOKENS:
            if token in text:
                fail(f"{path.relative_to(ROOT)} still embeds inline TigerKit state bootstrap token {token!r}")


def check_helper_examples_are_repo_independent() -> None:
    for path in INSTALLED_HELPER_DOC_TARGETS:
        text = path.read_text()
        for token in RELATIVE_HELPER_EXAMPLES:
            if token in text:
                fail(f"{path.relative_to(ROOT)} still documents repo-local TigerKit helper invocation: {token!r}")
        if "claude plugin list --json" not in text:
            fail(f"{path.relative_to(ROOT)} missing installed-plugin helper resolution flow")
        if INSTALLED_HELPER_UPDATE_GUARD not in text:
            fail(f"{path.relative_to(ROOT)} missing stale-installed-plugin update guard")


def check_shared_boundary_reference() -> None:
    usage_text = USAGE_PATH.read_text()
    if SHARED_BOUNDARY_MARKER not in usage_text:
        fail(f"{USAGE_PATH.relative_to(ROOT)} missing shared command boundary reference section")
    for path in NO_NON_GOALS_COMMANDS:
        text = path.read_text()
        if "## Non-goals" in text:
            fail(f"{path.relative_to(ROOT)} still exposes a Non-goals section after boundary consolidation")
        if SHARED_BOUNDARY_MARKER not in text:
            fail(f"{path.relative_to(ROOT)} missing shared command boundary reference")
    for path, required_lines in REHOMED_BOUNDARY_GUARDS.items():
        text = path.read_text()
        for line in required_lines:
            if line not in text:
                fail(f"{path.relative_to(ROOT)} missing re-homed command-specific boundary: {line!r}")


def check_wrapper_skill_thinness() -> None:
    total_bytes = 0
    for path, command_owner in WRAPPER_SKILL_COMMAND_OWNERS.items():
        text = path.read_text()
        total_bytes += len(text.encode("utf-8"))
        if WRAPPER_DISABLE_MODEL_INVOCATION_LINE not in text:
            fail(
                f"{path.relative_to(ROOT)} missing wrapper disable-model-invocation frontmatter line"
            )
        if command_owner not in text:
            fail(f"{path.relative_to(ROOT)} missing canonical command owner reference {command_owner!r}")
        if "얇은 wrapper" not in text:
            fail(f"{path.relative_to(ROOT)} missing thin-wrapper marker")
    if total_bytes > WRAPPER_SKILL_TOTAL_BUDGET:
        fail(
            f"wrapper skill byte budget exceeded: {total_bytes} > {WRAPPER_SKILL_TOTAL_BUDGET}"
        )


def check_browser_verify_entry_skill_size() -> None:
    text = BROWSER_VERIFY_ENTRY_SKILL_PATH.read_text()
    size = len(text.encode("utf-8"))
    if size > BROWSER_VERIFY_ENTRY_BUDGET:
        fail(
            f"browser-verify entry skill byte budget exceeded: {size} > {BROWSER_VERIFY_ENTRY_BUDGET}"
        )
    if "commands/browser-verify.md" not in text:
        fail("skills/browser-verify/SKILL.md missing canonical command owner reference 'commands/browser-verify.md'")
    if "references/modes/env-diff.md" not in text:
        fail("skills/browser-verify/SKILL.md missing env-diff reference handoff")
    if "red-loop-first" not in text:
        fail("skills/browser-verify/SKILL.md missing red-loop-first boundary")


def check_browser_verify_reference_owners() -> None:
    policy_text = BROWSER_VERIFY_CANONICAL_POLICY_PATH.read_text()
    for required_heading in ("## Driver policy", "## Behavior 판정 규칙", "## Mutation 안전"):
        if required_heading not in policy_text:
            fail(f"commands/browser-verify.md missing canonical policy heading {required_heading!r}")
    for path, needles in BROWSER_VERIFY_REFERENCE_OWNERS.items():
        text = path.read_text()
        for needle in needles:
            if needle not in text:
                fail(f"{path.relative_to(ROOT)} missing browser-verify owner needle {needle!r}")
        if "skills/browser-verify/SKILL.md" in text and "commands/browser-verify.md" not in text:
            fail(f"{path.relative_to(ROOT)} still points canonical browser-verify policy at skills/browser-verify/SKILL.md")


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
    check_description_budget()
    check_no_inline_state_bootstrap()
    check_helper_examples_are_repo_independent()
    check_shared_boundary_reference()
    check_wrapper_skill_thinness()
    check_browser_verify_entry_skill_size()
    check_browser_verify_reference_owners()
    check_command_output_block_shape()
    check_output_contract_helper_sync()
    print("command surface drift ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
