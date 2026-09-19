#!/usr/bin/env python3
"""Check mechanically decidable documentation contracts; prose still needs review."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import audit_catalog
import validate_skills
from artifact_policy import validate_artifact_guards

ROOT = Path(__file__).resolve().parents[1]


def visible_lines(text: str):
    fence = None
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
        if comment:
            if '-->' not in line:
                continue
            line = line.split('-->', 1)[1]
            comment = False
        while '<!--' in line:
            before, after = line.split('<!--', 1)
            if '-->' in after:
                line = before + after.split('-->', 1)[1]
            else:
                line = before
                comment = True
                break
        stripped = line.strip()
        match = re.match(r'^(`{3,}|~{3,})', stripped)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, stripped


def table_cells(line: str) -> list[str]:
    # GFM treats pipes inside code spans as delimiters too. An odd backslash escapes it.
    cells, start = [], 0
    for index, char in enumerate(line):
        if char != '|':
            continue
        slash = index - 1
        while slash >= 0 and line[slash] == '\\':
            slash -= 1
        if (index - 1 - slash) % 2:
            continue
        cells.append(line[start:index].strip())
        start = index + 1
    cells.append(line[start:].strip())
    if line.startswith('|'):
        cells.pop(0)
    if cells and cells[-1] == '' and line.endswith('|'):
        cells.pop()
    return cells


def table_errors(text: str) -> list[str]:
    lines = list(visible_lines(text))
    errors = []
    width = None
    for index, (number, line) in enumerate(lines):
        cells = table_cells(line)
        is_separator = len(cells) > 1 and all(re.fullmatch(r':?-{3,}:?', c) for c in cells)
        if is_separator and index:
            width = len(cells)
            if len(table_cells(lines[index-1][1])) != width:
                errors.append(f'line {number-1}: table header column count differs from separator')
        elif width is not None:
            if not line or '|' not in line:
                width = None
            elif len(cells) != width:
                errors.append(f'line {number}: table has {len(cells)} columns; expected {width} (escape literal pipes)')
    return errors


def catalog_kind_errors(text: str, kinds: dict[str, str]) -> list[str]:
    errors = []
    inside = False
    for number, line in visible_lines(text):
        if line == '## 스킬 구성':
            inside = True
        elif inside and line.startswith('## '):
            break
        elif inside and line.startswith('|'):
            cells = table_cells(line)
            if len(cells) < 2:
                continue
            name = cells[0].strip('`')
            if name in kinds:
                expected = 'user' if kinds[name] == 'user-invoked' else kinds[name]
                if cells[1].strip('`') != expected:
                    errors.append(f'README.md:{number}: {name} invocation must be {expected}')
    return errors


def main() -> int:
    errors = []
    files = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--', '*.md'], cwd=ROOT, capture_output=True, check=True).stdout.decode().split('\0')
    for relative in sorted(set(files) - {''}):
        path = ROOT / relative
        if path.is_file():
            errors.extend(f'{relative}: {e}' for e in table_errors(path.read_text(encoding='utf-8')))
    skills = validate_skills.discover_skills()
    kinds = {name: validate_skills.nested(data, 'metadata', 'tigerkit', 'kind') for name, (_, data, _) in skills.items()}
    errors.extend(catalog_kind_errors((ROOT / 'README.md').read_text(encoding='utf-8'), kinds))
    parity = audit_catalog.readme_catalog_parity(set(skills), ROOT)
    for category, names in parity.items():
        if names:
            errors.append(f'README catalog {category}: {", ".join(names)}')
    errors.extend(validate_skills.validate_repo_links())
    errors.extend(validate_artifact_guards(ROOT))
    if errors:
        print('\n'.join(errors))
        return 1
    print('Documentation tables, catalog kinds/parity, relative links and artifact policy: Pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
