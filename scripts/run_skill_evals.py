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
TERMINAL_STATUSES = {
    "Pass",
    "Fail",
    "Blocked",
    "Unverifiable",
    "Pending",
    "NotApplicable",
}
SUPPORTED_HOSTS = ("claude-code", "codex", "hermes-agent")


def validate_adapter_result(result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    skill_loaded = result.get("skill_loaded")
    loaded_skills = result.get("loaded_skills")
    if not isinstance(skill_loaded, bool) and not isinstance(loaded_skills, list):
        errors.append("adapter result requires boolean skill_loaded or string-list loaded_skills")
    if isinstance(loaded_skills, list) and (
        not all(isinstance(value, str) and value.strip() for value in loaded_skills)
        or len(set(loaded_skills)) != len(loaded_skills)
    ):
        errors.append("adapter result loaded_skills must contain unique non-empty strings")
    selected_skill = result.get("selected_skill")
    if "selected_skill" in result and selected_skill is not None and not (
        isinstance(selected_skill, str) and selected_skill.strip()
    ):
        errors.append("adapter result selected_skill must be a non-empty string or null")
    if (
        isinstance(loaded_skills, list)
        and isinstance(selected_skill, str)
        and selected_skill not in loaded_skills
    ):
        errors.append("adapter result selected_skill must appear in loaded_skills")
    if not isinstance(result.get("output"), str):
        errors.append("adapter result requires string output")
    for field in ("total_tokens", "duration_ms"):
        value = result.get(field)
        if value is not None and not isinstance(value, (int, float)):
            errors.append(f"adapter result {field} must be numeric or null")
    terminal_status = result.get("terminal_status")
    if terminal_status not in TERMINAL_STATUSES:
        errors.append(
            "adapter result terminal_status must be one of "
            + ", ".join(sorted(TERMINAL_STATUSES))
        )
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
    if int(candidate.get("routing_runs", 0)) > 0 and float(
        candidate.get("routing_pass_rate", 0.0)
    ) < 1.0:
        reasons.append("candidate catalog routing matrix has failures")
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


def load_catalog_contract(root: Path) -> dict[str, object] | None:
    path = root / "evals" / "catalog-routing.json"
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("evals/catalog-routing.json must contain one object")
    return value


def _contract_case_map(contract: Mapping[str, object], key: str) -> dict[str, Mapping[str, object]]:
    rows = contract.get(key, [])
    if not isinstance(rows, list):
        return {}
    return {
        str(row["id"]): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }


def _migration_map(contract: Mapping[str, object]) -> dict[str, str]:
    migrations = contract.get("migrations", [])
    if not isinstance(migrations, list):
        return {}
    result: dict[str, str] = {}
    for row in migrations:
        if not isinstance(row, dict):
            continue
        old = row.get("from")
        new = row.get("to")
        reason = row.get("reason")
        if all(isinstance(value, str) and value.strip() for value in (old, new, reason)):
            result[str(old)] = str(new)
    return result


def _terminal_values(assertions: object) -> set[str]:
    if not isinstance(assertions, list):
        return set()
    aliases = {"pending": "Pending"}
    values: set[str] = set()
    for assertion in assertions:
        if not isinstance(assertion, dict) or assertion.get("type") != "terminal_status":
            continue
        expected = assertion.get("expected")
        allowed = assertion.get("allowed", [])
        raw_values = [expected] if isinstance(expected, str) else allowed if isinstance(allowed, list) else []
        for value in raw_values:
            if not isinstance(value, str):
                continue
            normalized = aliases.get(value, value)
            if normalized in TERMINAL_STATUSES:
                values.add(normalized)
    return values


def _terminal_forbidden(assertions: object) -> set[str]:
    if not isinstance(assertions, list):
        return set()
    values: set[str] = set()
    for assertion in assertions:
        if not isinstance(assertion, dict) or assertion.get("type") != "terminal_status":
            continue
        forbidden = assertion.get("forbidden", [])
        if isinstance(forbidden, list):
            values.update(
                value
                for value in forbidden
                if isinstance(value, str) and value in TERMINAL_STATUSES
            )
    return values


def compare_eval_contracts(
    baseline: Mapping[str, Mapping[str, object]],
    candidate: Mapping[str, Mapping[str, object]],
) -> list[str]:
    """Reject deleted or mechanically weakened eval coverage before model execution."""
    errors: list[str] = []
    for skill, baseline_contract in sorted(baseline.items()):
        candidate_contract = candidate.get(skill)
        if candidate_contract is None:
            errors.append(f"{skill}: candidate deleted the baseline eval contract")
            continue
        for section, key in (("trigger", "queries"), ("behavior", "evals")):
            baseline_data = baseline_contract[f"{section}s" if section == "trigger" else "behavior"]
            candidate_data = candidate_contract[f"{section}s" if section == "trigger" else "behavior"]
            if not isinstance(baseline_data, dict) or not isinstance(candidate_data, dict):
                errors.append(f"{skill}: {section} contract must be an object")
                continue
            baseline_cases = _contract_case_map(baseline_data, key)
            candidate_cases = _contract_case_map(candidate_data, key)
            migrations = _migration_map(candidate_data)
            for case_id, baseline_case in sorted(baseline_cases.items()):
                candidate_case = candidate_cases.get(case_id)
                if candidate_case is None:
                    migrated_to = migrations.get(case_id)
                    if not migrated_to or migrated_to not in candidate_cases:
                        errors.append(
                            f"{skill}: candidate deleted {section} case {case_id!r} "
                            "without an explicit migration reason"
                        )
                    continue
                if section == "trigger":
                    if candidate_case.get("should_trigger") is not baseline_case.get("should_trigger"):
                        errors.append(
                            f"{skill}: trigger case {case_id!r} changed expected routing "
                            "without an explicit migration"
                        )
                    continue
                if baseline_case.get("safety") is True and candidate_case.get("safety") is not True:
                    errors.append(f"{skill}: behavior case {case_id!r} weakened safety coverage")
                baseline_types = {
                    str(row.get("type"))
                    for row in baseline_case.get("assertions", [])
                    if isinstance(row, dict) and row.get("type") != "judge"
                }
                candidate_types = {
                    str(row.get("type"))
                    for row in candidate_case.get("assertions", [])
                    if isinstance(row, dict) and row.get("type") != "judge"
                }
                if not baseline_types.issubset(candidate_types):
                    errors.append(
                        f"{skill}: behavior case {case_id!r} removed mechanical assertions "
                        f"{sorted(baseline_types - candidate_types)}"
                    )
                candidate_nonterminal = [
                    json.dumps(assertion, ensure_ascii=False, sort_keys=True)
                    for assertion in candidate_case.get("assertions", [])
                    if isinstance(assertion, dict)
                    and assertion.get("type") not in {"judge", "terminal_status"}
                ]
                for assertion in baseline_case.get("assertions", []):
                    if not isinstance(assertion, dict) or assertion.get("type") in {
                        "judge",
                        "terminal_status",
                    }:
                        continue
                    fingerprint = json.dumps(
                        assertion, ensure_ascii=False, sort_keys=True
                    )
                    if fingerprint in candidate_nonterminal:
                        candidate_nonterminal.remove(fingerprint)
                    else:
                        errors.append(
                            f"{skill}: behavior case {case_id!r} weakened assertion "
                            f"{assertion!r}"
                        )
                baseline_terminal = _terminal_values(baseline_case.get("assertions"))
                candidate_terminal = _terminal_values(candidate_case.get("assertions"))
                if baseline_terminal and (
                    not candidate_terminal or not candidate_terminal.issubset(baseline_terminal)
                ):
                    errors.append(
                        f"{skill}: behavior case {case_id!r} weakened terminal expectations"
                    )
                baseline_forbidden = _terminal_forbidden(
                    baseline_case.get("assertions")
                )
                candidate_forbidden = _terminal_forbidden(
                    candidate_case.get("assertions")
                )
                if not baseline_forbidden.issubset(candidate_forbidden):
                    errors.append(
                        f"{skill}: behavior case {case_id!r} removed forbidden terminal values"
                    )
    return errors


def compare_catalog_contracts(
    baseline: Mapping[str, object] | None,
    candidate: Mapping[str, object] | None,
) -> list[str]:
    if baseline is None:
        return []
    if candidate is None:
        return ["catalog routing: candidate deleted the baseline contract"]
    errors: list[str] = []
    baseline_cases = _contract_case_map(baseline, "cases")
    candidate_cases = _contract_case_map(candidate, "cases")
    migrations = _migration_map(candidate)
    for case_id, baseline_case in sorted(baseline_cases.items()):
        candidate_case = candidate_cases.get(case_id)
        if candidate_case is None:
            migrated_to = migrations.get(case_id)
            if not migrated_to or migrated_to not in candidate_cases:
                errors.append(
                    f"catalog routing: candidate deleted case {case_id!r} "
                    "without an explicit migration reason"
                )
            continue
        if (
            candidate_case.get("expected_selected_skill")
            != baseline_case.get("expected_selected_skill")
        ):
            errors.append(
                f"catalog routing: case {case_id!r} changed expected selection "
                "without an explicit migration"
            )
        if baseline_case.get("critical") is True and candidate_case.get("critical") is not True:
            errors.append(f"catalog routing: case {case_id!r} weakened critical coverage")
    baseline_hosts = baseline.get("critical_hosts", [])
    candidate_hosts = candidate.get("critical_hosts", [])
    if (
        isinstance(baseline_hosts, list)
        and isinstance(candidate_hosts, list)
        and not set(baseline_hosts).issubset(set(candidate_hosts))
    ):
        errors.append("catalog routing: candidate removed critical host coverage")
    return errors


def validate_case_filter_union(
    baseline: Mapping[str, Mapping[str, object]],
    candidate: Mapping[str, Mapping[str, object]],
    selected: set[str] | None,
    *,
    baseline_catalog: Mapping[str, object] | None = None,
    candidate_catalog: Mapping[str, object] | None = None,
) -> list[str]:
    if not selected:
        return []
    known_catalog: set[str] = set()
    for catalog in (baseline_catalog, candidate_catalog):
        if not isinstance(catalog, Mapping):
            continue
        cases = catalog.get("cases", [])
        if isinstance(cases, list):
            known_catalog.update(
                f"catalog:behavior:{case['id']}"
                for case in cases
                if isinstance(case, dict) and isinstance(case.get("id"), str)
            )
    errors: list[str] = []
    for case in sorted(selected):
        if (
            case not in known_catalog
            and validate_case_filter(baseline, {case})
            and validate_case_filter(candidate, {case})
        ):
            errors.append(f"unknown eval case: {case}")
    return errors


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
        loaded_skills = result.get("loaded_skills")
        if isinstance(loaded_skills, list):
            catalog_loaded = skill in loaded_skills
            if isinstance(result.get("skill_loaded"), bool) and result["skill_loaded"] is not catalog_loaded:
                raise RuntimeError("adapter result skill_loaded disagrees with loaded_skills")
            result["skill_loaded"] = catalog_loaded
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


def _safe_checkout_path(checkout: Path, relative: object) -> tuple[Path, bool]:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return checkout, False
    target = (checkout / relative).resolve()
    root = checkout.resolve()
    return target, target != root and root in target.parents


def _changed_paths(checkout: Path, initial_head: str | None) -> list[str] | None:
    if initial_head is None:
        return None
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "-z", initial_head, "--"],
        cwd=checkout,
        text=False,
        capture_output=True,
        check=False,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=checkout,
        text=False,
        capture_output=True,
        check=False,
    )
    if tracked.returncode != 0 or untracked.returncode != 0:
        return None
    values = tracked.stdout.split(b"\0") + untracked.stdout.split(b"\0")
    return sorted({value.decode("utf-8", "surrogateescape") for value in values if value})


