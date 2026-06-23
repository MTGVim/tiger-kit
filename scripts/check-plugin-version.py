#!/usr/bin/env python3
"""Validate TigerKit plugin version and command manifest invariants.

The authoritative plugin version lives in .claude-plugin/plugin.json.
This script intentionally avoids hard-coded release numbers so patch/minor
bumps do not require eval rewrites.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
SUPPORT_MATRIX_PATH = ROOT / "support" / "execute-support-matrix.json"
EVALS_PATH = ROOT / "evals" / "evals.json"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # pragma: no cover - CLI diagnostic
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc


def fail(message: str) -> None:
    raise SystemExit(f"plugin version check failed: {message}")


def main() -> int:
    plugin = load_json(PLUGIN_PATH)
    marketplace = load_json(MARKETPLACE_PATH)
    support_matrix = load_json(SUPPORT_MATRIX_PATH)
    evals = load_json(EVALS_PATH)

    version = plugin.get("version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        fail(f".claude-plugin/plugin.json version must be semver, got {version!r}")

    commands = plugin.get("commands")
    if not isinstance(commands, list) or not commands:
        fail("plugin commands must be a non-empty list")

    seen: set[str] = set()
    for command in commands:
        if not isinstance(command, str):
            fail(f"command entry must be a string, got {command!r}")
        if command in seen:
            fail(f"duplicate command entry: {command}")
        seen.add(command)
        command_path = (ROOT / command).resolve()
        if ROOT not in command_path.parents:
            fail(f"command path escapes repo: {command}")
        if not command_path.exists():
            fail(f"command path does not exist: {command}")

    plugin_name = plugin.get("name")
    marketplace_plugins = marketplace.get("plugins")
    if not isinstance(marketplace_plugins, list) or not marketplace_plugins:
        fail("marketplace plugins must be a non-empty list")
    if not any(item.get("name") == plugin_name and item.get("source") == "./" for item in marketplace_plugins if isinstance(item, dict)):
        fail(f"marketplace.json must expose plugin {plugin_name!r} with source './'")

    support_version = support_matrix.get("pluginVersion")
    if support_version != version:
        fail(f"support/execute-support-matrix.json pluginVersion {support_version!r} must match plugin version {version!r}")

    command_set = set(commands)
    expected_active = {
        "./commands/gap.md",
        "./commands/route.md",
        "./commands/reflect.md",
    }
    if command_set != expected_active:
        fail(f"plugin commands must be exactly {sorted(expected_active)!r}, got {sorted(command_set)!r}")

    eval_text = EVALS_PATH.read_text()
    if re.search(r"Version is \d+\.\d+\.\d+", eval_text):
        fail(
            "evals/evals.json hard-codes a plugin version; "
            "assert version format/policy instead so future bumps work"
        )
    if "plugin-version-and-command-manifest" not in eval_text:
        fail("evals/evals.json must include a plugin version/manifest invariant eval")

    print(f"plugin version ok: {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
