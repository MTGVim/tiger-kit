#!/usr/bin/env python3
"""Validate authored course data and build a local self-contained HTML course."""
from __future__ import annotations
import argparse,base64,copy,hashlib,json,math,re,shutil,subprocess,tempfile,wave
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from render_page import render

ID=re.compile(r'[a-z0-9][a-z0-9-]{0,79}')
ASSETS=Path(__file__).resolve().parents[1]/'assets'
def identifier(value):
    if not isinstance(value,str) or not ID.fullmatch(value):raise ValueError('invalid stable ID')
    return value

def text(value,limit=10000):
    if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError('missing or oversized authored text')
    return value

def collection_path(value):
    if value is None:return None
    text(value,2000)
    decoded=unquote(value);url=urlsplit(value)
    if url.scheme or url.netloc or url.query or url.fragment or decoded.startswith('/') or '\\' in decoded or ':' in decoded or any(ord(c)<32 for c in decoded) or any(ord(c)<33 for c in value):
        raise ValueError('collection home must be a relative HTML path')
    if not decoded.endswith('.html'):raise ValueError('collection home must be a relative HTML path')
    return value

def check_header(page,title):
    class Header(HTMLParser):
        def __init__(self):super().__init__();self.inside=False;self.parts=[]
        def handle_starttag(self,tag,attrs):
            if tag=='header':self.inside=True
        def handle_endtag(self,tag):
            if tag=='header':self.inside=False
        def handle_data(self,data):
            if self.inside:self.parts.append(' '.join(data.split()))
    parser=Header();parser.feed(page)
    if parser.parts.count(' '.join(title.split()))!=1:raise ValueError('course title must occur once in the page header')

def check_visible_objectives(page,objectives):
    class SvgText(HTMLParser):
        def __init__(self):super().__init__();self.inside=False;self.value=''
        def handle_starttag(self,tag,attrs):
            if tag=='text':self.inside=True;self.value=''
        def handle_data(self,data):
            if self.inside:self.value+=data
        def handle_endtag(self,tag):
            if tag=='text':
                if any(re.search(r'(?<![a-z0-9-])'+re.escape(id)+r'(?![a-z0-9-])',self.value) for id in objectives):
                    raise ValueError('internal objective ID leaked into visible SVG text')
                self.inside=False
    SvgText().feed(page)

def narration_seconds(course,base):
    total=0
    for lesson in course['lessons']:
        if lesson['kind']=='video':
            if lesson['video']['has_audio']:total+=lesson['video']['duration']
        elif lesson['narration']=='generated':
            for slide in lesson['slides']:
                for cue in slide['narration']:
                    with wave.open(str(safe_file(base,cue['audio'])),'rb') as wav:total+=wav.getnframes()/wav.getframerate()
    return round(total,3)

def safe_file(base,name):
    if not isinstance(name,str) or not name or '\\' in name:raise ValueError('invalid local media path')
    q=Path(name)
    if q.is_absolute() or '..' in q.parts:raise ValueError('media must stay inside the authored course directory')
    p=base/q
    if p.resolve()!=p.absolute() or not p.is_file():raise ValueError('media must be a regular nonsymlink file')
    return p

def media_uri(base,name,kind):
    path=safe_file(base,name)
    mime={'.wav':'audio/wav','.mp4':'video/mp4','.webm':'video/webm','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'}.get(path.suffix.lower())
    if not mime or not mime.startswith(kind+'/'):raise ValueError('unsupported media file type')
    if path.stat().st_size>500_000_000:raise ValueError('media exceeds the single-file build budget; split the course')
    if kind=='audio':
        with wave.open(str(path),'rb') as wav:
            if wav.getnchannels()!=1 or wav.getnframes()<1 or wav.getsampwidth()!=2:raise ValueError('expected nonempty mono PCM16 narration WAV')
            if not any(wav.readframes(wav.getnframes())):raise ValueError('silent narration WAV')
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()

