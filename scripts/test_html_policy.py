"""Exercise shared-contract validation with installed-package mutations."""
import re
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

    def test_templates_declare_system_generation_default(self):
        for relative in ('skills/tk-research/assets/report.html', 'skills/tk-qa-sheet/assets/qa-sheet-template.html'):
            text = (ROOT / relative).read_text()
            self.assertIn('data-default-theme="system"', text)

    def test_templates_use_native_segmented_theme_radios(self):
        for relative in ('skills/tk-research/assets/report.html', 'skills/tk-qa-sheet/assets/qa-sheet-template.html'):
            text = (ROOT / relative).read_text()
            self.assertIn('<fieldset class="ht-theme-control"', text)
            self.assertIn('data-ht-theme-control', text)
            self.assertIn('name="ht-theme"', text)
            self.assertNotIn('<select id="ht-theme"', text)
            for value in ('system', 'light', 'dark'):
                self.assertIn(f'value="{value}"', text)

    def test_templates_avoid_page_level_mobile_overflow_patterns(self):
        report = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        qa = (ROOT / 'skills/tk-qa-sheet/assets/qa-sheet-template.html').read_text()
        self.assertNotIn('nav ul{display:flex;overflow:auto', report)
        self.assertNotIn('flex-wrap: wrap', qa)
        self.assertIn('grid-template-columns:repeat(2,minmax(0,1fr))', report)
        self.assertIn('header > * { min-width: 0; max-width: 100%; }', qa)
        environment = re.search(r'\.environment\s*\{([^}]*)\}', qa)
        self.assertIsNotNone(environment)
        self.assertRegex(environment.group(1), r'white-space\s*:\s*normal\s*;')
        self.assertRegex(environment.group(1), r'overflow-wrap\s*:\s*anywhere\s*;')
        self.assertIn('grid-template-areas: "title environment environment environment" "progress filter theme reset"', qa)
        self.assertIn('min-width: min(14rem, 100%)', qa)
        self.assertIn('class="only-open-filter"', qa)

    def test_shared_contract_contains_render_safe_authoring_rules(self):
        text = (ROOT / 'skills/tk-explain/references/html-output.md').read_text()
        self.assertIn('## Render-safe authoring', text)
        self.assertIn('11 CSS px after scaling', text)
        self.assertIn('emulated mobile CSS viewport width matching `innerWidth`', text)
        self.assertIn('`.ht-token`', text)

    def test_clear_writing_rejects_fragmentary_korean_headings(self):
        text = (ROOT / 'skills/tk-rewrite/references/clear-writing.md').read_text()
        self.assertIn('요청 함수의 이동 위치', text)
        self.assertIn('colloquial interrogative ending', text)
        self.assertIn('dangling connective ending', text)

    def test_final_head_replay_and_reason_first_auth_contracts(self):
        local = (ROOT / 'skills/tk-prep/references/local-execution.md').read_text()
        lifecycle = (ROOT / 'skills/tk-browser-verify/references/session-lifecycle.md').read_text()
        results = (ROOT / 'skills/tk-browser-verify/references/results.md').read_text()
        environment = (ROOT / 'skills/tk-browser-verify/references/environment.md').read_text()
        qa = (ROOT / 'skills/tk-qa-sheet/SKILL.md').read_text()
        self.assertIn("intervening diff touches a runtime-verified screen's render path or request path", local)
        self.assertIn('replay the same', local)
        self.assertIn('After any baseline, after, or acceptance capture', lifecycle)
        self.assertIn('stop the run-owned development server immediately', lifecycle)
        self.assertIn('Do not defer secret cleanup until browser-session cleanup', lifecycle)
        self.assertNotIn('defer normal cleanup', lifecycle)
        self.assertIn('no baseline-to-final-head process hold', results)
        self.assertIn('freshly owned runtime resources', local)
        self.assertIn('Before showing paths or input mechanics', environment)
        self.assertIn('why the existing evidence or authenticated state cannot satisfy it', environment)
        self.assertIn('what a recapture needs', qa)
        self.assertIn('why the old evidence/session cannot satisfy it', qa)

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
            path = root / 'skills/tk-teach/assets/html-theme.css'
            path.parent.mkdir(exist_ok=True)
            path.write_text(':root { --bg: red; }\n')
        self.check_mutation(mutate)

    def test_clear_writing_drift_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-qa-sheet/references/clear-writing.md'
            path.write_text('# drift\n')
        self.check_mutation(mutate)

    def test_templates_avoid_generic_reader_order_headings(self):
        for relative in ('skills/tk-research/assets/report.html', 'skills/tk-qa-sheet/assets/qa-sheet-template.html'):
            text = (ROOT / relative).read_text()
            for phrase in ('먼저 볼 것', '먼저 확인할 것', '처음 읽는 분께'):
                self.assertNotIn(phrase, text)

    def test_feedback_guard_loss_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-teach/SKILL.md'
            text = path.read_text()
            start = text.find('<!-- tigerkit:skill-feedback -->')
            end = text.find('<!-- /tigerkit:skill-feedback -->', start)
            if start >= 0 and end >= 0:
                text = text[:start] + text[end + len('<!-- /tigerkit:skill-feedback -->'):]
            path.write_text(text)
        self.check_mutation(mutate)


if __name__ == '__main__':
    unittest.main()
