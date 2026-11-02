"""Validate receipt-driven on-screen disclosure before movie encoding."""
from __future__ import annotations

import math


def check(data, receipts, end, hard_captions=False, callouts_rendered=False):
    if not isinstance(receipts, list) or not math.isfinite(end) or end <= 0:
        raise ValueError('invalid disclosure receipts or duration')
    notices = set()
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise ValueError('TTS receipt must be an object')
        required = receipt.get('disclosure_required', False)
        if not isinstance(required, bool):
            raise ValueError('disclosure_required must be boolean')
        if required:
            notice = receipt.get('disclosure_notice')
            if not isinstance(notice, str) or not notice.strip():
                raise ValueError('disclosure_required needs a nonempty disclosure_notice')
            notices.add(notice.strip())
    declarations = data.get('disclosure_scene', [])
    if not isinstance(declarations, list):
        raise ValueError('disclosure_scene must be a list')
    sources = [('disclosure_scene', declarations)]
    if hard_captions:
        sources.append(('captions', data.get('captions', [])))
    if callouts_rendered:
        sources.append(('callouts', data.get('callouts', [])))
    for _, rows in sources:
        if not isinstance(rows, list):
            raise ValueError('disclosure intervals must be lists')
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('text'), str):
                raise ValueError('disclosure interval needs text')
            a, b = row.get('start_ms'), row.get('end_ms')
            if any(isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) for x in (a, b)):
                raise ValueError('disclosure times must be finite numbers')
            if not 0 <= a < b <= end:
                raise ValueError('disclosure interval must fit inside the video')
    results = []
    for notice in sorted(notices):
        spans = sorted((r['start_ms'], r['end_ms'], key)
                       for key, rows in sources for r in rows if notice in r['text'])
        gaps, used = [], set()
        reach = 0
        for index, (start, stop, key) in enumerate(spans):
            # Only the two video endpoints may have a one-second tolerance.
            if start > reach and not (index == 0 and start <= 1000):
                gaps.append([reach, start])
            reach = max(reach, stop)
            used.add(key)
        if reach < end - 1000:
            gaps.append([reach, end])
        if not spans or gaps:
            raise ValueError(f'AI disclosure is not visible throughout the video; uncovered_ms={gaps}')
        row = {'notice': notice, 'sources': sorted(used), 'coverage': 'declared' if 'disclosure_scene' in used else 'assembler-rendered'}
        if 'disclosure_scene' in used:
            row['human_action'] = 'check first, middle and last decoded frames show the readable notice outside captions'
        results.append(row)
    return {'required': bool(notices), 'pass': True, 'notices': results}
