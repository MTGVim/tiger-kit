"""Behavior protection for explanation-first courses and explicit narration routes."""
import copy,json,math,os,re,struct,subprocess,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import patch
from test_course import fixture,builder,catalog
from components import svg
from slide_components import table

def diagram():
    caption='응답을 반영하기 전에 요청 번호를 검사합니다.'
    return {'id':'commit-path','type':'diagram','title':'번호가 일치하면 결과를 반영합니다',
            'objective_ids':['predict'],
            'visual':{'nodes':[{'id':'response','label':'응답 도착','row':0,'column':0},
                               {'id':'guard','label':'번호 검사','row':0,'column':1},
                               {'id':'result','label':'일치 시 반영','row':0,'column':2}],
                      'edges':[{'id':'check','from':'response','to':'guard'},
                               {'id':'commit','from':'guard','to':'result'}]},
            'narration':[{'id':'explain','speech':caption,'caption':caption,
                          'focus':['node-response','node-guard','node-result','edge-check','edge-commit']}],
            'transcript':caption}

class ExplanationAuthoringTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.data=fixture()
    def tearDown(self):self.tmp.cleanup()
    def build(self):
        source=self.root/'course.json';source.write_text(json.dumps(self.data))
        return builder.build(source,self.root/'build')
    def lesson_data(self):
        html=(self.root/'build/lesson-lesson-1.html').read_text()
        return json.loads(re.search(r'<script[^>]*id="lesson-data"[^>]*>(.*?)</script>',html,re.S)[1])
    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),'Browser narration recovery needs an explicitly configured browser')
    def test_browser_narration_settings_and_silent_recovery(self):
        for lesson in self.data['lessons']:lesson['narration']='browser'
        second=diagram();second['id']='two-row';second['narration'][0]['id']='two-row-explanation'
        second['visual']['nodes']=[{'id':str(i),'label':word,'row':i//3,'column':i%3} for i,word in enumerate(['입력','검사','반영','출력','완료','대기'])]
        pairs=[(0,1),(1,2),(2,5),(5,4),(4,3)]
        second['visual']['edges']=[{'id':str(i),'from':str(a),'to':str(b)} for i,(a,b) in enumerate(pairs)]
        second['narration'][0]['focus']=['node-'+str(i) for i in range(6)]+['edge-'+str(i) for i in range(5)]
        self.data['lessons'][0]['slides']=[diagram(),second]
        self.data['pacing']={key:0 for key in ['initialLeadInMs','postSlideHoldMs','slidePauseMs','sentencePauseMs']}
        self.build()
        env={**os.environ,'TK_COURSE_BROWSER_PAGE':str(self.root/'build/index.html')}
        result=subprocess.run(['node','--test',str(Path(__file__).resolve().parents[1]/'evals/skills/tk-course/browser-narration.test.cjs')],env=env,capture_output=True,text=True,timeout=60)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_browser_course_needs_no_audio_tool_and_declares_browser_transport(self):
        for lesson in self.data['lessons']:lesson['narration']='browser'
        self.data['lessons'][0]['slides']=[diagram()]
        with patch.object(builder.shutil,'which',return_value=None):
            self.build()
        data=self.lesson_data()
        self.assertEqual(data['production_choices']['voice'],'browser')
        self.assertFalse(any(c.get('audio') for s in data['slides'] for c in s['narration']))
        self.assertEqual(self.selected_mode(),'device')
        self.assertIn('node-guard',(self.root/'build/index.html').read_text())
        self.assertEqual(json.loads((self.root/'build/course.json').read_text())['narration_seconds'],0)
    def selected_mode(self):
        html=(self.root/'build/lesson-lesson-1.html').read_text()
        options=re.search(r'<select id="voice-mode">(.*?)</select>',html,re.S)[1]
        return re.search(r'<option value="([^"]+)" selected>',options)[1]
    def test_browser_catalog_reports_unmeasured_speech_not_silence(self):
        for lesson in self.data['lessons']:lesson['narration']='browser'
        source=self.root/'course.json';source.write_text(json.dumps(self.data))
        builder.build(source,self.root/'working',dist=self.root/'dist')
        public=(self.root/'dist/index.html').read_text()
        self.assertIn('브라우저 음성 · 길이 미정',public)
        self.assertEqual(catalog.duration_label({**self.data,'narration_seconds':0}),'브라우저 음성 · 길이 미정')
        with self.assertRaises(ValueError):catalog.duration_label({**self.data,'narration_seconds':float('nan')})
    def test_explicit_silence_remains_silent_in_the_player(self):
        self.build();self.assertEqual(self.selected_mode(),'silent')
    def test_browser_selection_does_not_hide_selected_file_audio(self):
        lesson=self.data['lessons'][0];lesson['narration']='browser'
        clip=self.root/'voice.wav'
        with wave.open(str(clip),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000)
            wav.writeframes(b''.join(struct.pack('<h',int(10000*math.sin(i/5))) for i in range(2000)))
        lesson['slides'][0]['narration'][0]['audio']='voice.wav'
        with self.assertRaisesRegex(ValueError,'browser.*file audio'):self.build()
        self.assertFalse((self.root/'build').exists())
    def test_supplied_audio_is_measured_and_uses_assets(self):
        with wave.open(str(self.root/'voice.wav'),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000)
            wav.writeframes(b''.join(struct.pack('<h',int(10000*math.sin(i/5))) for i in range(2000)))
        for lesson in self.data['lessons']:
            lesson['narration']='supplied';lesson['slides'][0]['narration'][0]['audio']='voice.wav'
        self.build();data=self.lesson_data()
        self.assertEqual(data['production_choices']['voice'],'supplied')
        self.assertEqual(self.selected_mode(),'assets')
        self.assertTrue(data['slides'][0]['narration'][0]['audio'].startswith('data:audio/'))
        self.assertEqual(json.loads((self.root/'build/course.json').read_text())['narration_seconds'],.5)
    def test_diagram_preserves_entities_arrows_and_accessible_relationships(self):
        slide=diagram();markup=svg(0,slide,responsive=True)
        self.assertIn('node-guard',markup);self.assertIn('edge-commit',markup)
        self.assertIn('marker-end=',markup)
        self.assertIn('응답 도착 → 번호 검사',table(slide))
        slide['visual']['nodes'][0]['label']='<script>'
        markup=svg(0,slide);self.assertIn('&lt;script&gt;',markup);self.assertNotIn('<script>',markup)
    def test_invalid_graphs_fail_before_output(self):
        mutations=[
            lambda v:v['nodes'][1].update(column=0),
            lambda v:v['nodes'][1].update(row=True),
            lambda v:v['edges'][0].update(to='missing'),
            lambda v:v['edges'][0].update(to='result'),
            lambda v:v['nodes'][1].update(id='response'),
            lambda v:v['edges'].append({'id':'reverse','from':'guard','to':'response'}),
        ]
        for change in mutations:
            slide=diagram();change(slide['visual'])
            with self.subTest(visual=slide['visual']),self.assertRaises(ValueError):svg(0,slide)

if __name__=='__main__':unittest.main()
