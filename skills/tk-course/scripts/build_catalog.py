#!/usr/bin/env python3
"""Build an optional local landing page for explicitly selected sibling courses."""
import argparse,json,os
from pathlib import Path
from html import escape as h
from urllib.parse import quote
from app_shell import THEME_CONTROL,BOOTSTRAP
from build_course import identifier,text,ASSETS

def build(root,output):
    root=root.absolute();output=output.absolute()
    if root.resolve()!=root or not root.is_dir() or output.resolve()!=output or output.parent!=root or output.exists():raise ValueError('use a safe collection root and a new HTML output in that root')
    items=[];ids=set()
    for entry in sorted(root.iterdir()):
        if entry.is_symlink():continue
        if not entry.is_dir() or not (entry/'course.json').is_file():continue
        source=entry/'course.json';index=entry/'index.html'
        if source.resolve()!=source or index.resolve()!=index or not index.is_file():raise ValueError('unsafe or missing course entry')
        course=json.loads(source.read_text());id=identifier(course['id']);text(course['title']);text(course['description'])
        if id in ids:raise ValueError('duplicate course identity; no implicit merge')
        ids.add(id);items.append((entry.name,course))
    if len(items)<2:raise ValueError('a collection landing requires at least two courses')
    cards=''.join('<article class="ht-card"><h2><a href="'+h(quote(name,safe='')+'/index.html',quote=True)+'">'+h(c['title'])+'</a></h2><p>'+h(c['description'])+'</p><ul>'+''.join('<li>'+h(o['description'])+'</li>' for o in c['objectives'])+'</ul></article>' for name,c in items)
    css=(ASSETS/'html-theme.css').read_text();js=(ASSETS/'html-theme.js').read_text()
    page='<!doctype html><html lang="ko" data-default-theme="system"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>학습 코스</title><script>'+BOOTSTRAP+'</script><style>'+css+'main{max-width:1100px;margin:auto;padding:32px;display:grid;gap:20px}</style><header class="ht-topbar"><p class="ht-topbar-title">학습 코스</p>'+THEME_CONTROL+'</header><main><h1>학습 코스</h1>'+cards+'</main><footer>🤖 본 강의 자료는 AI가 작성했습니다.</footer><script>'+js+'</script></html>'
    with output.open('x',encoding='utf-8') as f:f.write(page)
    return {'path':str(output),'courses':len(items),'progress':'owned by each course; not copied into the catalog'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    try:print(json.dumps(build(a.root,a.output),ensure_ascii=False))
    except (ValueError,OSError,KeyError,TypeError) as e:print(json.dumps({'status':'failed','detail':str(e)},ensure_ascii=False));raise SystemExit(1)
