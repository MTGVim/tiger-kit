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
    def test_versus_revisions_modes_and_cli_replay(self):
        self.data = fixture(3, 1, 'text')
        self.manifest.write_text(json.dumps(self.data))
        public, key = builder.build(self.manifest, self.root / 'first-versus', mode='versus')
        previous = self.root / 'first-versus/answer-key.json'
        same, _ = builder.build(self.manifest, self.root / 'split-versus', previous, mode='versus', delivery='split')
        self.assertEqual(public['revision'], same['revision'])
        self.assertEqual(public['items'][0]['cards'], same['items'][0]['cards'])
        self.data['items'][0]['script'] = '수정한 공통 평가 지침입니다.'
        self.manifest.write_text(json.dumps(self.data))
        changed, _ = builder.build(self.manifest, self.root / 'context-change', previous, mode='versus')
        self.assertNotEqual(public['revision'], changed['revision'])
        export = {'schema':1,'mode':'versus','study':key['study'],'version':key['version'],'revision':public['revision'],
                  'evaluator':'test','revealed':False,'active':0,'items':[{**key['comparison']['items'][0], 'events':['both','co-winners']}]}
        result = subprocess.run(['python3', str(PACKAGE / 'scripts/build_gallery.py'), 'summarize', '-', '--key', str(previous), '--blind'], input=json.dumps(export), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['totals']['complete'], 1)
        result = subprocess.run(['python3', str(PACKAGE / 'scripts/build_gallery.py'), 'build', str(self.manifest), '--output', str(self.root / 'cli-versus'), '--mode', 'versus', '--delivery', 'split'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        parser = Parser(); parser.feed((self.root / 'cli-versus/index.html').read_text())
        for script in parser.scripts:
            syntax = subprocess.run(['node', '--check'], input=script, text=True, capture_output=True)
            self.assertEqual(syntax.returncode, 0, syntax.stderr)
        changed = copy.deepcopy(export); changed['items'][0]['cards'][0]['failed'] = int(changed['items'][0]['cards'][0]['failed'])
        with self.assertRaises(ValueError): builder.summarize(changed, key)

    def test_versus_summary_validates_replay_and_preserves_failures(self):
        self.data = fixture(5, 2, 'text')
        self.manifest.write_text(json.dumps(self.data))
        public, key = builder.build(self.manifest, self.root / 'versus', mode='versus')
        export = {'schema': 1, 'mode': 'versus', 'study': key['study'], 'version': key['version'],
                  'revision': public['revision'], 'evaluator': 'test', 'revealed': False, 'active': 0,
                  'items': [{**copy.deepcopy(item), 'events': events} for item, events in zip(
                      key['comparison']['items'], [['both', 'both', 'co-winners'], ['left', 'right', 'left', 'left', 'left', 'right']])]}
        summary = builder.summarize(export, key, blind=True)
        self.assertEqual(summary['mode'], 'versus')
        self.assertEqual(summary['totals'], {'items': 2, 'complete': 2, 'pending': 0, 'incomparable': 0, 'failures': 1, 'outputs': 10})
        self.assertEqual(len(summary['items'][0]['winners']), 4)
        expected = key['comparison']['items'][1]['cards'][-1]['candidate']
        self.assertEqual(summary['items'][1]['winners'], [expected])
        self.assertEqual(summary['items'][1]['round'], 3)
        self.assertIn('공동', builder.markdown(summary))
        for candidate in self.data['candidates']:
            self.assertNotIn(candidate['name'], json.dumps(summary)); self.assertNotIn(candidate['id'], json.dumps(summary))
        invalid = []
        for field, value in [('study', 'other'), ('revision', 'stale'), ('version', 'other'), ('evaluator', ''), ('revealed', 'yes'), ('active', True)]:
            changed = copy.deepcopy(export); changed[field] = value; invalid.append(changed)
        changed = copy.deepcopy(export); changed['items'][0]['cards'][0]['fingerprint'] = 'stale'; invalid.append(changed)
        for events in [['co-winners'], ['right'] * 9, ['both'] * 100001]:
            changed = copy.deepcopy(export); changed['items'][0]['events'] = events; invalid.append(changed)
        for changed in invalid:
            with self.assertRaises(ValueError): builder.summarize(changed, key)
        export['items'][1]['events'] = []
        self.assertEqual(builder.summarize(export, key)['totals']['pending'], 1)

    def test_split_delivery_has_neutral_assets_and_no_embedded_key(self):
        import base64
        import zipfile
        self.data = fixture(3, 1)
        (self.root / 'prepared.html').write_text('<!doctype html><title>문서</title><p>중립 원본</p>')
        self.data['outputs'][1]['links'] = [{'label': '원본 문서', 'path': 'prepared.html'}]
        self.manifest.write_text(json.dumps(self.data, ensure_ascii=False))
        public, key = builder.build(self.manifest, self.root / 'split', delivery='split')
        root = self.root / 'split'
        self.assertTrue((root / 'answer-key.json').is_file())
        with zipfile.ZipFile(root / 'comparison.zip') as archive:
            self.assertEqual(set(archive.namelist()), {'index.html', *('assets/' + p.name for p in (root / 'assets').iterdir())})
            self.assertIsNone(archive.testzip())
            page = archive.read('index.html').decode()
            self.assertNotIn('data:audio/', page)
            mapping = base64.b64encode(json.dumps({'candidates':key['candidates']}, ensure_ascii=False).encode()).decode()
            self.assertNotIn(mapping, page)
            self.assertNotIn('answer-key.json', archive.namelist())
            for candidate in self.data['candidates']:
                for name in (candidate['id'], candidate['name']):
                    self.assertNotIn(name.encode(), b''.join(archive.read(p) for p in archive.namelist()))
                    self.assertNotIn(base64.b64encode(name.encode()), archive.read('index.html'))
            for card in public['items'][0]['cards']:
                if card['failed']: continue
                with wave.open(str(root / card['src']), 'rb') as audio:
                    self.assertEqual(audio.getnframes(), 1600)
                self.assertEqual(archive.read(card['src']), (self.root / 'prepared.wav').read_bytes())
                for link in card.get('links', []):
                    self.assertEqual(archive.read(link['href']), (self.root / 'prepared.html').read_bytes())
            self.assertIn('id="key-file"', page)

    def test_long_image_original_link_annotation_and_legacy_fingerprint(self):
        from PIL import Image
        Image.new('RGB', (600, 11000), 'white').save(self.root / 'tall.png')
        self.data = fixture(2, 1, kind='image')
        row = self.data['outputs'][1]
        row['path'] = 'tall.png'
        public, _ = self.build('legacy')
        legacy = next(c for c in public['items'][0]['cards'] if not c['failed'])
        page = (self.root / 'legacy/gallery.html').read_text()
        self.assertIn('원본 크기로 보기', page)
        self.assertTrue((self.root / 'legacy' / legacy['display_file']).exists())
        self.assertIn('target="_blank" rel="noopener noreferrer"', page)
        row['annotation'] = '<b>검증 완료</b>'
        (self.root / 'prepared.html').write_text('<html><p>익명 원본</p></html>')
        row['links'] = [{'label': '원본 문서', 'path': 'prepared.html'}]
        public2, _ = self.build('extended', self.root / 'legacy/answer-key.json')
        card = next(c for c in public2['items'][0]['cards'] if not c['failed'])
        self.assertNotEqual(card['fingerprint'], legacy['fingerprint'])
        page = (self.root / 'extended/gallery.html').read_text()
        self.assertIn('&lt;b&gt;검증 완료&lt;/b&gt;', page)
        self.assertNotIn('href="prepared.html"', page)
        self.assertTrue((self.root / 'extended' / card['links'][0]['href']).exists())
        public3, _ = self.build('same', self.root / 'extended/answer-key.json')
        self.assertEqual(card['fingerprint'], next(c for c in public3['items'][0]['cards'] if not c['failed'])['fingerprint'])

    def test_additional_public_evidence_rejects_identity_and_missing_files(self):
        self.data = fixture(2, 1, kind='text')
        row = self.data['outputs'][1]
        row['annotation'] = 'Model 1 won'
        with self.assertRaises(ValueError): self.build()
        del row['annotation']
        row['links'] = [{'label': '원본', 'path': 'prepared.html'}]
        (self.root / 'prepared.html').write_text('<title>Model&#32;1</title>')
        with self.assertRaises(ValueError): self.build()
        (self.root / 'prepared.html').write_text('<title>Anonymous</title>')
        row['links'][0]['label'] = 'engine-1'
        with self.assertRaises(ValueError): self.build()
        row['links'][0] = {'label': '원본', 'path': 'absent.html'}
        with self.assertRaises(ValueError): self.build()

    def test_binary_links_allow_short_ids_and_format_changes_reset_rating(self):
        from PIL import Image
        import random
        self.data = fixture(2, 1, kind='text')
        for i, candidate in enumerate(self.data['candidates']):
            candidate['id'] = ('a', 'b')[i]
            self.data['outputs'][i]['candidate_id'] = candidate['id']
        image = Image.frombytes('RGB', (64, 64), random.Random(7).randbytes(64 * 64 * 3))
        image.save(self.root / 'mobile.png')
        row = self.data['outputs'][1]
        row['links'] = [{'label': '모바일', 'path': 'mobile.png'}]
        self.build('binary')
        for suffix in ('html', 'txt'):
            (self.root / ('original.' + suffix)).write_text('<h1>Title</h1>')
        row['links'] = [{'label': '원본', 'path': 'original.html'}]
        public, _ = self.build('html', self.root / 'binary/answer-key.json')
        row['links'][0]['path'] = 'original.txt'
        public2, _ = self.build('txt', self.root / 'html/answer-key.json')
        card = lambda p: next(c for c in p['items'][0]['cards'] if not c['failed'])
        self.assertNotEqual(card(public)['fingerprint'], card(public2)['fingerprint'])

    def test_versus_html_previews_copy_blind_bytes_and_bind_revisions(self):
        import zipfile
        from PIL import Image
        Image.new('RGB', (800, 3400), 'white').save(self.root / 'capture.png')
        original = '<!doctype html><title>문서</title><details><summary>정답</summary>설명</details>'
        (self.root / 'prepared.html').write_text(original)
        self.data = fixture(3, 1, 'image')
        for row in self.data['outputs']:
            row.pop('error', None)
            row['path'] = 'capture.png'
            row['links'] = [{'label': '상호작용 문서', 'path': 'prepared.html'}]
        self.data['outputs'][0] = {k:v for k,v in self.data['outputs'][0].items() if k != 'links'}
        self.data['outputs'][0].update(kind='html', path='prepared.html')
        self.manifest.write_text(json.dumps(self.data))
        public, key = builder.build(self.manifest, self.root / 'html-versus', mode='versus')
        page = (self.root / 'html-versus/gallery.html').read_text()
        parser = Parser(); parser.feed(page)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertEqual(page.count('data-html-src='), 3)
        self.assertNotIn('<iframe', page)  # Frames are mounted on demand, never all in initial HTML.
        self.assertIn('class="sample-content"', page)
        self.assertIn('class="sample-choice"', page)
        for card in public['items'][0]['cards']:
            name = card.get('html_src') or card['links'][0]['href']
            self.assertRegex(name, r'^item-0001-slot-\d{4}-link-\d{4}\.html$')
            self.assertEqual((self.root / 'html-versus' / name).read_text(), original)
        previous = self.root / 'html-versus/answer-key.json'
        split, _ = builder.build(self.manifest, self.root / 'html-split', previous, mode='versus', delivery='split')
        self.assertEqual(public['revision'], split['revision'])
        with zipfile.ZipFile(self.root / 'html-split/comparison.zip') as archive:
            self.assertNotIn('answer-key.json', archive.namelist())
            for card in split['items'][0]['cards']:
                name = card.get('html_src') or card['links'][0]['href']
                self.assertTrue(name.startswith('assets/item-'))
                self.assertEqual(archive.read(name).decode(), original)
        (self.root / 'prepared.html').write_text(original + '<p>추가 조건</p>')
        changed, _ = builder.build(self.manifest, self.root / 'html-changed', previous, mode='versus')
        self.assertNotEqual(public['revision'], changed['revision'])
        self.assertEqual((self.root / 'html-versus' / next(c['html_src'] for c in public['items'][0]['cards'] if c['kind'] == 'html')).read_text(), original)
        with self.assertRaises(ValueError): builder.build(self.manifest, self.root / 'html-gallery')
        (self.root / 'prepared.html').write_text('<title>Model&#32;0</title>')
        with self.assertRaises(ValueError): builder.build(self.manifest, self.root / 'html-identity', mode='versus')

    def test_single_versus_embeds_minimal_validatable_key_and_separate_option(self):
        import base64
        import re
        self.data = fixture(3, 1, 'text')
        self.manifest.write_text(json.dumps(self.data))
        public, key = builder.build(self.manifest, self.root / 'embedded', mode='versus')
        page = (self.root / 'embedded/gallery.html').read_text()
        code = re.search(r'const embeddedAnswerKeyCode = "([^"]+)"', page)[1]
        embedded = json.loads(base64.b64decode(code))
        self.assertEqual(embedded['comparison']['revision'], public['revision'])
        self.assertEqual(len(embedded['outputs']), 3)
        self.assertTrue(all(set(row) == {'item', 'candidate', 'fingerprint', 'failed'} for row in embedded['outputs']))
        self.assertTrue(all(set(row) == {'name'} for row in embedded['candidates'].values()))
        self.assertNotIn('engine-0 failed', json.dumps(embedded))
        self.assertNotIn('<button id="reveal" disabled', page)
        previous = self.root / 'embedded/answer-key.json'
        separate, _ = builder.build(self.manifest, self.root / 'separate', previous, mode='versus', answer_key='separate')
        self.assertEqual(public['revision'], separate['revision'])
        page = (self.root / 'separate/gallery.html').read_text()
        self.assertIn('const embeddedAnswerKeyCode = ""', page)
        self.assertNotIn(code, page)
        self.assertNotIn('<button id="reveal" disabled', page)
        with self.assertRaises(ValueError):
            builder.build(self.manifest, self.root / 'unsafe-split', mode='versus', delivery='split', answer_key='embedded')

    def test_runtime_import_export_regressions(self):
        for script in ('test_blind_comparison_runtime.cjs', 'test_blind_comparison_versus.cjs'):
            result=subprocess.run(['node','--test',str(ROOT/'scripts'/script)],capture_output=True,text=True)
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
    def test_sticky_context_keeps_shared_script_and_rejects_identity_cues(self):
        self.data=fixture(3,2,'text')
        self.data['items'][0].update(title='발음 평가',script='공통 대본 <script>bad()</script>\n두 번째 줄입니다.')
        public,key=self.build();page=(self.root/'built/gallery.html').read_text()
        self.assertEqual(public['items'][0]['script'],self.data['items'][0]['script'])
        self.assertIn('공통 대본 &lt;script&gt;bad()&lt;/script&gt;',page)
        self.assertEqual(page.count('class="item-context"'),2)
        self.assertIn('aria-labelledby="context-0001" tabindex="0"',page)
        self.assertIn('<h2 id="context-0002">항목 2</h2>',page)
        for field in ('title','script'):
            self.data=fixture(3,1,'text');self.data['items'][0][field]='Model 1'
            with self.assertRaises(ValueError):self.build('bad-'+field)
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
    def test_partial_blind_stdin_summary_without_writing_or_revealing_key(self):
        _,key=self.build()
        valid=[r for r in key['outputs'] if not r['failed']]
        ratings=[{**{k:r[k] for k in ('item','candidate','fingerprint')},'score':score,'note':'','favorite':False}
                 for r,score in zip(valid,[4,None,2])]
        export={'schema':1,'study':key['study'],'version':key['version'],'evaluator':'test','revealed':False,'ratings':ratings}
        before=set(self.root.rglob('*'))
        result=subprocess.run(['python3',str(PACKAGE/'scripts/build_gallery.py'),'summarize','-',
                               '--key',str(self.root/'built/answer-key.json'),'--blind'],
                              input=json.dumps(export),text=True,capture_output=True,cwd=self.root)
        self.assertEqual(result.returncode,0,result.stderr)
        summary=json.loads(result.stdout)
        self.assertEqual(summary['totals'],{'rated':2,'missing':42,'failures':1,'total':45})
        self.assertEqual(set(self.root.rglob('*')),before)
        self.assertTrue(summary['blind']);self.assertFalse(summary['revealed'])
        for c in self.data['candidates']:
            self.assertNotIn(c['name'],result.stdout);self.assertNotIn(c['id'],result.stdout)
        self.assertNotIn(self.data['study_id'],result.stdout)
        self.assertTrue(all(row['candidate_id'] in key['candidates'] for row in summary['items']))
        self.assertEqual(sorted(row['mean'] for row in summary['candidates'] if row['mean'] is not None),[2,4])
        duplicate=json.dumps(export).replace('"schema": 1','"schema": 1, "schema": 1')
        invalid=subprocess.run(['python3',str(PACKAGE/'scripts/build_gallery.py'),'summarize','-',
                                '--key',str(self.root/'built/answer-key.json'),'--blind'],
                               input=duplicate,text=True,capture_output=True)
        self.assertNotEqual(invalid.returncode,0);self.assertEqual(invalid.stdout,'')
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
