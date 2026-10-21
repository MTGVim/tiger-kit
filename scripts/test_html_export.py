"""Check the offline export boundary and exercise actual browser-script output bytes."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('html_export', ROOT / 'skills/tk-explain/scripts/package_html.py')
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)


class ExportTest(unittest.TestCase):
    def test_source_bytes_zip_integrity_reexport_and_share_contract(self):
        result = subprocess.run(['node', '--test', 'evals/skills/tk-explain/export.test.cjs'],
                                cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_link_or_unsafe_path_does_not_mutate_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / 'index.html'
            source = '<html><body><a href="lesson.html">Lesson</a></body></html>'
            page.write_text(source)
            for names in (['index.html'], ['../outside.html'], ['.env'], ['index.html', './index.html']):
                with self.assertRaises(ValueError):
                    export.package(root, names, 'course.zip')
                self.assertEqual(page.read_text(), source)
            (root / 'lesson.html').symlink_to(page)
            with self.assertRaises(ValueError):
                export.package(root, ['index.html', 'lesson.html'], 'course.zip')
            self.assertEqual(page.read_text(), source)

    def test_mcp_default_disables_optional_statistics_and_does_not_rewrite_existing_registrations(self):
        text = (ROOT / 'skills/tk-browser-verify/references/environment.md').read_text()
        self.assertIn('"--headless", "--isolated", "--no-usage-statistics"', text)
        self.assertIn('Existing registrations are unchanged', text)
        wizard = (ROOT / 'skills/tk-wizard/references/consumer-handoffs.md').read_text()
        self.assertIn('"--headless", "--isolated", "--no-usage-statistics"', wizard)

    def test_icon_controls_keep_accessible_names_and_actions_precede_theme(self):
        from html.parser import HTMLParser
        class Controls(HTMLParser):
            def __init__(self):
                super().__init__()
                self.order = []
                self.names = []
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'data-ht-download' in attrs: self.order.append('download')
                if 'data-ht-theme-control' in attrs: self.order.append('theme')
                if tag == 'input' and attrs.get('name') == 'ht-theme':
                    self.names.append(attrs.get('aria-label'))
        for relative in ('skills/tk-research/assets/report.html', 'skills/tk-qa-sheet/assets/qa-sheet-template.html'):
            parser = Controls()
            parser.feed((ROOT / relative).read_text())
            self.assertEqual(parser.order, ['download', 'theme'])
            self.assertEqual(parser.names, ['시스템', '라이트', '다크'])


if __name__ == '__main__':
    unittest.main()
