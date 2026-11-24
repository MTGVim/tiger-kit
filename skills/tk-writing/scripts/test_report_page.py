#!/usr/bin/env python3
"""Regression tests for the report builder and report-shell checks."""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_page
import check_page
import deliver_page


class ReportPageTests(unittest.TestCase):
    def setUp(self):
        self.args = SimpleNamespace(lang="ko", toc_label="목차", css=build_page.asset("page.css"),
                                    js=build_page.asset("page.js"), no_download=True)
        self.manuscript = "# 요청 문서\n\n## 요청\n> 진행 방향을 검토해 주세요.\n\n## 참고 부록 ~~\n### 세부 근거\n\n- 결정: 추후 확인\n"

    def test_folded_appendix_has_one_toc_entry_and_one_details(self):
        page = build_page.build(self.manuscript, self.args)
        self.assertIn('<section id="s2" class="is-quiet is-folded"', page)
        self.assertIn('<details class="rp-fold"><summary><h2 id="s2-h">참고 부록</h2></summary>', page)
        self.assertEqual(page.count('<details class="rp-fold">'), 1)
        self.assertEqual(page.count('<li><a href="#s2">참고 부록</a></li>'), 1)
        self.assertNotIn('~~</h2>', page)
        self.assertEqual(check_page.static_check(page), [])

    def test_old_quiet_section_does_not_fold(self):
        page = build_page.build("# 제목\n\n## 부록 ~\n내용", self.args)
        self.assertIn('<section id="s1" aria-labelledby="s1-h" class=is-quiet>', page)
        self.assertNotIn('<details class="rp-fold">', page)

    def test_no_download_removes_controls_status_and_export(self):
        page = build_page.build(self.manuscript, self.args)
        self.assertNotIn('<button type="button" data-ht-download', page)
        self.assertNotIn('<span data-ht-export-status', page)
        self.assertNotIn('<template data-ht-export', page)
        self.assertEqual(check_page.static_check(page), [])

    def test_default_retains_download_control(self):
        self.args.no_download = False
        page = build_page.build(self.manuscript, self.args)
        self.assertIn('<button type="button" data-ht-download', page)
        self.assertTrue(any('download button without embedded export' in error
                            for error in check_page.static_check(page)))

    def test_manual_toc_is_not_a_valid_report_shell(self):
        manual = '<html><body><h1>제목</h1><nav class="toc">목차</nav></body></html>'
        errors = check_page.static_check(manual)
        self.assertTrue(any('report shell missing' in error for error in errors))
        self.assertFalse(any('one shell TOC' in error for error in errors))

    def test_shell_without_toc_reports_rebuild_instead_of_manual_toc(self):
        page = build_page.build(self.manuscript, self.args)
        page = page.replace('<nav class="toc"', '<nav class="other"')
        self.assertTrue(any('one shell TOC' in error and 'build_page.py' in error
                            for error in check_page.static_check(page)))

    def test_report_css_controls_are_in_pixels_and_rowspan_has_background(self):
        css = Path(self.args.css).read_text(encoding="utf-8")
        self.assertIn('.rp-tools { position: sticky; font-size: 14px;', css)
        self.assertIn('tbody td[rowspan], tbody th[rowspan] { background: var(--bg); }', css)
        js = Path(self.args.js).read_text(encoding="utf-8")
        self.assertIn("'80'", js)
        self.assertIn("'130'", js)

    def test_report_zoom_keeps_toolbar_dimensions(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            if os.environ.get("REPORT_BROWSER_REQUIRED"):
                self.fail("Playwright is required for report browser regression checks")
            self.skipTest("Playwright is not installed")
        html = build_page.build(self.manuscript, self.args)
        evidence = Path("artifacts")
        evidence.mkdir(exist_ok=True)
        with sync_playwright() as playwright:
            executable = (shutil.which("chromium") or shutil.which("google-chrome")
                          or shutil.which("google-chrome-stable"))
            browser = playwright.chromium.launch(headless=True, **(
                {"executable_path": executable} if executable else {}))
            try:
                for width in (375, 1440):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    page.set_content(html, wait_until="load")
                    select = page.locator("[data-ht-font-size]")
                    select.wait_for()
                    metrics = {}
                    for size in ("100", "80", "130"):
                        select.select_option(size)
                        metrics[size] = page.evaluate("""() => {
                            const rect = el => {
                                const r = el.getBoundingClientRect();
                                return [r.width, r.height];
                            };
                            return {
                                bar: rect(document.querySelector('.rp-tools')),
                                select: rect(document.querySelector('[data-ht-font-size]')),
                                theme: rect(document.querySelector('.rp-tools .ht-theme-option > span')),
                                rootFont: parseFloat(getComputedStyle(document.documentElement).fontSize)
                            };
                        }""")
                        page.screenshot(path=str(evidence / f"report-zoom-{width}-{size}.png"))
                    for size in ("80", "130"):
                        for control in ("bar", "select", "theme"):
                            for before, after in zip(metrics["100"][control], metrics[size][control]):
                                self.assertAlmostEqual(before, after, delta=1,
                                                       msg=f"{width}px {control} changed at {size}%")
                        self.assertNotEqual(metrics["100"]["rootFont"], metrics[size]["rootFont"])
                    page.close()
            finally:
                browser.close()

    def test_no_download_delivery_skips_packaging(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, result = base / 'source.html', base / 'result.html'
            source.write_text(build_page.build(self.manuscript, self.args), encoding='utf-8')
            called = []
            def fake_run(command, check):
                script = Path(command[1]).name
                called.append(script)
                if script == "add_feedback_studio.py":
                    result.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            with patch.object(deliver_page.subprocess, 'run', side_effect=fake_run):
                deliver_page.deliver(source, result)
            self.assertEqual(called, ['add_feedback_studio.py', 'check_page.py'])
            self.assertNotIn('<template data-ht-export', result.read_text(encoding="utf-8"))


if __name__ == '__main__':
    unittest.main()
