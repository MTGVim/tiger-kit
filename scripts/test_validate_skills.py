#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile
import unittest

from validate_skills import validate_release_behavior_fixtures, validate_runtime_scratch


class RuntimeScratchTest(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)

    def test_allows_ignored_runtime_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.init_repo(root)
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            (root / ".tigerkit").mkdir()
            (root / ".tigerkit" / "evidence.txt").write_text("local\n", encoding="utf-8")

            self.assertEqual(validate_runtime_scratch(root), [])

    def test_rejects_tracked_runtime_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.init_repo(root)
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            (root / ".tigerkit").mkdir()
            (root / ".tigerkit" / "evidence.txt").write_text("tracked\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "-f", ".tigerkit/evidence.txt"],
                cwd=root,
                check=True,
            )

            self.assertEqual(
                validate_runtime_scratch(root),
                [".tigerkit: remove tracked TigerKit runtime scratch"],
            )

    def test_rejects_runtime_scratch_in_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".tigerkit").mkdir()

            self.assertEqual(
                validate_runtime_scratch(root),
                [".tigerkit: remove TigerKit runtime scratch from packaged repository"],
            )


class ReleaseFixtureTest(unittest.TestCase):
    def test_maintainer_release_behavior_fixtures_validate(self) -> None:
        self.assertEqual(validate_release_behavior_fixtures(), [])


if __name__ == "__main__":
    unittest.main()
