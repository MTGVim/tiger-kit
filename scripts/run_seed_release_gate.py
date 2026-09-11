#!/usr/bin/env python3
"""Seed-first TigerKit release gate.

기존 결정론적 release gate의 정적 검사와 language/ledger/package 검사를 재사용하면서,
모든 활성 skill의 baseline 계약 보존을 검증한다. 과거의 포괄적 교체 예외는 허용하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

if __package__:
    from . import run_release_gate as base
    from .check_runtime_guard import validate_runtime_guard
    from .run_skill_evals import (
        compare_catalog_contracts,
        compare_eval_contracts,
        detached_worktree,
        load_catalog_contract,
        load_eval_contracts,
        load_retired_catalog_cases,
        load_retired_skill_contracts,
        resolve_ref,
    )
    from .validate_skills import validate_portable_artifacts
else:
    import run_release_gate as base
    from check_runtime_guard import validate_runtime_guard
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
    from validate_skills import validate_portable_artifacts

ROOT = Path(__file__).resolve().parents[1]


def preservation_errors(
    baseline: dict[str, dict[str, object]],
    candidate: dict[str, dict[str, object]],
    manifest: dict[str, object],
    retired_skills: set[str],
) -> list[str]:
    """Preserve every active contract; historical blanket exemptions never apply."""
    errors: list[str] = []
    if manifest.get("replaced_skill_eval_contracts"):
        errors.append("replaced_skill_eval_contracts is unsupported: use case migrations, not skill-wide exemptions")
    if manifest.get("replace_catalog_contract"):
        errors.append("replace_catalog_contract is unsupported: preserve or explicitly migrate cases")
    errors.extend(compare_eval_contracts(baseline, candidate, retired_skills=retired_skills))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base.ensure_clean_worktree()
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("--output must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)

    baseline_sha = resolve_ref(args.baseline)
    candidate_sha = resolve_ref(args.candidate)

    # 기존 gate를 candidate self-check 모드로 실행해 language, ledger, portable,
    # unittest, package smoke와 diff 검사를 그대로 보존한다.
    self_output = output / "self-check"
    completed = subprocess.run(
        [
            "python3",
            "scripts/run_release_gate.py",
            "--baseline",
            args.candidate,
            "--candidate",
            args.candidate,
            "--output",
            str(self_output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    self_result_path = self_output / "release-gate.json"
    if self_result_path.is_file():
        self_result = json.loads(self_result_path.read_text(encoding="utf-8"))
    else:
        self_result = {
            "status": "Fail",
            "blocking_reasons": [
                "candidate self-check did not produce release-gate.json",
                completed.stderr[-1000:],
            ],
        }

    contract_errors: list[str] = []
    with detached_worktree(args.baseline) as baseline_root, detached_worktree(args.candidate) as candidate_root:
        baseline_contracts = load_eval_contracts(
            baseline_root, None, allow_legacy_skill_local=True
        )
        candidate_contracts = load_eval_contracts(candidate_root, None)
        manifest = json.loads((candidate_root / "evals/release-critical.json").read_text(encoding="utf-8"))

        candidate_catalog = load_catalog_contract(candidate_root)
        baseline_catalog = load_catalog_contract(baseline_root)

        contract_errors.extend(preservation_errors(
            baseline_contracts, candidate_contracts, manifest,
            load_retired_skill_contracts(candidate_root),
        ))
        contract_errors.extend(compare_catalog_contracts(
            baseline_catalog, candidate_catalog,
            retired_cases=load_retired_catalog_cases(candidate_root),
        ))

        contract_errors.extend(
            base.validate_manifest_cases(candidate_contracts, candidate_catalog, manifest)
        )
        contract_errors.extend(
            base.compare_language_regression(
                base.scan_language(baseline_root),
                base.scan_language(candidate_root),
            )
        )
        ledger_errors, _ = base.validate_ledger_eval_coverage(candidate_contracts)
        contract_errors.extend(ledger_errors)
        contract_errors.extend(validate_portable_artifacts(candidate_root))
        contract_errors.extend(validate_runtime_guard(candidate_root))

    self_blockers = [
        str(value)
        for value in self_result.get("blocking_reasons", [])
        if str(value)
    ]
    blockers = sorted(set(self_blockers + contract_errors))

    result = {
        "status": "Fail" if blockers else "Pass",
        "release_blocked": bool(blockers),
        "baseline": baseline_sha,
        "candidate": candidate_sha,
        "contract_preservation": "all active skills and catalog cases",
        "self_check": self_result,
        "contract_errors": contract_errors,
        "blocking_reasons": blockers,
    }

    (output / "release-gate.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
