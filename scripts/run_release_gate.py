#!/usr/bin/env python3
"""Run TigerKit's deterministic release gate and advisory live quality canary."""
from __future__ import annotations

import argparse
import copy
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Mapping

from run_skill_evals import (
    SUPPORTED_HOSTS,
    compare_catalog_contracts,
    compare_eval_contracts,
    detached_worktree,
    git_head,
    grade_behavior,
    isolated_checkout,
    load_catalog_contract,
    load_eval_contracts,
    resolve_ref,
    run_adapter,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evals/release-critical.json"
BUILTIN_ADAPTER = ROOT / "scripts/adapters/tigerkit_host_adapter.py"
HOST_ORDER = ("codex", "claude-code", "hermes-agent")


def run_checked(command: list[str], *, cwd: Path) -> dict[str, object]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return {
        "command": shlex.join(command),
        "passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }


def load_manifest() -> dict[str, object]:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("release-critical manifest must be an object")
    if value.get("hosts") != list(HOST_ORDER):
        raise ValueError("release-critical hosts must be ordered codex, claude-code, hermes-agent")
    if not set(HOST_ORDER).issubset(set(SUPPORTED_HOSTS)):
        raise ValueError("release-critical host order contains an unsupported host")
    runs = value.get("runs")
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 2:
        raise ValueError("release-critical runs must be an integer of at least two")
    for field in ("behavior_cases", "catalog_cases"):
        rows = value.get(field)
        if not isinstance(rows, list) or not rows or not all(isinstance(row, str) and row for row in rows):
            raise ValueError(f"release-critical {field} must be a non-empty string list")
    return value


def normalized_assertions(case: Mapping[str, object]) -> list[dict[str, object]]:
    rows = case.get("assertions", [])
    if not isinstance(rows, list):
        raise ValueError(f"case {case.get('id')} assertions must be a list")
    result: list[dict[str, object]] = []
    for raw in rows:
        if not isinstance(raw, dict) or raw.get("type") == "judge":
            continue
        row = copy.deepcopy(raw)
        if row.get("type") in {"event_order", "event_absent", "event_count"}:
            row["hosts"] = list(HOST_ORDER)
        if row.get("type") == "git_commit_count_delta" and "expected" not in row and isinstance(row.get("count"), int):
            row["expected"] = row.pop("count")
        result.append(row)
    if not any(row.get("type") == "terminal_status" for row in result):
        raise ValueError(f"case {case.get('id')} needs a mechanical terminal assertion")
    return result


def behavior_case_map(contracts: Mapping[str, Mapping[str, object]]) -> dict[str, tuple[str, Mapping[str, object]]]:
    result: dict[str, tuple[str, Mapping[str, object]]] = {}
    for skill, contract in contracts.items():
        rows = contract["behavior"]["evals"]  # type: ignore[index]
        for case in rows:
            result[f"{skill}:behavior:{case['id']}"] = (skill, case)
    return result


def catalog_case_map(contract: Mapping[str, object] | None) -> dict[str, Mapping[str, object]]:
    if not isinstance(contract, Mapping):
        return {}
    rows = contract.get("cases", [])
    if not isinstance(rows, list):
        return {}
    return {f"catalog:behavior:{row['id']}": row for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)}


def validate_manifest_cases(
    contracts: Mapping[str, Mapping[str, object]],
    catalog: Mapping[str, object] | None,
    manifest: Mapping[str, object],
) -> list[str]:
    behavior = behavior_case_map(contracts)
    routing = catalog_case_map(catalog)
    errors = [f"missing release behavior case: {case_id}" for case_id in manifest["behavior_cases"] if str(case_id) not in behavior]  # type: ignore[index]
    errors.extend(f"missing release catalog case: {case_id}" for case_id in manifest["catalog_cases"] if str(case_id) not in routing)  # type: ignore[index]
    return errors


def run_one_host(
    host: str,
    candidate_root: Path,
    contracts: Mapping[str, Mapping[str, object]],
    catalog: Mapping[str, object] | None,
    *,
    adapter_command: str,
    manifest: Mapping[str, object],
) -> tuple[list[dict[str, object]], list[str], str | None]:
    records: list[dict[str, object]] = []
    failures: list[str] = []
    behavior = behavior_case_map(contracts)
    routing = catalog_case_map(catalog)
    runs = int(manifest["runs"])
    for case_id in manifest["behavior_cases"]:  # type: ignore[index]
        skill, case = behavior[str(case_id)]
        assertions = normalized_assertions(case)
        for run_number in range(1, runs + 1):
            try:
                with isolated_checkout(candidate_root) as checkout:
                    initial_head = git_head(checkout)
                    adapter_result = run_adapter(adapter_command, checkout=checkout, skill=skill, prompt=str(case["prompt"]), mode="behavior", host=host)
                    assertion_results = grade_behavior("", adapter_result, assertions, checkout=checkout, initial_head=initial_head, host=host)
            except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                records.append({"host": host, "case": case_id, "run": run_number, "passed": False, "unavailable": str(exc)})
                return records, failures, str(exc)
            passed = all(bool(row["passed"]) for row in assertion_results)
            records.append({"host": host, "case": case_id, "run": run_number, "passed": passed, "terminal_status": adapter_result.get("terminal_status"), "events": adapter_result.get("events"), "assertions": assertion_results})
            if not passed:
                failures.append(f"{host} {case_id} run {run_number} failed")
    for case_id in manifest["catalog_cases"]:  # type: ignore[index]
        case = routing[str(case_id)]
        for run_number in range(1, runs + 1):
            try:
                with isolated_checkout(candidate_root) as checkout:
                    adapter_result = run_adapter(adapter_command, checkout=checkout, skill=str(case["focus_skill"]), prompt=str(case["prompt"]), mode="catalog-routing", host=host)
            except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                records.append({"host": host, "case": case_id, "run": run_number, "passed": False, "unavailable": str(exc)})
                return records, failures, str(exc)
            expected = case.get("expected_selected_skill")
            loaded = adapter_result.get("loaded_skills")
            passed = adapter_result.get("selected_skill") == expected and (expected is None or isinstance(loaded, list) and expected in loaded)
            records.append({"host": host, "case": case_id, "run": run_number, "passed": passed, "expected_selected_skill": expected, "actual_selected_skill": adapter_result.get("selected_skill"), "loaded_skills": loaded})
            if not passed:
                failures.append(f"{host} {case_id} run {run_number} failed")
    return records, sorted(set(failures)), None


def run_live_gate(
    candidate_root: Path,
    contracts: Mapping[str, Mapping[str, object]],
    catalog: Mapping[str, object] | None,
    *,
    adapter_command: str,
    manifest: Mapping[str, object],
) -> tuple[list[dict[str, object]], list[dict[str, object]], str | None]:
    records: list[dict[str, object]] = []
    host_results: list[dict[str, object]] = []
    selected_host: str | None = None
    for index, host in enumerate(HOST_ORDER):
        host_records, failures, unavailable = run_one_host(host, candidate_root, contracts, catalog, adapter_command=adapter_command, manifest=manifest)
        records.extend(host_records)
        if unavailable is not None:
            host_results.append({"host": host, "status": "unavailable", "reason": unavailable})
            continue
        if failures:
            host_results.append({"host": host, "status": "failed", "failures": failures})
            continue
        selected_host = host
        host_results.append({"host": host, "status": "passed"})
        for remaining in HOST_ORDER[index + 1:]:
            host_results.append({"host": remaining, "status": "not-run", "reason": f"{host} already passed"})
        break
    return records, host_results, selected_host


def default_adapter_command() -> str:
    return f"{shlex.quote(sys.executable)} {shlex.quote(str(BUILTIN_ADAPTER))}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--adapter-command", help="override the built-in ordered host adapter")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("--output must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    baseline_sha = resolve_ref(args.baseline)
    candidate_sha = resolve_ref(args.candidate)
    static_records: list[dict[str, object]] = []
    contract_errors: list[str] = []
    adapter_command = args.adapter_command or default_adapter_command()
    with detached_worktree(args.baseline) as baseline_root, detached_worktree(args.candidate) as candidate_root:
        baseline_contracts = load_eval_contracts(baseline_root, None)
        candidate_contracts = load_eval_contracts(candidate_root, None)
        baseline_catalog = load_catalog_contract(baseline_root)
        candidate_catalog = load_catalog_contract(candidate_root)
        contract_errors.extend(compare_eval_contracts(baseline_contracts, candidate_contracts))
        contract_errors.extend(compare_catalog_contracts(baseline_catalog, candidate_catalog))
        contract_errors.extend(validate_manifest_cases(candidate_contracts, candidate_catalog, manifest))
        commands = [
            ["python3", "scripts/validate_skills.py"],
            ["python3", "scripts/validate_skills.py", "--links-only"],
            ["python3", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
            ["python3", "scripts/audit_catalog.py", "--check"],
            ["git", "diff", "--exit-code"],
            ["npx", "--yes", "skills@1.5.9", "add", ".", "--list"],
            ["npx", "--yes", "skills", "add", ".", "--list"],
            ["git", "diff", "--check"],
        ]
        for command in commands:
            static_records.append(run_checked(command, cwd=candidate_root))
        live_records, host_results, selected_host = run_live_gate(candidate_root, candidate_contracts, candidate_catalog, adapter_command=adapter_command, manifest=manifest)
    static_failures = [str(row["command"]) for row in static_records if not bool(row["passed"])]
    blocking_reasons = sorted(set(contract_errors + static_failures))
    result = {
        "status": "Fail" if blocking_reasons else "Pass",
        "release_blocked": bool(blocking_reasons),
        "baseline": baseline_sha,
        "candidate": candidate_sha,
        "manifest": manifest,
        "contract_errors": contract_errors,
        "static": static_records,
        "blocking_reasons": blocking_reasons,
        "quality": {
            "status": "Pass" if selected_host else "Advisory",
            "adapter": "override" if args.adapter_command else "built-in",
            "host_order": list(HOST_ORDER),
            "selected_host": selected_host,
            "hosts": host_results,
            "records": live_records,
        },
    }
    (output / "release-gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if blocking_reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
