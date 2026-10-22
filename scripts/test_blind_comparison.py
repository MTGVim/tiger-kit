from __future__ import annotations
import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
import wave
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'skills/tk-blind-comparison'
spec = importlib.util.spec_from_file_location('blind_gallery', PACKAGE / 'scripts/build_gallery.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def fixture(candidates=5, items=9, kind='audio'):
    result = {'study_id': 'sample-listening-study', 'version': '1', 'seed': 'fixed-seed', 'title': '문장 비교',
              'transformations': ['검증용 사본이며 실제 품질 평가는 아직 없습니다.'], 'favorite': True,
              'candidates': [{'id': f'engine-{c}', 'name': f'Model {c}'} for c in range(candidates)],
              'items': [{'id': f'prompt-{i}', 'description': f'같은 입력 {i}의 결과를 비교해 주세요.'} for i in range(items)], 'outputs': []}
    for i in range(items):
        for c in range(candidates):
            row = {'item_id': f'prompt-{i}', 'candidate_id': f'engine-{c}', 'kind': kind}
            if i == 0 and c == 0:
                row['error'] = 'engine-0 failed to generate'
            elif kind == 'text':
                row['text'] = f'동일한 문제를 설명하는 응답 {c}입니다. <script>bad()</script>'
            else:
                row['path'] = 'prepared.wav'
            result['outputs'].append(row)
    return result


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.attrs=[]; self.visible=[]; self.script=False; self.scripts=[]; self.kind=''; self.buffer=''
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.attrs.extend(attrs.values())
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='script': self.script=True; self.kind=attrs.get('type','js'); self.buffer=''
    def handle_endtag(self, tag):
        if tag=='script':
            if self.kind=='js': self.scripts.append(self.buffer)
            self.script=False
    def handle_data(self, value):
        if self.script: self.buffer+=value
        else: self.visible.append(value)


class BlindComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.manifest=self.root/'manifest.json'; self.data=fixture()
        with wave.open(str(self.root/'prepared.wav'),'wb') as f:
            f.setparams((1,2,16000,0,'NONE','not compressed')); f.writeframes(b'\x01\x00'*1600)
    def tearDown(self): self.tmp.cleanup()
    def build(self, name='built', previous=None):
        self.manifest.write_text(json.dumps(self.data,ensure_ascii=False))
        return builder.build(self.manifest,self.root/name,previous)
    def test_runtime_import_export_regressions(self):
        result=subprocess.run(['node','--test',str(ROOT/'scripts/test_blind_comparison_runtime.cjs')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_audio_grid_blinding_failure_offline_and_script_syntax(self):
        original=(self.root/'prepared.wav').read_bytes()
        public,key=self.build(); page=(self.root/'built/gallery.html').read_text(); parser=Parser();parser.feed(page)
        self.assertEqual(len(key['outputs']),45);self.assertEqual(page.count('class="sample"'),45);self.assertEqual(page.count('class="failure"'),1)
        self.assertEqual(page.count('<audio '),44);self.assertEqual(len(parser.ids),len(set(parser.ids)))
        surface=' '.join(x for x in parser.attrs+parser.visible if x is not None)+json.dumps(public)
        for c in self.data['candidates']:
            self.assertNotIn(c['name'],surface);self.assertNotIn(c['id'],surface)
        self.assertNotIn('src="http',page);self.assertNotIn('src="prepared',page)
        for path in (self.root/'built').iterdir():
            self.assertTrue(path.name.isascii());self.assertNotIn('engine',path.name)
        self.assertEqual((self.root/'prepared.wav').read_bytes(),original)
        for script in parser.scripts:
            result=subprocess.run(['node','--check'],input=script,text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
    def test_incremental_add_remove_reorder_and_changed_output(self):
        old,key=self.build(); old_key=self.root/'built/answer-key.json'
        self.data=fixture(6);self.data['version']='2';public,new=self.build('added',old_key)
        for c in key['registry']: self.assertEqual(key['registry'][c],new['registry'][c])
        old_tuples={(r['item'],r['candidate'],r['fingerprint']) for r in key['outputs']}
        new_tuples={(r['item'],r['candidate'],r['fingerprint']) for r in new['outputs']}
        self.assertTrue(old_tuples.issubset(new_tuples))
        self.assertTrue(any([x['candidate'] for x in key['order'][i]] != [x['candidate'] for x in new['order'][i] if x['candidate'] in key['candidates']] for i in key['order']))
        self.data['candidates'].reverse();self.data['items'].reverse();self.data['outputs'].reverse()
        _,reordered=self.build('reordered',self.root/'added/answer-key.json');self.assertEqual(new['order'],reordered['order'])
        self.data=fixture(4);_,removed=self.build('removed',old_key)
        self.assertEqual(key['registry']['engine-3'],removed['registry']['engine-3']);self.assertIn('engine-4',removed['registry'])
        self.data=fixture(5,1,'text');_,first=self.build('text-first')
        self.data['outputs'][1]['text']='내용을 수정했습니다.';_,changed=self.build('text-changed',self.root/'text-first/answer-key.json')
        before={r['candidate']:r for r in first['outputs']};after={r['candidate']:r for r in changed['outputs']}
        token=first['registry']['engine-1'];self.assertNotEqual(before[token]['fingerprint'],after[token]['fingerprint'])
    def test_text_escaping_identity_guard_and_neutral_labels(self):
        self.data=fixture(3,1,'text');public,key=self.build();page=(self.root/'built/gallery.html').read_text()
        self.assertIn('&lt;script&gt;bad()',page);self.assertNotIn('<script>bad()',page)
        self.data['outputs'][1]['text']='Model 1에서 생성했습니다.'
        with self.assertRaises(ValueError):self.build('identity')
        self.assertFalse((self.root/'identity').exists())
        self.data=fixture(3,1,'text');self.data['candidates'][0]['name']='표본'
        public,key=self.build('labels');self.assertTrue(all('표본' not in c['label'] for c in public['items'][0]['cards']))
    def test_missing_duplicate_failed_or_invalid_kind_and_unsafe_paths(self):
        for mutate in [lambda d:d['outputs'].pop(),lambda d:d['outputs'].append(d['outputs'][0]),lambda d:d['outputs'][1].update(kind='html'),lambda d:d.update(candidates=d['candidates'][:1])]:
            self.data=fixture();mutate(self.data)
            with self.assertRaises(ValueError):self.build('invalid')
            self.assertFalse((self.root/'invalid').exists())
        self.data=fixture();self.build()
        with self.assertRaises(ValueError):self.build()
        (self.root/'linked').symlink_to(self.root/'built',target_is_directory=True)
        with self.assertRaises(ValueError):self.build('linked/child')
    def test_results_means_missing_failures_and_invalid_exports(self):
        public,key=self.build(); rows=[r for r in key['outputs'] if not r['failed']]
        rated=[{'item':r['item'],'candidate':r['candidate'],'fingerprint':r['fingerprint'],'score':5 if i==0 else None,'note':'메모','favorite':False} for i,r in enumerate(rows)]
        export={'schema':1,'study':key['study'],'version':key['version'],'evaluator':'test-evaluator','revealed':False,'ratings':rated}
        summary=builder.summarize(export,key);self.assertEqual(summary['evaluators'],1)
        self.assertEqual(sum(r['failures'] for r in summary['candidates']),1)
        self.assertEqual(sum(r['rated'] for r in summary['candidates']),1)
        self.assertEqual(sum(r['missing'] for r in summary['candidates']),43)
        self.assertIn('항목',builder.markdown(summary))
        spoof=copy.deepcopy(export);spoof['ratings'][0].update(candidate_name='wrong',candidate_id='wrong',item_id='wrong',failed=True)
        trusted=builder.summarize(spoof,key)
        scored=next(r for r in trusted['items'] if r['score'] is not None)
        self.assertNotEqual(scored['candidate_name'],'wrong');self.assertNotEqual(scored['item_id'],'wrong');self.assertFalse(scored['failed'])
        variants=[]
        for score in [0,6,True,1.2,'5']:
            x=copy.deepcopy(export);x['ratings'][0]['score']=score;variants.append(x)
        x=copy.deepcopy(export);x['ratings'].append(x['ratings'][0]);variants.append(x)
        x=copy.deepcopy(export);x['version']='other';variants.append(x)
        x=copy.deepcopy(export);x['ratings'][0]['fingerprint']='stale';variants.append(x)
        x=copy.deepcopy(export);failed=next(r for r in key['outputs'] if r['failed']);x['ratings'].append({**{k:failed[k] for k in ('item','candidate','fingerprint')},'score':None,'note':'','favorite':False});variants.append(x)
        for x in variants:
            with self.assertRaises(ValueError):builder.summarize(x,key)
    def test_normalized_image_canvas_and_metadata_stay_anonymous(self):
        from PIL import Image, PngImagePlugin
        raw=self.root/'raw.png';info=PngImagePlugin.PngInfo();info.add_text('producer','Model 0');Image.new('RGB',(120,80),'blue').save(raw,pnginfo=info)
        # The author follows images.md to create common-canvas clean display copies.
        with Image.open(raw) as im:
            clean=Image.new('RGB',(160,100),'white');clean.paste(im,(20,10));clean.save(self.root/'display.png')
        self.data=fixture(4,1,'image')
        for r in self.data['outputs']:
            r.pop('error',None);r['path']='display.png'
        self.build()
        with Image.open(raw) as im:self.assertIn('producer',im.info)
        for path in (self.root/'built').glob('item-*.png'):
            with Image.open(path) as im:self.assertEqual(im.size,(160,100));self.assertNotIn('producer',im.info)

if __name__=='__main__': unittest.main()
