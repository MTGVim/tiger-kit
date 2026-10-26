import json
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


class ResearchReportTest(unittest.TestCase):
    def report_html(self, *, navigation=True, empty_navigation=False):
        root = Path(__file__).resolve().parents[1]
        template = (root / 'skills/tk-research/assets/report.html').read_text(encoding='utf-8')
        style = re.search(r'<style\b[^>]*>.*?</style>', template, re.I | re.S).group()
        script = re.search(r'<script\b[^>]*>.*?</script>', template, re.I | re.S).group()
        if not navigation:
            nav = ''
        elif empty_navigation:
            nav = '''
<nav class="ht-doc-nav"></nav><nav class="ht-doc-controls"></nav>
'''
        else:
            nav = '''
<nav class="ht-doc-nav"><a href="#overview">Overview</a><a href="#evidence">Evidence</a><a href="#verification">Verification</a><a href="#sources">Sources</a></nav>
<nav class="ht-doc-controls"><a href="#document-top">Top</a><a href="#document-bottom">Bottom</a></nav>
'''
        return f'''<!doctype html>
<html lang="en" data-default-theme="system"><head><title>Evidence-backed report</title>{style}</head><body class="ht-document" id="document-top">
<header class="ht-topbar"><p class="ht-topbar-title">A decision supported by current evidence</p><fieldset class="ht-theme-control" data-ht-theme-control hidden><legend class="ht-theme-label">Theme</legend><div class="ht-theme-buttons"><label class="ht-theme-option"><input type="radio" name="ht-theme" value="system"><span>System</span></label><label class="ht-theme-option"><input type="radio" name="ht-theme" value="light"><span>Light</span></label><label class="ht-theme-option"><input type="radio" name="ht-theme" value="dark"><span>Dark</span></label></div></fieldset></header>
<main class="ht-doc-content">
  <section id="overview"><h2>Overview</h2><p>A substantive conclusion supported by current evidence.<sup id="cite-1-1"><a href="#ref-1">[1]</a></sup></p></section>
  <section id="evidence"><h2>Evidence</h2><p>Evidence summary.</p></section>
  <section id="verification"><h2>Verification</h2></section>
  <section id="sources"><h2>Sources</h2><ol><li id="ref-1"><a href="https://example.test/source">Source</a> <a href="#cite-1-1">↩ 1</a></li></ol></section>
</main>
<footer id="document-bottom">정본은 연구 자료입니다.</footer>
{nav}
{script}
</body></html>'''

    def check_report(self, html):
        root = Path(__file__).resolve().parents[1]
        checker = root / 'skills/tk-research/scripts/check_report.py'
        with tempfile.TemporaryDirectory(prefix='tk-research-report-test-') as temp_dir:
            report_path = Path(temp_dir) / 'report.html'
            report_path.write_text(html, encoding='utf-8')
            return subprocess.run(
                ['python3', str(checker), str(report_path)],
                capture_output=True, text=True, check=False)

    def assert_rejected(self, html, expected_message):
        result = self.check_report(html)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected_message, result.stderr)

    def test_report_checker_accepts_template_and_complete_report(self):
        root = Path(__file__).resolve().parents[1]
        checker = root / 'skills/tk-research/scripts/check_report.py'
        template = root / 'skills/tk-research/assets/report.html'
        result = subprocess.run(
            ['python3', str(checker), str(template)],
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.check_report(self.report_html())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_theme_labels_require_styled_input_span_structure(self):
        html = self.report_html()
        for replacement in ('System', '<span> </span>', '<em>System</em>',
                            '<em></em><span>System</span>'):
            with self.subTest(replacement=replacement):
                self.assert_rejected(html.replace('<span>System</span>', replacement),
                                     'non-empty span')
        self.assert_rejected(html.replace('class="ht-theme-option"', 'class="other"'),
                             'all theme inputs')
        self.assert_rejected(html.replace('type="radio"', 'type="text"'), 'radio input')

    def test_toc_labels_preserve_target_heading_text(self):
        html = self.report_html()
        self.assert_rejected(html.replace('href="#evidence">Evidence', 'href="#evidence">Facts'),
                             "target heading's full text")
        for label in ('Short label<small>Evidence</small>', ' Evidence\n '):
            with self.subTest(label=label):
                result = self.check_report(html.replace('href="#evidence">Evidence',
                                                       'href="#evidence">' + label))
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_renderer_builds_checked_report_and_resolves_theme_preference(self):
        root = Path(__file__).resolve().parents[1]
        renderer = root / 'skills/tk-research/scripts/render_report.py'
        checker = root / 'skills/tk-research/scripts/check_report.py'
        payload = {
            'title': 'ETag {{REPORT_META}} validation supports efficient cache checks',
            'topbar_title': '{{REPORT_TITLE}} lets the server confirm whether a cached response changed',
            'meta': 'Official documentation reviewed on 2026-10-16: {{REPORT_TOPBAR_TITLE}}.',
            'sections': [
                {
                    'id': 'overview',
                    'title': '목표와 결론',
                    'html': '<p>ETag validation reduces transfer when a representation is unchanged.'
                            '<sup id="cite-1"><a href="#ref-1">[1.1]</a></sup>'
                            '<sup id="cite-2"><a href="#ref-1">[1.2]</a></sup></p>',
                },
                {
                    'id': 'verification',
                    'title': '검증 및 예외',
                    'html': '<ul><li><strong>정적 검증:</strong> 완료.</li>'
                            '<li><strong>화면 검증:</strong> 검증 불가. 화면 검증이 필요하지 않은 단순 보고서.</li></ul>'
                            '<p>{{REPORT_TITLE}} and {{REPORT_META}}</p>',
                },
            ],
            'sources': [
                {
                    'id': 'ref-1', 'title': 'HTTP caching documentation',
                    'url': 'https://example.test/http-cache', 'local_path': '',
                    'date': '2026-10-16', 'revision': 'current',
                    'link_unavailable': False, 'citations': ['cite-1', 'cite-2'],
                },
            ],
        }
        with tempfile.TemporaryDirectory(prefix='tk-report-renderer-') as directory:
            workspace = Path(directory)
            input_path = workspace / 'content.json'
            output_path = workspace / 'report.html'
            input_path.write_text(json.dumps(payload), encoding='utf-8')
            original_payload = input_path.read_bytes()
            env = dict(os.environ, XDG_CONFIG_HOME=str(workspace / 'config'))
            rejected = subprocess.run(
                [sys.executable, str(renderer), '--input', str(input_path), '--output', str(input_path)],
                cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('must not overwrite', rejected.stderr)
            self.assertEqual(input_path.read_bytes(), original_payload)
            template_path = root / 'skills/tk-research/assets/report.html'
            template_before = template_path.read_bytes()
            rejected = subprocess.run(
                [sys.executable, str(renderer), '--input', str(input_path), '--output', str(template_path)],
                cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(template_path.read_bytes(), template_before)
            result = subprocess.run(
                [sys.executable, str(renderer), '--input', str(input_path), '--output', str(output_path)],
                cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('created default HTML theme settings', result.stderr)
            rendered = output_path.read_text(encoding='utf-8')
            # Reuse the existing HTML parser, without applying its report-only CLI to lessons.
            spec = importlib.util.spec_from_file_location('report_reference_parser', checker)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            parser = module.ReportParser()
            parser.feed(rendered)
            parser.close()
            nodes = list(parser.root.descendants())
            reference = next(node for node in nodes if node.attrs.get('id') == 'ref-1')
            self.assertFalse(any(node.tag in {'p', 'br'} for node in reference.descendants()))
            links = [node for node in reference.descendants() if node.tag == 'a']
            self.assertEqual([node.attrs.get('href') for node in links],
                             ['https://example.test/http-cache', '#cite-1', '#cite-2'])
            self.assertTrue(all(node.attrs.get('aria-label') for node in links[1:]))
            self.assertEqual([node.text_content() for node in links[1:]], ['[1.1]', '[1.2]'])
            self.assertTrue(any(node.attrs.get('data-ht-backlinks') == 'ref-1'
                                for node in reference.descendants()))
            self.assertIn('2026-10-16', reference.text_content())
            self.assertIn('current', reference.text_content())
            ids = {node.attrs.get('id') for node in nodes}
            self.assertTrue(all(node.attrs['href'][1:] in ids for node in links[1:]))
            self.assertIn('data-default-theme="system"', rendered)
            self.assertIn('<title>ETag {{REPORT_META}} validation supports efficient cache checks · 연구 보고서</title>', rendered)
            self.assertIn('<p class="ht-topbar-title">{{REPORT_TITLE}} lets the server', rendered)
            self.assertIn('Official documentation reviewed on 2026-10-16: {{REPORT_TOPBAR_TITLE}}.', rendered)
            self.assertIn('<p>{{REPORT_TITLE}} and {{REPORT_META}}</p>', rendered)
            settings = workspace / 'config/tigerkit/settings.json'
            self.assertEqual(json.loads(settings.read_text()), {'html': {'theme': 'system'}})
            checked = subprocess.run([sys.executable, str(checker), str(output_path)],
                                     capture_output=True, text=True, check=False)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            result = subprocess.run(
                [sys.executable, str(renderer), '--input', str(input_path), '--output', str(output_path),
                 '--theme', 'light'], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rendered = output_path.read_text(encoding='utf-8')
            self.assertIn('data-default-theme="light"', rendered)
            self.assertIn('data-theme="light"', rendered)
            self.assertNotIn('data-html-mode', rendered)

    def test_reports_reject_modes_and_selectors(self):
        report = self.report_html().replace(
            '<header class="ht-topbar">',
            '<header class="ht-topbar"><fieldset class="ht-mode-control">Modes</fieldset>', 1)
        self.assert_rejected(report, 'document mode selector')
        report = self.report_html().replace(
            '<p>Evidence summary.</p>', '<p data-html-mode="standard">Evidence summary.</p>', 1)
        self.assert_rejected(report, 'without presentation modes')

    def test_conclusion_is_required_even_without_navigation(self):
        report = re.sub(
            r'  <section id="overview">.*?</section>\n',
            '', self.report_html(navigation=False), flags=re.S,
        )
        report = re.sub(
            r'  <section id="evidence">.*?</section>\n',
            '', report, flags=re.S,
        )
        self.assert_rejected(report, 'substantive conclusion in #overview')

    def test_short_report_can_omit_both_navigation_controls(self):
        html = self.report_html(navigation=False)
        html = html.replace('  <section id="verification"><h2>Verification</h2></section>\n', '')
        result = self.check_report(html)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_long_report_requires_both_navigation_controls(self):
        self.assert_rejected(self.report_html(navigation=False), 'navigation')
        html = self.report_html().replace(
            '<nav class="ht-doc-controls"><a href="#document-top">Top</a>'
            '<a href="#document-bottom">Bottom</a></nav>', '')
        self.assert_rejected(html, 'navigation')

    def test_navigation_exemption_cannot_leave_only_one_control(self):
        html = self.report_html(navigation=False)
        html = re.sub(r'  <section id="evidence">.*?</section>\n', '', html, flags=re.S)
        html = re.sub(r'  <section id="verification">.*?</section>\n', '', html, flags=re.S)
        html = html.replace(
            '</main>', '</main><nav class="ht-doc-nav"></nav>')
        self.assert_rejected(html, 'navigation')

    def test_present_navigation_must_contain_toc_and_movement_links(self):
        result = self.check_report(self.report_html(empty_navigation=True))
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('table of contents', result.stderr)
        self.assertIn('top and bottom', result.stderr)
        missing_toc_link = self.report_html().replace(
            '<a href="#verification">Verification</a>', '')
        self.assert_rejected(missing_toc_link, 'missing section links')
        missing_bottom_link = self.report_html().replace(
            '<a href="#document-bottom">Bottom</a>', '')
        self.assert_rejected(missing_bottom_link, 'top and bottom')

    def test_local_fragments_must_resolve_to_unique_ids(self):
        broken_link = self.report_html().replace('href="#overview"', 'href="#missing"')
        self.assert_rejected(broken_link, 'fragment')
        broken_non_anchor_link = self.report_html().replace(
            '</body>', '<link href="#missing">\n</body>')
        self.assert_rejected(broken_non_anchor_link, 'fragment')
        duplicate_id = self.report_html().replace(
            '<section id="evidence">', '<section id="overview">')
        self.assert_rejected(duplicate_id, 'duplicate id')

    def test_unsafe_links_and_external_assets_are_rejected(self):
        for url in ('javascript:alert(1)', 'java&#x09;script:alert(1)'):
            unsafe_link = self.report_html().replace(
                'href="#overview"', f'href="{url}"')
            self.assert_rejected(unsafe_link, 'unsafe URL scheme')
        for asset in (
            '<script src="https://example.test/report.js"></script>',
            '<link rel="stylesheet" href="https://example.test/report.css">',
            '<img src="https://example.test/figure.png" alt="figure">',
            '<source srcset="https://example.test/figure.png 1x">',
            '<iframe src="https://example.test/widget"></iframe>',
            '<video src="https://example.test/clip.mp4"></video>',
            '<object data="https://example.test/widget"></object>',
            '<svg><image href="https://example.test/figure.svg"></image></svg>',
            '<svg><image xlink:href="https://example.test/figure.svg"></image></svg>',
            '<svg><rect fill="url(https://example.test/paint.svg#gradient)"></rect></svg>',
            '<svg><rect filter="url(https://example.test/filter.svg#blur)"></rect></svg>',
            '<svg><rect stroke="u\\72l(https://example.test/paint.svg#gradient)"></rect></svg>',
            '<style>@import url("https://example.test/report.css");</style>',
            '<style>u\\72l(https://example.test/bg.png)</style>',
            '<style>@\\69mport url("https://example.test/report.css")</style>',
            '<div style="background-image:url(https://example.test/bg.png)"></div>',
            '<div style=\'background-image:image-set("https://example.test/p.png" 1x)\'></div>',
            '<script>fetch("https://example.test/data")</script>',
            '<script>const image = new Image(); image.src = "https://example.test/pixel";</script>',
            '<meta http-equiv="refresh" content="0;url=https://example.test/">',
        ):
            self.assert_rejected(
                self.report_html().replace('</body>', asset + '\n</body>'),
                'runtime',
            )
        local_svg_reference = self.report_html().replace(
            '</body>', '<svg><defs><linearGradient id="local-gradient"></linearGradient>'
            '</defs><rect fill="url(#local-gradient)"></rect></svg>\n</body>')
        self.assertEqual(self.check_report(local_svg_reference).returncode, 0)
        event_handler = self.report_html().replace(
            '<body class="ht-document" id="document-top">',
            '<body class="ht-document" id="document-top" onload="fetch(\'https://example.test/\')">',
        )
        self.assert_rejected(event_handler, 'event handlers')

    def test_extra_inline_css_is_allowed_but_network_css_and_script_drift_fail(self):
        extra_css = self.report_html().replace(
            '</head>', '<style>.ht-chat-turn{border:1px solid var(--line)}</style></head>')
        self.assertEqual(self.check_report(extra_css).returncode, 0)
        for css in (
            '<style>@import url("https://example.test/theme.css");</style>',
            '<style>@font-face{font-family:Remote;src:url(https://example.test/font.woff2)}</style>',
        ):
            self.assert_rejected(
                self.report_html().replace('</head>', '</head>' + css),
                'runtime network CSS',
            )
        changed_script = self.report_html().replace(
            '</body>', '<script>document.body.dataset.changed="yes"</script></body>')
        self.assert_rejected(changed_script, 'inline scripts must match')

    def test_missing_source_link_is_a_warning_and_explicit_note_resolves_it(self):
        unlinked = self.report_html().replace(
            '<a href="https://example.test/source">Source</a>', 'Source', 1)
        result = self.check_report(unlinked)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('WARN', result.stderr)
        linked_unavailable = unlinked.replace('Source ', 'Source · 링크 없음 ', 1)
        result = self.check_report(linked_unavailable)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('WARN', result.stderr)

    def test_citations_and_reference_backlinks_must_resolve(self):
        broken_citation = self.report_html().replace(
            '<a href="#ref-1">[1]</a>', '<a href="#missing-reference">[1]</a>')
        self.assert_rejected(broken_citation, 'citation')
        missing_backlink = self.report_html().replace(
            '<a href="#cite-1-1">↩ 1</a>', '')
        self.assert_rejected(missing_backlink, 'backlink')
        multiple_citations = self.report_html().replace(
            '<sup id="cite-1-1"><a href="#ref-1">[1]</a></sup>',
            '<sup id="cite-1-1"><a href="#ref-1">[1]</a></sup> '
            '<sup id="cite-1-2"><a href="#ref-1">[1]</a></sup>',
        ).replace(
            '<a href="#cite-1-1">↩ 1</a>',
            '<a href="#cite-1-1">↩ 1</a> '
            '<a href="#cite-1-2">↩ 2</a>',
        )
        self.assertEqual(self.check_report(multiple_citations).returncode, 0)
        missing_second_backlink = multiple_citations.replace(
            '<a href="#cite-1-2">↩ 2</a>', '')
        self.assert_rejected(missing_second_backlink, 'backlink')

    def test_user_file_has_no_automatic_authorship_notice_and_keeps_references(self):
        root = Path(__file__).resolve().parents[1]
        template = (root / 'skills/tk-research/assets/report.html').read_text()
        self.assertNotIn('🤖', template)
        self.assertNotIn('AI가 작성', template)
        self.assertIn('실행 상태의 정본이 아닙니다.', template)
        self.assertEqual(self.check_report(self.report_html()).returncode, 0)
        self.assert_rejected(self.report_html().replace('<a href="#cite-1-1">↩ 1</a>', ''), 'backlink')

    def test_document_toc_defaults_to_left_rail_or_collapsible_mobile_control(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / 'skills/tk-explain/assets/html-theme.js').read_text()
        setup = r'''
const assert = require('node:assert/strict');
const listeners = {};
const summary={focus(){}};
const toc={open:true,querySelector:()=>summary};
const nav={querySelector:()=>toc,querySelectorAll:()=>[],addEventListener(){},contains(){return true}};
const bar={getBoundingClientRect:()=>({height:80,bottom:80})};
const media={matches:true,addEventListener:(event,fn)=>{listeners.media=fn}};
globalThis.matchMedia=()=>media;globalThis.location={hash:''};globalThis.innerHeight=900;
globalThis.getComputedStyle=()=>({position:'sticky'});
globalThis.document={querySelector:s=>s==='.ht-doc-nav'?nav:s==='.ht-topbar'?bar:null,
 getElementById:()=>null,documentElement:{style:{setProperty(){}}},addEventListener(){}};
globalThis.addEventListener=(event,fn)=>{listeners[event]=fn};globalThis.requestAnimationFrame=f=>f();
'''
        checks = r'''
assert.equal(toc.open,false,'mobile navigation starts collapsed');
media.matches=false;listeners.media();assert.equal(toc.open,true,'desktop navigation remains exposed');
'''
        result = subprocess.run(['node', '-e', setup + script + checks],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_current_section_uses_visible_content_across_navigation_breakpoint(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / 'skills/tk-explain/assets/html-theme.js').read_text()
        # Shared navigation must respect the sticky bar and select a nested section
        # at the reading edge rather than its larger enclosing parent.
        setup = r'''
const assert = require('node:assert/strict');
const listeners = {};
const fakeLinks=['overview','unknowns','conditions','frontier','sources'].map(id=>({hash:'#'+id,
 setAttribute(){this.current=true},removeAttribute(){this.current=false}}));
const fakeSections=[{id:'overview',top:-300,bottom:-100},
 {id:'unknowns',top:90,bottom:490},{id:'conditions',top:120,bottom:450},
 {id:'frontier',top:510,bottom:700},{id:'sources',top:730,bottom:890}]
 .map(s=>({...s,getBoundingClientRect(){return this},contains(other){return this.id==='unknowns'&&other.id==='conditions'}}));
let mobile=false;
const nav={querySelector:()=>null,querySelectorAll:()=>fakeLinks,addEventListener(){},contains(){return true}};
const bar={getBoundingClientRect:()=>({height:80,bottom:80})};
globalThis.location={hash:'#unknowns'};globalThis.innerHeight=900;
globalThis.getComputedStyle=()=>({position:mobile?'static':'sticky'});
globalThis.document={querySelector:s=>s==='.ht-doc-nav'?nav:s==='.ht-topbar'?bar:null,
 getElementById:id=>fakeSections.find(s=>s.id===id),documentElement:{style:{setProperty(){}}},addEventListener(){}};
globalThis.addEventListener=(event,fn)=>{listeners[event]=fn};globalThis.requestAnimationFrame=f=>f();
'''
        checks = r'''
listeners.scroll();assert.equal(fakeLinks.find(a=>a.current).hash,'#conditions');
mobile=true;listeners.resize();assert.equal(fakeLinks.find(a=>a.current).hash,'#unknowns');
// Moving the child to the mobile reading edge must activate it there too.
fakeSections.find(s=>s.id==='unknowns').top=-20;
fakeSections.find(s=>s.id==='conditions').top=20;
listeners.scroll();assert.equal(fakeLinks.find(a=>a.current).hash,'#conditions');
'''
        result = subprocess.run(['node', '-e', setup + script + checks],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
