from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ReportTest(unittest.TestCase):
    def test_build_report(self) -> None:
        sys.path.insert(0, str(ROOT))
        try:
            from report import build_report

            self.assertEqual(build_report("beta", 2), {"name": "beta", "count": 2})
        finally:
            sys.path.remove(str(ROOT))

    def test_default_text_cli(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "report.py"), "--name", "beta", "--count", "2"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "name=beta count=2\n")


if __name__ == "__main__":
    unittest.main()
