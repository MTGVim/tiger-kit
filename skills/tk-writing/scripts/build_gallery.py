#!/usr/bin/env python3
"""변형 비교 갤러리를 한 장의 오프라인 HTML로 만든다. 외부 요청 없음.

사용법: build_gallery.py manifest.json out.html
manifest: {"title": str, "lede": str, "items": [{"id", "name", "href", "thumb", "diff", "misfit", "baseline"}]}
href와 thumb은 out.html 기준 상대 경로다. baseline이 true인 항목은 기준 줄로 맨 위에 둔다.
"""
import argparse
import html
import os
import tempfile
from urllib.parse import urlsplit, unquote
import json
import sys
from pathlib import Path

e = html.escape
CSS = '''
:root { color-scheme: light; --bg:#fff; --text:#1c1e22; --muted:#4a505a; --line:#e2e4e8; --line-strong:#b9bec7; --accent:#1b4fd8; --ink-h:#112f86; --tint-2:#e3ebff; --on-accent:#fff; }
:root[data-theme="dark"] { color-scheme: dark; --bg:#0f1115; --text:#e9ebee; --muted:#b4bbc6; --line:#262a31; --line-strong:#4a515c; --accent:#8db3ff; --ink-h:#b9d0ff; --tint-2:#1f2940; --on-accent:#0c1a38; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { color-scheme: dark; --bg:#0f1115; --text:#e9ebee; --muted:#b4bbc6; --line:#262a31; --line-strong:#4a515c; --accent:#8db3ff; --ink-h:#b9d0ff; --tint-2:#1f2940; --on-accent:#0c1a38; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.7 -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", "Noto Sans KR", sans-serif; word-break: keep-all; overflow-wrap: break-word; }
a { color: var(--accent); text-underline-offset: 3px; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.page { max-width: 64rem; margin: 0 auto; padding: 28px 16px 64px; }
h1 { margin: 0; font-size: 1.75rem; line-height: 1.3; color: var(--ink-h); }
.lede { margin: 6px 0 0; color: var(--muted); font-size: .9375rem; }
.rows { list-style: none; margin: 28px 0 0; padding: 0; }
.row { display: grid; grid-template-columns: 15rem minmax(0, 1fr) auto; gap: 8px 20px; padding: 20px 0; border-top: 1px solid var(--line); align-items: start; }
.row.base:first-child { border-top: 2px solid var(--accent); }
.thumb { display: block; border: 1px solid var(--line-strong); border-radius: 8px; overflow: hidden; line-height: 0; }
.thumb img { width: 100%; height: auto; }
h2 { margin: 0; font-size: 1.125rem; line-height: 1.4; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.id { font-size: .75rem; font-weight: 700; line-height: 1.6; padding: 0 9px; border-radius: 999px; color: var(--on-accent); background: var(--accent); }
.info p { margin: 2px 0 0; }
dl { margin: 8px 0 0; }
dt { font-size: .8125rem; font-weight: 700; color: var(--ink-h); margin-top: 8px; }
dd { margin: 0; font-size: .9375rem; line-height: 1.6; }
.pick { margin: 0; padding: 0; border: 0; display: flex; gap: 6px; min-width: 0; }
.pick legend { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.pick label { position: relative; cursor: pointer; }
.pick input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.pick span { display: block; min-width: 56px; text-align: center; padding: 6px 12px; border: 1px solid var(--line-strong); border-radius: 8px; font-size: .875rem; color: var(--muted); }
.pick input:checked + span { background: var(--tint-2); color: var(--text); font-weight: 700; border-color: var(--accent); }
.pick input:focus-visible + span { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (max-width: 860px) { .row { grid-template-columns: minmax(0, 1fr); } .thumb { max-width: 22rem; } }
'''
# localStorage는 보는 사람 한 명의 편의일 뿐이라 막혀도 화면은 그대로 동작한다.
JS = '''(function () {
  var key = 'gallery-pick:' + location.pathname, saved = Object.create(null);
  try {
    var value = JSON.parse(localStorage.getItem(key) || '{}');
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      Object.keys(value).forEach(function (id) {
        if (value[id] === 'keep' || value[id] === 'drop') saved[id] = value[id];
      });
    }
  } catch (e) {}
  [].forEach.call(document.querySelectorAll('.row[data-key]'), function (row) {
    var id = row.getAttribute('data-key');
    [].forEach.call(row.querySelectorAll('input'), function (i) {
      if (saved[id] === i.value) i.checked = true;
      i.addEventListener('change', function () { saved[id] = i.value; try { localStorage.setItem(key, JSON.stringify(saved)); } catch (e) {} });
    });
  });
})();'''


