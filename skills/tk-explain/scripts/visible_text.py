#!/usr/bin/env python3
"""Extract authored review text and image alt text, not a browser visibility verdict."""
import argparse
from html.parser import HTMLParser
from pathlib import Path


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        hidden = bool(self.stack and self.stack[-1][1]) or tag in ('script', 'style', 'template', 'head') or 'hidden' in attrs
        if not hidden:
            if tag == 'img' and attrs.get('alt'):
                self.parts.append('\n[image: ' + attrs['alt'] + ']\n')
            elif tag in ('p', 'div', 'section', 'br', 'li', 'tr', 'h1', 'h2', 'h3', 'figcaption', 'summary'):
                self.parts.append('\n')
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag in ('td', 'th'):
            self.parts.append(' | ')

    def handle_data(self, data):
        if not self.stack or not self.stack[-1][1]:
            self.parts.append(data)

    def text(self):
        return '\n'.join(line for raw in ''.join(self.parts).splitlines() if (line := ' '.join(raw.split()))) + '\n'


def extract(source):
    parser = VisibleText()
    parser.feed(source)
    return parser.text()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html')
    args = parser.parse_args()
    print(extract(Path(args.html).read_text(encoding='utf-8')), end='')
