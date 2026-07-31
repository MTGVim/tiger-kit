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
        text = f"before\n{adapter.MARKER_START}\n{json.dumps(payload)}\n{adapter.MARKER_END}"
        self.assertEqual(adapter.extract_payload(text), payload)

    def test_rejects_missing_result_envelope(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "omitted"):
            adapter.extract_payload("plain output")

    def test_codex_jsonl_extracts_last_agent_message_and_usage(self) -> None:
        stdout = "\n".join(
            [
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "first"}}),
                json.dumps({"type": "turn.completed", "usage": {"total_tokens": 42}}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "second"}}),
            ]
        )
        text, tokens = adapter.codex_text(stdout)
        self.assertEqual(text, "first\nsecond")
        self.assertEqual(tokens, 42.0)

    def test_installs_all_skill_packages_into_isolated_host_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "repo"
            skill = checkout / "skills/tk-example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            home = root / "codex"
            with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
                installed = adapter.install_skills("codex", checkout)
            self.assertEqual(installed, ["tk-example"])
            self.assertTrue((home / "skills/tk-example/SKILL.md").is_file())

    def test_missing_executable_is_an_unavailable_host(self) -> None:
        with patch.object(adapter.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                adapter.executable_for("codex")


if __name__ == "__main__":
    unittest.main()
