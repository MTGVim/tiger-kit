#!/usr/bin/env python3
"""Run one tk-drive eval through Codex app-server's explicit skill input."""

from __future__ import annotations

import json
import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Callable, Mapping


TERMINAL_STATUSES = ("Pass", "Pending", "Blocked", "Fail", "Unverifiable")
EVENT_TYPES = {"phase_invocation"}
PHASES = {
    "tk-grill-me",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-prototype",
    "tk-implement",
}
LIVE_FIXTURES = {
    "[tigerkit-eval:prepared-single]\n/tk-drive": "single",
    "[tigerkit-eval:prepared-two-unit]\n/tk-drive": "two-unit",
    "/tk-drive Create canary-choice.txt containing alpha.": "cold-start",
}
LIVE_FIXTURE_CONTENT = {
    "single": {"canary-ready.txt": b"ready\n"},
    "two-unit": {
        "canary-alpha.txt": b"alpha\n",
        "canary-beta.txt": b"beta\n",
    },
    "cold-start": {"canary-choice.txt": b"alpha\n"},
}
STATUS_PATTERN = re.compile(
    r"(?m)^[ \t]*(?:[-*][ \t]+)?Status:[ \t]*"
    r"(Pass|Pending|Blocked|Fail|Unverifiable)[ \t]*$"
)


