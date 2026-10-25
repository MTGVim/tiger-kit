from __future__ import annotations
import copy,importlib.util,json,os,shutil,subprocess,sys,tempfile,unittest
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

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),
                         'Course volume render regression requires an explicitly configured local browser')
    def test_volume_popover_browser_geometry_keyboard_and_touch(self):
        import wave
        with wave.open(str(self.root/'voice.wav'),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000);wav.writeframes(b'\x01\x00'*8000)
        for lesson in self.data['lessons']:
            lesson['narration']='generated'
            for slide in lesson['slides']:
                for cue in slide['narration']:cue['audio']='voice.wav'
        self.write();builder.build(self.source,self.root/'volume-browser')
        env={**os.environ,'TK_COURSE_PAGE':str(self.root/'volume-browser/index.html')}
        result=subprocess.run(['node','--test',str(ROOT/'evals/skills/tk-course/volume-popover.test.cjs')],env=env,capture_output=True,text=True,timeout=120)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),
                         'Course preferences/navigation render regression needs an explicitly configured browser')
    def test_preferences_navigation_browser_matrix(self):
        import wave
        original=copy.deepcopy(self.data['lessons'][0])
        self.data['lessons']=[]
        for n in range(1,21):
            item=copy.deepcopy(original);item.update(id='lesson-'+str(n),title='조건과 결과 '+str(n),prerequisites=[])
            second=copy.deepcopy(item['slides'][0]);second['id']='next-slide';second['narration'][0]['id']='next-cue';item['slides'].append(second)
            item['notes']='조건과 결과를 비교합니다.\n'*120
            self.data['lessons'].append(item)
        topic=self.root/'browser-topic';topic.mkdir()
        with wave.open(str(topic/'voice.wav'),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000);wav.writeframes(b'\x01\x00'*8000)
        for lesson in self.data['lessons']:
            lesson['narration']='generated'
            for slide in lesson['slides']:
                for cue in slide['narration']:cue['audio']='voice.wav'
        source=topic/'course.json';source.write_text(json.dumps(self.data));dist=self.root/'dist'
        builder.build(source,topic/'build',dist=dist)
        alone=self.root/'standalone';shutil.copytree(dist/'browser-topic',alone)
        env={**os.environ,'TK_COURSE_PAGE':str(dist/'browser-topic/index.html'),'TK_COURSE_STANDALONE':str(alone/'index.html'),'TK_COURSE_LONG_PAGE':str(dist/'browser-topic/index.html')}
        result=subprocess.run(['node','--test',str(ROOT/'evals/skills/tk-course/preferences-navigation.test.cjs')],env=env,capture_output=True,text=True,timeout=180)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

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
    def test_internal_objectives_are_metadata_and_not_svg_copy(self):
        from components import svg
        slide=self.data['lessons'][0]['slides'][0]
        self.assertIn('data-objectives="predict"',svg(0,slide))
        builder.check_visible_objectives(svg(0,slide),['predict'])
        with self.assertRaisesRegex(ValueError,'objective ID'):
            builder.check_visible_objectives('<svg><text>목표: predict</text></svg>',['predict'])
        builder.check_visible_objectives('<svg data-objectives="predict"><text>prediction</text></svg>',['predict'])
        # A legacy component used to render all objective IDs in its footer.
        legacy={**slide,'type':'code','code':['const n = 1;'],'visual':{'footnote':'조건이 맞으면 반영합니다.'}}
        image=svg(0,legacy);builder.check_visible_objectives(image,['predict'])
        self.assertNotIn('>predict</text>',image)
        builder.build(self.source,self.root/'notice-free')
        for file in (self.root/'notice-free').glob('*.html'):
            self.assertNotIn('🤖',file.read_text());self.assertNotIn('AI가 작성',file.read_text())
        self.assertIn('Permission is hereby granted',(self.root/'notice-free/lesson-lesson-1.html').read_text())

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
        duplicate=self.root/'second/index.html';duplicate.write_text(duplicate.read_text().replace('other-course','sample-course'))
        with self.assertRaises(ValueError):catalog.build(self.root,self.root/'duplicate.html')
    def test_catalog_embedded_manifest_refresh_backlinks_and_zip(self):
        dist=self.root/'dist';inputs=[]
        for n in range(2):
            topic=self.root/f'topic-{n}';topic.mkdir();source=topic/'course.json'
            data=fixture('course-'+str(n));data['title']='코스 '+str(n);source.write_text(json.dumps(data))
            inputs.append(source);result=builder.build(source,topic/'build',dist=dist)
            self.assertEqual(result['catalog'],str(dist/'index.html'))
            self.assertFalse((topic/'build/index.html').exists())
            self.assertEqual(sorted(x.name for x in (topic/'build').iterdir()),['changes.json','course.json'])
        unrelated=self.root/'notes';unrelated.mkdir();(unrelated/'index.html').write_text('keep')
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result=catalog.build(dist,zip_output=True);page=(dist/'index.html').read_text()
        self.assertEqual(result['courses'],2);self.assertEqual(page.count('data-catalog-card data-search='),2)
        self.assertIn('topic-0/index.html',page);self.assertIn('코스와 강의 검색',page)
        self.assertIn('aria-live="polite"',page);self.assertIn('id="catalog-clear"',page)
        self.assertNotIn('🤖',page);self.assertNotIn('AI가 작성',page)
        self.assertIn('<h1 class="ht-visually-hidden">학습 코스</h1>',page)
        self.assertEqual(page.count('<svg data-objectives='),2)
        self.assertEqual(catalog.build(dist)['courses'],2)
        self.assertEqual(page,(dist/'index.html').read_text())
        for name,content in before.items():self.assertEqual(Path(name).read_bytes(),content)
        import zipfile
        with zipfile.ZipFile(result['zip']['path']) as archive:
            self.assertEqual(set(archive.namelist()),{'index.html',*[f'topic-{n}/{name}' for n in range(2) for name in ['index.html','course-files.json','lessons/lesson-lesson-1.html','lessons/lesson-lesson-1.js','lessons/lesson-lesson-2.html','lessons/lesson-lesson-2.js']]})
            moved=self.root/'moved';archive.extractall(moved)
        self.assertEqual(catalog.build(moved)['courses'],2)
        for source in inputs:
            html=(dist/source.parent.name/'index.html').read_text()
            self.assertIn('href=\"../index.html\"',html.replace('\\"','"'))
            self.assertIn('tigerkit-course-manifest',html[:65536])
        target=dist/'custom.html';target.write_text("<script>const x='<meta name=\"tigerkit-course-catalog\">';</script>")
        with self.assertRaisesRegex(ValueError,'unmarked'):catalog.build(dist,target)
        original=target.read_bytes();link=dist/'linked.html';link.symlink_to(target)
        with self.assertRaises(ValueError):catalog.build(dist,link)
        self.assertEqual(original,target.read_bytes());link.unlink()
        manifest=dist/'topic-0/index.html';saved=manifest.read_bytes();manifest.unlink();manifest.symlink_to(inputs[0])
        with self.assertRaisesRegex(ValueError,'symlink'):catalog.build(dist)
        self.assertEqual(page,(dist/'index.html').read_text());manifest.unlink();manifest.write_bytes(saved)
        # Discovery is independent of source/build JSON and never reads the large media tail.
        for source in inputs:source.unlink()
        self.assertEqual(catalog.build(dist)['courses'],2)
        with manifest.open('ab') as stream:stream.write(b'X'*1000000)
        self.assertEqual(catalog.build(dist)['courses'],2)
        manifest.write_text('<html>unmarked</html>')
        with self.assertRaisesRegex(ValueError,'manifest'):catalog.build(dist)
        self.assertEqual(page,(dist/'index.html').read_text())
        archive=Path(result['zip']['path']);archive.write_text('user archive')
        with self.assertRaisesRegex(ValueError,'unmarked'):catalog.check_archive(archive)

    def test_header_guard_collection_path_and_audio_duration(self):
        builder.check_header('<header><span>A &amp; B</span><p hidden></p></header>','A & B')
        with self.assertRaises(ValueError):builder.check_header('<header><span>Title</span><p>Title</p></header>','Title')
        for name in ['javascript:alert(1)','https://example.org/index.html','//example.org/index.html','/index.html','..\\index.html','../index.html#home','%2f%2fexample.org/index.html','../index.html\n']:
            with self.assertRaises(ValueError):builder.build(self.source,self.root/'unsafe',collection_home=name)
            self.assertFalse((self.root/'unsafe').exists())
        self.assertEqual(builder.collection_path('../../my%20catalog.html'),'../../my%20catalog.html')
        # This is a local WAV fixture, not generated/listened-to speech.
        import wave
        audio=self.root/'voice.wav'
        with wave.open(str(audio),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000);wav.writeframes(b'\x01\x00'*10000)
        for lesson in self.data['lessons']:
            lesson['narration']='generated'
            for slide in lesson['slides']:
                for cue in slide['narration']:cue['audio']='voice.wav'
        self.write();builder.build(self.source,self.root/'audio')
        built=json.loads((self.root/'audio/course.json').read_text());self.assertEqual(built['narration_seconds'],2.5)
        self.assertEqual(catalog.duration_label(built),'음성 3초');built.pop('narration_seconds')
        self.assertEqual(catalog.duration_label(built),'음성 길이 미기록')
        for lesson in built['lessons']:lesson['narration']='none'
        self.assertEqual(catalog.duration_label(built),'무음')
        single=self.root/'single';single.mkdir();builder.build(self.source,single/'one')
        self.assertEqual(catalog.build(single)['courses'],1)
        self.assertTrue((single/'index.html').exists())
        empty=self.root/'empty';empty.mkdir()
        with self.assertRaisesRegex(ValueError,'at least one'):catalog.build(empty)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg unavailable')
    def test_compressed_narration_preserves_originals_and_rejects_silence_corruption(self):
        import math,struct,wave
        from audio_media import inspect_audio
        from unittest.mock import patch
        audio=self.root/'voice.wav'
        with wave.open(str(audio),'wb') as f:
            f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000)
            f.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(i*2*math.pi*440/24000))) for i in range(24000)))
        original=audio.read_bytes()
        for lesson in self.data['lessons']:
            lesson['narration']='generated'
            for slide in lesson['slides']:
                for cue in slide['narration']:cue['audio']='voice.wav'
        self.write()
        for format,mime in [('opus','audio/webm;codecs=opus'),('mp3','audio/mpeg'),('wav','audio/wav')]:
            out=self.root/format;builder.build(self.source,out,audio_format=format)
            manifest=json.loads((out/'course.json').read_text())['audio_build']
            self.assertEqual(manifest['format'],format);self.assertEqual(manifest['source_bytes'],len(original))
            if format!='wav':self.assertLess(manifest['encoded_bytes'],len(original)/3)
            self.assertLessEqual(abs(manifest['files'][0]['seconds']-1),.1)
            self.assertIn('data:'+mime+';base64,',(out/'lesson-lesson-1.html').read_text())
            self.assertEqual(audio.read_bytes(),original)
        for ext,codec in [('webm','libopus'),('ogg','libopus'),('mp3','libmp3lame'),('m4a','aac')]:
            dest=self.root/('compressed.'+ext)
            subprocess.run(['ffmpeg','-v','error','-i',str(audio),'-c:a',codec,str(dest)],check=True)
            self.assertAlmostEqual(inspect_audio(dest),1,delta=.1)
        with patch('audio_media.shutil.which',return_value=None):
            with self.assertRaisesRegex(ValueError,'ffmpeg is required'):builder.build(self.source,self.root/'no-tool')
            builder.build(self.source,self.root/'wav-without-tools',audio_format='wav')
            with self.assertRaisesRegex(ValueError,'ffprobe is required'):inspect_audio(self.root/'compressed.webm')
        broken=self.root/'broken.mp3';broken.write_bytes(b'broken')
        with self.assertRaises((ValueError,subprocess.SubprocessError)):inspect_audio(broken)
        silent=self.root/'silent.wav'
        with wave.open(str(silent),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000);f.writeframes(b'\x00\x00'*24000)
        with self.assertRaisesRegex(ValueError,'silent'):inspect_audio(silent)
        compressed=self.root/'silent.webm';subprocess.run(['ffmpeg','-v','error','-i',str(silent),'-c:a','libopus',str(compressed)],check=True)
        with self.assertRaisesRegex(ValueError,'silent'):inspect_audio(compressed)

    def test_distribution_cli_defaults_and_existing_output_safety(self):
        topic=self.root/'topic';topic.mkdir();source=topic/'course.json';source.write_bytes(self.source.read_bytes())
        result=subprocess.run([sys.executable,str(SCRIPTS/'build_course.py'),'--input',str(source),'--output',str(topic/'build')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        shared=self.root/'dist/topic/index.html';self.assertTrue(shared.is_file());self.assertTrue((self.root/'dist/index.html').is_file())
        self.assertFalse(list((topic/'build').glob('*.html')))
        self.assertEqual(sorted(str(p.relative_to(self.root/'dist')) for p in (self.root/'dist').rglob('*') if p.is_file()),['index.html','topic/course-files.json','topic/index.html','topic/lessons/lesson-lesson-1.html','topic/lessons/lesson-lesson-1.js','topic/lessons/lesson-lesson-2.html','topic/lessons/lesson-lesson-2.js'])
        before=shared.read_bytes()
        with self.assertRaisesRegex(ValueError,'review'):builder.build(source,topic/'next',dist=self.root/'dist')
        self.assertEqual(shared.read_bytes(),before);self.assertFalse((topic/'next').exists())
        for work,shared_root in [(self.root/'overlap',self.root/'overlap'),(self.root/'outer',self.root/'outer/dist'),(self.root/'shared/work',self.root/'shared')]:
            work.parent.mkdir(parents=True,exist_ok=True)
            with self.assertRaisesRegex(ValueError,'overlap'):builder.build(source,work,dist=shared_root)
            self.assertFalse(work.exists());self.assertFalse((shared_root/'index.html').exists())
        custom=self.root/'custom';builder.build(source,topic/'optional',dist=custom,lesson_pages=True)
        self.assertEqual(len(list((topic/'optional').glob('lesson-*.html'))),2)
        self.assertFalse((custom/'topic/lesson-lesson-1.html').exists())
        target=self.root/'user-dist';target.mkdir();(target/'index.html').write_text('my page')
        with self.assertRaisesRegex(ValueError,'unmarked'):builder.build(source,topic/'blocked',dist=target)
        self.assertFalse((topic/'blocked').exists());self.assertFalse((target/'topic').exists())

    def test_program_authoring_context_stays_out_of_distribution_and_zip(self):
        import zipfile
        plan=self.root/'reliability.plan.md'
        original='# Supplied plan\nPRIVATE-PROGRAM-PLAN\n'+''.join(f'{n}. Course {n}\n' for n in range(1,9))
        plan.write_text(original)
        topic=self.root/'course-01';topic.mkdir()
        source=topic/'course.json';source.write_bytes(self.source.read_bytes())
        sources=topic/'sources.md'
        deferred='Deferred: [course-02](../reliability.plan.md#course-02)'
        sources.write_text(deferred)
        dist=self.root/'dist';builder.build(source,topic/'build',dist=dist)
        result=catalog.build(dist,zip_output=True)
        expected=['course-01/course-files.json','course-01/index.html','course-01/lessons/lesson-lesson-1.html','course-01/lessons/lesson-lesson-1.js','course-01/lessons/lesson-lesson-2.html','course-01/lessons/lesson-lesson-2.js','index.html']
        self.assertEqual(sorted(str(p.relative_to(dist)) for p in dist.rglob('*') if p.is_file()),expected)
        for page in dist.rglob('*.html'):
            self.assertNotIn('PRIVATE-PROGRAM-PLAN',page.read_text())
            self.assertNotIn('reliability.plan.md',page.read_text())
        with zipfile.ZipFile(result['zip']['path']) as archive:
            self.assertEqual(sorted(archive.namelist()),expected)
        self.assertEqual(plan.read_text(),original);self.assertEqual(sources.read_text(),deferred)

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
