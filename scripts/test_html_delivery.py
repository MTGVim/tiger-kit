"""User-delivered files keep provenance and omit automatic authorship labels."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class HtmlDeliveryTests(unittest.TestCase):
    def test_only_direct_remote_posting_packages_keep_robot_marker(self):
        marked=set()
        for path in (ROOT/'skills').rglob('*'):
            if path.is_file() and '🤖' in path.read_text(errors='replace'):
                marked.add(path.relative_to(ROOT/'skills').parts[0])
        self.assertEqual(marked,{'tk-pr-respond','tk-pr-rebase'})
        for name in marked:
            self.assertIn('_🤖 본 코멘트는 AI가 작성했습니다._',(ROOT/f'skills/{name}/SKILL.md').read_text())

    def test_all_shared_html_consumers_keep_delivery_boundary_and_chart_notice_removed(self):
        from shared_references import link_error
        reference = ROOT / 'skills/tk-writing/references/html-output.md'
        self.assertIn('omit automatic AI-authorship notices', reference.read_text())
        self.assertFalse(reference.is_symlink())
        for owner in ('tk-explain', 'tk-research', 'tk-prototype', 'tk-qa-sheet', 'tk-blind-comparison'):
            package = ROOT / 'skills' / owner
            self.assertFalse((package / 'references/html-output.md').exists())
            self.assertIsNone(link_error(package / 'SKILL.md', '../tk-writing/references/html-output.md', ROOT / 'skills'))
            chart = package / 'assets/chart-examples.html'
            self.assertNotIn('🤖', chart.read_text())
            self.assertNotIn('AI가 작성', chart.read_text())
