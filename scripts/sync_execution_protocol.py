#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-prep"
TARGET = ROOT / "skills/tk-pr-respond"
FILES = (
    Path("references/testing.md"),
    Path("references/sdd.md"),
    Path("scripts/sdd-unit-brief.py"),
    Path("scripts/sdd-review-package.py"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = [
        relative
        for relative in FILES
        if not (TARGET / relative).is_file()
        or (TARGET / relative).read_bytes() != (SOURCE / relative).read_bytes()
        or (TARGET / relative).stat().st_mode & 0o111 != (SOURCE / relative).stat().st_mode & 0o111
    ]
    if args.check:
        if drift:
            print("Out-of-sync shared execution protocol: " + ", ".join(str(path) for path in drift))
            return 1
        print("Shared execution protocol copies are synchronized.")
        return 0
    for relative in drift:
        target = TARGET / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / relative, target)
    print("Synchronized: " + (", ".join(str(path) for path in drift) if drift else "no changes"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
