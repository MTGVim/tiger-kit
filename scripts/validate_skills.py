#!/usr/bin/env python3
"""Validate TigerKit Agent Skills using only the Python standard library."""
from __future__ import annotations

import json
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
CORE_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
HOST_EXTENSION_FIELDS = {"argument-hint", "disable-model-invocation"}
MECHANICAL_ASSERTION_TYPES = {
    "terminal_status",
    "path_exists",
    "path_absent",
    "git_head_changed",
    "git_head_unchanged",
}
HYBRID_TRIGGER_FACETS = {"formal", "casual", "typo", "ko-en", "short", "compound"}
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
    "implement-auto-decides-unspecified-strategy",
    "implement-respects-explicit-strategy",
    "implement-routes-visible-ui-through-browser-verify",
    "implement-browser-tool-requires-browser-verify",
    "implement-runs-design-preflight-before-ui-edit",
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
    "browser-guard-mode-is-lightweight",
    "browser-guard-visual-claim-needs-screenshot",
    "browser-verdict-mode-preserves-contract",
    "browser-explicit-invocation-uses-verdict",
    "browser-auto-open-fallback-closes-owned-tabs",
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
    "code-review-bounds-large-diff-context",
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
    "handoff-resume-no-drift-continues",
    "handoff-resume-material-drift-blocks",
    "traceability-preserves-requirement-ids",
    "code-review-high-risk-is-conditional",
    "browser-accessibility-is-conditional",
    "learn-requires-eval-and-compatibility",
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


def parse_latest_changelog_version(text: str) -> str | None:
    match = re.search(r"(?m)^## (\d+\.\d+\.\d+)(?:\s|$)", text)
    return match.group(1) if match else None


def validate_release_version_contract(root: Path) -> list[str]:
    changelog = root / "CHANGELOG.md"
    readme = root / "README.md"
    if not changelog.is_file() or not readme.is_file():
        return []
    version = parse_latest_changelog_version(changelog.read_text(encoding="utf-8"))
    if version is None:
        return ["CHANGELOG.md: add a leading semantic version release heading"]
    if f"`v{version}`" not in readme.read_text(encoding="utf-8"):
        return [f"README.md: immutable snapshot must reference latest changelog release v{version}"]
    return []


def validate_release_alignment(
    main_sha: str,
    peeled_tag_sha: str,
    release_sha: str,
    ci_sha: str,
) -> list[str]:
    if len({main_sha, peeled_tag_sha, release_sha, ci_sha}) != 1:
        return ["release provenance: origin/main, peeled tag, GitHub Release, and CI SHA must match"]
    return []


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

    unknown_fields = sorted(set(data) - CORE_FRONTMATTER_FIELDS - HOST_EXTENSION_FIELDS)
    if unknown_fields:
        errors.append(f"{label}: SKILL.md frontmatter: unknown top-level fields: {', '.join(unknown_fields)}")

    if not isinstance(name, str) or not name:
        errors.append(f"{label}: SKILL.md field name: add a non-empty name")
    elif name != label:
        errors.append(f"{label}: SKILL.md field name: use directory name {label!r}")
    if isinstance(name, str) and (not name.startswith("tk-") or not KEBAB.fullmatch(name)):
        errors.append(f"{label}: SKILL.md field name: use tk- prefixed kebab-case")
    if isinstance(name, str) and len(name) > 64:
        errors.append(f"{label}: SKILL.md field name: keep within 64 characters")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: SKILL.md field description: add a non-empty description")
    elif len(description) > 1024:
        errors.append(f"{label}: SKILL.md field description: keep within 1024 characters")
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
        ".github/workflows/skills-canary.yml",
        ".github/workflows/skill-evals.yml",
        "scripts/validate_skills.py",
        "scripts/run_skill_evals.py",
        "scripts/sync_eval_compat.py",
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
        "CHANGELOG.md": ("13", "hybrid", "v18.0.4"),
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
    errors.extend(validate_release_version_contract(ROOT))
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


