#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("record_eval_event.py")


class RecordEvalEventTest(unittest.TestCase):
    def test_appends_strict_phase_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            env = os.environ.copy()
            env["TK_DRIVE_EVENT_LOG"] = str(event_log)

            subprocess.run(
                [sys.executable, str(SCRIPT), "phase_invocation", "tk-to-spec"],
                env=env,
                check=True,
            )
            subprocess.run(
                [sys.executable, str(SCRIPT), "phase_invocation", "tk-implement"],
                env=env,
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "phase_receipt",
                    "tk-implement",
                    "Pass",
                    "aggregate verification",
                ],
                env=env,
                check=True,
            )

            rows = [
                json.loads(line)
                for line in event_log.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                rows,
                [
                    {"type": "phase_invocation", "phase": "tk-to-spec"},
                    {"type": "phase_invocation", "phase": "tk-implement"},
                    {
                        "type": "phase_receipt",
                        "phase": "tk-implement",
                        "state": "Pass",
                        "transition": "aggregate verification",
                    },
                ],
            )
            self.assertEqual(event_log.stat().st_mode & 0o777, 0o600)

    def test_rejects_unknown_phase_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            env = os.environ.copy()
            env["TK_DRIVE_EVENT_LOG"] = str(event_log)

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "phase_invocation", "tk-unknown"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(event_log.exists())


if __name__ == "__main__":
    unittest.main()
