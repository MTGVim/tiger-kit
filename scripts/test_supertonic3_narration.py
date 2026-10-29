from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/tk-tts/scripts'
sys.path.insert(0, str(SCRIPTS))
import list_options
import qwen3 as common
import supertonic3


class Supertonic3Tests(unittest.TestCase):
    def test_optional_inventory_preserves_defaults_and_reports_disclosure(self):
        for system, machine, recommended in [('Darwin', 'arm64', 'qwen3-mlx-5bit'),
                                               ('Linux', 'x86_64', 'qwen3-pytorch')]:
            with patch.object(list_options.platform, 'system', return_value=system), \
                    patch.object(list_options.platform, 'machine', return_value=machine), \
                    patch.object(common.urllib.request, 'urlopen') as net:
                rows = list_options.options()
            self.assertEqual([r['id'] for r in rows if r['recommended']], [recommended])
            row = next(r for r in rows if r['id'] == 'supertonic3-onnx')
            self.assertEqual(row['speakers'], ['F1'])
            self.assertTrue(row['platform_supported'])
            self.assertFalse(row['runtime_verified'])
            self.assertTrue(row['disclosure_required'])
            self.assertEqual(row['upstream_status'], 'archived')
            net.assert_not_called()

    def test_manifest_pins_model_helper_licenses_and_core_wheels(self):
        data = supertonic3.manifest()
        self.assertEqual(len(data['files']), 11)
        self.assertEqual(sum(n.endswith('.onnx') for n in data['files']), 4)
        self.assertEqual([n for n in data['files'] if n.startswith('voice_styles/')], ['voice_styles/F1.json'])
        self.assertTrue({'LICENSE', 'README.md', 'runtime/LICENSE', 'runtime/helper.py'} <= data['files'].keys())
        for name, expected in data['dependencies'].items():
            pin = data['runtime_pins'][name]
            self.assertEqual(pin['version'], expected)
            self.assertTrue(any('macosx' in row['filename'] for row in pin['wheels']))
            self.assertTrue(all(len(row['sha256']) == 64 and row['bytes'] > 0 for row in pin['wheels']))

    def test_download_uses_pinned_source_urls_and_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'snapshot'
            url = supertonic3.manifest()['file_urls']['runtime/helper.py']
            payload = b'# pinned helper fixture\n'
            data = {'repository': 'owner/model', 'revision': 'fixed', 'file_urls': {'runtime/helper.py': url},
                    'files': {'runtime/helper.py': hashlib.sha256(payload).hexdigest()}}
            with patch.dict(common.os.environ, {'HF_HUB_CACHE': str(Path(directory).resolve() / 'hub')}), \
                    patch.object(common.urllib.request, 'urlopen', return_value=io.BytesIO(payload)) as net:
                common.download(root, data)
            self.assertEqual(net.call_args.args[0], url)
            self.assertEqual(common.verify(root, data), data)
            (root / 'runtime/helper.py').write_text('# changed')
            with patch.object(common.urllib.request, 'urlopen') as net:
                with self.assertRaisesRegex(ValueError, 'existing mismatched model file preserved'):
                    common.download(root, data)
            net.assert_not_called()

    def test_runtime_mismatch_names_actual_expected_and_restore(self):
        with patch.object(supertonic3.importlib.util, 'find_spec', return_value=object()), \
                patch.object(supertonic3.importlib.metadata, 'version', return_value='wrong'):
            with self.assertRaisesRegex(ValueError, 'actual=wrong, expected=.*pip install'):
                supertonic3.verify_runtime(supertonic3.manifest())

    def test_missing_runtime_never_downloads_or_loads_model(self):
        with patch.object(sys, 'argv', ['supertonic3', '--verify']), \
                patch.object(supertonic3.importlib.util, 'find_spec', side_effect=lambda n: None if n == 'soundfile' else object()), \
                patch.object(common.urllib.request, 'urlopen') as net, \
                patch.object(supertonic3, 'load_runtime') as load, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(supertonic3.main(), 1)
        self.assertEqual(json.loads(out.getvalue())['detail'], 'missing runtime module: soundfile')
        net.assert_not_called()
        load.assert_not_called()

    def test_unverified_snapshot_never_imports_helper(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(supertonic3, 'load_runtime') as load, patch.object(common.urllib.request, 'urlopen') as net:
                with self.assertRaisesRegex(ValueError, 'missing or unpinned'):
                    supertonic3.synthesize(Path(directory).resolve(), Path('unused.txt'), Path('unused.wav'))
            load.assert_not_called()
            net.assert_not_called()

    def run_mock_synthesis(self, root, audio=None, duration=None, providers=None):
        import numpy as np
        helper = Mock()
        model = helper.load_text_to_speech.return_value
        model.sample_rate = 44100
        for name in ['dp_ort', 'text_enc_ort', 'vector_est_ort', 'vocoder_ort']:
            getattr(model, name).get_providers.return_value = providers or ['CPUExecutionProvider']
        model.batch.return_value = (audio if audio is not None else np.full((1, 44600), .1),
                                    duration if duration is not None else np.array([1.0]))
        helper.chunk_text.side_effect = lambda row, max_len: ['first', 'second'] if row.startswith('첫') else ['third']
        script = root / 'script.txt'
        script.write_text('첫 문장입니다.\n다음 문장입니다.', encoding='utf-8')
        with patch.object(common, 'verify', return_value=supertonic3.manifest()), \
                patch.object(supertonic3, 'verify_runtime'), patch.object(supertonic3, 'load_runtime', return_value=helper), \
                patch.dict(sys.modules, {'soundfile': types.SimpleNamespace()}), \
                patch.dict(common.os.environ, {}, clear=True), patch.object(common, 'write_audio') as write, \
                patch.object(common.urllib.request, 'urlopen') as net:
            result = supertonic3.synthesize(root, script, root / 'voice.wav')
            self.assertEqual(common.os.environ['HF_HUB_OFFLINE'], '1')
        net.assert_not_called()
        return result, model, helper, write

    def test_cpu_sentence_order_chunk_padding_crop_and_disclosure_receipt(self):
        import numpy as np
        audio = np.concatenate([np.full(44100, .1), np.full(500, .8)])[None, :]
        with tempfile.TemporaryDirectory() as directory:
            result, model, helper, write = self.run_mock_synthesis(Path(directory).resolve(), audio=audio)
        helper.load_text_to_speech.assert_called_once_with(str(Path(directory).resolve() / 'onnx'), use_gpu=False)
        self.assertEqual([call.args[0] for call in model.batch.call_args_list], [['first'], ['second'], ['third']])
        self.assertTrue(all(c.args[1] == ['ko'] and c.kwargs == {'total_step': 8, 'speed': 1.05} for c in model.batch.call_args_list))
        samples, rate, _ = write.call_args.args
        self.assertEqual(rate, 44100)
        self.assertEqual(len(samples), 3 * rate + round(.3 * rate))
        self.assertLess(float(samples.max()), .11)
        self.assertTrue(np.all(samples[rate:rate + round(.3 * rate)] == 0))
        self.assertEqual(result['sentence_count'], 2)
        self.assertEqual(result['native_chunk_count'], 3)
        self.assertAlmostEqual(result['duration_seconds'], 3.3)
        self.assertEqual(result['human_action'], 'listen')
        self.assertEqual(result['speaker'], 'F1')
        self.assertTrue(result['disclosure_required'])
        self.assertEqual(result['disclosure_notice'], '이 음성은 AI로 합성되었습니다.')

    def test_invalid_silent_and_short_audio_rejected_without_wav(self):
        import numpy as np
        for audio, duration in [(np.zeros((1, 44100)), np.array([1.])),
                                (np.full((1, 44100), np.nan), np.array([1.])),
                                (np.full((1, 44100), .1), np.array([np.nan])),
                                (np.full((1, 44100), .1), np.array([0.])),
                                (np.full((1, 44100), .1), np.array([2.])),
                                (np.ones(44100), np.array([1.]))]:
            with self.subTest(duration=duration), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                with self.assertRaises(ValueError):
                    self.run_mock_synthesis(root, audio=audio, duration=duration)
                self.assertFalse((root / 'voice.wav').exists())

    def test_provider_fallback_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'CPUExecutionProvider only'):
                self.run_mock_synthesis(Path(directory).resolve(), providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])


if __name__ == '__main__':
    unittest.main()
