"""Exercise shared-contract validation with installed-package mutations."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HTMLPolicyTest(unittest.TestCase):
    def check_mutation(self, mutate):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('skills', 'scripts'):
                shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
            mutate(root)
            result = subprocess.run([sys.executable, 'scripts/sync_execution_protocol.py', '--check'],
                                    cwd=root, text=True, capture_output=True, timeout=30)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_theme_control_behavior(self):
        result = subprocess.run(['node', '--test', 'evals/skills/tk-explain/theme.test.cjs'],
                                cwd=ROOT, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_canonical_theme_blocks_release_check(self):
        self.check_mutation(lambda root: (root / 'skills/tk-explain/assets/html-theme.css').unlink())

    def test_template_theme_drift_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-research/assets/report.html'
            text = path.read_text()
            # A template with its own root rule can diverge from the package tokens.
            path.write_text(text.replace('--bg:', '--background:', 1))
        self.check_mutation(mutate)

    def test_package_theme_drift_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-study/assets/html-theme.css'
            path.parent.mkdir(exist_ok=True)
            path.write_text(':root { --bg: red; }\n')
        self.check_mutation(mutate)

    def test_feedback_guard_loss_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-study/SKILL.md'
            text = path.read_text()
            start = text.find('<!-- tigerkit:skill-feedback -->')
            end = text.find('<!-- /tigerkit:skill-feedback -->', start)
            if start >= 0 and end >= 0:
                text = text[:start] + text[end + len('<!-- /tigerkit:skill-feedback -->'):]
            path.write_text(text)
        self.check_mutation(mutate)


if __name__ == '__main__':
    unittest.main()