def load_json_object(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be an object")
        return None
    return value


def darwin_test_prompt_projection(behavior_data: dict[str, object]) -> list[dict[str, object]]:
    evals = behavior_data.get("evals", [])
    if not isinstance(evals, list):
        return []
    selected = [case for case in evals if isinstance(case, dict) and case.get("darwin") is True]
    return [
        {
            "id": index,
            "prompt": case.get("prompt"),
            "expected": case.get("expected_output"),
        }
        for index, case in enumerate(selected, 1)
    ]


def validate_skill_eval_files(skill_dir: Path, kind: str) -> list[str]:
    errors: list[str] = []
    label = skill_dir.name
    trigger_path = skill_dir / "evals" / "triggers.json"
    behavior_path = skill_dir / "evals" / "evals.json"
    for path in (trigger_path, behavior_path):
        if not path.is_file():
            errors.append(f"{label}: {path.relative_to(skill_dir)}: add executable eval contract")
    if errors:
        return errors

    trigger_data = load_json_object(trigger_path, errors)
    if trigger_data is not None:
        if trigger_data.get("skill") != label:
            errors.append(f"{label}: evals/triggers.json: skill must match directory name")
        if trigger_data.get("kind") != kind:
            errors.append(f"{label}: evals/triggers.json: kind must be {kind}")
        queries = trigger_data.get("queries")
        if not isinstance(queries, list) or not queries:
            errors.append(f"{label}: evals/triggers.json: queries must be a non-empty list")
        else:
            ids: list[str] = []
            splits: set[str] = set()
            split_queries: dict[str, set[str]] = {"train": set(), "validation": set()}
            validation_positive = 0
            validation_negative = 0
            validation_facets: set[str] = set()
            any_positive = False
            any_negative = False
            for index, query in enumerate(queries, 1):
                if not isinstance(query, dict):
                    errors.append(f"{label}: evals/triggers.json: query {index} must be an object")
                    continue
                query_id = query.get("id")
                split = query.get("split")
                text = query.get("query")
                should_trigger = query.get("should_trigger")
                facets = query.get("facets", [])
                if not isinstance(query_id, str) or not query_id:
                    errors.append(f"{label}: evals/triggers.json: query {index} needs id")
                else:
                    ids.append(query_id)
                if split not in {"train", "validation"}:
                    errors.append(f"{label}: evals/triggers.json: query {index} split must be train or validation")
                else:
                    splits.add(split)
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{label}: evals/triggers.json: query {index} needs query text")
                elif split in split_queries:
                    split_queries[split].add(" ".join(text.casefold().split()))
                if not isinstance(should_trigger, bool):
                    errors.append(f"{label}: evals/triggers.json: query {index} should_trigger must be boolean")
                elif should_trigger:
                    any_positive = True
                    if split == "validation":
                        validation_positive += 1
                else:
                    any_negative = True
                    if split == "validation":
                        validation_negative += 1
                if not isinstance(facets, list) or not all(
                    isinstance(facet, str) and facet in HYBRID_TRIGGER_FACETS for facet in facets
                ):
                    errors.append(
                        f"{label}: evals/triggers.json: query {index} facets must use "
                        f"{sorted(HYBRID_TRIGGER_FACETS)}"
                    )
                elif split == "validation":
                    validation_facets.update(facets)
            duplicates = sorted({value for value in ids if ids.count(value) > 1})
            if duplicates:
                errors.append(f"{label}: evals/triggers.json: duplicate query ids: {', '.join(duplicates)}")
            if splits != {"train", "validation"}:
                errors.append(f"{label}: evals/triggers.json: include both train and validation splits")
            overlap = sorted(split_queries["train"] & split_queries["validation"])
            if overlap:
                errors.append(f"{label}: evals/triggers.json: train/validation query overlap")
            if not any_positive or not any_negative:
                errors.append(f"{label}: evals/triggers.json: include trigger and non-trigger queries")
            if kind == "hybrid" and (validation_positive < 8 or validation_negative < 8):
                errors.append(
                    f"{label}: evals/triggers.json: hybrid validation needs at least 8 positive and 8 negative queries"
                )
            if kind == "hybrid" and validation_facets != HYBRID_TRIGGER_FACETS:
                missing_facets = ", ".join(sorted(HYBRID_TRIGGER_FACETS - validation_facets))
                errors.append(
                    f"{label}: evals/triggers.json: hybrid validation is missing query facets: "
                    f"{missing_facets or 'none'}"
                )

    behavior_data = load_json_object(behavior_path, errors)
    if behavior_data is not None:
        if behavior_data.get("skill_name") != label:
            errors.append(f"{label}: evals/evals.json: skill_name must match directory name")
        evals = behavior_data.get("evals")
        if not isinstance(evals, list) or not evals:
            errors.append(f"{label}: evals/evals.json: evals must be a non-empty list")
        else:
            ids: list[str] = []
            paths: set[str] = set()
            for index, case in enumerate(evals, 1):
                if not isinstance(case, dict):
                    errors.append(f"{label}: evals/evals.json: case {index} must be an object")
                    continue
                case_id = case.get("id")
                path_type = case.get("path")
                if not isinstance(case_id, str) or not case_id:
                    errors.append(f"{label}: evals/evals.json: case {index} needs id")
                else:
                    ids.append(case_id)
                if path_type not in {"success", "boundary"}:
                    errors.append(f"{label}: evals/evals.json: case {index} path must be success or boundary")
                else:
                    paths.add(path_type)
                for field in ("prompt", "expected_output"):
                    if not isinstance(case.get(field), str) or not str(case.get(field)).strip():
                        errors.append(f"{label}: evals/evals.json: case {index} needs {field}")
                assertions = case.get("assertions")
                if not isinstance(assertions, list) or not assertions:
                    errors.append(f"{label}: evals/evals.json: case {index} needs non-empty assertions")
                else:
                    has_mechanical = False
                    for assertion_index, assertion in enumerate(assertions, 1):
                        if not isinstance(assertion, dict):
                            errors.append(
                                f"{label}: evals/evals.json: case {index} assertion "
                                f"{assertion_index} must be an object"
                            )
                            continue
                        assertion_type = assertion.get("type")
                        if assertion_type == "judge":
                            if not isinstance(assertion.get("criterion"), str) or not str(
                                assertion.get("criterion")
                            ).strip():
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} judge assertion "
                                    f"{assertion_index} needs criterion"
                                )
                            continue
                        if assertion_type not in MECHANICAL_ASSERTION_TYPES:
                            errors.append(
                                f"{label}: evals/evals.json: case {index} assertion "
                                f"{assertion_index} has unknown type {assertion_type!r}"
                            )
                            continue
                        has_mechanical = True
                        if assertion_type == "terminal_status":
                            allowed = assertion.get("allowed")
                            if not isinstance(allowed, list) or not allowed or not all(
                                isinstance(value, str) and value.strip() for value in allowed
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} terminal_status "
                                    "assertion needs non-empty allowed values"
                                )
                        elif assertion_type in {"path_exists", "path_absent"}:
                            relative = assertion.get("path")
                            if (
                                not isinstance(relative, str)
                                or not relative
                                or Path(relative).is_absolute()
                                or ".." in Path(relative).parts
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} path assertion "
                                    "needs a safe relative path"
                                )
                    if not has_mechanical:
                        errors.append(
                            f"{label}: evals/evals.json: case {index} needs at least one "
                            "mechanical assertion; judge-only prose is not release evidence"
                        )
                if "safety" in case and not isinstance(case.get("safety"), bool):
                    errors.append(f"{label}: evals/evals.json: case {index} safety must be boolean")
                if "darwin" in case and not isinstance(case.get("darwin"), bool):
                    errors.append(f"{label}: evals/evals.json: case {index} darwin must be boolean")
                files = case.get("files", [])
                if not isinstance(files, list):
                    errors.append(f"{label}: evals/evals.json: case {index} files must be a list")
                else:
                    for relative in files:
                        if not isinstance(relative, str) or not (skill_dir / relative).is_file():
                            errors.append(f"{label}: evals/evals.json: case {index} missing input file {relative!r}")
            duplicates = sorted({value for value in ids if ids.count(value) > 1})
            if duplicates:
                errors.append(f"{label}: evals/evals.json: duplicate case ids: {', '.join(duplicates)}")
            if paths != {"success", "boundary"}:
                errors.append(f"{label}: evals/evals.json: include success and boundary paths")
        projection = darwin_test_prompt_projection(behavior_data)
        compatibility_path = skill_dir / "test-prompts.json"
        if label in EXPECTED_SKILLS and len(projection) != 2:
            errors.append(f"{label}: evals/evals.json: select exactly 2 Darwin compatibility prompts")
        if compatibility_path.is_file():
            try:
                compatibility = json.loads(compatibility_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"{label}: test-prompts.json: invalid JSON: {exc}")
            else:
                if compatibility != projection:
                    errors.append(f"{label}: test-prompts.json: regenerate from evals/evals.json Darwin cases")
        elif label in EXPECTED_SKILLS:
            errors.append(f"{label}: test-prompts.json: add Darwin compatibility projection")
    return errors


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
    for skill in sorted(EXPECTED_SKILLS):
        kind = "user-invoked" if skill in USER_INVOKED_SKILLS else "hybrid"
        errors.extend(validate_skill_eval_files(SKILLS / skill, kind))
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
    print(f"Validated Agent Skills portable core fields for {len(paths)} skills.")
    print(
        f"Validated TigerKit host extension profiles: "
        f"{len(USER_INVOKED_SKILLS)} user-invoked, {len(HYBRID_SKILLS)} hybrid."
    )
    print(f"Validated {len(paths)} skills with 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
