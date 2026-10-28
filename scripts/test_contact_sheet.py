from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/tk-browser-verify/scripts/contact_sheet.py"
spec = importlib.util.spec_from_file_location("contact_sheet", SCRIPT)
sheet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sheet)
try:
    from PIL import Image
except ImportError:
    Image = None


@unittest.skipUnless(Image, "optional Pillow unavailable")
class ContactSheetTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text("/.tigerkit/\n")
        self.root = self.repo / ".tigerkit/evidence/tk-browser-verify/fixture"
        self.root.mkdir(parents=True)
        self.rows = []
        for n, phase in enumerate(("baseline", "after", "failed-1", "after", "after")):
            target = self.root / phase / f"capture-{n}.png"
            target.parent.mkdir(exist_ok=True)
            Image.new("RGB", (200 + 20 * n, 100), (20 * n, 80, 100)).save(target)
            self.rows.append({"path": target.relative_to(self.root).as_posix(),
                              "criterion_id": f"BV-{n + 1:03d}", "phase": phase,
                              "state_region": f"state-{n}", "viewport": f"{390 + n * 100}x900",
                              "safe_for_sheet": True})
        self.index()

    def index(self, rows=None):
        (self.root / "README.md").write_text("# Existing evidence\n\nStatus: Fail\n\n```contact-sheet-captures\n" +
            json.dumps(self.rows if rows is None else rows) + "\n```\n")

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_paginates_links_and_labels_without_touching_evidence_or_verdict(self):
        before = self.snapshot()
        result = sheet.build(self.root)
        self.assertEqual(result["status"], "Created")
        self.assertEqual(len(result["sheets"]), 2)
        for name in result["sheets"]:
            with Image.open(self.root / name) as image:
                image.verify()
                self.assertEqual(image.width, 1168)
                self.assertLessEqual(image.height, 896)
        index = (self.root / "README.md").read_text()
        self.assertTrue(index.startswith(before["README.md"].decode()))
        self.assertIn("not acceptance evidence", index)
        self.assertIn("Tile 3: BV-003 / failed-1 / state-2 / 590x900", index)
        for row in self.rows:
            self.assertIn(f"[{row['path']}]({row['path']})", index)
            self.assertEqual((self.root / row["path"]).read_bytes(), before[row["path"]])
        # Inspect label inputs and cell order independently of link serialization.
        self.assertEqual(sheet.capture_rows(before["README.md"]), self.rows)
        with self.assertRaisesRegex(ValueError, "already exists"):
            sheet.build(self.root)

    def test_empty_single_and_explicit_single(self):
        for rows in ([], self.rows[:1]):
            self.index(rows)
            before = self.snapshot()
            self.assertEqual(sheet.build(self.root)["status"], "Skipped")
            self.assertEqual(self.snapshot(), before)
        self.assertEqual(sheet.build(self.root, single=True)["captures"], 1)

    def test_optional_dependency_missing_leaves_everything_unchanged(self):
        before = self.snapshot()
        with patch.dict(sys.modules, {"PIL": None}):
            self.assertEqual(sheet.build(self.root)["reason"], "Pillow unavailable")
        self.assertEqual(self.snapshot(), before)
        with patch.object(sheet.os, "supports_dir_fd", set()):
            self.assertEqual(sheet.build(self.root)["reason"], "safe directory handles unavailable")
        self.assertEqual(self.snapshot(), before)

    def test_corrupt_unreadable_sensitive_traversal_external_and_symlink_rejected(self):
        original = self.rows[0].copy()
        changes = [{"safe_for_sheet": False}, {"path": "../outside.png"},
                   {"path": "/tmp/outside.png"}, {"phase": "after"},
                   {"state_region": "private?secret=value"}]
        for change in changes:
            with self.subTest(change=change):
                self.rows[0] = {**original, **change}
                self.index()
                before = self.snapshot()
                with self.assertRaises((ValueError, OSError)):
                    sheet.build(self.root)
                self.assertEqual(self.snapshot(), before)
        self.rows[0] = original
        self.index()
        target = self.root / original["path"]
        data = target.read_bytes()
        target.write_bytes(b"not a png")
        with self.assertRaises(OSError):
            sheet.build(self.root)
        target.write_bytes(data)
        target.chmod(0)
        with self.assertRaises((ValueError, OSError)):
            sheet.build(self.root)
        target.chmod(0o600)
        target.unlink()
        target.symlink_to(self.root / self.rows[1]["path"])
        with self.assertRaises((ValueError, OSError)):
            sheet.build(self.root)
        target.unlink()
        target.write_bytes(data)
        directory = target.parent
        directory.rename(self.root / "saved-baseline")
        directory.symlink_to(self.root / "saved-baseline", target_is_directory=True)
        with self.assertRaises((ValueError, OSError)):
            sheet.build(self.root)

    def test_output_collision_and_mid_write_failure_preserve_index_and_originals(self):
        before = self.snapshot()
        (self.root / "contact-sheet-002.png").write_bytes(b"existing")
        with self.assertRaisesRegex(ValueError, "already exists"):
            sheet.build(self.root)
        self.assertEqual((self.root / "contact-sheet-002.png").read_bytes(), b"existing")
        (self.root / "contact-sheet-002.png").unlink()
        original_open = sheet.os.open
        def fail_second(path, flags, *args, **kwargs):
            if Path(path).name == "contact-sheet-002.png":
                raise OSError("synthetic storage failure")
            return original_open(path, flags, *args, **kwargs)
        with patch.object(sheet.os, "open", side_effect=fail_second) as mock_open, patch.object(sheet.os, "supports_dir_fd", {mock_open}), self.assertRaises(OSError):
            sheet.build(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_index_change_during_composition_is_preserved_and_outputs_rolled_back(self):
        original_draw = sheet.draw_sheet
        def concurrent_writer(*args):
            (self.root / "README.md").write_text("concurrent verifier update\n")
            return original_draw(*args)
        with patch.object(sheet, "draw_sheet", side_effect=concurrent_writer), self.assertRaisesRegex(ValueError, "index changed"):
            sheet.build(self.root)
        self.assertEqual((self.root / "README.md").read_text(), "concurrent verifier update\n")
        self.assertEqual(list(self.root.glob("contact-sheet-*.png")), [])

    def test_hardlinked_images_and_index_never_change_external_aliases(self):
        target = self.root / self.rows[0]["path"]
        external = self.repo / "external.png"
        sheet.os.link(target, external)
        before = external.read_bytes()
        with self.assertRaises(ValueError):
            sheet.build(self.root)
        self.assertEqual(external.read_bytes(), before)
        external.unlink()
        external_index = self.repo / "external-index.md"
        sheet.os.link(self.root / "README.md", external_index)
        before = external_index.read_bytes()
        with self.assertRaises(ValueError):
            sheet.build(self.root)
        self.assertEqual(external_index.read_bytes(), before)
        external_index.unlink()
        original_draw = sheet.draw_sheet
        def link_after_read(*args):
            if not external_index.exists():
                sheet.os.link(self.root / "README.md", external_index)
            return original_draw(*args)
        with patch.object(sheet, "draw_sheet", side_effect=link_after_read), self.assertRaisesRegex(ValueError, "hardlink"):
            sheet.build(self.root)
        self.assertEqual(external_index.read_bytes(), before)
        self.assertEqual(list(self.root.glob("contact-sheet-*.png")), [])

    def test_rejects_non_run_root_and_tracked_or_unignored_evidence(self):
        with self.assertRaises(ValueError):
            sheet.build(self.repo)
        (self.repo / ".gitignore").write_text("")
        with self.assertRaises(ValueError):
            sheet.build(self.root)
        (self.repo / ".gitignore").write_text("/.tigerkit/\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "-f", ".tigerkit/"], check=True)
        with self.assertRaises(ValueError):
            sheet.build(self.root)


if __name__ == "__main__":
    unittest.main()
