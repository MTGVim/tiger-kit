#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS_DIR = ROOT / "commands"
OUT_PATH = ROOT / "docs" / "help-map.json"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [item.strip().strip('"\'') for item in inner.split(",") if item.strip()]
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data


def command_entry(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    command = f"/tk:{path.stem}"
    flow = frontmatter.get("flow")
    if not isinstance(flow, list):
        flow = []
    return {
        "command": command,
        "path": f"commands/{path.name}",
        "description": frontmatter.get("description", ""),
        "argument_hint": frontmatter.get("argument-hint", ""),
        "flow": [f"/tk:{item}" if not str(item).startswith("/tk:") else str(item) for item in flow],
    }


def main() -> int:
    commands = [command_entry(path) for path in sorted(COMMANDS_DIR.glob("*.md"))]
    payload = {
        "schemaVersion": "tigerkit.help-map/v1",
        "source": "commands/*.md frontmatter",
        "commands": commands,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(OUT_PATH.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
