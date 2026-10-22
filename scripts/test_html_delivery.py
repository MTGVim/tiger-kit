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
        references=list((ROOT/'skills').glob('*/references/html-output.md'))
        self.assertEqual(len(references),8)
        for path in references:
            with self.subTest(package=path.parts[-3]):
                self.assertIn('omit automatic AI-authorship notices',path.read_text())
                chart=path.parents[1]/'assets/chart-examples.html'
                self.assertNotIn('🤖',chart.read_text())
                self.assertNotIn('AI가 작성',chart.read_text())
