#!/usr/bin/env python3
"""Conservative prose checks. Exit 0: no blockers; 1: blockers; 2: input error.

This tool is not a semantic or copyright checker. Code, quoted source, and exact
user headings can be protected. Static UI extraction is intentionally incomplete.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import NamedTuple


class Segment(NamedTuple):
    line: int
    scope: str
    text: str


# Only literal UI assignments/properties, not arbitrary script strings.
UI_LITERAL = re.compile(
    r'''(?:\b(?:textContent|innerText)\s*=|\b(?:label|caption|title|ariaLabel)\s*:|'''
    r'''setAttribute\(\s*['"](?:aria-label|title|placeholder)['"]\s*,)\s*'''
    r'''(?P<q>['"])(?P<text>(?:\\.|(?!(?P=q)).)*)(?P=q)'''
)


def script_segments(text: str, start: int = 1):
    for match in UI_LITERAL.finditer(text):
        yield Segment(start + text.count('\n', 0, match.start()), 'ui', match['text'])


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.segments = []
        self.heading = None
        self.heading_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        suppressed = bool(self.stack and self.stack[-1][1]) or tag in {
            'style', 'code', 'pre', 'blockquote', 'template', 'head'
        } or 'data-tk-protected' in attrs
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, suppressed))
        if suppressed:
            return
        if re.fullmatch('h[1-6]', tag):
            self.heading = (tag, self.getpos()[0])
            self.heading_parts = []
        for key in ('aria-label', 'alt', 'title', 'placeholder'):
            if attrs.get(key):
                self.segments.append(Segment(self.getpos()[0], 'ui', attrs[key]))

    def handle_endtag(self, tag):
        if self.heading and self.heading[0] == tag:
            self.segments.append(Segment(self.heading[1], 'heading', ''.join(self.heading_parts).strip()))
            self.heading = None
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        # Head scripts are inspected too, without treating source code as prose.
        if self.stack and self.stack[-1][0] == 'script':
            self.segments.extend(script_segments(data, self.getpos()[0]))
            return
        if self.stack and self.stack[-1][1]:
            return
        if self.heading:
            self.heading_parts.append(data)
        elif data.strip():
            self.segments.append(Segment(self.getpos()[0], 'body', data.strip()))


def extract(text: str, suffix: str):
    if suffix in {'.html', '.htm'}:
        parser = VisibleText()
        parser.feed(text)
        return parser.segments
    if suffix in {'.js', '.mjs'}:
        return list(script_segments(text))
    segments = []
    lines = text.splitlines()
    fence = None
    frontmatter = suffix == '.md' and bool(lines) and lines[0].strip() == '---'
    for number, line in enumerate(lines, 1):
        if frontmatter:
            if number > 1 and line.strip() == '---':
                frontmatter = False
            continue
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            continue
        if fence or line.lstrip().startswith(('>', '<!--')):
            continue
        clean = re.sub(r'`+[^`]*`+', '', line).strip()
        heading = re.match(r'^#{1,6}\s+(.+?)(?:\s+~)?$', clean)
        if heading:
            segments.append(Segment(number, 'heading', heading[1]))
        elif clean:
            neighbors = (lines[number-2] if number > 1 else '', lines[number] if number < len(lines) else '')
            isolated = re.match(r'^[-*]\s', clean) and not any(re.match(r'^\s*[-*]\s', v) for v in neighbors)
            segments.append(Segment(number, 'isolated-list' if isolated else 'body', clean))
    return segments


NEGATIVE_INSTRUCTION = re.compile(r'않습니다|않는다|금지|하지\s+마')
ALTERNATIVE_INSTRUCTION = re.compile(r'대신|한\s+뒤(?:에)?|[가-힣]+만(?=\s|[.,;:!?)]|$)')
LIST_PREFIX = re.compile(r'^\s*(?:[-+*]|\d+[.)])\s+')


def normalize_sentence(value):
    value = re.sub(r'`+[^`]*`+', '', value)
    value = LIST_PREFIX.sub('', value)
    return ' '.join(value.replace('**', '').replace('__', '').split())


def skill_sentences(text, suffix):
    # Join wrapped Markdown lines within the same paragraph/list item.
    # Preserve the starting line and never join across a heading, list item,
    # table cell, blank line, or protected block.
    if suffix not in {'.html', '.htm', '.js', '.mjs'}:
        text = re.sub(r'<!--.*?-->', lambda m: '\n' * m[0].count('\n'), text, flags=re.S)
    lines = text.splitlines()
    groups = []
    for segment in extract(text, suffix):
        if segment.scope == 'heading':
            continue
        if suffix in {'.html', '.htm', '.js', '.mjs'}:
            groups.append([segment])
            continue
        original = lines[segment.line - 1].lstrip()
        if original.startswith('|'):
            for cell in segment.text.strip('|').split('|'):
                if cell.strip():
                    groups.append([Segment(segment.line, segment.scope, cell.strip())])
            continue
        new_block = LIST_PREFIX.match(original) or original.startswith('<')
        previous = groups[-1][-1] if groups else None
        if (previous and previous.line + 1 == segment.line and not new_block
                and not lines[previous.line - 1].lstrip().startswith(('|', '<'))):
            groups[-1].append(segment)
        else:
            groups.append([segment])
    for group in groups:
        paragraph = '\n'.join(segment.text for segment in group)
        start = 0
        for delimiter in list(re.finditer(r'(?<=[.!?。])\s+', paragraph)) + [None]:
            end = delimiter.start() if delimiter else len(paragraph)
            value = normalize_sentence(paragraph[start:end])
            if value:
                line = group[0].line + paragraph[:start].count('\n')
                yield Segment(line, group[0].scope, value)
            if delimiter:
                start = delimiter.end()


def check(text, suffix, rules, profile, allowed_headings=(), allowed_boundaries=()):
    findings = []
    if profile == 'skill':
        boundaries = {normalize_sentence(value) for value in allowed_boundaries}
        for sentence in skill_sentences(text, suffix):
            if sentence.text in boundaries:
                continue
            if NEGATIVE_INSTRUCTION.search(sentence.text) and not ALTERNATIVE_INSTRUCTION.search(sentence.text):
                findings.append({'rule': 'negative-only-instruction', 'severity': 'warning',
                                 'line': sentence.line, 'scope': sentence.scope,
                                 'text': sentence.text, 'message': '대신 할 행동이나 실행 조건을 명시합니다. 순수 경계는 예외로 기록합니다.'})
    for segment in extract(text, suffix):
        if segment.scope == 'heading' and segment.text in allowed_headings:
            continue
        for rule in rules:
            if rule.get('profile') not in (None, profile):
                continue
            if rule['scope'] not in ('any', segment.scope):
                continue
            if re.search(rule['pattern'], segment.text):
                findings.append({'rule': rule['id'], 'severity': rule['severity'],
                                 'line': segment.line, 'scope': segment.scope,
                                 'text': segment.text, 'message': rule['message']})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path)
    parser.add_argument('--profile', choices=('prose', 'report', 'skill'), default='prose')
    parser.add_argument('--rules', type=Path, default=Path(__file__).resolve().parent.parent/'assets/prose-rules.json')
    parser.add_argument('--allow-heading', action='append', default=[], help='exact protected user heading; repeatable')
    parser.add_argument('--allow-boundary', action='append', default=[], help='exact pure boundary sentence; repeatable')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        rules = json.loads(args.rules.read_text(encoding='utf-8'))['rules']
        results = []
        for path in args.files:
            raw = path.read_bytes()
            findings = check(raw.decode('utf-8'), path.suffix.lower(), rules, args.profile, args.allow_heading, args.allow_boundary)
            results.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'findings': findings})
    except (OSError, ValueError, KeyError, re.error) as error:
        parser.exit(2, str(error) + '\n')
    report = {'profile': args.profile, 'protected_headings': args.allow_heading, 'protected_boundaries': args.allow_boundary, 'files': results,
              'limits': ['Static extraction does not cover computed UI, translated text, canvas, or semantics.']}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for result in results:
            for item in result['findings']:
                print(f"{result['path']}:{item['line']}: {item['severity']} {item['rule']}: {item['message']}")
        print('Blockers:', sum(x['severity']=='error' for r in results for x in r['findings']))
        if args.profile == 'skill':
            print('Negative-only warnings:', sum(x['rule']=='negative-only-instruction' for r in results for x in r['findings']))
    return 1 if any(x['severity']=='error' for r in results for x in r['findings']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
