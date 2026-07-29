#!/usr/bin/env python3
"""Run one tk-drive eval through Codex app-server's explicit skill input."""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
from collections import deque
from pathlib import Path
from typing import IO, Mapping


TERMINAL_STATUSES = ("Pass", "Pending", "Blocked", "Fail", "Unverifiable")
EVENT_TYPES = {"phase_invocation", "phase_receipt"}
PHASES = {
    "tk-grill-me",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-implement",
    "tk-reflect",
}
SUCCESS_STATES = {"Ready", "confirmed", "Pass"}
STATUS_PATTERN = re.compile(
    r"(?m)^[ \t]*(?:[-*][ \t]+)?Status:[ \t]*"
    r"(Pass|Pending|Blocked|Fail|Unverifiable)[ \t]*$"
)


class CodexObservation:
    def __init__(self) -> None:
        self.output = ""
        self.total_tokens: int | None = None
        self.duration_ms: int | float | None = None
        self.tool_uses = 0
        self._seen_tool_items: set[str] = set()
        self.turn_failed = False

    def consume(self, message: Mapping[str, object]) -> None:
        method = message.get("method")
        params = message.get("params")
        if not isinstance(params, dict):
            return
        if method in {"item/started", "item/completed"}:
            item = params.get("item")
            if not isinstance(item, dict):
                return
            item_type = item.get("type")
            item_id = item.get("id")
            if (
                item_type != "agentMessage"
                and isinstance(item_id, str)
                and item_id not in self._seen_tool_items
            ):
                self._seen_tool_items.add(item_id)
                self.tool_uses += 1
            if method == "item/completed" and item_type == "agentMessage":
                text = item.get("text")
                if isinstance(text, str):
                    self.output = text
            return
        if method == "thread/tokenUsage/updated":
            token_usage = params.get("tokenUsage")
            total = token_usage.get("total") if isinstance(token_usage, dict) else None
            value = total.get("totalTokens") if isinstance(total, dict) else None
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                self.total_tokens = value
            return
        if method != "turn/completed":
            return
        turn = params.get("turn")
        if not isinstance(turn, dict):
            self.turn_failed = True
            return
        value = turn.get("durationMs")
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
            self.duration_ms = value
        self.turn_failed = turn.get("status") != "completed" or turn.get("error") is not None
        items = turn.get("items")
        if not self.output and isinstance(items, list):
            for item in items:
                if not isinstance(item, dict) or item.get("type") != "agentMessage":
                    continue
                text = item.get("text")
                if isinstance(text, str):
                    self.output = text

    def fail(self, output: str) -> None:
        self.output = output
        self.turn_failed = True

    def result(
        self,
        *,
        skill: str,
        mode: str,
        available_skills: list[str],
        selected: bool,
        events: list[dict[str, str]],
    ) -> dict[str, object]:
        status = _terminal_status(
            self.output,
            mode=mode,
            is_error=self.turn_failed,
        )
        bounded_events = list(events)
        bounded_events.append({"type": "final_output", "terminal_status": status})
        loaded = [skill] if selected and skill in available_skills else []
        return {
            "loaded_skills": loaded,
            "selected_skill": skill if loaded else None,
            "skill_loaded": bool(loaded),
            "available_skills": available_skills,
            "output": self.output,
            "terminal_status": status,
            "events": bounded_events,
            "total_tokens": self.total_tokens,
            "duration_ms": self.duration_ms,
            "tool_uses": self.tool_uses,
            "nested_calls": sum(
                event.get("type") == "phase_invocation" for event in events
            ),
        }


