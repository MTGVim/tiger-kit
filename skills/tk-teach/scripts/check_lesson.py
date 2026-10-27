#!/usr/bin/env python3
"""Check lesson fragment relationships without grading content or learners."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import build_html


class Lesson(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.ids=set(); self.focus=[]; self.errors=[]; self.units=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs); ident=attrs.get('id')
        if ident: self.ids.add(ident)
        practice=next((a.get('id') for _,a in reversed(self.stack) if 'data-ht-practice' in a),None)
        if 'data-ht-nav-unit' in attrs: self.units+=1
        if 'data-ht-practice' in attrs and not ident: self.errors.append('practice requires an id')
        if 'data-ht-practice' in attrs and practice: self.errors.append('nested practice is not supported')
        if 'data-ht-focus' in attrs:
            target=attrs.get('data-ht-focus')
            if tag!='a' or not target or unquote(attrs.get('href',''))!='#'+target: self.errors.append('focus requires a matching native anchor')
            else: self.focus.append(target)
        for marker in ('data-ht-hint','data-ht-solution'):
            if marker in attrs:
                if tag!='details' or not practice: self.errors.append(marker+' requires details inside practice')
                if 'open' in attrs: self.errors.append(marker+' must start closed')
        if 'data-ht-retry' in attrs:
            if tag!='a' or not practice or attrs.get('href')!='#'+practice: self.errors.append('retry must link to its enclosing practice')
        if tag=='a' and 'href' in attrs:
            href=attrs['href']; parsed=urlsplit(href)
            if not href.startswith('#') and not (parsed.scheme in ('http','https') and parsed.netloc or parsed.scheme == 'mailto' and parsed.path):
                self.errors.append('local or unsafe link is not allowed: '+href)
        if tag not in build_html.VOID: self.stack.append((tag,attrs))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in build_html.VOID:self.handle_endtag(tag)
    def handle_endtag(self,tag):
        if tag not in build_html.VOID and self.stack:self.stack.pop()
    def finish(self):
        self.close()
        if not self.units:self.errors.append('at least one top-level lesson unit is required')
        for target in self.focus:
            if target not in self.ids:self.errors.append('focus target not found: '+target)
        return self.errors


def validate(body):
    common=build_html.Fragment()
    try:
        common.feed(body);common.finish()
        if not common.nav_units: return ['at least one top-level lesson unit is required']
    except ValueError as error: return [str(error)]
    lesson=Lesson();lesson.feed(body);return lesson.finish()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--body',required=True,type=Path);args=parser.parse_args()
    try: errors=validate(args.body.read_text(encoding='utf-8'))
    except (OSError,UnicodeError,ValueError) as error:parser.exit(2,str(error)+'\n')
    if errors:
        for error in errors: print(error)
        return 1
    print('Lesson structure verified; content accuracy and learning outcomes require separate review.')
    return 0

if __name__=='__main__':raise SystemExit(main())