def _candidate_diff(checkout: Path, initial_head: str | None) -> str | None:
    if initial_head is None:
        return None
    completed = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--binary", initial_head, "--"],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    chunks = [completed.stdout]
    for relative in _changed_paths(checkout, initial_head) or []:
        target = checkout / relative
        if not target.is_file() or subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=checkout,
            text=True,
            capture_output=True,
            check=False,
        ).returncode == 0:
            continue
        untracked = subprocess.run(
            ["git", "diff", "--no-index", "--binary", "--", "/dev/null", relative],
            cwd=checkout,
            text=True,
            capture_output=True,
            check=False,
        )
        if untracked.returncode in {0, 1}:
            chunks.append(untracked.stdout)
    return "".join(chunks)


def verify_mechanical_assertion(
    assertion: Mapping[str, object],
    *,
    adapter_result: Mapping[str, object],
    checkout: Path,
    initial_head: str | None,
) -> dict[str, object]:
    assertion_type = assertion.get("type")
    if assertion_type == "terminal_status":
        actual = adapter_result.get("terminal_status")
        expected = assertion.get("expected")
        allowed = assertion.get("allowed")
        forbidden = assertion.get("forbidden", [])
        if isinstance(expected, str):
            passed = actual == expected
            expectation = f"expected={expected!r}"
        else:
            passed = isinstance(allowed, list) and actual in allowed
            expectation = f"allowed={allowed!r}"
        if isinstance(forbidden, list) and actual in forbidden:
            passed = False
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": (
                f"terminal_status={actual!r}; {expectation}; forbidden={forbidden!r}"
            ),
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
    if assertion_type in {"output_contains", "output_absent"}:
        text = str(assertion.get("text", ""))
        output = str(adapter_result.get("output", ""))
        contains = text in output
        passed = bool(text) and (
            contains if assertion_type == "output_contains" else not contains
        )
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"text={text!r}; contains={contains}",
        }
    if assertion_type in {"path_text_contains", "path_text_absent"}:
        target, inside = _safe_checkout_path(checkout, assertion.get("path"))
        text = str(assertion.get("text", ""))
        readable = inside and target.is_file()
        try:
            content = (
                target.read_text(encoding="utf-8", errors="replace")
                if readable
                else ""
            )
        except OSError:
            readable = False
            content = ""
        contains = text in content
        passed = bool(text) and readable and (
            contains if assertion_type == "path_text_contains" else not contains
        )
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": (
                f"path={assertion.get('path')!r}; readable={readable}; "
                f"text={text!r}; contains={contains}"
            ),
        }
    if assertion_type == "changed_paths_equal":
        expected = assertion.get("paths", [])
        actual = _changed_paths(checkout, initial_head)
        passed = (
            isinstance(expected, list)
            and all(isinstance(value, str) for value in expected)
            and actual == sorted(set(expected))
        )
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"changed_paths={actual!r}; expected={expected!r}",
        }
    if assertion_type in {"git_diff_contains", "git_diff_absent"}:
        text = str(assertion.get("text", ""))
        diff = _candidate_diff(checkout, initial_head)
        contains = isinstance(diff, str) and text in diff
        passed = bool(text) and diff is not None and (
            contains if assertion_type == "git_diff_contains" else not contains
        )
        return {
            "type": assertion_type,
            "passed": passed,
            "evidence": f"diff_available={diff is not None}; text={text!r}; contains={contains}",
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
    catalog_contract: Mapping[str, object] | None = None,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    trigger_total = 0
    trigger_passed = 0
    behavior_total = 0
    behavior_passed = 0
    routing_total = 0
    routing_passed = 0
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
                        "host": host,
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
                        "host": host,
                        "run": run_number,
                        "passed": passed,
                        "safety": case.get("safety") is True,
                        "assertion_results": assertion_results,
                        "duration_ms": result["duration_ms"],
                        "total_tokens": result.get("total_tokens"),
                    }
                )
    if catalog_contract is not None:
        catalog_cases = catalog_contract.get("cases", [])
        if not isinstance(catalog_cases, list):
            raise ValueError("catalog routing cases must be a list")
        for case in catalog_cases:
            if not isinstance(case, dict):
                raise ValueError("catalog routing case must be an object")
            case_id = f"catalog:behavior:{case['id']}"
            if case_filter and case_id not in case_filter:
                continue
            for run_number in range(1, runs + 1):
                with isolated_checkout(checkout) as run_checkout:
                    result = run_adapter(
                        adapter_command,
                        checkout=run_checkout,
                        skill=str(case["focus_skill"]),
                        prompt=str(case["prompt"]),
                        mode="catalog-routing",
                        host=host,
                    )
                expected = case.get("expected_selected_skill")
                selected_skill = result.get("selected_skill")
                loaded_skills = result.get("loaded_skills")
                selection_matches = selected_skill == expected
                load_matches = expected is None or (
                    isinstance(loaded_skills, list) and expected in loaded_skills
                )
                passed = selection_matches and load_matches
                routing_total += 1
                routing_passed += int(passed)
                if case.get("critical") is True and not passed:
                    safety_failures += 1
                total_duration += float(result["duration_ms"])
                if result.get("total_tokens") is None:
                    tokens_available = False
                else:
                    total_tokens += float(result["total_tokens"])
                records.append(
                    {
                        "case": case_id,
                        "host": host,
                        "kind": "catalog-routing",
                        "run": run_number,
                        "passed": passed,
                        "safety": case.get("critical") is True,
                        "expected_selected_skill": expected,
                        "actual_selected_skill": selected_skill,
                        "loaded_skills": loaded_skills,
                        "evidence": (
                            f"selected_skill={selected_skill!r}; "
                            f"loaded_skills={loaded_skills!r}"
                        ),
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
        "routing_pass_rate": routing_passed / routing_total if routing_total else None,
        "safety_failures": safety_failures,
        "trigger_runs": trigger_total,
        "behavior_runs": behavior_total,
        "routing_runs": routing_total,
        "duration_ms": total_duration,
        "total_tokens": total_tokens if tokens_available else None,
        "token_metric_status": "verified" if tokens_available else "Unverifiable",
    }
    return summary, records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument(
        "--host",
        action="append",
        choices=(*SUPPORTED_HOSTS, "all"),
        required=True,
        help="repeat for a host matrix or pass all",
    )
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
            raise SystemExit("--output must be outside the repository; use a temporary directory")
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
    hosts = list(SUPPORTED_HOSTS) if "all" in args.host else list(dict.fromkeys(args.host))
    selected = set(args.skills) if args.skills else None
    try:
        with detached_worktree(args.baseline) as baseline_root, detached_worktree(
            args.candidate
        ) as candidate_root:
            baseline_contracts = load_eval_contracts(baseline_root, selected)
            candidate_contracts = load_eval_contracts(candidate_root, selected)
            baseline_catalog = load_catalog_contract(baseline_root)
            candidate_catalog = load_catalog_contract(candidate_root)
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError) as exc:
        if args.dry_run or output is None:
            raise SystemExit(f"cannot load eval contracts: {exc}") from exc
        result = {"status": "Unverifiable", "error": f"cannot load eval contracts: {exc}"}
        write_result(output, result)
        return 2
    contract_errors = compare_eval_contracts(baseline_contracts, candidate_contracts)
    contract_errors.extend(
        compare_catalog_contracts(baseline_catalog, candidate_catalog)
    )
    case_filter = set(args.cases) if args.cases else None
    case_errors = validate_case_filter_union(
        baseline_contracts,
        candidate_contracts,
        case_filter,
        baseline_catalog=baseline_catalog,
        candidate_catalog=candidate_catalog,
    )
    if case_errors:
        if args.dry_run or output is None:
            raise SystemExit("; ".join(case_errors))
        result = {"status": "Unverifiable", "error": "; ".join(case_errors)}
        write_result(output, result)
        return 2
    plan = {
        "baseline": baseline_sha,
        "candidate": candidate_sha,
        "hosts": hosts,
        "runs": args.runs,
        "skills": sorted(set(baseline_contracts) | set(candidate_contracts)),
        "baseline_trigger_cases": sum(
            len(value["triggers"]["queries"]) for value in baseline_contracts.values()  # type: ignore[index]
        ),
        "candidate_trigger_cases": sum(
            len(value["triggers"]["queries"]) for value in candidate_contracts.values()  # type: ignore[index]
        ),
        "baseline_behavior_cases": sum(
            len(value["behavior"]["evals"]) for value in baseline_contracts.values()  # type: ignore[index]
        ),
        "candidate_behavior_cases": sum(
            len(value["behavior"]["evals"]) for value in candidate_contracts.values()  # type: ignore[index]
        ),
        "catalog_cases": (
            len(candidate_catalog.get("cases", []))
            if isinstance(candidate_catalog, dict)
            and isinstance(candidate_catalog.get("cases"), list)
            else 0
        ),
        "cases": args.cases or "all",
        "contract_drift": contract_errors,
        "output": str(output) if output else "not-written-in-dry-run",
    }
    if args.dry_run:
        status = "Fail" if contract_errors else "Dry-run"
        print(json.dumps({"status": status, "plan": plan}, ensure_ascii=False, indent=2))
        return 1 if contract_errors else 0
    if contract_errors:
        result = {
            "status": "Fail",
            "reasons": contract_errors,
            "unverifiable": [],
            "plan": plan,
        }
        write_result(output, result)  # type: ignore[arg-type]
        return 1
    if not args.adapter_command or not args.grader_command:
        result = {
            "status": "Unverifiable",
            "error": "live eval requires --adapter-command and --grader-command",
            "plan": plan,
        }
        write_result(output, result)  # type: ignore[arg-type]
        return 2
    output.mkdir(parents=True, exist_ok=True)  # type: ignore[union-attr]
    baseline_by_host: dict[str, dict[str, object]] = {}
    candidate_by_host: dict[str, dict[str, object]] = {}
    verdict_by_host: dict[str, dict[str, object]] = {}
    baseline_records: list[dict[str, object]] = []
    candidate_records: list[dict[str, object]] = []
    try:
        with detached_worktree(args.baseline) as baseline_root, detached_worktree(args.candidate) as candidate_root:
            for host in hosts:
                baseline_summary, host_baseline_records = evaluate_checkout(
                    baseline_root,
                    baseline_contracts,
                    adapter_command=args.adapter_command,
                    grader_command=args.grader_command,
                    host=host,
                    runs=args.runs,
                    case_filter=case_filter,
                    catalog_contract=baseline_catalog,
                )
                candidate_summary, host_candidate_records = evaluate_checkout(
                    candidate_root,
                    candidate_contracts,
                    adapter_command=args.adapter_command,
                    grader_command=args.grader_command,
                    host=host,
                    runs=args.runs,
                    case_filter=case_filter,
                    catalog_contract=candidate_catalog,
                )
                baseline_by_host[host] = baseline_summary
                candidate_by_host[host] = candidate_summary
                baseline_records.extend(host_baseline_records)
                candidate_records.extend(host_candidate_records)
                verdict_by_host[host] = build_verdict(
                    baseline_summary,
                    candidate_summary,
                    resource_regression_reason=args.resource_regression_reason,
                )
    except (OSError, subprocess.SubprocessError, RuntimeError, ValueError) as exc:
        result = {"status": "Unverifiable", "error": str(exc), "plan": plan}
        write_result(output, result)  # type: ignore[arg-type]
        return 2
    statuses = {str(value["status"]) for value in verdict_by_host.values()}
    overall_status = (
        "Fail"
        if "Fail" in statuses
        else "Unverifiable"
        if "Unverifiable" in statuses
        else "Pass"
    )
    reasons = [
        f"[{host}] {reason}"
        for host, verdict in verdict_by_host.items()
        for reason in verdict["reasons"]  # type: ignore[union-attr]
    ]
    unverifiable = [
        f"[{host}] {reason}"
        for host, verdict in verdict_by_host.items()
        for reason in verdict["unverifiable"]  # type: ignore[union-attr]
    ]
    result = {
        "status": overall_status,
        "reasons": reasons,
        "unverifiable": unverifiable,
        "plan": plan,
        "baseline": baseline_by_host,
        "candidate": candidate_by_host,
        "host_verdicts": verdict_by_host,
        "resource_regression_reason": args.resource_regression_reason,
    }
    (output / "baseline-records.json").write_text(
        json.dumps(baseline_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "candidate-records.json").write_text(
        json.dumps(candidate_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_result(output, result)  # type: ignore[arg-type]
    return 0 if overall_status == "Pass" else 2 if overall_status == "Unverifiable" else 1


if __name__ == "__main__":
    raise SystemExit(main())
