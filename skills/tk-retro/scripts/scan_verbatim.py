#!/usr/bin/env python3
"""Find private literals and shared wording without emitting their contents."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import unicodedata


def normalize(text: str) -> str:
    return ' '.join(unicodedata.normalize('NFKC', text).split())


def mask(text: str, allowed: list[str]) -> str:
    for value in sorted(allowed, key=len, reverse=True):
        if value:
            text = text.replace(value, '\0' * len(value))
    return text


def scan(texts: list[str], messages: list[str], terms: list[str],
         allowed: list[str] | None = None, minimum: int = 10) -> dict:
    if minimum < 1:
        raise ValueError('minimum must be positive')
    exemptions = [normalize(value) for value in (allowed or [])]
    windows = set()
    for message in messages:
        source = mask(normalize(message), exemptions)
        windows.update(source[i:i + minimum] for i in range(len(source) - minimum + 1)
                       if '\0' not in source[i:i + minimum]
                       and any(c.isalnum() for c in source[i:i + minimum]))
    files = []
    for index, text in enumerate(texts, 1):
        # Exemptions never mask the private identifier inventory.
        identifiers = sum(text.count(term) for term in terms if term)
        target = mask(normalize(text), exemptions)
        runs = []
        for start in range(len(target) - minimum + 1):
            if target[start:start + minimum] not in windows:
                continue
            end = start + minimum
            if runs and start <= runs[-1][1]:
                runs[-1][1] = end
            else:
                runs.append([start, end])
        files.append({'file': index, 'identifier_matches': identifiers,
                      'verbatim_matches': len(runs), 'normalized_ranges': runs})
    return {'files': files, 'identifier_matches': sum(x['identifier_matches'] for x in files),
            'verbatim_matches': sum(x['verbatim_matches'] for x in files)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('files', nargs='+', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('expected object')
        for key in ('messages', 'terms', 'allow'):
            values = data.get(key, [] if key == 'allow' else None)
            if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
                raise ValueError('expected nonblank string list')
        if not data['messages'] or not any(normalize(x) for x in data['messages']):
            raise ValueError('missing comparison evidence')
        result = scan([p.read_text(encoding='utf-8') for p in args.files],
                      data['messages'], data['terms'], data.get('allow'))
    except (OSError, UnicodeError, ValueError, TypeError):
        print('{"error":"invalid input or unreadable file"}', file=sys.stderr)
        return 2
    print(json.dumps(result))
    return int(bool(result['identifier_matches'] or result['verbatim_matches']))


if __name__ == '__main__':
    raise SystemExit(main())
