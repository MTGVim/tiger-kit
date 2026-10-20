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

    def test_engine_selection_is_native_apple_specific_without_silent_fallback(self):
        with patch.object(qwen.platform, "system", return_value="Darwin"), patch.object(qwen.platform, "machine", return_value="arm64"):
            self.assertEqual(qwen.selected_engine("auto"), "mlx")
            self.assertEqual(qwen.selected_engine("pytorch"), "pytorch")
        with patch.object(qwen.platform, "system", return_value="Linux"), patch.object(qwen.platform, "machine", return_value="x86_64"):
            self.assertEqual(qwen.selected_engine("auto"), "pytorch")
            with self.assertRaises(ValueError): qwen.selected_engine("mlx")

    def test_sentence_boundaries_preserve_decimal_numbers(self):
        self.assertEqual(qwen.sentences("값은 3.14입니다. 다음입니다!\n마지막입니다."),
                         ["값은 3.14입니다.", "다음입니다!", "마지막입니다."])

    def test_cache_redirect_and_inventory_report_preserve_unowned_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory); (home / ".cache").mkdir()
            with patch.object(qwen.Path, "home", return_value=home), patch.dict(qwen.os.environ,
                    {"HF_HUB_CACHE": "/unowned/hub", "TRANSFORMERS_CACHE": "/unowned/transformers"}, clear=True):
                before, limits = qwen.cache_inventory()
                model = home / ".cache/tigerkit/tts/mlx/snapshots/revision"
                model.mkdir(parents=True)
                owned = qwen.configure_runtime(model)
                self.assertEqual(qwen.os.environ["HF_HUB_OFFLINE"], "1")
                self.assertTrue(Path(qwen.os.environ["HF_HOME"]).is_relative_to(owned))
                for key in ["HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE", "TRANSFORMERS_CACHE"]:
                    self.assertEqual(Path(qwen.os.environ[key]), owned / "huggingface/hub")
                extra = home / ".cache/unattributed"; extra.mkdir()
                report = qwen.cache_report(before, limits, owned)
                self.assertEqual(report["new_cache_entries"], [str(extra)])
                self.assertTrue(extra.exists())

    def test_peak_footprint_is_independent_of_rss_and_missing_measurement_is_explicit(self):
        import ctypes
        from unittest.mock import Mock
        def measured(pid, flavor, usage):
            self.assertEqual(flavor, 4)
            usage._obj.counters[28] = 9_100_000_000
            return 0
        library = Mock(); library.proc_pid_rusage.side_effect = measured
        with patch.object(qwen.platform, "system", return_value="Darwin"), \
                patch.object(qwen.resource, "getrusage", return_value=types.SimpleNamespace(ru_maxrss=2_000_000)), \
                patch.object(ctypes, "CDLL", return_value=library):
            result = qwen.memory_metrics()
            self.assertEqual(result["peak_rss_bytes"], 2_000_000)
            self.assertEqual(result["peak_footprint_bytes"], 9_100_000_000)
            library.proc_pid_rusage.side_effect = None; library.proc_pid_rusage.return_value = -1
            result = qwen.memory_metrics()
            self.assertIsNone(result["peak_footprint_bytes"])
            self.assertIn("RSS is not a substitute", result["memory_limitation"])

    def test_mlx_snapshot_and_package_pins(self):
        data = qwen.mlx_adapter().manifest()
        self.assertIn("8bit", data["repository"])
        self.assertEqual(data["package"]["version"], "0.6.1")
        self.assertEqual(data["mlx_version"], "0.32.4")
        self.assertEqual(len(data["revision"]), 40)
        self.assertTrue(all(len(value) == 64 for value in data["files"].values()))

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
            root = Path(directory); text = root / "script.txt"; text.write_text("Korean script. Second sentence.")
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
                self.assertEqual(model.generate_custom_voice.call_count, 2)
                self.assertEqual(result["sentence_count"], 2)
                self.assertEqual(result["human_action"], "listen")
                self.assertAlmostEqual(result["trimmed_leading_seconds"], 1.92, places=2)
                self.assertTrue(output.is_file())
                net.assert_not_called()

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "numpy unavailable")
    def test_mlx_uses_gpu_zero_cache_offline_paths_and_one_sentence_per_request(self):
        import numpy as np
        from unittest.mock import Mock
        backend = qwen.mlx_adapter()
        sound = np.concatenate([np.zeros(1000), np.sin(np.arange(2000) * .1) * .1])
        mx = Mock(); mx.metal.is_available.return_value = True; mx.get_peak_memory.return_value = 7_000_000_000
        mx.gpu = "gpu"
        model = Mock()
        model.generate_custom_voice.side_effect = lambda **kw: iter([types.SimpleNamespace(audio=sound, sample_rate=1000)])
        def load(path):
            mx.set_cache_limit.assert_called_once_with(0)
            mx.set_default_device.assert_called_once_with("gpu")
            self.assertEqual(qwen.os.environ["HF_HUB_OFFLINE"], "1")
            self.assertIsInstance(path, Path)
            return model
        loader = Mock(side_effect=load)
        sf = Mock(); sf.write.side_effect = lambda path, *a, **kw: path.write_bytes(b"decoded fixture")
        sf.read.return_value = (sound, 1000)
        modules = {"mlx": types.SimpleNamespace(core=mx), "mlx.core": mx,
                   "mlx_audio": types.SimpleNamespace(), "mlx_audio.tts": types.SimpleNamespace(),
                   "mlx_audio.tts.utils": types.SimpleNamespace(load_model=loader), "soundfile": sf}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); text = root / "script.txt"; text.write_text("첫 문장입니다. 다음 문장입니다.")
            output = root / "voice.wav"
            with patch.object(qwen, "verify", return_value=backend.manifest()), \
                    patch.object(qwen.platform, "system", return_value="Darwin"), patch.object(qwen.platform, "machine", return_value="arm64"), \
                    patch.object(backend.importlib.metadata, "version", side_effect=lambda name: "0.6.1" if name == "mlx-audio" else "0.32.4"), \
                    patch.object(qwen, "memory_metrics", return_value={"peak_footprint_bytes": 9_100_000_000}), \
                    patch.dict("sys.modules", modules), patch.dict(qwen.os.environ, {}, clear=True), \
                    patch.object(qwen.urllib.request, "urlopen") as net:
                result = backend.synthesize(root, text, output, "serena", qwen)
                self.assertEqual([c.kwargs["text"] for c in model.generate_custom_voice.call_args_list],
                                 ["첫 문장입니다.", "다음 문장입니다."])
                self.assertEqual(result["cache_limit"], 0)
                self.assertEqual(result["peak_footprint_bytes"], 9_100_000_000)
                self.assertEqual(result["peak_mlx_active_bytes"], 7_000_000_000)
                self.assertEqual(result["sentence_count"], 2)
                self.assertEqual(result["device"], "metal")
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
