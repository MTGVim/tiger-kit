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
MANUAL_REASONS = {
    'unauthorized-or-irreversible': '권한 없음 또는 되돌릴 수 없는 쓰기',
    'data-unavailable-after-search': '검색 후에도 데이터를 찾지 못함',
    'verified-capability-gap': '실제 시도에서 도구 한계 확인',
}


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
    automatable = item.get('automatable')
    if automatable is not None and type(automatable) is not bool:
        raise ValueError('automatable must be a boolean')
    if verification not in ('manual', 'verification-gap', 'auto-verified', 'partial', 'failed'):
        raise ValueError('invalid QA verification state')

    def valid_evidence(value):
        return isinstance(value, dict) and isinstance(value.get('ref'), str) and value['ref'].strip() \
            and isinstance(value.get('head'), str) and value['head'].strip()

    if verification == 'verification-gap':
        criterion = item.get('criterionId')
        if not isinstance(criterion, str) or not criterion.strip():
            raise ValueError('verification-gap rows need a stable criterionId')
        if evidence is not None or previous is not None or any(item.get(key) is not None for key in ('manualReason', 'searchScope', 'unblock')):
            raise ValueError('verification-gap rows cannot carry evidence or manual reasons')
        if automatable is False:
            raise ValueError('verification-gap rows must remain automatable')
        parts.append('<span class="badge gap">자동 검증 필요</span>')
    elif verification == 'manual':
        if evidence is not None:
            raise ValueError('manual QA rows cannot carry current automated evidence')
        reason = item.get('manualReason')
        if reason is not None:
            if reason not in MANUAL_REASONS:
                raise ValueError('invalid manual QA reason')
            scope = item.get('searchScope')
            unblock = item.get('unblock')
            if not isinstance(unblock, str) or not unblock.strip():
                raise ValueError('manual QA reasons need a concrete unblock')
            if reason in ('data-unavailable-after-search', 'verified-capability-gap') \
                    and (not isinstance(scope, str) or not scope.strip()):
                raise ValueError('data and capability limits need recorded searchScope')
            parts.append('<span class="manual-detail">이유: ' + html.escape(MANUAL_REASONS[reason]) + '</span>')
            if isinstance(scope, str) and scope.strip():
                parts.append('<span class="manual-detail">탐색·시도 범위: ' + text(scope) + '</span>')
            parts.append('<span class="manual-detail">해제 방법: ' + text(unblock) + '</span>')
        elif item.get('searchScope') is not None or item.get('unblock') is not None:
            raise ValueError('manual QA details need a manualReason')
        if automatable is True:
            parts.append('<span class="badge gap">요청된 체크리스트 · 자동화 가능</span>')
        if previous is not None and not valid_evidence(previous):
            raise ValueError('previous QA evidence needs nonblank ref and head')
        if previous is not None:
            parts.append('<span class="badge demoted">이전 head 검증</span>')
            parts.append('<span class="evidence">이전 근거: <code>' + html.escape(previous['ref']) +
                         '</code> @ <code class="ht-token">' + html.escape(previous['head']) + '</code></span>')
    else:
        if previous is not None or automatable is not None or any(item.get(key) is not None for key in ('manualReason', 'searchScope', 'unblock')):
            raise ValueError('automated QA rows cannot carry manual-only metadata')
        if not valid_evidence(evidence):
            raise ValueError('automated QA evidence needs nonblank ref and head')
        label = {'auto-verified': '자동 검증', 'partial': '부분 자동 확인', 'failed': '자동 실패'}[verification]
        klass = {'auto-verified': 'auto', 'partial': 'partial', 'failed': 'failed'}[verification]
        parts.append(f'<span class="badge {klass}">' + label + '</span>')
        parts.append('<span class="evidence">근거: <code>' + html.escape(evidence['ref']) +
                     '</code> @ <code class="ht-token">' + html.escape(evidence['head']) + '</code></span>')
    return (' ' + ' '.join(parts)) if parts else ''


def inventory(data: dict) -> str:
    if data.get('head') is not None and (not isinstance(data['head'], str) or not data['head'].strip()):
        raise ValueError('head must be a nonblank commit identifier')
    criterion_ids: set[str] = set()

    def criterion_id(item: dict) -> str:
        value = item.get('criterionId')
        if value is None:
            return ''
        if not isinstance(value, str) or not value.strip():
            raise ValueError('criterionId must be a nonblank string')
        if value in criterion_ids:
            raise ValueError('criterionId values must be unique')
        criterion_ids.add(value)
        return ' <code class="criterion-id">' + html.escape(value) + '</code>'

    def render_item(item: dict, gap_only: bool) -> str:
        checks = item.get('checks') or []
        if not checks:
            is_gap = item.get('verification', 'manual') == 'verification-gap'
            if is_gap != gap_only:
                return ''
            out = ['<li>' + text(item['title']) + criterion_id(item) + status(item)]
            if item.get('notes'):
                out.append('<ul>' + ''.join('<li>' + text(row) + '</li>' for row in item['notes']) + '</ul>')
            out.append('</li>')
            return ''.join(out)
        matching = [check for check in checks
                    if not check.get('heading') and (check.get('verification', 'manual') == 'verification-gap') == gap_only]
        if not matching:
            return ''
        out = ['<li>' + text(item['title']) + criterion_id(item)]
        if item.get('notes'):
            out.append('<ul>' + ''.join('<li>' + text(row) + '</li>' for row in item['notes']) + '</ul>')
        out.append('<ul>')
        for check in checks:
            if check.get('heading'):
                out.append('<li><strong>' + text(check['text']) + '</strong></li>')
                continue
            is_gap = check.get('verification', 'manual') == 'verification-gap'
            if is_gap != gap_only:
                continue
            out.append('<li><span>' + text(check['text']) + '</span>' + criterion_id(check) + status(check, item) + '</li>')
        out.extend(['</ul>', '</li>'])
        return ''.join(out)

    parts = ['<noscript id="qa-static">', '<style>header,.layout{display:none}</style>',
             '<main class="qa-static"><h1>' + text(data['title']) + '</h1>',
             '<p>체크 목록은 아래에서 읽을 수 있습니다. 체크·메모 저장과 필터를 사용하려면 JavaScript를 켜 주세요.</p>']
    environment = data.get('environment')
    if environment:
        parts.append('<p>' + text(environment['label']) + ' (' + text(environment['baseUrl']) + ')' + '</p>')
    if data.get('head'):
        parts.append('<p>기준 head: <code>' + html.escape(data['head']) + '</code></p>')
    if data.get('legend'):
        parts.append('<ul>' + ''.join('<li>' + text(row) + '</li>' for row in data['legend']) + '</ul>')
    gap_count = sum(
        1 for group in data['groups'] for item in group['items']
        for row in (item.get('checks') or [item])
        if not row.get('heading') and row.get('verification') == 'verification-gap'
    )
    if gap_count:
        parts.append('<section class="verification-gap-section"><h2>자동 검증 필요 (' + str(gap_count) + ')</h2>')
        parts.append('<p>자동화 가능한 미실행 행입니다. `/tk-browser-verify`를 인자 없이 실행한 뒤 시트를 다시 생성하세요.</p>')
        for group in data['groups']:
            items = ''.join(render_item(item, True) for item in group['items'])
            if items:
                parts.append('<section><h3>' + text(group['title']) + '</h3><ul>' + items + '</ul></section>')
        parts.append('</section>')
    for group in data['groups']:
        items = ''.join(render_item(item, False) for item in group['items'])
        if items:
            parts.append('<section class="group"><h2>' + text(group['title']) + '</h2><ul>' + items + '</ul></section>')
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