class CodexObservation:
    def __init__(self) -> None:
        self.output = ""
        self._terminal_output = ""
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
            is_agent_message = item_type in {"agentMessage", "agent_message"}
            if (
                not is_agent_message
                and isinstance(item_id, str)
                and item_id not in self._seen_tool_items
            ):
                self._seen_tool_items.add(item_id)
                self.tool_uses += 1
            if method == "item/completed" and is_agent_message:
                text = item.get("text")
                if isinstance(text, str):
                    self.output = f"{self.output}\n\n{text}" if self.output else text
                    self._terminal_output = text
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
                if not isinstance(item, dict) or item.get("type") not in {"agentMessage", "agent_message"}:
                    continue
                text = item.get("text")
                if isinstance(text, str):
                    self.output = f"{self.output}\n\n{text}" if self.output else text
                    self._terminal_output = text

    def fail(self, output: str) -> None:
        self.output = output
        self._terminal_output = output
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
            self._terminal_output or self.output,
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
        approval_handler: Callable[[Mapping[str, object]], bool] | None = None,
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
        self._approval_handler = approval_handler
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
        method = message.get("method")
        if "id" not in message or not isinstance(method, str):
            return False
        params = message.get("params")
        if (
            method == "item/commandExecution/requestApproval"
            and self._approval_handler is not None
            and isinstance(params, dict)
        ):
            decision = "accept" if self._approval_handler(params) else "decline"
            self.send({"id": message["id"], "result": {"decision": decision}})
            return True
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
    approval_policy: str,
) -> dict[str, object]:
    return {
        "threadId": thread_id,
        "approvalPolicy": approval_policy,
        "sandboxPolicy": {
            "type": "workspaceWrite",
            "writableRoots": [str(checkout)],
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


def _git_value(checkout: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    value = completed.stdout.strip()
    if completed.returncode != 0 or not value:
        raise RuntimeError(f"cannot resolve eval Git identity: {' '.join(arguments)}")
    return value


def _ensure_eval_branch(checkout: Path, kind: str) -> str:
    completed = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("cannot resolve eval Git identity: branch --show-current")
    branch = completed.stdout.strip()
    if branch:
        return branch
    branch = f"tigerkit-eval-{kind}"
    switched = subprocess.run(
        ["git", "switch", "-c", branch],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    if switched.returncode != 0:
        detail = switched.stderr.strip() or switched.stdout.strip()
        raise RuntimeError(f"cannot create prepared eval branch: {detail}")
    return branch


def _configure_eval_git(checkout: Path) -> None:
    hooks = checkout / ".tigerkit" / "no-hooks"
    hooks.mkdir(parents=True)
    for key, value in (
        ("core.hooksPath", str(hooks)),
        ("commit.gpgsign", "false"),
        ("tag.gpgsign", "false"),
    ):
        completed = subprocess.run(
            ["git", "config", "--local", key, value],
            cwd=checkout,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"cannot secure prepared eval Git config: {key}")


def _prepare_live_fixture(
    checkout: Path,
    skills_target: Path,
    prompt: str,
) -> str:
    kind = LIVE_FIXTURES.get(prompt)
    if kind is None:
        return prompt
    if kind == "cold-start":
        _configure_eval_git(checkout)
        return prompt

    tigerkit = checkout / ".tigerkit"
    if tigerkit.exists():
        raise RuntimeError("prepared eval fixture requires an empty .tigerkit path")
    tigerkit.mkdir()
    units = [
        (
            "T-EVAL-1",
            "Create `canary-ready.txt` containing `ready` plus one trailing newline.",
        )
    ]
    if kind == "two-unit":
        units = [
            (
                "T-EVAL-ALPHA",
                "Create `canary-alpha.txt` containing `alpha` plus one trailing newline.",
            ),
            (
                "T-EVAL-BETA",
                "Create `canary-beta.txt` containing `beta` plus one trailing newline.",
            ),
        ]
    dirty_inventory = [".tigerkit/spec.md", ".tigerkit/tickets.md"]
    instruction_inventory: list[str] = []
    profile = {
        "obligations": ["regression-seam"],
        "signals": ["state-compatibility"],
    }
    spec_lines = [
        "# TigerKit eval spec",
        "",
        "Status: Ready",
        "",
        "## Requirements",
        "",
    ]
    ticket_lines = ["# TigerKit eval tickets", "", "Status: Pass", ""]
    for index, (ticket_id, requirement) in enumerate(units, 1):
        spec_lines.append(f"- R{index}: {requirement}")
        ticket_lines.extend(
            (
                f"## {ticket_id}",
                "",
                "Status: pending",
                f"Requirement: R{index}",
                f"Acceptance: the exact file content for R{index} is verified.",
                "",
            )
        )
    spec_lines.extend(
        (
            "",
            "## Acceptance criteria",
            "",
            *[
                f"- AC{index}: Verify the exact file content required by R{index}."
                for index in range(1, len(units) + 1)
            ],
            "",
            "## Execution strategy",
            "",
            "PR evidence: N/A",
            "",
        )
    )
    spec = tigerkit / "spec.md"
    tickets = tigerkit / "tickets.md"
    spec.write_text("\n".join(spec_lines), encoding="utf-8")
    tickets.write_text("\n".join(ticket_lines), encoding="utf-8")

    head = _git_value(checkout, "rev-parse", "HEAD")
    branch = _ensure_eval_branch(checkout, kind)
    source = f"tigerkit-eval:{kind}"
    preflight_input = {
        "task": {
            "goal": f"Execute the {kind} TigerKit canary.",
            "included_scope": [ticket_id for ticket_id, _ in units],
            "excluded_scope": [],
            "confirmed_decisions": ["Use exact canary contents."],
        },
        "repository": {
            "root": str(checkout),
            "worktree": str(checkout),
            "branch": branch,
            "baseline_head": head,
            "dirty_paths": dirty_inventory,
        },
        "execution": {
            "procedure_graph": ["tk-implement", "aggregate verification"],
            "verification_profile": profile,
            "pr_evidence": {"decision": "N/A", "criterion": None},
            "units": [
                {
                    "id": ticket_id,
                    "strategy": "direct",
                    "risk": "low",
                    "additional_review": "not-required",
                }
                for ticket_id, _ in units
            ],
        },
        "browser": {
            "decision": "N/A",
            "environment_url": None,
            "account_role_or_tenant_class": None,
            "opaque_profile_hint": None,
            "authentication_expectation": None,
            "ask_identity_on_cold_start": None,
        },
        "sources": {
            "spec": ".tigerkit/spec.md",
            "tickets": ".tigerkit/tickets.md",
        },
    }
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".json", delete=False
    ) as handle:
        json.dump(preflight_input, handle)
        input_path = Path(handle.name)
    command = [
        sys.executable,
        str(skills_target / "tk-drive" / "scripts" / "preflight.py"),
        "write",
        str(tigerkit / "prep.md"),
        "--worktree",
        str(checkout),
        "--input",
        str(input_path),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=checkout,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        input_path.unlink(missing_ok=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"cannot create prepared eval fixture: {detail}")
    _configure_eval_git(checkout)
    return (
        "[tigerkit-eval: current preflight, Ready spec, tickets, and Git "
        "evidence show incomplete implementation units; infer the next action "
        "from current evidence and continue]\n/tk-drive"
    )


class LiveGitApprovalGate:
    """Approve only the fixture's exact, non-composite Git add/commit commands."""

    def __init__(self, checkout: Path, kind: str) -> None:
        self.checkout = checkout.resolve()
        self.expected = LIVE_FIXTURE_CONTENT[kind]

    def __call__(self, params: Mapping[str, object]) -> bool:
        allowed = self._is_allowed(params)
        if not allowed:
            command = params.get("command")
            cwd = params.get("cwd")
            print(
                "LiveGitApprovalGate declined "
                f"cwd={cwd!r} command={command!r} keys={sorted(params)}",
                file=sys.stderr,
            )
        return allowed

    def _is_allowed(self, params: Mapping[str, object]) -> bool:
        if params.get("networkApprovalContext") is not None:
            return False
        permissions = params.get("additionalPermissions")
        if isinstance(permissions, dict):
            network = permissions.get("network")
            if isinstance(network, dict) and network.get("enabled") is True:
                return False
        cwd = params.get("cwd")
        command = params.get("command")
        if not isinstance(cwd, str) or not isinstance(command, str):
            return False
        try:
            if Path(cwd).resolve() != self.checkout:
                return False
            wrapped_script = self._wrapped_script(command)
            if wrapped_script is not None:
                if self._allow_staged_content_script(wrapped_script):
                    return True
                if "\n" in wrapped_script:
                    return self._allow_multiline_script(wrapped_script)
            tokens = self._command_tokens(command)
        except (OSError, ValueError):
            return False
        if any(marker in command for marker in ("\x00", "\n", "\r", "`", "$")):
            return False
        if not tokens or Path(tokens[0]).name != "git":
            return False
        operators = {"&&", "||", ";", "|", "&", ">", ">>", "<", "<<"}
        present = [token for token in tokens if token in operators]
        if present:
            if present != ["&&"] or tokens.count("&&") != 1:
                return False
            boundary = tokens.index("&&")
            if not self._staged_paths():
                return self._allow_add(tokens[:boundary]) and self._allow_commit(
                    tokens[boundary + 1 :],
                    require_staged=False,
                )
            return False
        if len(tokens) >= 2 and tokens[1] == "add":
            return self._allow_add(tokens)
        if len(tokens) >= 2 and tokens[1] == "commit":
            return self._allow_commit(tokens)
        return False

    def _command_tokens(self, command: str) -> list[str]:
        wrapped = self._wrapped_script(command)
        return self._shell_tokens(wrapped) if wrapped is not None else self._shell_tokens(command)

    def _wrapped_script(self, command: str) -> str | None:
        tokens = self._shell_tokens(command)
        if (
            len(tokens) == 3
            and tokens[1] == "-lc"
            and Path(tokens[0]).is_absolute()
            and Path(tokens[0]).parent in {Path("/bin"), Path("/usr/bin")}
            and Path(tokens[0]).name in {"bash", "sh", "zsh"}
        ):
            return tokens[2]
        return None

    def _allow_multiline_script(self, script: str) -> bool:
        if "\x00" in script or "\r" in script or self._staged_paths():
            return False
        lines = script.splitlines()
        if len(lines) != 10 or any(not line.strip() for line in lines):
            return False
        add_tokens = self._shell_tokens(lines[0])
        if not self._allow_add(add_tokens):
            return False
        paths = add_tokens[2:]
        if paths[:1] == ["--"]:
            paths = paths[1:]
        branch = _git_value(self.checkout, "branch", "--show-current")
        head = _git_value(self.checkout, "rev-parse", "HEAD")
        staged = "\n".join(paths)
        expected_middle = [
            "git diff --cached --stat",
            "git diff --cached --numstat",
            "git diff --cached --name-status",
            "git diff --cached --check",
            shlex.join(["git", "diff", "--cached", "--", *paths]),
            f'test "$(git branch --show-current)" = {shlex.quote(branch)}',
            f'test "$(git rev-parse HEAD)" = {shlex.quote(head)}',
            f'test "$(git diff --cached --name-only)" = {shlex.quote(staged)}',
        ]
        return lines[1:-1] == expected_middle and self._allow_commit(
            self._shell_tokens(lines[-1]),
            require_staged=False,
        )

    def _allow_staged_content_script(self, script: str) -> bool:
        if "\x00" in script or "\r" in script or "\n" in script or self._staged_paths():
            return False
        for path, content in self.expected.items():
            if not self._allow_add(["git", "add", "--", path]):
                continue
            expected = " && ".join(
                (
                    f"git add -- {path}",
                    f'test "$(git show :{path} | wc -c | tr -d \' \')" = {len(content)}',
                    (
                        f'test "$(git show :{path} | od -An -tx1 | '
                        f'tr -d \' \\\\n\')" = {content.hex()}'
                    ),
                    "git diff --cached --stat",
                    "git diff --cached --numstat",
                    "git diff --cached --name-only",
                    "git diff --cached --check",
                    f"git diff --cached -- {path}",
                    "git rev-parse HEAD",
                    "git branch --show-current",
                )
            )
            if script == expected:
                return True
        return False

    @staticmethod
    def _shell_tokens(command: str) -> list[str]:
        lexer = shlex.shlex(
            command,
            posix=True,
            punctuation_chars=";&|<>",
        )
        lexer.whitespace_split = True
        return list(lexer)

    def _allow_add(self, tokens: list[str]) -> bool:
        paths = tokens[2:]
        if paths[:1] == ["--"]:
            paths = paths[1:]
        if not paths or len(paths) != len(set(paths)):
            return False
        if any(path not in self.expected for path in paths):
            return False
        return all(
            (self.checkout / path).is_file()
            and (self.checkout / path).read_bytes() == self.expected[path]
            for path in paths
        )

    def _allow_commit(
        self,
        tokens: list[str],
        *,
        require_staged: bool = True,
    ) -> bool:
        message: str | None = None
        if len(tokens) == 4 and tokens[2] in {"-m", "--message"}:
            message = tokens[3]
        elif len(tokens) == 3 and tokens[2].startswith("--message="):
            message = tokens[2].partition("=")[2]
        if not message or len(message) > 200 or "\x00" in message:
            return False
        if not require_staged:
            return True
        staged = self._staged_paths()
        return len(staged) == 1 and staged[0] in self.expected

    def _staged_paths(self) -> list[str]:
        completed = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "-z"],
            cwd=self.checkout,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            return []
        return [
            value.decode("utf-8")
            for value in completed.stdout.split(b"\0")
            if value
        ]


def _hide_project_skills_from_git(
    checkout: Path,
) -> tuple[Path, bytes | None] | None:
    completed = subprocess.run(
        ["git", "rev-parse", "--git-path", "info/exclude"],
        cwd=checkout,
        text=True,
        capture_output=True,
        check=False,
    )
    raw_path = completed.stdout.strip()
    if completed.returncode != 0 or not raw_path:
        return None
    exclude = Path(raw_path)
    if not exclude.is_absolute():
        exclude = checkout / exclude
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
        expected = {"type", "phase"}
        if set(event) != expected or event.get("phase") not in PHASES:
            raise RuntimeError(f"tk-drive event log line {line_number} has invalid fields")
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


def _scrubbed_child_env() -> dict[str, str]:
    allowed = (
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "TERM",
        "TZ",
    )
    child = {
        key: os.environ[key]
        for key in allowed
        if os.environ.get(key)
    }
    child["PATH"] = os.environ.get("PATH", os.defpath)
    return child


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
    approval_handler: Callable[[Mapping[str, object]], bool] | None,
) -> tuple[list[str], bool]:
    deadline = time.monotonic() + float(
        os.environ.get("TK_EVAL_TIMEOUT_SECONDS", "1200")
    )
    child_env = _scrubbed_child_env()
    child_env.update(
        {
            "HOME": str(run_dir / "home"),
            "CODEX_HOME": str(_prepare_codex_home(run_dir)),
            "TK_DRIVE_PROCEDURE_LOG": str(event_log),
            "TK_DRIVE_PROCEDURE_RECORDER": str(recorder),
            "GIT_AUTHOR_NAME": "TigerKit Eval",
            "GIT_AUTHOR_EMAIL": "tigerkit-eval@example.invalid",
            "GIT_COMMITTER_NAME": "TigerKit Eval",
            "GIT_COMMITTER_EMAIL": "tigerkit-eval@example.invalid",
        }
    )
    client = JsonRpcProcess(
        _app_server_command(),
        cwd=checkout,
        env=child_env,
        approval_handler=approval_handler,
    )
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
            "approvalPolicy": "on-request" if approval_handler else "never",
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
                prompt=(
                    prompt
                    + "\n\nEvaluation instrumentation only: immediately before "
                    "each participating procedure invocation, run "
                    '`"$TK_DRIVE_PROCEDURE_RECORDER" <canonical-phase>`. '
                    "This records invocation only and does not change routing."
                ),
                skill=skill,
                skill_path=skill_path,
                approval_policy="on-request" if approval_handler else "never",
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
        fixture_kind = LIVE_FIXTURES.get(prompt)
        prompt = _prepare_live_fixture(checkout, skills_target, prompt)
        exclude_state = _hide_project_skills_from_git(checkout)
        skill_path = skills_target / skill / "SKILL.md"
        recorder = (
            skills_target / "tk-drive" / "scripts" / "record_procedure_event.py"
        )
        available_skills, selected = _run_codex(
            checkout=checkout,
            prompt=prompt,
            skill=skill,
            skill_path=skill_path,
            event_log=event_log,
            recorder=recorder,
            run_dir=run_dir,
            observation=observation,
            approval_handler=(
                LiveGitApprovalGate(checkout, fixture_kind)
                if fixture_kind is not None
                else None
            ),
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