class JsonRpcProcess:
    def __init__(
        self,
        command: list[str],
        *,
        cwd: Path,
        env: Mapping[str, str],
    ) -> None:
        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._messages: queue.Queue[str | None] = queue.Queue()
        self._stderr: deque[str] = deque(maxlen=20)
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        threading.Thread(
            target=self._pump_stdout,
            args=(self.process.stdout,),
            daemon=True,
        ).start()
        threading.Thread(
            target=self._pump_stderr,
            args=(self.process.stderr,),
            daemon=True,
        ).start()

    def _pump_stdout(self, stream: IO[str]) -> None:
        for line in stream:
            self._messages.put(line)
        self._messages.put(None)

    def _pump_stderr(self, stream: IO[str]) -> None:
        for line in stream:
            self._stderr.append(line.rstrip())

    def send(self, message: Mapping[str, object]) -> None:
        if self.process.stdin is None:
            raise RuntimeError("Codex app-server stdin is unavailable")
        self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

    def receive(self, *, deadline: float) -> dict[str, object]:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Codex app-server eval timed out")
        try:
            line = self._messages.get(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError("Codex app-server eval timed out") from exc
        if line is None:
            detail = self._stderr[-1] if self._stderr else "no diagnostic"
            raise RuntimeError(f"Codex app-server exited before completion: {detail}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Codex app-server emitted malformed JSON") from exc
        if not isinstance(value, dict):
            raise RuntimeError("Codex app-server emitted a non-object message")
        return value

    def respond_to_server_request(self, message: Mapping[str, object]) -> bool:
        if "id" not in message or not isinstance(message.get("method"), str):
            return False
        self.send(
            {
                "id": message["id"],
                "error": {
                    "code": -32000,
                    "message": "TigerKit eval does not grant interactive input or approval",
                },
            }
        )
        return True

    def request(
        self,
        method: str,
        request_id: int,
        params: Mapping[str, object],
        *,
        deadline: float,
        observation: CodexObservation | None = None,
    ) -> dict[str, object]:
        self.send({"method": method, "id": request_id, "params": params})
        while True:
            message = self.receive(deadline=deadline)
            if message.get("id") == request_id and "method" not in message:
                error = message.get("error")
                if error is not None:
                    raise RuntimeError(f"Codex app-server {method} failed")
                result = message.get("result")
                if not isinstance(result, dict):
                    raise RuntimeError(f"Codex app-server {method} returned no result")
                return result
            if self.respond_to_server_request(message):
                continue
            if observation is not None:
                observation.consume(message)

    def close(self) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)


def _terminal_status(output: str, *, mode: str, is_error: bool) -> str:
    if is_error:
        return "Unverifiable"
    matches = STATUS_PATTERN.findall(output)
    if matches:
        return matches[-1]
    return "NotApplicable" if mode == "trigger" else "Unverifiable"


def _build_turn_start_params(
    *,
    thread_id: str,
    checkout: Path,
    prompt: str,
    skill: str,
    skill_path: Path,
) -> dict[str, object]:
    return {
        "threadId": thread_id,
        "sandboxPolicy": {
            "type": "workspaceWrite",
            "writableRoots": [str(checkout), str(checkout / ".git")],
            "networkAccess": False,
        },
        "input": [
            {"type": "text", "text": prompt},
            {"type": "skill", "name": skill, "path": str(skill_path)},
        ],
    }


