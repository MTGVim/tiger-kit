#!/usr/bin/env python3
"""Run TigerKit's deterministic release gate."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Mapping

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

from run_skill_evals import (
    compare_catalog_contracts,
    compare_eval_contracts,
    detached_worktree,
    load_catalog_contract,
    load_eval_contracts,
    load_retired_catalog_cases,
    load_retired_skill_contracts,
    resolve_ref,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evals/release-critical.json"


def run_checked(command: list[str], *, cwd: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
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


def ensure_clean_worktree(root: Path = ROOT) -> None:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    if completed.stdout.strip():
        raise ValueError("release gate requires a clean worktree; commit candidate changes first")


def load_manifest() -> dict[str, object]:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("release-critical manifest must be an object")
    for field in ("behavior_cases", "catalog_cases"):
        rows = value.get(field)
        if not isinstance(rows, list) or not rows or not all(isinstance(row, str) and row for row in rows):
            raise ValueError(f"release-critical {field} must be a non-empty string list")
    if value.get("progress_contract") != {"version": 1, "scope": "all-tk-skills"}:
        raise ValueError("release-critical progress_contract must cover all tk-* skills at version 1")
    retired = value.get("retired_skill_contracts", [])
    if not isinstance(retired, list) or not all(isinstance(row, str) and row for row in retired):
        raise ValueError("release-critical retired_skill_contracts must be a string list")
    retired_catalog = value.get("retired_catalog_cases", [])
    if not isinstance(retired_catalog, list) or not all(isinstance(row, str) and row for row in retired_catalog):
        raise ValueError("release-critical retired_catalog_cases must be a string list")
    return value


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_clean_worktree()
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("--output must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    baseline_sha = resolve_ref(args.baseline)
    candidate_sha = resolve_ref(args.candidate)
    static_records: list[dict[str, object]] = []
    contract_errors: list[str] = []
    with detached_worktree(args.baseline) as baseline_root, detached_worktree(args.candidate) as candidate_root:
        baseline_contracts = load_eval_contracts(baseline_root, None)
        candidate_contracts = load_eval_contracts(candidate_root, None)
        baseline_catalog = load_catalog_contract(baseline_root)
        candidate_catalog = load_catalog_contract(candidate_root)
        contract_errors.extend(
            compare_eval_contracts(
                baseline_contracts,
                candidate_contracts,
                retired_skills=load_retired_skill_contracts(candidate_root),
            )
        )
        contract_errors.extend(
            compare_catalog_contracts(
                baseline_catalog,
                candidate_catalog,
                retired_cases=load_retired_catalog_cases(candidate_root),
            )
        )
        contract_errors.extend(validate_manifest_cases(candidate_contracts, candidate_catalog, manifest))
        commands = [
            ["python3", "scripts/validate_skills.py"],
            ["python3", "scripts/validate_skills.py", "--links-only"],
            ["python3", "-B", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
            ["python3", "scripts/audit_catalog.py", "--check"],
            ["python3", "scripts/validate_progress_contract.py"],
            ["git", "diff", "--exit-code"],
            ["npx", "--yes", "skills@1.5.9", "add", ".", "--list"],
            ["npx", "--yes", "skills", "add", ".", "--list"],
            ["git", "diff", "--check"],
        ]
        for command in commands:
            static_records.append(run_checked(command, cwd=candidate_root))
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
    }
    (output / "release-gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if blocking_reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
