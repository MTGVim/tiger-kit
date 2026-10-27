"""Exercise lesson structure, examples and offline assembly."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1];PACKAGE=ROOT/'skills/tk-teach'
sys.path.insert(0,str(PACKAGE/'scripts'))
spec=importlib.util.spec_from_file_location('check_lesson',PACKAGE/'scripts/check_lesson.py')
check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
BODY=(PACKAGE/'assets/lesson-example.html').read_text()
CONCEPT=(PACKAGE/'assets/lesson-concept-example.html').read_text()

class LessonTest(unittest.TestCase):
    def test_code_and_non_code_examples_build_and_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for n,body in enumerate((BODY,CONCEPT)):
                self.assertEqual(check.validate(body),[])
                source=root/f'body{n}.html';source.write_text(body);out=root/f'lesson{n}.html'
                cmd=[sys.executable,str(PACKAGE/'scripts/build_html.py'),'--profile','lesson','--body',str(source),'--title','Lesson','--output',str(out),'--theme','system']
                built=subprocess.run(cmd,text=True,capture_output=True);self.assertEqual(built.returncode,0,built.stderr)
                text=out.read_text();self.assertIn('data-ht-profile="lesson"',text)
                result=subprocess.run([sys.executable,str(PACKAGE/'scripts/package_html.py'),'--root',str(root),'--name',out.name,out.name],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr);self.assertIn('data-ht-export',out.read_text())
            class Code(HTMLParser):
                def __init__(self): super().__init__();self.inside=False;self.text=''
                def handle_starttag(self,tag,attrs):
                    if tag=='code':self.inside=True
                def handle_endtag(self,tag):
                    if tag=='code':self.inside=False
                def handle_data(self,data):
                    if self.inside:self.text+=data
            code=Code();code.feed(BODY);self.assertEqual(code.text,'const isExpired = (age, ttl) => age >= ttl;\n')
            self.assertNotIn('<pre',CONCEPT);self.assertIn('점이 2개인 원은 B',CONCEPT)
    def test_missing_focus_and_duplicate_targets_fail(self):
        self.assertTrue(check.validate(BODY.replace('id="expiry-code"','id="missing"')))
        self.assertTrue(check.validate(BODY+'<p id="expiry-code">duplicate</p>'))
        self.assertTrue(check.validate(BODY.replace('href="#expiry-code"','href="#expiry-practice"')))
    def test_reveal_and_retry_relationships(self):
        self.assertTrue(check.validate(BODY.replace('<details data-ht-solution>','<details data-ht-solution open>')))
        self.assertTrue(check.validate(BODY.replace('<details data-ht-hint>','<details data-ht-hint open>')))
        self.assertTrue(check.validate(BODY.replace('href="#expiry-practice" data-ht-retry','href="#expiry-code" data-ht-retry')))
        self.assertTrue(check.validate(BODY.replace('</section>','</section><a href="#expiry-practice" data-ht-retry>retry</a>')))
        self.assertTrue(check.validate(BODY.replace('</section>','</section><details data-ht-solution><summary>answer</summary></details>')))
    def test_rejects_broken_structure_and_local_links(self):
        self.assertTrue(check.validate(BODY+'<a href="../secret">bad</a>'))
        self.assertTrue(check.validate(BODY+'<a href="javascript:alert(1)">bad</a>'))
        self.assertTrue(check.validate(BODY+'<script>alert(1)</script>'))
        self.assertTrue(check.validate(BODY.replace('<section id="expiry-rule" data-ht-nav-unit','<section id="expiry-rule"')))
    def test_multiple_practices_can_be_independent(self):
        other='<div id="other" data-ht-practice><h3>다른 활동</h3><details data-ht-solution><summary>해설</summary><p>답</p></details><a href="#other" data-ht-retry>다시</a></div>'
        self.assertEqual(check.validate(BODY.replace('</section>',other+'</section>')),[])
        self.assertTrue(check.validate(BODY.replace('<h3>먼저 예측해 보세요</h3>', '<div id="nested" data-ht-practice><h3>중첩</h3></div><h3>먼저 예측해 보세요</h3>')))

if __name__=='__main__':unittest.main()
