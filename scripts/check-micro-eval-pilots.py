#!/usr/bin/env python3
"""Validate TigerKit MICRO wording pilots and their real-agent results."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
PILOT_PATH = ROOT / "evals" / "micro-pilots" / "initial-command-wording.json"
RESULT_PATH = ROOT / "evals" / "results" / "micro-initial-command-wording.json"
SCHEMA = "tigerkit.micro-wording-pilot/v1"
SURFACES = {"/tk:route", "/tk:reflect", "/tk:learn"}
STATUSES = {"draft", "micro-validated"}
EVIDENCE_TIERS = {"micro-wording", "micro-real-agent"}
REAL_AGENT_TIER = "micro-real-agent"
SKILL_PATHS = {
    "/tk:route": "skills/route/SKILL.md",
    "/tk:reflect": "skills/reflect/SKILL.md",
    "/tk:learn": "skills/learn/SKILL.md",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"micro eval pilot check failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: top-level object required")
    return cast(dict[str, Any], value)


def nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def positive_int(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        fail(f"{field} must be a positive integer")
    return value


def object_list(value: object, field: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value or not all(isinstance(item, dict) for item in value):
        fail(f"{field} must be a non-empty list of objects")
    return cast(list[dict[str, Any]], value)


def string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{field} must be a non-empty list of strings")
    return cast(list[str], value)


def boolean(value: object, field: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{field} must be boolean")
    return value


def repo_file(value: object, field: str) -> Path:
    relative = nonempty(value, field)
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{field} must be a safe path relative to the checkout")
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        fail(f"{field} must remain inside the checkout")
    if not resolved.is_file():
        fail(f"{field} must point to an existing file")
    return resolved


def validate_common(document: dict[str, Any], label: str) -> None:
    if document.get("schemaVersion") != SCHEMA:
        fail(f"{label}.schemaVersion must be {SCHEMA!r}")
    nonempty(document.get("pilot_id"), f"{label}.pilot_id")


def validate_pilot(pilot: dict[str, Any]) -> tuple[dict[tuple[str, str], set[str]], int]:
    label = str(PILOT_PATH.relative_to(ROOT))
    validate_common(pilot, label)
    if pilot.get("kind") != "micro-wording-comparison":
        fail(f"{label}.kind must be 'micro-wording-comparison'")

    policy = pilot.get("sample_policy")
    if not isinstance(policy, dict):
        fail(f"{label}.sample_policy must be an object")
    default_count = positive_int(policy.get("samples_per_variant"), f"{label}.sample_policy.samples_per_variant")
    tie_count = positive_int(policy.get("extra_samples_per_tied_variant"), f"{label}.sample_policy.extra_samples_per_tied_variant")
    maximum = positive_int(policy.get("max_total_samples"), f"{label}.sample_policy.max_total_samples")
    if default_count != 1 or tie_count != 1:
        fail(f"{label}.sample_policy must require one sample per variant and one extra per tied variant")
    if maximum > 12:
        fail(f"{label}.sample_policy.max_total_samples must be bounded at 12 or fewer")

    rubric = object_list(pilot.get("observation_rubric"), f"{label}.observation_rubric")
    rubric_ids: set[str] = set()
    for index, item in enumerate(rubric):
        rubric_id = nonempty(item.get("id"), f"{label}.observation_rubric[{index}].id")
        nonempty(item.get("question"), f"{label}.observation_rubric[{index}].question")
        if rubric_id in rubric_ids:
            fail(f"{label}: duplicate rubric id {rubric_id!r}")
        rubric_ids.add(rubric_id)

    expected: dict[tuple[str, str], set[str]] = {}
    surfaces = object_list(pilot.get("surfaces"), f"{label}.surfaces")
    actual_surfaces = {item.get("surface") for item in surfaces}
    if actual_surfaces != SURFACES or len(surfaces) != len(SURFACES):
        fail(f"{label}: surfaces must be exactly {sorted(SURFACES)!r}")

    for surface_item in surfaces:
        surface = cast(str, surface_item["surface"])
        status = surface_item.get("status")
        if status not in STATUSES:
            fail(f"{label}.{surface}.status must be one of {sorted(STATUSES)!r}")
        if surface_item.get("evidence_tier") not in EVIDENCE_TIERS:
            fail(f"{label}.{surface}.evidence_tier must identify MICRO evidence")
        if status == "micro-validated" and surface_item.get("evidence_tier") != REAL_AGENT_TIER:
            fail(f"{label}.{surface}.micro-validated status requires {REAL_AGENT_TIER!r}")
        decision = surface_item.get("decision")
        if not isinstance(decision, dict):
            fail(f"{label}.{surface}.decision must be an object")
        if decision.get("selected_variant") is not None:
            nonempty(decision.get("selected_variant"), f"{label}.{surface}.decision.selected_variant")
        nonempty(decision.get("rationale"), f"{label}.{surface}.decision.rationale")
        if not isinstance(decision.get("public_wording_change"), bool):
            fail(f"{label}.{surface}.decision.public_wording_change must be boolean")

        questions = object_list(surface_item.get("questions"), f"{label}.{surface}.questions")
        for q_index, question in enumerate(questions):
            question_id = nonempty(question.get("id"), f"{label}.{surface}.questions[{q_index}].id")
            nonempty(question.get("question"), f"{label}.{surface}.{question_id}.question")
            variants = object_list(question.get("variants"), f"{label}.{surface}.{question_id}.variants")
            if len(variants) < 2:
                fail(f"{label}.{surface}.{question_id} must have at least two variants")
            variant_ids: set[str] = set()
            for v_index, variant in enumerate(variants):
                variant_id = nonempty(variant.get("id"), f"{label}.{surface}.{question_id}.variants[{v_index}].id")
                nonempty(variant.get("prompt"), f"{label}.{surface}.{question_id}.{variant_id}.prompt")
                nonempty(variant.get("wording_under_test"), f"{label}.{surface}.{question_id}.{variant_id}.wording_under_test")
                if variant_id in variant_ids:
                    fail(f"{label}.{surface}.{question_id}: duplicate variant id {variant_id!r}")
                variant_ids.add(variant_id)
            key = (surface, question_id)
            if key in expected:
                fail(f"{label}: duplicate question key {key!r}")
            expected[key] = variant_ids

    total_variants = sum(len(variants) for variants in expected.values())
    if total_variants > maximum:
        fail(f"{label}: {total_variants} baseline samples exceed max_total_samples={maximum}")
    return expected, maximum


def validate_results(results: dict[str, Any], pilot: dict[str, Any], expected: dict[tuple[str, str], set[str]], maximum: int) -> None:
    label = str(RESULT_PATH.relative_to(ROOT))
    validate_common(results, label)
    if results.get("kind") != "micro-wording-results":
        fail(f"{label}.kind must be 'micro-wording-results'")
    if results.get("pilot_id") != pilot.get("pilot_id"):
        fail(f"{label}.pilot_id must match pilot")
    if results.get("status") != "micro-validated":
        fail(f"{label}.status must be 'micro-validated' for completed MICRO evidence")
    if results.get("evidence_tier") != REAL_AGENT_TIER:
        fail(f"{label}.evidence_tier must be {REAL_AGENT_TIER!r}")

    runtime = results.get("runtime")
    if not isinstance(runtime, dict):
        fail(f"{label}.runtime must be an object")
    if runtime.get("agent") != "Hermes Agent":
        fail(f"{label}.runtime.agent must identify Hermes Agent")
    nonempty(runtime.get("agent"), f"{label}.runtime.agent")
    nonempty(runtime.get("agent_version"), f"{label}.runtime.agent_version")
    nonempty(runtime.get("model"), f"{label}.runtime.model")
    nonempty(runtime.get("host"), f"{label}.runtime.host")
    nonempty(runtime.get("provider"), f"{label}.runtime.provider")

    invocation = results.get("invocation")
    if not isinstance(invocation, dict):
        fail(f"{label}.invocation must be an object")
    required_invocation = {
        "executable": "hermes",
        "subcommand": "chat",
        "quiet": True,
        "query_mode": "single-query",
        "session_reuse": False,
        "working_directory": str(ROOT),
    }
    for field, required in required_invocation.items():
        if type(invocation.get(field)) is not type(required) or invocation.get(field) != required:
            fail(f"{label}.invocation.{field} must be {required!r}")
    nonempty(invocation.get("command_shape"), f"{label}.invocation.command_shape")
    nonempty(invocation.get("provider"), f"{label}.invocation.provider")
    nonempty(invocation.get("model"), f"{label}.invocation.model")
    nonempty(invocation.get("isolation"), f"{label}.invocation.isolation")
    nonempty(invocation.get("context"), f"{label}.invocation.context")
    if invocation["provider"] != runtime["provider"]:
        fail(f"{label}.invocation.provider must match runtime.provider")
    if invocation["model"] != runtime["model"]:
        fail(f"{label}.invocation.model must match runtime.model")

    checkout = results.get("checkout")
    if not isinstance(checkout, dict):
        fail(f"{label}.checkout must be an object")
    if checkout.get("root") != str(ROOT):
        fail(f"{label}.checkout.root must be the current checkout {str(ROOT)!r}")
    git_commit = nonempty(checkout.get("git_commit"), f"{label}.checkout.git_commit")
    if not GIT_SHA_RE.fullmatch(git_commit):
        fail(f"{label}.checkout.git_commit must be a lowercase 40-character Git SHA")
    canonical_skills = checkout.get("canonical_skills")
    if not isinstance(canonical_skills, dict) or set(canonical_skills) != SURFACES:
        fail(f"{label}.checkout.canonical_skills must cover exactly {sorted(SURFACES)!r}")
    for surface, expected_path in SKILL_PATHS.items():
        skill = canonical_skills.get(surface)
        if not isinstance(skill, dict):
            fail(f"{label}.checkout.canonical_skills.{surface} must be an object")
        if skill.get("path") != expected_path:
            fail(f"{label}.checkout.canonical_skills.{surface}.path must be {expected_path!r}")
        skill_path = repo_file(skill.get("path"), f"{label}.checkout.canonical_skills.{surface}.path")
        skill_sha = nonempty(skill.get("sha256"), f"{label}.checkout.canonical_skills.{surface}.sha256")
        if not SHA256_RE.fullmatch(skill_sha):
            fail(f"{label}.checkout.canonical_skills.{surface}.sha256 must be a lowercase SHA-256")
        actual_skill_sha = hashlib.sha256(skill_path.read_bytes()).hexdigest()
        if skill_sha != actual_skill_sha:
            fail(f"{label}.checkout.canonical_skills.{surface}.sha256 does not match the current checkout file")

    records = object_list(results.get("records"), f"{label}.records")
    if len(records) > maximum:
        fail(f"{label}: result count {len(records)} exceeds max_total_samples={maximum}")
    counts: dict[tuple[str, str, str], int] = {}
    selections: dict[str, set[str]] = {surface: set() for surface in SURFACES}
    for index, record in enumerate(records):
        prefix = f"{label}.records[{index}]"
        surface = nonempty(record.get("surface"), f"{prefix}.surface")
        question_id = nonempty(record.get("question_id"), f"{prefix}.question_id")
        variant_id = nonempty(record.get("variant_id"), f"{prefix}.variant_id")
        if (surface, question_id) not in expected or variant_id not in expected[(surface, question_id)]:
            fail(f"{prefix}: record does not match a declared pilot variant")
        if surface not in SKILL_PATHS or record.get("canonical_skill_path") != SKILL_PATHS[surface]:
            fail(f"{prefix}.canonical_skill_path must identify the current checkout skill for {surface}")
        nonempty(record.get("session_id"), f"{prefix}.session_id")
        nonempty(record.get("declared_prompt"), f"{prefix}.declared_prompt")
        sample_index = positive_int(record.get("sample_index"), f"{prefix}.sample_index")
        key = (surface, question_id, variant_id)
        counts[key] = counts.get(key, 0) + 1
        if sample_index != counts[key]:
            fail(f"{prefix}.sample_index must be contiguous per variant")
        if record.get("succeeded") is not True:
            fail(f"{prefix}.succeeded must be true for recorded evidence")
        if not SHA256_RE.fullmatch(nonempty(record.get("output_sha256"), f"{prefix}.output_sha256")):
            fail(f"{prefix}.output_sha256 must be a lowercase SHA-256")
        excerpt = nonempty(record.get("output_excerpt"), f"{prefix}.output_excerpt")
        if len(excerpt) > 1200:
            fail(f"{prefix}.output_excerpt must stay concise (<=1200 characters)")
        output_byte_length = positive_int(record.get("output_byte_length"), f"{prefix}.output_byte_length")
        if output_byte_length < len(excerpt.encode("utf-8")):
            fail(f"{prefix}.output_byte_length cannot be shorter than output_excerpt bytes")
        observation = record.get("observation")
        if not isinstance(observation, dict):
            fail(f"{prefix}.observation must be an object")
        observed_scores = observation.get("rubric")
        if not isinstance(observed_scores, dict) or set(observed_scores) != {item["id"] for item in pilot["observation_rubric"]}:
            fail(f"{prefix}.observation.rubric must score every declared rubric item")
        if not all(value in {"pass", "partial", "fail"} for value in observed_scores.values()):
            fail(f"{prefix}.observation.rubric values must be pass|partial|fail")
        nonempty(observation.get("notes"), f"{prefix}.observation.notes")
        if sample_index > 1 and observation.get("tied") is not True:
            fail(f"{prefix}: extra samples require an explicit tied observation")
        selected_variant = boolean(record.get("selected_variant"), f"{prefix}.selected_variant")
        nonempty(record.get("selection_rationale"), f"{prefix}.selection_rationale")
        if record.get("status") != "micro-validated":
            fail(f"{prefix}.status must be 'micro-validated'")
        if record.get("evidence_tier") != REAL_AGENT_TIER:
            fail(f"{prefix}.evidence_tier must be {REAL_AGENT_TIER!r}")
        if selected_variant:
            selections[surface].add(variant_id)

    for (surface, question_id), variant_ids in expected.items():
        for variant_id in variant_ids:
            count = counts.get((surface, question_id, variant_id), 0)
            if count not in {1, 2}:
                fail(f"{label}: {surface}/{question_id}/{variant_id} must have one sample, or two only for a tie")

    summaries = object_list(results.get("surface_results"), f"{label}.surface_results")
    if {item.get("surface") for item in summaries} != SURFACES or len(summaries) != len(SURFACES):
        fail(f"{label}.surface_results must cover exactly {sorted(SURFACES)!r}")
    pilot_by_surface = {item["surface"]: item for item in pilot["surfaces"]}
    for summary in summaries:
        surface = cast(str, summary["surface"])
        status = summary.get("status")
        if status not in STATUSES or status != pilot_by_surface[surface]["status"]:
            fail(f"{label}.{surface}.status must be valid and match pilot")
        if summary.get("evidence_tier") not in EVIDENCE_TIERS:
            fail(f"{label}.{surface}.evidence_tier must identify MICRO evidence")
        if summary.get("evidence_tier") != REAL_AGENT_TIER:
            fail(f"{label}.{surface}.evidence_tier must be {REAL_AGENT_TIER!r} for real-agent evidence")
        decision = summary.get("decision")
        if not isinstance(decision, dict):
            fail(f"{label}.{surface}.decision must be an object")
        selected = decision.get("selected_variant")
        if selected is not None:
            selected = nonempty(selected, f"{label}.{surface}.decision.selected_variant")
        nonempty(decision.get("rationale"), f"{label}.{surface}.decision.rationale")
        if decision.get("public_wording_change") is not False:
            fail(f"{label}.{surface}.decision.public_wording_change must remain false for Issue 1")
        declared_variant_ids = {
            variant_id
            for (declared_surface, _question_id), variant_ids in expected.items()
            if declared_surface == surface
            for variant_id in variant_ids
        }
        if status == "micro-validated":
            if selected is None or selected not in declared_variant_ids or selections[surface] != {selected}:
                fail(f"{label}.{surface}: micro-validated requires one consistently selected variant")
        elif selected is not None or selections[surface]:
            fail(f"{label}.{surface}: draft status must not claim a selected winner")


def main() -> int:
    pilot = load_json(PILOT_PATH)
    expected, maximum = validate_pilot(pilot)
    results = load_json(RESULT_PATH)
    validate_results(results, pilot, expected, maximum)
    digest = hashlib.sha256(RESULT_PATH.read_bytes()).hexdigest()
    print(f"micro eval pilots ok: {len(SURFACES)} surfaces; results sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
