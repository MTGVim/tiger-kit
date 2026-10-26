"""Code rendering preserves source and remains safe in an offline HTML document."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import os
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('highlight_code', ROOT / 'skills/tk-explain/scripts/highlight_code.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = ''
    def handle_data(self, data):
        self.text += data


class CodeBlocksTest(unittest.TestCase):
    def test_exact_text_and_escaped_markup_across_languages(self):
        for language in ('kt', 'ts', 'js', 'python', 'json', 'diff', 'unknown'):
            for source in ('', '\n', ' \t\n\n', 'val x = "<script>&\\n"\n',
                           '/* first\n second */\nfun x() = 42',
                           '+ added\n- removed\n context\n',
                           '한글 🙂 </code></pre><img src=x onerror=alert(1)>'):
                with self.subTest(language=language, source=source):
                    markup = MODULE.highlight(source, language, line_start=43)
                    parser = Text(); parser.feed(markup)
                    self.assertEqual(parser.text, source)
                    self.assertNotIn('<script>', markup)
                    self.assertNotIn('<img ', markup)
        self.assertNotIn('ht-code-keyword', MODULE.highlight('class unknown', 'unknown'))
        self.assertIn('ht-code-keyword', MODULE.highlight('class Known', 'kt'))
        self.assertIn('ht-code-add', MODULE.highlight('+ added', 'diff'))
        self.assertIn('ht-code-delete', MODULE.highlight('- removed', 'diff'))
        for source in ('x\r\ny', 'x\x00y'):
            with self.assertRaises(ValueError): MODULE.highlight(source, 'kt')

    def test_rich_tokens_and_nested_templates_preserve_exact_source(self):
        source = 'const value: Result = service.read({enabled: true, key: `hi ${user.name} ${fn({n: 2})} ${`nested ${x}`} \u003c`});\n'
        markup = MODULE.highlight(source, 'ts')
        parser = Text(); parser.feed(markup)
        self.assertEqual(parser.text, source)
        for kind, text in [('function', 'read'), ('property', 'name'), ('property', 'enabled'),
                           ('type', 'Result'), ('literal', 'true'), ('punctuation', '${')]:
            self.assertIn(f'<span class="ht-code-{kind}">{text}</span>', markup)
        for source in ['`unfinished ${obj.value', '`escaped \\${notCode}`', 'const x = /* comment */ "s";']:
            parser = Text(); parser.feed(MODULE.highlight(source, 'ts'))
            self.assertEqual(parser.text, source)

    def test_research_template_footer_is_a_shell_child(self):
        class Structure(HTMLParser):
            def __init__(self):
                super().__init__(); self.stack = []; self.parent = None
            def handle_starttag(self, tag, attrs):
                if tag == 'footer' and dict(attrs).get('id') == 'document-bottom':
                    self.parent = self.stack[-1]
                if tag not in ('meta', 'input', 'img', 'br', 'hr', 'link'):
                    self.stack.append(tag)
            def handle_endtag(self, tag):
                if tag in self.stack:
                    del self.stack[len(self.stack) - 1 - self.stack[::-1].index(tag):]
        parser = Structure()
        parser.feed((ROOT / 'skills/tk-research/assets/report.html').read_text())
        self.assertEqual(parser.parent, 'body')

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),
                         'Shell render regression requires an explicitly configured local browser')
    def test_document_shell_and_code_browser_regression(self):
        result = subprocess.run(['node', '--test', 'evals/skills/tk-explain/document-shell.test.cjs',
                                 'evals/skills/tk-explain/reader-enhancements.test.cjs'],
                                cwd=ROOT, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
