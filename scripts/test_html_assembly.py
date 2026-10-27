"""Exercise installed-package assembly, semantic navigation and safe output reuse."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('tk-explain', 'tk-explain-diff', 'tk-teach')
BODY = '''<p class="ht-lede">캐시는 만료 시각 전까지만 값을 반환합니다.</p>
<section id="before"><h2>만료 <code>전</code> &amp; 후</h2><p>예시 값은 10입니다.</p>
<section id="boundary"><h3>경계 조건</h3><p>같은 시각에는 만료됩니다.</p></section></section>
<section id="practice"><h2>값 예측하기</h2><p>만료 시각과 같으면 값을 반환할까요?</p>
<details><summary>해설 보기</summary><p>반환하지 않습니다.</p></details></section>'''


def load(skill, filename='build_html.py'):
    path = ROOT / 'skills' / skill / 'scripts' / filename
    spec = importlib.util.spec_from_file_location(skill.replace('-', '_') + filename, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HTMLAssemblyTests(unittest.TestCase):
    def test_installed_packages_assemble_unchanged_assets_and_full_native_toc(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                package = ROOT / 'skills' / skill
                source = load(skill).assemble(BODY, '캐시 <만료> $body', theme='dark')
                self.assertIn('<title>캐시 &lt;만료&gt; $body</title>', source)
                self.assertIn('data-default-theme="dark" data-theme="dark"', source)
                self.assertIn(BODY, source)
                self.assertIn('<a href="#before">만료 전 &amp; 후</a><ol>', source)
                self.assertIn('<a href="#boundary">경계 조건</a>', source)
                self.assertIn('<style>' + (package / 'assets/html-theme.css').read_text() + '</style>', source)
                self.assertIn('<script>' + (package / 'assets/html-theme.js').read_text() + '</script>', source)
                self.assertEqual(source.count('<h1>'), 1)
                self.assertIn('<details class="ht-doc-toc" open>', source)
                self.assertIn('<details><summary>해설 보기</summary>', source)
                self.assertNotIn('data-ht-font-size', (package / 'assets/document-shell.html').read_text())

    def test_closed_profiles_use_local_assets_and_top_level_units(self):
        module = load('tk-explain')
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / 'package'
            shutil.copytree(ROOT / 'skills/tk-explain', package)
            assets = package / 'assets'
            shell = (assets / 'document-shell.html').read_text()
            for profile in ('lesson', 'change'):
                (assets / (profile + '-shell.html')).write_text(shell)
                (assets / (profile + '.css')).write_text('.ht-profile-example { color: red; }')
                (assets / (profile + '.js')).write_text('const profileExample = true;')
            marked = '<section id="unit" data-ht-nav-unit><h2>Unit</h2><section id="detail"><h3>Detail</h3></section></section>'
            with patch.object(module, 'PACKAGE', package):
                for profile in ('lesson', 'change'):
                    source = module.assemble(marked, 'Example', profile=profile)
                    self.assertIn('data-ht-profile="' + profile + '"', source)
                    toc_part = source.split('<div class="ht-doc-toc-panel"', 1)[1].split('</div>', 1)[0]
                    self.assertIn('href="#unit"', toc_part)
                    self.assertNotIn('href="#detail"', toc_part)
                    self.assertIn('.ht-profile-example', source)
                    self.assertIn('const profileExample = true;', source)
                    with self.assertRaises(ValueError): module.assemble(BODY, 'Example', profile=profile)
                    for unsafe in ('<script>alert(1)</script>', '<a href="#missing">broken</a>', '<details><p>x</p><summary>late</summary></details>'):
                        with self.assertRaises(ValueError): module.assemble(marked + unsafe, 'Example', profile=profile)
                    with self.assertRaises(ValueError): module.assemble(marked.replace('<section id="detail"', '<section data-ht-nav-unit id="detail"'), 'Example', profile=profile)
                for bad in ('../reader', 'unknown'):
                    with self.assertRaises(ValueError): module.assemble(marked, 'Example', profile=bad)
                (assets / 'change.js').unlink()
                with self.assertRaisesRegex(ValueError, 'profile assets unavailable'):
                    module.assemble(marked, 'Example', profile='change')

    def test_missing_profile_asset_does_not_create_output_or_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = root / 'body.html'; body.write_text('<section id="unit" data-ht-nav-unit><h2>Unit</h2></section>')
            output = root / 'result.html'; output.write_text('existing')
            env = dict(os.environ, XDG_CONFIG_HOME=str(root / 'config'))
            result = subprocess.run([sys.executable, str(ROOT / 'skills/tk-explain/scripts/build_html.py'),
                '--body', str(body), '--title', 'Test', '--output', str(output), '--profile', 'lesson', '--replace'],
                capture_output=True, text=True, env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'existing')
            self.assertFalse((root / 'config').exists())

    def test_warns_for_unknown_theme_class_but_keeps_custom_components(self):
        module = load('tk-explain')
        with self.assertWarnsRegex(UserWarning, 'ht-table-wrap'):
            output = module.assemble(BODY + '<div class="ht-table-wrap custom-chart"></div>', 'Cache')
        self.assertIn('custom-chart', output)
        import warnings
        with warnings.catch_warnings(record=True) as notes:
            module.assemble(BODY + '<div class="ht-table-scroll custom-chart"></div><div class></div>', 'Cache')
        self.assertEqual(notes, [])

    def test_cli_warns_once_for_plain_pre_and_accepts_generated_code(self):
        helper = load('tk-explain', 'highlight_code.py')
        generated = helper.highlight('const value = 1;\n', 'js')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body, output = root / 'body.html', root / 'result.html'
            command = [sys.executable, str(ROOT / 'skills/tk-explain/scripts/build_html.py'),
                       '--body', str(body), '--title', 'Cache', '--output', str(output), '--theme', 'system']
            for fragment, expected in [
                ('<pre><code>plain</code></pre><pre class="other">text</pre>', 2),
                (generated, 0),
                ('<p>No preformatted text</p>', 0),
            ]:
                with self.subTest(fragment=fragment):
                    body.write_text(BODY + fragment)
                    result = subprocess.run(command + ['--replace'], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(output.exists())
                    self.assertEqual(result.stderr.count('without .ht-code'), bool(expected))
                    if expected:
                        self.assertIn(f'{expected} <pre> block(s)', result.stderr)
                        self.assertIn('scripts/highlight_code.py', result.stderr)
                    else:
                        self.assertEqual(result.stderr, '')

    def test_reference_fragment_assembles_with_valid_anchors_and_classes(self):
        import warnings
        with warnings.catch_warnings(record=True) as notes:
            for skill in SKILLS:
                module = load(skill)
                body = (ROOT / 'skills' / skill / 'assets/reader-example.html').read_text()
                module.assemble(body, '캐시의 만료 조건')
        self.assertEqual(notes, [])

    def test_rejects_broken_structure_before_delivering_a_document(self):
        bad = [
            '<section id="a"><h2>A</h2>',
            '<section><h2>A</h2></section>',
            '<section id="a"><p>No heading</p></section>',
            BODY + '<p id="boundary">duplicate</p>',
            BODY + '<p id="document-top">reserved</p>',
            BODY + '<a href="#absent">broken</a>',
            BODY + '<details><p>answer</p><summary>late</summary></details>',
            BODY + '<details>answer<summary>late</summary></details>',
            BODY + '<script>alert(1)</script>',
            '<html>' + BODY + '</html>',
            '<h1>Repeated title</h1>' + BODY,
        ]
        for body in bad:
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    load('tk-explain').assemble(body, 'Cache')

    def test_generated_links_url_encode_literal_percent_and_fragment_characters(self):
        source = load('tk-explain').assemble(
            '<section id="cache%2Fttl#경계"><h2>경계</h2></section>', 'Cache')
        self.assertIn('href="#cache%252Fttl%23%EA%B2%BD%EA%B3%84"', source)

    def test_preserves_footer_code_and_escaped_inputs_without_recursive_substitution(self):
        source = load('tk-explain').assemble(
            BODY, 'Cache', lang='en', css='.cache-figure { color: var(--text); }',
            script='const marker = "$title";', footer='<p><a href="#boundary">Boundary</a></p>')
        self.assertIn('const marker = "$title";', source)
        self.assertIn('<footer id="document-bottom"><p>', source)
        self.assertIn('lang="en"', source)
        with self.assertRaises(ValueError):
            load('tk-explain').assemble(BODY, 'Cache', script='const x = "</script>";')

    def test_cli_existing_output_is_unchanged_and_explicit_theme_needs_no_global_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body, output = root / 'body.html', root / 'result.html'
            body.write_text(BODY)
            env = dict(os.environ, XDG_CONFIG_HOME=str(root / 'config'))
            command = [sys.executable, str(ROOT / 'skills/tk-teach/scripts/build_html.py'),
                       '--body', str(body), '--title', 'Cache', '--output', str(output), '--theme', 'system']
            built = subprocess.run(command, capture_output=True, text=True, env=env)
            self.assertEqual(built.returncode, 0, built.stderr)
            first = output.read_bytes()
            body.write_text(BODY.replace('10', '11'))
            refused = subprocess.run(command, capture_output=True, text=True, env=env)
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(output.read_bytes(), first)
            replaced = subprocess.run(command + ['--replace'], capture_output=True, text=True, env=env)
            self.assertEqual(replaced.returncode, 0, replaced.stderr)
            self.assertNotEqual(output.read_bytes(), first)
            self.assertFalse((root / 'config').exists())

    def test_theme_bootstrap_and_invalid_settings_preserve_unrelated_bytes(self):
        module = load('tk-explain')
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, XDG_CONFIG_HOME=directory):
            theme, notes = module.resolve_theme()
            self.assertEqual(theme, 'system')
            self.assertEqual(len(notes), 1)
            config = Path(directory) / 'tigerkit/settings.json'
            for value, expected, warns in [
                ('{"html":{"theme":"dark"},"other":7}', 'dark', False),
                ('{"html":{"theme":null}}', 'system', False),
                ('{"html":{"theme":" "}}', 'system', False),
                ('{"html":{"theme":"blue"},"other":7}', 'system', True),
                ('{"html":[]}', 'system', True),
                ('{malformed', 'system', True),
            ]:
                config.write_text(value)
                actual, notes = module.resolve_theme()
                self.assertEqual(actual, expected)
                self.assertEqual(bool(notes), warns)
                self.assertEqual(config.read_text(), value)

    def test_packaged_document_retains_source_and_reusable_export_without_external_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = load('tk-explain').assemble(BODY, 'Cache')
            (root / 'cache.html').write_text(document)
            manifest = load('tk-explain', 'package_html.py').package(root, ['cache.html'], 'cache.html')
            self.assertEqual(base64.b64decode(manifest['files'][0]['base64']).decode(), document)
            final = (root / 'cache.html').read_text()
            payload = re.search(r'<template data-ht-export data-entry="cache.html">(.*?)</template>', final).group(1)
            self.assertEqual(json.loads(base64.b64decode(payload)), manifest)
            self.assertNotRegex(final, r'<(?:script|link)[^>]+(?:src|href)=')


if __name__ == '__main__':
    unittest.main()
