#!/usr/bin/env python3
"""Validate the shared compact progress-output contract."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "Progress is optional and nonterminal:"
MARKERS = ("🚗", "🙋", "⏳")
LEGACY = ("⚙️", "🧹", "👤", "👀", "❓", "🛑", "✅", "❌", "⏳ Waiting")


def _validate_markers(label: str, text: str, *, require_all: bool = False) -> list[str]:
    errors: list[str] = []
    for marker in MARKERS:
        if require_all and f"{marker} " not in text:
            errors.append(f"{label}: missing spaced progress marker {marker!r}")
        for match in re.finditer(re.escape(marker), text):
            index = match.start()
            if index and text[index - 1] == "`" and index + 1 < len(text) and text[index + 1] == "`":
                continue
            suffix = text[index + len(marker):]
            if not suffix.startswith(" ") or suffix.startswith("  "):
                errors.append(f"{label}: progress marker {marker!r} must be followed by one space")
                break
    for token in LEGACY:
        for match in re.finditer(re.escape(token), text):
            line = text.count("\n", 0, match.start()) + 1
            line_text = text.splitlines()[line - 1] if text.splitlines() else ""
            if token == "🛑" and "CHECKPOINT" in line_text:
                continue
            errors.append(f"{label}: legacy progress marker {token!r} remains")
            break
    for legacy_route in ("🤖 drive", "🤖 sweep", "🤖 respond", "🤖 browser-verify"):
        if legacy_route in text:
            errors.append(f"{label}: legacy progress route {legacy_route!r} remains")
    return errors


def validate_skill_text(label: str, text: str) -> list[str]:
    errors = _validate_markers(label, text, require_all=False)
    if text.count(CANONICAL) > 1:
        errors.append(f"{label}: shared progress contract may appear at most once")
    return errors


def validate_all(root: Path = ROOT) -> list[str]:
    paths = sorted((root / "skills").glob("tk-*/SKILL.md"))
    if not paths:
        return ["skills: no tk-* SKILL.md files found"]
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_skill_text(str(path.relative_to(root)), path.read_text(encoding="utf-8")))
        for reference in sorted(path.parent.glob("references/**/*.md")):
            errors.extend(_validate_markers(str(reference.relative_to(root)), reference.read_text(encoding="utf-8"), require_all=False))
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"progress contract: Pass ({len(list((ROOT / 'skills').glob('tk-*/SKILL.md')))} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
