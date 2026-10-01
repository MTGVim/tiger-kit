#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import os
import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).parent / "adapters/tigerkit_host_adapter.py"
SPEC = importlib.util.spec_from_file_location("tigerkit_host_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class HostAdapterTest(unittest.TestCase):
    def test_codex_checks_observed_version_and_flag_support(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            for help_text, code, expected in (("--ignore-user-config", 0, True),
                                              ("--ephemeral", 0, False),
                                              ("--ignore-user-config", 1, False)):
                with self.subTest(help=help_text, code=code), patch.object(adapter.subprocess, "run", side_effect=[
                    subprocess.CompletedProcess([], 0, "codex-cli 1.2.3\n", ""),
                    subprocess.CompletedProcess([], code, help_text, "")
                ]):
                    proof = adapter.codex_preflight("codex", checkout, {})
                    self.assertEqual(proof["host_version"], "codex-cli 1.2.3")
                    self.assertIs(proof["supports_user_config_exclusion"], expected)
            with patch.object(adapter.subprocess, "run", side_effect=subprocess.TimeoutExpired("codex", 30)):
                proof = adapter.codex_preflight("codex", checkout, {})
                self.assertIsNone(proof["host_version"])
                self.assertFalse(proof["supports_user_config_exclusion"])

    def test_codex_profile_cannot_claim_isolation_from_flag_or_agent_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "repo"
            skill = checkout / "skills/tk-example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Project fixture\n")
            auth = root / "auth-home"
            auth.mkdir()
            (auth / "auth.json").write_text("synthetic-auth")
            (auth / "config.toml").write_text('developer_instructions = "USER_SENTINEL"\n')
            (auth / "AGENTS.md").write_text("GLOBAL_SENTINEL")
            payload = {"output": "profile evidence", "terminal_status": "Pass", "selected_skill": "tk-example",
                       "loaded_skills": ["tk-example"], "events": [{"type": "final_output", "terminal_status": "Pass"}],
                       "execution_provenance": {"isolation_status": "Pass"}}
            stdout = json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text":
                adapter.MARKER_START + json.dumps(payload) + adapter.MARKER_END}})
            seen = {}
            def process(command, *, cwd, env):
                seen.update(command=command, auth=env["CODEX_HOME"])
                self.assertEqual((cwd / ".agents/skills/tk-example/SKILL.md").read_text(), "# Project fixture\n")
                return stdout, "", 0, 1
            output = io.StringIO()
            with patch.object(adapter.Path, "cwd", return_value=checkout), patch.object(adapter, "executable_for", return_value="codex"), patch.object(adapter, "codex_preflight", return_value={"host_version":"codex-cli 1.2.3", "supports_user_config_exclusion":True}), patch.object(adapter, "run_process", side_effect=process), patch.dict(os.environ, {"TK_EVAL_HOST":"codex", "TK_EVAL_PROMPT":"task", "TK_EVAL_AUTH_CODEX_HOME":str(auth), "TK_EVAL_WATCH_PATHS":"[]"}), contextlib.redirect_stdout(output):
                self.assertEqual(adapter.main(), 0)
            result = json.loads(output.getvalue())
            self.assertIn("--ignore-user-config", seen["command"])
            self.assertEqual(seen["auth"], str(auth))
            self.assertEqual(result["execution_provenance"]["isolation_status"], "Unverifiable")
            self.assertEqual(result["execution_provenance"]["project_fixture_status"], "installed")
            self.assertEqual(list(root.rglob("auth.json")), [auth / "auth.json"])
            self.assertEqual((auth / "config.toml").read_text(), 'developer_instructions = "USER_SENTINEL"\n')
            self.assertNotIn("USER_SENTINEL", output.getvalue())
            self.assertNotIn("GLOBAL_SENTINEL", output.getvalue())
            (checkout / ".agents/skills/tk-example/SKILL.md").unlink()
            proof = adapter.codex_provenance({"host_version":"codex-cli 1.2.3", "supports_user_config_exclusion":True}, checkout, ["tk-example"])
            self.assertEqual(proof["project_fixture_status"], "Unverifiable")

    def test_codex_unsupported_isolation_stops_before_task_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            skill = checkout / "skills/tk-example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Fixture\n")
            output = io.StringIO()
            with patch.object(adapter.Path, "cwd", return_value=checkout), patch.object(adapter, "executable_for", return_value="codex"), patch.object(adapter, "codex_preflight", return_value={"host_version":"codex-cli old", "supports_user_config_exclusion":False}), patch.object(adapter, "run_process") as process, patch.dict(os.environ, {"TK_EVAL_HOST":"codex", "TK_EVAL_PROMPT":"task"}), contextlib.redirect_stdout(output):
                with self.assertRaisesRegex(RuntimeError, "unavailable; evaluation was not run"):
                    adapter.main()
            process.assert_not_called()
            self.assertEqual(output.getvalue(), "")

    def test_observed_model_uses_host_metadata_not_agent_envelope(self) -> None:
        self.assertEqual(adapter.observed_execution_identity("claude-code", json.dumps({
            "modelUsage": {"actual-model": {"inputTokens": 10}},
            "result": "agent says another model"})), {"model": "actual-model"})
        for value in ({"model": "requested-only"}, {"modelUsage": {}},
                      {"modelUsage": {"a": {}, "b": {}}}):
            self.assertIsNone(adapter.observed_execution_identity("claude-code", json.dumps(value)))
        stream = json.dumps({"type": "session_meta", "payload": {
            "model": "actual-model", "reasoning_effort": "high"}})
        self.assertEqual(adapter.observed_execution_identity("codex", stream),
                         {"model": "actual-model", "config": {"reasoning_effort": "high"}})
        self.assertIsNone(adapter.observed_execution_identity("codex", json.dumps({
            "type": "item.completed", "item": {"text": '{"model":"claimed"}'}})))

    def test_missing_and_invalid_tokens_are_not_zero(self) -> None:
        self.assertIsNone(adapter.claude_text('{"usage":{}}')[1])
        self.assertIsNone(adapter.claude_text('{"usage":{"input_tokens":10}}')[1])
        self.assertEqual(adapter.claude_text('{"usage":{"input_tokens":10,"output_tokens":2,"cache_read_input_tokens":3}}')[1], 15)
        for value in (-1, True, float("nan"), float("inf"), "10"):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                adapter.claude_text(json.dumps({"usage": {"input_tokens": value, "output_tokens": 1}}))

    def test_extracts_marker_delimited_payload(self) -> None:
        payload = {
            "output": "done",
            "terminal_status": "Pass",
            "selected_skill": "tk-drive",
            "loaded_skills": ["tk-drive"],
            "events": [
                {"type": "phase_invocation", "phase": "tk-drive"},
                {"type": "final_output", "terminal_status": "Pass"},
            ],
        }
        text = (
            f"before\n{adapter.MARKER_START}\n"
            f"{json.dumps(payload)}\n{adapter.MARKER_END}"
        )
        self.assertEqual(adapter.extract_payload(text), payload)

    def test_rejects_missing_result_envelope(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "omitted"):
            adapter.extract_payload("plain output")

    def test_codex_jsonl_extracts_agent_messages_and_usage(self) -> None:
        stdout = "\n".join(
            [
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {"type": "agent_message", "text": "first"},
                    }
                ),
                json.dumps({"type": "turn.completed", "usage": {"total_tokens": 42}}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {"type": "agent_message", "text": "second"},
                    }
                ),
            ]
        )
        text, tokens = adapter.codex_text(stdout)
        self.assertEqual(text, "first\nsecond")
        self.assertEqual(tokens, 42.0)

    def test_installs_skills_only_inside_disposable_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "repo"
            skill = checkout / "skills/tk-example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")

            installed = adapter.install_skills("codex", checkout)

            self.assertEqual(installed, ["tk-example"])
            self.assertTrue((checkout / ".agents/skills/tk-example/SKILL.md").is_file())
            self.assertTrue((checkout / ".codex/skills/tk-example/SKILL.md").is_file())

    def test_codex_reuses_real_auth_home_without_installing_user_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "real-home"
            home.mkdir()
            with patch.object(adapter, "real_home", return_value=home), patch.dict(os.environ, {}, clear=True):
                env = adapter.host_environment("codex")
            self.assertEqual(env["CODEX_HOME"], str(home / ".codex"))
            self.assertFalse((home / ".codex/skills").exists())

    def test_hermes_copies_provider_config_but_not_oauth_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_home = root / "source"
            source = source_home / ".hermes"
            source.mkdir(parents=True)
            (source / "config.yaml").write_text("model: test\n", encoding="utf-8")
            (source / ".env").write_text("KEY=value\n", encoding="utf-8")
            (source / "auth.json").write_text("secret\n", encoding="utf-8")
            isolated = root / "isolated"
            with patch.object(adapter, "real_home", return_value=source_home), patch.dict(
                os.environ, {"HERMES_HOME": str(isolated)}
            ):
                adapter.host_environment("hermes-agent")
            self.assertTrue((isolated / "config.yaml").is_file())
            self.assertTrue((isolated / ".env").is_file())
            self.assertFalse((isolated / "auth.json").exists())

    def test_missing_executable_is_an_unavailable_host(self) -> None:
        with patch.object(adapter.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                adapter.executable_for("codex")

    def test_claude_executable_can_use_a_shim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            shim = Path(directory) / "claude-shim"
            shim.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            shim.chmod(0o755)
            with patch.dict(os.environ, {"TK_EVAL_CLAUDE_EXECUTABLE": str(shim)}):
                self.assertEqual(adapter.executable_for("claude-code"), str(shim))

    def test_path_watch_reports_read_and_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            (checkout / "read.md").write_text("read me\n", encoding="utf-8")
            (checkout / "unread.md").write_text("leave me\n", encoding="utf-8")

            watch = adapter.arm_path_watch(checkout, ["read.md", "unread.md"])
            self.assertTrue(watch[0])
            (checkout / "read.md").read_text(encoding="utf-8")
            result = adapter.finish_path_watch(watch)

            self.assertEqual(
                result,
                {"available": True, "read_paths": ["read.md"]},
            )

    def test_path_watch_is_unavailable_when_atime_cannot_be_armed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            (checkout / "watched.md").write_text("watch me\n", encoding="utf-8")
            with patch.object(adapter.os, "utime", side_effect=OSError("no atime")):
                watch = adapter.arm_path_watch(checkout, ["watched.md"])
            self.assertEqual(
                adapter.finish_path_watch(watch),
                {"available": False, "read_paths": []},
            )

    def test_path_watch_rejects_paths_outside_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "repo"
            checkout.mkdir()
            outside = checkout.parent / "outside.md"
            outside.write_text("secret\n", encoding="utf-8")

            watch = adapter.arm_path_watch(checkout, ["../outside.md"])

            self.assertEqual(
                adapter.finish_path_watch(watch),
                {"available": False, "read_paths": []},
            )


if __name__ == "__main__":
    unittest.main()
