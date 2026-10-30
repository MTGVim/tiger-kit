from __future__ import annotations

from fractions import Fraction
import hashlib
import html
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import wave
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'skills/tk-video/scripts/build_movie.py'
spec = importlib.util.spec_from_file_location('animation_movie', SOURCE)
movie = importlib.util.module_from_spec(spec)
spec.loader.exec_module(movie)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'media tools unavailable')
class AnimationTests(unittest.TestCase):
    def fixture(self, root, fps='30', count=30, audio=False):
        video = root / 'source.mp4'
        command = ['ffmpeg', '-v', 'error', '-nostdin', '-n', '-f', 'lavfi', '-i', f'testsrc2=size=128x96:rate={fps}']
        if audio:
            command += ['-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000', '-ac', '2', '-c:a', 'aac']
        command += ['-frames:v', str(count), '-t', str(count / float(Fraction(fps))), '-c:v', 'libx264', '-threads', '1', '-pix_fmt', 'yuv420p', str(video)]
        subprocess.run(command, check=True, capture_output=True)
        data = {'mode': 'animation', 'video_path': str(video), 'caption_style': 'none'}
        manifest = root / 'manifest.json'
        manifest.write_text(json.dumps(data))
        return video, manifest, data

    def decoded(self, path):
        return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'])

    def test_source_rate_duration_resolution_and_motion_are_preserved(self):
        for fps, count in [('30', 30), ('30000/1001', 30), ('60', 60)]:
            with self.subTest(fps=fps), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                source, manifest, _ = self.fixture(root, fps, count)
                digest = hashlib.sha256(source.read_bytes()).hexdigest()
                result = movie.build(manifest, root / 'result.mp4')
                self.assertEqual(result['media_status'], 'ready')
                self.assertAlmostEqual(result['fps'], float(Fraction(fps)), places=6)
                self.assertEqual(result['fps_source'], 'video_stream')
                self.assertEqual((result['width'], result['height']), (128, 96))
                self.assertEqual(result['timing'], 'rendered')
                stream = next(s for s in movie.probe(root / 'result.mp4')['streams'] if s['codec_type'] == 'video')
                self.assertEqual(int(stream['nb_frames']), count)
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
                raw = self.decoded(root / 'result.mp4')
                size = 128 * 96 * 3
                self.assertGreater(len({hashlib.sha256(raw[i:i + size]).digest() for i in range(0, len(raw), size)}), 5)

    def test_soft_captions_have_tracks_and_vtt_without_burning_or_libass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, manifest, data = self.fixture(root)
            off = movie.build(manifest, root / 'off.mp4')
            data.pop('caption_style')
            data['captions'] = [{'start_ms': 0, 'end_ms': 1000, 'text': '버전 2와 <DOM>'}]
            manifest.write_text(json.dumps(data))
            with patch.object(movie, 'subtitle_filter', return_value=False) as filters:
                result = movie.build(manifest, root / 'soft.mp4')
            filters.assert_not_called()
            self.assertEqual(result['subtitles'], 'soft')
            self.assertEqual(result['media_status'], 'ready')
            self.assertEqual(self.decoded(Path(off['path'])), self.decoded(Path(result['path'])))
            subtitle = next(s for s in movie.probe(root / 'soft.mp4')['streams'] if s['codec_type'] == 'subtitle')
            self.assertEqual(subtitle['codec_name'], 'mov_text')
            self.assertEqual(result['subtitle_default'], bool(subtitle['disposition']['default']))
            self.assertEqual(subtitle['disposition']['forced'], 0)
            vtt = Path(result['captions_vtt_path']).read_text()
            self.assertTrue(vtt.startswith('WEBVTT\n'))
            self.assertIn('버전 2와 &lt;DOM&gt;', vtt)
            round_trip = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', result['path'], '-map', '0:s:0', '-f', 'srt', '-']).decode()
            self.assertIn('버전 2와 <DOM>', html.unescape(round_trip))

    def test_explicit_hard_captions_keep_missing_filter_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, manifest, data = self.fixture(root)
            data.update(caption_style='band', caption_delivery='hard', captions=[{'start_ms': 0, 'end_ms': 1000, 'text': 'Explicit hard captions'}])
            manifest.write_text(json.dumps(data))
            with patch.object(movie, 'media_tools', return_value=(shutil.which('ffmpeg'), shutil.which('ffprobe'), False)):
                result = movie.build(manifest, root / 'blocked.mp4')
            self.assertEqual(result['media_status'], 'blocked')
            self.assertEqual(result['prerequisite'], 'ffmpeg-subtitles-filter')
            self.assertEqual(result['subtitles'], 'soft')

    def test_embedded_stereo_audio_is_retained_and_conflicting_audio_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, manifest, _ = self.fixture(root, audio=True)
            result = movie.build(manifest, root / 'native-audio.mp4')
            stream = next(s for s in movie.probe(root / 'native-audio.mp4')['streams'] if s['codec_type'] == 'audio')
            self.assertEqual(stream['channels'], 2)
            self.assertTrue(result['source_audio_preserved'])
            self.assertTrue(result['audio'])
            with self.assertRaisesRegex(ValueError, 'embedded audio'):
                movie.build(manifest, root / 'conflict.mp4', source)

    def test_invalid_timing_long_audio_and_overwrite_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, manifest, data = self.fixture(root)
            for start, stop in [(-1, 500), (500, 500), (0, 1001)]:
                data['captions'] = [{'start_ms': start, 'end_ms': stop, 'text': 'Invalid interval'}]
                manifest.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    movie.build(manifest, root / 'invalid.mp4')
                self.assertFalse((root / 'invalid.mp4').exists())
            data.pop('captions'); manifest.write_text(json.dumps(data))
            voice = root / 'too-long.wav'
            with wave.open(str(voice), 'wb') as wav:
                wav.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
                wav.writeframes(b'\0' * (22050 * 2 * 2))
            with self.assertRaises(ValueError):
                movie.build(manifest, root / 'long.mp4', voice)
            output = root / 'existing.mp4'; output.write_bytes(b'preserve')
            with self.assertRaises(ValueError):
                movie.build(manifest, output)
            self.assertEqual(output.read_bytes(), b'preserve')

    def test_selected_narration_offsets_and_silence_guards_remain_active(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, manifest, data = self.fixture(root)
            voice = root / 'voice.wav'
            def audio(silent=False):
                import struct
                with wave.open(str(voice), 'wb') as wav:
                    wav.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
                    wav.writeframes(b''.join(struct.pack('<h', 0 if silent else int(8000 * math.sin(i * 2 * math.pi * 440 / 22050))) for i in range(5512)))
            audio()
            data.update(narration_requested=True, scenes=[{'start_ms': 500, 'audio_path': str(voice)}])
            manifest.write_text(json.dumps(data))
            result = movie.build(manifest, root / 'offset.mp4')
            self.assertEqual(result['media_status'], 'ready')
            self.assertTrue(result['audio'])
            samples = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', result['path'], '-map', '0:a:0', '-ar', '22050', '-f', 's16le', '-'])
            import array
            pcm = array.array('h', samples)
            self.assertLess(max(abs(x) for x in pcm[:8000]), 50)
            self.assertGreater(max(abs(x) for x in pcm[12000:16000]), 1000)
            audio(silent=True)
            result = movie.build(manifest, root / 'silent.mp4')
            self.assertIn('narration-silent', result['media_validation']['errors'])
            data['scenes'] = []; manifest.write_text(json.dumps(data))
            result = movie.build(manifest, root / 'missing.mp4')
            self.assertIn('narration-missing', result['media_validation']['errors'])

    def test_vtt_collisions_overlaps_and_symlinks_preserve_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, manifest, data = self.fixture(root)
            data.update(caption_style='overlay-rounded', captions=[{'start_ms': 0, 'end_ms': 1000, 'text': 'DOM'}])
            manifest.write_text(json.dumps(data))
            sidecar = root / 'collision.vtt'; sidecar.write_text('preserve')
            with self.assertRaisesRegex(ValueError, 'existing WebVTT'):
                movie.build(manifest, root / 'collision.mp4')
            self.assertEqual(sidecar.read_text(), 'preserve')
            self.assertFalse((root / 'collision.mp4').exists())
            data['captions'].append({'start_ms': 500, 'end_ms': 900, 'text': 'overlap'})
            manifest.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'overlapping'):
                movie.build(manifest, root / 'overlap.mp4')
            data['captions'] = []; link = root / 'link.mp4'; link.symlink_to(source)
            data['video_path'] = str(link); manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                movie.build(manifest, root / 'linked.mp4')
            self.assertTrue(source.is_file())

    def test_explicit_rate_conversion_is_reported_not_inherited_from_stills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _, manifest, _ = self.fixture(root)
            result = movie.build(manifest, root / 'converted.mp4', fps=15)
            self.assertEqual(result['fps'], 15)
            self.assertEqual(result['source_video']['fps'], 30)
            self.assertTrue(any('converted' in row for row in result['warnings']))
            for value in (0, -1, True, float('nan')):
                with self.subTest(fps=value), self.assertRaises(ValueError):
                    movie.build(manifest, root / 'bad-rate.mp4', fps=value)


if __name__ == '__main__':
    unittest.main()
