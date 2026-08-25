#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-prep/references"
TARGET = ROOT / "skills/tk-pr-respond/references"
FILES = ("testing.md", "sdd.md", "diagnosis.md", "test-doubles.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = [
        name
        for name in FILES
        if not (TARGET / name).is_file()
        or (TARGET / name).read_bytes() != (SOURCE / name).read_bytes()
    ]
    if args.check:
        if drift:
            print("Out-of-sync shared execution protocol: " + ", ".join(drift))
            return 1
        print("Shared execution protocol copies are synchronized.")
        return 0
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in drift:
        shutil.copyfile(SOURCE / name, TARGET / name)
    print("Synchronized: " + (", ".join(drift) if drift else "no changes"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
