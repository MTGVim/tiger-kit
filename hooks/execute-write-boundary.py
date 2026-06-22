#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import json
import os
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"TigerKit execute boundary: cannot read boundary file: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("TigerKit execute boundary: boundary file must be object")
    return data


def norm_repo_rel(repo_root: Path, value: str) -> tuple[str, Path]:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    resolved = path.resolve(strict=False)
    try:
        rel = resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        raise SystemExit(f"TigerKit execute boundary: path outside repo: {value}")
    return rel, resolved


def path_matches(path: str, patterns: list[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatch(path, pattern) for pattern in patterns)


def tool_name(payload: dict[str, Any]) -> str:
    for key in ("tool_name", "tool", "name"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def classify_operation(repo_root: Path, tool: str, tool_input: dict[str, Any], raw_path: str) -> str:
    explicit = tool_input.get("operation")
    if explicit in {"create", "modify", "delete"}:
        return str(explicit)
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    if tool == "Write":
        return "modify" if path.exists() else "create"
    return "modify"


def extract_path_operations(repo_root: Path, payload: dict[str, Any]) -> list[tuple[str, str]]:
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if not isinstance(tool_input, dict):
        return []
    tool = tool_name(payload)
    paths: list[tuple[str, str]] = []
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.append((value, classify_operation(repo_root, tool, tool_input, value)))
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict):
                value = edit.get("file_path") or edit.get("path")
                if isinstance(value, str):
                    paths.append((value, classify_operation(repo_root, tool, tool_input, value)))
    return paths


def main() -> int:
    boundary_path = os.environ.get("TIGERKIT_EXECUTE_BOUNDARY_FILE")
    if not boundary_path:
        return 0
    boundary = load_json(Path(boundary_path).expanduser())
    repo_root = Path(str(boundary.get("repoRoot") or os.getcwd())).expanduser().resolve()
    modify = [str(x) for x in boundary.get("modify") or []]
    create = [str(x) for x in boundary.get("create") or []]
    delete = [str(x) for x in boundary.get("delete") or []]
    exclude = [str(x) for x in boundary.get("exclude") or []]
    payload = json.loads(sys.stdin.read() or "{}")
    for raw_path, operation in extract_path_operations(repo_root, payload):
        rel, _ = norm_repo_rel(repo_root, raw_path)
        if path_matches(rel, exclude):
            print(f"TigerKit execute boundary rejected excluded {operation} path: {rel}", file=sys.stderr)
            return 2
        if operation == "modify" and not path_matches(rel, modify):
            print(f"TigerKit execute boundary rejected out-of-scope modify path: {rel}", file=sys.stderr)
            return 2
        if operation == "create" and rel not in create:
            print(f"TigerKit execute boundary rejected undeclared create path: {rel}", file=sys.stderr)
            return 2
        if operation == "delete" and rel not in delete:
            print(f"TigerKit execute boundary rejected undeclared delete path: {rel}", file=sys.stderr)
            return 2
        if operation not in {"create", "modify", "delete"}:
            print(f"TigerKit execute boundary rejected unknown operation for path: {rel}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
