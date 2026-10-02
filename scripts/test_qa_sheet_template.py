"""Protect the bundled QA renderer without third-party test dependencies."""
from pathlib import Path
import subprocess
import unittest


class QASheetTemplateTest(unittest.TestCase):
    def test_renderer_behavior(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["node", "--test", "evals/skills/tk-qa-sheet/template.test.cjs"],
            cwd=root, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
