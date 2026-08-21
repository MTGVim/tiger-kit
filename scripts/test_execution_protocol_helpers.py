#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / "skills/tk-prep"
RESPOND = ROOT / "skills/tk-pr-respond"
SHARED = (
    Path("references/testing.md"),
    Path("references/sdd.md"),
    Path("scripts/sdd-unit-brief.py"),
    Path("scripts/sdd-review-package.py"),
)
HELPERS = (
    Path("scripts/sdd-unit-brief.py"),
    Path("scripts/sdd-review-package.py"),
)


class ExecutionProtocolHelpersTest(unittest.TestCase):
    def run_python(self, script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=cwd or ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_shared_protocol_copies_match_canonical_package(self) -> None:
        for relative in SHARED:
            canonical = PREP / relative
            consumer = RESPOND / relative
            self.assertTrue(canonical.is_file(), relative)
            self.assertTrue(consumer.is_file(), relative)
            self.assertEqual(consumer.read_bytes(), canonical.read_bytes(), relative)
            self.assertEqual(
                bool(consumer.stat().st_mode & 0o111),
                bool(canonical.stat().st_mode & 0o111),
                relative,
            )
        for relative in HELPERS:
            self.assertTrue((PREP / relative).stat().st_mode & 0o111, relative)
            self.assertTrue((RESPOND / relative).stat().st_mode & 0o111, relative)

    def test_sync_check_covers_references_and_helpers(self) -> None:
        completed = self.run_python(ROOT / "scripts/sync_execution_protocol.py", "--check")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("synchronized", completed.stdout.lower())

    def test_unit_brief_extracts_exact_global_constraints_and_one_unit(self) -> None:
        seed = """<!-- tigerkit:seed -->
Status: Ready
Task identity: fixture

```md
### Unit 99: fake
```

## Execution

Execution shape: SDD

### Global constraints
- exact literal: KEEP_ME

### Unit 1: Parser
- Goal: parser
- Scope: one

### Unit 2: API
- Goal: api
- Scope: two
- Acceptance criteria: AC-2

## Verification
- later
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_path = root / "seed.md"
            output = root / "unit-2.md"
            seed_path.write_text(seed, encoding="utf-8")
            completed = self.run_python(
                PREP / "scripts/sdd-unit-brief.py",
                str(seed_path),
                "2",
                str(output),
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("### Global constraints", text)
            self.assertIn("KEEP_ME", text)
            self.assertIn("### Unit 2: API", text)
            self.assertIn("AC-2", text)
            self.assertNotIn("Unit 1: Parser", text)
            self.assertNotIn("Unit 99: fake", text)
            self.assertNotIn("## Verification", text)

    def test_unit_brief_rejects_nonsequential_units(self) -> None:
        seed = """## Execution
Execution shape: SDD
### Global constraints
- stable
### Unit 1: One
- Goal: one
### Unit 3: Three
- Goal: three
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed_path = root / "seed.md"
            output = root / "unit.md"
            seed_path.write_text(seed, encoding="utf-8")
            completed = self.run_python(
                PREP / "scripts/sdd-unit-brief.py",
                str(seed_path),
                "1",
                str(output),
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())
            self.assertIn("sequential", completed.stderr)

    def test_review_package_covers_exact_multi_commit_range(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "TigerKit Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "tigerkit@example.invalid"], cwd=repo, check=True)
            (repo / "a.txt").write_text("alpha\n", encoding="utf-8")
            subprocess.run(["git", "add", "--", "a.txt"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
            base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()

            (repo / "a.txt").write_text("alpha\nbeta\n", encoding="utf-8")
            subprocess.run(["git", "add", "--", "a.txt"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "first change"], cwd=repo, check=True)
            (repo / "b.txt").write_text("gamma\n", encoding="utf-8")
            subprocess.run(["git", "add", "--", "b.txt"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "second change"], cwd=repo, check=True)
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()

            output = repo / "review.diff"
            completed = self.run_python(
                PREP / "scripts/sdd-review-package.py",
                base,
                head,
                str(output),
                cwd=repo,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn(f"Base: {base}", text)
            self.assertIn(f"Head: {head}", text)
            self.assertIn("first change", text)
            self.assertIn("second change", text)
            self.assertIn("a.txt", text)
            self.assertIn("b.txt", text)
            self.assertIn("+beta", text)
            self.assertIn("+gamma", text)


if __name__ == "__main__":
    unittest.main()
