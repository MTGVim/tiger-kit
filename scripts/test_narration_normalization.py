import importlib.util,json,math,shutil,struct,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('normalize_audio',ROOT/'skills/tk-tts/scripts/normalize_audio.py');normalizer=importlib.util.module_from_spec(spec);spec.loader.exec_module(normalizer)
class NarrationNormalizationTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def tone(self,name,amplitude,seconds=2):
        path=self.root/name
        with wave.open(str(path),'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000)
            wav.writeframes(b''.join(struct.pack('<h',int(amplitude*32767*math.sin(i*2*math.pi*440/24000))) for i in range(int(24000*seconds))))
        return path
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg unavailable')
    def test_two_pass_matches_different_levels_without_changing_originals_or_duration(self):
        inputs=[self.tone('quiet.wav',.03),self.tone('loud.wav',.5)];before=[p.read_bytes() for p in inputs]
        result=normalizer.normalize(inputs,self.root/'normalized')
        self.assertEqual([p.read_bytes() for p in inputs],before)
        self.assertTrue(all(r['mode']=='ebu-r128-two-pass' for r in result['files']))
        self.assertLess(abs(result['files'][0]['after']['rms_db']-result['files'][1]['after']['rms_db']),.5)
        for row in result['files']:
            self.assertAlmostEqual(row['after']['seconds'],row['before']['seconds'],delta=.1)
            self.assertLessEqual(float(row['loudness']['output_tp']),-1.4)
            self.assertAlmostEqual(float(row['loudness']['output_i']),-18,delta=.5)
        self.assertEqual(result['human_action'],'listen')
        with self.assertRaisesRegex(ValueError,'new safe'):normalizer.normalize(inputs,self.root/'normalized')
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg unavailable')
    def test_short_clips_report_rms_fallback_instead_of_claiming_lufs(self):
        result=normalizer.normalize([self.tone('short.wav',.02,.1)],self.root/'short-normalized')
        row=result['files'][0];self.assertEqual(row['mode'],'rms-fallback');self.assertTrue(row['limitation']);self.assertLessEqual(row['after']['peak_db'],-1.4)
    def test_missing_tool_silence_and_unsafe_input_preserve_destinations(self):
        tone=self.tone('safe.wav',.2)
        with patch.object(normalizer.shutil,'which',return_value=None):
            with self.assertRaisesRegex(ValueError,'FFmpeg'):normalizer.normalize([tone],self.root/'absent')
        self.assertFalse((self.root/'absent').exists())
        silent=self.tone('silent.wav',0)
        with self.assertRaisesRegex(ValueError,'silent'):normalizer.normalize([silent],self.root/'silent-output')
        link=self.root/'link.wav';link.symlink_to(tone)
        with self.assertRaisesRegex(ValueError,'nonsymlink'):normalizer.normalize([link],self.root/'unsafe')
