"""Bounded, data-driven offline SVG figures and their cue-reference contract."""
from html import escape
import math
import unicodedata

TYPES={'image','bar','line','stacked','output','code','timeline','hook','cover','course-map','summary'}

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
    if kind=='image':
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
        if not any(line.strip() for line in lines) or sum(len(wrap(line,28)) for line in lines)>(30 if legacy else 20):
            raise ValueError('code/output exceeds the narrow-screen row budget; split the slide')
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
    """A second, purpose-built portrait layout keeps mobile labels readable."""
    v=slide['visual'];kind=slide['type'];w=760 if compact else 1600;m=52 if compact else 90;right=w-m
    size=36 if compact else 34;title_size=50 if compact else 56
    parts=[box(0,0,w,2500,'var(--slide-paper)'),t(m,66,slide.get('eyebrow',''),28,fill='var(--slide-muted)')]
    title_step=line_step(title_size,64)
    if kind!='cover':parts.append(multi(m,144,slide['title'],26 if compact else 90,title_size,title_step,weight='700'))
    title_rows=len(wrap(slide['title'],26 if compact else 90))
    top=max(260,144+(title_rows-1)*title_step+100) if kind!='cover' else 260;bottom=900
    def g(key,*items,aliases=()):return group(slide,key,list(items),aliases)
    if kind=='image':
        iw=right-m
        ih=iw/v.get('aspect_ratio',16/9)
        parts.append(g('image',f'<image x="{m}" y="{top}" width="{iw}" height="{ih}" href="{escape(v["src"],quote=True)}" preserveAspectRatio="xMidYMid meet" aria-label="{escape(v["alt"],quote=True)}"/>'))
        for i,r in enumerate(v.get('regions',[]),1):
            x=m+r['x']*iw;y=top+r['y']*ih
            parts.append(g('region-'+r['id'],f'<rect class="focus-halo" x="{x}" y="{y}" width="{r["width"]*iw}" height="{r["height"]*ih}" fill="none" stroke="var(--slide-accent)" stroke-width="4"/>',t(x+6,y+32,str(i),28,fill='var(--slide-accent)',weight='700')))
        y=top+ih+64;limit=36 if compact else 110
        parts.append(multi(m,y,v['description'],limit,32,48));y+=len(wrap(v['description'],limit))*48+16
        for i,r in enumerate(v.get('regions',[]),1):
            parts.append(multi(m,y,str(i)+'. '+r['label'],limit,30,46));y+=len(wrap(str(i)+'. '+r['label'],limit))*46+8
        parts.append(multi(m,y,'이용 범위: '+v['rights'],limit,28,42));y+=len(wrap('이용 범위: '+v['rights'],limit))*42
        bottom=max(bottom,y+130);source=v['source']
    elif kind in {'bar','line','stacked'}:
        data=v['data'];unit=v['unit'];bottom=1100 if compact else 940
        ylabel=v['y_label']+' · '+unit;xlabel=v['x_label']+(' · '+v['x_unit'] if kind=='line' else '')
        if compact:
            yr=len(wrap(ylabel,38));xr=len(wrap(xlabel,38))
            axis_step=line_step(32,42)
            parts += [multi(m,top,ylabel,38,32,axis_step),multi(m,top+yr*axis_step+16,xlabel,38,32,axis_step)]
            top+=max(0,(yr+xr)*axis_step+32-80)
        else:parts += [t(m,top,ylabel,32),t(right,top+40,xlabel,32,'end')]
        if kind=='line':
            points=[p for series in data for p in series['points']];xs=[p['x'] for p in points];ys=[p['y'] for p in points]
            low=min(0,min(ys));high=max(0,max(ys));span=high-low or 1
            left=m+72;xr=right-24;yt=top+104;yb=top+(370 if compact else 410)
            px=lambda x:left+(x-min(xs))/(max(xs)-min(xs))*(xr-left)
            py=lambda y:yb-(y-low)/span*(yb-yt)
            for j in range(4):
                value=low+span*j/3;y=py(value)
                parts += [path(f'M{left:g} {y:g}H{xr:g}'),t(left-12,y+10,format(value,'.3g'),28,'end')]
            ticks=data[0]['points'];last_right=-math.inf
            for pi,p in enumerate(ticks):
                value=str(p['x']);x=px(p['x']);size_estimate=width(value)*23
                anchor='start' if pi==0 else 'end' if pi==len(ticks)-1 else 'middle'
                start=x if anchor=='start' else x-size_estimate if anchor=='end' else x-size_estimate/2
                end=start+size_estimate
                if pi in (0,len(ticks)-1) or start>last_right+12 and end<xr-width(str(ticks[-1]['x']))*23-12:
                    parts.append(t(x,yb+45,value,32,anchor));last_right=end
            legend_limit=18 if compact else 40
            legend_step=line_step(32 if compact else size,42);value_step=line_step(32 if compact else 34,42)
            for si,series in enumerate(data):parts.append(multi(m if si==0 else w/2+10,yb+110,series['label'],legend_limit,32 if compact else size,legend_step,weight='600'))
            rowtop=yb+110+max(len(wrap(series['label'],legend_limit)) for series in data)*legend_step+24
            rowstep=max(60,max(len(wrap(str(p['x'])+': '+fmt(p['y'])+' '+unit,legend_limit)) for p in points)*value_step+16)
            for si,series in enumerate(data,1):
                color='var(--slide-accent)' if si==1 else 'var(--slide-muted)'
                d='M'+' L'.join(f'{px(p["x"]):g} {py(p["y"]):g}' for p in series['points'])
                # A focused point also brings its trajectory into context; series focus covers every point.
                indices=[str(i) for i,c in enumerate(slide['narration']) if 'series-'+str(si) in c.get('focus',[]) or any('point-'+str((si-1)*len(series['points'])+pi+1) in c.get('focus',[]) for pi in range(len(series['points'])))]
                parts.append('<g class="explain-focus" data-focus-key="series-'+str(si)+'" data-emphasis="'+' '.join(indices)+'">'+path(d,color,'10 8' if si>1 else '')+'</g>')
                for pi,p in enumerate(series['points']):
                    key='point-'+str((si-1)*len(series['points'])+pi+1);x=px(p['x']);y=py(p['y']);value=fmt(p['y'])+' '+unit
                    mark=f'<circle class="chart-mark" cx="{x:g}" cy="{y:g}" r="10" fill="{color}"/>' if si==1 else box(x-9,y-9,18,18,color)
                    label_x=m if si==1 else w/2+10
                    row=str(p['x'])+': '+value
                    parts.append(g(key,'<title>'+escape(series['label']+' · '+str(p['x'])+' '+v['x_unit']+' · '+str(p['y'])+' '+unit)+'</title>',mark,multi(label_x,rowtop+pi*rowstep,row,legend_limit,32 if compact else 34,value_step),aliases=('series-'+str(si),)))
            bottom=max(bottom,rowtop+len(data[0]['points'])*rowstep+110)
        elif kind=='bar':
            vals=[d['value'] for d in data];low=min(0,min(vals));high=max(0,max(vals));span=high-low or 1
            horizontal=v.get('orientation','vertical')=='horizontal'
            if horizontal:
                left=m;xr=right;scale=lambda n:left+(n-low)/span*(xr-left);zero=scale(0);rowtop=top+115;text_step=line_step(32,42)
                for i,item in enumerate(data):
                    end=scale(item['value']);value=fmt(item['value'])+' '+unit;limit=36 if compact else 100
                    value_y=rowtop+len(wrap(item['label'],limit))*text_step+14;bar_y=value_y+len(wrap(value,limit))*text_step+8
                    parts.append(g('bar-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(min(zero,end),bar_y,abs(end-zero),38,'var(--slide-accent)'),multi(m,rowtop,item['label'],limit,32,text_step),multi(m,value_y,value,limit,32,text_step),path(f'M{zero:g} {bar_y-10:g}V{bar_y+48:g}','var(--slide-text)'),t(zero,bar_y+84,'0',28,'middle')))
                    rowtop=bar_y+145
                bottom=max(bottom,rowtop+100)
            else:
                left=m+70;xr=right;yt=top+110;yb=top+480;scale=lambda n:yb-(n-low)/span*(yb-yt);zero=scale(0);step=(xr-left)/len(data)
                for j in range(4):
                    val=low+span*j/3;y=scale(val)
                    parts.extend([path(f'M{left:g} {y:g}H{xr:g}'),t(left-12,y+10,format(val,'.3g'),28,'end')])
                labelrows=max(len(wrap(item['label'],max(4,int(step/19)))) for item in data)
                label_step=line_step(30,38);value_step=line_step(32,40);legend_top=yb+95+labelrows*label_step
                for i,item in enumerate(data):
                    x=left+step*(i+.5);end=scale(item['value']);bw=step*.55
                    value=item['label']+' · '+fmt(item['value'])+' '+unit;limit=38 if compact else 100
                    parts.append(g('bar-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(x-bw/2,min(zero,end),bw,abs(end-zero),'var(--slide-accent)'),multi(x,yb+55,item['label'],max(4,int(step/19)),30,label_step,anchor='middle'),multi(m,legend_top,value,limit,32,value_step)))
                    legend_top+=len(wrap(value,limit))*value_step+24
                parts.append(path(f'M{left:g} {zero:g}H{xr:g}','var(--slide-text)'))
                bottom=max(bottom,legend_top+100)
        else:
            total=sum(item['value'] for item in data);x=m;scale=(right-m)/total
            parts.append(t(m,top+80,'합계 '+fmt(total)+' '+unit,36,weight='600'))
            legend_y=top+285;value_step=line_step(size,46)
            for i,item in enumerate(data):
                span=item['value']*scale;value=str(i+1)+'. '+item['label']+' · '+fmt(item['value'])+' '+unit+' ('+fmt(round(item['value']/total*100,1))+'%)';limit=36 if compact else 100
                # The legend carries exact values even when a segment is too small to label inside.
                parts.append(g('segment-'+str(i+1),'<title>'+escape(item['label']+' · '+str(item['value'])+' '+unit)+'</title>',box(x,top+150,span,72,'var(--slide-accent)' if i==0 else 'var(--slide-muted)'),t(x+span/2,top+198,str(i+1) if span>40 else '',30,'middle',fill='var(--slide-paper)'),multi(m,legend_y,value,limit,size,value_step)))
                x+=span
                legend_y+=len(wrap(value,limit))*value_step+32
            parts += [t(m,top+140,'0',28),t(right,top+140,fmt(total),28,'end')];bottom=max(bottom,legend_y+100)
        source=v['source']
    elif kind in {'code','output'}:
        lines=slide['code'] if kind=='code' else v['data'];rowtop=top+20;step=line_step(34 if compact else 22,48 if compact else 45)
        displayrows=sum(len(wrap(line,28 if compact else 100)) for line in lines);height=displayrows*step+42
        parts.append(box(m,top-20,right-m,height,'var(--slide-soft)'))
        aliases={0:'request-id',1:'await',2:'compare',3:'compare',4:'render',5:'compare'}
        for i,line in enumerate(lines):
            wraps=wrap(line,28 if compact else 100);fragments=[t(m+16,rowtop,str(i+1),28,fill='var(--slide-muted)')]
            for j,row in enumerate(wraps):
                fragments.append(f'<text x="{m+70}" y="{rowtop+j*step:g}" font-size="{34 if compact else 22}" font-family="monospace" fill="var(--slide-text)" xml:space="preserve" style="white-space:pre">'+escape(row)+'</text>')
            parts.append(g('line-'+str(i+1),box(m+4,rowtop-32,right-m-8,len(wraps)*step,'none'),*fragments,aliases=([aliases[i]] if kind=='code' and i in aliases else [])))
            rowtop+=len(wraps)*step
        bottom=max(1000,rowtop+210)
        if kind=='code':
            footnote_step=line_step(32,42)
            parts.append(g('takeaway',multi(m,rowtop+80,v['footnote'],36 if compact else 110,32,footnote_step)))
            bottom=max(bottom,rowtop+80+len(wrap(v['footnote'],36 if compact else 110))*footnote_step+80);source=''
        else:source=v['source']
    elif kind=='timeline':
        events,legacy=timeline(slide);lanes=v['lanes'];col=(right-m)/len(lanes);limit=max(8,int(col/19));text_step=line_step(30,38);rowheight=max(70,max(len(wrap(e['label'],limit)) for e in events)*text_step+24)
        headerheight=max(len(wrap(lane,limit)) for lane in lanes)*text_step;eventtop=top+headerheight+55
        for i,lane in enumerate(lanes):
            x=m+col*(i+.5);parts.extend([multi(x,top,lane,limit,30,text_step,anchor='middle'),path(f'M{x:g} {top+headerheight:g}V{eventtop+len(events)*rowheight:g}')])
        for i,event in enumerate(events):
            x=m+col*(event['lane']+.5);y=eventtop+i*rowheight
            parts.append(g('event-'+str(i+1),box(x-col*.45,y-38,col*.9,rowheight-15),multi(x,y,event['label'],max(8,int(col/19)),30,text_step,anchor='middle'),aliases=([['request-a','request-b','response-b','response-a'][i]] if legacy else [])))
        bottom=max(1000,eventtop+len(events)*rowheight+200)
        if v.get('callout'):
            callout_top=bottom-140;callout_step=line_step(32,42)
            parts.append(g('callout',multi(m,callout_top,v['callout'],36 if compact else 110,32,callout_step),aliases=(['overwrite'] if legacy else [])))
            bottom=max(bottom,callout_top+len(wrap(v['callout'],36 if compact else 110))*callout_step+50)
        source=''
    elif kind=='hook':
        # Every card is one focus group, including its background and label.
        cardtop=top;value_step=line_step(48,58);question_step=line_step(36,46)
        for line in v['title_lines']:
            parts.append(multi(m,cardtop,line,26 if compact else 72,48,value_step,weight='600'));cardtop+=len(wrap(line,26 if compact else 72))*value_step
        cardtop+=30;cards=v['cards'];cols=1 if compact else min(2,len(cards));cw=(right-m-28*(cols-1))/cols;value_limit=int((cw-48)/34)
        cardheight=110+max(len(wrap(c['value'],value_limit)) for c in cards)*value_step;cardstep=cardheight+24
        for i,card in enumerate(cards):
            x=m+(i%cols)*(cw+28);y=cardtop+(i//cols)*cardstep
            parts.append(g('card-'+str(i+1),box(x,y,cw,cardheight),t(x+24,y+48,card['label'],32,fill='var(--slide-muted)'),multi(x+24,y+116,card['value'],value_limit,48,value_step,weight='700'),aliases=([['first-search','latest-search'][i]] if i<2 else [])))
        question_top=cardtop+math.ceil(len(cards)/cols)*cardstep+70;question_limit=36 if compact else 110
        bottom=max(1000,question_top+len(wrap(v['question'],question_limit))*question_step+80)
        parts.append(multi(m,question_top,v['question'],question_limit,36,question_step));source=''
    elif kind=='cover':
        cover_step=line_step(58,74);question_step=line_step(42,58)
        parts.append(g('title',t(m,top+80,'제 '+str(v['number'])+'강',42,fill='var(--slide-accent)'),multi(m,top+180,slide['title'],24 if compact else 80,58,cover_step,weight='700')))
        question_top=top+180+len(wrap(slide['title'],24 if compact else 80))*cover_step+90
        parts.append(g('question',multi(m,question_top,v['question'],30 if compact else 90,42,question_step)));bottom=max(1100 if compact else 1000,question_top+len(wrap(v['question'],30 if compact else 90))*question_step+100);source=''
    elif kind=='course-map':
        y=top;item_step=line_step(30,36)
        for i,item in enumerate(v['lessons'],1):
            current=i==v['current'];badge='현재' if current else '✓ 앞서 다룸' if i<v['current'] else '다음';height=(76 if compact else 24)+len(wrap(item,34 if compact else 70))*item_step
            parts.append(g('lesson-'+str(i),box(m,y,right-m,height,'var(--slide-soft)','var(--slide-accent)' if current else 'none'),t(m+16,y+35,str(i)+'. '+badge,27,fill='var(--slide-accent)' if current else 'var(--slide-muted)'),multi(m+(16 if compact else 230),y+(84 if compact else 42),item,34 if compact else 70,30,item_step)))
            y+=height+14
        bottom=max(1100,y+130);source=''
    else:
        y=top;question_step=line_step(36,46);answer_step=line_step(34,44)
        for i,item in enumerate(v['items'],1):
            limit=32 if compact else 100;answer_top=52+len(wrap(item['question'],limit))*question_step+18;height=answer_top+len(wrap(item['answer'],limit))*answer_step+12
            parts.append(g('answer-'+str(i),box(m,y,right-m,height),multi(m+24,y+52,item['question'],limit,36,question_step,weight='600'),multi(m+24,y+answer_top,item['answer'],limit,34,answer_step)))
            y+=height+24
        bottom=max(1100 if compact else 1000,y+90);source=''
    if source:
        source_top=bottom-86;source_step=line_step(28,36);source_limit=40 if compact else 120
        parts.append(multi(m,source_top,'출처: '+source,source_limit,28,source_step,fill='var(--slide-muted)'))
        bottom=max(bottom,source_top+len(wrap('출처: '+source,source_limit))*source_step+44)
    parts.append(t(right,bottom-22,str(index+1),24,'end',fill='var(--slide-muted)'))
    parts[0]=box(0,0,w,bottom,'var(--slide-paper)')
    variant='narrow' if compact else 'wide';prefix=f'slide-{index}-{variant}'
    return f'<svg class="course-visual-{variant}" viewBox="0 0 {w} {bottom}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{prefix}-title {prefix}-desc" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="{prefix}-title">{escape(slide["title"])}</title><desc id="{prefix}-desc">{escape(slide["transcript"])}</desc>'+''.join(parts)+'</svg>'

def table(slide):
    """Static, keyboard-readable original values, also used by the no-JS fallback."""
    kind=slide['type'];v=slide['visual']
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
