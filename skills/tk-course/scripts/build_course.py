#!/usr/bin/env python3
"""Validate authored course data and build a local self-contained HTML course."""
from __future__ import annotations
import argparse,base64,copy,hashlib,json,math,re,shutil,subprocess,tempfile,warnings,wave
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from datetime import datetime
from render_page import render
from audio_media import MIME,inspect_audio,AudioBuild
from distribution import embedded_manifest,safe_path,read_manifest,atomic_text,course_dates
from slide_components import TYPES,contract as figure_contract,table as figure_table
from readiness import validate_readiness,readiness_html

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
                    total+=inspect_audio(safe_file(base,cue['audio']))
    return round(total,3)

def safe_file(base,name):
    if not isinstance(name,str) or not name or '\\' in name:raise ValueError('invalid local media path')
    q=Path(name)
    if q.is_absolute() or '..' in q.parts:raise ValueError('media must stay inside the authored course directory')
    p=base/q
    if p.resolve()!=p.absolute() or not p.is_file():raise ValueError('media must be a regular nonsymlink file')
    return p

def media_uri(base,name,kind,audio_build=None):
    path=safe_file(base,name)
    mime=(MIME if kind=='audio' else {'.mp4':'video/mp4','.webm':'video/webm','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'}).get(path.suffix.lower())
    if not mime or not mime.startswith(kind+'/'):raise ValueError('unsupported media file type')
    if path.stat().st_size>500_000_000:raise ValueError('media exceeds the single-file build budget; split the course')
    if kind=='audio':
        if audio_build:return audio_build.uris[name]
        inspect_audio(path)
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
    return sorted({c['audio'] for s in lesson['slides'] for c in s['narration'] if c.get('audio')}|{s['visual']['src'] for s in lesson['slides'] if s['type']=='image'})

def course_pacing(course):
    value=course.get('pacing')
    defaults={'initialLeadInMs':5000,'postSlideHoldMs':1800,'slidePauseMs':1200,'sentencePauseMs':600}
    if 'pacing' not in course:return defaults
    if not isinstance(value,dict) or set(value)-set(defaults):raise ValueError('invalid pacing fields')
    if any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=5000 for v in value.values()):raise ValueError('invalid pacing range')
    # An authored legacy slide/sentence pause keeps its original, immediate-first-play meaning.
    return {**defaults,'initialLeadInMs':0,'postSlideHoldMs':0,**value}

def validate(course,base):
    if not isinstance(course,dict) or course.get('schema')!=1:raise ValueError('unsupported course schema')
    course_pacing(course)
    identifier(course['id']);text(course['title'],120);text(course['revision'],120);text(course['description']);text(course['level'],100)
    objectives=course['objectives'];known={identifier(o['id']) for o in objectives}
    if not known or len(known)!=len(objectives):raise ValueError('duplicate or missing objective')
    for o in objectives:text(o['description'])
    validate_readiness(course,identifier,text)
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
                elif slide['type'] in TYPES:
                    targets,coverage=figure_contract(slide)
                    if slide['type']=='image':image_info(base,slide['visual']['src'])
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
                    if cue.get('audio'):inspect_audio(safe_file(base,cue['audio']))
                if slide['type'] in TYPES:
                    if any(not focused&alternatives for alternatives in coverage):raise ValueError('visual elements lack a narration cue')
                elif focused!=targets:raise ValueError('visual elements lack a narration cue')
                if any(attached) and not all(attached):raise ValueError('partial generated narration')
                # Preflight geometry before creating output or transcoding media.
                from components import svg
                layout=copy.deepcopy(slide)
                if slide['type']=='image':layout['visual']['aspect_ratio']=image_info(base,slide['visual']['src'])
                svg(0,layout)
            voice=lesson.get('narration')
            if voice not in {'generated','none'}:raise ValueError('explicit narration choice required')
            if voice=='generated' and not all(c.get('audio') for s in slides for c in s['narration']):raise ValueError('selected generated narration is missing; synthesize or explicitly choose none')
            if slides[-1].get('role') not in {'summary','closing'}:
                warnings.warn('lesson '+lesson['id']+' lacks a final summary/closing role; review its greeting, connection, goal and ending',UserWarning,stacklevel=2)
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
    preview=course.get('preview_slide')
    if preview is not None:
        if not isinstance(preview,dict) or set(preview)!={'lesson_id','slide_id'}:raise ValueError('preview_slide requires lesson_id and slide_id')
        if not any(l['id']==preview['lesson_id'] and l['kind']=='slides' and any(s['id']==preview['slide_id'] for s in l['slides']) for l in lessons):raise ValueError('unknown preview_slide reference')
    slide_lessons=[l for l in lessons if l['kind']=='slides']
    for previous,current in zip(slide_lessons,slide_lessons[1:]):
        if previous['slides'][0]['type']==current['slides'][0]['type']:
            warnings.warn('consecutive lesson openings repeat '+current['slides'][0]['type']+'; choose a question-led opening',UserWarning,stacklevel=2)
    return course

