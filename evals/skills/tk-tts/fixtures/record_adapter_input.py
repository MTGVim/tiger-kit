#!/usr/bin/env python3
"""Record an eval-only adapter boundary; never load a model or create audio."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text-file', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    source = args.text_file.absolute()
    receipt = args.receipt.absolute()
    for path in (source, receipt):
        if not path.is_relative_to(root) or path.resolve() != path:
            parser.error('paths must be repository-owned and nonsymlink')
    if not source.is_file() or receipt.exists() or not receipt.parent.is_dir():
        parser.error('input must exist and receipt must use a fresh path with an existing parent')
    payload = source.read_bytes()
    record = {
        'text_file': source.relative_to(root).as_posix(),
        'text': payload.decode('utf-8'),
        'sha256': hashlib.sha256(payload).hexdigest(),
        'synthesized': False,
    }
    with receipt.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
