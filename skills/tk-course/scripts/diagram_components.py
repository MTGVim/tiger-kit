"""Fixed-canvas relationship diagrams; no generated markup or graph runtime."""
import re
from html import escape

ID=re.compile(r'[a-z0-9][a-z0-9-]{0,79}')

def contract(visual, label):
    nodes=visual.get('nodes');edges=visual.get('edges',[])
    if not isinstance(nodes,list) or not 2<=len(nodes)<=6:
        raise ValueError('diagram requires 2-6 nodes')
    if not isinstance(edges,list) or not 1<=len(edges)<=7:
        raise ValueError('diagram requires 1-7 relationships')
    known={};cells=set();groups=[]
    for node in nodes:
        if not isinstance(node,dict):raise ValueError('invalid diagram node')
        key=node.get('id')
        if not isinstance(key,str) or not ID.fullmatch(key) or key in known:
            raise ValueError('invalid or duplicate diagram node ID')
        row,column=node.get('row'),node.get('column')
        if type(row) is not int or type(column) is not int or not 0<=row<=1 or not 0<=column<=2:
            raise ValueError('diagram position must be an integer in the 2 by 3 grid')
        if (row,column) in cells:raise ValueError('diagram nodes overlap')
        label(node.get('label'),48)
        known[key]=node;cells.add((row,column));groups.append({'node-'+key})
    keys=set();pairs=set();connected=set()
    for edge in edges:
        if not isinstance(edge,dict):raise ValueError('invalid diagram edge')
        key=edge.get('id');a,b=edge.get('from'),edge.get('to')
        if not isinstance(key,str) or not ID.fullmatch(key) or key in keys:
            raise ValueError('invalid or duplicate diagram edge ID')
        if not isinstance(a,str) or not isinstance(b,str) or a not in known or b not in known or a==b or frozenset((a,b)) in pairs:
            raise ValueError('invalid or duplicate diagram relationship')
        start,end=known[a],known[b]
        if abs(start['row']-end['row'])+abs(start['column']-end['column'])!=1:
            raise ValueError('diagram relationships join adjacent grid cells; split complex routes')
        keys.add(key);pairs.add(frozenset((a,b)));connected.update((a,b));groups.append({'edge-'+key})
    if connected!=set(known):raise ValueError('diagram contains an unexplained isolated node')
    return groups

def render(visual, top, bottom, wrap, box, text, group):
    nodes=visual['nodes'];cols=1+max(n['column'] for n in nodes);rows=1+max(n['row'] for n in nodes)
    # Keep essential labels/arrows above the lower caption region. Multirow graphs
    # need compact labels; reject excessive density instead of shrinking their type.
    bottom=min(bottom,660 if rows==1 else 560)
    column_gap=100;row_gap=60
    cw=(1420-column_gap*(cols-1))/cols;rh=(bottom-top-row_gap*(rows-1))/rows
    # Marker IDs are supplied per SVG by the caller so catalog/slide copies stay independent.
    marker=visual['_marker']
    result=[f'<defs><marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="var(--slide-accent)"/></marker></defs>']
    positions={n['id']:(90+n['column']*(cw+column_gap),top+n['row']*(rh+row_gap)) for n in nodes}
    known={n['id']:n for n in nodes}
    for edge in visual['edges']:
        a,b=known[edge['from']],known[edge['to']];ax,ay=positions[a['id']];bx,by=positions[b['id']]
        if a['row']==b['row']:
            forward=bx>ax;x1=ax+cw+6 if forward else ax-6;x2=bx-12 if forward else bx+cw+12;y1=y2=ay+rh/2
        else:
            forward=by>ay;y1=ay+rh+6 if forward else ay-6;y2=by-12 if forward else by+rh+12;x1=x2=ax+cw/2
        title=escape(a['label']+' → '+b['label'])
        result.append(group('edge-'+edge['id'],f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" fill="none" stroke="var(--slide-accent)" stroke-width="5" marker-end="url(#{marker})" role="img" aria-label="{title}"><title>{title}</title></path>'))
    for node in nodes:
        x,y=positions[node['id']];lines=wrap(node['label'],int((cw-48)/28))
        if len(lines)*84+24>rh:raise ValueError('diagram node exceeds fixed frame; split the explanation')
        baseline=min(y+rh/2-(len(lines)-1)*42+20,540-56*.4-(len(lines)-1)*84)
        if baseline-56<y+12:raise ValueError('diagram label exceeds caption-safe region; split the explanation')
        content=box(x,y,cw,rh)+''.join(text(x+cw/2,baseline+i*84,line,56,anchor='middle',weight='600') for i,line in enumerate(lines))
        result.append(group('node-'+node['id'],content))
    return ''.join(result)

def notes(visual):
    names={n['id']:n['label'] for n in visual['nodes']}
    return '<ul>'+''.join('<li>'+escape(names[e['from']])+' → '+escape(names[e['to']])+'</li>' for e in visual['edges'])+'</ul>'
