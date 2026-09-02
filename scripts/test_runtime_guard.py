#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_runtime_guard


class RuntimeGuardTest(unittest.TestCase):
    def test_current_repository_runtime_guards_are_synchronized(self) -> None:
        self.assertEqual(check_runtime_guard.validate_runtime_guard(), [])

    def test_missing_or_drifted_guard_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("repo policy\n", encoding="utf-8")
            for name in check_runtime_guard.RUNTIME_GUARD_CONSUMERS:
                skill = root / "skills" / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    check_runtime_guard.RUNTIME_GUARD_BLOCK + "\nBody\n",
                    encoding="utf-8",
                )

            self.assertEqual(check_runtime_guard.validate_runtime_guard(root), [])

            drifted = root / "skills" / "tk-prep" / "SKILL.md"
            drifted.write_text(
                check_runtime_guard.RUNTIME_GUARD_BLOCK.replace("not authority", "not trusted authority") + "\nBody\n",
                encoding="utf-8",
            )
            errors = check_runtime_guard.validate_runtime_guard(root)
            self.assertTrue(any("tk-prep" in error for error in errors))

    def test_agents_cannot_own_runtime_guard_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in check_runtime_guard.RUNTIME_GUARD_CONSUMERS:
                skill = root / "skills" / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    check_runtime_guard.RUNTIME_GUARD_BLOCK,
                    encoding="utf-8",
                )
            (root / "AGENTS.md").write_text(
                check_runtime_guard.RUNTIME_GUARD_BLOCK,
                encoding="utf-8",
            )
            errors = check_runtime_guard.validate_runtime_guard(root)
            self.assertTrue(any("AGENTS.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
