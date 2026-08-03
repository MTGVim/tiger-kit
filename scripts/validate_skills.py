#!/usr/bin/env python3
"""Validate TigerKit Agent Skills from skill-local canonical contracts."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)
SKILLS = ROOT / "skills"
KINDS = {"user-invoked", "hybrid"}
INVOCATION_LABELS = {"user-invoked": "[user]", "hybrid": "[user/auto]"}
RELATIONSHIPS = {"copied", "adapted", "inspired-by", "forked", "native"}
SUPPORTED_EVAL_HOSTS = {"claude-code", "codex", "hermes-agent"}
HOST_ORDER = ("codex", "claude-code", "hermes-agent")
HYBRID_TRIGGER_FACETS = {"formal", "casual", "typo", "ko-en", "short", "compound"}
TERMINAL_STATUSES = {
    "Pass",
    "Fail",
    "Blocked",
    "Unverifiable",
    "Pending",
    "NotApplicable",
}
MECHANICAL_ASSERTION_TYPES = {
    "event_absent",
    "event_count",
    "event_order",
    "terminal_status",
    "path_exists",
    "path_absent",
    "git_head_changed",
    "git_head_unchanged",
    "output_contains",
    "output_absent",
    "path_text_contains",
    "path_text_absent",
    "path_text_equals",
    "git_commit_count_delta",
    "changed_paths_equal",
    "git_diff_contains",
    "git_diff_absent",
}
EVENT_TYPES = {"phase_invocation", "final_output"}
CORE_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
HOST_EXTENSION_FIELDS = {"argument-hint", "disable-model-invocation"}
KEBAB = re.compile(r"^tk-[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
HANGUL_SYLLABLE = re.compile(r"[가-힣]")
QUESTION_TOOL_TOKENS = (
    "AskUserQuestion",
    "request_user_input",
    "Hermes Agent `clarify`",
    "native structured input",
    "native structured question",
    "native structured-question",
    "structured-input call",
)


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
        raise ValueError("missing YAML frontmatter")
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


def nested(data: Mapping[str, object], *keys: str) -> object | None:
    value: object = data
    for key in keys:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def load_json_object(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{_display_path(path)}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{_display_path(path)}: top-level value must be an object")
        return None
    return value


def discover_skills() -> dict[str, tuple[Path, dict[str, object], str]]:
    result: dict[str, tuple[Path, dict[str, object], str]] = {}
    for path in sorted(SKILLS.glob("tk-*/SKILL.md")):
        data, text = frontmatter(path)
        result[path.parent.name] = (path.parent, data, text)
    return result


def _safe_relative(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and not Path(value).is_absolute()
        and ".." not in Path(value).parts
    )


def validate_frontmatter_and_body(
    name: str, skill_dir: Path, data: dict[str, object], text: str
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    label = str(skill_dir.relative_to(ROOT))
    declared_name = data.get("name")
    description = data.get("description")
    kind = nested(data, "metadata", "tigerkit", "kind")
    origin = nested(data, "metadata", "tigerkit", "origin")
    relationship = nested(data, "metadata", "tigerkit", "relationship")

    unknown = sorted(set(data) - CORE_FRONTMATTER_FIELDS - HOST_EXTENSION_FIELDS)
    if unknown:
        errors.append(f"{label}: unknown frontmatter fields: {', '.join(unknown)}")
    if declared_name != name or not KEBAB.fullmatch(name) or len(name) > 64:
        errors.append(f"{label}: name must equal the tk-* directory name")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{label}: description must be non-empty and at most 1024 characters")
    if kind not in KINDS:
        errors.append(f"{label}: metadata.tigerkit.kind must be one of {sorted(KINDS)}")
    elif isinstance(description, str) and not description.startswith(f"{INVOCATION_LABELS[str(kind)]} "):
        errors.append(f"{label}: description must begin with {INVOCATION_LABELS[str(kind)]}")
    if relationship not in RELATIONSHIPS:
        errors.append(f"{label}: metadata.tigerkit.relationship is invalid")
    if origin != "tigerkit" and not nested(data, "metadata", "tigerkit", "upstream-skill"):
        errors.append(f"{label}: external origin requires metadata.tigerkit.upstream-skill")

    openai_path = skill_dir / "agents/openai.yaml"
    openai_text = openai_path.read_text(encoding="utf-8") if openai_path.is_file() else ""
    if "display_name:" in openai_text:
        errors.append(f"{label}: agents/openai.yaml must use the canonical skill name")
    disabled = data.get("disable-model-invocation") is True
    implicit_blocked = "allow_implicit_invocation: false" in openai_text
    if kind == "user-invoked":
        if not isinstance(data.get("argument-hint"), str) or not str(data.get("argument-hint")).strip():
            errors.append(f"{label}: user-invoked skill requires argument-hint")
        if not disabled:
            errors.append(f"{label}: user-invoked skill requires disable-model-invocation: true")
        for token in ("interface:", "short_description:", "policy:", "allow_implicit_invocation: false"):
            if token not in openai_text:
                errors.append(f"{label}: agents/openai.yaml missing {token}")
        if 'short_description: "[user] ' not in openai_text:
            errors.append(f"{label}: Codex short_description must begin with [user]")
    elif kind == "hybrid":
        if disabled:
            errors.append(f"{label}: hybrid skill must allow implicit invocation")
        if implicit_blocked:
            errors.append(f"{label}: hybrid Codex policy must not block implicit invocation")
        if openai_text and 'short_description: "[user/auto] ' not in openai_text:
            errors.append(f"{label}: Codex short_description must begin with [user/auto]")

    if name != "tk-adhd":
        terminal = "### 🔴 HARD GATE · terminal user summary"
        language = "### 🔴 HARD GATE · response language"
        decision = "## User decision questions"
        for heading in (terminal, language, decision):
            if text.count(heading) != 1:
                errors.append(f"{label}: require exactly one {heading}")
        if terminal in text and language in text and text.index(terminal) > text.index(language):
            errors.append(f"{label}: terminal summary gate must precede response language gate")

    forbidden = {
        "commands/": "legacy command runtime",
        "~/.tigerkit": "global TigerKit state",
        "/tk:": "legacy invocation namespace",
        "scripts/tigerkit_state.py": "legacy state helper",
    }
    for token, reason in forbidden.items():
        if token in text:
            errors.append(f"{label}: remove {reason} reference {token!r}")

    for target in LINK.findall(text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target) or target.startswith("#"):
            continue
        resolved = (skill_dir / target).resolve()
        if resolved != skill_dir.resolve() and skill_dir.resolve() not in resolved.parents:
            errors.append(f"{label}: keep links inside the skill package: {target!r}")
        elif not resolved.exists():
            errors.append(f"{label}: broken skill-local link {target!r}")

    non_empty = sum(bool(line.strip()) for line in text.splitlines())
    limit = 160 if kind == "hybrid" else 120
    if non_empty > limit:
        warnings.append(f"{label}: {non_empty} non-empty SKILL.md lines (warning limit {limit})")
    return errors, warnings


def validate_skill_language(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    paths = [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]
    for path in paths:
        if not path.is_file():
            continue
        in_fence = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            prose = "" if in_fence else re.sub(r"`[^`]*`", "", line)
            if HANGUL_SYLLABLE.search(prose):
                errors.append(
                    f"{_display_path(path)}:{number}: canonical operational prose must be English"
                )
    return errors


def validate_plain_chat_contract(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".yaml", ".yml", ".py", ".mjs"}:
            continue
        text = path.read_text(encoding="utf-8")
        for token in QUESTION_TOOL_TOKENS:
            if token in text:
                errors.append(
                    f"{_display_path(path)}: render questions in plain chat; remove {token!r}"
                )
    return errors


def validate_trigger_contract(
    name: str, kind: str, path: Path
) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    ids: set[str] = set()
    data = load_json_object(path, errors)
    if data is None:
        return errors, ids
    if data.get("skill") != name:
        errors.append(f"{_display_path(path)}: skill must equal {name}")
    if data.get("kind") != kind:
        errors.append(f"{_display_path(path)}: kind must equal {kind}")
    queries = data.get("queries")
    if not isinstance(queries, list) or not queries:
        errors.append(f"{_display_path(path)}: queries must be a non-empty list")
        return errors, ids

    splits: set[str] = set()
    normalized_by_split: dict[str, set[str]] = {"train": set(), "validation": set()}
    positives = 0
    negatives = 0
    validation_positive = 0
    validation_negative = 0
    facets: set[str] = set()
    for index, row in enumerate(queries, 1):
        if not isinstance(row, dict):
            errors.append(f"{_display_path(path)}: query {index} must be an object")
            continue
        query_id = row.get("id")
        split = row.get("split")
        query = row.get("query")
        should_trigger = row.get("should_trigger")
        row_facets = row.get("facets", [])
        if not isinstance(query_id, str) or not query_id:
            errors.append(f"{_display_path(path)}: query {index} needs id")
        elif query_id in ids:
            errors.append(f"{_display_path(path)}: duplicate id {query_id}")
        else:
            ids.add(query_id)
        if split not in {"train", "validation"}:
            errors.append(f"{_display_path(path)}: query {query_id or index} has invalid split")
        else:
            splits.add(str(split))
        if not isinstance(query, str) or not query.strip():
            errors.append(f"{_display_path(path)}: query {query_id or index} needs text")
        elif split in normalized_by_split:
            normalized_by_split[str(split)].add(" ".join(query.casefold().split()))
        if not isinstance(should_trigger, bool):
            errors.append(f"{_display_path(path)}: query {query_id or index} needs boolean should_trigger")
        elif should_trigger:
            positives += 1
            validation_positive += int(split == "validation")
        else:
            negatives += 1
            validation_negative += int(split == "validation")
        if not isinstance(row_facets, list) or not all(
            isinstance(facet, str) and facet in HYBRID_TRIGGER_FACETS for facet in row_facets
        ):
            errors.append(f"{_display_path(path)}: invalid facets on {query_id or index}")
        elif split == "validation":
            facets.update(row_facets)

    if splits != {"train", "validation"}:
        errors.append(f"{_display_path(path)}: include train and validation splits")
    if normalized_by_split["train"] & normalized_by_split["validation"]:
        errors.append(f"{_display_path(path)}: train/validation prompts overlap")
    if not positives or not negatives:
        errors.append(f"{_display_path(path)}: include positive and negative cases")
    if kind == "hybrid":
        if validation_positive < 8 or validation_negative < 8:
            errors.append(f"{_display_path(path)}: hybrid validation needs 8 positive and 8 negative cases")
        if facets != HYBRID_TRIGGER_FACETS:
            errors.append(f"{_display_path(path)}: hybrid validation must cover all facets")
    return errors, ids


def _validate_event_matcher(value: object, *, allow_final: bool) -> bool:
    if not isinstance(value, dict):
        return False
    event_type = value.get("type")
    if event_type == "phase_invocation":
        return isinstance(value.get("phase"), str) and bool(str(value.get("phase")).strip())
    if allow_final and event_type == "final_output":
        status = value.get("terminal_status")
        return status is None or status in TERMINAL_STATUSES
    return False


def validate_behavior_contract(name: str, path: Path) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    ids: set[str] = set()
    data = load_json_object(path, errors)
    if data is None:
        return errors, ids
    if data.get("skill_name") != name:
        errors.append(f"{_display_path(path)}: skill_name must equal {name}")
    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{_display_path(path)}: evals must be a non-empty list")
        return errors, ids

    paths: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"{_display_path(path)}: case {index} must be an object")
            continue
        case_id = case.get("id")
        path_type = case.get("path")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{_display_path(path)}: case {index} needs id")
        elif case_id in ids:
            errors.append(f"{_display_path(path)}: duplicate case id {case_id}")
        else:
            ids.add(case_id)
        if path_type not in {"success", "boundary"}:
            errors.append(f"{_display_path(path)}: case {case_id or index} has invalid path")
        else:
            paths.add(str(path_type))
        for field in ("prompt", "expected_output"):
            if not isinstance(case.get(field), str) or not str(case.get(field)).strip():
                errors.append(f"{_display_path(path)}: case {case_id or index} needs {field}")
        hosts = case.get("hosts")
        if hosts is not None and (
            not isinstance(hosts, list)
            or not hosts
            or len(set(hosts)) != len(hosts)
            or not all(isinstance(host, str) and host in SUPPORTED_EVAL_HOSTS for host in hosts)
        ):
            errors.append(f"{_display_path(path)}: case {case_id or index} has invalid hosts")

        assertions = case.get("assertions")
        mechanical = False
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{_display_path(path)}: case {case_id or index} needs assertions")
            continue
        for assertion_index, assertion in enumerate(assertions, 1):
            if not isinstance(assertion, dict):
                errors.append(f"{_display_path(path)}: assertion {assertion_index} must be an object")
                continue
            assertion_type = assertion.get("type")
            if assertion_type == "judge":
                if not isinstance(assertion.get("criterion"), str) or not str(assertion.get("criterion")).strip():
                    errors.append(f"{_display_path(path)}: judge assertion needs criterion")
                continue
            if assertion_type not in MECHANICAL_ASSERTION_TYPES:
                errors.append(f"{_display_path(path)}: unknown assertion type {assertion_type!r}")
                continue
            mechanical = True
            if assertion_type == "terminal_status":
                expected = assertion.get("expected")
                allowed = assertion.get("allowed")
                if (expected is None) == (allowed is None):
                    errors.append(f"{_display_path(path)}: terminal_status needs expected or allowed")
                values = [expected] if expected is not None else allowed
                if not isinstance(values, list) or not values or not all(value in TERMINAL_STATUSES for value in values):
                    errors.append(f"{_display_path(path)}: invalid terminal status values")
            elif assertion_type == "event_order":
                if not _validate_event_matcher(assertion.get("before"), allow_final=False) or not _validate_event_matcher(assertion.get("after"), allow_final=False):
                    errors.append(f"{_display_path(path)}: event_order needs phase matchers")
                forbidden = assertion.get("forbidden_between", [])
                if not isinstance(forbidden, list) or not forbidden or not all(
                    _validate_event_matcher(value, allow_final=True) for value in forbidden
                ):
                    errors.append(f"{_display_path(path)}: event_order needs forbidden_between matchers")
            elif assertion_type == "event_absent":
                if not _validate_event_matcher(assertion.get("event"), allow_final=True):
                    errors.append(f"{_display_path(path)}: event_absent needs an event matcher")
            elif assertion_type == "event_count":
                if not _validate_event_matcher(assertion.get("event"), allow_final=False):
                    errors.append(f"{_display_path(path)}: event_count needs a phase matcher")
                minimum = assertion.get("min")
                maximum = assertion.get("max")
                if minimum is None and maximum is None:
                    errors.append(f"{_display_path(path)}: event_count needs min or max")
            elif assertion_type in {"path_exists", "path_absent", "path_text_contains", "path_text_absent", "path_text_equals"}:
                if not _safe_relative(assertion.get("path")):
                    errors.append(f"{_display_path(path)}: path assertion needs a safe relative path")
            elif assertion_type == "changed_paths_equal":
                values = assertion.get("paths")
                if not isinstance(values, list) or not all(_safe_relative(value) for value in values):
                    errors.append(f"{_display_path(path)}: changed_paths_equal needs safe paths")
            elif assertion_type in {"output_contains", "output_absent", "git_diff_contains", "git_diff_absent", "path_text_contains", "path_text_absent", "path_text_equals"}:
                if not isinstance(assertion.get("text"), str) or not str(assertion.get("text")).strip():
                    errors.append(f"{_display_path(path)}: {assertion_type} needs text")
        if not mechanical:
            errors.append(f"{_display_path(path)}: case {case_id or index} needs mechanical evidence")
        files = case.get("files", [])
        if not isinstance(files, list) or not all(
            isinstance(relative, str) and (path.parent.parent / relative).is_file() for relative in files
        ):
            errors.append(f"{_display_path(path)}: case {case_id or index} has missing input files")
    if paths != {"success", "boundary"}:
        errors.append(f"{_display_path(path)}: include success and boundary paths")
    return errors, ids


def validate_catalog(
    skill_names: set[str], behavior_ids: Mapping[str, set[str]]
) -> tuple[list[str], set[str]]:
    path = ROOT / "evals/catalog-routing.json"
    errors: list[str] = []
    ids: set[str] = set()
    data = load_json_object(path, errors)
    if data is None:
        return errors, ids
    if data.get("version") != 1:
        errors.append(f"{_display_path(path)}: version must be 1")
    hosts = data.get("critical_hosts")
    if not isinstance(hosts, list) or set(hosts) != SUPPORTED_EVAL_HOSTS:
        errors.append(f"{_display_path(path)}: critical_hosts must cover all supported hosts")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{_display_path(path)}: cases must be a non-empty list")
        return errors, ids
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"{_display_path(path)}: case {index} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{_display_path(path)}: case {index} needs id")
        elif case_id in ids:
            errors.append(f"{_display_path(path)}: duplicate id {case_id}")
        else:
            ids.add(case_id)
        if not isinstance(case.get("boundary"), str) or not str(case.get("boundary")).strip():
            errors.append(f"{_display_path(path)}: case {case_id or index} needs boundary")
        if not isinstance(case.get("prompt"), str) or not str(case.get("prompt")).strip():
            errors.append(f"{_display_path(path)}: case {case_id or index} needs prompt")
        if case.get("focus_skill") not in skill_names:
            errors.append(f"{_display_path(path)}: case {case_id or index} has unknown focus_skill")
        selected = case.get("expected_selected_skill")
        if selected is not None and selected not in skill_names:
            errors.append(f"{_display_path(path)}: case {case_id or index} has unknown selected skill")
        if not isinstance(case.get("critical"), bool):
            errors.append(f"{_display_path(path)}: case {case_id or index} needs critical boolean")
    return errors, ids


def validate_release_critical(
    behavior_ids: Mapping[str, set[str]], catalog_ids: set[str]
) -> list[str]:
    path = ROOT / "evals/release-critical.json"
    errors: list[str] = []
    data = load_json_object(path, errors)
    if data is None:
        return errors
    if data.get("hosts") != list(HOST_ORDER):
        errors.append(f"{_display_path(path)}: hosts must be ordered {', '.join(HOST_ORDER)}")
    runs = data.get("runs")
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 2:
        errors.append(f"{_display_path(path)}: runs must be at least 2")
    known_behavior = {
        f"{skill}:behavior:{case_id}"
        for skill, ids in behavior_ids.items()
        for case_id in ids
    }
    behavior = data.get("behavior_cases")
    routing = data.get("catalog_cases")
    if not isinstance(behavior, list) or not behavior or not all(value in known_behavior for value in behavior):
        errors.append(f"{_display_path(path)}: behavior_cases must reference canonical cases")
    known_catalog = {f"catalog:behavior:{case_id}" for case_id in catalog_ids}
    if not isinstance(routing, list) or not routing or not all(value in known_catalog for value in routing):
        errors.append(f"{_display_path(path)}: catalog_cases must reference canonical cases")
    retired = data.get("retired_skill_contracts", [])
    if not isinstance(retired, list) or not all(isinstance(value, str) and value for value in retired):
        errors.append(f"{_display_path(path)}: retired_skill_contracts must be a string list")
    elif any(value in behavior_ids for value in retired):
        errors.append(f"{_display_path(path)}: retired_skill_contracts contains an active skill")
    return errors


def validate_invocation_graph(
    skills: Mapping[str, tuple[Path, dict[str, object], str]],
) -> list[str]:
    errors: list[str] = []
    kinds = {
        name: nested(data, "metadata", "tigerkit", "kind")
        for name, (_, data, _) in skills.items()
    }

    def phases(value: object) -> list[str]:
        if isinstance(value, Mapping):
            found = []
            if value.get("type") == "phase_invocation" and isinstance(value.get("phase"), str):
                found.append(str(value["phase"]))
            for child in value.values():
                found.extend(phases(child))
            return found
        if isinstance(value, list):
            return [phase for child in value for phase in phases(child)]
        return []

    for owner, (skill_dir, _, _) in skills.items():
        try:
            cases = json.loads((skill_dir / "evals/evals.json").read_text(encoding="utf-8")).get("evals", [])
        except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
            continue
        for case in cases:
            if not isinstance(case, Mapping):
                continue
            for target in phases(case.get("assertions", [])):
                if target != owner and kinds.get(target) == "user-invoked":
                    errors.append(
                        f"{_display_path(skill_dir / 'evals/evals.json')}: case {case.get('id')} "
                        f"cannot invoke user-invoked skill {target}; make the target hybrid or remove the handoff"
                    )
    return errors


def validate_repo_links() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if ".git" in path.parts or ".tigerkit" in path.parts or relative.parts[0] in {".agents", ".codex"}:
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^(?:[a-z]+:)?//", target) or target.startswith("#"):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{relative}: broken relative link {target!r}")
    return errors


def parse_latest_changelog_version(text: str) -> str | None:
    match = re.search(
        r"(?m)^## ((?:\d{4}\.\d{2}\.\d{2}-\d+|\d+\.\d+\.\d+))(?:\s|$)",
        text,
    )
    return match.group(1) if match else None


def validate_repository_contract(skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    required = (
        "README.md",
        "MIGRATION.md",
        "CHANGELOG.md",
        "NOTICE.md",
        "LICENSE",
        ".gitignore",
        "scripts/validate_skills.py",
        "scripts/run_skill_evals.py",
        "scripts/run_release_gate.py",
        "evals/catalog-routing.json",
        "evals/release-critical.json",
    )
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"{relative}: required repository file is missing")

    obsolete = [
        "scripts/sync_eval_compat.py",
        "evals/trigger-cases.yaml",
        "evals/behavior-cases.yaml",
        *[f"skills/{name}/test-prompts.json" for name in sorted(skill_names)],
    ]
    for relative in obsolete:
        if (ROOT / relative).exists():
            errors.append(f"{relative}: remove duplicate eval compatibility surface")

    for relative in (
        ".github/workflows/validate.yml",
        ".github/workflows/skills-canary.yml",
        ".github/workflows/skill-evals.yml",
        ".github/workflows/auto-patch-tag.yml",
    ):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: validation and release remain local-only")
    for relative in (".claude-plugin", "commands", "hooks", "docs/tigerkit", "package.json"):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: remove legacy/runtime surface")
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    if ".tigerkit/" not in ignored.splitlines():
        errors.append(".gitignore: include .tigerkit/")

    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file() and parse_latest_changelog_version(
        changelog.read_text(encoding="utf-8")
    ) is None:
        errors.append("CHANGELOG.md: add a leading semantic release heading")

    for directory in SKILLS.glob("*/**"):
        if directory.is_dir() and directory.name in {"references", "scripts", "agents", "evals"} and not any(directory.iterdir()):
            errors.append(f"{directory.relative_to(ROOT)}: remove empty optional directory")
    return errors


def validate_all() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        skills = discover_skills()
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"skills: cannot discover catalog: {exc}"], []
    if not skills:
        return ["skills: no skills/tk-*/SKILL.md files found"], []

    behavior_ids: dict[str, set[str]] = {}
    for name, (skill_dir, data, text) in skills.items():
        skill_errors, skill_warnings = validate_frontmatter_and_body(name, skill_dir, data, text)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        errors.extend(validate_skill_language(skill_dir))
        errors.extend(validate_plain_chat_contract(skill_dir))
        kind = nested(data, "metadata", "tigerkit", "kind")
        trigger_path = skill_dir / "evals/triggers.json"
        behavior_path = skill_dir / "evals/evals.json"
        if not trigger_path.is_file():
            errors.append(f"{_display_path(trigger_path)}: add canonical trigger contract")
        else:
            trigger_errors, _ = validate_trigger_contract(name, str(kind), trigger_path)
            errors.extend(trigger_errors)
        if not behavior_path.is_file():
            errors.append(f"{_display_path(behavior_path)}: add canonical behavior contract")
            behavior_ids[name] = set()
        else:
            behavior_errors, ids = validate_behavior_contract(name, behavior_path)
            errors.extend(behavior_errors)
            behavior_ids[name] = ids

    catalog_errors, catalog_ids = validate_catalog(set(skills), behavior_ids)
    errors.extend(catalog_errors)
    errors.extend(validate_invocation_graph(skills))
    errors.extend(validate_release_critical(behavior_ids, catalog_ids))
    errors.extend(validate_repository_contract(set(skills)))
    errors.extend(validate_repo_links())
    return errors, warnings


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--links-only":
        errors = validate_repo_links()
        for error in errors:
            print(f"ERROR: {error}")
        if errors:
            return 1
        print("Validated Markdown relative links with 0 errors.")
        return 0

    errors, warnings = validate_all()
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Validation failed with {len(errors)} errors.")
        return 1
    count = len(discover_skills())
    print(f"Validated {count} auto-discovered Agent Skills with 0 errors.")
    print("Validated skill-local trigger/behavior SSOT and catalog routing contracts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
