#!/usr/bin/env python3
"""Build an opt-in navigation overview from the existing evidence README."""
from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import warnings
from contextlib import contextmanager

BLOCK = re.compile(r"^```contact-sheet-captures\n(.*?)\n```$", re.M | re.S)
MAX_CAPTURES = 120
PER_SHEET = 4
TILE_W, TILE_H, LABEL_H, GAP = 560, 320, 104, 16


@contextmanager
def directory_handle(root: Path):
    """Pin each directory without following a swapped symlink."""
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in root.absolute().parts[1:]:
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        yield fd
    finally:
        os.close(fd)


def regular_file(root: Path, relative: str, limit: int) -> bytes:
    """Reject symlinks in every component, and inspect only bounded regular files."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(p in {"..", "."} for p in parts):
        raise ValueError("unsafe evidence path")
    with directory_handle(root / Path(relative).parent) as parent_fd:
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                    or info.st_size > limit or not info.st_mode & 0o444):
                raise ValueError("unreadable or oversized evidence file")
            data = stream.read(limit + 1)
            if len(data) > limit:
                raise ValueError("evidence file grew beyond size bound")
            return data


def run_root(path: Path) -> Path:
    absolute = path.absolute()
    if absolute != absolute.resolve() or absolute.is_symlink():
        raise ValueError("run directory must not contain symlinks")
    repository = subprocess.run(["git", "-C", str(absolute), "rev-parse", "--show-toplevel"],
                                check=True, capture_output=True, text=True).stdout.strip()
    repo = Path(repository).resolve()
    relative = absolute.relative_to(repo).parts
    if (len(relative) != 4 or relative[:3] != (".tigerkit", "evidence", "tk-browser-verify")
            or not absolute.is_dir()):
        raise ValueError("expected a run-owned browser evidence directory")
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files", "--", ".tigerkit/"],
                             check=True, capture_output=True, text=True).stdout
    ignored = subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", "--", ".tigerkit/"],
                             capture_output=True).returncode == 0
    if tracked or not ignored:
        raise ValueError("evidence directory must be untracked and ignored")
    return absolute


def capture_rows(index: bytes) -> list[dict]:
    blocks = BLOCK.findall(index.decode("utf-8"))
    if len(blocks) != 1:
        raise ValueError("README requires one contact-sheet-captures JSON block")
    rows = json.loads(blocks[0])
    if not isinstance(rows, list) or len(rows) > MAX_CAPTURES:
        raise ValueError("capture list is invalid or exceeds 120 entries")
    paths = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "path", "criterion_id", "phase", "state_region", "viewport", "safe_for_sheet"
        }:
            raise ValueError("capture row requires exact provenance and safety fields")
        for key in ("path", "criterion_id", "phase", "state_region", "viewport"):
            value = row[key]
            if (not isinstance(value, str) or not value or len(value) > (160 if key == "path" else 64)
                    or not re.fullmatch(r"[A-Za-z0-9_./: @+(),=-]+", value)):
                raise ValueError("use concise publication-safe ASCII capture labels")
        parts = Path(row["path"]).parts
        if (len(parts) < 2 or parts[0] != row["phase"] or row["path"] in paths
                or not re.fullmatch(r"[A-Za-z0-9_./-]+", row["path"])
                or not re.fullmatch(r"baseline|after|failed-[A-Za-z0-9_-]+", row["phase"])
                or Path(row["path"]).suffix.lower() != ".png"):
            raise ValueError("capture path/phase is invalid or duplicated")
        if row["safe_for_sheet"] is not True:
            raise ValueError("sensitive or unreviewed capture cannot be composed")
        paths.add(row["path"])
    return rows


def draw_sheet(Image, ImageDraw, tiles):
    rows = (len(tiles) + 1) // 2
    sheet = Image.new("RGB", (2 * TILE_W + 3 * GAP, rows * (TILE_H + LABEL_H + GAP) + GAP), "#eef1f5")
    draw = ImageDraw.Draw(sheet)
    for i, (row, image) in enumerate(tiles):
        x, y = GAP + i % 2 * (TILE_W + GAP), GAP + i // 2 * (TILE_H + LABEL_H + GAP)
        label = f"{row['criterion_id']} | {row['phase']} | {row['viewport']}\n{row['state_region']}\n{row['path']}"
        # Keep every label visible; the full path also remains linked in README.
        lines = [line[start:start + 72] for line in label.splitlines() for start in range(0, len(line), 72)]
        draw.multiline_text((x, y), "\n".join(lines), fill="#18202b", spacing=3)
        thumb = image.copy()
        thumb.thumbnail((TILE_W, TILE_H))
        sheet.paste(thumb, (x + (TILE_W - thumb.width) // 2, y + LABEL_H))
    buffer = io.BytesIO()
    sheet.save(buffer, format="PNG")
    return buffer.getvalue()


def build(path: Path, *, single: bool = False) -> dict:
    if (not all(hasattr(os, name) for name in ("O_DIRECTORY", "O_NOFOLLOW"))
            or os.open not in os.supports_dir_fd):
        return {"status": "Skipped", "reason": "safe directory handles unavailable", "sheets": []}
    root = run_root(path)
    original_index = regular_file(root, "README.md", 512_000)
    rows = capture_rows(original_index)
    if not rows or len(rows) == 1 and not single:
        return {"status": "Skipped", "reason": "fewer than two captures", "sheets": []}
    # Optional dependency: never install anything or start a browser.
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return {"status": "Skipped", "reason": "Pillow unavailable", "sheets": []}
    tiles = []
    for row in rows:
        data = regular_file(root, row["path"], 20_000_000)
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as image:
                if image.format != "PNG" or image.width * image.height > 16_000_000:
                    raise ValueError("capture is not a bounded PNG")
                image.load()
                thumb = image.convert("RGB")
                thumb.thumbnail((TILE_W, TILE_H))
                tiles.append((row, thumb))
    outputs = [(f"contact-sheet-{n // PER_SHEET + 1:03d}.png",
                draw_sheet(Image, ImageDraw, tiles[n:n + PER_SHEET]))
               for n in range(0, len(tiles), PER_SHEET)]
    if any(os.path.lexists(root / name) for name, _ in outputs):
        raise ValueError("contact sheet output already exists")
    addition = "\n\n## Contact sheet navigation (not acceptance evidence)\n\n"
    for n, (name, _) in enumerate(outputs):
        addition += f"- [{name}]({name})\n"
        for tile, row in enumerate(rows[n * PER_SHEET:(n + 1) * PER_SHEET], 1):
            addition += (f"  - Tile {tile}: {row['criterion_id']} / {row['phase']} / "
                         f"{row['state_region']} / {row['viewport']}: [{row['path']}]({row['path']})\n")
    created = []
    with directory_handle(root) as root_fd:
        try:
            for name, data in outputs:
                fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=root_fd)
                created.append(name)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(data)
            # Append only if the canonical index has not changed since it was read.
            fd = os.open("README.md", os.O_RDWR | os.O_NOFOLLOW, dir_fd=root_fd)
            with os.fdopen(fd, "r+b") as stream:
                if os.fstat(stream.fileno()).st_nlink != 1:
                    raise ValueError("evidence index must not be a hardlink")
                if stream.read(len(original_index) + 1) != original_index:
                    raise ValueError("evidence index changed; retry after reconciling it")
                try:
                    stream.write(addition.encode("utf-8"))
                    stream.flush()
                except OSError:
                    stream.truncate(len(original_index))
                    raise
        except Exception:
            for name in created:
                os.unlink(name, dir_fd=root_fd)
            raise
    return {"status": "Created", "sheets": [name for name, _ in outputs], "captures": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--single", action="store_true", help="explicitly request a one-capture sheet")
    args = parser.parse_args()
    try:
        result = build(args.run_dir, single=args.single)
    except (OSError, ValueError, subprocess.SubprocessError, Warning) as exc:
        # Do not echo image contents, source labels or arbitrary external paths.
        result = {"status": "Skipped", "reason": type(exc).__name__, "sheets": []}
    print(json.dumps(result))
    return 0 if result["status"] == "Created" else 2


if __name__ == "__main__":
    raise SystemExit(main())
