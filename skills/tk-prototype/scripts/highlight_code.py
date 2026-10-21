#!/usr/bin/env python3
"""Render source as escaped, static offline code markup without changing its text."""
import argparse
from html import escape
from pathlib import Path
import re
import sys

ALIASES = {'kt': 'kotlin', 'js': 'javascript', 'ts': 'typescript', 'tsx': 'typescript',
           'jsx': 'javascript', 'py': 'python', 'patch': 'diff'}
KEYWORDS = {
    'kotlin': 'abstract actual annotation as break by catch class companion const constructor continue crossinline data delegate do dynamic else enum expect external false field file final finally for fun get if import in infix init inline inner interface internal is lateinit noinline null object open operator out override package param private property protected public receiver reified return sealed set setparam super suspend tailrec this throw true try typealias typeof val var vararg when where while',
    'javascript': 'async await break case catch class const continue debugger default delete do else export extends false finally for from function get if import in instanceof let new null of return set static super switch this throw true try typeof undefined var void while with yield',
    'python': 'and as assert async await break case class continue def del elif else except False finally for from global if import in is lambda match None nonlocal not or pass raise return True try while with yield',
    'json': 'true false null',
}
KEYWORDS['typescript'] = KEYWORDS['javascript'] + ' abstract any as boolean declare enum implements infer interface is keyof namespace never number private protected public readonly satisfies string type unknown'
TOKEN = re.compile(r'(?P<comment>/\*[\s\S]*?\*/|//[^\r\n]*)|(?P<string>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)|(?P<number>\b(?:0[xX][\da-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b)|(?P<name>@[\w.]+)|(?P<word>\b[A-Za-z_$][\w$]*\b)')
PY_TOKEN = re.compile(TOKEN.pattern.replace(r'/\*[\s\S]*?\*/|//[^\r\n]*', r'\#[^\r\n]*'))
JSON_TOKEN = re.compile(r'(?P<string>"(?:\\.|[^"\\])*")|(?P<number>-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b)|(?P<word>\b(?:true|false|null)\b)')


def highlight(source, language='', line_start=None):
    """Return a pre/code component; line numbers are CSS metadata, never source text.

    Known languages use conservative lexical colors, not a compiler/parser. Unknown
    languages remain escaped plain text. Do not infer a language from untrusted code.
    """
    if '\r' in source or '\x00' in source:
        raise ValueError('HTML cannot preserve CR or NUL textContent; normalize explicitly')
    language = ALIASES.get(language.lower(), language.lower())
    parts = []
    position = 0
    keywords = set(KEYWORDS.get(language, '').split())
    pattern = PY_TOKEN if language == 'python' else JSON_TOKEN if language == 'json' else TOKEN
    if language in KEYWORDS:
        for match in pattern.finditer(source):
            parts.append((source[position:match.start()], None))
            kind = match.lastgroup
            if kind == 'word':
                kind = 'keyword' if match.group() in keywords else None
            parts.append((match.group(), kind))
            position = match.end()
    parts.append((source[position:], None))
    # Split raw tokens before escaping; tags cannot straddle physical source lines.
    lines = ['']
    for text, kind in parts:
        for piece in text.splitlines(keepends=True):
            ending = re.search(r'(\r\n|\r|\n)$', piece)
            body = piece[:ending.start()] if ending else piece
            encoded = escape(body, quote=False)
            lines[-1] += f'<span class="ht-code-{kind}">{encoded}</span>' if kind and body else encoded
            if ending:
                lines[-1] += ending.group()
                lines.append('')
    if lines[-1] == '' and source.endswith(('\r', '\n')):
        lines.pop()
    raw_lines = source.splitlines(keepends=True)
    rendered = []
    for index, line in enumerate(lines):
        raw = raw_lines[index] if index < len(raw_lines) else ''
        kind = ' ht-code-add' if language == 'diff' and raw.startswith('+') else ' ht-code-delete' if language == 'diff' and raw.startswith('-') else ''
        number = f' data-line="{line_start + index}"' if line_start is not None else ''
        rendered.append(f'<span class="ht-code-line{kind}"{number}>{line}</span>')
    numbered = ' data-numbered' if line_start is not None else ''
    return f'<pre class="ht-code"{numbered}><code>' + ''.join(rendered) + '</code></pre>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='UTF-8 source file, read without newline translation')
    parser.add_argument('--language', default='', help='kotlin/kt, javascript/js/jsx, typescript/ts/tsx, python/py, json, diff/patch; otherwise plain')
    parser.add_argument('--line-start', type=int, help='optional first source line number')
    args = parser.parse_args()
    source = args.source.read_bytes().decode('utf-8')
    # HTML parsing normalizes CRLF/CR to LF. Reject instead of silently changing textContent.
    if '\r' in source or '\x00' in source:
        parser.error('HTML cannot preserve CR or NUL textContent; explicitly normalize the source first')
    sys.stdout.write(highlight(source, args.language, args.line_start))


if __name__ == '__main__':
    main()