def _stage_project_skills(checkout: Path) -> tuple[Path, bool]:
    agents_dir = checkout / ".agents"
    skills_target = agents_dir / "skills"
    if skills_target.exists():
        raise RuntimeError(
            "host-native eval checkout must not contain pre-existing .agents/skills"
        )
    remove_agents_dir = not agents_dir.exists()
    skills_target.mkdir(parents=True)
    for source in sorted((checkout / "skills").glob("tk-*")):
        if source.is_dir():
            shutil.copytree(
                source,
                skills_target / source.name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
    return skills_target, remove_agents_dir


def _remove_project_skills(skills_target: Path, remove_agents_dir: bool) -> None:
    shutil.rmtree(skills_target)
    agents_dir = skills_target.parent
    if remove_agents_dir and agents_dir.exists() and not any(agents_dir.iterdir()):
        agents_dir.rmdir()


def _hide_project_skills_from_git(
    checkout: Path,
) -> tuple[Path, bytes | None] | None:
    git_dir = checkout / ".git"
    if not git_dir.is_dir():
        return None
    exclude = git_dir / "info" / "exclude"
    original = exclude.read_bytes() if exclude.is_file() else None
    exclude.parent.mkdir(parents=True, exist_ok=True)
    content = original or b""
    suffix = b"" if content.endswith(b"\n") or not content else b"\n"
    exclude.write_bytes(content + suffix + b".agents/skills/\n")
    return exclude, original


def _restore_git_exclude(state: tuple[Path, bytes | None] | None) -> None:
    if state is None:
        return
    path, original = state
    if original is None:
        path.unlink(missing_ok=True)
    else:
        path.write_bytes(original)


def _read_event_log(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    if path.stat().st_size > 1024 * 1024:
        raise RuntimeError("tk-drive event log exceeds 1 MiB")
    events: list[dict[str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if len(line) > 4096:
            raise RuntimeError(f"tk-drive event log line {line_number} is too long")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"tk-drive event log line {line_number} is malformed"
            ) from exc
        if not isinstance(event, dict) or event.get("type") not in EVENT_TYPES:
            raise RuntimeError(f"tk-drive event log line {line_number} has invalid type")
        event_type = event["type"]
        expected = (
            {"type", "phase"}
            if event_type == "phase_invocation"
            else {"type", "phase", "state", "transition"}
        )
        if set(event) != expected or event.get("phase") not in PHASES:
            raise RuntimeError(f"tk-drive event log line {line_number} has invalid fields")
        if event_type == "phase_receipt" and (
            event.get("state") not in SUCCESS_STATES
            or not isinstance(event.get("transition"), str)
            or not event["transition"].strip()
        ):
            raise RuntimeError(f"tk-drive event log line {line_number} has invalid receipt")
        events.append({key: str(value) for key, value in event.items()})
    return events


def _available_repo_skills(
    result: Mapping[str, object],
    *,
    checkout: Path,
) -> tuple[list[str], dict[str, object] | None]:
    data = result.get("data")
    if not isinstance(data, list):
        return [], None
    skills: list[dict[str, object]] = []
    for row in data:
        if not isinstance(row, dict) or row.get("cwd") != str(checkout):
            continue
        values = row.get("skills")
        if isinstance(values, list):
            skills.extend(value for value in values if isinstance(value, dict))
    names = sorted(
        {
            value["name"]
            for value in skills
            if isinstance(value.get("name"), str) and value.get("enabled") is True
        }
    )
    drive = next(
        (
            value
            for value in skills
            if value.get("name") == "tk-drive"
            and value.get("enabled") is True
            and value.get("path")
            == str(checkout / ".agents/skills/tk-drive/SKILL.md")
        ),
        None,
    )
    return names, drive


def _prepare_codex_home(run_dir: Path) -> Path:
    target = run_dir / "codex-home"
    target.mkdir(exist_ok=True)
    source_raw = os.environ.get("TK_EVAL_CODEX_HOME")
    if source_raw:
        source_auth = Path(source_raw) / "auth.json"
        if not source_auth.is_file():
            raise RuntimeError("TK_EVAL_CODEX_HOME does not contain auth.json")
        shutil.copy2(source_auth, target / "auth.json")
    return target


def _app_server_command() -> list[str]:
    command = ["codex", "app-server", "--stdio"]
    model = os.environ.get("TK_EVAL_CODEX_MODEL")
    if model:
        command.extend(["-c", f"model={json.dumps(model)}"])
    return command


def _run_codex(
    *,
    checkout: Path,
    prompt: str,
    skill: str,
    skill_path: Path,
    event_log: Path,
    recorder: Path,
    run_dir: Path,
    observation: CodexObservation,
) -> tuple[list[str], bool]:
    deadline = time.monotonic() + float(
        os.environ.get("TK_EVAL_TIMEOUT_SECONDS", "1200")
    )
    child_env = os.environ.copy()
    child_env.update(
        {
            "CODEX_HOME": str(_prepare_codex_home(run_dir)),
            "TK_DRIVE_EVENT_LOG": str(event_log),
            "TK_DRIVE_EVENT_RECORDER": str(recorder),
            "GIT_AUTHOR_NAME": "TigerKit Eval",
            "GIT_AUTHOR_EMAIL": "tigerkit-eval@example.invalid",
            "GIT_COMMITTER_NAME": "TigerKit Eval",
            "GIT_COMMITTER_EMAIL": "tigerkit-eval@example.invalid",
        }
    )
    client = JsonRpcProcess(_app_server_command(), cwd=checkout, env=child_env)
    try:
        client.request(
            "initialize",
            0,
            {
                "clientInfo": {
                    "name": "tigerkit_eval",
                    "title": "TigerKit Eval",
                    "version": "1.0.0",
                }
            },
            deadline=deadline,
        )
        client.send({"method": "initialized", "params": {}})
        skill_result = client.request(
            "skills/list",
            1,
            {"cwds": [str(checkout)], "forceReload": True},
            deadline=deadline,
        )
        available_skills, selected_skill = _available_repo_skills(
            skill_result,
            checkout=checkout,
        )
        if skill != "tk-drive" or selected_skill is None:
            raise RuntimeError("Codex did not expose the staged repo tk-drive skill")
        thread_params: dict[str, object] = {
            "cwd": str(checkout),
            "approvalPolicy": "never",
            "sandbox": "workspace-write",
            "ephemeral": True,
            "serviceName": "tigerkit_eval",
        }
        thread_result = client.request(
            "thread/start",
            2,
            thread_params,
            deadline=deadline,
        )
        thread = thread_result.get("thread")
        thread_id = thread.get("id") if isinstance(thread, dict) else None
        if not isinstance(thread_id, str):
            raise RuntimeError("Codex app-server did not return a thread ID")
        client.request(
            "turn/start",
            3,
            _build_turn_start_params(
                thread_id=thread_id,
                checkout=checkout,
                prompt=prompt,
                skill=skill,
                skill_path=skill_path,
            ),
            deadline=deadline,
            observation=observation,
        )
        while True:
            message = client.receive(deadline=deadline)
            if client.respond_to_server_request(message):
                continue
            observation.consume(message)
            if (
                message.get("method") == "turn/completed"
                and isinstance(message.get("params"), dict)
                and message["params"].get("threadId") == thread_id
            ):
                break
        return available_skills, True
    finally:
        client.close()


def main() -> int:
    if os.environ.get("TK_EVAL_HOST") != "codex":
        raise SystemExit("codex_eval_adapter.py requires TK_EVAL_HOST=codex")
    checkout = Path.cwd()
    prompt = os.environ["TK_EVAL_PROMPT"]
    skill = os.environ["TK_EVAL_SKILL"]
    mode = os.environ["TK_EVAL_MODE"]
    run_dir = Path(os.environ["TK_EVAL_RUN_DIR"])
    event_log = run_dir / "tk-drive-events.jsonl"
    observation = CodexObservation()
    available_skills: list[str] = []
    selected = False
    started = time.monotonic()
    skills_target: Path | None = None
    remove_agents_dir = False
    exclude_state: tuple[Path, bytes | None] | None = None
    try:
        skills_target, remove_agents_dir = _stage_project_skills(checkout)
        exclude_state = _hide_project_skills_from_git(checkout)
        skill_path = skills_target / skill / "SKILL.md"
        recorder = skills_target / "tk-drive" / "scripts" / "record_eval_event.py"
        available_skills, selected = _run_codex(
            checkout=checkout,
            prompt=prompt,
            skill=skill,
            skill_path=skill_path,
            event_log=event_log,
            recorder=recorder,
            run_dir=run_dir,
            observation=observation,
        )
    except (OSError, RuntimeError, TimeoutError, ValueError) as exc:
        observation.fail(f"Codex eval is unverifiable: {exc}")
    finally:
        if skills_target is not None:
            _remove_project_skills(skills_target, remove_agents_dir)
        _restore_git_exclude(exclude_state)
    if observation.duration_ms is None:
        observation.duration_ms = round((time.monotonic() - started) * 1000)
    try:
        events = _read_event_log(event_log)
    except RuntimeError as exc:
        observation.fail(f"Codex eval event evidence is unverifiable: {exc}")
        events = []
    print(
        json.dumps(
            observation.result(
                skill=skill,
                mode=mode,
                available_skills=available_skills,
                selected=selected,
                events=events,
            ),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
