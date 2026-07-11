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
    record["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()


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


CASES: list[tuple[str, Mutation]] = [
    ("missing scenario", missing_scenario),
    ("duplicate scenario", duplicate_scenario),
    ("extra scenario", extra_scenario),
    ("forged source hash", forged_source_hash),
    ("forged assistant result hash", forged_result_hash),
    ("wrong reason", wrong_reason),
    ("eligible extra changed path", eligible_extra_changed_path),
    ("tracked target mutation", tracked_target_mutation),
    ("not-ignored target mutation", not_ignored_target_mutation),
    ("ignore mutation", ignore_mutation),
    ("second ignore mutation", ignore_second_mutation),
    ("symlink target mutation", symlink_target_mutation),
    ("symlink link mutation", symlink_link_mutation),
    ("honored/observed state-root mismatch", honored_observed_root_mismatch),
    ("inventory/observed state-root mismatch", inventory_observed_root_mismatch),
    ("non-git fallback write", non_git_fallback_write),
    ("reused session ID", reused_session_id),
    ("wrapper/consumer mismatch", wrapper_consumer_mismatch),
    ("modelUsage mismatch", model_usage_mismatch),
    ("plugin commit mismatch", plugin_commit_mismatch),
    ("plugin live blob mismatch", live_plugin_blob_mismatch),
    ("source traversal", source_path_traversal),
    ("source symlink substitution", source_symlink_substitution),
    ("source special entry", raw_special_entry),
]


def assert_controlled_rejection(name: str, completed: subprocess.CompletedProcess[str]) -> None:
    output = completed.stdout + completed.stderr
    assert completed.returncode != 0, f"{name}: mutation was accepted"
    assert "Traceback" not in output, f"{name}: validator raised an uncontrolled traceback: {output}"
    assert "full eval pilot check failed:" in output, output


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
        for name, mutate in CASES:
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
                assert_controlled_rejection(name, completed)
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
