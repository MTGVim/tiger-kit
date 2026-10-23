from __future__ import annotations
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from test_course import fixture,builder,catalog,ROOT
from distribution import read_manifest

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.dist=self.root/'dist';self.inputs={}
        for folder,id,title in [('aa-flaky','flaky','Flaky Test'),('zz-speed','speed','테스트 실행 최적화')]:
            topic=self.root/folder;topic.mkdir();source=topic/'course.json';data=fixture(id);data['title']=title;source.write_text(json.dumps(data));builder.build(source,topic/'build',dist=self.dist);self.inputs[id]=source
    def settings(self,value):
        (self.dist/'catalog.json').write_text(json.dumps(value,ensure_ascii=False))
    def hashes(self):return {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.dist.glob('*/index.html')}
    def test_collection_order_title_requires_dates_and_zip_leave_courses_unchanged(self):
        before=self.hashes();settings={'schema':1,'title':'Reliability <script>','order':['speed','flaky'],'requires':{'flaky':['speed']}};self.settings(settings)
        result=catalog.build(self.dist,zip_output=True);page=(self.dist/'index.html').read_text()
        self.assertLess(page.index('data-course-id="speed"'),page.index('data-course-id="flaky"'))
        self.assertIn('Reliability &lt;script&gt;',page);self.assertIn('먼저 들을 코스: 테스트 실행 최적화',page);self.assertIn('권장 1',page);self.assertIn('등록 ',page)
        self.assertEqual(before,self.hashes())
        with zipfile.ZipFile(result['zip']['path']) as archive:self.assertEqual(set(archive.namelist()),{'index.html','aa-flaky/index.html','zz-speed/index.html','catalog.json'})
        self.settings({'schema':1,'order':['flaky','speed']});catalog.build(self.dist)
        page=(self.dist/'index.html').read_text();self.assertLess(page.index('data-course-id="flaky"'),page.index('data-course-id="speed"'));self.assertEqual(before,self.hashes())
        (self.dist/'catalog.json').unlink();catalog.build(self.dist)
        self.assertNotIn('class="catalog-order"',(self.dist/'index.html').read_text());self.assertEqual(before,self.hashes())
    def test_invalid_settings_preserve_catalog_and_courses(self):
        before=(self.dist/'index.html').read_bytes();hashes=self.hashes()
        cases=[{'schema':True},{'schema':2},{'schema':1,'order':['speed','speed']},{'schema':1,'order':['absent']},{'schema':1,'requires':{'flaky':['absent']}},{'schema':1,'order':['flaky','speed'],'requires':{'flaky':['speed']}},{'schema':1,'requires':{'flaky':['speed'],'speed':['flaky']}},{'schema':1,'requires':{'speed':['speed']}},{'schema':1,'requires':{'flaky':['speed','speed']}},{'schema':1,'order':None},{'schema':1,'groups':[]},{'schema':1,'title':''}]
        for value in cases:
            with self.subTest(value=value):
                self.settings(value)
                with self.assertRaises(ValueError):catalog.build(self.dist)
                self.assertEqual(before,(self.dist/'index.html').read_bytes());self.assertEqual(hashes,self.hashes())
        (self.dist/'catalog.json').write_text('{"schema":1,"schema":1}')
        with self.assertRaisesRegex(ValueError,'duplicate'):catalog.build(self.dist)
        (self.dist/'catalog.json').unlink();(self.dist/'catalog.json').symlink_to(self.inputs['speed'])
        with self.assertRaisesRegex(ValueError,'symlink'):catalog.build(self.dist)
    def test_unlisted_courses_follow_title_and_requires_are_checked_against_full_order(self):
        self.settings({'schema':1,'order':['speed']});result=catalog.build(self.dist)
        self.assertEqual([x['course_id'] for x in result['course_links']],['speed','flaky'])
        self.settings({'schema':1,'order':[]});self.assertEqual([x['course_id'] for x in catalog.build(self.dist)['course_links']],['flaky','speed'])
    def test_new_course_requires_one_explicit_placement_and_invalid_input_writes_nothing(self):
        self.settings({'schema':1,'order':['speed','flaky'],'requires':{'flaky':['speed']}})
        topic=self.root/'new';topic.mkdir();source=topic/'course.json';source.write_text(json.dumps(fixture('new')))
        before=self.hashes();raw=(self.dist/'catalog.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'placement'):builder.build(source,topic/'build',dist=self.dist)
        self.assertFalse((topic/'build').exists());self.assertFalse((self.dist/'new').exists());self.assertEqual(raw,(self.dist/'catalog.json').read_bytes())
        with self.assertRaisesRegex(ValueError,'position'):builder.build(source,topic/'bad',dist=self.dist,catalog_position=0)
        builder.build(source,topic/'build',dist=self.dist,catalog_position=2)
        self.assertEqual(json.loads((self.dist/'catalog.json').read_text())['order'],['speed','new','flaky'])
        for p,hash in before.items():self.assertEqual(hash,hashlib.sha256(p.read_bytes()).hexdigest())
    def test_predeclared_new_course_does_not_need_another_placement(self):
        self.settings({'schema':1,'order':['speed','flaky','new']})
        topic=self.root/'new';topic.mkdir();source=topic/'course.json';source.write_text(json.dumps(fixture('new')))
        builder.build(source,topic/'build',dist=self.dist)
        self.assertEqual([x['course_id'] for x in catalog.build(self.dist)['course_links']],['speed','flaky','new'])
    def test_dates_follow_content_and_revision_not_mtime_or_collection_changes(self):
        source=self.inputs['speed'];topic=source.parent;data=json.loads(source.read_text())
        with patch.object(builder,'build_day',return_value='2026-10-01'):builder.build(source,topic/'dated')
        old=topic/'dated/course.json';self.assertEqual(read_manifest(topic/'dated/index.html')['created_at'],'2026-10-01')
        os.utime(old,(1,1));data['title']='다른 제목';source.write_text(json.dumps(data))
        with patch.object(builder,'build_day',return_value='2026-10-03'):builder.build(source,topic/'retained',old)
        retained=json.loads((topic/'retained/course.json').read_text());self.assertEqual(retained['updated_at'],'2026-10-01')
        data['lessons'][0]['revision']='2';source.write_text(json.dumps(data))
        with patch.object(builder,'build_day',return_value='2026-10-05'):builder.build(source,topic/'changed',topic/'retained/course.json')
        changed=json.loads((topic/'changed/course.json').read_text());self.assertEqual(changed['created_at'],'2026-10-01');self.assertEqual(changed['updated_at'],'2026-10-05')
        pages=json.loads((topic/'changed/index.html').read_text().split('<script id="course-pages" type="application/json">')[1].split('</script>')[0]);self.assertIn('등록 2026-10-01 · 업데이트 2026-10-05',next(iter(pages.values())))
        data['lessons'].pop();source.write_text(json.dumps(data))
        with patch.object(builder,'build_day',return_value='2026-10-07'):builder.build(source,topic/'removed',topic/'changed/course.json')
        self.assertEqual(json.loads((topic/'removed/course.json').read_text())['updated_at'],'2026-10-07')
        data['lessons'].append(fixture()['lessons'][1]);source.write_text(json.dumps(data))
        with patch.object(builder,'build_day',return_value='2026-10-09'):builder.build(source,topic/'added',topic/'removed/course.json')
        self.assertEqual(json.loads((topic/'added/course.json').read_text())['updated_at'],'2026-10-09')
    def test_legacy_dates_stay_unknown_until_changed_and_invalid_dates_fail(self):
        source=self.inputs['speed'];previous=source.parent/'build/course.json';old=json.loads(previous.read_text());old.pop('created_at');old.pop('updated_at');previous.write_text(json.dumps(old))
        builder.build(source,source.parent/'legacy',previous)
        self.assertNotIn('created_at',read_manifest(source.parent/'legacy/index.html'));self.assertNotIn('updated_at',read_manifest(source.parent/'legacy/index.html'))
        from distribution import date_label
        self.assertEqual(date_label({}),'')
        for value in ('2026-2-01','2026-02-30',None,True):
            with self.assertRaises(ValueError):date_label({'created_at':value})
        with self.assertRaises(ValueError):date_label({'created_at':'2026-10-03','updated_at':'2026-10-01'})

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),'Configured local browser required')
    def test_catalog_and_player_browser_regression(self):
        import math,struct,wave
        for n in range(1,5):
            topic=self.root/f'card-{n}';topic.mkdir();data=fixture(f'course-{n}')
            data['title']='실패율을 직접 재고 순서 섞기와 seed를 함께 비교하는 테스트 실행 최적화 '+str(n)
            data['description']=('needle 실제 설명을 끝까지 읽고 원인을 비교하는 실습입니다. ')*4
            data['level']='중급: Vitest나 Jest, Playwright를 실제 프로젝트에서 사용하는 개발자'
            created=['2026-10-02','2026-10-01','2026-10-03','2026-10-01'][n-1];updated=['2026-10-05','2026-10-05','2026-10-04','2026-10-01'][n-1]
            source=topic/'course.json';source.write_text(json.dumps(data))
            with patch.object(builder,'build_day',return_value=created):builder.build(source,topic/'old')
            if n==4:
                old=topic/'old/course.json';value=json.loads(old.read_text());value.pop('created_at');value.pop('updated_at');old.write_text(json.dumps(value))
            else:
                data['lessons'][0]['revision']='2';source.write_text(json.dumps(data))
            with patch.object(builder,'build_day',return_value=updated):builder.build(source,topic/'build',topic/'old/course.json',dist=self.root/'browser/dist')
        browser_root=self.root/'browser'
        (browser_root/'dist/catalog.json').write_text(json.dumps({'schema':1,'order':['course-1','course-2','course-3','course-4'],'requires':{'course-2':['course-1']}}));catalog.build(browser_root/'dist')
        topic=browser_root/'player';topic.mkdir();data=fixture('player')
        with wave.open(str(topic/'voice.wav'),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000);wav.writeframes(b''.join(struct.pack('<h',int(3000*math.sin(i*2*math.pi*440/24000))) for i in range(48000)))
        for lesson in data['lessons']:
            lesson['narration']='generated';slide=lesson['slides'][0];cue=slide['narration'][0];slide['narration']=[{**cue,'id':f'cue-{n}','audio':'voice.wav','caption':f'설명 {n}입니다.','speech':f'설명 {n}입니다.'} for n in range(3)];slide['transcript']=' '.join(c['caption'] for c in slide['narration'])
        source=topic/'course.json';source.write_text(json.dumps(data));builder.build(source,topic/'build',dist=browser_root/'player-dist')
        (browser_root/'blocked.html').write_text('<iframe id="host" src="player-dist/player/index.html" allow="fullscreen &#39;none&#39;" style="width:100%;height:100vh;border:0"></iframe>')
        if shutil.which('ffmpeg'):
            topic=browser_root/'video';topic.mkdir();data=fixture('video');data['lessons']=data['lessons'][:1];lesson=data['lessons'][0];lesson.pop('slides');lesson['kind']='video';lesson['video']={'src':'video.mp4','narration':'none','captions':[{'id':'caption','start':0,'end':12,'caption':'영상을 확인합니다.'}]}
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=black:s=160x90:r=10:d=12','-an','-c:v','libx264',str(topic/'video.mp4')],check=True)
            source=topic/'course.json';source.write_text(json.dumps(data));builder.build(source,topic/'build',dist=browser_root/'video-dist')
        env={**os.environ,'TK_CATALOG_FIXTURE':str(browser_root)}
        result=subprocess.run(['node','--test',str(ROOT/'evals/skills/tk-course/catalog-player.test.cjs')],env=env,capture_output=True,text=True,timeout=150)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
