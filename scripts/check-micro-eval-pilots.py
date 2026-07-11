#!/usr/bin/env python3
"""Validate TigerKit MICRO wording pilots and durable real-agent evidence."""
from __future__ import annotations

import hashlib
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = ROOT / "evals" / "micro-pilots"
PILOT_PATH = PILOT_DIR / "initial-command-wording.json"
RESULTS_DIR = ROOT / "evals" / "results"
RESULT_PATH = RESULTS_DIR / "micro-initial-command-wording.json"
FULL_RESULT_PATH = RESULTS_DIR / "full-reflect-repo-local-safety.json"
RAW_DIR = RESULTS_DIR / "raw" / "micro-initial-command-wording"
FULL_RAW_DIR = RESULTS_DIR / "raw" / "full-reflect-repo-local-safety"
SCHEMA = "tigerkit.micro-wording-pilot/v1"
SOURCE_SCHEMA = "tigerkit.micro-session-source/v1"
SURFACES = {"/tk:route", "/tk:reflect", "/tk:learn"}
STATUSES = {"draft", "micro-validated"}
EVIDENCE_TIERS = {"micro-wording", "micro-real-agent"}
REAL_AGENT_TIER = "micro-real-agent"
SKILL_PATHS = {
    "/tk:route": "skills/route/SKILL.md",
    "/tk:reflect": "skills/reflect/SKILL.md",
    "/tk:learn": "skills/learn/SKILL.md",
}
BASELINE_SESSION_IDS = {
    "route-a-minimal": "20260711_142028_734018",
    "route-b-explicit": "20260711_142131_cc6e8d",
    "reflect-a-minimal": "20260711_142157_3cfad4",
    "reflect-b-explicit": "20260711_142248_a60164",
    "learn-a-minimal": "20260711_142325_130eb4",
    "learn-b-explicit": "20260711_142349_6b4ba5",
}
EVAL_COMMIT = "58feb98f97c98b83a0d283a396ba2f58a625f56b"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SESSION_ID_RE = re.compile(r"^[0-9]{8}_[0-9]{6}_[0-9a-f]{6}$")
ALLOWED_EVIDENCE_TOOLS = {"read_file", "skill_view"}
FORBIDDEN_HOST_MARKERS = ("/home/", "/Users/", "/tmp/", "/root/")
WINDOWS_USER_PATH_RE = re.compile(r"(?i)(?:^|[^A-Za-z0-9])[A-Z]:[\\/](?:Users|home|root|tmp)(?:[\\/]|$)")
EXPECTED_SESSION_MODEL = "gpt-5.6-luna"
EVAL_REQUEST_INSTRUCTIONS = {
    "/tk:route": "Answer the route request with a bounded route choice and concrete first step, without inventing missing facts.",
    "/tk:reflect": "Provide a truthful preview-only classification of the learning, showing the likely durable target, evidence, and next action without claiming any file was changed.",
    "/tk:learn": "Provide a bounded skill-only preview with honest pending verification; do not claim a skill or file was written.",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"micro eval pilot check failed: {message}")


def canonical_eval_request(surface: str, canonical_skill_path: str, declared_prompt: str) -> str:
    instruction = EVAL_REQUEST_INSTRUCTIONS.get(surface)
    if instruction is None:
        fail(f"canonical eval request has an unsupported surface: {surface!r}")
    expected_path = SKILL_PATHS.get(surface)
    if canonical_skill_path != expected_path:
        fail(f"canonical eval request path must be {expected_path!r} for {surface}")
    prompt_terminator = "" if declared_prompt.endswith(".") else "."
    return (
        "This is one isolated, no-write, preview-only TigerKit MICRO evaluation. "
        "Work from the current checkout root repo-root. "
        f"Before answering, use the file-reading tool to read and follow the exact canonical skill file at {canonical_skill_path} from this checkout; "
        "do not use any globally installed or stale copy. "
        "Do not write, modify, or create files. "
        f"Treat this declared variant prompt as the user request: {declared_prompt}{prompt_terminator} "
        f"{instruction} "
        "Return only the concise user-facing answer."
    )


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
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


