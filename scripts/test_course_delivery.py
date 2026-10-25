"""Portable public media, bounded entry HTML and explicit distribution allowlists."""
import hashlib,json,re,shutil,subprocess,tempfile,unittest,wave,zipfile
from pathlib import Path
from unittest.mock import patch
from test_course import fixture,builder,catalog,ROOT
from distribution import delivery_files,read_manifest

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.topic=self.root/'topic #한글';self.topic.mkdir()
        self.source=self.topic/'course.json';self.dist=self.root/'dist';self.data=fixture()
        self.data['lessons'][0]['id']='index';self.data['lessons'][1]['prerequisites']=['index']
        self.audio=self.topic/'private voice.wav'
        with wave.open(str(self.audio),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000);wav.writeframes(b'\x01\x00'*480000)
        for lesson in self.data['lessons']:
            lesson['narration']='supplied'
            for slide in lesson['slides']:
                for cue in slide['narration']:cue['audio']=self.audio.name
        self.source.write_text(json.dumps(self.data,ensure_ascii=False))

    def build(self,**options):
        return builder.build(self.source,self.topic/'build',dist=self.dist,audio_format='wav',**options)

    def test_default_folder_deduplicates_audio_and_zip_survives_move(self):
        original=self.audio.read_bytes();result=self.build(lesson_pages=True)
        entry=Path(result['path']);public=entry.parent
        self.assertEqual(result['delivery'],'folder');self.assertLess(entry.stat().st_size,10000)
        self.assertIn('entire',result['share_hint']);self.assertIn('frame.srcdoc=',entry.read_text())
        self.assertNotIn('id=\"lesson-data\"',entry.read_text())
        self.assertNotIn('fetch(',entry.read_text())
        files=delivery_files(public,read_manifest(entry))
        clips=list((public/'assets/audio').iterdir());self.assertEqual(len(clips),1)
        self.assertEqual(clips[0].read_bytes(),original);self.assertEqual(self.audio.read_bytes(),original)
        self.assertEqual(clips[0].stem,hashlib.sha256(original).hexdigest())
        for lesson in self.data['lessons']:
            page=public/'lessons'/('lesson-'+lesson['id']+'.html');html=page.read_text()
            self.assertNotIn('data:audio/',html);self.assertIn('href="../../index.html"',html)
            data=json.loads(re.search(r'id="lesson-data"[^>]*>(.*?)</script>',html,re.S)[1])
            path=data['slides'][0]['narration'][0]['audio']
            self.assertEqual((page.parent/path).resolve(),clips[0].resolve())
            direct=self.topic/'build'/('lesson-'+lesson['id']+'.html')
            self.assertIn('"audio": "assets/audio/',direct.read_text())
        (public/'private-notes.md').write_text('PRIVATE');(public/'assets/audio/unlisted.wav').write_bytes(original)
        archive=catalog.build(self.dist,zip_output=True)['zip']['path']
        with zipfile.ZipFile(archive) as zip:
            self.assertEqual(set(zip.namelist()),{'index.html',*[p.relative_to(self.dist).as_posix() for p in files]})
            moved=self.root/'moved';zip.extractall(moved)
        shutil.rmtree(self.dist);self.audio.unlink();self.source.unlink()
        self.assertEqual(catalog.build(moved)['courses'],1)
        moved_files=delivery_files(moved/self.topic.name,read_manifest(moved/self.topic.name/'index.html'))
        self.assertTrue(all(p.is_file() for p in moved_files))

    def test_single_file_is_explicit_and_aggregate_limit_refuses_before_publication(self):
        result=self.build(single_file=True)
        entry=Path(result['path']);self.assertIn('data:audio/wav;base64,',entry.read_text())
        self.assertEqual(delivery_files(entry.parent,read_manifest(entry)),[entry])
        with patch.object(builder,'SINGLE_FILE_LIMIT',100):
            with self.assertRaisesRegex(ValueError,'default folder'):
                builder.build(self.source,self.topic/'over-budget',dist=self.root/'oversized',audio_format='wav',single_file=True)
        self.assertFalse((self.root/'oversized').exists());self.assertFalse((self.topic/'over-budget').exists())
        pages=json.loads(re.search(r'id="course-pages"[^>]*>(.*?)</script>',entry.read_text(),re.S)[1])
        with patch.object(builder,'SINGLE_FILE_LIMIT',sum(len(page.encode('utf-8')) for page in pages.values())):
            with self.assertRaisesRegex(ValueError,'default folder'):
                builder.build(self.source,self.topic/'final-budget',dist=self.root/'final-oversized',audio_format='wav',single_file=True)
        self.assertFalse((self.root/'final-oversized').exists())

    def test_generated_loader_selects_one_lesson_and_retains_the_entry_frame(self):
        result=self.build()
        check=subprocess.run(['node',str(ROOT/'scripts/test_course_delivery_runtime.cjs'),result['path']],capture_output=True,text=True)
        self.assertEqual(check.returncode,0,check.stdout+check.stderr)

    def test_missing_symlinked_or_unlisted_file_preserves_catalog_and_archive(self):
        self.build();public=self.dist/self.topic.name;manifest=public/'course-files.json'
        result=catalog.build(self.dist,zip_output=True);archive=Path(result['zip']['path'])
        prior=(self.dist/'index.html').read_bytes();prior_zip=archive.read_bytes();original=manifest.read_bytes()
        value=json.loads(original)
        for name in ['../private.wav','assets/audio/private.wav','lessons/lesson-other.html','/etc/passwd']:
            manifest.write_text(json.dumps({**value,'files':value['files']+[name]}))
            with self.assertRaisesRegex(ValueError,'unexpected'):catalog.build(self.dist,zip_output=True)
            self.assertEqual(prior,(self.dist/'index.html').read_bytes());self.assertEqual(prior_zip,archive.read_bytes())
        manifest.write_bytes(original)
        clip=next((public/'assets/audio').iterdir());content=clip.read_bytes();clip.unlink()
        with self.assertRaisesRegex(ValueError,'missing public'):catalog.build(self.dist,zip_output=True)
        clip.symlink_to(self.audio)
        with self.assertRaisesRegex(ValueError,'symlink'):catalog.build(self.dist,zip_output=True)
        clip.unlink();clip.write_bytes(content)
        self.assertEqual(prior,(self.dist/'index.html').read_bytes());self.assertEqual(prior_zip,archive.read_bytes())

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_images_video_and_compressed_audio_remain_external(self):
        from PIL import Image
        Image.new('RGB',(800,450),'#5b8aaa').save(self.topic/'image.png')
        slide=self.data['lessons'][0]['slides'][0]
        slide['type']='image';slide['visual']={'src':'image.png','alt':'Inspected screen','description':'Screen evidence','source':'Locally authored fixture','rights':'Original test illustration','regions':[]}
        slide['narration'][0]['focus']=['image']
        lesson=self.data['lessons'][1];lesson.pop('slides');lesson['kind']='video';lesson.pop('narration')
        movie=self.topic/'movie.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=black:s=160x90:d=1','-an','-c:v','libx264',str(movie)],check=True)
        lesson['video']={'src':movie.name,'poster':'image.png','narration':'none','captions':[{'id':'v1','start':0,'end':1,'caption':'영상을 확인합니다.'}]}
        self.source.write_text(json.dumps(self.data))
        result=builder.build(self.source,self.topic/'build',dist=self.dist,audio_format='opus')
        public=Path(result['path']).parent
        for kind in ['image','video','audio']:self.assertEqual(len(list((public/'assets'/kind).iterdir())),1)
        for page in public.rglob('*.html'):self.assertNotRegex(page.read_text(),r'data:(?:image|video|audio)/')
        self.assertTrue(all(p.is_file() for p in delivery_files(public,read_manifest(public/'index.html'))))

if __name__=='__main__':unittest.main()
