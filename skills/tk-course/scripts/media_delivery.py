"""Copy only rendered media and build a small file-based course entry."""
import hashlib,json,shutil
from html import escape
from distribution import embedded_manifest

SINGLE_FILE_LIMIT=10_000_000

class MediaFiles:
    def __init__(self,root,prefix='../'):
        self.root=root;self.prefix=prefix;self.files=set();self.cache={}

    def uri(self,path,kind):
        key=(path,kind)
        if key not in self.cache:
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
            digest=digest.hexdigest()
            name='assets/'+kind+'/'+digest+path.suffix.lower()
            target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True)
            if not target.exists():shutil.copyfile(path,target)
            self.files.add(name);self.cache[key]=name
        return self.prefix+self.cache[key]

def lesson_loader(id,page):
    return 'window.CourseLessonLoader('+json.dumps(id)+','+json.dumps(page,ensure_ascii=False)+');\n'

def folder_index(course):
    pages={l['id']:'lessons/lesson-'+l['id']+'.js' for l in course['lessons']}
    encoded=json.dumps(pages,ensure_ascii=False).replace('<','\\u003c')
    # Classic scripts work from file:// without fetch/CORS. srcdoc keeps all lessons on the
    # entry's storage origin, preserving pre-folder course progress and preferences.
    script="""const pages=JSON.parse(document.getElementById('course-pages').textContent),ids=Object.keys(pages),frame=document.getElementById('course-frame');let entering=false,ui=null,pending=null,loader=null;window.CourseLessonLoader=(id,html)=>{if(id!==pending||typeof html!=='string')return;const base=document.createElement('base');base.href=new URL('lessons/',location.href).href;frame.srcdoc=html.replace('<head>','<head>'+base.outerHTML);};function show(id,enter){if(!Object.hasOwn(pages,id))return;entering=enter;pending=id;loader?.remove();const script=document.createElement('script');loader=script;script.src=pages[id];script.onload=()=>script.remove();document.head.appendChild(script);}frame.addEventListener('load',()=>{if(entering)frame.contentWindow.postMessage({type:'course-enter',ui},'*');});window.addEventListener('message',e=>{if(e.source!==frame.contentWindow||e.data?.type!=='course-lesson'||!ids.includes(e.data.id))return;ui=e.data.ui;show(e.data.id,true);});show(ids[0],false);"""
    links=''.join('<li><a href="lessons/lesson-'+l['id']+'.html">'+escape(l['title'])+'</a></li>' for l in course['lessons'])
    home=('<a href="'+escape(course['collection_home'],quote=True)+'">전체 코스</a>') if course.get('collection_home') else ''
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8">'+embedded_manifest(course)+'<meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(course['title'])+'</title><style>html,body{margin:0;height:100%;overflow:hidden}iframe{display:block;width:100%;height:100dvh;border:0}</style></head><body><iframe id="course-frame" title="'+escape(course['title'],quote=True)+'" allow="fullscreen *" allowfullscreen></iframe><noscript><style>html,body{overflow:auto}iframe{display:none}</style><h1>'+escape(course['title'])+'</h1>'+home+'<ul>'+links+'</ul></noscript><script id="course-pages" type="application/json">'+encoded+'</script><script>'+script+'</script></html>'
