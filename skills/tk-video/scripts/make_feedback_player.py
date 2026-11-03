#!/usr/bin/env python3
"""Write a video feedback player HTML next to an MP4, from its SRT captions.

The HTML references the video by a relative path and never embeds it, so the page stays small.

Usage:
  python3 make_feedback_player.py --video <out.mp4> --captions <out.srt> [--output <out.html>] [--title <text>]
  python3 make_feedback_player.py --selftest

Exit codes: 0 written / selftest passed, 2 bad input (missing file, existing output, unparsable SRT, video not beside output).
Standard library only.
"""
import argparse
import importlib.util
from pathlib import Path
import hashlib
import json
import os
import re
import sys
import tempfile
from urllib.parse import quote

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback-player.template.html")
TOKEN = "__FEEDBACK_PLAYER_DATA__"
MAX_HTML_BYTES = 512 * 1024  # a transcript-only page; anything larger means media leaked in

_TS = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{3})")


def _ms(stamp):
    m = _TS.fullmatch(stamp.strip())
    if not m:
        raise ValueError(f"bad SRT timestamp: {stamp!r}")
    h, mi, s, ms = (int(x) for x in m.groups())
    if mi >= 60 or s >= 60:
        raise ValueError("SRT minutes and seconds must be below 60")
    return ((h * 60 + mi) * 60 + s) * 1000 + ms


def parse_srt(text):
    """Return [{start_ms, end_ms, text}] in file order. Multi-line cue text is joined with a space."""
    cues = []
    blocks = re.split(r"\r?\n\s*\r?\n", text.lstrip("\ufeff").strip())
    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        if "-->" not in lines[0]:  # first line is the cue number
            lines = lines[1:]
        if not lines or "-->" not in lines[0]:
            raise ValueError(f"SRT block without timing line: {block[:40]!r}")
        start, end = lines[0].split("-->", 1)
        if not end.split():
            raise ValueError("SRT cue has no end timestamp")
        start_ms, end_ms = _ms(start), _ms(end.split()[0])
        if end_ms < start_ms:
            raise ValueError(f"SRT cue ends before it starts: {lines[0]!r}")
        cues.append({"start_ms": start_ms, "end_ms": end_ms, "text": " ".join(s.strip() for s in lines[1:])})
    if not cues:
        raise ValueError("SRT has no cues")
    return cues


