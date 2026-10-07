#!/usr/bin/env python3
"""Regenerate the no-JavaScript reading projection from a QA sheet's own JSON."""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import tempfile
from pathlib import Path

DATA = re.compile(r'<script\b[^>]*\bid="qa-data"[^>]*>(.*?)</script>', re.S)
STATIC = re.compile(r'<noscript id="qa-static">.*?</noscript>', re.S)


def text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError('QA prose must be a string')
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', html.escape(value))


def status(item: dict, parent: dict | None = None) -> str:
    observed = item.get('provenance') == 'observed' and (parent is None or parent.get('provenance') == 'observed')
    parts = [] if observed else ['<span class="badge">코드 기준</span>']
    verification = item.get('verification', 'manual')
    evidence = item.get('evidence')
    previous = item.get('previousEvidence')
    if verification not in ('manual', 'auto-verified', 'partial'):
        raise ValueError('invalid QA verification state')

    def valid_evidence(value):
        return isinstance(value, dict) and isinstance(value.get('ref'), str) and value['ref'].strip() \
            and isinstance(value.get('head'), str) and value['head'].strip()

    if verification == 'manual':
        if evidence is not None:
            raise ValueError('manual QA rows cannot carry current automated evidence')
        if previous is not None and not valid_evidence(previous):
            raise ValueError('previous QA evidence needs nonblank ref and head')
        if previous is not None:
            parts.append('<span class="badge demoted">이전 head 검증</span>')
            parts.append('<span class="evidence">이전 근거: <code>' + html.escape(previous['ref']) +
                         '</code> @ <code class="ht-token">' + html.escape(previous['head']) + '</code></span>')
    else:
        if previous is not None:
            raise ValueError('automated QA rows cannot carry previous evidence')
        if not valid_evidence(evidence):
            raise ValueError('automated QA evidence needs nonblank ref and head')
        label = '자동 검증' if verification == 'auto-verified' else '부분 자동 확인'
        klass = 'auto' if verification == 'auto-verified' else 'partial'
        parts.append(f'<span class="badge {klass}">' + label + '</span>')
        parts.append('<span class="evidence">근거: <code>' + html.escape(evidence['ref']) +
                     '</code> @ <code class="ht-token">' + html.escape(evidence['head']) + '</code></span>')
    return (' ' + ' '.join(parts)) if parts else ''


def inventory(data: dict) -> str:
    parts = ['<noscript id="qa-static">', '<style>header,.layout{display:none}</style>',
             '<main class="qa-static"><h1>' + text(data['title']) + '</h1>',
             '<p>체크 목록은 아래에서 읽을 수 있습니다. 체크·메모 저장과 필터를 사용하려면 JavaScript를 켜 주세요.</p>']
    environment = data.get('environment')
    if environment:
        parts.append('<p>' + text(environment['label']) + ' (' + text(environment['baseUrl']) + ')' + '</p>')
    if data.get('legend'):
        parts.append('<ul>' + ''.join('<li>' + text(row) + '</li>' for row in data['legend']) + '</ul>')
    for group in data['groups']:
        parts.append('<section class="group"><h2>' + text(group['title']) + '</h2><ul>')
        for item in group['items']:
            parts.append('<li>' + text(item['title']) + status(item))
            if item.get('notes'):
                parts.append('<ul>' + ''.join('<li>' + text(row) + '</li>' for row in item['notes']) + '</ul>')
            if item.get('checks'):
                parts.append('<ul>')
                for check in item['checks']:
                    tag = 'strong' if check.get('heading') else 'span'
                    badge = '' if check.get('heading') else status(check, item)
                    parts.append(f'<li><{tag}>' + text(check['text']) + f'</{tag}>' + badge + '</li>')
                parts.append('</ul>')
            parts.append('</li>')
        parts.append('</ul></section>')
    parts.extend(['</main>', '</noscript>'])
    return '\n'.join(parts)


def render(path: Path) -> None:
    if any(part.is_symlink() for part in (path, *path.parents)) or not path.is_file():
        raise ValueError('target must be an owned regular file without symlink components')
    original = path.read_bytes()
    source = original.decode('utf-8')
    matches = DATA.findall(source)
    if len(matches) != 1 or len(STATIC.findall(source)) != 1:
        raise ValueError('target needs exactly one qa-data and qa-static region')
    projection = inventory(json.loads(matches[0]))
    candidate = STATIC.sub(lambda _: projection, source).encode('utf-8')
    if candidate == original:
        return
    fd, temporary = tempfile.mkstemp(prefix='.qa-static-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(candidate)
        os.chmod(temporary, path.stat().st_mode & 0o777)
        if path.read_bytes() != original:
            raise ValueError('target changed during rendering')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        render(args.path.absolute())
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f'Cannot render static inventory: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
