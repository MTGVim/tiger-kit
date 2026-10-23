#!/usr/bin/env python3
"""Build or refresh an optional offline gallery for sibling courses."""
import argparse,json,math,os,tempfile,zipfile
from pathlib import Path
from html import escape as h
from html.parser import HTMLParser
from urllib.parse import quote
from app_shell import THEME_CONTROL,BOOTSTRAP,theme_styles
from build_course import identifier,text,ASSETS
from components import svg
from distribution import safe_path,read_manifest,atomic_text

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

def validate_metadata(course):
    identifier(course['id']);text(course['revision'],120)
    for key in ('title','description','level'):text(course[key])
    if not course['objectives']:raise ValueError('missing course objectives')
    for goal in course['objectives']:text(goal['description'])
    if not isinstance(course['lessons'],list) or not 1<=len(course['lessons'])<=200:raise ValueError('course requires lessons')
    for lesson in course['lessons']:identifier(lesson['id']);text(lesson['title'])
    duration_label(course)
    # Render through the fixed SVG components; never trust arbitrary manifest HTML.
    preview(course,0)
    return course

def discover(root):
    items=[];ids=set()
    for entry in sorted(root.iterdir()):
        if entry.is_symlink():raise ValueError('symlinked distribution entry')
        if not entry.is_dir():continue
        index=entry/'index.html'
        course=validate_metadata(read_manifest(index));id=course['id']
        if id in ids:raise ValueError('duplicate course identity; no implicit merge')
        ids.add(id);items.append((entry,course))
    return items

def preview(course,n):
    first=course['lessons'][0]
    if course.get('preview_slide') is not None:slide=course['preview_slide']
    elif first.get('slides'):slide=first['slides'][0]
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

def build(root,output=None,*,zip_output=False):
    root=root.absolute();output=(output or root/'index.html').absolute()
    if root.resolve()!=root or not root.is_dir() or output.resolve()!=output or output.parent!=root or output.suffix!='.html':raise ValueError('use a safe collection root and an HTML output in that root')
    owned_output(output)
    items=discover(root)
    if not items:raise ValueError('a collection landing requires at least one course')
    archive=root.parent/(root.name+'.zip')
    if zip_output:check_archive(archive)
    cards=[];links=[]
    for n,(base,c) in enumerate(items):
        href=quote((base.relative_to(root)/'index.html').as_posix(),safe='/')
        home=quote(os.path.relpath(output,base),safe='/')
        links.append({'course_id':c['id'],'path':str(base/'index.html'),'collection_home':home})
        search=' '.join([c['title'],c['description'],*[o['description'] for o in c['objectives']],*[l['title'] for l in c['lessons']]])
        cards.append('<article class="catalog-card" data-catalog-card data-search="'+h(search,quote=True)+'"><a class="catalog-preview" href="'+h(href,quote=True)+'" aria-label="'+h(c['title']+' 코스 열기',quote=True)+'">'+preview(c,n)+'</a><div class="catalog-copy"><h2><a href="'+h(href,quote=True)+'">'+h(c['title'])+'</a></h2><p class="catalog-description">'+h(c['description'])+'</p><p class="catalog-meta"><span>'+h(c['level'])+'</span><span>'+str(len(c['lessons']))+'개 강의</span><span>'+h(duration_label(c))+'</span></p></div></article>')
    css=theme_styles('',ASSETS)+'\n'+(ASSETS/'catalog.css').read_text();js=(ASSETS/'html-theme.js').read_text()
    search_js=(ASSETS/'catalog.js').read_text()
    probe_js="window.addEventListener('message',e=>{if(e.source===window.parent&&e.data?.type==='tigerkit-catalog-probe')window.parent.postMessage({type:'tigerkit-catalog-ready',token:e.data.token,ids:"+json.dumps([c['id'] for _,c in items])+"},'*');});"
    page='<!doctype html><html lang="ko" data-default-theme="system"><head><meta charset="utf-8"><meta name="'+MARKER+'" content="1"><meta name="viewport" content="width=device-width,initial-scale=1"><title>학습 코스</title><script>'+BOOTSTRAP+'</script><style>'+css+'</style></head><body class="course-catalog"><header class="ht-topbar"><p class="ht-topbar-title">학습 코스</p><div class="ht-document-actions">'+THEME_CONTROL+'</div></header><main class="catalog-home"><h1 class="ht-visually-hidden">학습 코스</h1><div id="catalog-search-controls" hidden><label for="catalog-search">코스와 강의 검색</label><input id="catalog-search" type="search" placeholder="제목, 설명, 학습 목표, 강의 제목으로 검색" autocomplete="off"><p id="catalog-count" role="status" aria-live="polite"></p></div><div class="catalog-results"><div class="catalog-grid">'+''.join(cards)+'</div><section id="catalog-empty" aria-labelledby="catalog-empty-title" hidden><h2 id="catalog-empty-title">검색 결과가 없습니다.</h2><p>다른 단어로 검색하거나 검색어를 지워 보세요.</p><button id="catalog-clear" type="button">검색어 지우기</button></section></div></main><script>'+js+'</script><script>'+search_js+'</script><script>'+probe_js+'</script></body></html>'
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=root,prefix='.course-catalog-',suffix='.tmp',delete=False) as f:temporary=Path(f.name);f.write(page)
        # Repeat ownership checks immediately before the atomic replacement.
        if output.resolve()!=output:raise ValueError('unsafe catalog output')
        owned_output(output);os.replace(temporary,output)
    finally:
        if temporary and temporary.exists():temporary.unlink()
    result={'path':str(output),'courses':len(items),'progress':'owned by each course; not copied into the catalog','course_links':links}
    if zip_output:
        check_archive(archive);temporary=None
        try:
            with tempfile.NamedTemporaryFile(dir=archive.parent,prefix='.course-zip-',suffix='.tmp',delete=False) as f:temporary=Path(f.name)
            with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as z:
                z.comment=ZIP_MARKER
                for path in [output,*[base/'index.html' for base,_ in items]]:
                    safe_path(path);z.write(path,path.relative_to(root).as_posix())
            check_archive(archive);os.replace(temporary,archive)
        finally:
            if temporary and temporary.exists():temporary.unlink()
        result['zip']={'path':str(archive),'bytes':archive.stat().st_size,'courses':[c['title'] for _,c in items]}
    return result

ZIP_MARKER=b'tigerkit-course-distribution:1'
def check_archive(path):
    safe_path(path)
    if not path.exists():return
    if not path.is_file() or not zipfile.is_zipfile(path):raise ValueError('refusing to replace an unmarked archive')
    with zipfile.ZipFile(path) as z:
        if z.comment!=ZIP_MARKER:raise ValueError('refusing to replace an unmarked archive')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('courses'));p.add_argument('--dist',type=Path);p.add_argument('--output',type=Path);p.add_argument('--zip',action='store_true');a=p.parse_args()
    try:print(json.dumps(build(a.dist or a.root/'dist',a.output,zip_output=a.zip),ensure_ascii=False))
    except (ValueError,OSError,KeyError,TypeError,IndexError) as e:print(json.dumps({'status':'failed','detail':str(e)},ensure_ascii=False));raise SystemExit(1)
