#!/usr/bin/env python3
"""Check static skill-size budgets and compare newly introduced context growth."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

try:
    from .validate_skills import frontmatter
except ImportError:
    from validate_skills import frontmatter


MANIFEST = "evals/token-budget.json"
SYNC_BLOCKS = ("result-summary", "output-notation", "questions", "skill-feedback", "summary-body")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?。！？])\s+")


def load_manifest(root: Path):
    path = root / MANIFEST
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return {}, [f"{MANIFEST}: cannot read budget manifest ({error})"]
    if not isinstance(value, dict) or value.get("version") != 1:
        return {}, [f"{MANIFEST}: expected version 1 object"]
    if not isinstance(value.get("limits"), dict):
        return {}, [f"{MANIFEST}: limits must be an object"]
    if not isinstance(value.get("rationales", {}), dict):
        return {}, [f"{MANIFEST}: rationales must be an object"]
    if any(not isinstance(reason, str) or not reason.strip() for reason in value.get("rationales", {}).values()):
        return {}, [f"{MANIFEST}: every rationale must be non-empty text"]
    return value, []


def _description_chars(path: Path) -> int:
    data, _ = frontmatter(path)
    description = data.get("description", "")
    if not isinstance(description, str):
        return len(str(description))
    return len(description)


def _shared_block_bytes(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    total = 0
    for name in SYNC_BLOCKS:
        match = re.search(
            rf"<!-- tigerkit:{re.escape(name)} -->.*?<!-- /tigerkit:{re.escape(name)} -->",
            text,
            re.DOTALL,
        )
        if match:
            total += len(match.group(0).encode("utf-8"))
    return total


def collect_metrics(
    root: Path,
    manifest: dict[str, object],
    *,
    allow_missing_always_read=False,
    use_before_paths=False,
):
    errors: list[str] = []
    metrics: dict[str, int] = {}
    skill_files = sorted((root / "skills").glob("tk-*/SKILL.md"))
    descriptions = []
    total_bytes = 0
    common_bytes = 0
    for path in skill_files:
        relative = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
            description_chars = _description_chars(path)
            block_bytes = _shared_block_bytes(path)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{relative}: cannot measure skill context ({error})")
            continue
        metrics[f"skill_md:{relative}"] = size
        descriptions.append(description_chars)
        total_bytes += size
        common_bytes += block_bytes
    metrics["skill_md_total_bytes"] = total_bytes
    metrics["description_total_chars"] = sum(descriptions)
    metrics["description_max_chars"] = max(descriptions, default=0)
    metrics["shared_block_bytes"] = common_bytes
    metrics["shared_block_ratio_ppm"] = round(common_bytes / total_bytes * 1_000_000) if total_bytes else 0

    limits = manifest.get("limits", {})
    always_read = limits.get("always_read", {}) if isinstance(limits, dict) else {}
    if not isinstance(always_read, dict):
        errors.append(f"{MANIFEST}: limits.always_read must be an object")
        always_read = {}
    for group, spec in always_read.items():
        if not isinstance(group, str) or not isinstance(spec, dict) or not isinstance(spec.get("paths"), list):
            errors.append(f"{MANIFEST}: always_read.{group} must declare a paths list")
            continue
        total = 0
        paths = spec.get("before_paths", spec["paths"]) if use_before_paths else spec["paths"]
        for relative in paths:
            if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
                errors.append(f"{MANIFEST}: unsafe always-read path in {group}: {relative!r}")
                continue
            path = root / relative
            try:
                total += path.stat().st_size
            except OSError:
                if not allow_missing_always_read:
                    errors.append(f"{MANIFEST}: always-read file is missing: {relative}")
        metrics[f"always_read:{group}"] = total
    return metrics, errors


def static_errors(root: Path):
    manifest, errors = load_manifest(root)
    if errors:
        return errors, {}, manifest
    metrics, metric_errors = collect_metrics(root, manifest)
    errors.extend(metric_errors)
    limits = manifest["limits"]
    expected = {
        "max_skill_md_bytes": ("skill_md_max_bytes", max(
            (value for key, value in metrics.items() if key.startswith("skill_md:")), default=0)),
        "max_total_skill_md_bytes": ("skill_md_total_bytes", metrics.get("skill_md_total_bytes", 0)),
        "max_total_description_chars": ("description_total_chars", metrics.get("description_total_chars", 0)),
        "max_single_description_chars": ("description_max_chars", metrics.get("description_max_chars", 0)),
        "max_shared_block_bytes": ("shared_block_bytes", metrics.get("shared_block_bytes", 0)),
        "max_shared_block_ratio_ppm": (
            "shared_block_ratio_ppm", metrics.get("shared_block_ratio_ppm", 0)
        ),
    }
    for limit_name, (metric_name, actual) in expected.items():
        ceiling = limits.get(limit_name)
        if not isinstance(ceiling, int) or ceiling < 0:
            errors.append(f"{MANIFEST}: {limit_name} must be a non-negative integer")
        elif actual > ceiling:
            errors.append(f"token budget exceeded: {metric_name} {actual} > {ceiling} ({limit_name})")
    for key, value in metrics.items():
        if key.startswith("always_read:"):
            group = key.split(":", 1)[1]
            ceiling = limits.get("always_read", {}).get(group, {}).get("max_bytes")
            if not isinstance(ceiling, int) or ceiling < 0:
                errors.append(f"{MANIFEST}: always_read.{group}.max_bytes must be a non-negative integer")
            elif value > ceiling:
                errors.append(f"token budget exceeded: {key} {value} > {ceiling}")
    return errors, metrics, manifest


def _normalized_sentences(root: Path):
    per_skill: dict[str, set[str]] = {}
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
        sync_names = "|".join(map(re.escape, SYNC_BLOCKS))
        text = re.sub(
            rf"<!-- tigerkit:(?!(?:{sync_names}) -->)[\w-]+ -->.*?(?=<!-- /?tigerkit:|\Z)",
            " ", text, flags=re.DOTALL,
        )
        for name in SYNC_BLOCKS:
            text = re.sub(
                rf"<!-- tigerkit:{re.escape(name)} -->.*?<!-- /tigerkit:{re.escape(name)} -->",
                " ", text, flags=re.DOTALL,
            )
        text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
        text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
        text = re.sub(r"https?://\S+", " ", text)
        text = re.sub(r"\[[^]]+\]\([^)]+\)", lambda match: match.group(0).split("]", 1)[0][1:], text)
        chunks = []
        for paragraph in re.split(r"\n\s*\n", text):
            stripped = paragraph.strip()
            if not stripped or stripped.startswith(("#", "```")):
                continue
            if stripped.startswith(("- ", "* ", "+ ")):
                chunks.extend(line.strip() for line in stripped.splitlines())
            else:
                chunks.append(" ".join(line.strip() for line in stripped.splitlines()))
        sentences = set()
        for chunk in chunks:
            chunk = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", chunk)
            chunk = re.sub(r"[`*_>#]", "", chunk)
            for sentence in SENTENCE_SPLIT.split(chunk):
                normalized = " ".join(sentence.split()).strip(" -–—:;,.\t")
                if len(normalized) >= 60:
                    sentences.add(normalized.casefold())
        per_skill[path.relative_to(root).as_posix()] = sentences
    occurrences: dict[str, set[str]] = defaultdict(set)
    for skill_path, sentences in per_skill.items():
        for sentence in sentences:
            occurrences[sentence].add(skill_path)
    return {sentence: paths for sentence, paths in occurrences.items() if len(paths) > 1}


def compare_token_budget(baseline_root: Path, candidate_root: Path) -> list[str]:
    errors, candidate_metrics, candidate_manifest = static_errors(candidate_root)
    if errors:
        return errors
    baseline_has_manifest = (baseline_root / MANIFEST).is_file()
    if baseline_has_manifest:
        baseline_manifest, baseline_manifest_errors = load_manifest(baseline_root)
        if baseline_manifest_errors:
            errors.extend(baseline_manifest_errors)
            return errors
    else:
        baseline_manifest = {}
    baseline_metrics, metric_errors = collect_metrics(
        baseline_root,
        candidate_manifest,
        allow_missing_always_read=True,
        use_before_paths=not baseline_has_manifest,
    )
    errors.extend(metric_errors)
    rationales = candidate_manifest.get("rationales", {})
    ratio = candidate_manifest.get("max_growth_ratio", 0.1)
    if not isinstance(ratio, (int, float)) or ratio < 0:
        errors.append(f"{MANIFEST}: max_growth_ratio must be non-negative")
        ratio = 0.1
    for metric, value in candidate_metrics.items():
        before = baseline_metrics.get(metric, 0)
        if value > before * (1 + ratio) and not rationales.get(metric):
            errors.append(
                f"unexplained context growth: {metric} increased from {before} to {value}; "
                f"add a concise rationale under rationales.{metric}"
            )

    old_limits = baseline_manifest.get("limits", {})
    new_limits = candidate_manifest.get("limits", {})
    if isinstance(old_limits, dict) and isinstance(new_limits, dict):
        for key, new_value in new_limits.items():
            if key == "always_read" or not isinstance(new_value, int):
                continue
            old_value = old_limits.get(key)
            if isinstance(old_value, int) and new_value > old_value and not rationales.get(f"budget_increase:{key}"):
                errors.append(
                    f"budget ceiling increased without a rationale: {key} {old_value} -> {new_value}"
                )
        old_always = old_limits.get("always_read", {})
        new_always = new_limits.get("always_read", {})
        if isinstance(old_always, dict) and isinstance(new_always, dict):
            for group, spec in new_always.items():
                old_spec = old_always.get(group)
                if not isinstance(spec, dict) or not isinstance(old_spec, dict):
                    continue
                old_max, new_max = old_spec.get("max_bytes"), spec.get("max_bytes")
                key = f"always_read:{group}"
                if (isinstance(old_max, int) and isinstance(new_max, int) and new_max > old_max
                        and not rationales.get(f"budget_increase:{key}")):
                    errors.append(
                        f"budget ceiling increased without a rationale: {key} {old_max} -> {new_max}"
                    )
    if (candidate_manifest.get("max_growth_ratio", 0.1)
            > baseline_manifest.get("max_growth_ratio", 0.1)
            and not rationales.get("budget_increase:max_growth_ratio")):
        errors.append("budget ceiling increased without a rationale: max_growth_ratio")

    before_duplicates = _normalized_sentences(baseline_root)
    after_duplicates = _normalized_sentences(candidate_root)
    new_duplicates = sorted(set(after_duplicates) - set(before_duplicates))
    for sentence in new_duplicates:
        paths = ", ".join(sorted(after_duplicates[sentence]))
        errors.append(f"new duplicate skill sentence in {paths}: {sentence}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check static ceilings only")
    parser.add_argument("--baseline", help="compare growth and new duplicate sentences with a baseline worktree")
    parser.add_argument("--candidate", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    candidate = args.candidate.resolve()
    if args.baseline:
        baseline = Path(args.baseline).resolve()
        errors = compare_token_budget(baseline, candidate)
    else:
        errors, _, _ = static_errors(candidate)
    if errors:
        print("\n".join(f"FAIL {error}" for error in errors), file=sys.stderr)
        return 1
    print("Static skill context budgets and baseline growth: Pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
