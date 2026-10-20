from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("optional_qwen3", ROOT / "skills/tk-video/scripts/narration/qwen3.py")
qwen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qwen)


class Qwen3NarrationTests(unittest.TestCase):
    def test_reviewed_pins_include_weights_tokenizer_and_package(self):
        data = qwen.manifest()
        self.assertEqual(data["package"]["version"], "0.1.1")
        self.assertEqual(len(data["package"]["sha256"]), 64)
        self.assertEqual(len(data["revision"]), 40)
        self.assertIn("model.safetensors", data["files"])
        self.assertIn("speech_tokenizer/model.safetensors", data["files"])
        self.assertIn("README.md", data["files"])
        self.assertTrue(all(len(x) == 64 for x in data["files"].values()))

    def test_offline_verification_rejects_tamper_extra_files_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "file").write_bytes(b"expected")
            data = {"files": {"file": hashlib.sha256(b"expected").hexdigest()}}
            with patch.object(qwen, "manifest", return_value=data), patch.object(qwen.urllib.request, "urlopen") as net:
                self.assertEqual(qwen.verify(root), data)
                (root / "override.py").write_text("unreviewed")
                with self.assertRaises(ValueError): qwen.verify(root)
                (root / "override.py").unlink()
                (root / "link").symlink_to(root / "file")
                with self.assertRaises(ValueError): qwen.verify(root)
                (root / "link").unlink(); (root / "file").write_bytes(b"changed")
                with self.assertRaises(ValueError): qwen.verify(root)
                net.assert_not_called()

    def test_invalid_speaker_is_rejected_before_model_loading(self):
        with self.assertRaises(ValueError):
            qwen.synthesize(Path("missing"), Path("missing.txt"), Path("out.wav"), "unselected")

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "numpy unavailable")
    def test_synthesis_uses_local_snapshot_and_offline_nested_loads(self):
        import numpy as np
        from unittest.mock import Mock
        sound = np.sin(np.arange(2000) * .1).astype(np.float32) * .1
        model = Mock()
        model.generate_custom_voice.return_value = ([np.concatenate([np.zeros(1000), sound])], 1000)
        factory = Mock()
        factory.from_pretrained.return_value = model
        torch = types.SimpleNamespace(float32="float32")
        sf = Mock()
        sf.write.side_effect = lambda path, *a, **kw: path.write_bytes(b"decoded wav fixture")
        sf.read.return_value = (sound, 1000)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); text = root / "script.txt"; text.write_text("Korean script")
            output = root / "voice.wav"
            with patch.object(qwen, "verify", return_value=qwen.manifest()), \
                    patch.object(qwen.importlib.metadata, "version", return_value="0.1.1"), \
                    patch.dict("sys.modules", {"torch": torch, "soundfile": sf, "qwen_tts": types.SimpleNamespace(Qwen3TTSModel=factory)}), \
                    patch.dict(qwen.os.environ, {}, clear=True), patch.object(qwen.urllib.request, "urlopen") as net:
                result = qwen.synthesize(root, text, output, "sohee", "cpu")
                self.assertEqual(qwen.os.environ["HF_HUB_OFFLINE"], "1")
                self.assertEqual(qwen.os.environ["TRANSFORMERS_OFFLINE"], "1")
                self.assertEqual(factory.from_pretrained.call_args.args, (str(root),))
                self.assertTrue(factory.from_pretrained.call_args.kwargs["local_files_only"])
                self.assertEqual(model.generate_custom_voice.call_args.kwargs["speaker"], "sohee")
                self.assertEqual(result["human_action"], "listen")
                self.assertAlmostEqual(result["trimmed_leading_seconds"], .96, places=2)
                self.assertTrue(output.is_file())
                net.assert_not_called()

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "numpy unavailable")
    def test_trim_leading_silence_preserves_speech_and_rejects_invalid_audio(self):
        import numpy as np
        speech = np.sin(np.arange(2000) * .1).astype(np.float32) * .1
        trimmed, seconds = qwen.trim_leading_silence(np.concatenate([np.zeros(1000), speech]), 1000)
        self.assertAlmostEqual(seconds, .96, places=2)
        np.testing.assert_array_equal(trimmed[-2000:], speech)
        for invalid in [np.zeros(200), np.array([np.nan]), np.zeros((2, 20))]:
            with self.assertRaises(ValueError): qwen.trim_leading_silence(invalid, 1000)


if __name__ == "__main__":
    unittest.main()
