#!/usr/bin/env python3
"""Write one delivery HTML with N-item feedback and an optional video card.

The original page is never modified. An archify page keeps its finalize receipt bound to the original bytes;
keep that original and its receipt in the run evidence directory and pass an explicit delivery --output.

Usage:
  python3 add_feedback_studio.py --input <page.html> [--video <id>=<movie.mp4> ...] --output <delivery/stem.html>
  python3 add_feedback_studio.py --selftest

--video ID=MP4 (repeatable) puts a video where the first image of element ID is: an archify @image block id, or any
element id on other pages. The video is referenced by a relative path (never embedded), so the MP4 must sit in the
output's folder or below it. The image stays in the page as the poster, as the print/export picture (archify strips
".interactive" from exports) and as the fallback when the file is missing or JavaScript is off.

Exit codes: 0 written / selftest ok, 2 bad input. Standard library only.
"""
import argparse
import hashlib
from html_controls import theme_assets, theme_default, write_html
import json
import html as htmllib
import os
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback-studio.js")
MARK = "<!-- feedback-studio -->"
RATES = ("0.75", "1", "1.25", "1.5", "2")


def video_wrap(rel):
    """Video placed right before the target <img>; the image stays as poster, export and no-JS fallback."""
    src = htmllib.escape(quote(rel, safe="/"), quote=True)
    speed = "".join(f'<button type="button" data-rate="{r}">{r}×</button>' for r in RATES)
    # "interactive": archify hides it without JS and strips it from exports/print, so the image shows there
    return (f'<div class="fs-root fs-vwrap interactive" data-fs-video hidden><video controls preload="metadata" playsinline src="{src}"></video>'
            f'<div class="fs-speed" role="group" aria-label="재생 속도"><span class="fs-hint">배속</span>{speed}</div>'
            f'<p class="fs-video-missing" hidden>영상 파일({htmllib.escape(rel)})을 찾지 못해 이미지를 보여 줍니다. 이 HTML과 같은 폴더에 두면 재생됩니다.</p></div>')


class ImageTargets(HTMLParser):
    """Track actual element ancestry, retaining byte-for-byte source outside inserts."""
    VOID = frozenset("area base br col embed hr img input link meta param source track wbr".split())

    def __init__(self, page, targets):
        super().__init__(convert_charrefs=True)
        self.offsets = [0]
        self.offsets.extend(m.end() for m in re.finditer("\\n", page))
        self.stack = []
        self.targets = set(targets)
        self.seen = set()
        self.images = {}

    def handle_starttag(self, tag, attrs):
        ident = dict(attrs).get("id")
        if ident in self.targets:
            if ident in self.seen:
                raise ValueError(f"duplicate target id={ident!r}")
            self.seen.add(ident)
        if tag == "img":
            line, col = self.getpos()
            for _, ancestor in self.stack:
                if ancestor in self.targets:
                    self.images.setdefault(ancestor, self.offsets[line - 1] + col)
        if tag not in self.VOID:
            self.stack.append((tag, ident))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


class InlineAssets(HTMLParser):
    """Collect live inline assets, not prose, data scripts or template contents."""

    def __init__(self, page):
        super().__init__()
        self.inert = []
        self.active = None
        self.assets = {'script': [], 'style': []}
        self.feed(page)

    def handle_starttag(self, tag, attrs):
        if tag in ('template', 'noscript'):
            self.inert.append(tag)
        if tag not in self.assets or self.inert:
            return
        attrs = dict(attrs)
        kind = (attrs.get('type') or '').strip().lower()
        if tag == 'script':
            if 'src' in attrs or 'nomodule' in attrs or kind not in ('', 'module', 'text/javascript', 'application/javascript'):
                return
        elif kind not in ('', 'text/css') or (attrs.get('media') or '').strip().lower() not in ('', 'all'):
            return
        self.active = (tag, [])

    def handle_data(self, data):
        if self.active:
            self.active[1].append(data)

    def handle_endtag(self, tag):
        if self.active and self.active[0] == tag:
            self.assets[tag].append(''.join(self.active[1]))
            self.active = None
        if tag in self.inert:
            index = len(self.inert) - 1 - self.inert[::-1].index(tag)
            del self.inert[index:]


