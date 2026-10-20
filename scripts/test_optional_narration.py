from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-browser-verify/scripts/narration/ppaso.py"
spec = importlib.util.spec_from_file_location("optional_ppaso", SOURCE)
ppaso = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ppaso)


class OptionalNarrationTests(unittest.TestCase):
    def test_all_pinned_files_have_full_sha256(self):
        data = ppaso.manifest()
        self.assertEqual(len(data["revision"]), 40)
        self.assertIn("onnx/vocoder.onnx.data", data["files"])
        self.assertIn("runtime/data/g2p_mfa.py", data["files"])
        self.assertIn("README_ko.md", data["files"])
        self.assertTrue(all(len(x) == 64 for x in data["files"].values()))

    def test_offline_verification_rejects_tamper_without_network_or_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "file").write_bytes(b"expected")
            data = {"files": {"file": hashlib.sha256(b"expected").hexdigest()}}
            with patch.object(ppaso, "manifest", return_value=data), patch.object(ppaso.urllib.request, "urlopen") as net:
                self.assertEqual(ppaso.verify(root), data)
                (root / "acoustic.onnx").write_bytes(b"unpinned flat override")
                with self.assertRaises(ValueError): ppaso.verify(root)
                (root / "acoustic.onnx").unlink()
                (root / "runtime").mkdir()
                (root / "runtime/__init__.py").write_text("raise RuntimeError('unpinned')")
                with self.assertRaises(ValueError): ppaso.verify(root)
                (root / "runtime/__init__.py").unlink()
                (root / "file").write_bytes(b"tampered")
                with self.assertRaises(ValueError): ppaso.verify(root)
                net.assert_not_called()


if __name__ == "__main__":
    unittest.main()
