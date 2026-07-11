#!/usr/bin/env python3
"""Adversarial regression tests for the FULL real-agent evidence validator."""
from __future__ import annotations

import copy
import errno
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "check-full-eval-pilots.py"
FULL_RESULT = Path("evals/results/full-reflect-repo-local-safety.json")
FULL_RAW_DIR = Path("evals/results/raw/full-reflect-repo-local-safety")
GAP_RESULT = Path("evals/results/full-gap-stale-sot-precedence.json")
GAP_RAW_DIR = Path("evals/results/raw/full-gap-stale-sot-precedence")

Mutation = Callable[[dict[str, Any], Path], None]


class UnsupportedCase(Exception):
    """A platform does not support a requested filesystem adversarial case."""


def load_result(checkout: Path) -> dict[str, Any]:
    return json.loads((checkout / FULL_RESULT).read_text(encoding="utf-8"))


def load_gap_result(checkout: Path) -> dict[str, Any]:
    return json.loads((checkout / GAP_RESULT).read_text(encoding="utf-8"))


def write_result(checkout: Path, result: dict[str, Any]) -> None:
    (checkout / FULL_RESULT).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_gap_result(checkout: Path, result: dict[str, Any]) -> None:
    (checkout / GAP_RESULT).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def scenario_index(result: dict[str, Any], scenario_id: str) -> int:
    for index, scenario in enumerate(result["scenarios"]):
        if scenario.get("id") == scenario_id:
            return index
    raise AssertionError(f"fixture scenario not found: {scenario_id}")


