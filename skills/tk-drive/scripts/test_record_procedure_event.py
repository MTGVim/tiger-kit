#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("record_procedure_event.py")


class ProcedureEventTest(unittest.TestCase):
    def test_records_only_canonical_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            env = {**os.environ, "TK_DRIVE_PROCEDURE_LOG": str(path)}
            completed = subprocess.run(
                [str(SCRIPT), "tk-implement"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                {"type": "phase_invocation", "phase": "tk-implement"},
            )

    def test_records_remote_publication_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            env = {**os.environ, "TK_DRIVE_PROCEDURE_LOG": str(path)}
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "remote-publish"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                {"type": "phase_invocation", "phase": "remote-publish"},
            )

    def test_rejects_unknown_phase_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            env = {**os.environ, "TK_DRIVE_PROCEDURE_LOG": str(path)}
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "tk-implment"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertFalse(path.exists())
