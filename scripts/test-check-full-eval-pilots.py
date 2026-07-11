#!/usr/bin/env python3
"""Adversarial regression tests for the FULL real-agent evidence validator."""
from __future__ import annotations

import copy
import errno
import hashlib
import importlib.util
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


def load_gap_source(checkout: Path, scenario_id: str) -> dict[str, Any]:
    return json.loads(
        (checkout / GAP_RAW_DIR / f"{scenario_id}.json").read_text(encoding="utf-8")
    )


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


def forged_source_hash(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["source_sha256"] = "a" * 64


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


def target_inventory_mismatch(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        target = source["fixture"]["target"]
        target["before"]["sha256"] = "c" * 64
        target["after"]["sha256"] = "c" * 64

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


def fixture_inventory_bad_type(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["fixture"].update({"fixture_inventory_before": ["not-an-inventory-record"]}),
    )


def state_inventory_bad_type(result: dict[str, Any], checkout: Path) -> None:
    rewrite_source(
        checkout,
        result,
        "tracked-claude-local-reject",
        lambda source: source["state_root"].update({"inventory_after": ["not-an-inventory-record"]}),
    )


def git_snapshot_bad_status_porcelain(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        for snapshot_name in ("git_before", "git_after"):
            source["fixture"][snapshot_name]["status_porcelain"] = ""

    rewrite_source(checkout, result, "tracked-claude-local-reject", mutate)


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


def live_plugin_blob_mismatch(_result: dict[str, Any], checkout: Path) -> None:
    contract = checkout / "commands" / "reflect.md"
    contract.write_bytes(contract.read_bytes() + b"\nundeclared live plugin mutation\n")


def source_path_traversal(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["source_path"] = "../full-pilots/reflect-repo-local-safety.json"


def unexpected_root_result_file(_result: dict[str, Any], checkout: Path) -> None:
    (checkout / "evals" / "results" / "unexpected.json").write_text("{}\n", encoding="utf-8")


def gap_wrong_classification(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"][0]["final_classification"] = "missing"


def gap_missing_scenario(result: dict[str, Any], _checkout: Path) -> None:
    result["scenarios"].pop()


def gap_missing_source_ref(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["source_refs"].pop(),
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
        lambda source: source["gap_observation"].update(
            {"recommendation": "1. Decide precedence between S1 and C2."}
        ),
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


def gap_assistant_result_hash_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["consumer_output"].update(
            {"result_sha256": "0" * 64, "raw_result_sha256": "0" * 64}
        ),
    )


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


def gap_model_usage_mismatch(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["runtime"]["model_usage"]["gpt-5.5(high)"]["outputTokens"] += 1

    rewrite_gap_source(checkout, result, "stale-plan-vs-live-surface-conflict", mutate)


def gap_git_status_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["fixture"]["git_before"].update({"status_porcelain": [" M README.md"]}),
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


def gap_live_contract_blob_mismatch(_result: dict[str, Any], checkout: Path) -> None:
    contract = checkout / "commands" / "gap.md"
    contract.write_bytes(contract.read_bytes() + b"\nundeclared GAP live contract mutation\n")


def gap_malformed_source_ref(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["gap_observation"]["source_refs"][0].pop("byte_length"),
    )


def gap_runtime_home_unrecorded_delta(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["runtime_home"]["inventory_after"].append(
            {
                "path": "temporary-home/.claude/unrecorded.json",
                "kind": "regular",
                "mode": "0o600",
                "size": 0,
                "sha256": "0" * 64,
            }
        )

    rewrite_gap_source(checkout, result, "stale-plan-vs-live-surface-conflict", mutate)


def gap_false_write_free_claim(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["session"].update({"write_free": True}),
    )


def gap_product_surface_plugin_write(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["product_surface"].update(
            {"plugin_changed_paths": ["plugin-root/commands/gap.md"]}
        ),
    )


def gap_state_honor_status_mutation(result: dict[str, Any], checkout: Path) -> None:
    rewrite_gap_source(
        checkout,
        result,
        "stale-plan-vs-live-surface-conflict",
        lambda source: source["state_root"].update({"honor_status": "honored"}),
    )


CASES: list[tuple[str, Mutation, str | None]] = [
    ("missing scenario", missing_scenario, None),
    ("forged source hash", forged_source_hash, "source_sha256 does not match"),
    ("wrong reason", wrong_reason, "receipt.reason_code does not match"),
    ("eligible extra changed path", eligible_extra_changed_path, "receipt.changed_paths does not match"),
    ("tracked target mutation", tracked_target_mutation, "rejected target state changed"),
    ("not-ignored target mutation", not_ignored_target_mutation, "rejected target state changed"),
    ("ignore mutation", ignore_mutation, "ignore file"),
    ("symlink link mutation", symlink_link_mutation, "link text changed"),
    ("target/inventory mismatch", target_inventory_mismatch, "target"),
    ("fixture inventory bad type", fixture_inventory_bad_type, "must be an object"),
    ("state inventory bad type", state_inventory_bad_type, "must be an object"),
    ("Git snapshot bad status porcelain", git_snapshot_bad_status_porcelain, "status_porcelain"),
    ("honored/observed state-root mismatch", honored_observed_root_mismatch, "honored"),
    ("non-git fallback write", non_git_fallback_write, None),
    ("reused session ID", reused_session_id, None),
    ("wrapper/consumer mismatch", wrapper_consumer_mismatch, None),
    ("plugin live blob mismatch", live_plugin_blob_mismatch, None),
    ("source traversal", source_path_traversal, None),
    ("unexpected root result file", unexpected_root_result_file, None),
]

GAP_CASES: list[tuple[str, Mutation, str | None]] = [
    ("GAP missing scenario", gap_missing_scenario, "scenarios must contain exactly the three approved scenario records"),
    ("GAP missing source ref", gap_missing_source_ref, "source_refs role/type/path/hash/access records do not match"),
    ("GAP source role swap", gap_source_role_swap, "source_refs role/type/path/hash/access records do not match"),
    ("GAP evidence type swap", gap_evidence_type_swap, "type must match its source-ref type"),
    ("GAP scenario2 falsely resolved", gap_precedence_falsely_resolved, "does not preserve the approved source-precedence decision"),
    ("GAP recommendation source-role mismatch", gap_precedence_fake_resolved_order, "recommendation must keep the source-precedence decision between S1 and S2"),
    ("GAP scenario3 direct implementation evidence", gap_direct_implementation_evidence, "direct_implementation_evidence must be empty"),
    ("GAP empty recommendation", gap_empty_recommendation, "recommendation must be a non-empty string"),
    ("GAP raw prompt hash mutation", gap_prompt_hash_mutation, "command.prompt_sha256 does not match the approved exact request"),
    ("GAP raw assistant result hash mutation", gap_assistant_result_hash_mutation, "consumer_output result hashes do not match the approved assistant result"),
    ("GAP raw source hash anchor mismatch", gap_source_hash_anchor_mismatch, "source_sha256 does not match the canonical durable source"),
    ("GAP deterministic source manifest mismatch", gap_source_manifest_mismatch, "source_manifest_sha256 does not bind the deterministic source inventory"),
    ("GAP reused session ID", gap_reused_session_id, "session_id must be unique across all GAP scenarios"),
    ("GAP wrapper mismatch", gap_wrapper_mismatch, "session must preserve the actual isolated runtime and derived model truth"),
    ("GAP modelUsage mismatch", gap_model_usage_mismatch, "runtime.model_usage does not match the actual recorded modelUsage"),
    ("GAP Git status mutation", gap_git_status_mutation, "git_before.status_porcelain must be an empty list for the read-only run"),
    ("GAP packet/write injection", gap_packet_write_injection, "fixture.fallback_writes must be empty"),
    ("GAP source path traversal", gap_source_path_traversal, "source_path must be a normalized POSIX path relative to the checkout"),
    ("GAP live contract blob mismatch", gap_live_contract_blob_mismatch, "live contract blob differs from the immutable Git blob"),
    ("GAP malformed source ref", gap_malformed_source_ref, "gap_observation.source_refs[0] has malformed fields"),
    ("GAP unrecorded runtime-home delta", gap_runtime_home_unrecorded_delta, "runtime_home.changed_paths must match the complete before/after delta"),
    ("GAP false write-free claim", gap_false_write_free_claim, "session.write_free must be false when runtime_home.changed_paths is non-empty"),
    ("GAP product plugin write", gap_product_surface_plugin_write, "product_surface.plugin_changed_paths must be empty"),
    ("GAP state honor status mutation", gap_state_honor_status_mutation, "state_root.honor_status must be 'not_observable_no_writes'"),
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


def test_gap_scenario3_prompt_is_neutral() -> None:
    leakage_markers = (
        "pilot.expected",
        "pilot.must_observe",
        "must_observe",
        "expected classification",
        "expected gap",
        "expected treatment",
        "a plan or generated artifact",
        "not direct implementation",
        "keep the absence",
        "absence of direct current evidence",
        "do not infer the presence",
        "must remain ambiguous",
        "must be missing",
    )
    for scenario_id in (
        "stale-plan-vs-live-surface-conflict",
        "unresolved-source-precedence-stays-ambiguous",
        "plan-only-current-is-not-implementation-proof",
    ):
        source = load_gap_source(ROOT, scenario_id)
        prompt = source["command"]["argv"][3]
        assert isinstance(prompt, str)
        found = [marker for marker in leakage_markers if marker in prompt.lower()]
        assert not found, f"{scenario_id} prompt leaks expected evidence treatment: {found!r}"


def test_gap_scenarios_record_complete_runtime_home_inventories() -> None:
    for scenario_id in (
        "stale-plan-vs-live-surface-conflict",
        "unresolved-source-precedence-stays-ambiguous",
        "plan-only-current-is-not-implementation-proof",
    ):
        source = load_gap_source(ROOT, scenario_id)
        runtime_home = source.get("runtime_home")
        assert isinstance(runtime_home, dict), f"{scenario_id}: runtime_home is missing"
        assert set(runtime_home) == {
            "root",
            "inventory_before",
            "inventory_after",
            "changed_paths",
            "housekeeping",
        }
        assert runtime_home["root"] == "temporary-home"
        assert isinstance(runtime_home["inventory_before"], list)
        assert isinstance(runtime_home["inventory_after"], list)
        assert isinstance(runtime_home["changed_paths"], list)
        housekeeping = runtime_home["housekeeping"]
        assert isinstance(housekeeping, dict)
        assert set(housekeeping) == {"classification", "out_of_scope", "paths"}
        assert housekeeping["classification"] == "consumer_runtime_housekeeping"
        assert housekeeping["out_of_scope"] is True
        assert isinstance(housekeeping["paths"], list)
        before = {item["path"]: item for item in runtime_home["inventory_before"]}
        after = {item["path"]: item for item in runtime_home["inventory_after"]}
        assert len(before) == len(runtime_home["inventory_before"])
        assert len(after) == len(runtime_home["inventory_after"])
        for inventory in (runtime_home["inventory_before"], runtime_home["inventory_after"]):
            for item in inventory:
                assert item["kind"] in {"directory", "regular"}
                if item["kind"] == "directory":
                    assert set(item) == {"path", "kind", "mode"}
                else:
                    assert set(item) == {"path", "kind", "mode", "size", "sha256"}
        calculated = sorted(
            path
            for path in set(before) | set(after)
            if before.get(path) != after.get(path)
        )
        assert calculated
        assert runtime_home["changed_paths"] == calculated
        assert housekeeping["paths"] == calculated

        write_boundary = source.get("write_boundary")
        assert isinstance(write_boundary, dict), f"{scenario_id}: write_boundary is missing"
        assert set(write_boundary) == {
            "product_surface_write_free",
            "product_surface_changed_paths",
            "runtime_home_housekeeping_only",
            "runtime_home_changed_paths",
        }
        assert isinstance(write_boundary["product_surface_write_free"], bool)
        assert write_boundary["product_surface_changed_paths"] == []
        assert write_boundary["runtime_home_changed_paths"] == calculated
        assert write_boundary["runtime_home_housekeeping_only"] is True

        session = source.get("session")
        assert isinstance(session, dict)
        assert session["write_free"] is False

        state_root = source.get("state_root")
        assert isinstance(state_root, dict)
        assert set(state_root) == {
            "requested",
            "observed_root",
            "honor_status",
            "observation_basis",
            "inventory_before",
            "inventory_after",
            "packet_paths_before",
            "packet_paths_after",
        }
        assert state_root["requested"] == "state-root"
        assert state_root["observed_root"] is None
        assert state_root["honor_status"] == "not_observable_no_writes"
        assert state_root["observation_basis"] == (
            "post-run inventory capture; no generated state marker or packet was produced by read-only /tk:gap"
        )
        assert state_root["inventory_before"] == []
        assert state_root["inventory_after"] == []
        assert isinstance(state_root["packet_paths_before"], list)
        assert isinstance(state_root["packet_paths_after"], list)
        assert state_root["packet_paths_before"] == []
        assert state_root["packet_paths_after"] == []

        product_surface = source.get("product_surface")
        assert isinstance(product_surface, dict)
        assert set(product_surface) == {
            "fixture_changed_paths",
            "plugin_changed_paths",
            "tigerkit_state_changed_paths",
            "gap_packet_paths_before",
            "gap_packet_paths_after",
            "gap_packet_changed_paths",
            "changed_paths",
        }
        assert product_surface["changed_paths"] == []
        assert product_surface["fixture_changed_paths"] == []
        assert product_surface["plugin_changed_paths"] == []
        assert product_surface["tigerkit_state_changed_paths"] == []
        assert product_surface["gap_packet_paths_before"] == []
        assert product_surface["gap_packet_paths_after"] == []
        assert product_surface["gap_packet_changed_paths"] == []

        canonical = source.get("canonical_tigerkit")
        assert isinstance(canonical, dict)
        assert canonical["root"] == "canonical-user-tigerkit"
        assert canonical["inventory_before"]
        assert canonical["inventory_after"]
        assert canonical["inventory_before"] == canonical["inventory_after"]
        assert canonical["unchanged"] is True
        assert source["write_boundary"]["product_surface_write_free"] is True


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
    test_gap_scenario3_prompt_is_neutral()
    test_gap_scenarios_record_complete_runtime_home_inventories()
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
