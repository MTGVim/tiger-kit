#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("write_reflect_ledger.py")


class WriteReflectLedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repository = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q"], cwd=self.repository, check=True)
        self.scratch = self.repository / ".tigerkit"
        self.scratch.mkdir()
        self.source = self.scratch / "candidate-ledger.md"

    def run_writer(self, source: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo",
                str(self.repository),
                "--source",
                str(source or self.source),
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_writes_and_replaces_bounded_ledger(self) -> None:
        self.source.write_text("# Reflection ledger\n\nfirst\n", encoding="utf-8")
        first = self.run_writer()
        self.assertEqual(first.returncode, 0, first.stdout)
        target = self.scratch / "reflect.md"
        self.assertEqual(target.read_text(encoding="utf-8"), "# Reflection ledger\n\nfirst\n")
        self.assertEqual(target.stat().st_mode & 0o777, 0o600)

        self.source.write_text("# Reflection ledger\n\nsecond\n", encoding="utf-8")
        second = self.run_writer()
        self.assertEqual(second.returncode, 0, second.stdout)
        self.assertEqual(json.loads(second.stdout)["path"], ".tigerkit/reflect.md")
        self.assertEqual(target.read_text(encoding="utf-8"), "# Reflection ledger\n\nsecond\n")

    def test_rejects_noncanonical_or_sensitive_content(self) -> None:
        for content in (
            "not a ledger\n",
            "# Reflection ledger\n\ndiff --git a/x b/x\n",
            "# Reflection ledger\n\nAuthorization: Bearer secret\n",
        ):
            with self.subTest(content=content):
                self.source.write_text(content, encoding="utf-8")
                completed = self.run_writer()
                self.assertEqual(completed.returncode, 2)

    def test_rejects_source_outside_tigerkit(self) -> None:
        outside = self.repository / "ledger.md"
        outside.write_text("# Reflection ledger\n", encoding="utf-8")
        completed = self.run_writer(outside)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("inside .tigerkit", completed.stdout)


if __name__ == "__main__":
    unittest.main()