def rewrite_source(
    checkout: Path,
    result: dict[str, Any],
    scenario_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    index = scenario_index(result, scenario_id)
    record = result["scenarios"][index]
    source_path = checkout / Path(record["source_path"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    mutate(source)
    source_path.write_text(
        json.dumps(source, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    record["source_sha256"] = source_sha256
    refresh_source_anchor(checkout, scenario_id, source_sha256)


def refresh_source_anchor(checkout: Path, scenario_id: str, source_sha256: str) -> None:
    """Refresh only the disposable validator's source anchor for a source mutation."""
    validator_path = checkout / "scripts" / "check-full-eval-pilots.py"
    validator = validator_path.read_text(encoding="utf-8")
    block_start = validator.index("FULL_SOURCE_HASHES = {")
    block_end = validator.index("\n}", block_start) + 2
    block = validator[block_start:block_end]
    key_prefix = f'"{scenario_id}": '
    matches = [
        line_index
        for line_index, line in enumerate(block.splitlines(keepends=True))
        if line.lstrip().startswith(key_prefix)
    ]
    assert len(matches) == 1, f"disposable validator source anchor not found for {scenario_id}"
    lines = block.splitlines(keepends=True)
    line_index = matches[0]
    line = lines[line_index]
    newline = "\n" if line.endswith("\n") else ""
    content = line[:-1] if newline else line
    prefix_start = line.index(key_prefix)
    lines[line_index] = (
        content[: prefix_start + len(key_prefix)]
        + f'"{source_sha256}",'
        + newline
    )
    validator_path.write_text(
        validator[:block_start] + "".join(lines) + validator[block_end:],
        encoding="utf-8",
    )


def rewrite_gap_source(
    checkout: Path,
    result: dict[str, Any],
    scenario_id: str,
    mutate: Callable[[dict[str, Any]], None],
    *,
    refresh_anchor: bool = True,
) -> None:
    index = scenario_index(result, scenario_id)
    record = result["scenarios"][index]
    source_path = checkout / Path(record["source_path"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    mutate(source)
    source_path.write_text(
        json.dumps(source, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    record["source_sha256"] = source_sha256
    if refresh_anchor:
        refresh_gap_source_anchor(checkout, scenario_id, source_sha256)


def refresh_gap_source_anchor(checkout: Path, scenario_id: str, source_sha256: str) -> None:
    """Refresh only the disposable validator's GAP source anchor."""
    validator_path = checkout / "scripts" / "check-full-eval-pilots.py"
    validator = validator_path.read_text(encoding="utf-8")
    block_start = validator.index("GAP_SOURCE_HASHES = {")
    block_end = validator.index("\n}", block_start) + 2
    block = validator[block_start:block_end]
    key_prefix = f'"{scenario_id}": '
    matches = [
        line_index
        for line_index, line in enumerate(block.splitlines(keepends=True))
        if line.lstrip().startswith(key_prefix)
    ]
    assert len(matches) == 1, f"disposable GAP source anchor not found for {scenario_id}"
    lines = block.splitlines(keepends=True)
    line_index = matches[0]
    line = lines[line_index]
    newline = "\n" if line.endswith("\n") else ""
    content = line[:-1] if newline else line
    prefix_start = line.index(key_prefix)
    lines[line_index] = content[: prefix_start + len(key_prefix)] + f'"{source_sha256}",' + newline
    validator_path.write_text(
        validator[:block_start] + "".join(lines) + validator[block_end:],
        encoding="utf-8",
    )


def swap_directory_for_symlink(path: Path) -> None:
    real_path = path.with_name(path.name + "-real")
    path.rename(real_path)
    path.symlink_to(real_path.name, target_is_directory=True)


def prepare_checkout(temp_root: Path) -> Path:
    checkout = temp_root / "relocated-tiger-kit"
    shutil.copytree(ROOT, checkout, symlinks=True)
    return checkout


def run_validator(checkout: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(checkout / "scripts" / "check-full-eval-pilots.py")],
        cwd=checkout,
        capture_output=True,
        text=True,
        check=False,
    )


def missing_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"].pop()


def duplicate_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"].append(copy.deepcopy(result["scenarios"][0]))


def extra_scenario(result: dict[str, Any], _checkout: Path) -> None:
    extra = copy.deepcopy(result["scenarios"][0])
    extra["id"] = "unexpected-scenario"
    result["scenarios"].append(extra)


def forged_source_hash(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["source_sha256"] = "a" * 64


def forged_result_hash(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["assistant_result_sha256"] = "b" * 64


def wrong_reason(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["receipt"].update({"reason_code": "`not_ignored`"}),
    )


def eligible_extra_changed_path(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "eligible-repo-local-apply",
        lambda source: source["receipt"]["changed_paths"].append("`git-root/extra.txt`"),
    )


def tracked_target_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["fixture"]["target"]["after"].update({"sha256": "c" * 64}),
    )


def not_ignored_target_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "not-ignored-claude-local-reject",
        lambda source: source["fixture"]["target"]["after"].update({"sha256": "d" * 64}),
    )


def ignore_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "not-ignored-claude-local-reject",
        lambda source: source["fixture"]["ignore_files"][0]["after"].update({"sha256": "e" * 64}),
    )


def ignore_second_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "not-ignored-claude-local-reject",
        lambda source: source["fixture"]["ignore_files"][1]["after"].update(
            {"mode": "0o600", "sha256": "f" * 64}
        ),
    )


def symlink_target_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "symlink-claude-local-reject",
        lambda source: source["fixture"]["external_target"].update({"sha256": "f" * 64}),
    )


def target_inventory_mismatch(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        target = source["fixture"]["target"]
        target["before"]["sha256"] = "c" * 64
        target["after"]["sha256"] = "c" * 64

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def external_target_inventory_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "symlink-claude-local-reject",
        lambda source: source["fixture"]["external_target"].update({"sha256": "f" * 64}),
    )


def fixture_inventory_bad_type(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["fixture"].update({"fixture_inventory_before": ["not-an-inventory-record"]}),
    )


def fixture_inventory_missing_field(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for inventory_name in ("fixture_inventory_before", "fixture_inventory_after"):
            source["fixture"][inventory_name][1].pop("size")

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def fixture_inventory_duplicate_path(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        inventory = source["fixture"]["fixture_inventory_before"]
        inventory.append(copy.deepcopy(inventory[0]))

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def fixture_inventory_unknown_kind(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for inventory_name in ("fixture_inventory_before", "fixture_inventory_after"):
            source["fixture"][inventory_name][0]["kind"] = "directory"

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def state_inventory_bad_type(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["state_root"].update({"inventory_after": ["not-an-inventory-record"]}),
    )


def state_inventory_missing_field(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["state_root"]["inventory_after"][0].pop("size")

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def state_inventory_duplicate_path(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        inventory = source["state_root"]["inventory_after"]
        inventory.append(copy.deepcopy(inventory[0]))

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def state_inventory_unknown_kind(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for item in source["state_root"]["inventory_after"]:
            item["kind"] = "directory"

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def git_snapshot_missing_head(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for snapshot_name in ("git_before", "git_after"):
            source["fixture"][snapshot_name].pop("head")

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def git_snapshot_boolean_status(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for snapshot_name in ("git_before", "git_after"):
            source["fixture"][snapshot_name]["rev_parse_status"] = True

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def git_snapshot_bad_status_porcelain(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for snapshot_name in ("git_before", "git_after"):
            source["fixture"][snapshot_name]["status_porcelain"] = ""

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def git_snapshot_bad_non_git_head(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for snapshot_name in ("git_before", "git_after"):
            source["fixture"][snapshot_name] = {
                **source["fixture"][snapshot_name],
                "is_worktree": False,
                "rev_parse_status": 128,
                "head": "not-a-sha",
                "branch": None,
            }

    rewrite_source(checkout, result, "non-git-repo-local-reject", mutate)


def symlink_link_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "symlink-claude-local-reject",
        lambda source: source["fixture"]["target"]["after"].update({"link_text": "../other-target.txt"}),
    )


def honored_observed_root_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "not-ignored-claude-local-reject",
        lambda source: source["state_root"].update({"honored": True}),
    )


def inventory_observed_root_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "not-ignored-claude-local-reject",
        lambda source: source["state_root"]["inventory_after"][0].update(
            {"path": "state-root/repos/git-root/branches/main/reflect/REFLECT-20260711-183816-e257.yaml"}
        ),
    )


def non_git_fallback_write(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "non-git-repo-local-reject",
        lambda source: source["fixture"].update(
            {"fallback_writes": [{"path": "fixture-root/CLAUDE.local.md", "kind": "regular"}]}
        ),
    )


def reused_session_id(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][1]["session_id"] = result["scenarios"][0]["session_id"]


def wrapper_consumer_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "eligible-repo-local-apply",
        lambda source: source["session"].update(
            {"wrapper": "other-wrapper", "consumer": "Other Consumer"}
        ),
    )


def model_usage_mismatch(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["runtime"]["model_usage"]["gpt-5.5(high)"]["outputTokens"] += 1

    rewrite_source(checkout, result, "eligible-repo-local-apply", mutate)


def plugin_commit_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "eligible-repo-local-apply",
        lambda source: source["plugin"].update({"commit": "0" * 40}),
    )


def live_plugin_blob_mismatch(_result: dict[str, Any], checkout: Path) -> None:
    contract = checkout / "commands" / "reflect.md"
    contract.write_bytes(contract.read_bytes() + b"\nundeclared live plugin mutation\n")


def source_path_traversal(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["source_path"] = "../full-pilots/reflect-repo-local-safety.json"


def source_symlink_substitution(result: dict[str, Any], checkout: Path) -> None:
    source_path = checkout / Path(result["scenarios"][0]["source_path"])
    alternate = checkout / Path(result["scenarios"][1]["source_path"])
    source_path.unlink()
    source_path.symlink_to(alternate)


def make_fifo(path: Path) -> None:
    try:
        os.mkfifo(path)
    except (AttributeError, NotImplementedError) as exc:
        raise UnsupportedCase("named pipes are unsupported on this platform") from exc
    except OSError as exc:
        unsupported_errors = {
            getattr(errno, "ENOSYS", -1),
            getattr(errno, "ENOTSUP", -1),
            getattr(errno, "EOPNOTSUPP", -1),
        }
        if exc.errno in unsupported_errors:
            raise UnsupportedCase("named pipes are unsupported on this platform") from exc
        raise


def raw_special_entry(_result: dict[str, Any], checkout: Path) -> None:
    make_fifo(checkout / FULL_RAW_DIR / "unexpected.fifo")


def gap_raw_directory_symlink(_result: dict[str, Any], checkout: Path) -> None:
    swap_directory_for_symlink(checkout / GAP_RAW_DIR)


def unexpected_root_result_file(_result: dict[str, Any], checkout: Path) -> None:
    (checkout / "evals" / "results" / "unexpected.json").write_text("{}\n", encoding="utf-8")


def gap_wrong_classification(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["final_classification"] = "missing"


def gap_missing_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"].pop()


def gap_duplicate_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][1]["id"] = result["scenarios"][0]["id"]


def gap_extra_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][2]["id"] = "unexpected-gap-scenario"


def gap_missing_source_ref(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["source_refs"].pop(),
    )


def gap_missing_manifest_entry(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "unresolved-source-precedence-stays-ambiguous",
        lambda source: source["gap_observation"]["source_refs"].pop(1),
    )


def gap_source_role_swap(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["source_refs"][0].update({"role": "Current"}),
    )


def gap_evidence_type_swap(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["current_evidence"][0].update({"type": "runtime"}),
    )


def gap_precedence_falsely_resolved(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["gap_observation"]["precedence"].update(
            {"status": "resolved", "resolved_order": ["S1", "S2"]}
        )

    rewrite_gap_source(checkout, result, "unresolved-source-precedence-stays-ambiguous", mutate)


def gap_precedence_fake_resolved_order(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "unresolved-source-precedence-stays-ambiguous",
        lambda source: source["gap_observation"]["precedence"].update({"resolved_order": ["S2"]}),
    )


def gap_direct_implementation_evidence(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "plan-only-current-is-not-implementation-proof",
        lambda source: source["gap_observation"].update(
            {"direct_implementation_evidence": [{"evidence_id": "C1", "type": "file-read", "strength": "direct"}]}
        ),
    )


def gap_direct_runtime_evidence(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "plan-only-current-is-not-implementation-proof",
        lambda source: source["gap_observation"].update(
            {"direct_runtime_evidence": [{"evidence_id": "C2", "type": "runtime", "strength": "direct"}]}
        ),
    )


def gap_empty_recommendation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"].update({"recommendation": ""}),
    )


def gap_prompt_hash_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["command"].update({"prompt_sha256": "0" * 64}),
    )


def gap_prompt_length_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["command"].update({"prompt_byte_length": source["command"]["prompt_byte_length"] + 1}),
    )


def gap_result_prompt_hash_mutation(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["prompt_sha256"] = "0" * 64


def gap_result_prompt_length_mutation(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["prompt_byte_length"] += 1


def gap_assistant_result_hash_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["consumer_output"].update(
            {"result_sha256": "0" * 64, "raw_result_sha256": "0" * 64}
        ),
    )


def gap_assistant_result_length_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["consumer_output"].update(
            {"result_byte_length": source["consumer_output"]["result_byte_length"] + 1}
        ),
    )


def gap_result_assistant_result_hash_mutation(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["assistant_result_sha256"] = "0" * 64


def gap_result_assistant_result_length_mutation(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["assistant_result_byte_length"] += 1


def gap_source_hash_anchor_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["privacy"]["normalized_paths"].append("unapproved-token"),
        refresh_anchor=False,
    )


def gap_source_manifest_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"].update({"source_manifest_sha256": "0" * 64}),
    )


def gap_reused_session_id(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][1]["session_id"] = result["scenarios"][0]["session_id"]


def gap_wrapper_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["session"].update({"wrapper": "other-wrapper"}),
    )


def gap_consumer_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["session"].update({"consumer": "Other Consumer"}),
    )


def gap_provider_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["session"].update({"provider": "other-provider"}),
    )


def gap_model_usage_mismatch(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["runtime"]["model_usage"]["gpt-5.5(high)"]["outputTokens"] += 1

    rewrite_gap_source(checkout, result, "stale-plan-vs-live-surface-conflict", mutate)


def gap_derived_model_mismatch(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["model"] = "configured-default"


def gap_git_head_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].update({"head": "0" * 40}),
    )


def gap_git_status_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].update({"status_porcelain": [" M README.md"]}),
    )


def gap_git_staged_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].update({"staged_paths": ["README.md"]}),
    )


def gap_git_unstaged_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].update({"unstaged_paths": ["README.md"]}),
    )


