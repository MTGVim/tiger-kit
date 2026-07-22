#!/usr/bin/env python3
"""Regenerate Darwin test-prompts.json projections from canonical eval contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_skills import ROOT, darwin_test_prompt_projection


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write projections instead of checking")
    args = parser.parse_args()
    changed: list[str] = []
    for skill_dir in sorted((ROOT / "skills").glob("tk-*")):
        source = skill_dir / "evals" / "evals.json"
        target = skill_dir / "test-prompts.json"
        behavior = json.loads(source.read_text(encoding="utf-8"))
        projection = darwin_test_prompt_projection(behavior)
        rendered = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current == rendered:
            continue
        changed.append(skill_dir.name)
        if args.write:
            target.write_text(rendered, encoding="utf-8")
    if changed and not args.write:
        print("Out-of-date Darwin projections: " + ", ".join(changed))
        return 1
    action = "Updated" if args.write else "Validated"
    print(f"{action} Darwin eval projections for 12 skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
