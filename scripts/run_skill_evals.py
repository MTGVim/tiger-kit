#!/usr/bin/env python3
"""Run TigerKit skill evals against a baseline and candidate in clean contexts."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Mapping


ROOT = Path(__file__).resolve().parents[1]
TOKEN_REGRESSION_RATIO = 1.25
DURATION_REGRESSION_RATIO = 1.50


def validate_adapter_result(result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if not isinstance(result.get("skill_loaded"), bool):
        errors.append("adapter result requires boolean skill_loaded")
    if not isinstance(result.get("output"), str):
        errors.append("adapter result requires string output")
    for field in ("total_tokens", "duration_ms"):
        value = result.get(field)
        if value is not None and not isinstance(value, (int, float)):
            errors.append(f"adapter result {field} must be numeric or null")
    terminal_status = result.get("terminal_status")
    if not isinstance(terminal_status, str) or not terminal_status.strip():
        errors.append("adapter result requires non-empty string terminal_status")
    return errors


def build_verdict(
    baseline: dict[str, object],
    candidate: dict[str, object],
    *,
    resource_regression_reason: str | None = None,
) -> dict[str, object]:
    reasons: list[str] = []
    unverifiable: list[str] = []
    if int(candidate.get("safety_failures", 0)) > 0:
        reasons.append("candidate has safety assertion failures")
    baseline_trigger_metrics = baseline.get("trigger_metrics")
    candidate_trigger_metrics = candidate.get("trigger_metrics")
    if isinstance(baseline_trigger_metrics, dict) and isinstance(candidate_trigger_metrics, dict):
        for kind in sorted(set(baseline_trigger_metrics) | set(candidate_trigger_metrics)):
            baseline_kind = baseline_trigger_metrics.get(kind)
            candidate_kind = candidate_trigger_metrics.get(kind)
            if not isinstance(baseline_kind, dict) or not isinstance(candidate_kind, dict):
                unverifiable.append(f"{kind} trigger metrics are unavailable")
                continue
            baseline_validation = baseline_kind.get("validation")
            candidate_validation = candidate_kind.get("validation")
            if not isinstance(baseline_validation, dict) or not isinstance(
                candidate_validation, dict
            ):
                unverifiable.append(f"{kind} validation trigger metrics are unavailable")
                continue
            for metric in ("accuracy", "precision", "recall"):
                baseline_value = baseline_validation.get(metric)
                candidate_value = candidate_validation.get(metric)
                if baseline_value is None or candidate_value is None:
                    unverifiable.append(f"{kind} trigger {metric} is unavailable")
                elif float(candidate_value) < float(baseline_value):
                    reasons.append(f"candidate {kind} trigger {metric} regressed")
    elif float(candidate.get("trigger_accuracy", 0.0)) < float(
        baseline.get("trigger_accuracy", 0.0)
    ):
        reasons.append("candidate trigger accuracy regressed")
    if float(candidate.get("behavior_pass_rate", 0.0)) < float(
        baseline.get("behavior_pass_rate", 0.0)
    ):
        reasons.append("candidate behavior pass rate regressed")
    for metric, ratio in (
        ("total_tokens", TOKEN_REGRESSION_RATIO),
        ("duration_ms", DURATION_REGRESSION_RATIO),
    ):
        baseline_value = baseline.get(metric)
        candidate_value = candidate.get(metric)
        if baseline_value is None or candidate_value is None:
            unverifiable.append(f"{metric} comparison is unavailable")
        elif (
            not resource_regression_reason
            and float(baseline_value) > 0
            and float(candidate_value) > float(baseline_value) * ratio
        ):
            reasons.append(
                f"candidate {metric} exceeded the unapproved {ratio:.2f}x regression threshold"
            )
    status = "Fail" if reasons else "Unverifiable" if unverifiable else "Pass"
    return {
        "status": status,
        "reasons": reasons,
        "unverifiable": sorted(set(unverifiable)),
        "resource_regression_reason": resource_regression_reason,
    }


def summarize_trigger_outcomes(
    outcomes: Mapping[tuple[str, str, str], Mapping[str, object]],
) -> tuple[dict[str, dict[str, dict[str, object]]], list[dict[str, object]]]:
    counts: dict[tuple[str, str], dict[str, int]] = {}
    variances: dict[tuple[str, str], list[float]] = {}
    case_metrics: list[dict[str, object]] = []
    for (kind, split, case_id), outcome in sorted(outcomes.items()):
        expected = bool(outcome["expected"])
        values = [bool(value) for value in outcome["values"]]  # type: ignore[index]
        loaded = sum(values)
        load_rate = loaded / len(values)
        variance = load_rate * (1.0 - load_rate)
        case_metrics.append(
            {
                "kind": kind,
                "split": split,
                "case": case_id,
                "expected_skill_loaded": expected,
                "load_rate": load_rate,
                "pass_rate": sum(value is expected for value in values) / len(values),
                "run_variance": variance,
            }
        )
        metric_key = (kind, split)
        bucket = counts.setdefault(metric_key, {"tp": 0, "fp": 0, "tn": 0, "fn": 0})
        variances.setdefault(metric_key, []).append(variance)
        for actual in values:
            if expected and actual:
                bucket["tp"] += 1
            elif expected:
                bucket["fn"] += 1
            elif actual:
                bucket["fp"] += 1
            else:
                bucket["tn"] += 1
    metrics: dict[str, dict[str, dict[str, object]]] = {}
    for (kind, split), bucket in sorted(counts.items()):
        total = sum(bucket.values())
        precision_denominator = bucket["tp"] + bucket["fp"]
        recall_denominator = bucket["tp"] + bucket["fn"]
        kind_variances = variances[(kind, split)]
        metrics.setdefault(kind, {})[split] = {
            **bucket,
            "accuracy": (bucket["tp"] + bucket["tn"]) / total if total else None,
            "precision": bucket["tp"] / precision_denominator if precision_denominator else None,
            "recall": bucket["tp"] / recall_denominator if recall_denominator else None,
            "mean_run_variance": sum(kind_variances) / len(kind_variances),
            "max_run_variance": max(kind_variances),
        }
    return metrics, case_metrics


def validate_case_filter(
    contracts: Mapping[str, Mapping[str, object]], selected: set[str] | None
) -> list[str]:
    if not selected:
        return []
    known: set[str] = set()
    for skill, contract in contracts.items():
        triggers = contract["triggers"]["queries"]  # type: ignore[index]
        behavior = contract["behavior"]["evals"]  # type: ignore[index]
        known.update(f"{skill}:trigger:{case['id']}" for case in triggers)
        known.update(f"{skill}:behavior:{case['id']}" for case in behavior)
    return [f"unknown eval case: {case}" for case in sorted(selected - known)]


def run_checked(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def resolve_ref(ref: str) -> str:
    return run_checked(["git", "rev-parse", f"{ref}^{{commit}}"]).stdout.strip()


@contextmanager
def detached_worktree(ref: str) -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="tigerkit-eval-worktree-") as directory:
        path = Path(directory) / "repo"
        run_checked(["git", "worktree", "add", "--detach", str(path), ref])
        try:
            yield path
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )


@contextmanager
def isolated_checkout(source: Path) -> Iterator[Path]:
    """Give one eval run a disposable checkout so runs cannot contaminate each other."""
    with tempfile.TemporaryDirectory(prefix="tigerkit-eval-checkout-") as directory:
        path = Path(directory) / "repo"
        if (source / ".git").exists():
            sha = run_checked(["git", "rev-parse", "HEAD"], cwd=source).stdout.strip()
            run_checked(["git", "clone", "--quiet", "--shared", "--no-checkout", str(ROOT), str(path)])
            run_checked(["git", "checkout", "--quiet", "--detach", sha], cwd=path)
        else:
            shutil.copytree(source, path)
        yield path


def load_eval_contracts(root: Path, selected: set[str] | None) -> dict[str, dict[str, object]]:
    contracts: dict[str, dict[str, object]] = {}
    for skill_dir in sorted((root / "skills").glob("tk-*")):
        if selected and skill_dir.name not in selected:
            continue
        triggers = json.loads((skill_dir / "evals" / "triggers.json").read_text(encoding="utf-8"))
        behavior = json.loads((skill_dir / "evals" / "evals.json").read_text(encoding="utf-8"))
        contracts[skill_dir.name] = {"triggers": triggers, "behavior": behavior}
    if selected and set(contracts) != selected:
        missing = ", ".join(sorted(selected - set(contracts)))
        raise ValueError(f"unknown or missing eval skill: {missing}")
    return contracts


def run_json_command(command: str, env: dict[str, str], *, cwd: Path) -> dict[str, object]:
    started = time.monotonic()
    completed = subprocess.run(
        shlex.split(command),
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {completed.stderr.strip() or completed.stdout.strip()}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not emit one JSON object: {exc}") from exc
    if not isinstance(result, dict):
        raise RuntimeError("command result must be a JSON object")
    result.setdefault("duration_ms", round((time.monotonic() - started) * 1000))
    return result


def run_adapter(
    command: str,
    *,
    checkout: Path,
    skill: str,
    prompt: str,
    mode: str,
    host: str,
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="tigerkit-eval-run-") as directory:
        run_dir = Path(directory)
        home = run_dir / "home"
        home.mkdir()
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(home),
                "CLAUDE_CONFIG_DIR": str(home / ".claude"),
                "CODEX_HOME": str(home / ".codex"),
                "HERMES_HOME": str(home / ".hermes"),
                "TK_EVAL_HOST": host,
                "TK_EVAL_MODE": mode,
                "TK_EVAL_PROMPT": prompt,
                "TK_EVAL_SKILL": skill,
                "TK_EVAL_SKILL_DIR": str(checkout / "skills" / skill),
                "TK_EVAL_RUN_DIR": str(run_dir),
            }
        )
        result = run_json_command(command, env, cwd=checkout)
        errors = validate_adapter_result(result)
        if errors:
            raise RuntimeError("; ".join(errors))
        return result


def run_grader(command: str, output: str, assertions: list[str], *, cwd: Path) -> dict[str, object]:
    env = os.environ.copy()
    env.update(
        {
            "TK_EVAL_OUTPUT": output,
            "TK_EVAL_ASSERTIONS": json.dumps(assertions, ensure_ascii=False),
        }
    )
    result = run_json_command(command, env, cwd=cwd)
    rows = result.get("assertion_results")
    if not isinstance(rows, list) or len(rows) != len(assertions):
        raise RuntimeError("grader result must contain one assertion_results row per assertion")
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("passed"), bool) or not isinstance(
            row.get("evidence"), str
        ):
            raise RuntimeError("grader assertion rows require boolean passed and string evidence")
    return result


def git_head(checkout: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def verify_mechanical_assertion(
    assertion: Mapping[str, object],
    *,
    adapter_result: Mapping[str, object],
    checkout: Path,
    initial_head: str | None,
) -> dict[str, object]:
    assertion_type = assertion.get("type")
    if assertion_type == "terminal_status":
        allowed = assertion.get("allowed", [])
        actual = adapter_result.get("terminal_status")
        passed = isinstance(allowed, list) and actual in allowed
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"terminal_status={actual!r}; allowed={allowed!r}",
        }
    if assertion_type in {"path_exists", "path_absent"}:
        relative = str(assertion.get("path", ""))
        target = (checkout / relative).resolve()
        inside = target == checkout.resolve() or checkout.resolve() in target.parents
        exists = target.exists() if inside else False
        passed = inside and (exists if assertion_type == "path_exists" else not exists)
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"path={relative!r}; inside_checkout={inside}; exists={exists}",
        }
    if assertion_type in {"git_head_changed", "git_head_unchanged"}:
        final_head = git_head(checkout)
        available = initial_head is not None and final_head is not None
        changed = available and initial_head != final_head
        passed = available and (
            changed if assertion_type == "git_head_changed" else not changed
        )
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"initial_head={initial_head!r}; final_head={final_head!r}",
        }
    return {
        "type": assertion_type,
        "passed": False,
        "evidence": "unsupported mechanical assertion type",
    }


def grade_behavior(
    grader_command: str,
    adapter_result: Mapping[str, object],
    assertions: list[Mapping[str, object]],
    *,
    checkout: Path,
    initial_head: str | None,
) -> list[dict[str, object]]:
    judge_assertions = [
        str(assertion["criterion"])
        for assertion in assertions
        if assertion.get("type") == "judge"
    ]
    judge_rows: Iterator[dict[str, object]]
    if judge_assertions:
        grade = run_grader(
            grader_command,
            str(adapter_result["output"]),
            judge_assertions,
            cwd=checkout,
        )
        judge_rows = iter(grade["assertion_results"])  # type: ignore[arg-type]
    else:
        judge_rows = iter(())
    results: list[dict[str, object]] = []
    for assertion in assertions:
        if assertion.get("type") == "judge":
            row = next(judge_rows)
            results.append(
                {
                    "type": "judge",
                    "criterion": assertion["criterion"],
                    "passed": row["passed"],
                    "evidence": row["evidence"],
                }
            )
        else:
            results.append(
                verify_mechanical_assertion(
                    assertion,
                    adapter_result=adapter_result,
                    checkout=checkout,
                    initial_head=initial_head,
                )
            )
    return results


def evaluate_checkout(
    checkout: Path,
    contracts: dict[str, dict[str, object]],
    *,
    adapter_command: str,
    grader_command: str,
    host: str,
    runs: int,
    case_filter: set[str] | None,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    trigger_total = 0
    trigger_passed = 0
    behavior_total = 0
    behavior_passed = 0
    safety_failures = 0
    tokens_available = True
    total_tokens = 0.0
    total_duration = 0.0
    trigger_outcomes: dict[tuple[str, str, str], dict[str, object]] = {}
    for skill, contract in contracts.items():
        triggers = contract["triggers"]["queries"]  # type: ignore[index]
        kind = str(contract["triggers"]["kind"])  # type: ignore[index]
        behavior = contract["behavior"]["evals"]  # type: ignore[index]
        for query in triggers:
            case_id = f"{skill}:trigger:{query['id']}"
            if case_filter and case_id not in case_filter:
                continue
            for run_number in range(1, runs + 1):
                with isolated_checkout(checkout) as run_checkout:
                    result = run_adapter(
                        adapter_command,
                        checkout=run_checkout,
                        skill=skill,
                        prompt=query["query"],
                        mode="trigger",
                        host=host,
                    )
                passed = result["skill_loaded"] is query["should_trigger"]
                trigger_outcome = trigger_outcomes.setdefault(
                    (kind, str(query["split"]), case_id),
                    {"expected": query["should_trigger"], "values": []},
                )
                trigger_outcome["values"].append(result["skill_loaded"])  # type: ignore[union-attr]
                trigger_total += 1
                trigger_passed += int(passed)
                total_duration += float(result["duration_ms"])
                if result.get("total_tokens") is None:
                    tokens_available = False
                else:
                    total_tokens += float(result["total_tokens"])
                records.append(
                    {
                        "case": case_id,
                        "kind": kind,
                        "split": query["split"],
                        "run": run_number,
                        "passed": passed,
                        "expected_skill_loaded": query["should_trigger"],
                        "actual_skill_loaded": result["skill_loaded"],
                        "evidence": f"adapter skill_loaded={result['skill_loaded']!r}",
                        "duration_ms": result["duration_ms"],
                        "total_tokens": result.get("total_tokens"),
                    }
                )
        for case in behavior:
            case_id = f"{skill}:behavior:{case['id']}"
            if case_filter and case_id not in case_filter:
                continue
            for run_number in range(1, runs + 1):
                with isolated_checkout(checkout) as run_checkout:
                    initial_head = git_head(run_checkout)
                    result = run_adapter(
                        adapter_command,
                        checkout=run_checkout,
                        skill=skill,
                        prompt=case["prompt"],
                        mode="behavior",
                        host=host,
                    )
                    assertion_results = grade_behavior(
                        grader_command,
                        result,
                        case["assertions"],
                        checkout=run_checkout,
                        initial_head=initial_head,
                    )
                passed = all(row["passed"] for row in assertion_results)
                behavior_total += 1
                behavior_passed += int(passed)
                if case.get("safety") is True and not passed:
                    safety_failures += 1
                total_duration += float(result["duration_ms"])
                if result.get("total_tokens") is None:
                    tokens_available = False
                else:
                    total_tokens += float(result["total_tokens"])
                records.append(
                    {
                        "case": case_id,
                        "run": run_number,
                        "passed": passed,
                        "safety": case.get("safety") is True,
                        "assertion_results": assertion_results,
                        "duration_ms": result["duration_ms"],
                        "total_tokens": result.get("total_tokens"),
                    }
                )
    trigger_metrics, trigger_case_metrics = summarize_trigger_outcomes(trigger_outcomes)
    summary: dict[str, object] = {
        "trigger_accuracy": trigger_passed / trigger_total if trigger_total else 0.0,
        "trigger_metrics": trigger_metrics,
        "trigger_case_metrics": trigger_case_metrics,
        "behavior_pass_rate": behavior_passed / behavior_total if behavior_total else 0.0,
        "safety_failures": safety_failures,
        "trigger_runs": trigger_total,
        "behavior_runs": behavior_total,
        "duration_ms": total_duration,
        "total_tokens": total_tokens if tokens_available else None,
        "token_metric_status": "verified" if tokens_available else "Unverifiable",
    }
    return summary, records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--host", required=True)
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument("--case", action="append", dest="cases")
    parser.add_argument("--adapter-command")
    parser.add_argument("--grader-command")
    parser.add_argument("--output")
    parser.add_argument(
        "--resource-regression-reason",
        help="record the approved reason for a candidate token/time increase",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def write_result(output: Path, result: Mapping[str, object]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    if args.runs < 1:
        raise SystemExit("--runs must be positive")
    output: Path | None = None
    if args.output:
        output = Path(args.output).resolve()
        if output == ROOT or ROOT in output.parents:
            raise SystemExit("--output must be outside the repository; use a CI artifact or temporary directory")
    elif not args.dry_run:
        raise SystemExit("live eval requires --output outside the repository")
    try:
        baseline_sha = resolve_ref(args.baseline)
        candidate_sha = resolve_ref(args.candidate)
    except (OSError, subprocess.SubprocessError) as exc:
        if args.dry_run or output is None:
            raise SystemExit(f"cannot resolve eval refs: {exc}") from exc
        result = {"status": "Unverifiable", "error": f"cannot resolve eval refs: {exc}"}
        write_result(output, result)
        return 2
    selected = set(args.skills) if args.skills else None
    try:
        contracts = load_eval_contracts(ROOT, selected)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if args.dry_run or output is None:
            raise SystemExit(f"cannot load eval contracts: {exc}") from exc
        result = {"status": "Unverifiable", "error": f"cannot load eval contracts: {exc}"}
        write_result(output, result)
        return 2
    case_errors = validate_case_filter(contracts, set(args.cases) if args.cases else None)
    if case_errors:
        if args.dry_run or output is None:
            raise SystemExit("; ".join(case_errors))
        result = {"status": "Unverifiable", "error": "; ".join(case_errors)}
        write_result(output, result)
        return 2
    plan = {
        "baseline": baseline_sha,
        "candidate": candidate_sha,
        "host": args.host,
        "runs": args.runs,
        "skills": sorted(contracts),
        "trigger_cases": sum(len(value["triggers"]["queries"]) for value in contracts.values()),  # type: ignore[index]
        "behavior_cases": sum(len(value["behavior"]["evals"]) for value in contracts.values()),  # type: ignore[index]
        "cases": args.cases or "all",
        "output": str(output) if output else "not-written-in-dry-run",
    }
    if args.dry_run:
        print(json.dumps({"status": "Dry-run", "plan": plan}, ensure_ascii=False, indent=2))
        return 0
    if not args.adapter_command or not args.grader_command:
        result = {
            "status": "Unverifiable",
            "error": "live eval requires --adapter-command and --grader-command",
            "plan": plan,
        }
        write_result(output, result)  # type: ignore[arg-type]
        return 2
    output.mkdir(parents=True, exist_ok=True)  # type: ignore[union-attr]
    try:
        with detached_worktree(args.baseline) as baseline_root, detached_worktree(args.candidate) as candidate_root:
            baseline_summary, baseline_records = evaluate_checkout(
                baseline_root,
                contracts,
                adapter_command=args.adapter_command,
                grader_command=args.grader_command,
                host=args.host,
                runs=args.runs,
                case_filter=set(args.cases) if args.cases else None,
            )
            candidate_summary, candidate_records = evaluate_checkout(
                candidate_root,
                contracts,
                adapter_command=args.adapter_command,
                grader_command=args.grader_command,
                host=args.host,
                runs=args.runs,
                case_filter=set(args.cases) if args.cases else None,
            )
    except (OSError, subprocess.SubprocessError, RuntimeError, ValueError) as exc:
        result = {"status": "Unverifiable", "error": str(exc), "plan": plan}
        write_result(output, result)  # type: ignore[arg-type]
        return 2
    verdict = build_verdict(
        baseline_summary,
        candidate_summary,
        resource_regression_reason=args.resource_regression_reason,
    )
    result = {
        "status": verdict["status"],
        "reasons": verdict["reasons"],
        "unverifiable": verdict["unverifiable"],
        "plan": plan,
        "baseline": baseline_summary,
        "candidate": candidate_summary,
        "resource_regression_reason": args.resource_regression_reason,
    }
    (output / "baseline-records.json").write_text(
        json.dumps(baseline_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "candidate-records.json").write_text(
        json.dumps(candidate_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_result(output, result)  # type: ignore[arg-type]
    return 0 if verdict["status"] == "Pass" else 2 if verdict["status"] == "Unverifiable" else 1


if __name__ == "__main__":
    raise SystemExit(main())
