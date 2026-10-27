"""Test change HTML source fidelity, navigation and output safety."""
import copy
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'skills/tk-explain-diff'
SCRIPT=PACKAGE/'scripts/build_change.py'
MODEL=json.loads((PACKAGE/'assets/change-flow-example.json').read_text())
SOURCES=json.loads((PACKAGE/'assets/change-example.sources.json').read_text())

class Capture(HTMLParser):
    def __init__(self): super().__init__();self.ids=[];self.links=[];self.nav=[];self.code=[];self.current=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.links.append(attrs['href'][1:])
        if tag=='section' and 'data-ht-nav-unit' in attrs:self.nav.append(attrs.get('id'))
        if tag=='code':self.current=[]
    def handle_data(self,text):
        if self.current is not None:self.current.append(text)
    def handle_endtag(self,tag):
        if tag=='code' and self.current is not None:self.code.append(''.join(self.current));self.current=None

class ChangeHTMLTest(unittest.TestCase):
    def build(self,root,model=MODEL,sources=SOURCES,extra=()):
        root=Path(root);(root/'model.json').write_text(json.dumps(model,ensure_ascii=False));(root/'sources.json').write_text(json.dumps(sources,ensure_ascii=False))
        output=root/'result.html';env=dict(os.environ,XDG_CONFIG_HOME=str(root/'config'))
        cmd=[sys.executable,str(SCRIPT),'--model',str(root/'model.json'),'--sources',str(root/'sources.json'),'--output',str(output),'--theme','system',*extra]
        return subprocess.run(cmd,capture_output=True,text=True,env=env),output
    def test_groups_evidence_and_flow_are_distinct_and_linked(self):
        with tempfile.TemporaryDirectory() as root:
            result,out=self.build(root);self.assertEqual(result.returncode,0,result.stderr)
            text=out.read_text();parser=Capture();parser.feed(text)
            self.assertEqual(parser.nav,['change-group-ttl-duration','change-group-expiry-boundary'])
            self.assertEqual(len(parser.ids),len(set(parser.ids)));self.assertTrue(set(parser.links)<=set(parser.ids))
            self.assertIn('TTL과 문구가 30초입니다.',text);self.assertIn('TTL과 문구가 60초입니다.',text)
            self.assertEqual(text.count('id="evidence-e-policy-base"'),1)
            first_group=text.split('id="change-group-ttl-duration"',1)[1].split('</section>',1)[0]
            self.assertIn('id="evidence-e-policy-base"',first_group)
            self.assertGreaterEqual(text.count('href="#evidence-e-policy-base"'),2)
            self.assertIn('data-change-flow-controls hidden',text);self.assertIn('이전 판정',text);self.assertIn('이후 판정',text)
            self.assertIn('data-change-node="cache"',text);self.assertIn('data-change-edge="cache-policy"',text);self.assertIn('원문 근거',text)
    def test_escaping_and_exact_copy_source(self):
        with tempfile.TemporaryDirectory() as root:
            model=copy.deepcopy(MODEL);sources=copy.deepcopy(SOURCES)
            dangerous='const x = "</script><img src=x> 한글 %";\n'
            sources['files'][0]['text']=dangerous;model['evidence'][0].update(end=1,sha256=hashlib.sha256(dangerous.encode()).hexdigest())
            result,out=self.build(root,model,sources);self.assertEqual(result.returncode,0,result.stderr)
            text=out.read_text();parser=Capture();parser.feed(text)
            self.assertIn(dangerous,parser.code);self.assertNotIn('<img src=x>',text)
    def test_invalid_input_preserves_output_and_settings(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);model=copy.deepcopy(MODEL);model['evidence'][0]['sha256']='bad'
            output=root/'result.html';output.write_text('original')
            result,out=self.build(root,model,extra=('--replace',));self.assertNotEqual(result.returncode,0)
            self.assertEqual(out.read_text(),'original');self.assertFalse((root/'config').exists())
    def test_supplement_navigation_is_rejected_and_broken_anchor_fails(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);intro=root/'intro.html'
            intro.write_text('<section id="extra" data-ht-nav-unit><h2>Extra</h2></section>')
            result,out=self.build(root,extra=('--intro',str(intro)));self.assertNotEqual(result.returncode,0);self.assertFalse(out.exists())
            intro.write_text('<p><a href="#missing">broken</a></p>')
            result,out=self.build(root,extra=('--intro',str(intro)));self.assertNotEqual(result.returncode,0);self.assertFalse(out.exists())
    def test_graphless_export_and_unavailable_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);model=copy.deepcopy(MODEL);del model['graph']
            result,out=self.build(root,model);self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotIn('data-change-flow-controls hidden',out.read_text())
            result=subprocess.run([sys.executable,str(PACKAGE/'scripts/package_html.py'),'--root',str(root),'--name','result.html','result.html'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertIn('data-ht-export',out.read_text())
            model['evidence'][0].update(availability='unavailable',sha256=None,reason='접근 불가')
            for group in model['groups']:
                for side in ('before','after'):
                    if 'e-policy-base' in group[side]['evidence']:group[side].update(basis='inference',limitation='접근 불가')
            result,out=self.build(root,model,extra=('--replace',));self.assertEqual(result.returncode,0,result.stderr);self.assertIn('확인할 수 없는 근거: 접근 불가',out.read_text())

if __name__=='__main__':unittest.main()