def boolean(value: object, field: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{field} must be boolean")
    return value


def safe_relative(value: object, field: str) -> str:
    relative = nonempty(value, field)
    if "\x00" in relative or "\\" in relative:
        fail(f"{field} must be a normalized POSIX path relative to the checkout")
    candidate = PurePosixPath(relative)
    if (
        candidate.is_absolute()
        or not candidate.parts
        or any(part in {"", ".", ".."} for part in candidate.parts)
        or candidate.as_posix() != relative
    ):
        fail(f"{field} must be a normalized POSIX path relative to the checkout")
    return relative


def repo_file(value: object, field: str) -> tuple[str, Path]:
    relative = safe_relative(value, field)
    candidate = ROOT.joinpath(*PurePosixPath(relative).parts)
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        fail(f"{field} must remain inside the checkout")

    current = ROOT
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            fail(f"{field} must not traverse a symlink")
    if not candidate.is_file():
        fail(f"{field} must point to an existing regular file")
    return relative, candidate


def reject_host_paths(value: object, label: str) -> None:
    if isinstance(value, str):
        if any(marker in value for marker in FORBIDDEN_HOST_MARKERS) or WINDOWS_USER_PATH_RE.search(value):
            fail(f"{label} must not disclose host-specific absolute paths")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_host_paths(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_host_paths(item, f"{label}[{index}]")


def require_real_directory(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        fail(f"{label} must be an existing real directory: {exc}")
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(f"{label} must be a real directory, not a symlink or special entry")


def inventory_entries(path: Path, label: str) -> list[Path]:
    try:
        entries = list(path.iterdir())
    except OSError as exc:
        fail(f"cannot inspect {label}: {exc}")
    for entry in entries:
        try:
            mode = entry.lstat().st_mode
        except OSError as exc:
            fail(f"cannot inspect {label} entry {entry.name!r}: {exc}")
        if stat.S_ISLNK(mode):
            fail(f"{label} must not contain symlinks: {entry.name!r}")
        if not stat.S_ISREG(mode) and not stat.S_ISDIR(mode):
            fail(f"{label} contains an unsupported special entry: {entry.name!r}")
    return entries


def validate_inventory() -> None:
    fixed_directories = (
        (PILOT_DIR, str(PILOT_DIR.relative_to(ROOT))),
        (RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT))),
        (RESULTS_DIR / "raw", f"{RESULTS_DIR.relative_to(ROOT)}/raw"),
        (RAW_DIR, str(RAW_DIR.relative_to(ROOT))),
        (FULL_RAW_DIR, str(FULL_RAW_DIR.relative_to(ROOT))),
    )
    for path, label in fixed_directories:
        require_real_directory(path, label)

    pilot_entries = inventory_entries(PILOT_DIR, str(PILOT_DIR.relative_to(ROOT)))
    result_entries = inventory_entries(RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT)))

    pilot_files = {entry.name for entry in pilot_entries if entry.is_file()}
    if pilot_files != {PILOT_PATH.name}:
        fail(f"{PILOT_DIR.relative_to(ROOT)} contains unexpected pilot files: {sorted(pilot_files)!r}")
    pilot_dirs = {entry.name for entry in pilot_entries if entry.is_dir()}
    if pilot_dirs:
        fail(f"{PILOT_DIR.relative_to(ROOT)} contains unexpected directories: {sorted(pilot_dirs)!r}")

    result_files = {entry.name for entry in result_entries if entry.is_file()}
    if result_files != {
        RESULT_PATH.name,
        FULL_RESULT_PATH.name,
        "full-gap-stale-sot-precedence.json",
    }:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected result files: {sorted(result_files)!r}")
    result_dirs = {entry.name for entry in result_entries if entry.is_dir()}
    if result_dirs != {"raw"}:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected directories: {sorted(result_dirs)!r}")

    raw_parent = RESULTS_DIR / "raw"
    raw_entries = inventory_entries(raw_parent, str(raw_parent.relative_to(ROOT)))
    raw_files = {entry.name for entry in raw_entries if entry.is_file()}
    if raw_files:
        fail(f"{raw_parent.relative_to(ROOT)} contains unexpected files: {sorted(raw_files)!r}")
    raw_dirs = {entry.name for entry in raw_entries if entry.is_dir()}
    if raw_dirs != {
        RAW_DIR.name,
        FULL_RAW_DIR.name,
        "full-gap-stale-sot-precedence",
    }:
        fail(f"{raw_parent.relative_to(ROOT)} contains unexpected directories: {sorted(raw_dirs)!r}")


def validate_common(document: dict[str, Any], label: str) -> None:
    if document.get("schemaVersion") != SCHEMA:
        fail(f"{label}.schemaVersion must be {SCHEMA!r}")
    nonempty(document.get("pilot_id"), f"{label}.pilot_id")
    reject_host_paths(document, label)


