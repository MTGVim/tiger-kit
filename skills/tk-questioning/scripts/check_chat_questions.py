#!/usr/bin/env python3
"""Check the most common chat question layout regressions (not semantics)."""
import argparse
import re
from pathlib import Path

QUESTION = re.compile(r'^❓\s+\*\*Q\d+\s*·')
OPTION = re.compile(r'(?<!\w)-\s*\([a-z]\)\s+')
RECOMMEND = re.compile(r'^➡️')

def check(text):
    lines = text.splitlines()
    issues = []
    question_lines = [i for i, line in enumerate(lines) if QUESTION.match(line.strip())]
    for i, line in enumerate(lines):
        if len(OPTION.findall(line)) > 1:
            issues.append((i + 1, '선택지를 한 줄에 여러 개 배치했습니다'))
        if '❓' in line and '➡️' in line:
            issues.append((i + 1, '질문과 추천이 한 줄에 합쳐졌습니다'))
        if RECOMMEND.match(line.strip()):
            if i and lines[i - 1].strip() and (QUESTION.match(lines[i - 1].strip()) or OPTION.search(lines[i - 1])):
                issues.append((i + 1, '질문·선택지와 추천 사이에 빈 줄이 없습니다'))
    for i in question_lines[1:]:
        before = lines[max(0, i - 3):i]
        if len(before) < 3 or before != ['', '---', '']:
            issues.append((i + 1, '다음 질문 전에 빈 줄·수평선·빈 줄을 넣으세요'))
    return issues

def selftest():
    good = '❓ **Q1 · 첫 질문**\n질문\n- (a) 선택\n\n➡️ 추천\n\n---\n\n❓ **Q2 · 둘째 질문**\n질문\n- (a) 선택\n\n➡️ 추천\n'
    assert not check(good)
    assert check(good.replace('\n\n---\n\n', '\n\n'))
    assert check(good.replace('- (a) 선택', '- (a) 선택 - (b) 다른 선택'))
    assert check(good.replace('- (a) 선택\n\n➡️', '- (a) 선택\n➡️'))
    assert check(good.replace('❓ **Q1 · 첫 질문**', '❓ **Q1 · 첫 질문** ➡️ 추천'))
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path, help='UTF-8 chat question draft')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.input is None:
        parser.error('input file required unless --selftest is set')
    issues = check(args.input.read_text(encoding='utf-8'))
    for line, message in issues:
        print('line {}: {}'.format(line, message))
    return 1 if issues else 0

if __name__ == '__main__':
    raise SystemExit(main())
