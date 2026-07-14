#!/usr/bin/env python3
"""Validate TigerKit Agent Skills using only the Python standard library."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
KINDS = {"user-invoked", "hybrid"}
INVOCATION_LABELS = {
    "user-invoked": "[user]",
    "hybrid": "[user/auto]",
}
RELATIONSHIPS = {"copied", "adapted", "inspired-by", "forked", "native"}
EXPECTED_SKILLS = {
    "tk-grill-me",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-implement",
    "tk-prototype",
    "tk-reflect",
    "tk-learn",
    "tk-grooming",
    "tk-handoff",
    "tk-browser-verify",
    "tk-diagnosing-bugs",
    "tk-code-review",
    "tk-merge-conflict",
}
USER_INVOKED_SKILLS = {
    "tk-grill-me",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-implement",
    "tk-prototype",
    "tk-reflect",
    "tk-learn",
    "tk-grooming",
    "tk-handoff",
}
HYBRID_SKILLS = EXPECTED_SKILLS - USER_INVOKED_SKILLS
KEBAB = re.compile(r"^tk-[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
REQUIRED_BEHAVIOR_CASES = {
    "implement-proposes-strategy-before-editing",
    "implement-respects-explicit-strategy",
    "implement-non-agent-tools-are-not-delegation",
    "implement-delegation-is-single-level",
    "implement-tdd-follows-user-decision",
    "implement-commits-after-verification",
    "implement-does-not-commit-failing-change",
    "implement-does-not-push",
    "browser-owned-session-cleans-up",
    "browser-attached-session-is-preserved",
    "browser-first-tool-call-owns-lazy-session",
    "browser-refuses-real-payment",
    "grill-me-keeps-one-question-at-a-time",
    "grill-me-researches-facts-before-asking",
    "grill-me-does-not-write-domain-docs",
    "grill-me-does-not-create-adrs",
    "implement-tdd-requires-observed-red",
    "implement-tdd-uses-public-behavior",
    "implement-non-tdd-still-verifies",
    "code-review-pins-fixed-point",
    "code-review-rejects-invalid-ref",
    "code-review-rejects-empty-diff",
    "code-review-separates-standards-and-spec",
    "code-review-does-not-edit",
    "code-review-bounds-reviewers",
    "diagnosing-bugs-requires-red-capable-loop",
    "diagnosing-bugs-does-not-patch-without-reproduction",
    "diagnosing-bugs-reruns-original-reproduction",
    "diagnosing-bugs-cleans-instrumentation",
    "diagnosing-bugs-reports-missing-seam",
    "diagnosing-bugs-standalone-commit-requires-explicit-invocation",
    "diagnosing-bugs-inside-implement-does-not-commit",
    "merge-conflict-requires-active-operation",
    "merge-conflict-finishes-operation",
    "merge-conflict-does-not-abort",
    "merge-conflict-does-not-force-push",
    "reflect-is-report-only",
    "to-spec-does-not-create-tickets",
    "prototype-is-not-production",
    "grooming-defaults-report-only",
    "legacy-global-state-is-not-scanned",
}


def scalar(value: str) -> object:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    return value


def frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML frontmatter; add a leading --- block")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc

    data: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, data)]
    for number, raw in enumerate(lines[1:end], 2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        match = re.match(r"\s*([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if not match:
            raise ValueError(f"line {number}: unsupported frontmatter syntax")
        key, raw_value = match.groups()
        while stack[-1][0] >= indent:
            stack.pop()
        target = stack[-1][1]
        if raw_value in {None, ""}:
            child: dict[str, object] = {}
            target[key] = child
            stack.append((indent, child))
        else:
            target[key] = scalar(raw_value)
    return data, text


def nested(data: dict[str, object], *keys: str) -> object | None:
    value: object = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = path.parent
    label = skill_dir.name
    try:
        data, text = frontmatter(path)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"{label}: {path.relative_to(ROOT)}: {exc}"], []

    name = data.get("name")
    description = data.get("description")
    kind = nested(data, "metadata", "tigerkit", "kind")
    origin = nested(data, "metadata", "tigerkit", "origin")
    relationship = nested(data, "metadata", "tigerkit", "relationship")

    if not isinstance(name, str) or not name:
        errors.append(f"{label}: SKILL.md field name: add a non-empty name")
    elif name != label:
        errors.append(f"{label}: SKILL.md field name: use directory name {label!r}")
    if isinstance(name, str) and (not name.startswith("tk-") or not KEBAB.fullmatch(name)):
        errors.append(f"{label}: SKILL.md field name: use tk- prefixed kebab-case")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: SKILL.md field description: add a non-empty description")
    if not isinstance(kind, str) or kind not in KINDS:
        errors.append(f"{label}: metadata.tigerkit.kind: use one of {sorted(KINDS)}")
    elif isinstance(description, str) and not description.startswith(f"{INVOCATION_LABELS[kind]} "):
        errors.append(
            f"{label}: SKILL.md field description: prefix with {INVOCATION_LABELS[kind]!r}"
        )
    if label in USER_INVOKED_SKILLS and kind != "user-invoked":
        errors.append(f"{label}: metadata.tigerkit.kind: expected user-invoked")
    if label in HYBRID_SKILLS and kind != "hybrid":
        errors.append(f"{label}: metadata.tigerkit.kind: expected hybrid")
    if relationship not in RELATIONSHIPS:
        errors.append(f"{label}: metadata.tigerkit.relationship: use one of {sorted(RELATIONSHIPS)}")
    if origin != "tigerkit" and not nested(data, "metadata", "tigerkit", "upstream-skill"):
        errors.append(f"{label}: metadata.tigerkit.upstream-skill: required for external origins")

    openai = skill_dir / "agents" / "openai.yaml"
    openai_text = openai.read_text(encoding="utf-8") if openai.is_file() else ""
    disabled = data.get("disable-model-invocation") is True
    implicit_blocked = "allow_implicit_invocation: false" in openai_text
    if kind == "user-invoked":
        argument_hint = data.get("argument-hint")
        if not isinstance(argument_hint, str) or not argument_hint.strip():
            errors.append(f"{label}: argument-hint: add the explicit invocation input shape")
        if not disabled:
            errors.append(f"{label}: disable-model-invocation: set true for user-invoked skills")
        if not openai.is_file():
            errors.append(f"{label}: agents/openai.yaml: add Codex interface policy")
        else:
            for needle in (
                "interface:",
                "display_name:",
                "short_description:",
                "policy:",
                "allow_implicit_invocation: false",
            ):
                if needle not in openai_text:
                    errors.append(f"{label}: agents/openai.yaml: add {needle}")
            if 'short_description: "[user] ' not in openai_text:
                errors.append(f"{label}: agents/openai.yaml: prefix short_description with '[user]'")
    elif kind == "hybrid":
        if disabled:
            errors.append(f"{label}: disable-model-invocation: remove implicit-invocation block")
        if implicit_blocked:
            errors.append(f"{label}: agents/openai.yaml: remove allow_implicit_invocation: false")

    forbidden = {
        "commands/": "remove command-runtime references",
        "~/.tigerkit": "use repo-local .tigerkit scratch only",
        "/tk:": "use tk-* Agent Skill invocation names",
        "repo-root/scripts/": "move runtime code into this skill directory",
        "scripts/tigerkit_state.py": "remove legacy state helper dependency",
    }
    for token, fix in forbidden.items():
        if token in text:
            errors.append(f"{label}: SKILL.md: forbidden {token!r}; {fix}")

    for target in LINK.findall(text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target) or target.startswith("#"):
            continue
        resolved = (skill_dir / target).resolve()
        if resolved != skill_dir.resolve() and skill_dir.resolve() not in resolved.parents:
            errors.append(f"{label}: SKILL.md link {target!r}: keep references inside the skill directory")
        elif not resolved.exists():
            errors.append(f"{label}: SKILL.md link {target!r}: create the referenced file or remove the link")

    non_empty = sum(bool(line.strip()) for line in text.splitlines())
    limit = 250 if kind == "hybrid" else 120
    if non_empty > limit:
        warnings.append(
            f"{label}: SKILL.md: {non_empty} non-empty lines; move detail into references/ "
            f"(warning limit {limit})"
        )
    return errors, warnings


def validate_runtime_scratch(root: Path) -> list[str]:
    scratch = root / ".tigerkit"
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "--", ".tigerkit"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        tracked = None

    if tracked is not None and tracked.returncode == 0:
        if tracked.stdout.strip():
            return [".tigerkit: remove tracked TigerKit runtime scratch"]
        return []
    if scratch.exists():
        return [".tigerkit: remove TigerKit runtime scratch from packaged repository"]
    return []


def validate_repository_contract() -> list[str]:
    errors: list[str] = []
    required_files = (
        "README.md",
        "MIGRATION.md",
        "CHANGELOG.md",
        "NOTICE.md",
        "LICENSE",
        ".gitignore",
        ".github/workflows/validate.yml",
        "scripts/validate_skills.py",
        "evals/trigger-cases.yaml",
        "evals/behavior-cases.yaml",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"{relative}: required TigerKit 19 repository file is missing")
    for relative in (".claude-plugin", "commands", "hooks", "docs/tigerkit", "package.json"):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: remove legacy/runtime surface from TigerKit 19")
    errors.extend(validate_runtime_scratch(ROOT))
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    if ".tigerkit/" not in ignored.splitlines():
        errors.append(".gitignore: document TigerKit repo-local scratch with .tigerkit/")
    required_text = {
        "README.md": (
            "TigerKit 19",
            "v19.0.1",
            "13",
            "Claude Code",
            "Codex",
            "Hermes Agent",
            "npx skills add",
            "사용 시나리오",
        ),
        "MIGRATION.md": (
            "TigerKit 19",
            "Removed Skills",
            "model-only",
            "hybrid",
            "CONTEXT.md",
        ),
        "CHANGELOG.md": ("19.0.1", "13", "hybrid", "v18.0.4"),
        "NOTICE.md": (
            "mattpocock/skills",
            "relationship: adapted",
            "Behavior merged from removed adapted skills",
            "MIT License",
        ),
    }
    for relative, needles in required_text.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{relative}: document required release contract {needle!r}")
    for directory in SKILLS.glob("*/**"):
        if directory.is_dir() and directory.name in {"references", "scripts", "agents"} and not any(directory.iterdir()):
            errors.append(f"{directory.relative_to(ROOT)}: remove empty optional directory")
    return errors


def validate_repo_links() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or ".tigerkit" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^(?:[a-z]+:)?//", target) or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken relative link {target!r}")
    for path in ROOT.rglob("*"):
        if ".git" not in path.parts and ".tigerkit" not in path.parts and path.is_symlink() and not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken symlink")
    return errors


def parse_trigger_cases(path: Path) -> tuple[dict[str, dict[str, int]], list[str]]:
    entries: dict[str, dict[str, int]] = {}
    duplicates: list[str] = []
    current: str | None = None
    mode: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- skill: "):
            current = line.removeprefix("- skill: ").strip()
            if current in entries:
                duplicates.append(current)
            entries[current] = {"examples": 0, "nearby": 0, "positive": 0, "negative": 0}
            mode = None
        elif line.strip() in {"examples:", "nearby:", "positive:", "negative:"}:
            mode = line.strip()[:-1]
        elif line.startswith("    - ") and current and mode:
            entries[current][mode] += 1
    return entries, duplicates


def parse_behavior_cases(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    duplicates: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- case: "):
            if current is not None:
                entries.append(current)
            current = {"case": line.removeprefix("- case: ").strip()}
            case = current["case"]
            if case in seen:
                duplicates.append(case)
            seen.add(case)
        elif current is not None and line.startswith("  skill: "):
            current["skill"] = line.removeprefix("  skill: ").strip()
        elif current is not None and line.startswith("  expect: "):
            current["expect"] = line.removeprefix("  expect: ").strip()
    if current is not None:
        entries.append(current)
    return entries, duplicates


def validate_eval_fixtures() -> list[str]:
    errors: list[str] = []
    trigger_path = ROOT / "evals" / "trigger-cases.yaml"
    behavior_path = ROOT / "evals" / "behavior-cases.yaml"
    if not trigger_path.is_file():
        errors.append("evals/trigger-cases.yaml: add trigger fixtures")
    else:
        trigger_text = trigger_path.read_text(encoding="utf-8")
        if "Static contract fixtures." not in trigger_text or "do not execute models" not in trigger_text:
            errors.append("evals/trigger-cases.yaml: describe static non-model fixtures")
        entries, duplicates = parse_trigger_cases(trigger_path)
        if duplicates:
            errors.append(f"evals/trigger-cases.yaml: duplicate skills: {', '.join(sorted(set(duplicates)))}")
        if set(entries) != EXPECTED_SKILLS:
            errors.append("evals/trigger-cases.yaml: cover exactly the 13 canonical skills")
        for skill, values in sorted(entries.items()):
            if skill in USER_INVOKED_SKILLS:
                if values["examples"] < 2:
                    errors.append(f"evals/trigger-cases.yaml: {skill} needs at least 2 examples")
                if values["positive"] or values["negative"]:
                    errors.append(f"evals/trigger-cases.yaml: {skill} user-invoked entry must not use positive/negative")
            elif skill in HYBRID_SKILLS:
                if values["positive"] < 3 or values["negative"] < 3:
                    errors.append(f"evals/trigger-cases.yaml: {skill} needs positive and negative counts of at least 3")
                if values["examples"] or values["nearby"]:
                    errors.append(f"evals/trigger-cases.yaml: {skill} hybrid entry must use positive/negative")
    if not behavior_path.is_file():
        errors.append("evals/behavior-cases.yaml: add behavior-boundary fixtures")
    else:
        behavior_text = behavior_path.read_text(encoding="utf-8")
        if "Static contract fixtures." not in behavior_text or "do not execute models" not in behavior_text:
            errors.append("evals/behavior-cases.yaml: describe static non-model fixtures")
        entries, duplicates = parse_behavior_cases(behavior_path)
        if duplicates:
            errors.append(f"evals/behavior-cases.yaml: duplicate cases: {', '.join(sorted(set(duplicates)))}")
        cases = {entry.get("case", "") for entry in entries}
        missing = sorted(REQUIRED_BEHAVIOR_CASES - cases)
        if missing:
            errors.append(f"evals/behavior-cases.yaml: missing required cases: {', '.join(missing)}")
        for index, entry in enumerate(entries, 1):
            missing_fields = [field for field in ("case", "skill", "expect") if not entry.get(field)]
            if missing_fields:
                errors.append(
                    f"evals/behavior-cases.yaml: entry {index} missing fields: {', '.join(missing_fields)}"
                )
            skill = entry.get("skill")
            if skill and skill not in EXPECTED_SKILLS:
                errors.append(f"evals/behavior-cases.yaml: {entry.get('case', index)} references unknown skill {skill}")
    return errors


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--links-only":
        link_errors = validate_repo_links()
        if link_errors:
            for error in link_errors:
                print(f"ERROR: {error}")
            return 1
        print("Validated Markdown relative links with 0 errors.")
        return 0
    paths = sorted(SKILLS.glob("*/SKILL.md"))
    errors: list[str] = []
    warnings: list[str] = []
    actual_skills = {path.parent.name for path in paths}
    missing = sorted(EXPECTED_SKILLS - actual_skills)
    extra = sorted(actual_skills - EXPECTED_SKILLS)
    if missing:
        errors.append(f"skills: missing canonical skills: {', '.join(missing)}")
    if extra:
        errors.append(f"skills: remove non-canonical skill directories: {', '.join(extra)}")
    if not paths:
        errors.append("skills: no skills/*/SKILL.md files found")
    errors.extend(validate_repository_contract())
    errors.extend(validate_repo_links())
    errors.extend(validate_eval_fixtures())
    for path in paths:
        skill_errors, skill_warnings = validate_skill(path)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(errors)} errors.")
        return 1
    print(f"Validated {len(paths)} skills with 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
