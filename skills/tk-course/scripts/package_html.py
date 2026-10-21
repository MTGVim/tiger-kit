#!/usr/bin/env python3
"""Embed an explicit offline download allowlist into generated HTML documents."""
import argparse
import base64
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

PAYLOAD = re.compile(r'<template\b(?=[^>]*\bdata-ht-export(?:=|\s|>))[^>]*>.*?</template>', re.S)


def package(root, names, filename):
    root = Path(root).resolve(strict=True)
    if not names or len(names) != len(set(names)):
        raise ValueError('provide a non-empty, unique file allowlist')
    sources = {}
    for name in names:
        path = Path(name)
        if path.is_absolute() or any(part in ('.', '..') or part.startswith('.') for part in path.parts):
            raise ValueError('allowlist paths must be relative and contain no hidden components')
        current = root
        for part in path.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError('symlinks are not exportable')
        if not current.is_file() or current.stat().st_nlink != 1:
            raise ValueError('allowlist entries must be ordinary single-link files')
        key = path.as_posix()
        if key in sources:
            raise ValueError('duplicate normalized export path')
        data = current.read_bytes()
        is_html = path.suffix.lower() in ('.html', '.htm')
        if is_html:
            text = PAYLOAD.sub('', data.decode('utf-8'))
            if len(re.findall(r'</body\s*>', text, re.I)) != 1:
                raise ValueError('HTML needs one closing body tag')
            data = text.encode('utf-8')
        sources[key] = (data, is_html)
    if not any(is_html for _, is_html in sources.values()):
        raise ValueError('export requires at least one HTML document')
    if len(sources) == 1 and not next(iter(sources.values()))[1]:
        raise ValueError('a single export must be HTML')
    expected = '.html' if len(sources) == 1 else '.zip'
    if Path(filename).name != filename or not filename.isascii() or not filename.endswith(expected):
        raise ValueError('use an ASCII basename ending in ' + expected)

    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr not in ('href', 'src') or not value:
                    continue
                url = urlsplit(value)
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (root / self.name).parent / unquote(url.path)
                try:
                    relative = target.resolve().relative_to(root).as_posix()
                except ValueError:
                    raise ValueError('local link escapes export root') from None
                if relative not in sources:
                    raise ValueError('local link missing from allowlist: ' + relative)
    for name, (data, is_html) in sources.items():
        if is_html:
            parser = Links()
            parser.name = name
            parser.feed(data.decode('utf-8'))
    manifest = {'name': filename, 'files': [
        {'path': name, 'html': is_html, 'base64': base64.b64encode(data).decode('ascii')}
        for name, (data, is_html) in sources.items()
    ]}
    encoded = base64.b64encode(json.dumps(manifest, ensure_ascii=True, separators=(',', ':')).encode()).decode()
    # All validation precedes writes. Payloads contain source bytes without payloads,
    # so repeated packaging is bounded and generated ZIPs can retain their own controls.
    for name, (data, is_html) in sources.items():
        if is_html:
            marker = '<template data-ht-export data-entry="' + html.escape(name, quote=True) + '">' + encoded + '</template>'
            text = re.sub(r'</body\s*>', lambda m: marker + m.group(), data.decode('utf-8'), flags=re.I)
            (root / name).write_text(text, encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--name', required=True, help='ASCII .html or .zip download basename')
    parser.add_argument('files', nargs='+', help='explicit relative file allowlist, including linked pages/assets')
    args = parser.parse_args()
    try:
        result = package(args.root, args.files, args.name)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print('Embedded export for ' + str(len(result['files'])) + ' files')
