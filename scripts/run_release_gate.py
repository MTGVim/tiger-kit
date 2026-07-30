#!/usr/bin/env python3
"""Run TigerKit's local release gate without GitHub Actions."""
from __future__ import annotations

import argparse
import copy
import json
import shlex
import subprocess
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
MANIFEST = ROOT / "evals" / "release-critical.json"


def run_checked(command: list[str], *, cwd: Path) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
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
    hosts = value.get("hosts")
    runs = value.get("runs")
    behavior = value.get("behavior_cases")
    routing = value.get("catalog_cases")
    if hosts != list(SUPPORTED_HOSTS):
        raise ValueError("release-critical hosts must exactly match supported hosts")
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 2:
        raise ValueError("release-critical runs must be an integer of at least two")
    if not isinstance(behavior, list) or not all(isinstance(v, str) and v for v in behavior):
        raise ValueError("release-critical behavior_cases must be a string list")
    if not isinstance(routing, list) or not all(isinstance(v, str) and v for v in routing):
        raise ValueError("release-critical catalog_cases must be a string list")
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
            row["hosts"] = list(SUPPORTED_HOSTS)
        if (
            row.get("type") == "git_commit_count_delta"
            and "expected" not in row
            and isinstance(row.get("count"), int)
        ):
            row["expected"] = row.pop("count")
        result.append(row)
    if not any(row.get("type") == "terminal_status" for row in result):
        raise ValueError(f"case {case.get('id')} needs a mechanical terminal assertion")
    return result


def behavior_case_map(
    contracts: Mapping[str, Mapping[str, object]],
) -> dict[str, tuple[str, Mapping[str, object]]]:
    result: dict[str, tuple[str, Mapping[str, object]]] = {}
    for skill, contract in contracts.items():
        behavior = contract["behavior"]["evals"]  # type: ignore[index]
        for case in behavior:
            result[f"{skill}:behavior:{case['id']}"] = (skill, case)
    return result


def catalog_case_map(
    contract: Mapping[str, object] | None,
) -> dict[str, Mapping[str, object]]:
    if not isinstance(contract, Mapping):
        return {}
    rows = contract.get("cases", [])
    if not isinstance(rows, list):
        return {}
    return {
        f"catalog:behavior:{row['id']}": row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }


def run_live_gate(
    candidate_root: Path,
    contracts: Mapping[str, Mapping[str, object]],
    catalog: Mapping[str, object] | None,
    *,
    adapter_command: str,
    manifest: Mapping[str, object],
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    records: list[dict[str, object]] = []
    failures: list[str] = []
    unavailable: list[str] = []
    behavior = behavior_case_map(contracts)
    routing = catalog_case_map(catalog)
    runs = int(manifest["runs"])

    for host in SUPPORTED_HOSTS:
        for case_id in manifest["behavior_cases"]:  # type: ignore[index]
            item = behavior.get(str(case_id))
            if item is None:
                failures.append(f"missing release behavior case: {case_id}")
                continue
            skill, case = item
            assertions = normalized_assertions(case)
            for run_number in range(1, runs + 1):
                try:
                    with isolated_checkout(candidate_root) as checkout:
                        initial_head = git_head(checkout)
                        adapter_result = run_adapter(
                            adapter_command,
                            checkout=checkout,
                            skill=skill,
                            prompt=str(case["prompt"]),
                            mode="behavior",
                            host=host,
                        )
                        assertion_results = grade_behavior(
                            "",
                            adapter_result,
                            assertions,
                            checkout=checkout,
                            initial_head=initial_head,
                            host=host,
                        )
                    passed = all(bool(row["passed"]) for row in assertion_results)
                except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                    unavailable.append(f"{host} {case_id}: {exc}")
                    records.append(
                        {
                            "host": host,
                            "case": case_id,
                            "run": run_number,
                            "passed": False,
                            "unavailable": str(exc),
                        }
                    )
                    continue
                records.append(
                    {
                        "host": host,
                        "case": case_id,
                        "run": run_number,
                        "passed": passed,
                        "terminal_status": adapter_result.get("terminal_status"),
                        "events": adapter_result.get("events"),
                        "assertions": assertion_results,
                    }
                )
                if not passed:
                    failures.append(f"{host} {case_id} run {run_number} failed")

        for case_id in manifest["catalog_cases"]:  # type: ignore[index]
            case = routing.get(str(case_id))
            if case is None:
                failures.append(f"missing release catalog case: {case_id}")
                continue
            for run_number in range(1, runs + 1):
                try:
                    with isolated_checkout(candidate_root) as checkout:
                        adapter_result = run_adapter(
                            adapter_command,
                            checkout=checkout,
                            skill=str(case["focus_skill"]),
                            prompt=str(case["prompt"]),
                            mode="catalog-routing",
                            host=host,
                        )
                    expected = case.get("expected_selected_skill")
                    loaded = adapter_result.get("loaded_skills")
                    passed = (
                        adapter_result.get("selected_skill") == expected
                        and (
                            expected is None
                            or isinstance(loaded, list)
                            and expected in loaded
                        )
                    )
                except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                    unavailable.append(f"{host} {case_id}: {exc}")
                    records.append(
                        {
                            "host": host,
                            "case": case_id,
                            "run": run_number,
                            "passed": False,
                            "unavailable": str(exc),
                        }
                    )
                    continue
                records.append(
                    {
                        "host": host,
                        "case": case_id,
                        "run": run_number,
                        "passed": passed,
                        "expected_selected_skill": expected,
                        "actual_selected_skill": adapter_result.get("selected_skill"),
                        "loaded_skills": loaded,
                    }
                )
                if not passed:
                    failures.append(f"{host} {case_id} run {run_number} failed")

    return records, sorted(set(failures)), sorted(set(unavailable))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--adapter-command", required=True)
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

    with detached_worktree(args.baseline) as baseline_root, detached_worktree(
        args.candidate
    ) as candidate_root:
        baseline_contracts = load_eval_contracts(baseline_root, None)
        candidate_contracts = load_eval_contracts(candidate_root, None)
        baseline_catalog = load_catalog_contract(baseline_root)
        candidate_catalog = load_catalog_contract(candidate_root)
        contract_errors.extend(compare_eval_contracts(baseline_contracts, candidate_contracts))
        contract_errors.extend(compare_catalog_contracts(baseline_catalog, candidate_catalog))

        commands = [
            ["python3", "scripts/validate_skills.py"],
            ["python3", "scripts/validate_skills.py", "--links-only"],
            ["python3", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
            ["python3", "scripts/sync_eval_compat.py"],
            ["git", "diff", "--exit-code"],
            ["npx", "--yes", "skills@1.5.9", "add", ".", "--list"],
            ["npx", "--yes", "skills", "add", ".", "--list"],
            ["git", "diff", "--check"],
        ]
        for command in commands:
            static_records.append(run_checked(command, cwd=candidate_root))

        live_records, live_failures, unavailable = run_live_gate(
            candidate_root,
            candidate_contracts,
            candidate_catalog,
            adapter_command=args.adapter_command,
            manifest=manifest,
        )

    static_failures = [
        str(row["command"]) for row in static_records if not bool(row["passed"])
    ]
    reasons = sorted(set(contract_errors + static_failures + live_failures))
    status = "Fail" if reasons else "Unverifiable" if unavailable else "Pass"
    result = {
        "status": status,
        "baseline": baseline_sha,
        "candidate": candidate_sha,
        "manifest": manifest,
        "contract_errors": contract_errors,
        "static": static_records,
        "live": live_records,
        "reasons": reasons,
        "unavailable": unavailable,
    }
    (output / "release-gate.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "Pass" else 1 if status == "Fail" else 2


if __name__ == "__main__":
    raise SystemExit(main())
