"""Exercise standalone SVG authoring without treating static checks as playback."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tk-explain/scripts/build_animated_svg.py"
FIXTURES = ROOT / "evals/skills/tk-explain/fixtures/animated-svg"
spec = importlib.util.spec_from_file_location("build_animated_svg", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NS = {"svg": "http://www.w3.org/2000/svg"}


class AnimatedSvgTest(unittest.TestCase):
    def scene(self):
        return json.loads((FIXTURES / "queue.json").read_text())

    def test_queue_retry_and_fanout_have_static_meaning_and_one_clock(self):
        for path in sorted(FIXTURES.glob("*.json")):
            with self.subTest(path=path.name):
                scene = json.loads(path.read_text())
                svg, schedule = module.build(scene)
                self.assertEqual(path.with_suffix(".svg").read_text(), svg)
                root = ET.fromstring(svg)
                self.assertEqual(root.get("role"), "img")
                self.assertEqual(len(root.findall("svg:style", NS)), 1)
                self.assertIn("prefers-reduced-motion:reduce", svg)
                self.assertIn(".packet{display:none;animation:none}", svg)
                self.assertNotIn("<script", svg)
                self.assertNotIn("<animate", svg)
                self.assertNotIn("url(", svg)
                self.assertNotIn("href=", svg)
                texts = [element.text or "" for element in root.findall("svg:text", NS)]
                self.assertTrue(any(scene["title"] == text for text in texts))
                for event in scene["events"]:
                    self.assertTrue(any(event["label"] in text for text in texts))
                    self.assertIn("@keyframes event-" + event["id"], svg)
                    self.assertIn("animation-name:event-" + event["id"], svg)
                    self.assertLess(schedule[event["id"]]["end"], scene["loop"] * 0.9)
                if path.stem == "queue":
                    self.assertAlmostEqual(schedule["started"]["start"], schedule["sent"]["end"] + 1)
                if path.stem == "retry":
                    self.assertEqual(schedule["first"]["edge"], schedule["retry"]["edge"])
                    self.assertAlmostEqual(schedule["retry"]["start"] - schedule["first"]["end"], 2)
                if path.stem == "fanout":
                    self.assertEqual(schedule["a"]["start"], schedule["b"]["start"])

    def test_rejects_incoherent_timing_graph_overlaps_and_unreadable_labels(self):
        mutations = [
            lambda d: d.update(loop=float("nan")),
            lambda d: d["events"][0].update(travel=-1),
            lambda d: d["events"][0].update(at=7.1),
            lambda d: d["events"][1].update(after="started"),
            lambda d: d["events"][1].update(at=1),
            lambda d: d["events"][1].update(id="sent"),
            lambda d: d["events"][0].update(edge="missing"),
            lambda d: d["nodes"][1].update(x=40),
            lambda d: d["nodes"][0].update(label="길어서 상자 안에 들어가지 않는 제목"),
            lambda d: d["edges"][0].update(points=[[220,192],[460,202]]),
            lambda d: d["edges"][0].update(points=[[225,192],[460,192]]),
            lambda d: d["edges"][0].update(points=[[220,192],[220,192],[460,192]]),
            lambda d: d.update(events=d["events"]*3),
        ]
        for mutate in mutations:
            scene = self.scene(); mutate(scene)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                module.build(scene)

    def test_user_text_is_data_and_ids_cannot_inject_css_or_markup(self):
        scene = self.scene()
        scene["description"] = '<script src="https://invalid.example/x"></script>'
        svg, _ = module.build(scene)
        root = ET.fromstring(svg)
        self.assertEqual(root.find("svg:desc", NS).text, scene["description"])
        self.assertEqual(root.findall(".//svg:script", NS), [])
        scene["events"][0]["id"] = "x};evil"
        with self.assertRaises(ValueError):
            module.build(scene)

    def test_cli_roundtrip_refuses_overwrite_and_detects_missing_keyframes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "queue.svg"
            command = [sys.executable, str(SCRIPT), "--spec", str(FIXTURES / "queue.json"), "--output", str(output)]
            result = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["runtime_verified"])
            original = output.read_bytes()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(subprocess.run([*command, "--check"], capture_output=True).returncode, 0)
            output.write_text(output.read_text().replace("@keyframes event-sent", "@keyframes absent"))
            self.assertNotEqual(subprocess.run([*command, "--check"], capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
