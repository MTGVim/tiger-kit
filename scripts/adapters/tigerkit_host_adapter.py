#!/usr/bin/env python3
"""Run one TigerKit eval through the selected host CLI and normalize its result."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

MARKER_START = "<!-- TIGERKIT_EVAL_RESULT_START -->"
MARKER_END = "<!-- TIGERKIT_EVAL_RESULT_END -->"
TERMINAL_STATUSES = {
    "Pass",
    "Fail",
    "Blocked",
    "Unverifiable",
    "Pending",
    "NotApplicable",
}


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing {name}")
    return value


def executable_for(host: str) -> str:
    candidates = {
        "codex": ("codex",),
        "claude-code": ("claude",),
        "hermes-agent": ("hermes",),
    }.get(host)
    if candidates is None:
        raise RuntimeError(f"unsupported host {host}")
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise RuntimeError(f"{host} executable unavailable")


def install_skills(host: str, checkout: Path) -> list[str]:
    source = checkout / "skills"
    homes = {
        "codex": Path(require_env("CODEX_HOME")) / "skills",
        "claude-code": Path(require_env("CLAUDE_CONFIG_DIR")) / "skills",
        "hermes-agent": Path(require_env("HERMES_HOME")) / "skills",
    }
    target = homes[host]
    target.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for skill_dir in sorted(source.glob("tk-*")):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        destination = target / skill_dir.name
        shutil.copytree(skill_dir, destination, dirs_exist_ok=True)
        installed.append(skill_dir.name)
    return installed


def harness_prompt(prompt: str, installed: Iterable[str]) -> str:
    installed_json = json.dumps(list(installed), ensure_ascii=False)
    return f"""You are running an isolated TigerKit behavior evaluation.
Use the repository and installed Agent Skills normally. Perform the user's task; do not merely describe it.
At the very end, emit exactly one marker-delimited JSON object and no prose after it.

{MARKER_START}
{{
  "output": "the terminal user-facing result without this envelope",
  "terminal_status": "Pass | Fail | Blocked | Unverifiable | Pending | NotApplicable",
  "selected_skill": "one selected skill name or null",
  "loaded_skills": ["every TigerKit skill actually loaded"],
  "events": [
    {{"type": "phase_invocation", "phase": "skill or internal phase actually invoked"}},
    {{"type": "final_output", "terminal_status": "same terminal status"}}
  ]
}}
{MARKER_END}

Do not claim a skill or phase was loaded or invoked unless it actually was. The installed catalog is {installed_json}.

USER TASK:
{prompt}
"""


def run_process(command: list[str], *, cwd: Path) -> tuple[str, str, int, float]:
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=900,
    )
    duration_ms = round((time.monotonic() - started) * 1000)
    return completed.stdout, completed.stderr, completed.returncode, duration_ms


def codex_text(stdout: str) -> tuple[str, float | None]:
    messages: list[str] = []
    tokens: float | None = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        item = event.get("item")
        if event.get("type") == "item.completed" and isinstance(item, dict):
            if item.get("type") in {"agent_message", "assistant_message"}:
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    messages.append(text)
        usage = event.get("usage")
        if isinstance(usage, dict):
            value = usage.get("total_tokens")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                tokens = float(value)
    return "\n".join(messages) if messages else stdout, tokens


def claude_text(stdout: str) -> tuple[str, float | None]:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError:
        return stdout, None
    if not isinstance(value, dict):
        return stdout, None
    result = value.get("result")
    usage = value.get("usage")
    tokens: float | None = None
    if isinstance(usage, dict):
        total = usage.get("input_tokens", 0)
        output = usage.get("output_tokens", 0)
        if all(isinstance(item, (int, float)) and not isinstance(item, bool) for item in (total, output)):
            tokens = float(total) + float(output)
    return result if isinstance(result, str) else stdout, tokens


def extract_payload(text: str) -> dict[str, object]:
    if text.count(MARKER_START) != 1 or text.count(MARKER_END) != 1:
        raise RuntimeError("host output omitted the TigerKit eval result envelope")
    raw = text.split(MARKER_START, 1)[1].split(MARKER_END, 1)[0].strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"malformed TigerKit eval result envelope: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("TigerKit eval result envelope must be an object")
    output = payload.get("output")
    status = payload.get("terminal_status")
    selected = payload.get("selected_skill")
    loaded = payload.get("loaded_skills")
    events = payload.get("events")
    if not isinstance(output, str):
        raise RuntimeError("eval envelope requires string output")
    if status not in TERMINAL_STATUSES:
        raise RuntimeError("eval envelope requires a canonical terminal_status")
    if selected is not None and not isinstance(selected, str):
        raise RuntimeError("eval envelope selected_skill must be string or null")
    if not isinstance(loaded, list) or not all(isinstance(value, str) for value in loaded):
        raise RuntimeError("eval envelope loaded_skills must be a string list")
    if not isinstance(events, list) or not all(isinstance(value, dict) for value in events):
        raise RuntimeError("eval envelope events must be an object list")
    return payload


def main() -> int:
    host = require_env("TK_EVAL_HOST")
    prompt = require_env("TK_EVAL_PROMPT")
    checkout = Path.cwd()
    executable = executable_for(host)
    installed = install_skills(host, checkout)
    wrapped = harness_prompt(prompt, installed)

    if host == "codex":
        command = [
            executable,
            "exec",
            "--json",
            "--ephemeral",
            "--full-auto",
            "--skip-git-repo-check",
            wrapped,
        ]
    elif host == "claude-code":
        command = [
            executable,
            "-p",
            wrapped,
            "--output-format",
            "json",
            "--max-turns",
            "40",
            "--dangerously-skip-permissions",
        ]
    else:
        command = [
            executable,
            "chat",
            "-q",
            wrapped,
            "--toolsets",
            "terminal,skills",
            "--ignore-user-config",
        ]

    stdout, stderr, returncode, duration_ms = run_process(command, cwd=checkout)
    if returncode != 0:
        raise RuntimeError(stderr.strip() or stdout.strip() or f"{host} exited {returncode}")
    if host == "codex":
        text, total_tokens = codex_text(stdout)
    elif host == "claude-code":
        text, total_tokens = claude_text(stdout)
    else:
        text, total_tokens = stdout, None
    payload = extract_payload(text)
    payload["duration_ms"] = duration_ms
    payload["total_tokens"] = total_tokens
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
