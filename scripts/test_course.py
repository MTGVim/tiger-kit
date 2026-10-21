from __future__ import annotations
import copy,importlib.util,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'skills/tk-course/scripts'
sys.path.insert(0,str(SCRIPTS))
import build_course as builder
import build_catalog as catalog

def fixture(id='sample-course'):
    def lesson(n):
        caption='이 장에서는 입력에 따라 결과가 달라지는 이유를 알아봅니다.'
        return {'id':'lesson-'+str(n),'title':'조건과 결과 '+str(n),'revision':'1','section':'원리','kind':'slides','prerequisites':[] if n==1 else ['lesson-1'],'objective_ids':['predict'],'narration':'none','notes':'조건이 충족되면 결과가 바뀝니다. 다른 조건에서도 결과를 예측해 보세요.','slides':[{'id':'slide-'+str(n),'title':'입력에 따른 결과','type':'content','eyebrow':'원리','objective_ids':['predict'],'visual':{'items':[{'label':'입력과 조건','text':'조건에 맞는 입력만 결과에 반영합니다.'}]},'narration':[{'id':'cue-'+str(n),'speech':caption,'caption':caption,'focus':['item-1']}],'transcript':caption}],'questions':[{'id':'question-'+str(n),'prompt':'조건을 만족하지 않은 입력의 결과는 무엇인가요?','choices':[['skip','기존 결과를 유지합니다.'],['replace','항상 새 결과로 바꿉니다.']],'answer':'skip','explanation':'조건을 만족해야 새 결과가 반영됩니다.','objective_ids':['predict']}]}
    return {'schema':1,'id':id,'revision':'1','title':'조건에 따른 결과 예측','description':'조건과 결과의 관계를 배우고 새로운 입력을 예측하는 코스입니다.','level':'입문','objectives':[{'id':'predict','description':'주어진 조건에서 결과를 예측하고 근거를 설명합니다.'}],'sources':[{'title':'테스트용 출처','url':'https://example.org/spec'}],'lessons':[lesson(1),lesson(2)]}

class CourseTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.source=self.root/'course.json';self.data=fixture();self.write()
    def tearDown(self):self.tmp.cleanup()
    def write(self):self.source.write_text(json.dumps(self.data,ensure_ascii=False))
    def test_runtime_progress_opacity_and_grading(self):
        p=subprocess.run(['node','--test',str(ROOT/'scripts/test_course_runtime.cjs')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_build_multiple_lessons_and_actual_script_syntax(self):
        self.data['title']='새 주제 <script>alert(1)</script>';self.write()
        result=builder.build(self.source,self.root/'built');self.assertEqual(result['lessons'],2)
        page=(self.root/'built/index.html').read_text();self.assertIn('srcdoc',page);self.assertIn('기존 결과를 유지합니다.',page);self.assertNotIn('<title>새 주제 <script>',page)
        class Scripts(HTMLParser):
            def __init__(self):super().__init__();self.kind=None;self.current='';self.scripts=[];self.ids=[]
            def handle_starttag(self,tag,attrs):
                a=dict(attrs)
                if 'id' in a:self.ids.append(a['id'])
                if tag=='script':self.kind=a.get('type','js');self.current=''
            def handle_data(self,text):
                if self.kind:self.current+=text
            def handle_endtag(self,tag):
                if tag=='script':
                    if self.kind=='js':self.scripts.append(self.current)
                    self.kind=None
        for name in ['index','lesson-lesson-1','lesson-lesson-2']:
            html=(self.root/f'built/{name}.html').read_text();parser=Scripts();parser.feed(html)
            self.assertEqual(len(parser.ids),len(set(parser.ids)))
            for script in parser.scripts:
                p=subprocess.run(['node','--check'],input=script,text=True,capture_output=True);self.assertEqual(p.returncode,0,p.stderr)
            if name!='index':
                self.assertIn('id="caption-opacity"',html);self.assertIn('value="50"',html);self.assertIn('data-course-jump="lesson-2"',html);self.assertIn('id="reading-note"',html);self.assertNotIn('비동기 검색',html);self.assertNotIn('react.dev/reference/react/useEffect',html);self.assertIn('https://example.org/spec',html)
    def test_preflight_rejects_invalid_before_output(self):
        variants=[]
        x=fixture();x['lessons'][1]['id']='lesson-1';variants.append(x)
        x=fixture();x['lessons'][0]['prerequisites']=['lesson-2'];variants.append(x)
        x=fixture();x['lessons'][0]['slides'][0]['narration'][0]['focus']=[];variants.append(x)
        x=fixture();x['lessons'][0]['narration']='generated';variants.append(x)
        x=fixture();x['sources'][0]['url']='javascript:alert(1)';variants.append(x)
        for n,x in enumerate(variants):
            self.data=x;self.write();out=self.root/f'bad-{n}'
            with self.assertRaises(ValueError):builder.build(self.source,out)
            self.assertFalse(out.exists())
    def test_unsafe_or_missing_audio_and_symlink_are_rejected(self):
        self.data['lessons'][0]['slides'][0]['narration'][0]['audio']='../outside.wav';self.write()
        with self.assertRaises(ValueError):builder.build(self.source,self.root/'bad')
        path=self.root/'linked.json';path.symlink_to(self.source)
        with self.assertRaises(ValueError):builder.build(path,self.root/'bad')
    def test_incremental_revision_and_retention(self):
        old=copy.deepcopy(self.data);previous=self.root/'previous.json';previous.write_text(json.dumps(old))
        self.data['lessons'][0]['notes']='핵심 설명이 바뀌었습니다.';self.write()
        with self.assertRaisesRegex(ValueError,'revision'):builder.build(self.source,self.root/'bad',previous)
        self.data['lessons'][0]['revision']='2';self.write();builder.build(self.source,self.root/'changed',previous)
        changes=json.loads((self.root/'changed/changes.json').read_text());self.assertEqual([x['status'] for x in changes],['changed','retained']);self.assertEqual(json.loads(previous.read_text()),old)
        with self.assertRaises(ValueError):builder.build(self.source,self.root/'changed',previous)
    def test_collection_links_preserve_courses_and_reject_duplicate_identity(self):
        builder.build(self.source,self.root/'first');self.data=fixture('other-course');self.write();builder.build(self.source,self.root/'second')
        result=catalog.build(self.root,self.root/'catalog.html');self.assertEqual(result['courses'],2);self.assertIn('first/index.html',(self.root/'catalog.html').read_text())
        duplicate=self.root/'second/course.json';d=json.loads(duplicate.read_text());d['id']='sample-course';duplicate.write_text(json.dumps(d))
        with self.assertRaises(ValueError):catalog.build(self.root,self.root/'duplicate.html')
    def test_index_lesson_identity_cannot_overwrite_bundle_and_start_is_bound(self):
        self.data['lessons'][0]['id']='index';self.data['lessons'][1]['prerequisites']=['index'];self.write()
        builder.build(self.source,self.root/'reserved')
        self.assertIn('id="course-pages"',(self.root/'reserved/index.html').read_text())
        page=(self.root/'reserved/lesson-index.html').read_text()
        self.assertRegex(page,r'id="home-start"[^>]*data-course-jump="index"')
    def test_every_accepted_code_line_renders_and_notes_have_one_surface(self):
        slide=self.data['lessons'][0]['slides'][0];caption=slide['transcript']
        slide.update(type='code',code=['const id = 1;', 'await work();', 'if (id) {', '  compare();', '  render();', '}'],visual={'footnote':'결과 반영 전에 조건을 확인합니다.'},narration=[{'id':'code-cue','speech':caption,'caption':caption,'focus':['request-id','await','compare','render','takeaway']}]);self.write()
        builder.build(self.source,self.root/'code')
        page=(self.root/'code/lesson-lesson-1.html').read_text()
        self.assertIn('if (id) {',page)
        self.assertIn('<p id="reading-note">'+self.data['lessons'][0]['notes']+'</p>',page)
        self.assertNotIn('<p>'+self.data['lessons'][0]['notes']+'</p>',page)
    def test_collection_url_segments_remain_distinct(self):
        from urllib.parse import urlsplit,unquote
        names=['topic#1','topic?1','100% topic']
        for n,name in enumerate(names):
            self.data=fixture('course-'+str(n));self.write();builder.build(self.source,self.root/name)
        catalog.build(self.root,self.root/'catalog.html')
        class Links(HTMLParser):
            def __init__(self):super().__init__();self.links=[]
            def handle_starttag(self,tag,attrs):
                if tag=='a':self.links.append(dict(attrs)['href'])
        parser=Links();parser.feed((self.root/'catalog.html').read_text())
        for link in parser.links:
            u=urlsplit(link);self.assertFalse(u.query or u.fragment);self.assertTrue((self.root/unquote(u.path)).is_file())
        self.assertEqual(len(set(parser.links)),3)
    def test_changed_objective_requires_new_affected_lesson_revisions(self):
        builder.build(self.source,self.root/'old');previous=self.root/'old/course.json'
        self.data['objectives'][0]['description']='결과를 예측하고 실패 조건까지 설명합니다.';self.write()
        with self.assertRaisesRegex(ValueError,'revision'):builder.build(self.source,self.root/'bad-objective',previous)
        for lesson in self.data['lessons']:lesson['revision']='2'
        self.write();builder.build(self.source,self.root/'new-objective',previous)
        self.assertEqual([x['status'] for x in json.loads((self.root/'new-objective/changes.json').read_text())],['changed','changed'])
    def test_changed_same_path_audio_uses_persisted_digest(self):
        import wave,struct
        audio=self.root/'voice.wav'
        def wav(value):
            with wave.open(str(audio),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(struct.pack('<h',value)*240)
        wav(100);self.data['lessons'][0]['narration']='generated';self.data['lessons'][0]['slides'][0]['narration'][0]['audio']='voice.wav';self.write()
        builder.build(self.source,self.root/'old');previous=self.root/'old/course.json'
        wav(200)
        with self.assertRaisesRegex(ValueError,'revision'):builder.build(self.source,self.root/'bad-audio',previous)
        self.data['lessons'][0]['revision']='2';self.write();builder.build(self.source,self.root/'new-audio',previous)
        self.assertEqual(json.loads((self.root/'new-audio/changes.json').read_text())[0]['status'],'changed')
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg unavailable')
    def test_finished_video_requires_embedded_audio_when_selected(self):
        movie=self.root/'silent.mp4';subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=black:s=160x90:d=1','-an','-c:v','libx264',str(movie)],check=True)
        l=self.data['lessons'][1];l.pop('slides');l['kind']='video';l['video']={'src':'silent.mp4','narration':'embedded','captions':[{'id':'v1','start':0,'end':1,'caption':'조건과 결과를 확인합니다.'}]};self.write()
        with self.assertRaisesRegex(ValueError,'audio stream'):builder.build(self.source,self.root/'bad')
        self.data['lessons'][1]['video']['narration']='none';self.write();builder.build(self.source,self.root/'video-course')
        html=(self.root/'video-course/lesson-lesson-2.html').read_text();self.assertIn('data:video/mp4;base64,',html);self.assertIn('"has_audio": false',html)
if __name__=='__main__':unittest.main()
