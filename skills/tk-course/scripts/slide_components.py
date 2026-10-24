"""Bounded, data-driven offline SVG figures and their cue-reference contract."""
from html import escape
import math
import unicodedata
import diagram_components as diagrams

TYPES={'diagram','image','bar','line','stacked','output','code','timeline','hook','cover','course-map','summary'}

def width(value):
    return sum(4 if c=='\t' else 2 if unicodedata.east_asian_width(c) in 'WF' or c in 'MWmw' else 1 for c in value)

def label(value,limit):
    if not isinstance(value,str) or not value.strip() or '\n' in value or '\r' in value or width(value)>limit:
        raise ValueError('missing or oversized figure text; split the slide')
    return value

def number(value):
    if type(value) not in (int,float) or not math.isfinite(value) or abs(value)>1e12:
        raise ValueError('visual.data requires bounded finite numeric values')
    return value

def rows(value,low,high):
    if not isinstance(value,list) or not low<=len(value)<=high:
        raise ValueError('figure row budget exceeded; split the slide')
    return value

def wrap(value,limit):
    """Soft wraps preserve every original character, including leading spaces."""
    result=[];chunk=''
    for char in value:
        if chunk and width(chunk+char)>limit:
            boundary=chunk.rfind(' ')+1
            if boundary>=len(chunk)/2 and boundary<len(chunk):result.append(chunk[:boundary]);chunk=chunk[boundary:]
            else:result.append(chunk);chunk=''
        chunk+=char
    return result+[chunk]

def timeline(slide):
    visual=slide['visual'];events=visual['events']
    if all(isinstance(e,str) for e in events):
        if len(events)!=4 or len(visual['lanes'])!=2:raise ValueError('legacy timeline requires two lanes and four events')
        return [{'label':e,'lane':lane} for e,lane in zip(events,[0,1,1,0])],True
    return events,False