def load_controls(root):
    root = Path(root).absolute()
    if root.resolve() != root or not re.search(r'^name: [\"\']?tk-writing[\"\']?$', (root / 'SKILL.md').read_text(), re.M):
        raise ValueError('writing-root must identify the installed nonsymlink tk-writing owner')
    spec = importlib.util.spec_from_file_location('tigerkit_html_controls', root / 'scripts/html_controls.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    editor = (root / 'scripts/feedback-editor.js').read_text(encoding='utf-8')
    return module, module.theme_assets() + '<script>' + editor + '</script>'


def render(title, video_rel, cues, video_digest='', controls='', poster_rel=None):
    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()
    if html.count(TOKEN) != 1 or html.count('__SHARED_HTML_CONTROLS__') != 1:
        raise ValueError("template must contain the data token exactly once")
    key_src = video_rel + "\n" + video_digest + "\n" + json.dumps(cues, ensure_ascii=False)
    data = {
        "title": title,
        "video": video_rel,
        "video_url": quote(video_rel, safe="/"),
        "poster_url": quote(poster_rel, safe="/") if poster_rel else None,
        "storage_key": video_rel + ":" + hashlib.sha256(key_src.encode("utf-8")).hexdigest()[:12],
        "cues": cues,
    }
    # "<" escaped so cue text such as "</script>" cannot close the data block
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return html.replace('__SHARED_HTML_CONTROLS__', controls).replace(TOKEN, payload)


def write_new(path, text):
    """Create path exclusively; never overwrite an existing file."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)


def safe_input(path):
    path = os.path.abspath(path)
    if os.path.realpath(path) != path or not os.path.isfile(path) or os.path.getsize(path) == 0:
        raise ValueError("input must be a nonempty regular nonsymlink file")
    return path


def safe_output(path):
    path = os.path.abspath(path)
    if os.path.realpath(path) != path or not os.path.isdir(os.path.dirname(path)):
        raise ValueError("output must have an existing nonsymlink parent")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--video")
    ap.add_argument("--captions")
    ap.add_argument("--poster", help="existing preview JPEG/PNG beside or below the player; no playback offset")
    ap.add_argument("--output", help="default: <video stem>.html beside the video")
    ap.add_argument("--title", help="default: video file stem")
    ap.add_argument("--writing-root", help="verified installed tk-writing owner path")
    ap.add_argument("--theme", choices=['system', 'light', 'dark'], help="resolved generation default")
    ap.add_argument("--replace", action="store_true", help="replace an owned existing player delivery file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.video or not a.captions or not a.writing_root:
        ap.error("--video, --captions and --writing-root are required")
    try:
        video = safe_input(a.video)
        captions = safe_input(a.captions)
        stem = os.path.splitext(os.path.basename(video))[0]
        out = safe_output(a.output or os.path.join(os.path.dirname(video), stem + ".html"))
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2
    if os.path.exists(out) and not a.replace:
        print(f"output exists; use --output to choose another name or --replace for an owned player: {out}", file=sys.stderr)
        return 2
    if out in (video, captions):
        print("player output cannot replace its video or captions", file=sys.stderr)
        return 2
    video_rel = os.path.relpath(video, os.path.dirname(out))
    if video_rel.split(os.sep)[0] == "..":
        print("put the HTML in the video's folder or above it so the relative link survives copying", file=sys.stderr)
        return 2
    try:
        poster_rel = None
        poster_path = a.poster or os.path.splitext(video)[0] + '.poster.jpg'
        if a.poster or os.path.isfile(poster_path):
            poster = safe_input(poster_path)
            if os.path.splitext(poster)[1].lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
                raise ValueError('poster must be a supported image')
            poster_rel = os.path.relpath(poster, os.path.dirname(out)).replace(os.sep, '/')
            if poster_rel.split('/')[0] == '..':
                raise ValueError('poster must stay beside or below the player')
        with open(captions, encoding="utf-8") as f:
            cues = parse_srt(f.read())
        digest = hashlib.sha256()
        with open(video, 'rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''): digest.update(block)
        shared, controls = load_controls(a.writing_root)
        html = render(a.title or stem, video_rel.replace(os.sep, "/"), cues, digest.hexdigest()[:12], controls, poster_rel)
        html = shared.theme_default(html, a.theme)
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2
    if len(html.encode("utf-8")) > MAX_HTML_BYTES:
        print("HTML is unexpectedly large; refusing to write", file=sys.stderr)
        return 2
    try:
        shared.write_html(out, html, a.replace)
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2
    print(json.dumps({"path": out, "video": video_rel, "cues": len(cues), "bytes": len(html.encode("utf-8"))}, ensure_ascii=False))
    return 0


def selftest():
    srt = "\ufeff1\n00:00:00,000 --> 00:00:02,500\n첫 줄\n둘째 줄\n\n2\n00:00:03,000 --> 00:01:02,010\n</script> 포함\n"
    cues = parse_srt(srt)
    assert cues == [
        {"start_ms": 0, "end_ms": 2500, "text": "첫 줄 둘째 줄"},
        {"start_ms": 3000, "end_ms": 62010, "text": "</script> 포함"},
    ], cues
    html = render("시험", "a.mp4", cues)
    assert TOKEN not in html and "</script> 포함" not in html and "\\u003c/script> 포함" in html
    data = json.loads(re.search(r'<script id="fp-data" type="application/json">(.*?)</script>', html, re.S).group(1))
    assert data["cues"][1]["text"] == "</script> 포함" and data["video"] == "a.mp4"
    for bad in ("1\n00:00:01,000 --> 00:00:00,500\nx\n", "", "1\nno timing\n"):
        try:
            parse_srt(bad)
            raise AssertionError(f"accepted bad SRT: {bad!r}")
        except ValueError:
            pass
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "x.html")
        write_new(p, "a")
        try:
            write_new(p, "b")
            raise AssertionError("overwrote an existing file")
        except FileExistsError:
            pass
    print("selftest ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
