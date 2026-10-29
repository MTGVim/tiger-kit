from __future__ import annotations
import importlib.util,io,json,sys,tempfile,types,unittest,contextlib
from pathlib import Path
from unittest.mock import patch,Mock
ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'skills/tk-tts/scripts'
sys.path.insert(0,str(SCRIPTS))
import qwen3
import ppaso
import list_options
from narration_policy import errors,sync,OWNERS
class TTSOwnerTests(unittest.TestCase):
    def test_option_inventory_is_read_only_and_preserves_first_class_and_legacy(self):
        with patch.object(qwen3.urllib.request,'urlopen') as net:
            rows=list_options.options();self.assertEqual({x['id'] for x in rows},{'qwen3-mlx-5bit','ppaso-onnx','qwen3-mlx-8bit','qwen3-pytorch'});self.assertTrue(all(not x['runtime_verified'] for x in rows));net.assert_not_called()
        self.assertIn('5bit',qwen3.mlx_adapter().manifest()['repository']);self.assertIn('8bit',qwen3.mlx_adapter().manifest(8)['repository'])
        self.assertNotEqual(qwen3.mlx_adapter().manifest()['files']['model.safetensors'],qwen3.mlx_adapter().manifest(8)['files']['model.safetensors'])
    def test_option_setup_status_never_claims_model_readiness_from_module_presence(self):
        for found, expected in [(None, 'missing'), (object(), 'modules-present-unverified')]:
            with patch.object(list_options.importlib.util, 'find_spec', return_value=found):
                rows = list_options.options()
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(row['dependency_status'] == expected for row in rows))
            self.assertTrue(all(row['model_cache_status'] == 'not-inspected' for row in rows))
            self.assertTrue(all(row['runtime_verified'] is False for row in rows))

    def test_mac_wheels_have_hashes_and_dictionary_is_pinned(self):
        d=ppaso.manifest();self.assertIn('python-mecab-ko-dic',d['dependencies'])
        for name in ['numpy','soundfile','python-mecab-ko','onnxruntime']:
            wheels=d['runtime_pins'][name]['wheels'];self.assertTrue(any('macosx' in x['filename'] for x in wheels),name);self.assertTrue(all(len(x['sha256'])==64 for x in wheels))
        self.assertTrue(qwen3.mlx_adapter().manifest()['mlx_wheels']['wheels'])
    def test_snapshot_whitelist_excludes_optional_assets(self):
        d=ppaso.manifest();self.assertEqual(sum(x.startswith('onnx/') for x in d['files']),8);self.assertIn('runtime/dict/korean_mfa.dict',d['files']);self.assertIn('example/ppaso_tts.py',d['files']);self.assertFalse(any(x.startswith(('rknn/','samples/')) or 'avatar' in x or 'lipsync' in x for x in d['files']))
        self.assertEqual(d['revision'],'53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9')
    def test_ppaso_mismatch_names_actual_expected_and_restore(self):
        with patch.object(ppaso.importlib.util,'find_spec',return_value=object()),patch.object(ppaso.importlib.metadata,'version',return_value='wrong'):
            with self.assertRaisesRegex(ValueError,'actual=wrong, expected=.*pip install'):ppaso.verify_runtime(ppaso.manifest())
    def test_ppaso_missing_dependency_never_downloads_or_loads_model(self):
        with patch.object(sys,'argv',['ppaso','--verify']),patch.object(ppaso.importlib.util,'find_spec',side_effect=lambda n:None if n=='soundfile' else object()),patch.object(qwen3.urllib.request,'urlopen') as net,patch.object(ppaso,'load_runtime') as load,contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(ppaso.main(),1);self.assertEqual(json.loads(out.getvalue())['detail'],'missing runtime module: soundfile');net.assert_not_called();load.assert_not_called()
    def test_shared_narration_contract_detects_drift_and_repairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in OWNERS:
                p=root/'skills'/name/'SKILL.md';p.parent.mkdir(parents=True);p.write_text('# Skill\n')
            self.assertEqual(len(errors(root)),len(OWNERS));sync(root);self.assertEqual(errors(root),[])
            p=root/'skills/tk-explain/SKILL.md';p.write_text(p.read_text().replace('Ask the creator','Assume the creator'));self.assertTrue(errors(root));sync(root);self.assertEqual(errors(root),[])
    def test_ppaso_silence_rejects_without_switching_engine(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);script=root/'text.txt';script.write_text('테스트 문장입니다.');output=root/'voice.wav';factory=Mock();factory.return_value.synthesize.return_value=np.zeros(1000)
            with patch.object(qwen3,'verify',return_value=ppaso.manifest()),patch.object(ppaso,'verify_runtime'),patch.object(ppaso,'load_runtime',return_value=factory),patch.dict(sys.modules,{'soundfile':types.SimpleNamespace()}),patch.object(qwen3,'write_audio') as write:
                with self.assertRaisesRegex(ValueError,'silent narration'):ppaso.synthesize(root,script,output)
                write.assert_not_called();factory.assert_called_once_with(root,backend='onnx',device='cpu');self.assertFalse(output.exists())
if __name__=='__main__':unittest.main()
