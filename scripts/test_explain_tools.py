import importlib.util
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/tk-explain/scripts'
spec = importlib.util.spec_from_file_location('visible_text', SCRIPTS / 'visible_text.py')
visible = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visible)


class ExplainTools(unittest.TestCase):
    def test_review_text_includes_alt_and_revealed_answer_excludes_code_and_hidden(self):
        result = visible.extract('<head><title>Hidden title</title></head><h1>실제 제목</h1>'
            '<script>bad()</script><style>body{}</style><div hidden>secret</div>'
            '<p aria-hidden="true">Visible factual label</p><p>A &amp; B</p><img alt="벽 옆의 경로"><details><summary>답</summary>조건을 바꾸면 결과도 바뀝니다.</details>')
        for text in ('실제 제목', 'Visible factual label', 'A & B', '[image: 벽 옆의 경로]', '조건을 바꾸면 결과도 바뀝니다.'):
            self.assertIn(text, result)
        for text in ('bad()', 'body{}', 'secret', 'Hidden title'):
            self.assertNotIn(text, result)

    def test_missing_chrome_blocks_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / 'figure.svg', Path(tmp) / 'figure.png'
            source.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="560" height="200"/>')
            result = subprocess.run(['node', str(SCRIPTS / 'svg_to_png.mjs'), str(source), str(dest)],
                env={**os.environ, 'CHROME_PATH': str(Path(tmp) / 'missing')}, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Blocked', result.stderr)
            self.assertFalse(dest.exists())

    def test_cli_real_and_symlink_usage_and_missing_browser_are_not_silent(self):
        scripts = [SCRIPTS / 'capture_page.mjs', SCRIPTS / 'svg_to_png.mjs',
                   ROOT / 'skills/tk-research/scripts/svg_to_png.mjs']
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'input.html'
            page.write_text('<!doctype html><h1>Capture</h1>')
            svg = root / 'input.svg'
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="560" height="200"/>')
            for index, script in enumerate(scripts):
                # Reproduce installation through a linked package directory.
                link = root / f'package-{index}'
                link.symlink_to(script.parent.parent, target_is_directory=True)
                for entry in (script, link / 'scripts' / script.name):
                    with self.subTest(entry=entry):
                        usage = subprocess.run(['node', str(entry)], capture_output=True, text=True, timeout=30)
                        self.assertEqual(usage.returncode, 2, usage.stderr)
                        self.assertIn('Usage:', usage.stderr)
                        output = root / 'missing-browser.png'
                        source = page if script.name == 'capture_page.mjs' else svg
                        result = subprocess.run(['node', str(entry), str(source), str(output)],
                            env={**os.environ, 'CHROME_PATH': str(root / 'missing')},
                            capture_output=True, text=True, timeout=30)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn('Blocked', result.stderr)
                        self.assertFalse(output.exists())

    def test_import_with_cli_arguments_never_runs_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, script in enumerate([SCRIPTS / 'capture_page.mjs', SCRIPTS / 'svg_to_png.mjs',
                    ROOT / 'skills/tk-research/scripts/svg_to_png.mjs']):
                link = root / f'package-{index}'
                link.symlink_to(script.parent.parent, target_is_directory=True)
                entry = link / 'scripts' / script.name
                wrapper = root / 'import.mjs'
                wrapper.write_text(f'import * as helper from {str(entry.as_uri())!r};\n'
                                   'console.log(typeof (helper.capture || helper.convert));')
                output = root / 'unexpected.png'
                result = subprocess.run(['node', str(wrapper), 'missing-input', str(output)],
                    capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), 'function')
                self.assertEqual(result.stderr, '')
                self.assertFalse(output.exists())

    def test_capture_rejects_invalid_explicit_height_before_browser_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            page, dest = Path(tmp) / 'source.html', Path(tmp) / 'output.png'
            page.write_text('<!doctype html><title>Capture</title>')
            for height in ('0', '-1', 'NaN', '100001'):
                result = subprocess.run(['node', str(SCRIPTS / 'capture_page.mjs'), str(page), str(dest), '1200', height],
                    capture_output=True, text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Height must be', result.stderr)
                self.assertFalse(dest.exists())

    @unittest.skipUnless(os.environ.get('TK_CHROMIUM_EXECUTABLE'), 'Local Chrome not configured')
    def test_short_document_capture_has_no_viewport_floor_and_explicit_height_works(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'short.html'
            page.write_text('<!doctype html><style>html,body{margin:0;width:1200px;height:580px;background:#fff}h1{margin:0}</style><h1>Short canvas</h1>')
            env = {**os.environ, 'CHROME_PATH': os.environ['TK_CHROMIUM_EXECUTABLE']}
            for suffix, args in [('auto', []), ('explicit', ['580'])]:
                dest = root / (suffix + '.png')
                result = subprocess.run(['node', str(SCRIPTS / 'capture_page.mjs'), str(page), str(dest), '1200', *args],
                    env=env, capture_output=True, text=True, timeout=40)
                self.assertEqual(result.returncode, 0, result.stderr)
                with Image.open(dest) as image:
                    self.assertEqual(image.size, (1200, 580))

    @unittest.skipUnless(os.environ.get('TK_CHROMIUM_EXECUTABLE'), 'Local Chrome not configured')
    def test_svg_image_is_inert_transparent_double_resolution_and_page_capture_is_full(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / 'figure.svg', Path(tmp) / 'figure.png'
            source.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 200">
              <rect id="box" x="10" y="10" width="100" height="100" fill="red"/>
              <script>document.getElementById('box').setAttribute('fill','blue')</script></svg>''')
            env = {**os.environ, 'CHROME_PATH': os.environ['TK_CHROMIUM_EXECUTABLE']}
            command = ['node', str(SCRIPTS / 'svg_to_png.mjs'), str(source), str(dest)]
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=40)
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(dest) as img:
                self.assertEqual(img.size, (1120, 400))
                self.assertEqual(img.convert('RGBA').getpixel((40, 40)), (255, 0, 0, 255))
                self.assertEqual(img.convert('RGBA').getpixel((500, 300))[3], 0)
            original = dest.read_bytes()
            self.assertNotEqual(subprocess.run(command, env=env, capture_output=True, timeout=40).returncode, 0)
            self.assertEqual(original, dest.read_bytes())
            page, capture = Path(tmp) / 'long.html', Path(tmp) / 'long.png'
            page.write_text('<!doctype html><style>body{margin:0;height:11000px;background:#fff}</style><h1>Long page</h1>')
            result = subprocess.run(['node', str(SCRIPTS / 'capture_page.mjs'), str(page), str(capture), '800'],
                env=env, capture_output=True, text=True, timeout=40)
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(capture) as img:
                self.assertGreaterEqual(img.height, 11000)
                self.assertEqual(img.width, 800)

    @unittest.skipUnless(os.environ.get('TK_CHROMIUM_EXECUTABLE'), 'Local Chrome not configured')
    def test_symlink_cli_produces_decodable_png(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html, svg = root / 'input.html', root / 'input.svg'
            html.write_text('<!doctype html><style>body{margin:0}</style><h1>Capture</h1>')
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="560" height="200"/>')
            for index, script in enumerate([SCRIPTS / 'capture_page.mjs', SCRIPTS / 'svg_to_png.mjs',
                    ROOT / 'skills/tk-research/scripts/svg_to_png.mjs']):
                link = root / f'package-{index}'
                link.symlink_to(script.parent.parent, target_is_directory=True)
                source = html if script.name == 'capture_page.mjs' else svg
                output = root / f'capture-{index}.png'
                result = subprocess.run(['node', str(link / 'scripts' / script.name), str(source), str(output)],
                    env={**os.environ, 'CHROME_PATH': os.environ['TK_CHROMIUM_EXECUTABLE']},
                    capture_output=True, text=True, timeout=40)
                self.assertEqual(result.returncode, 0, result.stderr)
                with Image.open(output) as image:
                    self.assertEqual(image.format, 'PNG')
                    self.assertGreater(image.width, 0)
                    self.assertGreater(image.height, 0)
