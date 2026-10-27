#!/usr/bin/env python3
"""Render a validated source-bound change model into one offline HTML document."""
import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path

import build_html
import change_model
import highlight_code


def esc(value):
    return html.escape(str(value), quote=True)


BASIS_LABEL = {'source': '원문 근거', 'inference': '추론', 'unverified': '미검증'}
DELTA_LABEL = {'added': '추가', 'modified': '변경', 'removed': '삭제', 'unchanged': '변경 없음'}


def check_supplement(fragment):
    class Markers(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if any(key == 'data-ht-nav-unit' for key, _ in attrs):
                raise ValueError('supplements cannot define navigation units')
        handle_startendtag = handle_starttag
    parser = Markers(); parser.feed(fragment); parser.close()


def render_body(model, sources, intro='', outro=''):
    errors = change_model.validate_model(model, sources)
    if errors:
        raise ValueError(json.dumps(errors, ensure_ascii=False))
    check_supplement(intro); check_supplement(outro)
    ev = {item['id']: item for item in model['evidence']}
    src = {(f['kind'], f['version'], f['path']): f['text'] for f in sources['files']}
    units = {item['id']: item for item in model['units']}
    links = {key: [] for key in ev}
    snapshot = model['snapshot']; versions = snapshot['versions']
    body = ['<p class="ht-lede">' + esc(model['summary']) + '</p>']
    body.append('<p>대상: ' + esc(snapshot['repository']) + ' · 비교: ' + esc(snapshot['comparison']) + '</p>')
    body.append('<p>이전: ' + esc(snapshot['from']) + ' / ' + esc(versions[snapshot['from']]['id']) +
                ' · 이후: ' + esc(snapshot['to']) + ' / ' + esc(versions[snapshot['to']]['id']) + '</p>')
    if not model['inventory_complete']: body.append('<p>변경 목록의 한계: ' + esc(model['inventory_limit']) + '</p>')
    body.append(intro)
    graph = model.get('graph', {}); edges = {e['id']: e for e in graph.get('edges', [])}; nodes = {n['id']: n for n in graph.get('nodes', [])}
    for index, group in enumerate(model['groups'], 1):
        body.append('<section id="change-group-' + esc(group['id']) + '" data-ht-nav-unit class="ht-change-group"><h2>' + esc(group['title']) + '</h2><p>' + esc(group['summary']) + '</p>')
        counter = [0]
        def references(ids):
            parts = []
            for ident in dict.fromkeys(ids):
                counter[0] += 1; position = counter[0]
                origin = f'cite-change-{index}-{position}'; links[ident].append((origin,index,position))
                parts.append('<sup id="' + origin + '"><a href="#evidence-' + esc(ident) + '">[' + str(position) + ']</a></sup>')
            return ' '.join(parts)
        body.append('<div class="ht-change-pair">')
        for side, label in (('before','이전'),('after','이후')):
            claim=group[side]
            body.append('<div class="ht-change-side"><h3>' + label + '</h3><p>' + esc(claim['text']) + ' ' + references(claim['evidence']) + '</p><p>근거 유형: ' + esc(BASIS_LABEL[claim['basis']]) + '</p>')
            if claim['limitation']: body.append('<p>한계: ' + esc(claim['limitation']) + '</p>')
            body.append('</div>')
        body.append('</div>')
        for claim in group['invariants']:
            body.append('<p>보존 조건: ' + esc(claim['text']) + ' (' + esc(BASIS_LABEL[claim['basis']]) + ') ' + references(claim['evidence']) + '</p>')
            if claim['limitation']: body.append('<p>한계: ' + esc(claim['limitation']) + '</p>')
        for item in group['limitations']: body.append('<p>한계: ' + esc(item) + '</p>')
        for item in group['checkpoints']: body.append('<p>확인할 지점: ' + esc(item) + '</p>')
        evidence_ids = list(group['evidence_ids'])
        for side in ('before','after'): evidence_ids.extend(group[side]['evidence'])
        for claim in group['invariants']: evidence_ids.extend(claim['evidence'])
        for uid in group['unit_ids']:
            evidence_ids.extend(units[uid]['before']); evidence_ids.extend(units[uid]['after'])
        evidence_ids=list(dict.fromkeys(evidence_ids))
        for flow in graph.get('flows', []):
            if flow['group_id'] == group['id']:
                for step in flow['steps']:
                    edge = edges[step['edge_id']]
                    evidence_ids.extend(edge['evidence_ids'])
                    evidence_ids.extend(nodes[edge['from']]['evidence_ids'])
                    evidence_ids.extend(nodes[edge['to']]['evidence_ids'])
        if evidence_ids:
            body.append('<p>관련 근거: ' + references(evidence_ids) + '</p>')
        for flow in graph.get('flows', []):
            if flow['group_id'] != group['id']: continue
            body.append('<div class="ht-change-flow" data-change-flow><h3>' + esc(flow['title']) + ' · ' + esc(flow['version']) + '</h3><ol>')
            for step in flow['steps']:
                edge=edges[step['edge_id']]; source=nodes[edge['from']]; target=nodes[edge['to']]
                body.append('<li data-change-step><div class="ht-change-flow-path">'
                    '<span class="ht-change-flow-node" data-change-node="' + esc(source['id']) + '"><strong>' + esc(source['label']) + '</strong><small>' + esc(DELTA_LABEL[source['delta']]) + '</small></span>'
                    '<span class="ht-change-flow-edge" data-change-edge="' + esc(edge['id']) + '"><span aria-hidden="true">→</span> ' + esc(edge['label']) + ' <small>' + esc(DELTA_LABEL[edge['delta']]) + '</small> <span aria-hidden="true">→</span></span>'
                    '<span class="ht-change-flow-node" data-change-node="' + esc(target['id']) + '"><strong>' + esc(target['label']) + '</strong><small>' + esc(DELTA_LABEL[target['delta']]) + '</small></span></div>'
                    '<p>' + esc(step['explanation']) + ' · 근거: ' + esc(BASIS_LABEL[edge['basis']]) + ((' · 한계: ' + esc(edge['limitation'])) if edge['limitation'] else '') + '</p></li>')
            body.append('</ol><div class="ht-change-flow-controls" data-change-flow-controls hidden><button type="button">이전 단계</button><button type="button">다음 단계</button><button type="button">처음으로</button></div></div>')
        first_evidence = [ident for ident, origins in links.items() if origins and origins[0][1] == index]
        if first_evidence:
            body.append('<div class="ht-change-evidence-grid">')
            body.extend(('evidence', ident) for ident in first_evidence)
            body.append('</div>')
        body.append('</section>')
    body.append(outro)
    body.append('<section id="change-evidence"><h2>변경 근거</h2>')
    for unit in model['units']:
        if unit['disposition'] != 'primary':
            body.append('<p>변경 단위 ' + esc(unit['id']) + ': ' + esc(unit['disposition']) + ' · ' + esc(unit['reason']) + '</p>')
    languages={'.py':'python','.ts':'typescript','.tsx':'typescript','.js':'javascript','.jsx':'javascript','.json':'json','.kt':'kotlin','.diff':'diff'}
    rendered = {}
    for item in model['evidence']:
        fragments = []
        ident=item['id']; label=esc(item['version']) + ' / ' + esc(item['path'])
        if item['start'] is not None: label += ':' + str(item['start']) + '-' + str(item['end'])
        fragments.append('<article id="evidence-' + esc(ident) + '" class="ht-change-evidence"><h3>' + label + '</h3>')
        if item['availability']=='unavailable': fragments.append('<p>확인할 수 없는 근거: ' + esc(item['reason']) + '</p>')
        else:
            original=src[(item['kind'],item['version'],item['path'])]
            excerpt=''.join(original.splitlines(keepends=True)[item['start']-1:item['end']]) if item['start'] is not None else ''
            if not excerpt: fragments.append('<p>' + ('빈 메타데이터' if item['kind']=='metadata' else '빈 파일') + '</p>')
            elif item['kind']=='metadata': fragments.append('<p>변경 메타데이터</p><p class="ht-change-metadata">' + esc(excerpt) + '</p>')
            else: fragments.append(highlight_code.highlight(excerpt,languages.get(Path(item['path']).suffix.lower(),''),item['start']))
        if links[ident]:
            fragments.append('<p data-ht-backlinks="evidence-' + esc(ident) + '">돌아가기: ')
            for origin, group_index, position in links[ident]:
                fragments.append('<a href="#' + origin + '">그룹 ' + str(group_index) + ' [' + str(position) + ']</a> ')
            fragments.append('</p>')
        fragments.append('</article>')
        rendered[ident] = '\n'.join(fragments)
    body.extend(('evidence', ident) for ident in rendered if not links[ident])
    body.append('</section>')
    return '\n'.join(rendered[item[1]] if isinstance(item, tuple) else item for item in body)



def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('model','sources','output'): parser.add_argument('--'+name,required=True,type=Path)
    for name in ('intro','outro'): parser.add_argument('--'+name,type=Path)
    parser.add_argument('--theme',choices=('system','light','dark')); parser.add_argument('--lang',default='ko'); parser.add_argument('--replace',action='store_true');args=parser.parse_args()
    try:
        if args.output.is_symlink() or args.output.exists() and (not args.replace or not args.output.is_file() or args.output.stat().st_nlink != 1):
            raise ValueError('output exists or is unsafe; use a fresh path or authorized --replace')
        model=json.loads(args.model.read_text(encoding='utf-8')); sources=json.loads(args.sources.read_text(encoding='utf-8'))
        intro=args.intro.read_text(encoding='utf-8') if args.intro else ''; outro=args.outro.read_text(encoding='utf-8') if args.outro else ''
        body=render_body(model,sources,intro,outro)
        build_html.assemble(body,model['title'],theme=args.theme or 'system',lang=args.lang,profile='change',warn_plain_pre=False)
        theme,notes=build_html.resolve_theme(args.theme)
        result=build_html.assemble(body,model['title'],theme=theme,lang=args.lang,profile='change')
        with args.output.open('w' if args.replace else 'x',encoding='utf-8') as stream: stream.write(result)
        for note in notes: print(note)
        print('Built '+str(args.output)+'; structural and supplied-source checks only; content and requested screen checks remain.')
    except (OSError,UnicodeError,ValueError) as error: parser.exit(1,str(error)+'\n')

if __name__ == '__main__': main()