def legacy_slots(slide):
    kind=slide['type'];v=slide['visual']
    def short(x,n):text(x,n)
    if kind=='comparison':
        if len(v['cards'])!=2:raise ValueError('comparison slots')
        for c in v['cards']:short(c['title'],18);short(c['tag'],25);short(c['copy'],30)
        short(v['footnote'],60)
    elif kind=='prediction':
        if len(v['rows'])!=2:raise ValueError('prediction slots')
        for row in v['rows']:short(row['label'],10);short(row['sequence'],24)
        short(v['question'],55);short(v['hint'],55)

def image_info(base,name):
    try:from PIL import Image
    except ImportError as error:raise ValueError('Pillow is required for local teaching images') from error
    path=safe_file(base,name)
    expected={'.png':'PNG','.jpg':'JPEG','.jpeg':'JPEG','.webp':'WEBP'}.get(path.suffix.lower())
    if not expected:raise ValueError('unsupported image file type')
    with Image.open(path) as picture:
        if picture.format!=expected:raise ValueError('image encoding does not match file type')
        ratio=picture.width/picture.height;picture.verify()
    return ratio

def embed_visual(slide,base):
    if slide['type']!='image':return slide
    slide=copy.deepcopy(slide)
    slide['visual']['aspect_ratio']=image_info(base,slide['visual']['src'])
    slide['visual']['src']=media_uri(base,slide['visual']['src'],'image')
    return slide

def payload(course,lesson,base,audio_build=None):
    data=copy.deepcopy(lesson)
    meta={'id':course['id'],'revision':course['revision'],'lessons':[{'id':x['id'],'revision':x['revision']} for x in course['lessons']]}
    listing=[{'id':x['id'],'title':x['title'],'section':x['section'],'kind':x['kind'],'kind_label':('슬라이드 '+str(len(x['slides']))+'장') if x['kind']=='slides' else '영상'} for x in course['lessons']]
    mode=lesson['kind'];dummy={'id':'video-cover','title':lesson['title'][:45],'eyebrow':'강의','type':'content','objective_ids':lesson['objective_ids'],'visual':{'items':[{'label':'학습 목표','text':lesson['title'][:60]}]},'narration':[{'id':'cover','speech':lesson['title'],'caption':lesson['title'],'focus':['item-1']}],'transcript':lesson['title']}
    slides=data['slides'] if mode=='slides' else [copy.deepcopy(dummy) for _ in lesson['video']['captions']]
    slides=[embed_visual(slide,base) for slide in slides]
    for slide in slides:
        for cue in slide['narration']:
            if cue.get('audio'):
                if audio_build:cue['seconds']=next(row['seconds'] for row in audio_build.records if row['source']==cue['audio'])
                cue['audio']=media_uri(base,cue['audio'],'audio',audio_build)
    video={'src':'','duration':1,'has_audio':False};scenes=[{'id':'unused','caption':'','start':0,'end':1}]
    if mode=='video':
        video={**lesson['video'],'src':media_uri(base,lesson['video']['src'],'video')}
        if video.get('poster'):video['poster']=media_uri(base,video['poster'],'image')
        scenes=copy.deepcopy(video['captions'])
    data.update(sources=copy.deepcopy(course['sources']),title=course['title'],course_label=course['title'],lesson_id=lesson['id'],lesson_title=lesson['title'],course_meta=meta,course_lessons=listing,overview={'description':course['description'],'level':course['level'],'outcomes':[o['description'] for o in course['objectives']],**{k:course[k] for k in ('created_at','updated_at') if k in course}},slides=slides,lessons=[{'id':mode,'title':lesson['title'],'note':lesson['notes']}],published_lessons=[mode],video_lesson=video,video_scenes=scenes,video_transcript=' '.join(x['caption'] for x in scenes),production_choices={'voice':'none' if lesson.get('narration')=='none' else 'generated-local','pacing':course_pacing(course)},narration_revision=lesson['revision'])
    data['readiness']=copy.deepcopy(course.get('readiness',[]))
    return data