def fingerprint(lesson,course,base):
    # Renaming and reordering preserve learning content; substantive edits require a new revision.
    content={k:v for k,v in lesson.items() if k not in {'id','title','section','revision','prerequisites','content_fingerprint'}}
    content['outcomes']={o['id']:o['description'] for o in course['objectives'] if o['id'] in lesson['objective_ids']}
    media=media_paths(lesson)
    content['media_sha256']={}
    for name in media:
        with safe_file(base,name).open('rb') as stream:content['media_sha256'][name]=hashlib.file_digest(stream,'sha256').hexdigest()
    return hashlib.sha256(json.dumps(content,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def media_paths(lesson):
    if lesson['kind']=='video':return [lesson['video'][k] for k in ('src','poster') if lesson['video'].get(k)]
    return sorted({c['audio'] for s in lesson['slides'] for c in s['narration'] if c.get('audio')})

def validate(course,base):
    if not isinstance(course,dict) or course.get('schema')!=1:raise ValueError('unsupported course schema')
    identifier(course['id']);text(course['title'],120);text(course['revision'],120);text(course['description']);text(course['level'],100)
    objectives=course['objectives'];known={identifier(o['id']) for o in objectives}
    if not known or len(known)!=len(objectives):raise ValueError('duplicate or missing objective')
    for o in objectives:text(o['description'])
    lessons=course['lessons']
    if not isinstance(lessons,list) or not 1<=len(lessons)<=200:raise ValueError('course requires 1-200 lessons')
    ids=[identifier(l['id']) for l in lessons]
    if len(set(ids))!=len(ids):raise ValueError('duplicate lesson ID')
    covered=set();tested=set();prior=set()
    for lesson in lessons:
        text(lesson['title'],120);text(lesson['revision'],120);text(lesson['section'],100);text(lesson['notes'])
        deps=lesson.get('prerequisites',[])
        if not isinstance(deps,list) or len(set(deps))!=len(deps) or not set(deps)<=prior:raise ValueError('prerequisites must reference earlier lessons')
        prior.add(lesson['id'])
        if not lesson.get('objective_ids') or not set(lesson['objective_ids'])<=known:raise ValueError('unknown lesson objective')
        covered.update(lesson['objective_ids'])
        questions=lesson['questions'];qids=set()
        for q in questions:
            identifier(q['id']);text(q['prompt']);text(q['explanation']);choices=q['choices']
            if q['id'] in qids or not 2<=len(choices)<=6 or len({x[0] for x in choices})!=len(choices):raise ValueError('invalid question choices')
            qids.add(q['id'])
            for key,label in choices:identifier(key);text(label)
            if q['answer'] not in {x[0] for x in choices} or not set(q['objective_ids'])<=set(lesson['objective_ids']):raise ValueError('question answer/objective mismatch')
            tested.update(q['objective_ids'])
        if lesson['kind']=='slides':
            slides=lesson['slides'];sids=set();cids=set()
            if not isinstance(slides,list) or not 1<=len(slides)<=200:raise ValueError('missing slides')
            for slide in slides:
                identifier(slide['id']);text(slide['title'],45);text(slide.get('eyebrow',' '),100)
                if slide['id'] in sids:raise ValueError('duplicate slide ID')
                sids.add(slide['id']);cues=slide['narration']
                if not cues or not set(slide['objective_ids'])<=set(lesson['objective_ids']):raise ValueError('missing cues or invalid slide objectives')
                if slide['transcript']!=' '.join(c['caption'] for c in cues):raise ValueError('caption/transcript mismatch')
                if slide['type']=='content':
                    items=slide['visual']['items']
                    if not 1<=len(items)<=4:raise ValueError('content component allows 1-4 items')
                    for item in items:text(item['label'],36);text(item['text'],60)
                    targets={'item-'+str(i+1) for i in range(len(items))}
                else:
                    targets={'hook':{'first-search','latest-search'},'timeline':{'request-a','request-b','response-b','response-a','overwrite'},'code':{'request-id','await','compare','render','takeaway'},'comparison':{'cancel','guard','caveats'},'prediction':{'request-order','response-order','predict','practice'}}.get(slide['type'])
                    if targets is None:raise ValueError('unsupported component')
                    # The bounded legacy components retain their authored slot checks below.
                    legacy_slots(slide)
                focused=set();attached=[]
                for cue in cues:
                    identifier(cue['id']);text(cue['speech']);text(cue['caption'])
                    if cue['id'] in cids:raise ValueError('duplicate cue ID')
                    cids.add(cue['id'])
                    focus=cue.get('focus',[])
                    if not isinstance(focus,list) or len(set(focus))!=len(focus) or not set(focus)<=targets:raise ValueError('invalid cue visual reference')
                    focused.update(focus);attached.append(bool(cue.get('audio')))
                    if cue.get('audio'):media_uri(base,cue['audio'],'audio')
                if focused!=targets:raise ValueError('visual elements lack a narration cue')
                if any(attached) and not all(attached):raise ValueError('partial generated narration')
            voice=lesson.get('narration')
            if voice not in {'generated','none'}:raise ValueError('explicit narration choice required')
            if voice=='generated' and not all(c.get('audio') for s in slides for c in s['narration']):raise ValueError('selected generated narration is missing; synthesize or explicitly choose none')
        elif lesson['kind']=='video':
            video=lesson['video'];path=safe_file(base,video['src'])
            if path.suffix not in {'.mp4','.webm'}:raise ValueError('finished MP4/WebM required')
            probe=shutil.which('ffprobe')
            if not probe:raise ValueError('ffprobe is required to verify selected video')
            result=subprocess.run([probe,'-v','error','-show_format','-show_streams','-of','json',str(path)],capture_output=True,text=True,check=True)
            info=json.loads(result.stdout);duration=float(info['format']['duration'])
            if not math.isfinite(duration) or duration<=0 or not any(s.get('codec_type')=='video' for s in info['streams']):raise ValueError('invalid finished video')
            has_audio=any(s.get('codec_type')=='audio' for s in info['streams'])
            if video.get('narration') not in {'embedded','none'}:raise ValueError('explicit embedded/none video narration choice required')
            if video['narration']=='embedded' and not has_audio:raise ValueError('selected video narration has no audio stream')
            video['duration']=duration;video['has_audio']=has_audio
            previous=0
            for cue in video['captions']:
                identifier(cue['id']);text(cue['caption'])
                if not all(type(cue[k]) in (int,float) and math.isfinite(cue[k]) for k in ['start','end']) or not previous<=cue['start']<cue['end']<=duration+.05:raise ValueError('video caption timeline mismatch')
                previous=cue['end']
            if not video['captions']:raise ValueError('video requires captions and transcript')
            if video.get('poster'):media_uri(base,video['poster'],'image')
        else:raise ValueError('unknown lesson media kind')
    if covered!=known or tested!=known:raise ValueError('learning outcomes lack teaching or assessment')
    if not course.get('sources'):raise ValueError('course requires source provenance')
    for source in course['sources']:
        text(source['title']);url=source.get('url')
        if url is None:
            safe_file(base,source['local'])
        elif not isinstance(url,str) or not re.match(r'https://[^\s<>"\x00-\x20]+$',url):raise ValueError('invalid source link')
    return course

def legacy_slots(slide):
    kind=slide['type'];v=slide['visual']
    def short(x,n):text(x,n)
    if kind=='hook':
        if len(v['title_lines'])!=2 or len(v['cards'])!=2:raise ValueError('hook slots')
        for row in v['title_lines']:short(row,24)
        for c in v['cards']:short(c['label'],18);short(c['value'],3)
        short(v['question'],55)
    elif kind=='timeline':
        if len(v['lanes'])!=2 or len(v['events'])!=4:raise ValueError('timeline slots')
        for x in v['lanes']+v['events']:short(x,10)
        short(v['callout'],60)
    elif kind=='code':
        if len(slide['code'])>6 or any(len(x)>70 for x in slide['code']):raise ValueError('code slots')
        short(v['footnote'],60)
    elif kind=='comparison':
        if len(v['cards'])!=2:raise ValueError('comparison slots')
        for c in v['cards']:short(c['title'],18);short(c['tag'],25);short(c['copy'],30)
        short(v['footnote'],60)
    elif kind=='prediction':
        if len(v['rows'])!=2:raise ValueError('prediction slots')
        for row in v['rows']:short(row['label'],10);short(row['sequence'],24)
        short(v['question'],55);short(v['hint'],55)

def payload(course,lesson,base):
    data=copy.deepcopy(lesson)
    meta={'id':course['id'],'revision':course['revision'],'lessons':[{'id':x['id'],'revision':x['revision']} for x in course['lessons']]}
    listing=[{'id':x['id'],'title':x['title'],'section':x['section'],'kind':x['kind'],'kind_label':('슬라이드 '+str(len(x['slides']))+'장') if x['kind']=='slides' else '영상'} for x in course['lessons']]
    mode=lesson['kind'];dummy={'id':'video-cover','title':lesson['title'][:45],'eyebrow':'강의','type':'content','objective_ids':lesson['objective_ids'],'visual':{'items':[{'label':'학습 목표','text':lesson['title'][:60]}]},'narration':[{'id':'cover','speech':lesson['title'],'caption':lesson['title'],'focus':['item-1']}],'transcript':lesson['title']}
    slides=data['slides'] if mode=='slides' else [copy.deepcopy(dummy) for _ in lesson['video']['captions']]
    for slide in slides:
        for cue in slide['narration']:
            if cue.get('audio'):cue['audio']=media_uri(base,cue['audio'],'audio')
    video={'src':'','duration':1,'has_audio':False};scenes=[{'id':'unused','caption':'','start':0,'end':1}]
    if mode=='video':
        video={**lesson['video'],'src':media_uri(base,lesson['video']['src'],'video')}
        if video.get('poster'):video['poster']=media_uri(base,video['poster'],'image')
        scenes=copy.deepcopy(video['captions'])
    data.update(sources=copy.deepcopy(course['sources']),title=course['title'],course_label=course['title'],lesson_id=lesson['id'],lesson_title=lesson['title'],course_meta=meta,course_lessons=listing,overview={'description':course['description'],'level':course['level'],'outcomes':[o['description'] for o in course['objectives']]},slides=slides,lessons=[{'id':mode,'title':lesson['title'],'note':lesson['notes']}],published_lessons=[mode],video_lesson=video,video_scenes=scenes,video_transcript=' '.join(x['caption'] for x in scenes),production_choices={'voice':'none' if lesson.get('narration')=='none' else 'generated-local','pacing':{'slidePauseMs':1200,'sentencePauseMs':600}},narration_revision=lesson['revision'])
    return data

def bundle(pages,title,course):
    encoded=json.dumps(pages,ensure_ascii=False).replace('<','\\u003c')
    bootstrap="""const pages=JSON.parse(document.getElementById('course-pages').textContent),ids=Object.keys(pages),frame=document.getElementById('course-frame');let entering=false;function show(id,enter){if(!Object.hasOwn(pages,id))return;entering=enter;frame.srcdoc=pages[id];}frame.addEventListener('load',()=>{if(entering)frame.contentWindow.postMessage({type:'course-enter'},'*');});window.addEventListener('message',e=>{if(e.source!==frame.contentWindow||e.data?.type!=='course-lesson'||!ids.includes(e.data.id))return;show(e.data.id,true);});show(ids[0],false);"""
    fallback=('<a href="'+escape(course['collection_home'],quote=True)+'">← 전체 코스</a>') if course.get('collection_home') else ''
    for lesson in course['lessons']:
        fallback+='<section><h2>'+escape(lesson['title'])+'</h2><p>'+escape(lesson['notes'])+'</p>'
        for slide in lesson.get('slides',[]):fallback+='<h3>'+escape(slide['title'])+'</h3><p>'+escape(slide['transcript'])+'</p>'
        if lesson['kind']=='video':
            match=re.search(r'<video id="lesson-video"[^>]*>',pages[lesson['id']])
            if match:fallback+=match[0]+'</video>'
            fallback+=''.join('<p>'+escape(c['caption'])+'</p>' for c in lesson['video']['captions'])
        for q in lesson['questions']:
            fallback+='<article><h3>'+escape(q['prompt'])+'</h3><ul>'+''.join('<li>'+escape(choice[1])+'</li>' for choice in q['choices'])+'</ul><details><summary>해설 보기</summary><p>'+escape(q['explanation'])+'</p></details></article>'
        fallback+='</section>'
    fallback+='<section><h2>참고 자료</h2><ul>'+''.join('<li>'+('<a href="'+escape(item['url'],quote=True)+'">'+escape(item['title'])+'</a>' if item.get('url') else escape(item['title'])+' (제공 자료)')+'</li>' for item in course['sources'])+'</ul></section>'
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>html,body{margin:0;height:100%;overflow:hidden}iframe{display:block;width:100%;height:100dvh;border:0}</style><iframe id="course-frame" title="'+escape(title,quote=True)+'" allow="fullscreen" allowfullscreen></iframe><noscript><style>html,body{overflow:auto}iframe{display:none}</style>'+fallback+'</noscript><script id="course-pages" type="application/json">'+encoded+'</script><script>'+bootstrap+'</script></html>'

def build(source,output,previous=None,collection_home=None):
    source=source.absolute();output=output.absolute()
    if source.resolve()!=source or not source.is_file() or output.resolve()!=output or output.exists() or not output.parent.is_dir():raise ValueError('use safe authored input and a new output directory')
    collection_home=collection_path(collection_home)
    course=validate(json.loads(source.read_text()),source.parent);changes=[]
    course['collection_home']=collection_home;course['narration_seconds']=narration_seconds(course,source.parent)
    fingerprints={item['id']:fingerprint(item,course,source.parent) for item in course['lessons']}
    if previous:
        old=json.loads(previous.read_text())
        if old['id']!=course['id']:raise ValueError('course identity changed; do not merge progress implicitly')
        prior={x['id']:x for x in old['lessons']}
        for item in course['lessons']:
            before=prior.get(item['id'])
            old_fingerprint=None
            if before:
                old_fingerprint=before.get('content_fingerprint')
                if old_fingerprint is None:
                    if media_paths(before):raise ValueError('previous media identity is unavailable; use the prior built course.json with recorded digests')
                    old_fingerprint=fingerprint(before,old,previous.parent)
                if old_fingerprint!=fingerprints[item['id']] and before['revision']==item['revision']:raise ValueError('substantive lesson change requires a new content revision')
            changes.append({'id':item['id'],'status':'added' if before is None else 'changed' if old_fingerprint!=fingerprints[item['id']] else 'retained'})
        changes += [{'id':x,'status':'removed; historical progress is retained'} for x in prior if x not in {l['id'] for l in course['lessons']}]
    for item in course['lessons']:item['content_fingerprint']=fingerprints[item['id']]
    pages={l['id']:render({**payload(course,l,source.parent),'collection_home':collection_home}) for l in course['lessons']}
    for key,page in pages.items():
        check_header(page,course['title'])
        check_visible_objectives(page,[o['id'] for o in course['objectives']])
        if '비동기 검색' in page and '비동기 검색' not in json.dumps(course,ensure_ascii=False):raise ValueError('fixture content leaked into generic course')
    with tempfile.TemporaryDirectory(prefix='.course-build-',dir=output.parent) as tmp:
        stage=Path(tmp)/'course';stage.mkdir()
        (stage/'index.html').write_text(bundle(pages,course['title'],course))
        (stage/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
        (stage/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
        # Individual pages provide direct access as well as the single-file bundle.
        for key,page in pages.items():(stage/('lesson-'+key+'.html')).write_text(page)
        stage.rename(output)
    return {'path':str(output/'index.html'),'lessons':len(pages),'narration':'selected per lesson; runtime listening remains required','browser_verification':'pending','collection_hint':'코스가 2개 이상이면 build_catalog.py로 전체 홈을 만들 수 있습니다.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--previous',type=Path);p.add_argument('--collection-home');a=p.parse_args()
    try:print(json.dumps(build(a.input,a.output,a.previous,a.collection_home),ensure_ascii=False));return 0
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as e:print(json.dumps({'status':'failed','detail':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
