#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "install_user_guidance.py"


def run_installer(home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


class UserGuidanceInstallTests(unittest.TestCase):
    def test_all_skips_unconfigured_codex_and_claude(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            checked = run_installer(home, "--check", "--agent", "all")
            self.assertIn("skipped (claude-code not configured):", checked.stdout)
            self.assertIn("skipped (codex not configured):", checked.stdout)
            self.assertIn("skipped (SOUL.md not configured):", checked.stdout)
            self.assertNotIn("would create:", checked.stdout)
            self.assertNotIn("would update:", checked.stdout)

            applied = run_installer(home, "--apply", "--agent", "all")
            self.assertIn("skipped (claude-code not configured):", applied.stdout)
            self.assertIn("skipped (codex not configured):", applied.stdout)
            self.assertFalse((home / ".claude").exists())
            self.assertFalse((home / ".codex").exists())

    def test_existing_codex_directory_creates_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / ".codex").mkdir()

            checked = run_installer(home, "--check", "--agent", "codex")
            self.assertIn("would create:", checked.stdout)
            target = home / ".codex" / "AGENTS.md"
            self.assertFalse(target.exists())

            applied = run_installer(home, "--apply", "--agent", "codex")
            self.assertIn("created:", applied.stdout)
            self.assertTrue(target.is_file())
            self.assertIn("TIGERKIT_USER_GUIDANCE_BEGIN", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
