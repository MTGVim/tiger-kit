#!/usr/bin/env python3
"""Assemble authored HTML fragments with the unchanged offline document shell."""
import argparse
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from string import Template
from urllib.parse import quote, unquote

PACKAGE = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}
RESERVED = {'document-top', 'document-bottom'}


class Fragment(HTMLParser):
    """Collect native navigation while rejecting ambiguous fragment structure."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.sections = []
        self.active = []
        self.ids = set(RESERVED)
        self.links = []
        self.heading = None
        self.details = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'html', 'head', 'body', 'main', 'script', 'style', 'h1'}:
            raise ValueError('body/footer must be content fragments; use --css/--script for authored code')
        if self.details and self.details[-1]['first'] is None:
            self.details[-1]['first'] = tag
            if tag != 'summary':
                raise ValueError('details needs a first-child summary')
        identifier = attrs.get('id')
        if identifier is not None:
            if not identifier or re.search(r'\s', identifier) or identifier in self.ids:
                raise ValueError('empty, duplicate or reserved ID: ' + str(identifier))
            self.ids.add(identifier)
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.links.append(unquote(attrs['href'][1:]))
        if tag == 'section':
            if not identifier:
                raise ValueError('each section needs a stable ID')
            section = {'id': identifier, 'title': '', 'children': []}
            (self.active[-1]['children'] if self.active else self.sections).append(section)
            self.active.append(section)
        if re.fullmatch('h[2-6]', tag) and self.active and not self.active[-1]['title']:
            self.heading = self.active[-1]
        if tag == 'details':
            self.details.append({'first': None})
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            raise ValueError('unbalanced fragment closing tag: ' + tag)
        self.stack.pop()
        if re.fullmatch('h[2-6]', tag):
            self.heading = None
        if tag == 'section':
            if not self.active.pop()['title'].strip():
                raise ValueError('each section needs a non-empty heading')
        if tag == 'details':
            if self.details.pop()['first'] != 'summary':
                raise ValueError('details needs a first-child summary')

    def handle_data(self, value):
        if self.heading is not None:
            self.heading['title'] += value
        if self.details and self.details[-1]['first'] is None and value.strip():
            raise ValueError('details text must follow its summary')

    def finish(self):
        self.close()
        if self.stack:
            raise ValueError('unclosed fragment tag: ' + self.stack[-1])
        missing = set(self.links) - self.ids
        if missing:
            raise ValueError('missing fragment targets: ' + ', '.join(sorted(missing)))


def toc(sections):
    return '<ol>' + ''.join(
        '<li><a href="#' + html.escape(quote(s['id'], safe=''), quote=True) + '">' +
        html.escape(' '.join(s['title'].split())) + '</a>' +
        (toc(s['children']) if s['children'] else '') + '</li>' for s in sections
    ) + '</ol>'


def resolve_theme(explicit=None):
    if explicit:
        return explicit, []
    config = Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config') / 'tigerkit/settings.json'
    notes = []
    try:
        if not config.exists():
            config.parent.mkdir(parents=True, exist_ok=True)
            try:
                with config.open('x', encoding='utf-8') as stream:
                    stream.write('{"html":{"theme":"system"}}\n')
                notes.append('Created default HTML theme settings: ' + str(config))
            except FileExistsError:
                pass
        value = json.loads(config.read_text(encoding='utf-8'))
        if not isinstance(value, dict) or not isinstance(value.get('html', {}), dict):
            raise ValueError('expected settings object with an html object')
        theme = value.get('html', {}).get('theme')
        if theme is None or isinstance(theme, str) and not theme.strip():
            theme = 'system'
        if theme not in ('system', 'light', 'dark'):
            raise ValueError('unsupported html.theme')
        return theme, notes
    except (OSError, UnicodeError, ValueError) as error:
        return 'system', notes + ['Theme settings unavailable; preserved existing data: ' + str(error)]


def assemble(body, title, *, theme='system', lang='ko', css='', script='', footer=''):
    if not title.strip() or not body.strip():
        raise ValueError('a subject-specific title and non-empty body are required')
    if theme not in ('system', 'light', 'dark'):
        raise ValueError('unsupported theme')
    parser = Fragment()
    parser.feed(body)
    if parser.stack:
        raise ValueError('unclosed body fragment tag: ' + parser.stack[-1])
    if not parser.sections:
        raise ValueError('body needs at least one section with a heading')
    parser.feed(footer)
    parser.finish()
    if re.search(r'</style\b', css, re.I) or re.search(r'</script\b', script, re.I):
        raise ValueError('escape embedded closing style/script tags in authored code')
    template = Template((PACKAGE / 'assets/document-shell.html').read_text(encoding='utf-8'))
    return template.substitute(
        title=html.escape(title), lang=html.escape(lang, quote=True), theme=theme,
        theme_attr='' if theme == 'system' else ' data-theme="' + theme + '"',
        body=body, footer=footer, toc=toc(parser.sections),
        css=(PACKAGE / 'assets/html-theme.css').read_text(encoding='utf-8'),
        script=(PACKAGE / 'assets/html-theme.js').read_text(encoding='utf-8'),
        extra_css='<style>' + css + '</style>' if css else '',
        extra_script='<script>' + script + '</script>' if script else '',
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--body', type=Path, required=True, help='authored main-content HTML fragment, without h1')
    parser.add_argument('--title', required=True, help='subject-specific title, also used for h1/topbar')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--theme', choices=['system', 'light', 'dark'])
    parser.add_argument('--lang', default='ko')
    parser.add_argument('--css', type=Path, help='optional content-scoped CSS')
    parser.add_argument('--script', type=Path, help='optional reviewed, authored figure JavaScript')
    parser.add_argument('--footer', type=Path, help='optional provenance/footer HTML fragment')
    parser.add_argument('--replace', action='store_true', help='only for an authorized existing output replacement')
    args = parser.parse_args()
    try:
        if args.output.is_symlink() or args.output.exists() and (
            not args.replace or not args.output.is_file() or args.output.stat().st_nlink != 1
        ):
            raise ValueError('output exists or is unsafe; use a fresh path or authorized --replace')
        read = lambda path: path.read_text(encoding='utf-8') if path else ''
        body, css, script, footer = map(read, (args.body, args.css, args.script, args.footer))
        # Validate content before any preference bootstrap or output mutation.
        assemble(body, args.title, theme=args.theme or 'system', lang=args.lang, css=css, script=script, footer=footer)
        theme, notes = resolve_theme(args.theme)
        document = assemble(body, args.title, theme=theme, lang=args.lang, css=css, script=script, footer=footer)
        with args.output.open('w' if args.replace else 'x', encoding='utf-8') as stream:
            stream.write(document)
        for note in notes:
            print(note)
        print('Built ' + str(args.output) + '; structural preflight only; final export and owning content/static/requested checks remain required.')
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