def parse_tie_sets(
    policy: dict[str, Any],
    expected: dict[tuple[str, str], set[str]],
    label: str,
) -> dict[tuple[str, str], set[str]]:
    raw_tie_sets = policy.get("tie_sets")
    if not isinstance(raw_tie_sets, list):
        fail(f"{label}.sample_policy.tie_sets must be a list")
    tie_sets: dict[tuple[str, str], set[str]] = {}
    for index, item in enumerate(raw_tie_sets):
        prefix = f"{label}.sample_policy.tie_sets[{index}]"
        if not isinstance(item, dict):
            fail(f"{prefix} must be an object")
        surface = nonempty(item.get("surface"), f"{prefix}.surface")
        question_id = nonempty(item.get("question_id"), f"{prefix}.question_id")
        key = (surface, question_id)
        if key not in expected:
            fail(f"{prefix} must identify a declared question")
        variants = item.get("variant_ids")
        if (
            not isinstance(variants, list)
            or len(variants) < 2
            or not all(isinstance(variant, str) and variant.strip() for variant in variants)
        ):
            fail(f"{prefix}.variant_ids must contain at least two non-empty strings")
        variant_ids = set(cast(list[str], variants))
        if len(variant_ids) != len(variants):
            fail(f"{prefix}.variant_ids must not contain duplicates")
        if not variant_ids.issubset(expected[key]):
            fail(f"{prefix}.variant_ids must identify declared variants only")
        if key in tie_sets:
            fail(f"{label}: duplicate tie set for {key!r}")
        tie_sets[key] = variant_ids
    return tie_sets


def validate_pilot(
    pilot: dict[str, Any],
) -> tuple[dict[tuple[str, str], set[str]], dict[tuple[str, str], set[str]], int, dict[str, dict[str, Any]]]:
    label = str(PILOT_PATH.relative_to(ROOT))
    validate_common(pilot, label)
    if pilot.get("kind") != "micro-wording-comparison":
        fail(f"{label}.kind must be 'micro-wording-comparison'")

    policy = pilot.get("sample_policy")
    if not isinstance(policy, dict):
        fail(f"{label}.sample_policy must be an object")
    default_count = positive_int(policy.get("samples_per_variant"), f"{label}.sample_policy.samples_per_variant")
    tie_count = positive_int(
        policy.get("extra_samples_per_tied_variant"),
        f"{label}.sample_policy.extra_samples_per_tied_variant",
    )
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
    pilot_by_surface: dict[str, dict[str, Any]] = {}
    surfaces = object_list(pilot.get("surfaces"), f"{label}.surfaces")
    surface_values = [
        nonempty(item.get("surface"), f"{label}.surfaces[{index}].surface")
        for index, item in enumerate(surfaces)
    ]
    actual_surfaces = set(surface_values)
    if actual_surfaces != SURFACES or len(surfaces) != len(SURFACES):
        fail(f"{label}: surfaces must be exactly {sorted(SURFACES)!r}")

    for surface_item in surfaces:
        surface = nonempty(surface_item.get("surface"), f"{label}.surface")
        pilot_by_surface[surface] = surface_item
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
        selected = decision.get("selected_variant")
        if selected is not None:
            nonempty(selected, f"{label}.{surface}.decision.selected_variant")
        nonempty(decision.get("rationale"), f"{label}.{surface}.decision.rationale")
        if decision.get("public_wording_change") is not False:
            fail(f"{label}.{surface}.decision.public_wording_change must be false for Issue 1")

        questions = object_list(surface_item.get("questions"), f"{label}.{surface}.questions")
        for q_index, question in enumerate(questions):
            question_id = nonempty(question.get("id"), f"{label}.{surface}.questions[{q_index}].id")
            nonempty(question.get("question"), f"{label}.{surface}.{question_id}.question")
            variants = object_list(question.get("variants"), f"{label}.{surface}.{question_id}.variants")
            if len(variants) < 2:
                fail(f"{label}.{surface}.{question_id} must have at least two variants")
            variant_ids: set[str] = set()
            for v_index, variant in enumerate(variants):
                variant_id = nonempty(
                    variant.get("id"),
                    f"{label}.{surface}.{question_id}.variants[{v_index}].id",
                )
                nonempty(variant.get("prompt"), f"{label}.{surface}.{question_id}.{variant_id}.prompt")
                nonempty(
                    variant.get("wording_under_test"),
                    f"{label}.{surface}.{question_id}.{variant_id}.wording_under_test",
                )
                if variant_id in variant_ids:
                    fail(f"{label}.{surface}.{question_id}: duplicate variant id {variant_id!r}")
                variant_ids.add(variant_id)
            key = (surface, question_id)
            if key in expected:
                fail(f"{label}: duplicate question key {key!r}")
            expected[key] = variant_ids

    tie_sets = parse_tie_sets(policy, expected, label)
    baseline_samples = sum(len(variants) * default_count for variants in expected.values())
    required_extra_samples = sum(len(variants) * tie_count for variants in tie_sets.values())
    if baseline_samples + required_extra_samples > maximum:
        fail(f"{label}: required samples exceed max_total_samples={maximum}")

    for surface, surface_item in pilot_by_surface.items():
        decision = cast(dict[str, Any], surface_item["decision"])
        declared_variant_ids = {
            variant_id
            for (declared_surface, _question_id), variant_ids in expected.items()
            if declared_surface == surface
            for variant_id in variant_ids
        }
        selected = decision.get("selected_variant")
        if selected is not None and selected not in declared_variant_ids:
            fail(f"{label}.{surface}.decision.selected_variant must identify a declared variant")
        if surface_item["status"] == "micro-validated" and selected is None:
            fail(f"{label}.{surface}: micro-validated requires a selected variant")
        if surface_item["status"] == "draft" and selected is not None:
            fail(f"{label}.{surface}: draft status must not claim a selected winner")

    return expected, tie_sets, maximum, pilot_by_surface