def gap_requested_state_root_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["state_root"].update({"requested": "alternate-state-root"}),
    )


def gap_temp_home_inventory_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["temporary_home_tigerkit"]["inventory_after"].append(
            {
                "path": "temporary-home/.tigerkit/injected.json",
                "kind": "regular",
                "mode": "0o600",
                "size": 0,
                "sha256": "0" * 64,
            }
        ),
    )


def gap_packet_write_injection(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"].update(
            {"fallback_writes": [{"path": "fixture-root/gap-packet.json", "kind": "regular"}]}
        ),
    )


def gap_source_path_traversal(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["source_path"] = "../full-pilots/gap-stale-sot-precedence.json"


def gap_source_symlink_substitution(result: dict[str, Any], checkout: Path) -> None:
    source_path = checkout / Path(result["scenarios"][0]["source_path"])
    alternate = checkout / Path(result["scenarios"][1]["source_path"])
    source_path.unlink()
    source_path.symlink_to(alternate)


def gap_raw_special_entry(_result: dict[str, Any], checkout: Path) -> None:
    make_fifo(checkout / GAP_RAW_DIR / "unexpected.fifo")


def gap_plugin_commit_mismatch(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["plugin"].update({"commit": "0" * 40}),
    )


def gap_live_contract_blob_mismatch(_result: dict[str, Any], checkout: Path) -> None:
    contract = checkout / "commands" / "gap.md"
    contract.write_bytes(contract.read_bytes() + b"\nundeclared GAP live contract mutation\n")


def gap_malformed_source_manifest(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"].update({"source_manifest_sha256": "not-a-hash"}),
    )


def gap_malformed_source_ref(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["source_refs"][0].pop("byte_length"),
    )


def gap_malformed_git_record(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].pop("head"),
    )


