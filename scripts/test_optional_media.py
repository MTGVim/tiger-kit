from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib
import wave
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-video/scripts/build_movie.py"
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

    def test_diagnostic_hides_whole_space_containing_paths_and_credentials(self):
        error = subprocess.CalledProcessError(1, ["ffprobe"], stderr=(
            "/run/Private Project Name/movie.mp4: Invalid data found\n"
            "Authorization: Bearer EXAMPLE_TEST_VALUE\n"
            "password=words with spaces\n"
            "No such filter: 'subtitles'\n").encode())
        detail = movie.diagnostic(error)
        for private in ["Project Name", "EXAMPLE_TEST_VALUE", "words with spaces", "/run/"]:
            self.assertNotIn(private, detail)
        self.assertIn("No such filter", detail)
        self.assertLess(len(detail), 650)

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

    def test_frame_rate_selection_keeps_format_defaults_and_validates_overrides(self):
        frames = [(None, stamp) for stamp in [0, 50, 100, 150, 5000]]
        self.assertEqual(movie.frame_rate({}, frames, ".mp4", None), (20, "timestamps"))
        self.assertEqual(movie.frame_rate({"source_fps": 60}, frames, ".mp4", None), (30, "source_fps"))
        self.assertEqual(movie.frame_rate({"source_fps": 24}, frames, ".mp4", 12), (12, "override"))
        self.assertEqual(movie.frame_rate({"source_fps": 24}, frames, ".gif", None), (10, "default"))
        self.assertEqual(movie.frame_rate({"mode": "explainer"}, frames, ".mp4", None), (10, "default"))
        self.assertEqual(movie.frame_rate({}, frames[:2], ".mp4", None), (10, "fallback"))
        for value in [0, -1, True, float("nan"), float("inf"), 31]:
            with self.assertRaises(ValueError): movie.frame_rate({}, frames, ".mp4", value)
        for value in [0, -1, True, float("nan")]:
            with self.assertRaises(ValueError): movie.frame_rate({"source_fps": value}, frames, ".mp4", None)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_capture_rate_preserves_motion_frames_and_caps_dense_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); frames = []
            for i in range(72):
                path = root / f"motion-{i}.png"; png(path, (i * 3, 120, 220 - i * 2))
                frames.append({"path": str(path), "timestamp_ms": i * 1000 / 18})
            manifest = root / "frames.json"
            data = {"mode": "evidence", "frames": frames, "end_ms": 4000}
            manifest.write_text(json.dumps(data))
            native = movie.build(manifest, root / "native.mp4")
            sampled = movie.build(manifest, root / "ten.mp4", fps=10)
            fractional = movie.build(manifest, root / "fractional.mp4", fps=17.5)
            gif = movie.build(manifest, root / "animation.gif")
            custom_gif = movie.build(manifest, root / "custom.gif", fps=5)
            self.assertAlmostEqual(native["fps"], 18)
            self.assertEqual(native["fps_source"], "timestamps")
            self.assertAlmostEqual(sampled["fps"], 10)
            self.assertAlmostEqual(fractional["fps"], 17.5)
            self.assertAlmostEqual(fractional["encoded_duration_ms"], 4000, delta=1)
            self.assertAlmostEqual(gif["fps"], 10)
            self.assertAlmostEqual(custom_gif["fps"], 5)
            for name, count in [("native.mp4", 72), ("ten.mp4", 40), ("fractional.mp4", 70)]:
                stream = next(s for s in movie.probe(root / name)["streams"] if s["codec_type"] == "video")
                self.assertEqual(int(stream["nb_frames"]), count)
            self.assertEqual(native["duration_ms"], 4000)
            self.assertAlmostEqual(native["encoded_duration_ms"], 4000, delta=1)
            self.assertLess((root / "animation.gif").stat().st_size, 5 * 1024 * 1024)
            # Real timestamps above 25fps must survive the image demuxer's time base.
            for row in data["frames"]: row["timestamp_ms"] /= 2
            data["end_ms"] = 2000; data["source_fps"] = 36
            manifest.write_text(json.dumps(data))
            dense = movie.build(manifest, root / "capped.mp4")
            self.assertAlmostEqual(dense["fps"], 30)
            self.assertEqual(int(next(s for s in movie.probe(root / "capped.mp4")["streams"] if s["codec_type"] == "video")["nb_frames"]), 60)
            self.assertAlmostEqual(dense["encoded_duration_ms"], 2000, delta=1)
            decoded = subprocess.run([dense["ffmpeg_path"], "-v", "error", "-i", dense["path"],
                "-map", "0:v:0", "-f", "framemd5", "-"], capture_output=True, text=True, check=True).stdout
            hashes = [line.split(",")[-1].strip() for line in decoded.splitlines() if not line.startswith("#")]
            self.assertEqual(len(set(hashes)), 60)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_missing_subtitles_filter_retains_soft_captions_and_names_prerequisite(self):
        real_run = subprocess.run
        def without_subtitles(command, *args, **kwargs):
            if Path(command[0]).name == "ffmpeg" and "-filters" in command:
                return subprocess.CompletedProcess(command, 0, "Filters:\n ... fps V->V\n", "")
            return real_run(command, *args, **kwargs)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = self.fixture(root)
            with patch.object(movie.subprocess, "run", side_effect=without_subtitles):
                result = movie.build(manifest, root / "fallback.mp4")
                gif_result = movie.build(manifest, root / "fallback.gif")
            self.assertEqual(result["media_status"], "blocked")
            self.assertEqual(result["prerequisite"], "ffmpeg-subtitles-filter")
            self.assertEqual(result["subtitles"], "soft")
            self.assertIn("Observed result", (root / "fallback.srt").read_text())
            self.assertTrue(any(s["codec_name"] == "mov_text" for s in movie.probe(root / "fallback.mp4")["streams"]))
            self.assertEqual(gif_result["media_status"], "blocked")
            self.assertEqual(gif_result["subtitles"], "sidecar")
            self.assertTrue((root / "fallback.gif").is_file())

    def test_keg_discovery_and_explicit_override(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "bin").mkdir()
            keg = root / "bin/ffmpeg"; keg.touch(); keg.chmod(0o755)
            probe = root / "bin/ffprobe"; probe.touch(); probe.chmod(0o755)
            def which(name):
                return {"ffmpeg": "/path/ffmpeg", "ffprobe": "/path/ffprobe", "brew": "/path/brew", "chosen": "/chosen/ffmpeg"}.get(name)
            with patch.dict(movie.os.environ, {}, clear=True), patch.object(movie.shutil, "which", side_effect=which), \
                    patch.object(movie, "subtitle_filter", side_effect=lambda path: path == str(keg)), \
                    patch.object(movie.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, str(root), "")) as run:
                self.assertEqual(movie.media_tools(None, True), (str(keg), str(probe), True))
                run.assert_called_once()
                run.reset_mock()
                self.assertEqual(movie.media_tools("chosen", True), ("/chosen/ffmpeg", "/path/ffprobe", False))
                run.assert_not_called()
                with self.assertRaises(ValueError): movie.media_tools("missing", True)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_observed_scenes_preserve_offsets_and_reject_cross_scene_speech(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = self.fixture(root); audio = root / "speech.wav"
            with wave.open(str(audio), "wb") as wav:
                wav.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
                wav.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(i * 2 * math.pi * 440 / 22050))) for i in range(4410)))
            data = json.loads(manifest.read_text()); data["narration_requested"] = True
            data["scenes"] = [{"start_ms": 200, "audio_path": str(audio)}, {"start_ms": 700, "audio_path": str(audio)}]
            manifest.write_text(json.dumps(data))
            result = movie.build(manifest, root / "observed.mp4")
            self.assertEqual(result["media_status"], "ready")
            self.assertEqual(result["timing"], "observed")
            self.assertEqual(result["duration_ms"], 1000)
            raw = subprocess.run([result["ffmpeg_path"], "-v", "error", "-i", result["path"], "-map", "0:a:0", "-ac", "1", "-ar", "22050", "-f", "s16le", "-"], capture_output=True, check=True).stdout
            samples = struct.unpack("<" + "h" * (len(raw)//2), raw)
            def rms(start, stop):
                interval = samples[round(start*22050):round(stop*22050)]
                return math.sqrt(sum(v*v for v in interval)/len(interval))
            for start, stop in [(.02,.15),(.47,.63),(.94,.98)]: self.assertLess(rms(start,stop), 100)
            for start, stop in [(.23,.36),(.74,.86)]: self.assertGreater(rms(start,stop), 1000)
            if result["subtitles"] == "hard":
                stream = next(s for s in movie.probe(root / "observed.mp4")["streams"] if s["codec_type"] == "video")
                self.assertEqual(stream["width"], 64)
                self.assertGreater(stream["height"], 64)
            data["scenes"][1]["start_ms"] = 300
            manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.build(manifest, root / "overlap.mp4")
            data["scenes"][1]["start_ms"] = 900
            manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.build(manifest, root / "overrun.mp4")
            data["scenes"][1]["start_ms"] = 700
            manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.build(manifest, root / "mixed.mp4", audio)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_explainer_stills_use_presentation_holds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = self.fixture(root)
            data = json.loads(manifest.read_text())
            data["mode"] = "explainer"; data["captions"] = []
            data.pop("end_ms")
            for row, hold in zip(data["frames"], [500, 700]):
                row.pop("timestamp_ms"); row["hold_ms"] = hold
            manifest.write_text(json.dumps(data))
            result = movie.build(manifest, root / "explainer.mp4")
            self.assertEqual(result["timing"], "presentation")
            self.assertEqual(result["duration_ms"], 1200)
            self.assertAlmostEqual(float(movie.probe(root / "explainer.mp4")["format"]["duration"]), 1.2, delta=.15)
            data["frames"][0].pop("hold_ms"); data["frames"][1].pop("hold_ms")
            manifest.write_text(json.dumps(data))
            self.assertEqual(movie.load_manifest(manifest)[1], 6000)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_finished_media_distinguishes_static_explanation_and_silent_narration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = self.fixture(root)
            (root / "last.png").write_bytes((root / "first.png").read_bytes())
            result = movie.build(manifest, root / "static.mp4")
            self.assertTrue(any("repeated" in warning for warning in result["warnings"]))
            self.assertEqual(result["media_validation"]["status"], "pass")
            self.assertTrue(Path(result["contact_sheet"]).is_file())
            data = json.loads(manifest.read_text()); data["mode"] = "explainer"
            for row in data["frames"]: row.pop("timestamp_ms"); row["hold_ms"] = 500
            manifest.write_text(json.dumps(data))
            explained = movie.build(manifest, root / "stills.mp4")
            self.assertFalse(any("repeated" in warning for warning in explained["warnings"]))
            audio = root / "silent.wav"
            with wave.open(str(audio), "wb") as wav:
                wav.setparams((1, 2, 22050, 0, "NONE", "not compressed")); wav.writeframes(b"\0" * 22050)
            data["narration_requested"] = True; manifest.write_text(json.dumps(data))
            narrated = movie.build(manifest, root / "narrated.mp4", audio)
            self.assertEqual(narrated["media_validation"]["status"], "fail")
            self.assertIn("narration-silent", narrated["media_validation"]["errors"])
            self.assertTrue((root / "narrated.mp4").is_file())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
    def test_scene_audio_sets_measured_holds_and_preserves_scene_offsets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest = self.fixture(root); audio = root / "speech.wav"
            with wave.open(str(audio), "wb") as wav:
                wav.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
                wav.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(i * 2 * math.pi * 440 / 22050))) for i in range(70560)))
            data = json.loads(manifest.read_text()); data["mode"] = "explainer"; data["narration_requested"] = True
            data.pop("captions"); data.pop("end_ms")
            for row in data["frames"]: row.pop("timestamp_ms"); row["caption"] = "Scene description"
            data["frames"][0]["audio_path"] = str(audio)
            manifest.write_text(json.dumps(data))
            result = movie.build(manifest, root / "scenes.mp4")
            self.assertEqual(result["duration_ms"], 6450)
            self.assertEqual(result["media_validation"]["status"], "pass")
            self.assertTrue(result["audio"])
            data["captions"] = [{"start_ms": 0, "end_ms": 500, "text": "Too short"}]
            manifest.write_text(json.dumps(data))
            truncated = movie.build(manifest, root / "truncated-captions.mp4")
            self.assertIn("narration-subtitles-short", truncated["media_validation"]["errors"])
            data.pop("captions")
            data["frames"][0]["hold_ms"] = 100
            manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError): movie.build(manifest, root / "too-short.mp4")

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