def image_assets(page):
    """Reuse the package-owned image reader, including non-reader delivery HTML.

    The builder already inlines these sections; don't add another copy in studio.
    No image URL or bytes are copied here: the viewer reads the live img on opening.
    """
    assets = Path(__file__).resolve().parents[1] / 'assets'
    parts = []
    existing = InlineAssets(page).assets
    for name, start, end, tag in (
        ('html-theme.css', '/* image-reader:start */', '/* image-reader:end */', 'style'),
        ('html-theme.js', '// image-reader:start', '// image-reader:end', 'script'),
    ):
        text = (assets / name).read_text(encoding='utf-8')
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError('invalid shared image reader boundaries: ' + name)
        section = start + text.split(start, 1)[1].split(end, 1)[0] + end
        if any(content.strip() in (section.strip(), text.strip()) for content in existing[tag]):
            continue
        parts.append(f'<{tag}>\n{section}\n</{tag}>\n')
    return ''.join(parts)


def inject(page, js, videos=()):
    """videos: [(target_id, relative_video_path)]. target_id is an archify @image block id, or any element id
    whose first <img> becomes the video's poster and fallback."""
    if MARK in page:
        raise ValueError("page already has the feedback studio")
    if "</script" in js.lower():
        raise ValueError("studio script must not contain a closing script tag")
    # Add only a scope flag to the delivery body; never modify the evidence original.
    page, bodies = re.subn(
        r'<body\b([^>]*)>',
        lambda match: match.group(0) if re.search(r'\bdata-ht-image-reader(?:\s|=|$)', match.group(1), re.I)
        else '<body data-ht-image-reader' + match.group(1) + '>',
        page, count=1, flags=re.I,
    )
    if not bodies:
        raise ValueError('page has no <body>')
    end = page.lower().rfind("</body>")
    if end < 0:
        raise ValueError("page has no </body>")
    page = page[:end] + MARK + image_assets(page) + "\n<script>\n" + js + "\n</script>\n" + page[end:]
    targets = [target for target, _ in videos]
    if len(set(targets)) != len(targets):
        raise ValueError("duplicate video target")
    parser = ImageTargets(page, targets)
    parser.feed(page)
    inserts = []
    for target, rel in videos:
        if target not in parser.images:
            raise ValueError(f"id={target!r} has no descendant image to replace")
        inserts.append((parser.images[target], video_wrap(rel)))
    if len({pos for pos, _ in inserts}) != len(inserts):
        raise ValueError("video targets refer to the same image")
    for pos, markup in sorted(inserts, reverse=True):
        page = page[:pos] + markup + page[pos:]
    return page


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
    ap.add_argument("--input")
    ap.add_argument("--video", action="append", default=[], metavar="ID=MP4",
                    help="replace the image in element ID with this video (repeatable)")
    ap.add_argument("--output", help="required delivery path: <stem>.html, separate from the evidence input")
    ap.add_argument("--theme", choices=['system', 'light', 'dark'], help="resolved generation default; saved reader preference takes priority")
    ap.add_argument("--owner-skill", help="verified workflow owner, for example tk-explain or tk-research")
    ap.add_argument("--source-path", help="known editable source file, never inferred from the delivered HTML")
    ap.add_argument("--replace", action="store_true", help="replace an explicitly owned existing studio delivery file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.output:
        ap.error("--output is required; preserve the original in evidence and choose a delivery <stem>.html")
    if not a.input or not os.path.isfile(a.input):
        print("--input must be an existing HTML file", file=sys.stderr)
        return 2
    try:
        source = safe_input(a.input)
        out = safe_output(a.output)
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2
    if os.path.exists(out) and not a.replace:
        print(f"output exists; use --output to choose another name or --replace for an owned delivery: {out}", file=sys.stderr)
        return 2
    if out == source:
        print("studio output cannot replace its source", file=sys.stderr)
        return 2
    videos = []
    for spec in a.video:
        target, sep, path = spec.partition("=")
        if not sep or not target or not os.path.isfile(path):
            print(f"--video needs ID=existing.mp4, got: {spec}", file=sys.stderr)
            return 2
        try:
            path = safe_input(path)
        except (ValueError, OSError) as e:
            print(str(e), file=sys.stderr)
            return 2
        rel = os.path.relpath(path, os.path.dirname(out)).replace(os.sep, "/")
        if rel.split("/")[0] == "..":
            print("put the HTML in the video's folder or above it so the relative link survives copying", file=sys.stderr)
            return 2
        videos.append((target, rel))
    with open(a.input, encoding="utf-8") as f:
        page = f.read()
    with open(SCRIPT, encoding="utf-8") as f:
        js = f.read()
    try:
        js = js.replace('__FS_PAGE_VERSION__', hashlib.sha256(page.encode('utf-8')).hexdigest()[:12])
        if a.owner_skill and not re.fullmatch(r'tk-[a-z0-9]+(?:-[a-z0-9]+)*', a.owner_skill):
            raise ValueError('owner-skill must be an exact tk-* skill name')
        context = {'owner': a.owner_skill, 'source': safe_input(a.source_path) if a.source_path else None}
        js = js.replace('__FS_CONTEXT__', json.dumps(context, ensure_ascii=False).replace('<', '\\u003c'))
        editor = open(os.path.join(os.path.dirname(SCRIPT), 'feedback-editor.js'), encoding='utf-8').read()
        result = inject(page, editor + '\n' + js, videos)
        result = result.replace(MARK, MARK + theme_assets(), 1)
        result = theme_default(result, a.theme)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    try:
        write_html(out, result, a.replace)
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2
    added = len(result.encode("utf-8")) - len(page.encode("utf-8"))
    print(json.dumps({"path": out, "videos": [f"{t}={r}" for t, r in videos], "bytes_added": added}, ensure_ascii=False))
    return 0


def selftest():
    js = open(SCRIPT, encoding="utf-8").read()
    generic = '<!doctype html><html><head><title>t</title></head><body><h1>제목</h1><section id="a"><h2>A</h2><img src="a.png" alt="a"></section><section id="b"><h2>B</h2><p>x</p></section></BODY></html>'
    out = inject(generic, js)
    assert out.count(MARK) == 1 and out.index(MARK) < out.lower().rindex("</body>") and out.endswith("</BODY></html>")
    out = inject(generic, js, [("a", 'v "1".mp4')])
    assert out.index("data-fs-video") < out.index('<img src="a.png"') and 'src="v%20%221%22.mp4"' in out
    try:
        inject(generic, js, [("b", "v.mp4")])  # section b has no image: must not borrow a later one
        raise AssertionError("accepted a target without an image")
    except ValueError:
        pass
    archify = ('<html><body><div class="board"><section id="p1" class="panel"><div class="block block-image" id="card" data-block-type="image">'
               '<figure class="image"><img src="data:image/png;base64,AA" alt="c"></figure></div></section></div></body></html>')
    out = inject(archify, js, [("card", "m.mp4")])
    assert out.index("fs-vwrap interactive") < out.index('<img src="data:') and out.count("data-fs-video hidden><video") == 1  # the script also mentions the attribute
    for bad in ([("nope", "m.mp4")],):
        try:
            inject(archify, js, bad)
            raise AssertionError("accepted unknown id")
        except ValueError:
            pass
    for bad, why in ((inject(generic, js), "already"), ("<html><body>no end", "no </body>")):
        try:
            inject(bad, js)
            raise AssertionError(f"accepted page with {why}")
        except ValueError:
            pass
    try:
        inject(generic, "x</script>y")
        raise AssertionError("accepted script with closing tag")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.html")
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
