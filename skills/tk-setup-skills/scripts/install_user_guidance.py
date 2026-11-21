#!/usr/bin/env python3
"""Install TigerKit-owned user guidance without overwriting unrelated instructions."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tempfile
import time

SHARED_START = "<!-- MTGVIM_SHARED_AGENT_BASE_START -->"
SHARED_END = "<!-- MTGVIM_SHARED_AGENT_BASE_END -->"
LEGACY_START = "<!-- MTGVIM_FLUENT_KOREAN_START -->"
LEGACY_END = "<!-- MTGVIM_FLUENT_KOREAN_END -->"


def marker_range(text: str, start: str, end: str) -> tuple[int, int] | None:
    if text.count(start) != text.count(end) or text.count(start) > 1:
        raise ValueError("unbalanced or duplicate managed markers")
    if start not in text:
        return None
    i = text.index(start)
    j = text.index(end)
    if j <= i:
        raise ValueError("managed markers in the wrong order")
    return i, j + len(end)


def updated_text(original: str, body: str) -> str:
    shared = marker_range(original, SHARED_START, SHARED_END)
    legacy = marker_range(original, LEGACY_START, LEGACY_END)
    if shared and legacy and max(shared[0], legacy[0]) < min(shared[1], legacy[1]):
        raise ValueError("overlapping managed marker ranges")

    text = original
    if legacy:
        text = text[:legacy[0]] + text[legacy[1]:]
    shared = marker_range(text, SHARED_START, SHARED_END)
    replacement = SHARED_START + "\n" + body.rstrip() + "\n" + SHARED_END
    if shared:
        return text[:shared[0]] + replacement + text[shared[1]:]
    separator = "\n\n" if text.strip() else ""
    return text.rstrip("\n") + separator + replacement + "\n"


def safe_target(home: Path, target: Path) -> None:
    if not target.is_relative_to(home):
        raise ValueError("target escapes user home")
    cursor = target
    while cursor != home:
        if cursor.is_symlink():
            raise ValueError("symlink target or parent is not supported")
        cursor = cursor.parent
    if target.exists() and not target.is_file():
        raise ValueError("target is not a regular file")


def atomic_write(target: Path, content: bytes, original: bytes | None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if (target.read_bytes() if target.exists() else None) != original:
        raise ValueError("target changed since preflight")
    if original is not None:
        backup = target.with_name(target.name + ".bak-" + str(time.time_ns()))
        shutil.copy2(target, backup)
        print("backup:", backup)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".user-guidance-", delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if original is not None:
            tmp.chmod(target.stat().st_mode & 0o777)
        tmp.replace(target)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Install user guidance into selected agent files")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="show changes without writing (default)")
    mode.add_argument("--apply", action="store_true", help="backup and write approved changes")
    parser.add_argument("--agent", choices=("all", "claude-code", "codex", "hermes-agent"),
                        default="all", help="target one agent or all")
    args = parser.parse_args()

    home = Path.home().absolute()
    source = Path(__file__).resolve().parent.parent / "references" / "user-guidance.md"
    body = source.read_text(encoding="utf-8")
    options = {
        "claude-code": home / ".claude" / "CLAUDE.md",
        "codex": home / ".codex" / "AGENTS.md",
        "hermes-agent": home / ".hermes" / "SOUL.md",
    }
    selected = list(options) if args.agent == "all" else [args.agent]
    pending: list[tuple[Path, bytes | None, bytes]] = []
    # Preflight all selected files before modifying any of them.
    for agent in selected:
        target = options[agent]
        safe_target(home, target)
        if agent == "hermes-agent" and not target.is_file():
            print("skipped (SOUL.md not configured):", target)
            continue
        original = target.read_bytes() if target.exists() else None
        current = original.decode("utf-8") if original is not None else ""
        changed = updated_text(current, body).encode("utf-8")
        if changed == original:
            print("unchanged:", target)
        else:
            pending.append((target, original, changed))

    for target, original, changed in pending:
        if args.apply:
            safe_target(home, target)
            atomic_write(target, changed, original)
            print("updated:", target)
        else:
            print("would update:", target)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, UnicodeError) as exc:
        raise SystemExit("refusing user-guidance installation: " + str(exc))
