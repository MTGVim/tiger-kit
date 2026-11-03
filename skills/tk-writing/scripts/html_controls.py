"""Shared offline HTML controls and explicit replacement of owned delivery files."""
from pathlib import Path
import os
import re
import tempfile


def theme_default(page, value):
    if value is None:
        return page
    if value not in ('system', 'light', 'dark'):
        raise ValueError('invalid default theme')
    def replace(match):
        attrs = re.sub(r'\sdata-(?:default-)?theme\s*=\s*("[^"]*"|\x27[^\x27]*\x27|[^\s>]+)', '', match.group(1), flags=re.I)
        initial = '' if value == 'system' else f' data-theme="{value}"'
        return '<html' + attrs + f' data-default-theme="{value}"' + initial + '>'
    return re.sub(r'<html\b([^>]*)>', replace, page, count=1, flags=re.I)


def theme_assets():
    assets = Path(__file__).resolve().parent.parent / "assets"
    def section(name, start, end):
        text = (assets / name).read_text(encoding="utf-8")
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError(f"invalid shared theme boundaries: {name}")
        return text.split(start, 1)[1].split(end, 1)[0]
    css = section("html-theme.css", "/* theme-control:start */", "/* theme-control:end */")
    js = section("html-theme.js", "// theme-control:start", "// theme-control:end")
    return f"<style>{css}</style>\n<script>{js}</script>\n"


def write_html(path, text, replace=False):
    """Default exclusive creation; --replace only replaces a regular nonsymlink file."""
    path = Path(path).absolute()
    if path.resolve() != path or not path.parent.is_dir():
        raise ValueError("output must have a nonsymlink existing parent")
    if not replace or not path.exists():
        with path.open("x", encoding="utf-8") as stream:
            stream.write(text)
        return
    if not path.is_file() or path.stat().st_nlink != 1:
        raise ValueError("replacement requires a regular singly linked owned file")
    before = path.stat()
    fd, temporary = tempfile.mkstemp(prefix=".html-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
        current = path.lstat()
        if (before.st_dev, before.st_ino, before.st_mtime_ns, before.st_size) != (current.st_dev, current.st_ino, current.st_mtime_ns, current.st_size):
            raise ValueError("output changed during replacement; preserved")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
