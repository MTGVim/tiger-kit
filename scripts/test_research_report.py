from pathlib import Path
import re
import subprocess
import tempfile
import unittest


class ResearchReportTest(unittest.TestCase):
    def report_html(self, *, navigation=True, empty_navigation=False,
                    modes=("standard", "dialogue", "easy-dialogue")):
        root = Path(__file__).resolve().parents[1]
        template = (root / 'skills/tk-research/assets/report.html').read_text(encoding='utf-8')
        style = re.search(r'<style\b[^>]*>.*?</style>', template, re.I | re.S).group()
        script = re.search(r'<script\b[^>]*>.*?</script>', template, re.I | re.S).group()
        labels = {"standard": "기본형", "dialogue": "대화형", "easy-dialogue": "쉬운 대화형"}
        selectors = ''.join(
            f'<label class="ht-mode-option"><input type="radio" id="ht-mode-{mode}" name="ht-mode" value="{mode}"'
            f'{" checked" if index == 0 else ""}><span>{labels[mode]}</span></label>'
            for index, mode in enumerate(modes)
        )
        mode_selector = (
            f'<fieldset class="ht-mode-control"><legend>문서 형식</legend>'
            f'<div class="ht-mode-buttons">{selectors}</div></fieldset>'
            if len(modes) == 3 else ''
        )
        variants = ''.join(
            f'<div data-html-mode="{mode}"><p>{labels[mode]} finding.'
            f'<sup id="cite-{mode}-1-1"><a href="#ref-{mode}-1">[1]</a></sup></p></div>'
            for mode in modes
        )
        evidence = ''.join(
            f'<div data-html-mode="{mode}"><p>{labels[mode]} evidence.</p></div>'
            for mode in modes
        )
        sources = ''.join(
            f'<ol data-html-mode="{mode}"><li id="ref-{mode}-1">{labels[mode]} source '
            f'<a href="#cite-{mode}-1-1">↩ 1</a></li></ol>'
            for mode in modes
        )
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
<html><head>{style}</head><body class="ht-document" id="document-top">
<header class="ht-topbar">{mode_selector}</header>
<main class="ht-doc-content">
  <section id="overview"><h2>Overview</h2>{variants}</section>
  <section id="evidence"><h2>Evidence</h2>{evidence}</section>
  <section id="verification"><h2>Verification</h2></section>
  <section id="sources"><h2>Sources</h2>{sources}</section>
</main>
<footer id="document-bottom">🤖 본 보고서는 AI가 작성했습니다.</footer>
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

    def test_explicit_single_mode_is_complete_without_alternate_views(self):
        result = self.check_report(self.report_html(modes=("easy-dialogue",)))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_mode_selector_ids_match_css_selectors(self):
        report = self.report_html().replace(
            'id="ht-mode-easy-dialogue"', 'id="easy-dialogue-mode"', 1)
        self.assert_rejected(report, 'radio ids must match the shared theme selectors')

    def test_three_modes_are_complete_and_internal_links_stay_in_mode(self):
        missing_easy_conclusion = self.report_html().replace(
            'data-html-mode="easy-dialogue"><p>쉬운 대화형 finding.',
            'data-html-mode="dialogue"><p>쉬운 대화형 finding.',
            1,
        )
        self.assert_rejected(missing_easy_conclusion, 'incomplete document modes')
        cross_mode_citation = self.report_html().replace(
            'href="#ref-standard-1"', 'href="#ref-dialogue-1"', 1)
        self.assert_rejected(cross_mode_citation, 'cross-mode fragment')

    def test_conclusion_is_required_even_without_navigation(self):
        report = re.sub(
            r'  <section id="overview">.*?</section>\n',
            '', self.report_html(navigation=False), flags=re.S,
        )
        report = re.sub(
            r'  <section id="evidence">.*?</section>\n',
            '', report, flags=re.S,
        )
        self.assert_rejected(report, 'report conclusion must appear in every rendered mode')

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
        linked_source = self.report_html().replace(
            '<li id="ref-standard-1">기본형 source ',
            '<li id="ref-standard-1"><a href="https://example.test/source">Source</a> ',
        )
        self.assertEqual(self.check_report(linked_source).returncode, 0)
        event_handler = self.report_html().replace(
            '<body class="ht-document" id="document-top">',
            '<body class="ht-document" id="document-top" onload="fetch(\'https://example.test/\')">',
        )
        self.assert_rejected(event_handler, 'event handlers')

    def test_citations_and_reference_backlinks_must_resolve(self):
        broken_citation = self.report_html().replace(
            '<a href="#ref-standard-1">[1]</a>', '<a href="#missing-reference">[1]</a>')
        self.assert_rejected(broken_citation, 'citation')
        missing_backlink = self.report_html().replace(
            '<a href="#cite-standard-1-1">↩ 1</a>', '')
        self.assert_rejected(missing_backlink, 'backlink')
        multiple_citations = self.report_html().replace(
            '<sup id="cite-standard-1-1"><a href="#ref-standard-1">[1]</a></sup>',
            '<sup id="cite-standard-1-1"><a href="#ref-standard-1">[1]</a></sup> '
            '<sup id="cite-standard-1-2"><a href="#ref-standard-1">[1]</a></sup>',
        ).replace(
            '<a href="#cite-standard-1-1">↩ 1</a>',
            '<a href="#cite-standard-1-1">↩ 1</a> '
            '<a href="#cite-standard-1-2">↩ 2</a>',
        )
        self.assertEqual(self.check_report(multiple_citations).returncode, 0)
        missing_second_backlink = multiple_citations.replace(
            '<a href="#cite-standard-1-2">↩ 2</a>', '')
        self.assert_rejected(missing_second_backlink, 'backlink')

    def test_ai_authorship_notice_must_be_positive_and_appear_in_a_footer(self):
        for notice in (
            '본 보고서는 AI가 작성하지 않았습니다.',
            'This report was NOT written with AI.',
        ):
            html = self.report_html().replace(
                '🤖 본 보고서는 AI가 작성했습니다.', notice)
            self.assert_rejected(html, 'AI-authorship footer')
        positive_english = self.report_html().replace(
            '🤖 본 보고서는 AI가 작성했습니다.',
            'This report was written with AI.',
        )
        self.assertEqual(self.check_report(positive_english).returncode, 0)

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
