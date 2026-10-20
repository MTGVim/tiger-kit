from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import zlib


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-browser-verify/scripts/build_movie.py"
spec = importlib.util.spec_from_file_location("build_movie", SOURCE)
movie = importlib.util.module_from_spec(spec)
spec.loader.exec_module(movie)


def png(path, color):
    def chunk(kind, value):
        return struct.pack(">I", len(value)) + kind + value + struct.pack(">I", zlib.crc32(kind + value))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 64, 64, 8, 2, 0, 0, 0)) +
                     chunk(b"IDAT", zlib.compress((b"\0" + bytes(color) * 64) * 64)) + chunk(b"IEND", b""))


class OptionalMediaTests(unittest.TestCase):
    def fixture(self, root):
        first, last = root / "first.png", root / "last.png"
        png(first, (40, 90, 120)); png(last, (90, 140, 40))
        manifest = root / "frames.json"
        manifest.write_text(json.dumps({"frames": [{"path": str(first), "timestamp_ms": 0},
            {"path": str(last), "timestamp_ms": 700}], "end_ms": 1000,
            "captions": [{"start_ms": 0, "end_ms": 1000, "text": "Observed result"}]}))
        return manifest

    def test_rejects_ambiguous_timing_and_outside_frames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = self.fixture(root)
            data = json.loads(path.read_text()); data["frames"][1]["timestamp_ms"] = 0
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.load_manifest(path)
            data["frames"][1]["timestamp_ms"] = 700; data["end_ms"] = float("nan")
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.load_manifest(path)
            outside = root.parent / "outside.png"; data["frames"][0]["path"] = str(outside)
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.load_manifest(path)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_removed_narration_and_missing_audio_preserve_captioned_movie(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = self.fixture(root)
            # Copy the standalone assembler into a package with no narration module/dependencies.
            shutil.copyfile(SOURCE, root / "build_movie.py")
            isolated_spec = importlib.util.spec_from_file_location("isolated_movie", root / "build_movie.py")
            isolated = importlib.util.module_from_spec(isolated_spec)
            isolated_spec.loader.exec_module(isolated)
            result = isolated.build(path, root / "flow.mp4", root / "missing.wav")
            self.assertFalse(result["audio"]); self.assertTrue(result["warnings"])
            info = movie.probe(root / "flow.mp4")
            self.assertAlmostEqual(float(info["format"]["duration"]), 1, delta=.15)
            self.assertEqual(next(s["codec_name"] for s in info["streams"] if s["codec_type"] == "video"), "h264")
            self.assertTrue((root / "first.png").is_file())
            self.assertFalse(list(root.glob("movie-*/")))
            gif_result = isolated.build(path, root / "flow.gif")
            self.assertEqual(gif_result["media_type"], "image/gif")
            self.assertFalse(gif_result["audio"])
            self.assertAlmostEqual(float(movie.probe(root / "flow.gif")["format"]["duration"]), 1, delta=.15)
            before = (root / "flow.mp4").read_bytes()
            with self.assertRaises(ValueError): movie.build(path, root / "flow.mp4")
            self.assertEqual((root / "flow.mp4").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
