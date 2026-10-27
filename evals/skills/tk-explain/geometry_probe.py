#!/usr/bin/env python3
"""Repository-only compatibility experiment; never an installed SVG validator.

Run with the reviewed diagram-design checkout at the pinned revision below.
No network, dependency install or production HTML changes are performed.
Zero upstream findings is NOT a TigerKit geometry pass.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

REVISION = '97d795138448f6a739a0cebc3d9beb37a42077f1'
ROOT = Path(__file__).resolve().parents[3]


def svg(body):
    return '<svg viewBox="0 0 400 200">' + body + '</svg>'


def fixtures():
    line = '<path d="M 10 20 H 90" marker-end="url(#arrow)"/>'
    node = '<rect x="100" y="60" width="160" height="64" stroke="#333" fill="#fff"/>'
    mask = '<rect x="240" y="80" width="48" height="12" fill="#fff"/>'
    cases = [
        ('straight', svg(line), False, 'supported control'),
        ('duplicate', svg(line + line), True, 'supported overlap'),
        ('head-tail', svg(line + '<path d="M 90 20 H 180" marker-end="url(#arrow)"/>'), False, 'valid joint'),
        ('border', svg(node + '<path d="M 100 60 H 260" marker-end="url(#arrow)"/>'), True, 'border and corner candidates'),
        ('ports', svg(node + '<path d="M 260 90 H 340" marker-end="url(#arrow)"/>'
                      + '<path d="M 260 95 H 340" marker-end="url(#arrow)"/>'), True, 'close output ports'),
        ('mask-later-node', svg(mask + node), True, 'covered mask'),
        ('mask-earlier-node', svg(node + mask), False, 'visible mask'),
        ('diagonal', svg('<path d="M 10 20 L 90 80" marker-end="url(#arrow)"/>'), True, 'false positive under TigerKit non-orthogonal policy'),
        ('curve', svg('<path d="M 10 20 Q 40 80 90 20" marker-end="url(#arrow)"/>'), False, 'curved control'),
        ('invalid-path', svg('<path d="M 10 20 L ?" marker-end="url(#arrow)"/>'), True, 'parser diagnostic'),
        ('scaled-duplicates', svg('<g transform="scale(2)">' + line + line + '</g>'), False, 'unverified: unsupported transform silently omitted'),
        ('css-marker-duplicates', svg('<style>.edge {marker-end:url(#arrow)}</style>'
                                    + line.replace('marker-end="url(#arrow)"', 'class="edge"') * 2), False, 'unverified: CSS markers not resolved'),
        ('single-quote-duplicates', svg((line + line).replace('"', "'")), False, 'unverified: attribute parser ignores single quotes'),
        ('separate-canvases', svg(line) + svg(line), True, 'false positive: independent SVG coordinate systems conflated'),
    ]
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--sample', type=Path, action='append', default=[])
    args = parser.parse_args()
    revision = subprocess.check_output(['git', '-C', str(args.upstream), 'rev-parse', 'HEAD'], text=True).strip()
    source = args.upstream / 'scripts/verify-geometry.py'
    if revision != REVISION:
        parser.error('expected pinned upstream ' + REVISION)
    tracked = subprocess.check_output(['git', '-C', str(args.upstream), 'show', REVISION + ':scripts/verify-geometry.py'])
    if source.read_bytes() != tracked:
        parser.error('upstream verifier differs from pinned Git content')
    spec = importlib.util.spec_from_file_location('upstream_geometry', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = []
    with tempfile.TemporaryDirectory() as temp:
        for name, content, expected, interpretation in fixtures():
            path = Path(temp) / (name + '.html')
            path.write_text(content, encoding='utf-8')
            findings = module.check(path)
            results.append(dict(case=name, expected_findings=expected, findings=findings,
                                reproduced=bool(findings) == expected, interpretation=interpretation))
    samples = [ROOT / 'skills/tk-explain/assets/chart-examples.html', *args.sample]
    observations = [dict(sample=p.name, findings=module.check(p),
                         interpretation='observation only; not proof of geometry coverage') for p in samples]
    print(json.dumps(dict(upstream=revision, fixtures=results, samples=observations,
                          decision='defer runtime integration; unsupported inputs require Unverifiable'),
                     ensure_ascii=False, indent=2))
    return 0 if all(row['reproduced'] for row in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
