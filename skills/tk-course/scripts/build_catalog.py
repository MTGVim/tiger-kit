#!/usr/bin/env python3
"""Build or refresh an optional offline gallery for sibling courses."""
import argparse,json,math,os,tempfile
from pathlib import Path
from html import escape as h
from html.parser import HTMLParser
from urllib.parse import quote
from app_shell import THEME_CONTROL,BOOTSTRAP,theme_styles
from build_course import identifier,text,ASSETS
from components import svg

MARKER='tigerkit-course-catalog'
class CatalogMarker(HTMLParser):
    def __init__(self):super().__init__();self.owned=False
    def handle_starttag(self,tag,attrs):
        if tag=='meta' and dict(attrs).get('name')==MARKER:self.owned=True

def owned_output(output):
    if not output.exists():return
    if not output.is_file():raise ValueError('catalog output must be an HTML file')
    parser=CatalogMarker();parser.feed(output.read_text(encoding='utf-8'))
    if not parser.owned:raise ValueError('refusing to replace an unmarked catalog output')

def discover(root):
    items=[];ids=set()
    for entry in sorted(root.iterdir()):
        if entry.is_symlink() or not entry.is_dir():continue
        if not any(p.exists() or p.is_symlink() for p in (entry/'course.json',entry/'build/course.json')):continue
        # Prefer a published direct build; otherwise read the built manifest, not authored media paths.
        base=entry if (entry/'course.json').exists() and (entry/'index.html').exists() else entry/'build'
        source=base/'course.json';index=base/'index.html'
        if source.resolve()!=source or index.resolve()!=index or not source.is_file() or not index.is_file():raise ValueError('unsafe or missing course entry')
        course=json.loads(source.read_text(encoding='utf-8'));id=identifier(course['id'])
        for key in ('title','description','level'):text(course[key])
        for goal in course['objectives']:text(goal['description'])
        if not course['lessons']:raise ValueError('course requires lessons')
        for lesson in course['lessons']:text(lesson['title'])
        if id in ids:raise ValueError('duplicate course identity; no implicit merge')
        ids.add(id);items.append((base,course))
    if len(items)<2:raise ValueError('a collection landing requires at least two courses')
    return items

def preview(course,n):
    first=course['lessons'][0]
    if first.get('kind')=='slides':slide=first['slides'][0]
    else:slide={'type':'content','title':first['title'][:45],'eyebrow':'강의','visual':{'items':[{'label':'학습 목표','text':first['title'][:60]}]},'narration':[],'transcript':first['title'],'objective_ids':first.get('objective_ids',[])}
    return svg(n,slide)

def duration_label(course):
    seconds=course.get('narration_seconds')
    if seconds is None:
        silent=all(l.get('narration')=='none' if l.get('kind')=='slides' else l.get('video',{}).get('narration')=='none' and not l.get('video',{}).get('has_audio') for l in course['lessons'])
        return '무음' if silent else '음성 길이 미기록'
    if type(seconds) not in (int,float) or not math.isfinite(seconds) or seconds<0:raise ValueError('invalid built narration duration')
    if not seconds:return '무음'
    total=math.ceil(seconds);hours,rem=divmod(total,3600);minutes,secs=divmod(rem,60)
    return '음성 '+(f'{hours}시간 ' if hours else '')+(f'{minutes}분 ' if minutes else '')+f'{secs}초'

def build(root,output=None):
    root=root.absolute();output=(output or root/'index.html').absolute()
    if root.resolve()!=root or not root.is_dir() or output.resolve()!=output or output.parent!=root or output.suffix!='.html':raise ValueError('use a safe collection root and an HTML output in that root')
    owned_output(output)
    items=discover(root);cards=[];links=[]
    for n,(base,c) in enumerate(items):
        href=quote((base.relative_to(root)/'index.html').as_posix(),safe='/')
        home=quote(os.path.relpath(output,base),safe='/')
        links.append({'course_id':c['id'],'build_manifest':str(base/'course.json'),'collection_home':home,'rebuild_required':c.get('collection_home')!=home})
        search=' '.join([c['title'],c['description'],*[o['description'] for o in c['objectives']],*[l['title'] for l in c['lessons']]])
        cards.append('<article class="catalog-card" data-catalog-card data-search="'+h(search,quote=True)+'"><a class="catalog-preview" href="'+h(href,quote=True)+'" aria-label="'+h(c['title']+' 코스 열기',quote=True)+'">'+preview(c,n)+'</a><div class="catalog-copy"><h2><a href="'+h(href,quote=True)+'">'+h(c['title'])+'</a></h2><p class="catalog-description">'+h(c['description'])+'</p><p class="catalog-meta"><span>'+h(c['level'])+'</span><span>'+str(len(c['lessons']))+'개 강의</span><span>'+h(duration_label(c))+'</span></p></div></article>')
    css=theme_styles('',ASSETS)+'\n'+(ASSETS/'catalog.css').read_text();js=(ASSETS/'html-theme.js').read_text()
    search_js=(ASSETS/'catalog.js').read_text()
    page='<!doctype html><html lang="ko" data-default-theme="system"><head><meta charset="utf-8"><meta name="'+MARKER+'" content="1"><meta name="viewport" content="width=device-width,initial-scale=1"><title>학습 코스</title><script>'+BOOTSTRAP+'</script><style>'+css+'</style></head><body class="course-catalog"><header class="ht-topbar"><p class="ht-topbar-title">학습 코스</p><div class="ht-document-actions">'+THEME_CONTROL+'</div></header><main class="catalog-home"><h1 class="ht-visually-hidden">학습 코스</h1><div id="catalog-search-controls" hidden><label for="catalog-search">코스와 강의 검색</label><input id="catalog-search" type="search" placeholder="제목, 설명, 학습 목표, 강의 제목으로 검색" autocomplete="off"><p id="catalog-count" role="status" aria-live="polite"></p></div><div class="catalog-results"><div class="catalog-grid">'+''.join(cards)+'</div><section id="catalog-empty" aria-labelledby="catalog-empty-title" hidden><h2 id="catalog-empty-title">검색 결과가 없습니다.</h2><p>다른 단어로 검색하거나 검색어를 지워 보세요.</p><button id="catalog-clear" type="button">검색어 지우기</button></section></div></main><script>'+js+'</script><script>'+search_js+'</script></body></html>'
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=root,prefix='.course-catalog-',suffix='.tmp',delete=False) as f:temporary=Path(f.name);f.write(page)
        # Repeat ownership checks immediately before the atomic replacement.
        if output.resolve()!=output:raise ValueError('unsafe catalog output')
        owned_output(output);os.replace(temporary,output)
    finally:
        if temporary and temporary.exists():temporary.unlink()
    return {'path':str(output),'courses':len(items),'progress':'owned by each course; not copied into the catalog','course_links':links,'link_hint':'돌아가기 링크가 필요한 코스는 원본 course.json으로 새 출력 폴더에 --collection-home 값을 지정해 다시 빌드하세요.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True,type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    try:print(json.dumps(build(a.root,a.output),ensure_ascii=False))
    except (ValueError,OSError,KeyError,TypeError,IndexError) as e:print(json.dumps({'status':'failed','detail':str(e)},ensure_ascii=False));raise SystemExit(1)