def bundle(pages,title,course,base=None):
    encoded=json.dumps(pages,ensure_ascii=False).replace('<','\\u003c')
    bootstrap="""const pages=JSON.parse(document.getElementById('course-pages').textContent),ids=Object.keys(pages),frame=document.getElementById('course-frame');let entering=false,ui=null;function show(id,enter){if(!Object.hasOwn(pages,id))return;entering=enter;frame.srcdoc=pages[id];}frame.addEventListener('load',()=>{if(entering)frame.contentWindow.postMessage({type:'course-enter',ui},'*');});window.addEventListener('message',e=>{if(e.source!==frame.contentWindow||e.data?.type!=='course-lesson'||!ids.includes(e.data.id))return;ui=e.data.ui;show(e.data.id,true);});show(ids[0],false);"""
    fallback=('<a href="'+escape(course['collection_home'],quote=True)+'">전체 코스</a>') if course.get('collection_home') else ''
    fallback+=readiness_html(course.get('readiness',[]))
    for lesson in course['lessons']:
        fallback+='<section><h2>'+escape(lesson['title'])+'</h2><p>'+escape(lesson['notes'])+'</p>'
        for i,slide in enumerate(lesson.get('slides',[])):
            fallback+='<h3>'+escape(slide['title'])+'</h3><p>'+escape(slide['transcript'])+'</p>'+figure_table(slide)
            if slide['type']=='image' and base is not None:
                from components import svg
                fallback+=svg(i,embed_visual(slide,base)).replace('slide-title-',lesson['id']+'-fallback-title-').replace('slide-desc-',lesson['id']+'-fallback-desc-').replace('slide-'+str(i)+'-',lesson['id']+'-fallback-'+str(i)+'-')
        if lesson['kind']=='video':
            match=re.search(r'<video id="lesson-video"[^>]*>',pages[lesson['id']])
            if match:fallback+=match[0]+'</video>'
            fallback+=''.join('<p>'+escape(c['caption'])+'</p>' for c in lesson['video']['captions'])
        for q in lesson['questions']:
            fallback+='<article><h3>'+escape(q['prompt'])+'</h3><ul>'+''.join('<li>'+escape(choice[1])+'</li>' for choice in q['choices'])+'</ul><details><summary>해설 보기</summary><p>'+escape(q['explanation'])+'</p></details></article>'
        fallback+='</section>'
    fallback+='<section><h2>참고 자료</h2><ul>'+''.join('<li>'+('<a href="'+escape(item['url'],quote=True)+'">'+escape(item['title'])+'</a>' if item.get('url') else escape(item['title'])+' (제공 자료)')+'</li>' for item in course['sources'])+'</ul></section>'
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8">'+embedded_manifest(course)+'<meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>html,body{margin:0;height:100%;overflow:hidden}iframe{display:block;width:100%;height:100dvh;border:0}</style></head><body><iframe id="course-frame" title="'+escape(title,quote=True)+'" allow="fullscreen *" allowfullscreen></iframe><noscript><style>html,body{overflow:auto}iframe{display:none}</style>'+fallback+'</noscript><script id="course-pages" type="application/json">'+encoded+'</script><script>'+bootstrap+'</script></html>'

def build_day():
    return datetime.now().astimezone().date().isoformat()