def gap_malformed_state_record(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["state_root"].update({"inventory_before": {"unexpected": "record"}}),
    )


CASES: list[tuple[str, Mutation, str | None]] = [
    ("missing scenario", missing_scenario, None),
    ("duplicate scenario", duplicate_scenario, None),
    ("extra scenario", extra_scenario, None),
    ("forged source hash", forged_source_hash, "source_sha256 does not match"),
    ("forged assistant result hash", forged_result_hash, None),
    ("wrong reason", wrong_reason, "receipt.reason_code does not match"),
    ("eligible extra changed path", eligible_extra_changed_path, "receipt.changed_paths does not match"),
    ("tracked target mutation", tracked_target_mutation, "rejected target state changed"),
    ("not-ignored target mutation", not_ignored_target_mutation, "rejected target state changed"),
    ("ignore mutation", ignore_mutation, "ignore file"),
    ("second ignore mutation", ignore_second_mutation, "ignore file"),
    ("symlink target mutation", symlink_target_mutation, "external target"),
    ("symlink link mutation", symlink_link_mutation, "link text changed"),
    ("target/inventory mismatch", target_inventory_mismatch, "target"),
    ("external target/inventory mismatch", external_target_inventory_mismatch, "external target"),
    ("fixture inventory bad type", fixture_inventory_bad_type, "must be an object"),
    ("fixture inventory missing field", fixture_inventory_missing_field, "size"),
    ("fixture inventory duplicate path", fixture_inventory_duplicate_path, "duplicate path"),
    ("fixture inventory unknown kind", fixture_inventory_unknown_kind, "kind"),
    ("state inventory bad type", state_inventory_bad_type, "must be an object"),
    ("state inventory missing field", state_inventory_missing_field, "size"),
    ("state inventory duplicate path", state_inventory_duplicate_path, "duplicate path"),
    ("state inventory unknown kind", state_inventory_unknown_kind, "kind"),
    ("Git snapshot missing head", git_snapshot_missing_head, "head"),
    ("Git snapshot boolean status", git_snapshot_boolean_status, "rev_parse_status"),
    ("Git snapshot bad status porcelain", git_snapshot_bad_status_porcelain, "status_porcelain"),
    ("non-Git snapshot bad head", git_snapshot_bad_non_git_head, "head"),
    ("honored/observed state-root mismatch", honored_observed_root_mismatch, "honored"),
    ("inventory/observed state-root mismatch", inventory_observed_root_mismatch, "observed_root"),
    ("non-git fallback write", non_git_fallback_write, None),
    ("reused session ID", reused_session_id, None),
    ("wrapper/consumer mismatch", wrapper_consumer_mismatch, None),
    ("modelUsage mismatch", model_usage_mismatch, None),
    ("plugin commit mismatch", plugin_commit_mismatch, None),
    ("plugin live blob mismatch", live_plugin_blob_mismatch, None),
    ("source traversal", source_path_traversal, None),
    ("source symlink substitution", source_symlink_substitution, None),
    ("source special entry", raw_special_entry, None),
    ("approved GAP raw directory symlink", gap_raw_directory_symlink, None),
    ("unexpected root result file", unexpected_root_result_file, None),
]