def contract(slide):
    """Return allowed cue keys and coverage alternatives for each semantic element."""
    kind=slide['type'];v=slide['visual'];groups=[]
    def add(key,*aliases):groups.append({key,*aliases})
    if kind=='diagram':
        groups.extend(diagrams.contract(v,label))
    elif kind=='image':
        label(v.get('alt'),180);label(v.get('description'),240);label(v.get('source'),110);label(v.get('rights'),110)
        if not isinstance(v.get('src'),str) or not v['src']:raise ValueError('image requires local src')
        regions=v.get('regions',[])
        if not isinstance(regions,list) or len(regions)>6:raise ValueError('image region budget exceeded')
        add('image');ids=set()
        for region in regions:
            key=region.get('id')
            if not isinstance(key,str) or not key.isascii() or not key.replace('-','').isalnum() or key in ids:raise ValueError('invalid image region ID')
            ids.add(key);label(region.get('label'),40)
            x,y,w,h=[number(region[k]) for k in ('x','y','width','height')]
            if not (0<=x<1 and 0<=y<1 and 0<w<=1-x and 0<h<=1-y):raise ValueError('image region outside image')
            add('region-'+key)
    elif kind in {'bar','line','stacked'}:
        label(v.get('unit'),16);label(v.get('x_label'),44);label(v.get('y_label'),44);label(v.get('source'),110)
        data=rows(v.get('data'),1,6)
        if kind=='line':
            rows(data,1,2);label(v.get('x_unit'),16);xs=None
            for si,series in enumerate(data,1):
                label(series.get('label'),32);points=rows(series.get('points'),2,8)
                current=[number(p['x']) for p in points]
                if any(b<=a for a,b in zip(current,current[1:])):raise ValueError('line x values must increase strictly')
                if xs is not None and current!=xs:raise ValueError('line series require the same measured x values; split differing samples')
                xs=current
                for pi,p in enumerate(points):
                    number(p['y']);add('point-'+str((si-1)*len(points)+pi+1),'series-'+str(si))
        else:
            for i,item in enumerate(data,1):
                label(item.get('label'),28);number(item.get('value'))
                if kind=='stacked' and item['value']<0:raise ValueError('stacked values must be nonnegative')
                add(('bar-' if kind=='bar' else 'segment-')+str(i))
            if kind=='stacked' and sum(d['value'] for d in data)<=0:raise ValueError('stacked total must be positive')
            if kind=='bar' and v.get('orientation','vertical') not in {'horizontal','vertical'}:raise ValueError('invalid bar orientation')
    elif kind in {'code','output'}:
        lines=rows(slide.get('code') if kind=='code' else v.get('data'),1,12)
        legacy=kind=='code' and len(lines)<=6 and all(isinstance(line,str) and len(line)<=70 for line in lines) and all(set(c.get('focus',[]))<={'request-id','await','compare','render','takeaway'} for c in slide['narration'])
        if any(not isinstance(line,str) or '\n' in line or '\r' in line or width(line)>(140 if legacy else 100) or any(ord(c)<32 and c!='\t' for c in line) for line in lines):
            raise ValueError('code/output line budget exceeded; split the slide')
        if not any(line.strip() for line in lines):
            raise ValueError('code/output has no visible text; split the slide')
        aliases={0:'request-id',1:'await',2:'compare',3:'compare',4:'render',5:'compare'}
        for i,line in enumerate(lines):
            if line.strip():add('line-'+str(i+1),*([aliases[i]] if kind=='code' and i in aliases else []))
        if kind=='code':label(v.get('footnote'),120);add('takeaway')
        else:label(v.get('source'),110)
    elif kind=='timeline':
        lanes=rows(v.get('lanes'),1,4)
        for lane in lanes:label(lane,24)
        events,legacy=timeline(slide);rows(events,1,8)
        for i,event in enumerate(events,1):
            if not isinstance(event,dict) or type(event.get('lane')) is not int or not 0<=event['lane']<len(lanes):raise ValueError('invalid timeline lane')
            label(event.get('label'),32);add('event-'+str(i),*([['request-a','request-b','response-b','response-a'][i-1]] if legacy else []))
        if v.get('callout'):label(v['callout'],120);add('callout',*(['overwrite'] if legacy else []))
    elif kind=='hook':
        for line in rows(v.get('title_lines'),1,2):label(line,48)
        cards=rows(v.get('cards'),1,4)
        for i,card in enumerate(cards,1):
            label(card.get('label'),36);label(card.get('value'),32)
            add('card-'+str(i),*([['first-search','latest-search'][i-1]] if i<=2 else []))
        label(v.get('question'),110)
    elif kind=='cover':
        if type(v.get('number')) is not int or not 1<=v['number']<=200:raise ValueError('cover requires a lesson number')
        label(v.get('question'),110);add('title');add('question')
    elif kind=='course-map':
        items=rows(v.get('lessons'),1,8)
        if type(v.get('current')) is not int or not 1<=v['current']<=len(items):raise ValueError('invalid current course-map lesson')
        for i,item in enumerate(items,1):label(item,64);add('lesson-'+str(i))
    elif kind=='summary':
        for i,item in enumerate(rows(v.get('items'),2,3),1):
            label(item.get('question'),64);label(item.get('answer'),100);add('answer-'+str(i))
    else:raise ValueError('unsupported component')
    return set().union(*groups),groups

def fmt(value):return str(value) if type(value) is int else format(value,'.8g')

def t(x,y,value,size=36,anchor='start',fill='var(--slide-text)',weight='400'):
    return f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" xml:space="preserve">{escape(str(value))}</text>'

def box(x,y,w,h,fill='var(--slide-soft)',stroke='none'):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="12" fill="{fill}" stroke="{stroke}"/>'

def path(d,stroke='var(--slide-line)',dash=''):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="3"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

def multi(x,y,value,limit,size=36,step=46,**kw):
    return ''.join(t(x,y+i*step,row,size,**kw) for i,row in enumerate(wrap(value,limit)))

def line_step(size,minimum):
    # Noto Sans KR's ascent/descent also bounds Latin runs in the selected CJK font.
    return max(minimum,math.ceil(size*1.5))

def group(slide,key,parts,aliases=()):
    indices=[str(i) for i,c in enumerate(slide['narration']) if set(c.get('focus',[]))&{key,*aliases}]
    return '<g class="explain-focus" data-focus-key="'+key+'" data-emphasis="'+' '.join(indices)+'">'+''.join(parts)+'</g>'

