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

Mutation = Callable[[dict[str, Any], Path], None]


class UnsupportedCase(Exception):
    """A platform does not support a requested filesystem adversarial case."""


def load_result(checkout: Path) -> dict[str, Any]:
    return json.loads((checkout / FULL_RESULT).read_text(encoding="utf-8"))


def write_result(checkout: Path, result: dict[str, Any]) -> None:
    (checkout / FULL_RESULT).write_text(
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


def raw_special_entry(_result: dict[str, Any], checkout: Path) -> None:
    fifo_path = checkout / FULL_RAW_DIR / "unexpected.fifo"
    try:
        os.mkfifo(fifo_path)
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

        relocated = prepare_checkout(temp_root / "relocated-valid")
        completed = run_validator(relocated)
        if completed.returncode != 0:
            failures.append(
                "relocated checkout: valid artifact was rejected: "
                + (completed.stderr or completed.stdout).strip()
            )
        else:
            print("accepts relocated valid checkout")

        missing = prepare_checkout(temp_root / "missing-result")
        (missing / FULL_RESULT).unlink()
        completed = run_validator(missing)
        if completed.returncode == 0:
            failures.append("missing FULL result: mutation was accepted")
        else:
            print("rejects missing FULL result: exit=1")

    if failures:
        print("full validator adversarial tests failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"full validator adversarial tests ok: {len(CASES) - skipped} rejection cases"
        f" + relocation + missing result ({skipped} skipped)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
