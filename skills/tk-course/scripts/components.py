from html import escape as h
from app_shell import theme_svg
def text(x,y,t,size=42,fill='#182a42',weight='400',anchor=None):
    a=f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"{a}>{h(t)}</text>'
def rect(x,y,w,hh,fill='#f1f5fa',stroke='none',rx=18):return f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def focus(parts,cues,key):return '<g class="explain-focus" data-focus-key="'+key+'" data-emphasis="'+' '.join(map(str,cues))+'">'+''.join(parts)+'</g>'
def _svg(i,s):
    if s['type']=='content':return content_svg(i,s)
    v=s['visual']
    def f(key,parts):return focus(parts,[n for n,c in enumerate(s['narration']) if key in c.get('focus',[])],key)
    elements=[rect(0,0,1600,900,'#ffffff',rx=0),text(90,90,s['eyebrow'],27,'#446991','600')]
    title=s['title']
    if s['type']=='hook':
        elements += [text(90,210,v['title_lines'][0],64,weight='700'),text(90,294,v['title_lines'][1],64,weight='700')]
        for x,card,col,key in zip([90,825],v['cards'],['#e9eef5','#e9f4ee'],['first-search','latest-search']):
            elements += [rect(x,375,680,235,col),text(x+38,430,card['label'],30,'#596d83'),f(key,[rect(x,375,680,235,fill='none'),text(x+38,535,card['value'],82,weight='700')])]
        elements += [text(800,727,v['question'],39,'#46607c',anchor='middle')]
    else:
        elements += [text(90,196,title,56,weight='700')]
        if s['type']=='timeline':
            for y,label in zip([385,590],v['lanes']):
                elements += [text(90,y+12,label,34),f'<path d="M310 {y}H1450" stroke="#d4dce7" stroke-width="4"/>']
            for (x,y,color),label,key in zip([(350,385,'#5579a2'),(620,590,'#25835f'),(1050,590,'#25835f'),(1390,385,'#5579a2')],v['events'],['request-a','request-b','response-b','response-a']):
                elements += [f(key,[f'<circle class="focus-halo" cx="{x}" cy="{y}" r="28" fill="none"/>',f'<circle cx="{x}" cy="{y}" r="15" fill="{color}"/>',text(x,y-45,label,32,color,anchor='middle')])]
            elements += [f('overwrite',[rect(90,710,1420,80,'#fff2dc'),text(130,763,v['callout'],34,'#875018')])]
        elif s['type']=='code':
            elements += [rect(90,268,1420,442,'#142032')]
            for n,line in enumerate(s['code']):
                if not line.strip():continue
                y=335+58*n;key={0:'request-id',1:'await',2:'compare',3:'compare',4:'render',5:'compare'}[n]
                elements += [f(key,[f'<rect class="code-focus" x="110" y="{y-43}" width="1370" height="58" rx="5" fill="#243c56"/>',text(130,y,str(n+1),29,'#7d91a9'),f'<text x="200" y="{y}" font-family="monospace" font-size="37" fill="#e8eff8" xml:space="preserve">{h(line)}</text>'])]
            elements += [f('takeaway',[text(90,746,v['footnote'],36,'#46607c')])]
        elif s['type']=='comparison':
            for x,card,key in zip([90,825],v['cards'],['cancel','guard']):
                elements += [rect(x,305,680,335),text(x+38,373,card['title'],41,weight='600'),f(key,[rect(x,305,680,335,fill='none'),text(x+38,465,card['tag'],41,'#355d8a','600'),text(x+38,555,card['copy'],30,'#52677d')])]
            elements += [f('caveats',[text(90,736,v['footnote'],35,'#46607c')])]
        else:
            elements += [rect(90,285,1420,290)]
            for row,y,key in zip(v['rows'],[376,490],['request-order','response-order']):
                elements += [text(135,y,row['label'],34,'#61758c'),f(key,[rect(480,y-47,970,72,fill='none'),text(500,y+6,row['sequence'],52,weight='600')])]
            elements += [f('predict',[rect(90,637,1420,88,fill='none'),text(800,692,v['question'],39,'#355d8a',anchor='middle')]),f('practice',[text(800,765,v['hint'],30,'#61758c',anchor='middle')])]
    elements += [f'<path d="M90 838H1510" stroke="#e0e6ee" stroke-width="2"/>',text(1510,875,str(i+1),26,'#63768b',anchor='end')]
    return f'<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="slide-title-{i} slide-desc-{i}" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="slide-title-{i}">{h(title)}</title><desc id="slide-desc-{i}">{h(s["transcript"])}</desc>'+''.join(elements)+'</svg>'
def svg(i,s):
    objectives=h(' '.join(s.get('objective_ids',[])),quote=True)
    return theme_svg(_svg(i,s)).replace('<svg ',f'<svg data-objectives="{objectives}" ',1)

def content_svg(i,s):
    parts=[rect(0,0,1600,900,'#ffffff',rx=0),text(90,90,s.get('eyebrow',''),27,'#446991','600'),text(90,196,s['title'],56,weight='700')]
    for n,item in enumerate(s['visual']['items']):
        key='item-'+str(n+1); y=280+n*130
        cues=[j for j,c in enumerate(s['narration']) if key in c.get('focus',[])]
        parts.append(focus([rect(90,y,1420,112),text(125,y+43,item['label'],32,weight='600'),text(125,y+86,item['text'],30,'#596d83')],cues,key))
    return theme_svg(f'<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="slide-title-{i} slide-desc-{i}" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="slide-title-{i}">{h(s['title'])}</title><desc id="slide-desc-{i}">{h(s['transcript'])}</desc>'+''.join(parts)+'</svg>')
