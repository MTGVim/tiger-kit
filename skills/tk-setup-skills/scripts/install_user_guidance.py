#!/usr/bin/env python3
"""Install TigerKit-owned user guidance without overwriting unrelated instructions."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tempfile
import time

SHARED_START = "<!-- TIGERKIT_USER_GUIDANCE_BEGIN -->"
SHARED_END = "<!-- TIGERKIT_USER_GUIDANCE_END -->"
OLD_SHARED_START = "<!-- MTGVIM_SHARED_AGENT_BASE_START -->"
OLD_SHARED_END = "<!-- MTGVIM_SHARED_AGENT_BASE_END -->"
ROUTE_START = "<!-- TIGERKIT_ROUTE_MODE_BEGIN -->"
ROUTE_END = "<!-- TIGERKIT_ROUTE_MODE_END -->"
OLD_ROUTE_START = "<!-- route-mode:begin -->"
OLD_ROUTE_END = "<!-- route-mode:end -->"
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


def managed_spans(text: str) -> dict[str, tuple[str, tuple[int, int]] | None]:
    """Find managed regions and refuse partial, duplicate, mixed or overlapping markers."""
    candidates = {
        "user-guidance": (("current", SHARED_START, SHARED_END),
                          ("old", OLD_SHARED_START, OLD_SHARED_END)),
        "route-mode": (("current", ROUTE_START, ROUTE_END),
                       ("old", OLD_ROUTE_START, OLD_ROUTE_END)),
        "fluent-korean": (("old", LEGACY_START, LEGACY_END),),
    }
    found: dict[str, tuple[str, tuple[int, int]] | None] = {}
    for name, versions in candidates.items():
        matches = [(kind, span) for kind, begin, end in versions
                   if (span := marker_range(text, begin, end)) is not None]
        if len(matches) > 1:
            raise ValueError(f"mixed or duplicate managed markers: {name}")
        found[name] = matches[0] if matches else None
    active = [(name, entry[1]) for name, entry in found.items() if entry]
    for i, (left, (a, b)) in enumerate(active):
        for right, (c, d) in active[i + 1:]:
            if max(a, c) < min(b, d):
                raise ValueError(f"overlapping managed regions: {left}, {right}")
    return found


def migrate_route_markers(text: str) -> str:
    route = managed_spans(text)["route-mode"]
    if route is None or route[0] == "current":
        return text
    _, (a, b) = route
    original = text[a:b]
    replacement = original.replace(OLD_ROUTE_START, ROUTE_START, 1).replace(
        OLD_ROUTE_END, ROUTE_END, 1)
    return text[:a] + replacement + text[b:]


def updated_text(original: str, body: str, *, migrate_route: bool = False) -> str:
    spans = managed_spans(original)
    text = original
    fluent = spans["fluent-korean"]
    if fluent:
        a, b = fluent[1]
        text = text[:a] + text[b:]

    guidance = managed_spans(text)["user-guidance"]
    replacement = SHARED_START + "\n" + body.rstrip() + "\n" + SHARED_END
    if guidance:
        a, b = guidance[1]
        text = text[:a] + replacement + text[b:]
    else:
        separator = "\n\n" if text.strip() else ""
        text = text.rstrip("\n") + separator + replacement + "\n"

    if migrate_route:
        text = migrate_route_markers(text)
    managed_spans(text)
    return text


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
    parser.add_argument("--migrate-route-mode", action="store_true",
                        help="also migrate legacy route-mode marker names without changing their content")
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
        if agent in ("claude-code", "codex") and not target.parent.is_dir():
            print(f"skipped ({agent} not configured):", target)
            continue
        if agent == "hermes-agent" and not target.is_file():
            print("skipped (SOUL.md not configured):", target)
            continue
        original = target.read_bytes() if target.exists() else None
        current = original.decode("utf-8") if original is not None else ""
        found = managed_spans(current)
        guidance = found["user-guidance"]
        if guidance and guidance[0] == "old":
            print("user-guidance marker migration proposed:", target)
        if found["fluent-korean"]:
            print("legacy fluent-korean block removal proposed:", target)
        route = found["route-mode"]
        if route and route[0] == "old":
            if args.migrate_route_mode:
                print(("migrating" if args.apply else "would migrate") + " route-mode markers:", target)
            else:
                print("route-mode marker migration available (requires --migrate-route-mode):", target)
        changed = updated_text(current, body, migrate_route=args.migrate_route_mode).encode("utf-8")
        if changed == original:
            print("unchanged:", target)
        else:
            pending.append((target, original, changed))

    for target, original, changed in pending:
        if args.apply:
            safe_target(home, target)
            atomic_write(target, changed, original)
            print("created:" if original is None else "updated:", target)
        else:
            print("would create:" if original is None else "would update:", target)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, UnicodeError) as exc:
        raise SystemExit("refusing user-guidance installation: " + str(exc))