GAP_CASES: list[tuple[str, Mutation, str | None]] = [
    ("GAP missing scenario", gap_missing_scenario, "scenarios must contain exactly the three approved scenario records"),
    ("GAP duplicate scenario", gap_duplicate_scenario, "scenarios must contain exactly the approved scenario IDs in order"),
    ("GAP extra scenario", gap_extra_scenario, "scenarios must contain exactly the approved scenario IDs in order"),
    ("GAP missing source ref", gap_missing_source_ref, "source_refs role/type/path/hash/access records do not match"),
    ("GAP missing manifest entry", gap_missing_manifest_entry, "source_refs role/type/path/hash/access records do not match"),
    ("GAP source role swap", gap_source_role_swap, "source_refs role/type/path/hash/access records do not match"),
    ("GAP evidence type swap", gap_evidence_type_swap, "type must match its source-ref type"),
    ("GAP scenario2 falsely resolved", gap_precedence_falsely_resolved, "does not preserve the approved source-precedence decision"),
    ("GAP scenario2 fake resolved order", gap_precedence_fake_resolved_order, "does not preserve the approved source-precedence decision"),
    ("GAP scenario3 direct implementation evidence", gap_direct_implementation_evidence, "direct_implementation_evidence must be empty"),
    ("GAP scenario3 direct runtime evidence", gap_direct_runtime_evidence, "direct_runtime_evidence must be empty"),
    ("GAP empty recommendation", gap_empty_recommendation, "recommendation must be a non-empty string"),
    ("GAP raw prompt hash mutation", gap_prompt_hash_mutation, "command.prompt_sha256 does not match the approved exact request"),
    ("GAP raw prompt length mutation", gap_prompt_length_mutation, "command.prompt_byte_length does not match the approved request"),
    ("GAP result prompt hash mutation", gap_result_prompt_hash_mutation, "prompt hash/length does not match the exact recorded request"),
    ("GAP result prompt length mutation", gap_result_prompt_length_mutation, "prompt hash/length does not match the exact recorded request"),
    ("GAP raw assistant result hash mutation", gap_assistant_result_hash_mutation, "consumer_output result hashes do not match the approved assistant result"),
    ("GAP raw assistant result length mutation", gap_assistant_result_length_mutation, "consumer_output result hash/length does not match the exact result bytes"),
    ("GAP result assistant hash mutation", gap_result_assistant_result_hash_mutation, "assistant result hash/length does not match the canonical result"),
    ("GAP result assistant length mutation", gap_result_assistant_result_length_mutation, "assistant result hash/length does not match the canonical result"),
    ("GAP raw source hash anchor mismatch", gap_source_hash_anchor_mismatch, "source_sha256 does not match the canonical durable source"),
    ("GAP deterministic source manifest mismatch", gap_source_manifest_mismatch, "source_manifest_sha256 does not bind the deterministic source inventory"),
    ("GAP reused session ID", gap_reused_session_id, "session_id must be unique across all GAP scenarios"),
    ("GAP wrapper mismatch", gap_wrapper_mismatch, "session must preserve the actual isolated runtime and derived model truth"),
    ("GAP consumer mismatch", gap_consumer_mismatch, "session must preserve the actual isolated runtime and derived model truth"),
    ("GAP provider mismatch", gap_provider_mismatch, "session must preserve the actual isolated runtime and derived model truth"),
    ("GAP modelUsage mismatch", gap_model_usage_mismatch, "runtime.model_usage does not match the actual recorded modelUsage"),
    ("GAP derived-model mismatch", gap_derived_model_mismatch, "model/model_usage_keys must preserve the derived actual routing"),
    ("GAP Git HEAD mutation", gap_git_head_mutation, "git_before.head must preserve the recorded fixture Git HEAD"),
    ("GAP Git status mutation", gap_git_status_mutation, "git_before.status_porcelain must be an empty list for the read-only run"),
    ("GAP Git staged mutation", gap_git_staged_mutation, "git_before.staged_paths must be an empty list for the read-only run"),
    ("GAP Git unstaged mutation", gap_git_unstaged_mutation, "git_before.unstaged_paths must be an empty list for the read-only run"),
    ("GAP requested state-root mutation", gap_requested_state_root_mutation, "state_root requested/observed roots must be 'state-root'"),
    ("GAP temp-home inventory mutation", gap_temp_home_inventory_mutation, "temporary_home_tigerkit.inventory_after must be empty"),
    ("GAP packet/write injection", gap_packet_write_injection, "fixture.fallback_writes must be empty"),
    ("GAP source path traversal", gap_source_path_traversal, "source_path must be a normalized POSIX path relative to the checkout"),
    ("GAP source symlink substitution", gap_source_symlink_substitution, "must not contain symlinks"),
    ("GAP raw source special entry", gap_raw_special_entry, "contains an unsupported special entry"),
    ("GAP plugin commit mismatch", gap_plugin_commit_mismatch, ".plugin must identify the recorded plugin checkout and commit"),
    ("GAP live contract blob mismatch", gap_live_contract_blob_mismatch, "live contract blob differs from the immutable Git blob"),
    ("GAP malformed source manifest", gap_malformed_source_manifest, "source_manifest_sha256 must be a lowercase SHA-256"),
    ("GAP malformed source ref", gap_malformed_source_ref, "gap_observation.source_refs[0] has malformed fields"),
    ("GAP malformed Git record", gap_malformed_git_record, "fixture.git_before has malformed fields"),
    ("GAP malformed state record", gap_malformed_state_record, "state_root.inventory_before must be a list"),
    ("GAP wrong classification", gap_wrong_classification, "final_classification"),
]


