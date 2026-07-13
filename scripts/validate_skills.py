#!/usr/bin/env python3
"""Validate TigerKit Agent Skills using only the Python standard library."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
KINDS = {"user-invoked", "model-invoked", "hybrid"}
INVOCATION_LABELS = {
    "user-invoked": "[user]",
    "model-invoked": "[auto]",
    "hybrid": "[user/auto]",
}
RELATIONSHIPS = {"copied", "adapted", "inspired-by", "forked", "native"}
EXPECTED_SKILLS = {
    "tk-grill-me", "tk-grill-with-docs", "tk-grilling", "tk-domain-modeling",
    "tk-to-spec", "tk-to-tickets", "tk-implement", "tk-prototype",
    "tk-reflect", "tk-learn", "tk-grooming", "tk-handoff", "tk-browser-verify",
    "tk-tdd", "tk-diagnosing-bugs", "tk-code-review", "tk-merge-conflict",
    "tk-codebase-design",
}
KEBAB = re.compile(r"^tk-[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
EXPECTED_BEHAVIOR_CASES = {
    "small-implement-stays-direct", "implement-proposes-strategy-before-editing",
    "implement-respects-explicit-strategy", "implement-non-agent-tools-are-not-delegation",
    "implement-delegation-is-single-level", "implement-tdd-follows-user-decision",
    "implement-commits-after-verification", "implement-does-not-commit-failing-change",
    "implement-does-not-push", "implement-does-not-auto-reflect",
    "reflect-is-report-only", "to-spec-does-not-create-tickets",
    "prototype-is-not-production", "browser-refuses-real-payment",
    "browser-owned-session-cleans-up", "browser-attached-session-is-preserved",
    "browser-first-tool-call-owns-lazy-session", "code-review-does-not-edit",
    "grooming-defaults-report-only", "legacy-global-state-is-not-scanned",
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
            for needle in ("interface:", "display_name:", "short_description:", "policy:", "allow_implicit_invocation: false"):
                if needle not in openai_text:
                    errors.append(f"{label}: agents/openai.yaml: add {needle}")
            if 'short_description: "[user] ' not in openai_text:
                errors.append(f"{label}: agents/openai.yaml: prefix short_description with '[user]'")
    elif kind in {"model-invoked", "hybrid"}:
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
        warnings.append(f"{label}: SKILL.md: {non_empty} non-empty lines; move detail into references/ (warning limit {limit})")
    return errors, warnings


def validate_repository_contract() -> list[str]:
    errors: list[str] = []
    required_files = (
        "README.md", "MIGRATION.md", "CHANGELOG.md", "NOTICE.md", "LICENSE",
        ".gitignore", ".github/workflows/validate.yml",
        "scripts/validate_skills.py", "evals/trigger-cases.yaml", "evals/behavior-cases.yaml",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"{relative}: required TigerKit 18 repository file is missing")
    for relative in (".claude-plugin", "commands", "hooks", ".tigerkit", "docs/tigerkit", "package.json"):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: remove legacy/runtime surface from TigerKit 18")
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    if ".tigerkit/" not in ignored.splitlines():
        errors.append(".gitignore: document TigerKit repo-local scratch with .tigerkit/")
    required_text = {
        "README.md": ("Agent Skills", "Claude Code", "Codex", "Hermes Agent", "npx skills add", "18.0.0", "docs/tigerkit"),
        "MIGRATION.md": ("Claude Code plugin", "npx skills add", "not migrated", "credential", "/tk-implement"),
        "CHANGELOG.md": ("18.0.0", "Agent Skills", "Claude Code", "Codex", "Hermes Agent", "v18.0.0"),
        "NOTICE.md": ("mattpocock/skills", "relationship: adapted", "MIT License"),
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
        if ".git" in path.parts:
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
        if ".git" not in path.parts and path.is_symlink() and not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken symlink")
    return errors


def validate_eval_fixtures() -> list[str]:
    errors: list[str] = []
    trigger_path = ROOT / "evals" / "trigger-cases.yaml"
    behavior_path = ROOT / "evals" / "behavior-cases.yaml"
    if not trigger_path.is_file():
        errors.append("evals/trigger-cases.yaml: add trigger fixtures")
    else:
        counts: dict[str, dict[str, int]] = {}
        current: str | None = None
        mode: str | None = None
        for line in trigger_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("- skill: "):
                current = line.removeprefix("- skill: ").strip()
                counts[current] = {"positive": 0, "negative": 0}
                mode = None
            elif line.strip() in {"positive:", "negative:"}:
                mode = line.strip()[:-1]
            elif line.startswith("    - ") and current and mode:
                counts[current][mode] += 1
        if set(counts) != EXPECTED_SKILLS:
            errors.append("evals/trigger-cases.yaml: cover exactly the 18 canonical skills")
        for skill, values in sorted(counts.items()):
            if values != {"positive": 3, "negative": 2}:
                errors.append(f"evals/trigger-cases.yaml: {skill} needs positive 3 and negative 2")
    if not behavior_path.is_file():
        errors.append("evals/behavior-cases.yaml: add behavior-boundary fixtures")
    else:
        cases = {
            line.removeprefix("- case: ").strip()
            for line in behavior_path.read_text(encoding="utf-8").splitlines()
            if line.startswith("- case: ")
        }
        if cases != EXPECTED_BEHAVIOR_CASES:
            errors.append("evals/behavior-cases.yaml: cover the required boundary cases exactly")
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
