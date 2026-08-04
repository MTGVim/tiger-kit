#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).parent / "adapters/tigerkit_host_adapter.py"
SPEC = importlib.util.spec_from_file_location("tigerkit_host_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class HostAdapterTest(unittest.TestCase):
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
            with patch.object(adapter, "real_home", return_value=home):
                env = adapter.host_environment("codex")
            self.assertEqual(env["CODEX_HOME"], str(home / ".codex"))
            self.assertFalse((home / ".codex/skills").exists())

    def test_prepared_codex_prompt_uses_candidate_fixture_adapter_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            candidate = checkout / "skills/tk-drive/scripts/codex_eval_adapter.py"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("# fixture adapter\n", encoding="utf-8")

            self.assertEqual(
                adapter.prepared_codex_adapter(checkout, "[tigerkit-eval:prepared-respond-ci]\n/tk-pr-respond --ci"),
                candidate,
            )
            self.assertIsNone(adapter.prepared_codex_adapter(checkout, "/tk-pr-respond --ci"))

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


if __name__ == "__main__":
    unittest.main()