def assert_controlled_rejection(
    name: str,
    completed: subprocess.CompletedProcess[str],
    expected_fragment: str | None = None,
) -> None:
    output = completed.stdout + completed.stderr
    assert completed.returncode != 0, f"{name}: mutation was accepted"
    assert "Traceback" not in output, f"{name}: validator raised an uncontrolled traceback: {output}"
    assert "full eval pilot check failed:" in output, output
    if expected_fragment is not None:
        assert expected_fragment in output, (
            f"{name}: rejection did not reach the intended semantic diagnostic "
            f"{expected_fragment!r}: {output}"
        )


def test_missing_reflect_result_is_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="tiger-kit-full-validator-") as temp_dir:
        checkout = prepare_checkout(Path(temp_dir))
        result_path = checkout / FULL_RESULT
        if result_path.exists():
            result_path.unlink()
        completed = run_validator(checkout)
        output = completed.stdout + completed.stderr
        assert completed.returncode != 0, "missing FULL result was accepted"
        assert "full-reflect-repo-local-safety.json" in output, output
        assert "full eval pilot check failed:" in output, output


def test_missing_gap_result_is_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="tiger-kit-full-validator-") as temp_dir:
        checkout = prepare_checkout(Path(temp_dir))
        result_path = checkout / GAP_RESULT
        if result_path.exists():
            result_path.unlink()
        completed = run_validator(checkout)
        output = completed.stdout + completed.stderr
        assert completed.returncode != 0, "missing GAP result was accepted"
        assert "missing required result file: evals/results/full-gap-stale-sot-precedence.json" in output, output
        assert "full eval pilot check failed:" in output, output