def build(source,output,previous=None,collection_home=None,*,dist=None,audio_format='opus',lesson_pages=None,catalog_position=None):
    source=source.absolute();output=output.absolute()
    if source.resolve()!=source or not source.is_file() or output.resolve()!=output or output.exists() or not output.parent.is_dir():raise ValueError('use safe authored input and a new output directory')
    # The CLI always passes a distribution root. None preserves the in-process legacy builder API.
    legacy=dist is None
    if lesson_pages is None:lesson_pages=legacy
    shared=None
    if not legacy:
        dist=safe_path(dist)
        if output.is_relative_to(dist) or dist.is_relative_to(output) or source.is_relative_to(dist):raise ValueError('working/source paths must not overlap the distribution tree')
        shared=dist/source.parent.name/'index.html'
        safe_path(shared)
        if shared.exists():raise ValueError('review a new --dist staging tree before replacing an existing shared course')
        if dist.exists() and not dist.is_dir():raise ValueError('distribution root must be a directory')
        if (dist/'index.html').exists():
            from build_catalog import owned_output
            owned_output(dist/'index.html')
        collection_home=collection_home or '../index.html'
    collection_home=collection_path(collection_home)
    course=validate(json.loads(source.read_text()),source.parent);changes=[]
    course['collection_home']=collection_home;course['narration_seconds']=narration_seconds(course,source.parent)
    fingerprints={item['id']:fingerprint(item,course,source.parent) for item in course['lessons']}
    old=None;readiness_changed=False
    if previous:
        safe_path(previous)
        old=json.loads(previous.read_text())
        course_dates(old)
        if old['id']!=course['id']:raise ValueError('course identity changed; do not merge progress implicitly')
        readiness_changed=old.get('readiness',[])!=course.get('readiness',[])
        if readiness_changed and old['revision']==course['revision']:raise ValueError('readiness change requires a new course revision')
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
            changes.append({'id':item['id'],'status':'added' if before is None else 'changed' if old_fingerprint!=fingerprints[item['id']] or before['revision']!=item['revision'] else 'retained'})
        changes += [{'id':x,'status':'removed; historical progress is retained'} for x in prior if x not in {l['id'] for l in course['lessons']}]
    for key in ('created_at','updated_at'):course.pop(key,None)
    if old is None:
        today=build_day();course.update(created_at=today,updated_at=today)
    else:
        for key in ('created_at','updated_at'):
            if key in old:course[key]=old[key]
        if readiness_changed or any(change['status']!='retained' for change in changes):course['updated_at']=build_day()
    course_dates(course)
    settings=None;original_settings=None
    if not legacy:
        from build_catalog import discover,load_settings,place_course
        items=discover(dist) if dist.exists() else []
        if course['id'] in {c['id'] for _,c in items}:raise ValueError('duplicate course identity; no implicit merge')
        settings=load_settings(dist)
        if settings is not None:
            original_settings=(dist/'catalog.json').read_bytes()
            settings=place_course(settings,items,(shared.parent,course),catalog_position)
        elif catalog_position is not None:raise ValueError('--catalog-position requires catalog.json')
    for item in course['lessons']:item['content_fingerprint']=fingerprints[item['id']]
    with tempfile.TemporaryDirectory(prefix='.course-build-',dir=output.parent) as tmp:
        audio=AudioBuild(source.parent,[c['audio'] for l in course['lessons'] if l['kind']=='slides' for slide in l['slides'] for c in slide['narration'] if c.get('audio')],audio_format,tmp)
        course['audio_build']=audio.manifest()
        if not legacy:course['distribution']={'root':str(dist),'topic':source.parent.name}
        pages={l['id']:render({**payload(course,l,source.parent,audio),'collection_home':collection_home}) for l in course['lessons']}
        for page in pages.values():
            check_header(page,course['title']);check_visible_objectives(page,[o['id'] for o in course['objectives']])
            if '비동기 검색' in page and '비동기 검색' not in json.dumps(course,ensure_ascii=False):raise ValueError('fixture content leaked into generic course')
        bundled=bundle(pages,course['title'],course,source.parent)
        stage=Path(tmp)/'course';stage.mkdir()
        if legacy:(stage/'index.html').write_text(bundled)
        (stage/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
        (stage/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
        if lesson_pages:
            direct_home=collection_home
            if not legacy:
                import os
                from urllib.parse import quote
                direct_home=quote(os.path.relpath(dist/'index.html',output),safe='/')
            for l in course['lessons']:
                page=pages[l['id']] if legacy else render({**payload(course,l,source.parent,audio),'collection_home':direct_home})
                (stage/('lesson-'+l['id']+'.html')).write_text(page)
        if not legacy:
            # Validate the complete proposed gallery before creating either deliverable.
            from build_catalog import discover,validate_metadata,build as catalog_build
            items=discover(dist) if dist.exists() else []
            ids=[c['id'] for _,c in items]
            if course['id'] in ids:raise ValueError('duplicate course identity; no implicit merge')
            shared.parent.mkdir(parents=True,exist_ok=False)
            try:
                atomic_text(shared,bundled);validate_metadata(read_manifest(shared))
                if settings is not None and settings!=json.loads(original_settings):atomic_text(dist/'catalog.json',json.dumps(settings,ensure_ascii=False,indent=2)+'\n')
                catalog_build(dist)
            except Exception:
                if original_settings is not None:atomic_text(dist/'catalog.json',original_settings.decode('utf-8'))
                shared.unlink(missing_ok=True);shared.parent.rmdir();raise
        stage.rename(output)
    path=output/'index.html' if legacy else shared
    return {'path':str(path),'catalog':str(dist/'index.html') if not legacy else None,'lessons':len(pages),'audio':course['audio_build'],'narration':'selected per lesson; runtime listening remains required','browser_verification':'pending','share_hint':str(path)+' (one course); '+str(dist if not legacy else output)+' folder or build_catalog.py --zip (multiple courses)'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--previous',type=Path);p.add_argument('--collection-home');p.add_argument('--dist',type=Path);p.add_argument('--audio-format',choices=['opus','mp3','wav'],default='opus');p.add_argument('--lesson-pages',action='store_true');p.add_argument('--catalog-position',type=int);a=p.parse_args()
    try:print(json.dumps(build(a.input,a.output,a.previous,a.collection_home,dist=a.dist or a.input.absolute().parent.parent/'dist',audio_format=a.audio_format,lesson_pages=a.lesson_pages,catalog_position=a.catalog_position),ensure_ascii=False));return 0
    except (ValueError,KeyError,TypeError,OSError,subprocess.SubprocessError) as e:print(json.dumps({'status':'failed','detail':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
