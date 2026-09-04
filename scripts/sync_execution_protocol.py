#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-prep/references"
TARGET = ROOT / "skills/tk-pr-respond/references"
FILES = ("testing.md", "sdd.md", "diagnosis.md", "test-doubles.md")
REVIEW_SOURCE = ROOT / "skills/tk-review/references"
REVIEW_TARGETS = (
    ROOT / "skills/tk-prep/references",
    ROOT / "skills/tk-pr-respond/references",
)
REVIEW_FILES = (
    "review-protocol.md",
    "finding-quality.md",
    "typescript.md",
    "react.md",
    "security.md",
)
EXTERNAL_CONTRACT_SOURCE = ROOT / "skills/tk-prep/references/external-contracts.md"
EXTERNAL_CONTRACT_TARGET = ROOT / "skills/tk-wizard/references/external-contracts.md"
DOMAIN_CONTEXT_TARGETS = (
    ROOT / "skills/tk-ask-repo/references/domain-context.md",
    ROOT / "skills/tk-audit/references/domain-context.md",
    ROOT / "skills/tk-pr-open/references/domain-context.md",
    ROOT / "skills/tk-pr-respond/references/domain-context.md",
    ROOT / "skills/tk-review/references/domain-context.md",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    pairs = [(SOURCE / name, TARGET / name) for name in FILES]
    pairs.extend((SOURCE / "domain-context.md", target) for target in DOMAIN_CONTEXT_TARGETS)
    pairs.extend(
        (REVIEW_SOURCE / name, target / name)
        for target in REVIEW_TARGETS
        for name in REVIEW_FILES
    )
    pairs.append((EXTERNAL_CONTRACT_SOURCE, EXTERNAL_CONTRACT_TARGET))
    drift = [
        (source, target)
        for source, target in pairs
        if not target.is_file() or target.read_bytes() != source.read_bytes()
    ]
    if args.check:
        if drift:
            print(
                "Out-of-sync shared reference copies: "
                + ", ".join(str(target.relative_to(ROOT)) for _, target in drift)
            )
            return 1
        print("Shared reference copies are synchronized.")
        return 0
    for source, target in drift:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    print(
        "Synchronized: "
        + (", ".join(str(target.relative_to(ROOT)) for _, target in drift) if drift else "no changes")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
