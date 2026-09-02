#!/usr/bin/env python3
"""Audit the TigerKit catalog from canonical skill-local contracts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import validate_skills

ROOT = Path(__file__).resolve().parents[1]
README_SKILL_ROW = re.compile(r"^\|\s*`(tk-[a-z0-9-]+)`\s*\|")


def positive_trigger_count(skill_dir: Path) -> int:
    value = json.loads((skill_dir / "evals/triggers.json").read_text(encoding="utf-8"))
    rows = value.get("queries", [])
    if not isinstance(rows, list):
        return 0
    return sum(
        isinstance(row, dict) and row.get("should_trigger") is True
        for row in rows
    )


def behavior_paths(skill_dir: Path) -> set[str]:
    value = json.loads((skill_dir / "evals/evals.json").read_text(encoding="utf-8"))
    rows = value.get("evals", [])
    if not isinstance(rows, list):
        return set()
    return {
        str(row.get("path"))
        for row in rows
        if isinstance(row, dict) and row.get("path")
    }


def readme_skill_rows(root: Path = ROOT) -> list[str]:
    path = root / "README.md"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return []

    inside = False
    fenced = False
    comment = False
    table = False
    separator = False
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        if comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                comment = False
            else:
                continue
        while "<!--" in line:
            before, after = line.split("<!--", 1)
            if "-->" in after:
                line = before + after.split("-->", 1)[1]
            else:
                line = before
                comment = True
                break
        stripped = line.strip()

        if stripped == "## 스킬 구성":
            inside = True
            continue
        if inside and stripped.startswith("## "):
            break
        if not inside:
            continue
        if not table:
            if stripped.startswith("| 스킬 |"):
                table = True
            continue
        if not separator:
            if re.match(r"^\|\s*:?-{3,}", stripped):
                separator = True
            elif stripped:
                table = False
            continue
        if not stripped:
            break
        if stripped and not stripped.startswith("|"):
            break
        if match := README_SKILL_ROW.match(stripped):
            result.append(match.group(1))
    return result


def readme_skill_names(root: Path = ROOT) -> set[str]:
    return set(readme_skill_rows(root))


def readme_catalog_parity(
    skill_names: set[str], root: Path = ROOT
) -> dict[str, list[str]]:
    rows = readme_skill_rows(root)
    documented = set(rows)
    duplicates = sorted(name for name in documented if rows.count(name) != 1)
    return {
        "missing": sorted(skill_names - documented),
        "stale": sorted(documented - skill_names),
        "duplicates": duplicates,
    }


def catalog_consumers(skill_names: set[str]) -> dict[str, set[str]]:
    value = json.loads((ROOT / "evals/catalog-routing.json").read_text(encoding="utf-8"))
    result = {name: set() for name in skill_names}
    rows = value.get("cases", [])
    if not isinstance(rows, list):
        return result
    for row in rows:
        if not isinstance(row, dict):
            continue
        boundary = str(row.get("boundary", ""))
        for field in ("focus_skill", "expected_selected_skill"):
            skill = row.get(field)
            if isinstance(skill, str) and skill in result:
                result[skill].add(boundary)
    return result


def audit() -> dict[str, object]:
    skills = validate_skills.discover_skills()
    names = set(skills)
    catalog = catalog_consumers(names)
    readme_parity = readme_catalog_parity(names)
    rows: list[dict[str, object]] = []

    for name, (skill_dir, data, _) in sorted(skills.items()):
        kind = validate_skills.nested(data, "metadata", "tigerkit", "kind")
        triggers = positive_trigger_count(skill_dir)
        paths = behavior_paths(skill_dir)
        consumers = sorted(catalog[name])

        independent = kind == "user-invoked" or triggers > 0
        objective = {"success", "boundary"}.issubset(paths)
        # 명시 user skill은 자체 invocation이 consumer다. hybrid는 positive routing
        # evidence 또는 catalog boundary가 필요하다.
        referenced = kind == "user-invoked" or bool(consumers) or triggers > 0

        disposition = (
            "ContractComplete"
            if independent and objective and referenced
            else "Review"
        )
        basis: list[str] = []
        if kind == "user-invoked":
            basis.append("explicit independent invocation")
        if triggers:
            basis.append(f"{triggers} positive trigger cases")
        if objective:
            basis.append("success and boundary behavior")
        if consumers:
            basis.append(f"{len(consumers)} catalog boundaries")

        rows.append(
            {
                "skill": name,
                "kind": kind,
                "disposition": disposition,
                "positive_triggers": triggers,
                "behavior_paths": sorted(paths),
                "catalog_consumers": consumers,
                "basis": basis,
            }
        )

    review = [
        str(row["skill"])
        for row in rows
        if row["disposition"] != "ContractComplete"
    ]
    parity_ok = not any(readme_parity.values())
    return {
        "status": "Pass" if not review and parity_ok else "Review",
        "skill_count": len(rows),
        "contract_complete_count": len(rows) - len(review),
        "review": review,
        "readme_catalog": readme_parity,
        "skills": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = audit()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if args.check and result["status"] != "Pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
