"""Cross-platform agent-only development-server lease contract tests.

These tests deliberately use disposable Git repositories and an inert Python child,
never a user's development server. Run via unittest on POSIX or native Windows.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/tk-browser-verify/scripts/dev_server_guard.py"


class DevServerGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        home = Path(self.temporary.name)
        self.root = home / "root"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run([
            "git", "-C", str(self.root), "-c", "user.email=test@example.invalid",
            "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "seed",
        ], check=True)
        self.secondary = home / "secondary"
        subprocess.run([
            "git", "-C", str(self.root), "worktree", "add", "-q", "-b", "other", str(self.secondary),
        ], check=True)
        self.run_ids = []
        self.addCleanup(self.stop_all)

    def command(self, action, root=None, extras=(), expect=0):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), action, "--repo", str(root or self.root), *extras],
            text=True, capture_output=True, timeout=45,
        )
        self.assertEqual(process.returncode, expect, process.stderr + process.stdout)
        return json.loads(process.stdout)

    def start(self, root):
        result = self.command("start", root, extras=(
            "--cwd", str(root), "--wait-seconds", "15", "--max-seconds", "30",
            "--", sys.executable, "-c", "import time;time.sleep(25)",
        ))
        self.assertEqual(result["status"], "queued")
        self.run_ids.append((root, result["run_id"]))
        return result["run_id"]

    def wait_status(self, root, run_id, expected, seconds=12):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            response = self.command("status", root, extras=("--run-id", run_id))
            if response["status"] == expected:
                return response
            if response["status"] in (
                "failed", "blocked-orphan", "cleanup-unverifiable", "timeout", "orphaned-or-exited",
            ):
                self.fail("unexpected guard state: " + response["status"])
            time.sleep(0.25)
        self.fail("server did not reach " + expected)

    def stop_all(self):
        for root, run_id in self.run_ids:
            try:
                subprocess.run(
                    [sys.executable, str(SCRIPT), "stop", "--repo", str(root),
                     "--run-id", run_id, "--seconds", "8"],
                    capture_output=True, timeout=20,
                )
            except (OSError, subprocess.TimeoutExpired):
                pass

    def test_different_worktrees_serialize_server_lifetimes(self):
        first = self.start(self.root)
        self.wait_status(self.root, first, "running")
        second = self.start(self.secondary)
        time.sleep(0.5)
        self.assertEqual(
            self.command("status", self.secondary, extras=("--run-id", second))["status"],
            "queued",
        )
        self.assertEqual(
            self.command("stop", extras=("--run-id", first, "--seconds", "10"))["status"],
            "stopped",
        )
        self.wait_status(self.secondary, second, "running")
        self.assertEqual(
            self.command("stop", self.secondary, extras=("--run-id", second, "--seconds", "10"))["status"],
            "stopped",
        )

    def test_cannot_stop_another_worktrees_process(self):
        first = self.start(self.root)
        self.wait_status(self.root, first, "running")
        self.assertEqual(
            self.command("stop", self.secondary, extras=("--run-id", first), expect=2)["status"],
            "blocked",
        )
        self.assertEqual(
            self.command("status", extras=("--run-id", first))["status"], "running",
        )

    def test_user_owned_process_is_not_terminated(self):
        unrelated = subprocess.Popen(
            [sys.executable, "-c", "import time;time.sleep(20)"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        try:
            first = self.start(self.root)
            self.wait_status(self.root, first, "running")
            self.command("stop", extras=("--run-id", first, "--seconds", "10"))
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.terminate()
            unrelated.wait(timeout=8)


if __name__ == "__main__":
    unittest.main()
