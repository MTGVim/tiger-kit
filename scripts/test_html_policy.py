"""Exercise shared-contract validation with installed-package mutations."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HTMLPolicyTest(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),
                         'Document render regression requires an explicitly configured local browser')
    def test_document_pattern_render_regression(self):
        result = subprocess.run(['node', '--test', 'evals/skills/tk-explain/card-flow.test.cjs'],
                                cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_research_native_navigation_and_reference_targets(self):
        class Targets(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids, self.links = [], []
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs: self.ids.append(attrs['id'])
                if tag == 'a' and attrs.get('href', '').startswith('#'):
                    self.links.append(attrs['href'][1:])
        text = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        parser = Targets()
        parser.feed(text)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertTrue(set(parser.links) <= set(parser.ids))
        self.assertIn('class="ht-doc-toc"', text)
        self.assertIn('class="ht-doc-controls"', text)
        self.assertIn('class="ht-doc-content"', text)
        self.assertIn('class="ht-doc-nav-heading"', text)
        self.assertIn('<summary aria-label="목차 열기 또는 닫기">', text)
        self.assertIn('id="cite-1-2"', text)
        self.assertIn('href="#cite-1-2"', text)
        self.assertNotIn('data-html-mode', text)
        self.assertNotIn('ht-mode-control', text)
        self.assertNotIn('grid-template-columns:15rem', text)

    def test_document_surface_and_left_navigation_contract(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        report = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        surfaces = re.findall(r'--bg:\s*(#[0-9a-fA-F]{6});\s*--panel:\s*(#[0-9a-fA-F]{6})', css)
        self.assertGreaterEqual(len(surfaces), 3)
        for page, content in surfaces:
            self.assertNotEqual(page.lower(), content.lower())
        self.assertIn('.ht-doc-content {', css)
        self.assertIn('background: var(--panel)', css)
        self.assertIn('.ht-doc-nav { position: fixed; inset-inline-start:', css)
        self.assertIn('@media (max-width: 960px)', css)
        self.assertIn('.ht-doc-toc[open] > .ht-doc-toc-panel { display: block; }', css)
        self.assertIn('class="ht-doc-content"', report)
        self.assertIn('class="ht-doc-controls"', report)
        self.assertIn('<details class="ht-doc-toc" open>', report)

    def test_research_sections_are_flat_and_use_one_pixel_rules(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        report = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        custom_css = report.split('/* /tigerkit:html-theme.css */', 1)[1].split('</style>', 1)[0]
        section_rule = re.search(r'(?<![-\w])section\s*\{([^}]*)\}', custom_css)
        self.assertIsNotNone(section_rule)
        self.assertRegex(section_rule.group(1), r'border-top:\s*1px solid var\(--line\)')
        self.assertRegex(section_rule.group(1), r'background:\s*transparent')
        self.assertRegex(section_rule.group(1), r'border:\s*0')
        self.assertIn('border-block-start: 1px solid var(--line)', css)
        self.assertNotRegex(css, r'border(?:-[\w-]+)?\s*:\s*[2-9]px')

    def test_document_static_checks_and_conditional_browser_verification_contract(self):
        text = (ROOT / 'skills/tk-explain/references/html-output.md').read_text()
        normalized = ' '.join(text.split())
        for requirement in (
            'Every local fragment `href` resolves',
            'No runtime network requests are present',
            '`html[data-default-theme]`',
            'Every `<details>` has a first-child `<summary>`',
            'subject-specific `<title>`',
            'an interactive figure',
            'Keep browser checks for',
            'customized shared document shell/theme/navigation',
            'desktop left rail, narrow-screen TOC',
            'Do not replace or override their shell geometry',
            'data-ht-theme-control`\nattribute alone is insufficient',
            'create one coherent document from verified content and sources',
            'prose and tables need no technique assignment',
            'Avoid decorative thick borders; visible keyboard focus outlines are the exception',
            'Preserve every template `<script>` block exactly',
            'do not use `@import`, `url(...)`, remote fonts, or `image-set(...)`',
        ):
            self.assertIn(' '.join(requirement.split()), normalized)

    def test_explanation_owners_require_current_independent_review_and_opt_in_browser(self):
        canonical = ROOT / 'skills/tk-explain/references/content-review.md'
        for name in ('tk-explain', 'tk-explain-diff', 'tk-teach'):
            with self.subTest(skill=name):
                package = ROOT / 'skills' / name
                self.assertIn('(references/content-review.md)', (package / 'SKILL.md').read_text())
                self.assertEqual((package / 'references/content-review.md').read_bytes(), canonical.read_bytes())
        contract = ' '.join(canonical.read_text().split())
        for guard in ('separate reviewer with fresh context', 'final saved artifact and its exact version',
                      'minimum correction', 'current saved version',
                      'Ordinary chat and feedback', 'do not substitute self-review'):
            self.assertIn(guard, contract)
        html = ' '.join((ROOT / 'skills/tk-explain/references/html-output.md').read_text().split())
        self.assertIn('For `tk-explain`, `tk-explain-diff` and `tk-teach`', html)
        self.assertIn('only for explicitly requested screen/action checks', html)
        self.assertIn('Other document owners retain their scoped UI checks', html)
        self.assertNotIn('The composed shell still triggers', (ROOT / 'skills/tk-explain/references/html-assembly.md').read_text())

    def test_section_level_routing_replaces_document_modes(self):
        text = (ROOT / 'skills/tk-explain/references/html-output.md').read_text()
        explain = (ROOT / 'skills/tk-explain/SKILL.md').read_text()
        diff = (ROOT / 'skills/tk-explain-diff/SKILL.md').read_text()
        teach = (ROOT / 'skills/tk-teach/SKILL.md').read_text()
        normalized_explain = ' '.join(explain.split())
        normalized_diff = ' '.join(diff.split())
        self.assertIn('prose and tables need no technique assignment', ' '.join(text.split()))
        self.assertIn('explanation-techniques.md', text)
        self.assertIn('avoid repeating the same content', normalized_explain)
        self.assertIn('avoid repeating the same content', normalized_diff)
        self.assertIn('avoid rendering duplicate modes or hidden tabs', ' '.join(teach.split()))

    def test_explanations_default_to_natural_conversation(self):
        skill = (ROOT / 'skills/tk-explain/SKILL.md').read_text()
        contract = (ROOT / 'skills/tk-explain/references/html-output.md').read_text()
        self.assertIn('clear conversational voice by default', skill)
        self.assertIn('only when the user has explicitly requested them', contract)
        self.assertIn('Do not add visible `질문:` or `답변:`', contract)

    def test_shared_document_shell_styles_are_canonical(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        report = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        report_custom_css = report.split('/* /tigerkit:html-theme.css */', 1)[1]
        self.assertIn('.ht-topbar { position: sticky;', css)
        self.assertIn('.ht-topbar .ht-theme-control { margin: 0; width: max-content; }', css)
        self.assertNotIn('.ht-mode-control', css)
        self.assertNotIn('[data-html-mode]', css)
        self.assertIn('.ht-chat-turn[data-speaker="reader"]', css)
        self.assertIn('border-inline-start: 1px solid var(--accent)', css)
        self.assertIn('.ht-document .ht-doc-content > section[id]', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertNotRegex(report_custom_css, r'\.ht-doc-content\s*\{[^}]*\b(?:width|margin|position)\s*:')
        self.assertNotRegex(report_custom_css, r'\.ht-topbar\s*\{')

    def test_native_navigation_does_not_frame_content_targets(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        self.assertNotRegex(css, r'\.ht-document\s+:target\s*\{[^}]*outline:\s*[1-9]')
        self.assertRegex(css, r':focus-visible\s*\{[^}]*outline:\s*2px solid')

    def test_fragment_cue_expires_and_respects_reduced_motion(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        self.assertRegex(css, r'@keyframes ht-target-flash\s*\{\s*from\s*\{[^}]*var\(--accent\)')
        self.assertRegex(css, r'to\s*\{\s*outline-color: transparent;')
        self.assertIn('animation: ht-target-flash 1.5s ease-out;', css)
        self.assertNotIn('animation: ht-target-flash 1.5s ease-out forwards', css)
        self.assertRegex(css, r'@media \(prefers-reduced-motion: reduce\)\s*\{[^}]*\[id\]:target[^}]*animation: none;\s*background: var\(--hover\)')

    def test_shared_citation_preview_contract(self):
        css = (ROOT / 'skills/tk-explain/assets/html-theme.css').read_text()
        script = (ROOT / 'skills/tk-explain/assets/html-theme.js').read_text()
        self.assertIn('sup[id^="cite-"]:is(:target, :focus-visible) { outline: none; }', css)
        self.assertIn('sup[id^="cite-"] > a[href^="#ref-"]', script)
        self.assertIn("preview.setAttribute('role', 'tooltip')", script)
        self.assertIn("if (event.pointerType !== 'touch') show(link)", script)
        self.assertIn("link.addEventListener('focus', () => show(link))", script)
        self.assertIn("back.remove()", script)

    def test_research_theme_control_belongs_to_page_top_bar(self):
        class ThemeLocation(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack = []
                self.locations = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'data-ht-theme-control' in attrs:
                    self.locations.append(list(self.stack))
                if tag not in ('meta', 'link', 'br', 'hr', 'input', 'img'):
                    self.stack.append((tag, attrs))

            def handle_endtag(self, tag):
                if self.stack and self.stack[-1][0] == tag:
                    self.stack.pop()

        parser = ThemeLocation()
        parser.feed((ROOT / 'skills/tk-research/assets/report.html').read_text())
        self.assertEqual(len(parser.locations), 1)
        ancestors = parser.locations[0]
        self.assertNotIn('main', [tag for tag, _ in ancestors])
        self.assertTrue(any(tag == 'header' and 'ht-topbar' in attrs.get('class', '').split()
                            for tag, attrs in ancestors))

    def test_research_verification_summary_is_last_content_section(self):
        text = (ROOT / 'skills/tk-research/assets/report.html').read_text()
        sections = re.findall(r'<section\b[^>]*id="([^"]+)"', text)
        self.assertEqual(sections[-2:], ['verification', 'sources'])

    def test_merged_verification_items_block_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-research/assets/report.html'
            text = path.read_text()
            text, replaced = re.subn(
                r'<section id="verification">.*?</section>',
                '<section id="verification"><h2>검증 및 예외</h2>'
                '<p>정적 검증: 완료. 화면 검증: 확인하지 못했습니다.</p></section>',
                text, flags=re.S)
            self.assertEqual(replaced, 1)
            path.write_text(text)
        self.check_mutation(mutate)

    def test_unemphasized_verification_label_blocks_release_check(self):
        def mutate(root):
            path = root / 'skills/tk-research/assets/report.html'
            text = path.read_text()
            self.assertIn('<strong>정적 검증:</strong>', text)
            path.write_text(text.replace('<strong>정적 검증:</strong>', '정적 검증:', 1))
        self.check_mutation(mutate)

    def test_bold_outcomes_do_not_replace_bold_check_labels(self):
        from scripts.sync_execution_protocol import research_verification_errors
        text = ('<section id="verification"><ul>'
                '<li>정적 검증: <strong>완료.</strong></li>'
                '<li>화면 검증: <strong>검증 불가.</strong></li>'
                '</ul></section>')
        self.assertTrue(research_verification_errors(text))

    def test_bold_outcomes_are_allowed_after_bold_check_labels(self):
        from scripts.sync_execution_protocol import research_verification_errors
        text = ('<section id="verification"><ul>'
                '<li><strong>정적 검증:</strong> <strong>완료.</strong></li>'
                '<li><strong>화면 검증:</strong> <strong>검증 불가.</strong></li>'
                '</ul></section>')
        self.assertEqual(research_verification_errors(text), [])

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
        self.assertNotIn('flex-wrap: wrap', qa.split('/* /tigerkit:html-theme.css */', 1)[1])
        self.assertIn('class="ht-doc-nav"', report)
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
        text += (ROOT / 'skills/tk-explain/references/html-figures.md').read_text()
        self.assertIn('html-render.md', text)
        text += (ROOT / 'skills/tk-explain/references/html-render.md').read_text()
        self.assertIn('## Render-safe authoring', text)
        self.assertIn('11 CSS px after scaling', text)
        self.assertIn('emulated mobile CSS viewport width matching `innerWidth`', text)
        self.assertIn('`.ht-token`', text)

    def test_final_head_replay_and_reason_first_auth_contracts(self):
        local = (ROOT / 'skills/tk-prep/references/local-execution.md').read_text()
        lifecycle = (ROOT / 'skills/tk-browser-verify/references/session-lifecycle.md').read_text()
        results = (ROOT / 'skills/tk-browser-verify/references/results.md').read_text()
        environment = (ROOT / 'skills/tk-browser-verify/references/environment.md').read_text()
        qa = (ROOT / 'skills/tk-qa-sheet/SKILL.md').read_text()
        self.assertIn("intervening diff touches a runtime-verified screen's render path or request path", local)
        self.assertIn('replay the same', local)
        self.assertIn('After any baseline, after, or acceptance capture', lifecycle)
        self.assertIn('run-owned development server immediately', lifecycle)
        self.assertIn('Stop the exact run-owned loopback secret server immediately after injection', lifecycle)
        self.assertIn('Expiry blocks use of stale access material', lifecycle)
        self.assertIn('it does not delete the file', lifecycle)
        self.assertIn('Never retain', lifecycle)
        self.assertNotIn('project lock', local)
        self.assertNotIn('guard run ID', results)
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
