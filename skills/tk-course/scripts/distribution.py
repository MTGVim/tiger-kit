"""Bounded embedded catalog metadata and safe distribution-tree operations."""
import json,os,re,tempfile
from datetime import date
from pathlib import Path
from html.parser import HTMLParser

MANIFEST_ID='tigerkit-course-manifest'
LIMIT=65536

def course_dates(course):
    for key in ('created_at','updated_at'):
        if key in course:
            value=course[key]
            if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):raise ValueError('invalid course '+key)
            try:date.fromisoformat(value)
            except ValueError as exc:raise ValueError('invalid course '+key) from exc
    if course.get('created_at') and course.get('updated_at') and course['updated_at']<course['created_at']:raise ValueError('updated_at precedes created_at')

def date_label(course):
    course_dates(course)
    created=course.get('created_at');updated=course.get('updated_at')
    return ('등록 '+created if created else '')+(' · ' if created and updated and updated!=created else '')+('업데이트 '+updated if updated and updated!=created else '')
class Manifest(HTMLParser):
    def __init__(self):super().__init__();self.capture=False;self.complete=False;self.parts=[];self.count=0
    def handle_starttag(self,tag,attrs):
        if tag=='script' and dict(attrs).get('id')==MANIFEST_ID:
            self.capture=True;self.count+=1
            if dict(attrs).get('type')!='application/json':raise ValueError('invalid course manifest type')
    def handle_data(self,data):
        if self.capture:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.capture:self.capture=False;self.complete=True

def safe_path(path):
    path=path.absolute()
    if path.resolve()!=path:raise ValueError('symlinked distribution path is not allowed')
    return path

def read_manifest(path):
    path=safe_path(path)
    if not path.is_file():raise ValueError('missing course index.html')
    with path.open('rb') as f:prefix=f.read(LIMIT)
    parser=Manifest();parser.feed(prefix.decode('utf-8',errors='ignore'))
    if not parser.complete or parser.count!=1:raise ValueError('missing or oversized embedded course manifest (first 64KB)')
    value=json.loads(''.join(parser.parts))
    if not isinstance(value,dict) or type(value.get('schema')) is not int or value.get('schema')!=1:raise ValueError('invalid embedded course manifest schema')
    return value

def embedded_manifest(course):
    first=course['lessons'][0]
    preview=None
    if first['kind']=='slides':
        preview={k:v for k,v in first['slides'][0].items() if k!='narration'}
        preview['narration']=[]
    if course.get('preview_slide'):
        ref=course['preview_slide']
        lesson=next(l for l in course['lessons'] if l['id']==ref['lesson_id'])
        preview={k:v for k,v in next(s for s in lesson['slides'] if s['id']==ref['slide_id']).items() if k!='narration'}
        preview['narration']=[]
    if preview and preview['type']=='image':
        preview={**preview,'type':'content','visual':{'items':[{'label':'학습 화면','text':preview['visual']['description'][:60]}]}}
    value={k:course[k] for k in ('id','title','description','level','revision','objectives','narration_seconds')}
    value.update({k:course[k] for k in ('created_at','updated_at') if k in course})
    value.update(schema=1,lessons=[{'id':l['id'],'title':l['title'],'kind':l['kind'],'narration':l.get('narration','none')} for l in course['lessons']],preview_slide=preview)
    tag='<script type="application/json" id="'+MANIFEST_ID+'">'+json.dumps(value,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    if len(tag.encode())>LIMIT-1024:raise ValueError('course catalog metadata exceeds the first 64KB budget; shorten descriptions')
    return tag

def atomic_text(path,content):
    path=safe_path(path);temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,prefix='.course-',suffix='.tmp',delete=False) as f:
            temporary=Path(f.name);f.write(content)
        safe_path(path);os.replace(temporary,path)
    finally:
        if temporary and temporary.exists():temporary.unlink()
