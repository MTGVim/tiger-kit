#!/usr/bin/env python3
"""Run TigerKit's deterministic release gate."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Mapping

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

if __package__:
    from .language_contract import LANGUAGE_EXACT_WORDS, LANGUAGE_WORD
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
    from language_contract import LANGUAGE_EXACT_WORDS, LANGUAGE_WORD
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
MANIFEST = ROOT / "evals/release-critical.json"
LEDGER_PATH = re.compile(r"\.tigerkit/[A-Za-z0-9_.-]+\.md")
LANGUAGE_JSON_MACHINE_KEYS = {
    "allowed",
    "behavior",
    "catalog",
    "command",
    "expected",
    "files",
    "from",
    "hosts",
    "id",
    "kind",
    "migrations",
    "path",
    "retired_catalog_cases",
    "retired_skill_contracts",
    "skill_name",
    "safety",
    "should_trigger",
    "to",
    "type",
    "version",
}
LANGUAGE_JSON_PROSE_KEYS = {
    "boundary",
    "criterion",
    "description",
    "expected_output",
    "prompt",
    "query",
    "reason",
    "text",
}


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
    retired = value.get("retired_skill_contracts", [])
    if not isinstance(retired, list) or not all(isinstance(row, str) and row for row in retired):
        raise ValueError("release-critical retired_skill_contracts must be a string list")
    retired_catalog = value.get("retired_catalog_cases", [])
    if not isinstance(retired_catalog, list) or not all(isinstance(row, str) and row for row in retired_catalog):
        raise ValueError("release-critical retired_catalog_cases must be a string list")
    return value


def _language_targets(root: Path) -> list[Path]:
    paths: list[Path] = []
    paths.extend(sorted(root.glob("*.md")))
    paths.extend(sorted(root.glob("skills/tk-*/**/*.md")))
    paths.extend(sorted(root.glob("skills/tk-*/agents/*.yaml")))
    paths.extend(sorted(root.glob("skills/tk-*/evals/*.json")))
    paths.extend(sorted(root.glob("evals/*.json")))
    paths.extend(sorted(root.glob("evals/**/*.md")))
    return sorted({path for path in paths if path.is_file()})


def _mask_language_literals(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"\[(?:user|auto|user/auto)\]", " ", text)
    text = re.sub(
        r"^\s*(?:[-*+]\s+)?(?:name|argument-hint|disable-model-invocation|metadata|kind|origin|relationship|version|tigerkit)\s*:\s*.*$",
        " ",
        text,
    )
    text = re.sub(r"(?<!\w)--[A-Za-z0-9][A-Za-z0-9_-]*", " ", text)
    text = re.sub(r"^\s*(?:[-*+]\s+)?[A-Za-z][A-Za-z0-9_-]*\s*:\s*", "", text)
    text = re.sub(r"(?<!\w)(?:[./~]|skills/|\.tigerkit/)[^\s,;:)]+", " ", text)
    return text


def _language_word_allowed(word: str) -> bool:
    if word in LANGUAGE_EXACT_WORDS:
        return True
    if word.startswith("tk-"):
        return True
    if word.isupper() and len(word) > 1:
        return True
    if any(char.isdigit() for char in word):
        return True
    if "_" in word:
        return True
    return False


def _scan_language_text(text: str, location: str) -> list[dict[str, object]]:
    violations: list[dict[str, object]] = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not line.strip():
            continue
        masked = _mask_language_literals(line)
        words = sorted(
            {
                word
                for word in LANGUAGE_WORD.findall(masked)
                if not _language_word_allowed(word)
            }
        )
        if words:
            normalized = " ".join(line.split())
            stable_location = re.sub(r"\[\d+\]", "[]", location)
            violations.append(
                {
                    "fingerprint": f"{stable_location}|{normalized}",
                    "location": f"{location}:{line_number}",
                    "words": words,
                }
            )
    return violations


def _json_prose_values(value: object, path: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        values: list[tuple[str, str]] = []
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key == "text" and ".assertions[" in path:
                continue
            if key in LANGUAGE_JSON_PROSE_KEYS and isinstance(child, str):
                values.append((child_path, child))
            elif key not in LANGUAGE_JSON_MACHINE_KEYS:
                values.extend(_json_prose_values(child, child_path))
        return values
    if isinstance(value, list):
        values = []
        for index, child in enumerate(value):
            values.extend(_json_prose_values(child, f"{path}[{index}]"))
        return values
    return []


def scan_language(root: Path) -> dict[str, object]:
    violations: list[dict[str, object]] = []
    targets = _language_targets(root)
    for path in targets:
        relative = str(path.relative_to(root))
        # SKILL.md is the model-facing contract. User-facing output, evals,
        # agent metadata, and ledger/artifact prose remain Korean and stay
        # covered by this gate.
        if path.name == "SKILL.md" and path.parent.parent.name == "skills" and path.parent.name.startswith("tk-"):
            continue
        if path.suffix == ".json":
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                continue
            for location, text in _json_prose_values(value, relative):
                violations.extend(_scan_language_text(text, location))
        else:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            violations.extend(_scan_language_text(text, relative))
    return {"files": len(targets), "violations": violations}


def summarize_language(report: Mapping[str, object]) -> dict[str, object]:
    rows = report.get("violations", [])
    violations = [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
    by_file: dict[str, int] = {}
    for row in violations:
        location = str(row.get("location", ""))
        by_file[location.split(":", 1)[0]] = by_file.get(location.split(":", 1)[0], 0) + 1
    return {
        "files": int(report.get("files", 0)),
        "violations": len(violations),
        "by_file": dict(sorted(by_file.items())),
    }


def compare_language_regression(
    baseline: Mapping[str, object], candidate: Mapping[str, object]
) -> list[str]:
    baseline_rows = baseline.get("violations", [])
    candidate_rows = candidate.get("violations", [])
    baseline_fingerprints = Counter(
        str(row.get("fingerprint"))
        for row in baseline_rows
        if isinstance(row, dict) and row.get("fingerprint")
    )
    candidate_fingerprints = Counter(
        str(row.get("fingerprint"))
        for row in candidate_rows
        if isinstance(row, dict) and row.get("fingerprint")
    )
    def file_name(row: object) -> str:
        if not isinstance(row, dict):
            return ""
        location = str(row.get("location", "")).split(":", 1)[0]
        return location.split(".json.", 1)[0] + ".json" if ".json." in location else location

    def word_weight(row: object) -> int:
        if not isinstance(row, dict) or not isinstance(row.get("words"), list):
            return 1
        return len(row["words"])

    baseline_by_file = Counter(file_name(row) for row in baseline_rows)
    candidate_by_file = Counter(file_name(row) for row in candidate_rows)
    baseline_weight = Counter()
    candidate_weight = Counter()
    for row in baseline_rows:
        baseline_weight[file_name(row)] += word_weight(row)
    for row in candidate_rows:
        candidate_weight[file_name(row)] += word_weight(row)
    regressing_files = {
        path
        for path, count in candidate_by_file.items()
        if count > baseline_by_file[path] or candidate_weight[path] > baseline_weight[path]
    }
    errors: list[str] = []
    if len(candidate_rows) > len(baseline_rows):
        errors.append(
            "language regression: authored-prose violation count increased "
            f"from {len(baseline_rows)} to {len(candidate_rows)}"
        )
    if regressing_files:
        errors.append(
            "language regression: authored-prose violation weight increased in "
            + ", ".join(sorted(regressing_files)[:5])
        )
    increased = [
        fingerprint
        for fingerprint, count in candidate_fingerprints.items()
        if fingerprint in baseline_fingerprints and count > baseline_fingerprints[fingerprint]
    ]
    if increased:
        errors.append(
            "language regression: an existing English-prose violation was duplicated "
            f"({len(increased)} fingerprint(s))"
        )
    new_rows = [
        row
        for row in candidate_rows
        if isinstance(row, dict) and file_name(row) in regressing_files
    ]
    if new_rows:
        examples = ", ".join(str(row.get("location")) for row in new_rows[:5])
        errors.append(f"language regression: new English prose at {examples}")
    return errors


def validate_ledger_eval_coverage(
    contracts: Mapping[str, Mapping[str, object]],
) -> tuple[list[str], dict[str, dict[str, int]]]:
    artifacts: dict[str, dict[str, int]] = {}
    errors: list[str] = []
    for skill, contract in contracts.items():
        cases = contract.get("behavior", {}).get("evals", [])  # type: ignore[union-attr]
        if not isinstance(cases, list):
            continue
        for case in cases:
            if not isinstance(case, dict):
                continue
            assertions = case.get("assertions", [])
            if not isinstance(assertions, list):
                continue
            for assertion in assertions:
                if not isinstance(assertion, dict) or assertion.get("type") != "path_exists":
                    continue
                path = assertion.get("path")
                if not isinstance(path, str) or not LEDGER_PATH.fullmatch(path):
                    continue
                record = artifacts.setdefault(
                    path,
                    {
                        "existence_cases": 0,
                        "hangul_assertions": 0,
                        "korean_prose_assertions": 0,
                    },
                )
                record["existence_cases"] += 1
                has_hangul_assertion = any(
                    isinstance(row, dict)
                    and row.get("type") == "path_text_has_hangul"
                    and row.get("path") == path
                    for row in assertions
                )
                if has_hangul_assertion:
                    record["hangul_assertions"] += 1
                has_korean_prose_assertion = any(
                    isinstance(row, dict)
                    and row.get("type") == "path_text_has_korean_prose"
                    and row.get("path") == path
                    for row in assertions
                )
                if has_korean_prose_assertion:
                    record["korean_prose_assertions"] += 1
                if not has_hangul_assertion or not has_korean_prose_assertion:
                    missing = (
                        "path_text_has_hangul"
                        if not has_hangul_assertion
                        else "path_text_has_korean_prose"
                    )
                    errors.append(
                        f"{skill}#{case.get('id', '<unnamed>')}: ledger generation "
                        f"coverage for {path} needs {missing}"
                    )
    return errors, dict(sorted(artifacts.items()))


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
        baseline_language = scan_language(baseline_root)
        candidate_language = scan_language(candidate_root)
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
        ledger_errors, ledger_coverage = validate_ledger_eval_coverage(candidate_contracts)
        contract_errors.extend(ledger_errors)
        contract_errors.extend(compare_language_regression(baseline_language, candidate_language))
        contract_errors.extend(validate_portable_artifacts(candidate_root))
        commands = [
            ["python3", "scripts/validate_skills.py"],
            ["python3", "scripts/validate_skills.py", "--links-only"],
            ["python3", "-B", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
            ["python3", "scripts/audit_catalog.py", "--check"],
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
        "ledger_coverage": ledger_coverage,
        "language": {
            "baseline": summarize_language(baseline_language),
            "candidate": summarize_language(candidate_language),
        },
        "static": static_records,
        "blocking_reasons": blocking_reasons,
    }
    (output / "release-gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if blocking_reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
