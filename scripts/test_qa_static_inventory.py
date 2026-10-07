"""Protect static QA reading and generator/source consistency."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'skills/tk-qa-sheet/assets/qa-sheet-template.html'
HELPER = ROOT / 'skills/tk-qa-sheet/scripts/render_static_inventory.py'


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []
    def handle_data(self, value):
        self.parts.append(value)


def static_text(html):
    match = re.search(r'<noscript id="qa-static">(.*?)</noscript>', html, re.S)
    parser = Text()
    parser.feed(match[1] if match else '')
    return ''.join(parser.parts)


class QAStaticInventoryTest(unittest.TestCase):
    def test_template_core_inventory_is_readable_without_scripts(self):
        html = TEMPLATE.read_text()
        data = json.loads(re.search(r'id="qa-data">(.*?)</script>', html, re.S)[1])
        text = static_text(html)
        self.assertIn(data['title'], text)
        for group in data['groups']:
            self.assertIn(group['title'], text)
            for item in group['items']:
                self.assertIn(item['title'].replace('`', ''), text)
                for check in item.get('checks', []):
                    self.assertIn(check['text'].replace('`', ''), text)

    def test_unsafe_or_invalid_target_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'qa.html'
            target.write_text('invalid input')
            previous = target.read_bytes()
            link = root / 'linked.html'; link.symlink_to(target)
            for path in (target, link):
                result = subprocess.run([sys.executable, str(HELPER), str(path)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(target.read_bytes(), previous)
                self.assertFalse(list(root.glob('.qa-static-*')))

    def test_generator_updates_static_content_and_preserves_renderer(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'qa.html'
            html = TEMPLATE.read_text()
            data = {'title': 'New task', 'storageKey': 'new-task',
                'environment': {'label':'QA environment', 'baseUrl':'https://qa.example.test'},
                'groups': [{'title':'New group','items':[
                {'title':'<img src=x onerror=alert(1)> `Literal`', 'checks':[{'text':'Check A', 'provenance':'observed'}]},
                {'title':'Second', 'notes':['Note'], 'provenance':'observed'}]}]}
            replacement = json.dumps(data).replace('<', '\\u003c')
            html = re.sub(r'(id="qa-data">)(.*?)(</script>)', lambda m: m[1] + replacement + m[3], html, flags=re.S)
            path.write_text(html)
            result = subprocess.run([sys.executable, str(HELPER), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            actual = path.read_text(); text = static_text(actual)
            self.assertIn('Check A', text); self.assertIn('Second', text); self.assertIn('Note', text)
            self.assertIn('QA environment (https://qa.example.test)', text)
            self.assertIn('<img src=x onerror=alert(1)> Literal', text)
            region = re.search(r'<noscript id="qa-static">(.*?)</noscript>', actual, re.S)[1]
            self.assertNotIn('<img', region)
            self.assertIn('&lt;img', region)
            self.assertIn('코드 기준', text)
            self.assertIn('Check A</span> <span class="badge">코드 기준</span>', region)
            self.assertNotIn('영역 A', text)
            before = re.sub(r'<noscript id="qa-static">.*?</noscript>', '', html, flags=re.S)
            after = re.sub(r'<noscript id="qa-static">.*?</noscript>', '', actual, flags=re.S)
            self.assertEqual(before, after)
            previous = path.read_bytes()
            subprocess.run([sys.executable, str(HELPER), str(path)], check=True, capture_output=True)
            self.assertEqual(previous, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