def git_commit_bytes(commit: str, relative: str, field: str) -> bytes:
    safe_relative(relative, field)
    try:
        tree = subprocess.run(
            ["git", "ls-tree", "-z", commit, "--", relative],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"{field}: cannot inspect Git tree for {commit}: {exc}")
    entries = [entry for entry in tree.split(b"\0") if entry]
    matching = []
    for entry in entries:
        try:
            metadata, path_bytes = entry.split(b"\t", 1)
            mode, object_type, _object_id = metadata.split()
            path = path_bytes.decode("utf-8")
        except (UnicodeError, ValueError) as exc:
            fail(f"{field}: malformed Git tree entry: {exc}")
        if path == relative:
            matching.append((mode.decode("ascii"), object_type.decode("ascii")))
    if len(matching) != 1:
        fail(f"{field}: {relative!r} must resolve to exactly one Git tree entry")
    mode, object_type = matching[0]
    if object_type != "blob" or mode == "120000":
        fail(f"{field}: {relative!r} must be a non-symlink Git blob")
    try:
        return subprocess.run(
            ["git", "show", f"{commit}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"{field}: cannot read immutable Git blob: {exc}")


def validate_checkout(results: dict[str, Any], label: str) -> dict[str, str]:
    checkout = results.get("checkout")
    if not isinstance(checkout, dict):
        fail(f"{label}.checkout must be an object")
    if checkout.get("repo_id") != "tiger-kit":
        fail(f"{label}.checkout.repo_id must be 'tiger-kit'")
    git_commit = nonempty(checkout.get("git_commit"), f"{label}.checkout.git_commit")
    if not GIT_SHA_RE.fullmatch(git_commit):
        fail(f"{label}.checkout.git_commit must be a lowercase 40-character Git SHA")
    if git_commit != EVAL_COMMIT:
        fail(f"{label}.checkout.git_commit must identify the pre-implementation eval commit {EVAL_COMMIT}")
    try:
        verified_commit = subprocess.run(
            ["git", "rev-parse", "--verify", f"{git_commit}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"{label}.checkout.git_commit does not exist in this repository: {exc}")
    if verified_commit != git_commit:
        fail(f"{label}.checkout.git_commit did not resolve to the recorded commit")

    canonical_skills = checkout.get("canonical_skills")
    if not isinstance(canonical_skills, dict) or set(canonical_skills) != SURFACES:
        fail(f"{label}.checkout.canonical_skills must cover exactly {sorted(SURFACES)!r}")
    skill_hashes: dict[str, str] = {}
    for surface, expected_path in SKILL_PATHS.items():
        skill = canonical_skills.get(surface)
        if not isinstance(skill, dict):
            fail(f"{label}.checkout.canonical_skills.{surface} must be an object")
        if skill.get("path") != expected_path:
            fail(f"{label}.checkout.canonical_skills.{surface}.path must be {expected_path!r}")
        skill_sha = nonempty(skill.get("sha256"), f"{label}.checkout.canonical_skills.{surface}.sha256")
        if not SHA256_RE.fullmatch(skill_sha):
            fail(f"{label}.checkout.canonical_skills.{surface}.sha256 must be a lowercase SHA-256")
        _, live_skill_path = repo_file(expected_path, f"{label}.checkout.canonical_skills.{surface}.worktree_path")
        try:
            live_skill_sha = hashlib.sha256(live_skill_path.read_bytes()).hexdigest()
        except OSError as exc:
            fail(f"{label}.checkout.canonical_skills.{surface}: cannot read live skill file: {exc}")
        if live_skill_sha != skill_sha:
            fail(f"{label}.checkout.canonical_skills.{surface}.sha256 does not match the live skill file")
        blob = git_commit_bytes(git_commit, expected_path, f"{label}.checkout.canonical_skills.{surface}.path")
        immutable_skill_sha = hashlib.sha256(blob).hexdigest()
        if skill_sha != immutable_skill_sha:
            fail(f"{label}.checkout.canonical_skills.{surface}.sha256 does not match the immutable Git blob")
        if live_skill_sha != immutable_skill_sha:
            fail(f"{label}.checkout.canonical_skills.{surface}: live skill file differs from the immutable Git blob")
        skill_hashes[surface] = skill_sha
    return skill_hashes


def validate_tool_evidence(
    source: dict[str, Any],
    label: str,
    skill_path: str,
    skill_sha: str,
) -> str:
    session = source.get("session")
    if not isinstance(session, dict):
        fail(f"{label}.session must be an object")
    if session.get("source") != "tui":
        fail(f"{label}.session.source must be 'tui'")
    session_model = nonempty(session.get("model"), f"{label}.session.model")
    if session_model != EXPECTED_SESSION_MODEL:
        fail(f"{label}.session.model must be {EXPECTED_SESSION_MODEL!r}")
    if session.get("fresh") is not True or session.get("isolated") is not True:
        fail(f"{label}.session must record fresh=true and isolated=true")
    if session.get("write_free") is not True:
        fail(f"{label}.session.write_free must be true")

    evidence = source.get("tool_evidence")
    if not isinstance(evidence, dict):
        fail(f"{label}.tool_evidence must be an object")
    read = evidence.get("canonical_skill_read")
    if not isinstance(read, dict):
        fail(f"{label}.tool_evidence.canonical_skill_read must be an object")
    if read.get("tool") != "read_file" or read.get("path") != skill_path:
        fail(f"{label}.tool_evidence.canonical_skill_read must identify the canonical read_file path")
    if read.get("sha256") != skill_sha:
        fail(f"{label}.tool_evidence.canonical_skill_read.sha256 must match the immutable skill blob")
    observed_tools = evidence.get("observed_tools")
    if (
        not isinstance(observed_tools, list)
        or not observed_tools
        or not all(isinstance(tool, str) and tool in ALLOWED_EVIDENCE_TOOLS for tool in observed_tools)
    ):
        fail(f"{label}.tool_evidence.observed_tools contains an unapproved or missing tool")
    if read["tool"] not in observed_tools:
        fail(f"{label}.tool_evidence.observed_tools must include the canonical skill read tool")
    write_tools = evidence.get("write_tools")
    if write_tools != []:
        fail(f"{label}.tool_evidence.write_tools must be empty")
    return session_model


def validate_source(
    path: Path,
    record: dict[str, Any],
    expected_prompt: str,
    skill_sha: str,
) -> tuple[str, str, int]:
    label = str(path.relative_to(ROOT))
    source = load_json(path)
    if source.get("schemaVersion") != SOURCE_SCHEMA:
        fail(f"{label}.schemaVersion must be {SOURCE_SCHEMA!r}")
    reject_host_paths(source, label)
    for field in (
        "session_id",
        "surface",
        "question_id",
        "variant_id",
        "eval_user_request",
        "eval_user_request_sha256",
        "declared_prompt",
        "canonical_skill_path",
    ):
        nonempty(source.get(field), f"{label}.{field}")
    if source.get("session_id") != record.get("session_id"):
        fail(f"{label}.session_id must match the result record")
    for field in ("surface", "question_id", "variant_id", "canonical_skill_path"):
        if source.get(field) != record.get(field):
            fail(f"{label}.{field} must match the result record")
    eval_user_request = cast(str, source["eval_user_request"])
    canonical_request = canonical_eval_request(
        cast(str, record["surface"]),
        cast(str, record["canonical_skill_path"]),
        expected_prompt,
    )
    if eval_user_request != canonical_request:
        fail(f"{label}.eval_user_request must exactly match the canonical normalized evaluation request")
    eval_request_sha = nonempty(source.get("eval_user_request_sha256"), f"{label}.eval_user_request_sha256")
    if not SHA256_RE.fullmatch(eval_request_sha):
        fail(f"{label}.eval_user_request_sha256 must be a lowercase SHA-256")
    if eval_request_sha != hashlib.sha256(canonical_request.encode("utf-8")).hexdigest():
        fail(f"{label}.eval_user_request_sha256 does not match the canonical normalized evaluation request")
    if record.get("eval_user_request_sha256") != eval_request_sha:
        fail(f"{label}.eval_user_request_sha256 must match the result record")
    if (
        source.get("declared_prompt") != expected_prompt
        or source.get("declared_prompt") != record.get("declared_prompt")
    ):
        fail(f"{label}.declared_prompt must exactly match the declared pilot prompt")

    source_skill_sha = nonempty(source.get("canonical_skill_sha256"), f"{label}.canonical_skill_sha256")
    if not SHA256_RE.fullmatch(source_skill_sha):
        fail(f"{label}.canonical_skill_sha256 must be a lowercase SHA-256")
    if source_skill_sha != skill_sha:
        fail(f"{label}.canonical_skill_sha256 must match the immutable skill blob")

    request_sha = nonempty(source.get("request_sha256"), f"{label}.request_sha256")
    if not SHA256_RE.fullmatch(request_sha):
        fail(f"{label}.request_sha256 must be a lowercase SHA-256")
    actual_request_sha = hashlib.sha256(expected_prompt.encode("utf-8")).hexdigest()
    if request_sha != actual_request_sha:
        fail(f"{label}.request_sha256 does not match the exact declared prompt")
    if record.get("request_sha256") != request_sha:
        fail(f"{label}.request_sha256 must match the result record")

    response = nonempty(source.get("assistant_response"), f"{label}.assistant_response")
    if not response.endswith("\n") or response.endswith("\n\n"):
        fail(f"{label}.assistant_response must use exactly one terminal LF as its canonical byte surface")
    response_bytes = response.encode("utf-8")
    response_sha = nonempty(source.get("response_sha256"), f"{label}.response_sha256")
    if not SHA256_RE.fullmatch(response_sha):
        fail(f"{label}.response_sha256 must be a lowercase SHA-256")
    if response_sha != hashlib.sha256(response_bytes).hexdigest():
        fail(f"{label}.response_sha256 does not match the durable assistant response bytes")
    response_length = positive_int(source.get("response_byte_length"), f"{label}.response_byte_length")
    if response_length != len(response_bytes):
        fail(f"{label}.response_byte_length does not match the durable assistant response bytes")
    return response, response_sha, response_length


def validate_results(
    results: dict[str, Any],
    pilot: dict[str, Any],
    expected: dict[tuple[str, str], set[str]],
    tie_sets: dict[tuple[str, str], set[str]],
    maximum: int,
    pilot_by_surface: dict[str, dict[str, Any]],
) -> None:
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
    for field in ("agent", "agent_version", "model", "provider"):
        nonempty(runtime.get(field), f"{label}.runtime.{field}")
    if runtime.get("agent") != "Hermes Agent":
        fail(f"{label}.runtime.agent must identify Hermes Agent")

    invocation = results.get("invocation")
    if not isinstance(invocation, dict):
        fail(f"{label}.invocation must be an object")
    required_invocation: dict[str, object] = {
        "executable": "hermes",
        "subcommand": "chat",
        "quiet": True,
        "query_mode": "single-query",
        "session_reuse": False,
        "working_directory": "repo-root",
    }
    for field, required in required_invocation.items():
        if type(invocation.get(field)) is not type(required) or invocation.get(field) != required:
            fail(f"{label}.invocation.{field} must be {required!r}")
    for field in ("command_shape", "provider", "model", "isolation", "context"):
        nonempty(invocation.get(field), f"{label}.invocation.{field}")
    if invocation["provider"] != runtime["provider"]:
        fail(f"{label}.invocation.provider must match runtime.provider")
    if invocation["model"] != runtime["model"]:
        fail(f"{label}.invocation.model must match runtime.model")

    skill_hashes = validate_checkout(results, label)
    records = object_list(results.get("records"), f"{label}.records")
    if len(records) > maximum:
        fail(f"{label}: result count {len(records)} exceeds max_total_samples={maximum}")
    counts: dict[tuple[str, str, str], int] = {}
    session_ids: set[str] = set()
    source_paths: set[str] = set()
    raw_session_models: set[str] = set()
    records_by_surface: dict[str, list[dict[str, Any]]] = {surface: [] for surface in SURFACES}
    for index, record in enumerate(records):
        prefix = f"{label}.records[{index}]"
        surface = nonempty(record.get("surface"), f"{prefix}.surface")
        question_id = nonempty(record.get("question_id"), f"{prefix}.question_id")
        variant_id = nonempty(record.get("variant_id"), f"{prefix}.variant_id")
        key = (surface, question_id)
        if key not in expected or variant_id not in expected[key]:
            fail(f"{prefix}: record does not match a declared pilot variant")
        if surface not in SKILL_PATHS or record.get("canonical_skill_path") != SKILL_PATHS[surface]:
            fail(f"{prefix}.canonical_skill_path must identify the canonical skill for {surface}")
        session_id = nonempty(record.get("session_id"), f"{prefix}.session_id")
        if not SESSION_ID_RE.fullmatch(session_id):
            fail(f"{prefix}.session_id must use the Hermes session identity format")
        if session_id in session_ids:
            fail(f"{prefix}.session_id must be unique across all result records")
        session_ids.add(session_id)
        sample_index = positive_int(record.get("sample_index"), f"{prefix}.sample_index")
        count_key = (surface, question_id, variant_id)
        counts[count_key] = counts.get(count_key, 0) + 1
        if sample_index != counts[count_key]:
            fail(f"{prefix}.sample_index must be contiguous per variant")
        if sample_index == 1 and BASELINE_SESSION_IDS.get(variant_id) != session_id:
            fail(f"{prefix}.session_id must identify the recorded fresh baseline session for {variant_id}")
        if record.get("succeeded") is not True:
            fail(f"{prefix}.succeeded must be true for recorded evidence")

        declared_prompt = nonempty(record.get("declared_prompt"), f"{prefix}.declared_prompt")
        request_sha = nonempty(record.get("request_sha256"), f"{prefix}.request_sha256")
        if not SHA256_RE.fullmatch(request_sha):
            fail(f"{prefix}.request_sha256 must be a lowercase SHA-256")
        if request_sha != hashlib.sha256(declared_prompt.encode("utf-8")).hexdigest():
            fail(f"{prefix}.request_sha256 does not match declared_prompt")

        output_sha = nonempty(record.get("output_sha256"), f"{prefix}.output_sha256")
        if not SHA256_RE.fullmatch(output_sha):
            fail(f"{prefix}.output_sha256 must be a lowercase SHA-256")
        output_length = positive_int(record.get("output_byte_length"), f"{prefix}.output_byte_length")
        excerpt = nonempty(record.get("output_excerpt"), f"{prefix}.output_excerpt")
        if len(excerpt) > 1200:
            fail(f"{prefix}.output_excerpt must stay concise (<=1200 characters)")

        source_relative, source_path = repo_file(record.get("source_path"), f"{prefix}.source_path")
        source_filename = (
            f"{variant_id}.json" if sample_index == 1 else f"{variant_id}-sample-{sample_index}.json"
        )
        expected_source = (
            Path("evals/results/raw/micro-initial-command-wording") / source_filename
        ).as_posix()
        if source_relative != expected_source:
            fail(f"{prefix}.source_path must be the canonical durable source for {variant_id}")
        if source_relative in source_paths:
            fail(f"{prefix}.source_path must be unique per result record")
        source_paths.add(source_relative)
        source_sha = nonempty(record.get("source_sha256"), f"{prefix}.source_sha256")
        if not SHA256_RE.fullmatch(source_sha):
            fail(f"{prefix}.source_sha256 must be a lowercase SHA-256")
        actual_source_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if source_sha != actual_source_sha:
            fail(f"{prefix}.source_sha256 does not match the durable source bytes")

        source = load_json(source_path)
        response, response_sha, response_length = validate_source(
            source_path,
            record,
            cast(str, next(
                variant["prompt"]
                for item in pilot["surfaces"]
                if item["surface"] == surface
                for question in item["questions"]
                if question["id"] == question_id
                for variant in question["variants"]
                if variant["id"] == variant_id
            )),
            skill_hashes[surface],
        )
        if source.get("canonical_skill_path") != SKILL_PATHS[surface]:
            fail(f"{prefix}.source canonical skill path must match the result surface")
        raw_session_models.add(
            validate_tool_evidence(source, source_relative, SKILL_PATHS[surface], skill_hashes[surface])
        )
        if output_sha != response_sha or output_length != response_length:
            fail(f"{prefix}: output hash/length must match the durable assistant response")
        if not response.startswith(excerpt):
            fail(f"{prefix}.output_excerpt must be a prefix of the durable assistant response")

        observation = record.get("observation")
        if not isinstance(observation, dict):
            fail(f"{prefix}.observation must be an object")
        observed_scores = observation.get("rubric")
        if not isinstance(observed_scores, dict) or set(observed_scores) != {
            item["id"] for item in pilot["observation_rubric"]
        }:
            fail(f"{prefix}.observation.rubric must score every declared rubric item")
        if not all(value in {"pass", "partial", "fail"} for value in observed_scores.values()):
            fail(f"{prefix}.observation.rubric values must be pass|partial|fail")
        nonempty(observation.get("notes"), f"{prefix}.observation.notes")
        tied = observation.get("tied")
        if tied is not None and not isinstance(tied, bool):
            fail(f"{prefix}.observation.tied must be boolean when present")
        tie_key = (surface, question_id)
        if sample_index > 1:
            if tie_key not in tie_sets or variant_id not in tie_sets[tie_key]:
                fail(f"{prefix}: extra samples require an explicitly declared question-level tie set")
            if tied is not True:
                fail(f"{prefix}: extra samples require tied=true")
        elif tied is True and (tie_key not in tie_sets or variant_id not in tie_sets[tie_key]):
            fail(f"{prefix}: tied=true is not an authorization for an undeclared tie")

        boolean(record.get("selected_variant"), f"{prefix}.selected_variant")
        nonempty(record.get("selection_rationale"), f"{prefix}.selection_rationale")
        if record.get("status") != "micro-validated":
            fail(f"{prefix}.status must be 'micro-validated'")
        if record.get("evidence_tier") != REAL_AGENT_TIER:
            fail(f"{prefix}.evidence_tier must be {REAL_AGENT_TIER!r}")
        records_by_surface[surface].append(record)

    if len(raw_session_models) != 1:
        fail(f"{label}: raw source session models must agree across all records")
    raw_session_model = next(iter(raw_session_models))
    if runtime["model"] != raw_session_model:
        fail(f"{label}.runtime.model must match the raw source session model")
    if invocation["model"] != raw_session_model:
        fail(f"{label}.invocation.model must match the raw source session model")

    for (surface, question_id), variant_ids in expected.items():
        for variant_id in variant_ids:
            count = counts.get((surface, question_id, variant_id), 0)
            required_count = 1 + (1 if (surface, question_id) in tie_sets and variant_id in tie_sets[(surface, question_id)] else 0)
            if count != required_count:
                fail(
                    f"{label}: {surface}/{question_id}/{variant_id} must have exactly "
                    f"{required_count} sample(s) under the declared tie policy"
                )

    summaries = object_list(results.get("surface_results"), f"{label}.surface_results")
    summary_surface_values = [
        nonempty(item.get("surface"), f"{label}.surface_results[{index}].surface")
        for index, item in enumerate(summaries)
    ]
    if set(summary_surface_values) != SURFACES or len(summaries) != len(SURFACES):
        fail(f"{label}.surface_results must cover exactly {sorted(SURFACES)!r}")
    summary_by_surface: dict[str, dict[str, Any]] = {}
    for summary in summaries:
        surface = nonempty(summary.get("surface"), f"{label}.surface_results.surface")
        if surface in summary_by_surface:
            fail(f"{label}.surface_results contains duplicate surface {surface!r}")
        summary_by_surface[surface] = summary
        pilot_surface = pilot_by_surface[surface]
        if summary.get("status") != pilot_surface.get("status"):
            fail(f"{label}.{surface}.status must match pilot")
        if summary.get("evidence_tier") != pilot_surface.get("evidence_tier"):
            fail(f"{label}.{surface}.evidence_tier must match pilot")
        decision = summary.get("decision")
        if not isinstance(decision, dict):
            fail(f"{label}.{surface}.decision must be an object")
        if decision != pilot_surface.get("decision"):
            fail(f"{label}.{surface}.decision must exactly match the pilot decision")
        if decision.get("public_wording_change") is not False:
            fail(f"{label}.{surface}.decision.public_wording_change must remain false for Issue 1")

    for surface, records_for_surface in records_by_surface.items():
        summary_decision = cast(dict[str, Any], summary_by_surface[surface]["decision"])
        selected = summary_decision.get("selected_variant")
        selected_records = {
            record["variant_id"]
            for record in records_for_surface
            if record.get("selected_variant") is True
        }
        if selected is None or selected_records != {selected}:
            fail(f"{label}.{surface}: records and surface decision must select exactly the same variant")
        for record in records_for_surface:
            if record.get("selected_variant") is not (record.get("variant_id") == selected):
                fail(f"{label}.{surface}: record selected_variant flags must match the surface decision")

    raw_entries = inventory_entries(RAW_DIR, str(RAW_DIR.relative_to(ROOT)))
    actual_raw_files = {
        entry.relative_to(ROOT).as_posix()
        for entry in raw_entries
        if entry.is_file()
    }
    unexpected_raw_dirs = [entry.name for entry in raw_entries if entry.is_dir()]
    if unexpected_raw_dirs:
        fail(f"{RAW_DIR.relative_to(ROOT)} contains unexpected directories: {sorted(unexpected_raw_dirs)!r}")
    if actual_raw_files != source_paths:
        fail(
            f"{RAW_DIR.relative_to(ROOT)} inventory must equal referenced durable sources; "
            f"unexpected={sorted(actual_raw_files - source_paths)!r}, missing={sorted(source_paths - actual_raw_files)!r}"
        )


def main() -> int:
    validate_inventory()
    pilot = load_json(PILOT_PATH)
    expected, tie_sets, maximum, pilot_by_surface = validate_pilot(pilot)
    results = load_json(RESULT_PATH)
    validate_results(results, pilot, expected, tie_sets, maximum, pilot_by_surface)
    digest = hashlib.sha256(RESULT_PATH.read_bytes()).hexdigest()
    print(f"micro eval pilots ok: {len(SURFACES)} surfaces; results sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
