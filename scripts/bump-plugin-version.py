#!/usr/bin/env python3
"""Bump .claude-plugin/plugin.json version from an origin/main baseline.

Usage:
  python3 scripts/bump-plugin-version.py --part patch
  python3 scripts/bump-plugin-version.py 8.0.1
  python3 scripts/bump-plugin-version.py --dry-run --part minor

By default, calculated bumps use origin/main:.claude-plugin/plugin.json as the
baseline so stale local branches do not accidentally reuse an old version. Use
--base local only for offline/manual repair workflows.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / ".claude-plugin" / "plugin.json"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_version(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value)
    if not match:
        raise SystemExit(f"Expected plain semver MAJOR.MINOR.PATCH, got {value!r}")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def load_local_plugin() -> dict:
    return json.loads(PLUGIN_PATH.read_text())


def load_origin_plugin() -> dict:
    result = subprocess.run(
        ["git", "show", "origin/main:.claude-plugin/plugin.json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "Could not read origin/main:.claude-plugin/plugin.json. "
            "Run `git fetch origin` first or pass --base local for an explicit offline bump.\n"
            + result.stderr.strip()
        )
    return json.loads(result.stdout)


def bump_version(base: tuple[int, int, int], part: str) -> tuple[int, int, int]:
    major, minor, patch = base
    if part == "major":
        return major + 1, 0, 0
    if part == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def version_text(version: tuple[int, int, int]) -> str:
    return f"{version[0]}.{version[1]}.{version[2]}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", nargs="?", help="Explicit version, e.g. 8.0.1")
    parser.add_argument("--part", choices=["major", "minor", "patch"], default="patch")
    parser.add_argument("--base", choices=["origin-main", "local"], default="origin-main")
    parser.add_argument("--dry-run", action="store_true", help="Print the version change without writing plugin.json")
    args = parser.parse_args()

    local_plugin = load_local_plugin()
    local_raw = local_plugin.get("version")
    if not isinstance(local_raw, str):
        raise SystemExit("plugin.json is missing string version")
    local_version = parse_version(local_raw)

    if args.base == "origin-main":
        origin_raw = load_origin_plugin().get("version")
        if not isinstance(origin_raw, str):
            raise SystemExit("origin/main plugin.json is missing string version")
        base_raw = origin_raw
        base_version = parse_version(origin_raw)
    else:
        base_raw = local_raw
        base_version = local_version

    if args.version:
        new_raw = args.version
        new_version = parse_version(new_raw)
    else:
        new_version = bump_version(base_version, args.part)
        new_raw = version_text(new_version)

    if args.base == "origin-main" and new_version <= base_version:
        raise SystemExit(f"New version {new_raw} must be greater than origin/main version {base_raw}")

    if args.dry_run:
        print(f"base({args.base}) {base_raw}; local {local_raw}; new {new_raw}; dry-run")
        return 0

    local_plugin["version"] = new_raw
    PLUGIN_PATH.write_text(json.dumps(local_plugin, ensure_ascii=False, indent=2) + "\n")
    print(f"base({args.base}) {base_raw}; local {local_raw} -> {new_raw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