def test_not_ignored_requires_explicit_ignore_file_states() -> None:
    with tempfile.TemporaryDirectory(prefix="tiger-kit-full-validator-") as temp_dir:
        checkout = prepare_checkout(Path(temp_dir))
        result = load_result(checkout)
        index = scenario_index(result, "not-ignored-claude-local-reject")
        source_path = checkout / Path(result["scenarios"][index]["source_path"])
        source = json.loads(source_path.read_text(encoding="utf-8"))
        ignore_files = source["fixture"]["ignore_files"]
        assert len(ignore_files) == 2, ignore_files
        second = ignore_files[1]
        assert "before" in second and "after" in second, (
            "second ignore file lacks explicit before/after snapshots"
        )
        completed = run_validator(checkout)
        output = completed.stdout + completed.stderr
        assert completed.returncode == 0, output


def main() -> int:
    test_missing_reflect_result_is_rejected()
    test_missing_gap_result_is_rejected()
    test_not_ignored_requires_explicit_ignore_file_states()
    failures: list[str] = []
    skipped = 0
    with tempfile.TemporaryDirectory(prefix="tiger-kit-full-validator-") as temp_dir:
        temp_root = Path(temp_dir)
        for name, mutate, expected_fragment in CASES:
            checkout = prepare_checkout(temp_root / name.replace(" ", "-"))
            result = load_result(checkout)
            try:
                mutate(result, checkout)
            except UnsupportedCase as exc:
                skipped += 1
                print(f"skips {name}: {exc}")
                continue
            write_result(checkout, result)
            completed = run_validator(checkout)
            try:
                assert_controlled_rejection(name, completed, expected_fragment)
            except AssertionError as exc:
                failures.append(str(exc))
            else:
                print(f"rejects {name}: exit={completed.returncode}")

        for name, mutate, expected_fragment in GAP_CASES:
            checkout = prepare_checkout(temp_root / name.replace(" ", "-"))
            result = load_gap_result(checkout)
            try:
                mutate(result, checkout)
            except UnsupportedCase as exc:
                skipped += 1
                print(f"skips {name}: {exc}")
                continue
            write_gap_result(checkout, result)
            completed = run_validator(checkout)
            try:
                assert_controlled_rejection(name, completed, expected_fragment)
            except AssertionError as exc:
                failures.append(str(exc))
            else:
                print(f"rejects {name}: exit={completed.returncode}")

        relocated = prepare_checkout(temp_root / "relocated-valid")
        completed = run_validator(relocated)
        if completed.returncode != 0:
            failures.append(
                "relocated checkout: valid artifact was rejected: "
                + (completed.stderr or completed.stdout).strip()
            )
        else:
            print("accepts relocated valid checkout")

        missing = prepare_checkout(temp_root / "missing-gap-result")
        (missing / GAP_RESULT).unlink()
        completed = run_validator(missing)
        if completed.returncode == 0:
            failures.append("missing GAP result: mutation was accepted")
        else:
            output = completed.stdout + completed.stderr
            if "missing required result file: evals/results/full-gap-stale-sot-precedence.json" not in output:
                failures.append("missing GAP result: rejection did not reach the intended inventory diagnostic: " + output)
            else:
                print("rejects missing GAP result: exit=1")

    if failures:
        print("full validator adversarial tests failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"full validator adversarial tests ok: {len(CASES) + len(GAP_CASES) - skipped} rejection cases"
        f" + relocation + missing result ({skipped} skipped)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