def render(slide,index,compact=False):
    """Ordinary media has one 1600x900 canvas; density never changes its bounds."""
    v=slide['visual'];kind=slide['type'];parts=[];m=90;right=1510;top=260;end=805
    def fail(region):
        raise ValueError(f"slide {slide['id']}: {region} exceeds fixed 1600x900 canvas; split meaningful questions or states")
    def text_at(x,y,value,size=34,limit=None,step=None,**kw):
        # Stable type sizes: exceeding a region is an authoring error, never auto-fit.
        step=step or line_step(size,0)
        limit=limit or max(1,int((right-x)/(size*.56)))
        lines=wrap(value,limit)
        if y-size<0 or y+(len(lines)-1)*step+size*.4>end:fail('text '+str(value)[:48])
        return multi(x,y,value,limit,size,step,**kw)
    def g(key,*items,aliases=()):return group(slide,key,list(items),aliases)
    parts=[box(0,0,1600,900,'var(--slide-paper)'),'<g data-slide-metadata="true">'+t(m,66,slide.get('eyebrow',''),28,fill='var(--slide-muted)')+'</g>']
    if kind!='cover':
        title=wrap(slide['title'],80)
        if len(title)>2:fail('title')
        parts.append(text_at(m,144,slide['title'],56,80,84,weight='700'))
        top=max(260,144+(len(title)-1)*84+100)
    source=v.get('source','')
    if kind=='diagram':
        parts.append(diagrams.render({**v,'_marker':'diagram-arrow-'+str(index)+'-'+('compact' if compact else 'wide')},top,end,wrap,box,t,g))
    elif kind=='image':
        # Image pixels keep their intrinsic ratio in a fixed region. The adjacent rail
        # carries short teaching labels; full provenance lives in accessible notes.
        ratio=number(v.get('aspect_ratio',16/9))
        if ratio<=0:fail('image aspect ratio')
        aw=920;ah=end-top-10;iw=min(aw,ah*ratio);ih=iw/ratio
        if iw<aw*.5:fail('image region (portrait composite needs reauthoring)')
        x=m+(aw-iw)/2;y=top+(ah-ih)/2
        parts.append(g('image',f'<image x="{x:g}" y="{y:g}" width="{iw:g}" height="{ih:g}" href="{escape(v["src"],quote=True)}" preserveAspectRatio="xMidYMid meet" aria-label="{escape(v["alt"],quote=True)}"/>'))
        for i,r in enumerate(v.get('regions',[]),1):
            rx=x+r['x']*iw;ry=y+r['y']*ih
            parts.append(g('region-'+r['id'],f'<rect class="focus-halo" x="{rx:g}" y="{ry:g}" width="{r["width"]*iw:g}" height="{r["height"]*ih:g}" fill="none" stroke="var(--slide-accent)" stroke-width="4"/>',t(rx+6,ry+56,str(i),56,fill='var(--slide-accent)',weight='700')))
        y=top+56
        for value in [v['description']]+[str(i)+'. '+r['label'] for i,r in enumerate(v.get('regions',[]),1)]:
            parts.append(text_at(1060,y,value,56,14,84));y+=len(wrap(value,14))*84+20
        source='강의 노트에 권리 및 원본 출처 수록'
    elif kind in {'bar','line','stacked'}:
        data=v['data'];unit=v['unit']
        parts += [text_at(m,top,v['y_label']+' · '+unit,32,70),text_at(right,top+40,v['x_label']+(' · '+v['x_unit'] if kind=='line' else ''),32,70,anchor='end')]
        if kind=='line':
            points=[p for series in data for p in series['points']];xs=[p['x'] for p in points];ys=[p['y'] for p in points]
            low=min(0,min(ys));high=max(0,max(ys));span=high-low or 1
            left=m+72;xr=850;yt=top+104;yb=top+440
            px=lambda x:left+(x-min(xs))/(max(xs)-min(xs))*(xr-left)
            py=lambda y:yb-(y-low)/span*(yb-yt)
            for j in range(4):
                value=low+span*j/3;y=py(value)
                parts += [path(f'M{left:g} {y:g}H{xr:g}'),t(left-12,y+10,format(value,'.3g'),28,'end')]
            ticks=data[0]['points'];last_right=-math.inf
            for pi,p in enumerate(ticks):
                value=str(p['x']);x=px(p['x']);estimate=width(value)*23
                anchor='start' if pi==0 else 'end' if pi==len(ticks)-1 else 'middle'
                start=x if anchor=='start' else x-estimate if anchor=='end' else x-estimate/2
                if pi in (0,len(ticks)-1) or start>last_right+12 and start+estimate<xr-width(str(ticks[-1]['x']))*23-12:
                    parts.append(t(x,yb+48,value,32,anchor));last_right=start+estimate
            for si,series in enumerate(data,1):
                color='var(--slide-accent)' if si==1 else 'var(--slide-muted)';label_x=930+(si-1)*300
                parts.append(text_at(label_x,top+110,series['label'],34,16,51,weight='600'))
                rowtop=top+110+max(len(wrap(s['label'],16)) for s in data)*51+28
                d='M'+' L'.join(f'{px(p["x"]):g} {py(p["y"]):g}' for p in series['points'])
                indices=[str(i) for i,c in enumerate(slide['narration']) if 'series-'+str(si) in c.get('focus',[]) or any('point-'+str((si-1)*len(series['points'])+pi+1) in c.get('focus',[]) for pi in range(len(series['points'])))]
                parts.append('<g class="explain-focus" data-focus-key="series-'+str(si)+'" data-emphasis="'+' '.join(indices)+'">'+path(d,color,'10 8' if si>1 else '')+'</g>')
                rowstep=max(62,max(len(wrap(str(p['x'])+': '+fmt(p['y'])+' '+unit,16)) for p in points)*51+12)
                for pi,p in enumerate(series['points']):
                    x=px(p['x']);y=py(p['y']);key='point-'+str((si-1)*len(series['points'])+pi+1)
                    mark=f'<circle class="chart-mark" cx="{x:.8f}" cy="{y:.8f}" r="10" fill="{color}"/>' if si==1 else box(x-9,y-9,18,18,color)
                    parts.append(g(key,'<title>'+escape(series['label']+' · '+str(p['x'])+' '+v['x_unit']+' · '+str(p['y'])+' '+unit)+'</title>',mark,text_at(label_x,rowtop+pi*rowstep,str(p['x'])+': '+fmt(p['y'])+' '+unit,34,16,51),aliases=('series-'+str(si),)))
        elif kind=='bar':
            vals=[d['value'] for d in data];low=min(0,min(vals));high=max(0,max(vals));span=high-low or 1
            horizontal=v.get('orientation','vertical')=='horizontal'
            if horizontal:
                left=620;xr=right;scale=lambda n:left+(n-low)/span*(xr-left);zero=scale(0);y=top+115
                for i,item in enumerate(data):
                    labelrows=len(wrap(item['label'],26));rowheight=max(130,labelrows*48+40)
                    if y+rowheight-20>end:fail('horizontal bar rows')
                    value=fmt(item['value'])+' '+unit;target=scale(item['value'])
                    parts.append(g('bar-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(min(zero,target),y+15,abs(target-zero),38,'var(--slide-accent)'),text_at(m,y,item['label'],32,26,48),text_at(m,y+labelrows*48,value,32,26,48),path(f'M{zero:g} {y+5:g}V{y+65:g}','var(--slide-text)'),t(zero,y+100,'0',28,'middle')))
                    y+=rowheight
            else:
                left=m+70;xr=right;yt=top+110;yb=top+375;scale=lambda n:yb-(n-low)/span*(yb-yt);zero=scale(0);step=(xr-left)/len(data)
                for j in range(4):
                    val=low+span*j/3;y=scale(val)
                    parts.extend([path(f'M{left:g} {y:g}H{xr:g}'),t(left-12,y+10,format(val,'.3g'),28,'end')])
                for i,item in enumerate(data):
                    x=left+step*(i+.5);target=scale(item['value']);bw=step*.55;limit=max(4,int(step/19))
                    y=yb+55+len(wrap(item['label'],limit))*48
                    parts.append(g('bar-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(x-bw/2,min(zero,target),bw,abs(target-zero),'var(--slide-accent)'),text_at(x,yb+55,item['label'],30,limit,48,anchor='middle'),text_at(x,y,fmt(item['value'])+' '+unit,32,limit,48,anchor='middle')))
                parts.append(path(f'M{left:g} {zero:g}H{xr:g}','var(--slide-text)'))
        else:
            total=sum(item['value'] for item in data);x=m;scale=(right-m)/total
            parts.append(t(m,top+80,'합계 '+fmt(total)+' '+unit,36,weight='600'))
            for i,item in enumerate(data):
                span=item['value']*scale;lx=m+(i%2)*730;ly=top+310+(i//2)*100
                value=str(i+1)+'. '+item['label']+' · '+fmt(item['value'])+' '+unit+' ('+fmt(round(item['value']/total*100,1))+'%)'
                parts.append(g('segment-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(x,top+150,span,72,'var(--slide-accent)' if i==0 else 'var(--slide-muted)'),t(x+span/2,top+198,str(i+1) if span>40 else '',30,'middle',fill='var(--slide-paper)'),text_at(lx,ly,value,34,36,51)))
                x+=span
            parts += [t(m,top+140,'0',28),t(right,top+140,fmt(total),28,'end')]
    elif kind in {'code','output'}:
        lines=slide['code'] if kind=='code' else v['data'];rowtop=top+10;step=40
        displayrows=sum(len(wrap(line,100)) for line in lines)
        if rowtop+(displayrows-1)*step+40+(100 if kind=='code' else 0)>end:fail('code/output rows')
        parts.append(box(m,top-30,right-m,displayrows*step+40,'var(--slide-soft)'))
        aliases={0:'request-id',1:'await',2:'compare',3:'compare',4:'render',5:'compare'}
        for i,line in enumerate(lines):
            wraps=wrap(line,100);fragments=[t(m+16,rowtop,str(i+1),28,fill='var(--slide-muted)')]
            for j,row in enumerate(wraps):
                fragments.append(f'<text x="{m+70}" y="{rowtop+j*step:g}" font-size="22" font-family="monospace" fill="var(--slide-text)" xml:space="preserve" style="white-space:pre">'+escape(row)+'</text>')
            parts.append(g('line-'+str(i+1),box(m+4,rowtop-28,right-m-8,len(wraps)*step,'none'),*fragments,aliases=([aliases[i]] if kind=='code' and i in aliases else [])))
            rowtop+=len(wraps)*step
        if kind=='code':parts.append(g('takeaway',text_at(m,rowtop+50,v['footnote'],32,78,48)))
    elif kind=='timeline':
        events,legacy=timeline(slide);lanes=v['lanes'];col=(right-m)/len(lanes);limit=max(8,int(col/19));step=45
        headerheight=max(len(wrap(lane,limit)) for lane in lanes)*step;eventtop=top+headerheight+45
        rowheight=max(62,max(len(wrap(e['label'],limit)) for e in events)*step+18)
        tail=eventtop+(len(events)-1)*rowheight+rowheight-15
        if tail+(83 if v.get('callout') else 0)>end:fail('timeline events/callout')
        for i,lane in enumerate(lanes):
            x=m+col*(i+.5);parts.extend([text_at(x,top,lane,30,limit,step,anchor='middle'),path(f'M{x:g} {top+headerheight:g}V{tail:g}')])
        for i,event in enumerate(events):
            x=m+col*(event['lane']+.5);y=eventtop+i*rowheight
            parts.append(g('event-'+str(i+1),box(x-col*.45,y-35,col*.9,rowheight-12),text_at(x,y,event['label'],30,limit,step,anchor='middle'),aliases=([['request-a','request-b','response-b','response-a'][i]] if legacy else [])))
        if v.get('callout'):parts.append(g('callout',text_at(m,tail+70,v['callout'],32,78,48),aliases=(['overwrite'] if legacy else [])))
    elif kind=='hook':
        y=top
        title_lines=[] if ' '.join(' '.join(v['title_lines']).split())==' '.join(slide['title'].split()) else v['title_lines']
        for value in title_lines:
            if ' '.join(value.split())==' '.join(slide['title'].split()):continue
            parts.append(text_at(m,y,value,48,72,72,weight='600'));y+=len(wrap(value,72))*72
        cards=v['cards'];cols=3 if len(cards)==3 else min(2,len(cards));cw=(right-m-28*(cols-1))/cols;limit=int((cw-48)/27)
        cardheight=95+max(len(wrap(c['value'],limit)) for c in cards)*72
        cardtop=y+10;cardstep=cardheight+24
        for i,card in enumerate(cards):
            x=m+(i%cols)*(cw+28);cy=cardtop+(i//cols)*cardstep
            if cy+cardheight>end:fail('hook cards')
            parts.append(g('card-'+str(i+1),box(x,cy,cw,cardheight),text_at(x+24,cy+45,card['label'],32,34),text_at(x+24,cy+108,card['value'],48,limit,72,weight='700'),aliases=([['first-search','latest-search'][i]] if i<2 else [])))
        parts.append(text_at(m,cardtop+math.ceil(len(cards)/cols)*cardstep+45,v['question'],36,76,54))
    elif kind=='cover':
        parts.append(g('title',t(m,top+40,'제 '+str(v['number'])+'강',42,fill='var(--slide-accent)'),text_at(m,top+150,slide['title'],58,76,87,weight='700')))
        y=top+150+len(wrap(slide['title'],76))*87+70
        parts.append(g('question',text_at(m,y,v['question'],42,64,63)))
    elif kind=='course-map':
        y=top;step=45
        for i,item in enumerate(v['lessons'],1):
            current=i==v['current'];badge='현재' if current else '✓ 앞서 다룸' if i<v['current'] else '다음'
            height=20+len(wrap(item,62))*step
            if y+height>end:fail('course-map rows')
            parts.append(g('lesson-'+str(i),box(m,y,right-m,height,'var(--slide-soft)','var(--slide-accent)' if current else 'none'),t(m+16,y+40,str(i)+'. '+badge,27,fill='var(--slide-accent)' if current else 'var(--slide-muted)'),text_at(m+250,y+42,item,30,62,step)))
            y+=height+14
    else:
        y=top
        for i,item in enumerate(v['items'],1):
            answer_top=52+len(wrap(item['question'],74))*54+10;height=answer_top+len(wrap(item['answer'],78))*51+10
            if y+height>end:fail('summary cards')
            parts.append(g('answer-'+str(i),box(m,y,right-m,height),text_at(m+24,y+52,item['question'],36,74,54,weight='600'),text_at(m+24,y+answer_top,item['answer'],34,78,51)))
            y+=height+24
    if source:
        source_rows=wrap('출처: '+source,100)
        if len(source_rows)>2:fail('source footer')
        footer=multi(m,844,('' if kind=='image' else '출처: ')+source,100,28,42,fill='var(--slide-muted)')
        if kind=='image':footer='<a href="#panel-notes" data-figure-note="'+escape(slide['id'],quote=True)+'">'+footer+'</a>'
        parts.append('<g data-slide-metadata="true">'+footer+'</g>')
    parts.append('<g data-slide-metadata="true">'+t(right,878,str(index+1),24,'end',fill='var(--slide-muted)')+'</g>')
    variant='narrow' if compact else 'wide';prefix=f'slide-{index}-{variant}'
    return f'<svg class="course-visual-{variant}" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{prefix}-title {prefix}-desc" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="{prefix}-title">{escape(slide["title"])}</title><desc id="{prefix}-desc">{escape(slide["transcript"])}</desc>'+''.join(parts)+'</svg>'

def table(slide):
    """Static, keyboard-readable original values, also used by the no-JS fallback."""
    kind=slide['type'];v=slide['visual']
    if kind=='diagram':return diagrams.notes(v)
    if kind=='image':
        return '<p>'+escape(v['description'])+'</p><ol>'+''.join('<li>'+escape(r['label'])+'</li>' for r in v.get('regions',[]))+'</ol><p>이용 범위: '+escape(v['rights'])+'</p><p>출처: '+escape(v['source'])+'</p>'
    if kind not in {'bar','line','stacked','output','code'}:return ''
    if kind in {'code','output'}:
        values=slide['code'] if kind=='code' else v['data']
        return '<pre class="original-output">'+escape('\n'.join(values))+'</pre>'
    data=v['data'];rows_html='';unit=escape(v['unit'])
    if kind=='line':
        head='<th scope="col">'+escape(v['x_label']+' · '+v['x_unit'])+'</th>'+''.join('<th scope="col">'+escape(s['label'])+' · '+unit+'</th>' for s in data)
        for i,p in enumerate(data[0]['points']):rows_html+='<tr><th scope="row">'+escape(str(p['x']))+'</th>'+''.join('<td>'+escape(str(s['points'][i]['y']))+'</td>' for s in data)+'</tr>'
    else:
        head='<th scope="col">'+escape(v['x_label'])+'</th><th scope="col">'+escape(v['y_label'])+' · '+unit+'</th>'
        rows_html=''.join('<tr><th scope="row">'+escape(d['label'])+'</th><td>'+escape(str(d['value']))+'</td></tr>' for d in data)
    return '<table><caption>'+escape(slide['title'])+'</caption><thead><tr>'+head+'</tr></thead><tbody>'+rows_html+'</tbody></table><p>출처: '+escape(v['source'])+'</p>'
