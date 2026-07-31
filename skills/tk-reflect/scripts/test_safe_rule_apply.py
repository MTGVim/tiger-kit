#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("safe_rule_apply.py")


class SafeRuleApplyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name).resolve()
        self.repository = self.home / "repo"
        self.repository.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repository, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=self.repository,
            check=True,
        )
        (self.repository / ".gitignore").write_text(
            ".tigerkit/\n.ignored-rule.md\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".gitignore"], cwd=self.repository, check=True)
        subprocess.run(["git", "commit", "-qm", "initial"], cwd=self.repository, check=True)
        (self.repository / ".tigerkit").mkdir()
        self.candidate = self.repository / ".tigerkit" / "candidate.md"
        self.candidate.write_text("after\n", encoding="utf-8")
        self.environment = dict(os.environ, HOME=str(self.home))

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def command(
        self,
        *,
        target: Path,
        scope: str,
        validator: list[str] | None = None,
        user_managed: bool = True,
    ) -> list[str]:
        target_value = (
            str(target.relative_to(self.repository)) if scope == "repo" else str(target)
        )
        command = [
            sys.executable,
            str(SCRIPT),
            target_value,
            "--scope",
            scope,
            "--repo",
            str(self.repository),
            "--baseline-sha256",
            self.digest(target),
            "--candidate",
            str(self.candidate),
            "--validate-json",
            json.dumps(validator or [sys.executable, "-c", "raise SystemExit(0)"]),
        ]
        if user_managed:
            command.append("--user-managed")
        return command

    def run_apply(self, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            self.command(**kwargs),
            cwd=self.repository,
            env=self.environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_applies_repo_untracked_ignored_target(self) -> None:
        target = self.repository / ".ignored-rule.md"
        target.write_text("before\n", encoding="utf-8")
        completed = self.run_apply(target=target, scope="repo")
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(result["status"], "applied")
        self.assertEqual(result["git_state"], "untracked-ignored")
        self.assertIsNotNone(result["ignore_source"])
        self.assertEqual(target.read_text(encoding="utf-8"), "after\n")

    def test_applies_repo_untracked_visible_target(self) -> None:
        target = self.repository / ".visible-rule.md"
        target.write_text("before\n", encoding="utf-8")
        completed = self.run_apply(target=target, scope="repo")
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(result["git_state"], "untracked-visible")
        self.assertIsNone(result["ignore_source"])
        self.assertEqual(target.read_text(encoding="utf-8"), "after\n")

    def test_applies_existing_user_level_target(self) -> None:
        target = self.home / ".claude" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("before\n", encoding="utf-8")
        completed = self.run_apply(target=target, scope="user")
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(result["scope"], "user")
        self.assertEqual(result["git_state"], "not-applicable")
        self.assertEqual(target.read_text(encoding="utf-8"), "after\n")

    def test_rejects_tracked_repo_target(self) -> None:
        target = self.repository / "tracked.md"
        target.write_text("before\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.md"], cwd=self.repository, check=True)
        subprocess.run(["git", "commit", "-qm", "track rule"], cwd=self.repository, check=True)
        completed = self.run_apply(target=target, scope="repo")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("tracked targets", completed.stdout)
        self.assertEqual(target.read_text(encoding="utf-8"), "before\n")

    def test_rejects_user_scope_for_repo_local_target(self) -> None:
        target = self.repository / ".visible-rule.md"
        target.write_text("before\n", encoding="utf-8")
        completed = self.run_apply(target=target, scope="user")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("must use repo scope", completed.stdout)

    def test_requires_verified_user_managed_assertion(self) -> None:
        target = self.repository / ".visible-rule.md"
        target.write_text("before\n", encoding="utf-8")
        completed = self.run_apply(target=target, scope="repo", user_managed=False)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("user-managed ownership", completed.stdout)

    def test_failed_validation_restores_exact_before_image(self) -> None:
        target = self.repository / ".visible-rule.md"
        target.write_text("before\n", encoding="utf-8")
        baseline = self.digest(target)
        completed = self.run_apply(
            target=target,
            scope="repo",
            validator=[sys.executable, "-c", "raise SystemExit(9)"],
        )
        self.assertEqual(completed.returncode, 3, completed.stdout)
        self.assertEqual(json.loads(completed.stdout)["status"], "rolled-back")
        self.assertEqual(self.digest(target), baseline)
        self.assertEqual(target.read_text(encoding="utf-8"), "before\n")


if __name__ == "__main__":
    unittest.main()
