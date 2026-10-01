#!/usr/bin/env python3
"""Opt-in, bounded CLI diagnostics; never certify complete eval isolation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess

from artifact_policy import scratch_directory

CANDIDATE = "TIGERKIT_PROBE_CANDIDATE_79fba7"
AMBIENT_SKILL = "TIGERKIT_PROBE_AMBIENT_SKILL_835c11"
AMBIENT_RULE = "TIGERKIT_PROBE_AMBIENT_RULE_13dc82"
ENV_KEYS = ("PATH", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
            "SSL_CERT_FILE", "SSL_CERT_DIR", "CODEX_PROXY_CERT", "SystemRoot")


def stop_process(process: subprocess.Popen, grouped: bool) -> bool:
    """Terminate only this invocation's process group, including descendants."""
    clean = grouped
    try:
        if grouped:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        elif process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=0.25)
        except subprocess.TimeoutExpired:
            pass
        # The CLI may exit before its child, or a child may ignore SIGTERM.
        # Always kill the owned group before deleting its HOME/workdir.
        if grouped:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        elif process.poll() is None:
            process.kill()
        process.wait(timeout=1)
    except (OSError, subprocess.TimeoutExpired):
        clean = False
    finally:
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                stream.close()
    return clean


def invoke(cli: str, arguments: list[str], home: Path, workdir: Path,
           timeout: float) -> tuple[str, str, bool]:
    env = {key: os.environ[key] for key in ENV_KEYS if key in os.environ}
    env.update(HOME=str(home), CODEX_HOME=str(home / ".codex"))
    grouped = os.name == "posix" and hasattr(os, "killpg")
    try:
        process = subprocess.Popen([cli, *arguments], cwd=workdir, env=env,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True,
                                   start_new_session=grouped)
    except OSError:
        return "unavailable", "", True
    try:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            status = "completed" if process.returncode == 0 else "failed"
            output = stdout + (stderr if arguments == ["login", "status"] else "")
        except subprocess.TimeoutExpired:
            status, output = "timeout", ""
    finally:
        # Also runs on KeyboardInterrupt and other exceptions.
        clean = stop_process(process, grouped)
    return status, output, clean


def skill(path: Path, name: str, sentinel: str) -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {sentinel}\n---\n"
        "Return the word probe when explicitly invoked.\n", encoding="utf-8")


def strings(value: object) -> str:
    """Inspect host JSON only, never prose or an agent's self-report."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(strings(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(strings(item) for item in value.values())
    return ""


def probe(cli: str, root: Path, timeout: float = 5,
          auth_file: Path | None = None) -> dict[str, object]:
    """root is exclusively run-owned; caller must clean it even on failure."""
    result: dict[str, object] = {
        "isolation_status": "Unverifiable", "skill_activation": "Unverifiable",
        "task_execution": "Unverifiable", "plugins_apps_mcp_exclusion": "Unverifiable",
        "auth_discovery": "NotApplicable", "auth_unchanged": "NotApplicable",
    }
    auth_before = None
    process_cleanup = []
    if auth_file is not None:
        auth_file = auth_file.resolve(strict=True)
        auth_before = hashlib.sha256(auth_file.read_bytes()).digest()
        home = root / "auth-status"
        (home / ".codex").mkdir(parents=True, mode=0o700)
        (home / ".codex/auth.json").symlink_to(auth_file)
        # Only the non-refreshing status command sees the existing credentials.
        try:
            status, output, clean = invoke(cli, ["login", "status"], home, home, timeout)
            process_cleanup.append(clean)
            result["auth_discovery"] = ("Pass" if status == "completed" and
                                          "Logged in" in output else "Unverifiable")
        finally:
            (home / ".codex/auth.json").unlink(missing_ok=True)
            result["auth_unchanged"] = ("Pass" if hashlib.sha256(auth_file.read_bytes()).digest()
                                          == auth_before else "Fail")

    version_home = root / "version"
    (version_home / ".codex").mkdir(parents=True)
    status, output, clean = invoke(cli, ["--version"], version_home, version_home, timeout)
    process_cleanup.append(clean)
    version = output.strip()
    result["host_version"] = (version if status == "completed" and
                               version.startswith(("codex ", "codex-cli ")) and
                               len(version.split()) == 2 else None)
    observations: dict[str, str | None] = {}
    statuses: dict[str, str] = {}
    for arm in ("ambient-control", "candidate", "ablation"):
        home, workdir = root / arm / "home", root / arm / "workdir"
        (home / ".codex").mkdir(parents=True, mode=0o700)
        workdir.mkdir()
        config = '[features]\napps = false\nplugins = false\n'
        if arm == "ambient-control":
            config = f'developer_instructions = "{AMBIENT_RULE}"\n' + config
            skill(home / ".codex/skills/tk-probe-ambient", "tk-probe-ambient", AMBIENT_SKILL)
            skill(home / ".agents/skills/tk-probe-ambient", "tk-probe-ambient", AMBIENT_SKILL)
        elif arm == "candidate":
            skill(workdir / ".agents/skills/tk-probe-candidate", "tk-probe-candidate", CANDIDATE)
        (home / ".codex/config.toml").write_text(config, encoding="utf-8")
        status, output, clean = invoke(cli, ["debug", "prompt-input", "Reply with probe."],
                                       home, workdir, timeout)
        process_cleanup.append(clean)
        text = None
        if status == "completed":
            try:
                value = json.loads(output)
                if isinstance(value, (dict, list)):
                    text = strings(value)
            except json.JSONDecodeError:
                pass
        observations[arm], statuses[arm] = text, status
    result["prompt_input_status"] = statuses
    result["process_cleanup_status"] = "Pass" if all(process_cleanup) else "Unverifiable"
    control, candidate, ablation = (observations[arm] for arm in
                                    ("ambient-control", "candidate", "ablation"))
    observable = all(text is not None for text in (control, candidate, ablation))
    result["candidate_catalog_difference"] = ("Pass" if observable and CANDIDATE in candidate
                                                and CANDIDATE not in ablation else "Unverifiable")
    for key, sentinel in (("ambient_skill_catalog_exclusion", AMBIENT_SKILL),
                          ("ambient_rule_prompt_exclusion", AMBIENT_RULE)):
        result[key] = ("Pass" if observable and sentinel in control and
                       sentinel not in candidate and sentinel not in ablation else "Unverifiable")
    # Prompt catalog exposure is weaker than activation, task execution or a
    # complete capability inventory. Never promote the canonical adapter here.
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", default=shutil.which("codex"))
    parser.add_argument("--auth-file", type=Path,
                        help="Optional existing auth.json; used only by login status")
    parser.add_argument("--timeout", type=float, default=5,
                        help="Per-command timeout in seconds, maximum 15")
    args = parser.parse_args()
    if not args.cli or not 0 < args.timeout <= 15:
        parser.error("available --cli and timeout in (0, 15] are required")
    with scratch_directory("codex-isolation-probe") as directory:
        path = Path(directory)
        result = probe(args.cli, path, args.timeout, args.auth_file)
    result["cleanup_status"] = (result["process_cleanup_status"] if not path.exists() else "Fail")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
