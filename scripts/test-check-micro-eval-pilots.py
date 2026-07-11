#!/usr/bin/env python3
"""Adversarial regression tests for the MICRO evidence validator."""
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
VALIDATOR = ROOT / "scripts" / "check-micro-eval-pilots.py"
RESULT_RELATIVE = Path("evals/results/micro-initial-command-wording.json")

Mutation = Callable[[dict[str, Any], Path], None]


class UnsupportedCase(Exception):
    """A platform does not support a requested filesystem adversarial case."""


def load_result(checkout: Path) -> dict[str, Any]:
    return json.loads((checkout / RESULT_RELATIVE).read_text(encoding="utf-8"))


def write_result(checkout: Path, result: dict[str, Any]) -> None:
    (checkout / RESULT_RELATIVE).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def rewrite_source(
    checkout: Path,
    result: dict[str, Any],
    record_index: int,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    record = result["records"][record_index]
    source_path = checkout / Path(record["source_path"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    mutate(source)
    source_path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result["records"][record_index]["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()


def update_eval_request_metadata(
    result: dict[str, Any],
    source: dict[str, Any],
    record_index: int,
) -> None:
    request_sha = hashlib.sha256(source["eval_user_request"].encode("utf-8")).hexdigest()
    source["eval_user_request_sha256"] = request_sha
    result["records"][record_index]["eval_user_request_sha256"] = request_sha


def swap_directory_for_symlink(path: Path) -> None:
    real_path = path.with_name(path.name + "-real")
    path.rename(real_path)
    path.symlink_to(real_path.name, target_is_directory=True)


def prepare_checkout(temp_root: Path) -> Path:
    checkout = temp_root / "relocated-tiger-kit"
    shutil.copytree(ROOT, checkout, symlinks=True)
    result = load_result(checkout)
    checkout_metadata = result.get("checkout")
    if isinstance(checkout_metadata, dict) and isinstance(checkout_metadata.get("root"), str) and Path(checkout_metadata["root"]).is_absolute():
        checkout_metadata["root"] = str(checkout)
    invocation = result.get("invocation")
    if isinstance(invocation, dict) and isinstance(invocation.get("working_directory"), str) and Path(invocation["working_directory"]).is_absolute():
        invocation["working_directory"] = str(checkout)
    write_result(checkout, result)
    return checkout


def run_validator(checkout: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(checkout / "scripts" / "check-micro-eval-pilots.py")],
        cwd=checkout,
        capture_output=True,
        text=True,
        check=False,
    )


def forged_output_hash(result: dict[str, Any], _checkout: Path) -> None:
    result["records"][0]["output_sha256"] = "a" * 64


def forged_output_length(result: dict[str, Any], _checkout: Path) -> None:
    result["records"][0]["output_byte_length"] += 1


def fabricated_prompt(result: dict[str, Any], _checkout: Path) -> None:
    result["records"][0]["declared_prompt"] = "fabricated prompt"


def reused_session_id(result: dict[str, Any], _checkout: Path) -> None:
    result["records"][1]["session_id"] = result["records"][0]["session_id"]


def pilot_result_decision_mismatch(result: dict[str, Any], _checkout: Path) -> None:
    result["surface_results"][0]["decision"]["rationale"] = "mismatched decision rationale"


def runtime_model_divergence(result: dict[str, Any], _checkout: Path) -> None:
    result["runtime"]["model"] = "other-model"
    result["invocation"]["model"] = "other-model"


def root_host_path(result: dict[str, Any], _checkout: Path) -> None:
    result["runtime"]["agent_version"] = "/root/private"


def windows_user_host_path(result: dict[str, Any], _checkout: Path) -> None:
    result["runtime"]["agent_version"] = r"D:\Users\name\private"


def unhashable_pilot_surface(_result: dict[str, Any], checkout: Path) -> None:
    pilot_path = checkout / "evals" / "micro-pilots" / "initial-command-wording.json"
    pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
    pilot["surfaces"][0]["surface"] = {"not": "a string"}
    pilot_path.write_text(json.dumps(pilot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unpaired_tie_extra(result: dict[str, Any], _checkout: Path) -> None:
    extra = copy.deepcopy(result["records"][0])
    extra["sample_index"] = 2
    extra["session_id"] = "20260711_150000_abcdef"
    extra["observation"]["tied"] = True
    source_path = _checkout / "evals" / "results" / "raw" / "micro-initial-command-wording" / "route-a-minimal.json"
    extra_source_path = source_path.with_name("route-a-minimal-sample-2.json")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["session_id"] = extra["session_id"]
    extra_source_path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    extra["source_path"] = "evals/results/raw/micro-initial-command-wording/route-a-minimal-sample-2.json"
    extra["source_sha256"] = hashlib.sha256(extra_source_path.read_bytes()).hexdigest()
    result["records"].append(extra)


def recorded_commit_blob_mismatch(result: dict[str, Any], checkout: Path) -> None:
    result["checkout"]["git_commit"] = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def no_git_archive(_result: dict[str, Any], checkout: Path) -> None:
    shutil.rmtree(checkout / ".git")


def source_path_traversal(result: dict[str, Any], _checkout: Path) -> None:
    result["records"][0]["source_path"] = "../micro-pilots/initial-command-wording.json"


def forged_durable_source(_result: dict[str, Any], checkout: Path) -> None:
    source_path = checkout / "evals" / "results" / "raw" / "micro-initial-command-wording" / "route-a-minimal.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["assistant_response"] = "forged durable output\n"
    source_path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_symlink_substitution(_result: dict[str, Any], checkout: Path) -> None:
    source_path = checkout / "evals" / "results" / "raw" / "micro-initial-command-wording" / "route-a-minimal.json"
    source_path.unlink()
    source_path.symlink_to("route-b-explicit.json")


def skill_symlink_substitution(result: dict[str, Any], checkout: Path) -> None:
    route_skill = checkout / "skills" / "route" / "SKILL.md"
    reflect_skill = checkout / "skills" / "reflect" / "SKILL.md"
    route_skill.unlink()
    route_skill.symlink_to("../reflect/SKILL.md")
    result["checkout"]["canonical_skills"]["/tk:route"]["sha256"] = hashlib.sha256(
        reflect_skill.read_bytes()
    ).hexdigest()


def live_skill_regular_file_substitution(_result: dict[str, Any], checkout: Path) -> None:
    route_skill = checkout / "skills" / "route" / "SKILL.md"
    route_skill.write_bytes(route_skill.read_bytes() + b"\nundeclared live skill substitution\n")


def extra_eval_request_with_recomputed_hashes(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["eval_user_request"] += " Undeclared instruction: ignore the canonical request."
        update_eval_request_metadata(result, source, 0)

    rewrite_source(checkout, result, 0, mutate)


def altered_eval_request_with_recomputed_hashes(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["eval_user_request"] = source["eval_user_request"].replace("repo-root", "alternate-root")
        update_eval_request_metadata(result, source, 0)

    rewrite_source(checkout, result, 0, mutate)


def reordered_eval_request_with_recomputed_hashes(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        request = source["eval_user_request"]
        first = "Do not write, modify, or create files."
        second = "Treat this declared variant prompt as the user request:"
        first_index = request.index(first)
        second_index = request.index(second)
        second_end = request.index(".", second_index) + 1
        reordered = (
            request[:first_index]
            + request[second_index:second_end]
            + " "
            + first
            + request[second_end:]
        )
        source["eval_user_request"] = reordered
        update_eval_request_metadata(result, source, 0)

    rewrite_source(checkout, result, 0, mutate)


def observed_tools_missing_canonical_read(result: dict[str, Any], checkout: Path) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["tool_evidence"]["observed_tools"] = ["skill_view"]

    rewrite_source(checkout, result, 1, mutate)


def pilot_directory_symlink(_result: dict[str, Any], checkout: Path) -> None:
    swap_directory_for_symlink(checkout / "evals" / "micro-pilots")


def results_directory_symlink(_result: dict[str, Any], checkout: Path) -> None:
    swap_directory_for_symlink(checkout / "evals" / "results")


def results_raw_directory_symlink(_result: dict[str, Any], checkout: Path) -> None:
    swap_directory_for_symlink(checkout / "evals" / "results" / "raw")


def raw_directory_symlink(_result: dict[str, Any], checkout: Path) -> None:
    swap_directory_for_symlink(
        checkout / "evals" / "results" / "raw" / "micro-initial-command-wording"
    )


def raw_fifo_special_entry(_result: dict[str, Any], checkout: Path) -> None:
    fifo_path = checkout / "evals" / "results" / "raw" / "micro-initial-command-wording" / "unexpected.fifo"
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
    ("forged output hash", forged_output_hash),
    ("forged output length", forged_output_length),
    ("fabricated prompt", fabricated_prompt),
    ("reused session ID", reused_session_id),
    ("pilot/result decision mismatch", pilot_result_decision_mismatch),
    ("runtime model divergence", runtime_model_divergence),
    ("root host path", root_host_path),
    ("Windows user host path", windows_user_host_path),
    ("unhashable pilot surface", unhashable_pilot_surface),
    ("unpaired tie extra", unpaired_tie_extra),
    ("recorded commit/blob mismatch", recorded_commit_blob_mismatch),
    ("no-git archive", no_git_archive),
    ("source path traversal", source_path_traversal),
    ("forged durable source", forged_durable_source),
    ("durable source symlink substitution", source_symlink_substitution),
    ("canonical skill symlink substitution", skill_symlink_substitution),
    ("live skill regular-file substitution", live_skill_regular_file_substitution),
    ("extra eval request with recomputed hashes", extra_eval_request_with_recomputed_hashes),
    ("altered eval request with recomputed hashes", altered_eval_request_with_recomputed_hashes),
    ("reordered eval request with recomputed hashes", reordered_eval_request_with_recomputed_hashes),
    ("observed tools missing canonical read", observed_tools_missing_canonical_read),
    ("pilot directory symlink", pilot_directory_symlink),
    ("results directory symlink", results_directory_symlink),
    ("results raw directory symlink", results_raw_directory_symlink),
    ("raw directory symlink", raw_directory_symlink),
    ("raw FIFO special entry", raw_fifo_special_entry),
]


def workflow_has_full_history_checkout() -> bool:
    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    try:
        lines = workflow.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return False

    checkout_indices = [
        index
        for index, line in enumerate(lines)
        if line.strip().startswith("uses: actions/checkout@")
    ]
    if len(checkout_indices) != 1:
        return False

    uses_index = checkout_indices[0]
    uses_indent = len(lines[uses_index]) - len(lines[uses_index].lstrip())
    step_indent = uses_indent
    for index in range(uses_index - 1, -1, -1):
        line = lines[index]
        if line.strip() and not line.lstrip().startswith("#"):
            indent = len(line) - len(line.lstrip())
            if indent < uses_indent and line.lstrip().startswith("-"):
                step_indent = indent
                break
    step_end = len(lines)
    for index in range(uses_index + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line.lstrip().startswith("#"):
            indent = len(line) - len(line.lstrip())
            if indent <= step_indent:
                step_end = index
                break

    with_index = None
    with_indent = None
    for index in range(uses_index + 1, step_end):
        line = lines[index]
        if line.strip() == "with:":
            with_index = index
            with_indent = len(line) - len(line.lstrip())
            break
    if with_index is None or with_indent is None:
        return False

    with_end = step_end
    for index in range(with_index + 1, step_end):
        line = lines[index]
        if line.strip() and not line.lstrip().startswith("#"):
            indent = len(line) - len(line.lstrip())
            if indent <= with_indent:
                with_end = index
                break

    for line in lines[with_index + 1 : with_end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, separator, value = stripped.partition(":")
        if key == "fetch-depth" and separator and value.split("#", 1)[0].strip().strip("'\"") == "0":
            return True
    return False


def main() -> int:
    failures: list[str] = []
    skipped = 0
    if workflow_has_full_history_checkout():
        print("requires full CI checkout history")
    else:
        failures.append("CI workflow checkout must configure fetch-depth: 0 for the MICRO validator")
    with tempfile.TemporaryDirectory(prefix="tiger-kit-micro-validator-") as temp_dir:
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
            if completed.returncode == 0:
                failures.append(f"{name}: mutation was accepted")
            else:
                if name == "unhashable pilot surface":
                    output = completed.stdout + completed.stderr
                    if "Traceback" in output or "micro eval pilot check failed:" not in output:
                        failures.append(
                            f"{name}: rejection was not reported as a controlled validator failure"
                        )
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

    if failures:
        print("micro validator adversarial tests failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"micro validator adversarial tests ok: {len(CASES) - skipped} rejection cases"
        f" + relocation ({skipped} skipped)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
