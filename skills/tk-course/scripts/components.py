from html import escape as h
from app_shell import theme_svg
from slide_components import TYPES,render as figure_svg,contract as figure_contract
def text(x,y,t,size=42,fill='#182a42',weight='400',anchor=None):
    a=f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"{a}>{h(t)}</text>'
def rect(x,y,w,hh,fill='#f1f5fa',stroke='none',rx=18):return f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def focus(parts,cues,key):return '<g class="explain-focus" data-focus-key="'+key+'" data-emphasis="'+' '.join(map(str,cues))+'">'+''.join(parts)+'</g>'
def _svg(i,s):
    if s['type']=='content':return content_svg(i,s)
    v=s['visual']
    def f(key,parts):return focus(parts,[n for n,c in enumerate(s['narration']) if key in c.get('focus',[])],key)
    parts=[rect(0,0,1600,900,'#ffffff',rx=0),text(90,90,s['eyebrow'],27,'#446991','600'),text(90,196,s['title'],56,weight='700')]
    if s['type']=='comparison':
        for x,card,key in zip([90,825],v['cards'],['cancel','guard']):
            parts.append(f(key,[rect(x,305,680,335),text(x+38,373,card['title'],41,weight='600'),text(x+38,465,card['tag'],41,'#355d8a','600'),text(x+38,555,card['copy'],30,'#52677d')]))
        parts.append(f('caveats',[text(90,736,v['footnote'],35,'#46607c')]))
    elif s['type']=='prediction':
        parts.append(rect(90,285,1420,290))
        for row,y,key in zip(v['rows'],[376,490],['request-order','response-order']):
            parts.append(f(key,[text(135,y,row['label'],34,'#61758c'),rect(480,y-47,970,72,fill='none'),text(500,y+6,row['sequence'],52,weight='600')]))
        parts.extend([f('predict',[rect(90,637,1420,88,fill='none'),text(800,692,v['question'],39,'#355d8a',anchor='middle')]),f('practice',[text(800,765,v['hint'],30,'#61758c',anchor='middle')])])
    else:raise ValueError('unsupported component')
    parts.extend([f'<path d="M90 838H1510" stroke="#e0e6ee" stroke-width="2"/>',text(1510,875,str(i+1),26,'#63768b',anchor='end')])
    return f'<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="slide-title-{i} slide-desc-{i}" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="slide-title-{i}">{h(s["title"])}</title><desc id="slide-desc-{i}">{h(s["transcript"])}</desc>'+''.join(parts)+'</svg>'
def svg(i,s,responsive=False):
    objectives=h(' '.join(s.get('objective_ids',[])),quote=True)
    if s['type'] in TYPES:
        figure_contract(s)
        result=check_bounds(figure_svg(s,i),s.get('id','preview'))+(check_bounds(figure_svg(s,i,compact=True),s.get('id','preview')) if responsive else '')
        return result.replace('<svg ',f'<svg data-objectives="{objectives}" ')
    return check_bounds(theme_svg(_svg(i,s)),s.get('id','preview')).replace('<svg ',f'<svg data-objectives="{objectives}" ',1)

def content_svg(i,s):
    parts=[rect(0,0,1600,900,'#ffffff',rx=0),text(90,90,s.get('eyebrow',''),27,'#446991','600'),text(90,196,s['title'],56,weight='700')]
    for n,item in enumerate(s['visual']['items']):
        key='item-'+str(n+1); y=280+n*130
        cues=[j for j,c in enumerate(s['narration']) if key in c.get('focus',[])]
        parts.append(focus([rect(90,y,1420,112),text(125,y+43,item['label'],32,weight='600'),text(125,y+86,item['text'],30,'#596d83')],cues,key))
    return theme_svg(f'<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="slide-title-{i} slide-desc-{i}" font-family="-apple-system,BlinkMacSystemFont,Apple SD Gothic Neo,Noto Sans KR,sans-serif"><title id="slide-title-{i}">{h(s['title'])}</title><desc id="slide-desc-{i}">{h(s['transcript'])}</desc>'+''.join(parts)+'</svg>')


def check_bounds(markup,slide_id):
    """Conservative preflight; actual font/path/raster geometry still needs a browser."""
    from xml.etree import ElementTree as ET
    from slide_components import width
    root=ET.fromstring(markup)
    bounds=list(map(float,root.get('viewBox').split()))
    if bounds!=[0,0,1600,900]:raise ValueError(f'slide {slide_id}: expected fixed 1600x900 canvas')
    for e in root.iter():
        kind=e.tag.rsplit('}',1)[-1]
        if kind in {'rect','image'}:
            x,y,w,hh=[float(e.get(k,'0')) for k in ('x','y','width','height')]
        elif kind=='text':
            x=float(e.get('x','0'));size=float(e.get('font-size','34'))
            y=float(e.get('y','0'))-size;hh=size*1.4
            w=width(e.text or '')*size*.5
            anchor=e.get('text-anchor')
            x-=w/2 if anchor=='middle' else w if anchor=='end' else 0
        else:continue
        if min(x,y,w,hh)<-.5 or x+w>1600.5 or y+hh>900.5:
            region=(e.text or kind)[:48]
            raise ValueError(f'slide {slide_id}: {region} outside fixed canvas; split meaningful questions or states')
    return markup
