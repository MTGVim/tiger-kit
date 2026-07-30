#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("ignored_rule_apply.py")


class IgnoredRuleApplyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repository = Path(self.temporary.name).resolve()
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
            ".tigerkit/\n.local-rule.md\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", ".gitignore"],
            cwd=self.repository,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "initial"],
            cwd=self.repository,
            check=True,
        )
        self.target = self.repository / ".local-rule.md"
        self.target.write_text("before\n", encoding="utf-8")
        (self.repository / ".tigerkit").mkdir()
        self.candidate = self.repository / ".tigerkit" / "candidate.md"
        self.candidate.write_text("after\n", encoding="utf-8")

    def digest(self, path: Path | None = None) -> str:
        return hashlib.sha256((path or self.target).read_bytes()).hexdigest()

    def command(
        self,
        *,
        target: str = ".local-rule.md",
        baseline: str | None = None,
        candidate: Path | None = None,
        validator: list[str] | None = None,
    ) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT),
            target,
            "--repo",
            str(self.repository),
            "--baseline-sha256",
            baseline or self.digest(),
            "--candidate",
            str(candidate or self.candidate),
            "--validate-json",
            json.dumps(
                validator
                or [
                    sys.executable,
                    "-c",
                    (
                        "from pathlib import Path; "
                        "assert Path('.local-rule.md').read_text() == 'after\\n'"
                    ),
                ]
            ),
        ]

    def run_apply(self, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            self.command(**kwargs),
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_applies_existing_ignored_target_with_secure_backup(self) -> None:
        initial_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

        completed = self.run_apply()

        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertEqual(json.loads(completed.stdout)["status"], "applied")
        self.assertEqual(self.target.read_text(encoding="utf-8"), "after\n")
        backup = self.repository / ".tigerkit/reflect-backup/before.bin"
        self.assertEqual(backup.read_text(encoding="utf-8"), "before\n")
        self.assertEqual(backup.stat().st_mode & 0o777, 0o600)
        final_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(final_head, initial_head)

    def test_rejects_tracked_target_before_write(self) -> None:
        subprocess.run(
            ["git", "add", "-f", ".local-rule.md"],
            cwd=self.repository,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "track rule"],
            cwd=self.repository,
            check=True,
        )

        completed = self.run_apply()

        self.assertEqual(completed.returncode, 2)
        self.assertIn("tracked targets", completed.stdout)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "before\n")

    def test_rejects_new_external_symlink_and_ambiguous_targets(self) -> None:
        outside = self.repository.parent / f"{self.repository.name}-outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        symlink = self.repository / "linked-rule.md"
        symlink.symlink_to(outside)
        cases = (
            "missing-rule.md",
            "../outside.md",
            "linked-rule.md",
            "*.md",
        )
        for target in cases:
            with self.subTest(target=target):
                completed = self.run_apply(target=target)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")
                self.assertEqual(self.target.read_text(encoding="utf-8"), "before\n")

    def test_rejects_target_changed_since_baseline(self) -> None:
        stale = self.digest()
        self.target.write_text("changed externally\n", encoding="utf-8")

        completed = self.run_apply(baseline=stale)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("changed since", completed.stdout)
        self.assertEqual(
            self.target.read_text(encoding="utf-8"), "changed externally\n"
        )

    def test_failed_validation_restores_exact_before_image(self) -> None:
        baseline = self.digest()

        completed = self.run_apply(
            baseline=baseline,
            validator=[sys.executable, "-c", "raise SystemExit(9)"],
        )

        self.assertEqual(completed.returncode, 3, completed.stdout)
        self.assertEqual(json.loads(completed.stdout)["status"], "rolled-back")
        self.assertEqual(self.digest(), baseline)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "before\n")

    def test_rejects_candidate_outside_tigerkit(self) -> None:
        outside_candidate = self.repository / "candidate.md"
        outside_candidate.write_text("after\n", encoding="utf-8")

        completed = self.run_apply(candidate=outside_candidate)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("inside .tigerkit", completed.stdout)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "before\n")

    def test_rejects_symlink_candidate_inside_tigerkit(self) -> None:
        real_candidate = self.repository / ".tigerkit" / "real.md"
        real_candidate.write_text("after\n", encoding="utf-8")
        linked_candidate = self.repository / ".tigerkit" / "linked.md"
        linked_candidate.symlink_to(real_candidate)

        completed = self.run_apply(candidate=linked_candidate)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("non-symlink", completed.stdout)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "before\n")


if __name__ == "__main__":
    unittest.main()