def row(it):
    base = it.get('baseline')
    tag = '기준' if base else it['id']
    link = f'<p><a href="{e(it["href"])}">검토용 페이지 열기</a></p>'
    misfit = '' if base else f'<dt>이 문서에 맞지 않는 곳</dt><dd>{e(it["misfit"])}</dd>'
    pick = '' if base else (
        f'<fieldset class="pick"><legend>판정</legend>'
        f'<label><input type="radio" name="p-{e(it["id"])}" value="keep"><span>유지</span></label>'
        f'<label><input type="radio" name="p-{e(it["id"])}" value="drop"><span>제외</span></label></fieldset>')
    key = '' if base else f' data-key="{e(it["id"])}"'
    return (f'<li class="row{" base" if base else ""}"{key}>'
            f'<a class="thumb" href="{e(it["href"])}"><img src="{e(it["thumb"])}" alt="{e(it["name"])} 대표 장면" width="1440" height="900"></a>'
            f'<div class="info"><h2><span class="id">{e(tag)}</span>{e(it["name"])}</h2>{link}'
            f'<dl><dt>기준과 다른 점</dt><dd>{e(it["diff"])}</dd>{misfit}</dl></div>{pick}</li>')


def local_reference(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError('links must be nonempty local relative paths')
    decoded = unquote(value)
    url = urlsplit(decoded)
    if url.scheme or url.netloc or not url.path or url.path.startswith('/') or "\\" in decoded:
        raise ValueError('gallery links and thumbnails must be relative local files')
    return value


def validate(manifest):
    if not isinstance(manifest, dict):
        raise ValueError('manifest must be an object')
    for key in ('title', 'lede'):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            raise ValueError(f'{key} must be a nonempty string')
    items = manifest.get('items')
    if not isinstance(items, list) or len(items) < 2:
        raise ValueError('gallery requires a baseline and at least one variant')
    ids = set()
    baselines = 0
    for item in items:
        if not isinstance(item, dict):
            raise ValueError('each item must be an object')
        for key in ('id', 'name', 'href', 'thumb', 'diff'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'item.{key} must be a nonempty string')
        if item['id'] in ids:
            raise ValueError('gallery item ids must be unique')
        ids.add(item['id'])
        if not isinstance(item.get('baseline', False), bool):
            raise ValueError('baseline must be a boolean')
        if item.get('baseline', False):
            baselines += 1
        elif not isinstance(item.get('misfit'), str) or not item['misfit'].strip():
            raise ValueError('variants require a misfit string; use an explicit unknown when not evaluated')
        local_reference(item['href'])
        local_reference(item['thumb'])
    if baselines != 1:
        raise ValueError('gallery must contain exactly one baseline')


def verify_local_files(manifest, output, root):
    """Check containment and existence, without copying or following symlinks."""
    root = root.resolve(strict=True)
    output_parent = output.parent.resolve(strict=True)
    output_parent.relative_to(root)
    for item in manifest['items']:
        for key in ('href', 'thumb'):
            raw = unquote(urlsplit(item[key]).path)
            lexical = output_parent / raw
            # Resolve only after checking every lexical component for symlinks.
            current = Path(lexical.anchor)
            for part in lexical.parts[1:]:
                current = current / part
                if current.is_symlink():
                    raise ValueError('gallery resources must not use symlinks')
            target = lexical.resolve(strict=True)
            target.relative_to(root)
            if not target.is_file():
                raise ValueError('gallery reference is not a file: ' + raw)


def build(m):
    validate(m)
    items = sorted(m['items'], key=lambda it: not it.get('baseline', False))
    t = e(m['title'])
    return (f'<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="light dark">\n'
            f'<title>{t}</title>\n<style>{CSS}</style>\n</head>\n<body>\n<div class="page">\n'
            f'<header><h1>{t}</h1><p class="lede">{e(m["lede"])}</p></header>\n'
            f'<main><ul class="rows">\n' + '\n'.join(row(i) for i in items) +
            f'\n</ul></main>\n</div>\n<script>{JS}</script>\n</body>\n</html>\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--root', type=Path, help='allowed offline resource root; defaults to output parent')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
        rendered = build(manifest)
        verify_local_files(manifest, args.output, args.root or args.output.parent)
        if args.output.is_symlink():
            raise ValueError('output must not be a symlink')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.output.parent,
                                         prefix='.gallery-', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(rendered)
        try:
            os.replace(temporary, args.output)
        finally:
            temporary.unlink(missing_ok=True)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print('wrote', args.output, len(rendered.encode('utf-8')), 'bytes')


if __name__ == '__main__':
    main()
