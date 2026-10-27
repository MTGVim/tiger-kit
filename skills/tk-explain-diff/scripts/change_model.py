#!/usr/bin/env python3
"""Validate a change model against the supplied source bundle, without I/O side effects."""
import argparse
import hashlib
import json
import re

SLUG = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$')
HEX = re.compile(r'^[0-9a-fA-F]+$')


class Validator:
    def __init__(self):
        self.errors = []

    def error(self, code, path, message):
        self.errors.append({'code': code, 'path': path, 'message': message})

    def obj(self, value, path, required, optional=()):
        if not isinstance(value, dict):
            self.error('TYPE', path, 'expected object'); return False
        for key in sorted(set(required) - set(value)):
            self.error('MISSING', f'{path}.{key}', 'required field missing')
        for key in sorted(set(value) - set(required) - set(optional)):
            self.error('UNKNOWN_KEY', f'{path}.{key}', 'unknown field')
        return True

    def string(self, value, path, nullable=False):
        if value is None and nullable: return True
        if not isinstance(value, str) or not value.strip():
            self.error('TYPE', path, 'expected nonempty string' + (' or null' if nullable else '')); return False
        return True

    def choice(self, value, path, choices):
        if not isinstance(value, str) or value not in choices:
            self.error('VALUE', path, 'expected one of ' + ', '.join(choices)); return False
        return True

    def array(self, value, path):
        if not isinstance(value, list):
            self.error('TYPE', path, 'expected array'); return []
        return value

    def ident(self, value, path):
        if not isinstance(value, str) or not SLUG.fullmatch(value):
            self.error('ID', path, 'expected ASCII slug'); return False
        return True

    def path(self, value, path):
        if not self.string(value, path): return False
        if ('\\' in value or '\x00' in value or value.startswith('/') or '://' in value or
            any(p in ('', '.', '..') for p in value.split('/')) or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value)):
            self.error('PATH', path, 'expected safe repository-relative path'); return False
        return True

    def unique(self, rows, path):
        result = {}
        for i, row in enumerate(self.array(rows, path)):
            p = f'{path}[{i}]'
            if not isinstance(row, dict): self.error('TYPE', p, 'expected object'); continue
            identifier = row.get('id')
            if not self.ident(identifier, p + '.id'): continue
            if identifier in result: self.error('DUPLICATE_ID', p + '.id', 'duplicate id')
            else: result[identifier] = row
        return result

    def refs(self, values, path, known, kind):
        out = []
        for i, value in enumerate(self.array(values, path)):
            p = f'{path}[{i}]'
            if not self.ident(value, p): continue
            if value not in known: self.error('UNKNOWN_' + kind, p, f'unknown {kind.lower()} id {value!r}')
            else: out.append(value)
        return out


def validate_model(model, sources):
    v = Validator()
    if not v.obj(model, 'model', ('schema_version','title','summary','snapshot','inventory_complete','inventory_limit','units','evidence','groups'), ('graph',)):
        return v.errors
    if type(model.get('schema_version')) is not int or model.get('schema_version') != 1:
        v.error('VERSION', 'model.schema_version', 'expected 1')
    for key in ('title','summary'): v.string(model.get(key), 'model.' + key)
    if type(model.get('inventory_complete')) is not bool: v.error('TYPE','model.inventory_complete','expected boolean')
    v.string(model.get('inventory_limit'), 'model.inventory_limit', nullable=True)
    if model.get('inventory_complete') is False and not model.get('inventory_limit'):
        v.error('LIMITATION','model.inventory_limit','incomplete inventory needs a limitation')

    snapshot = model.get('snapshot')
    versions = {}
    if v.obj(snapshot, 'snapshot', ('repository','comparison','from','to','versions')):
        v.string(snapshot.get('repository'), 'snapshot.repository')
        v.choice(snapshot.get('comparison'), 'snapshot.comparison', ('merge-base','range','workspace','synthetic'))
        raw = snapshot.get('versions')
        if not isinstance(raw, dict): v.error('TYPE','snapshot.versions','expected object')
        else:
            for key, value in raw.items():
                p = 'snapshot.versions.' + str(key)
                if not v.ident(key,p): continue
                if not v.obj(value,p,('kind','id')): continue
                kind = value.get('kind'); ident = value.get('id')
                v.choice(kind,p+'.kind',('commit','index','worktree','untracked','synthetic'))
                if v.string(ident,p+'.id'):
                    if kind == 'commit' and (len(ident) not in (40,64) or not HEX.fullmatch(ident)):
                        v.error('FINGERPRINT',p+'.id','commit requires full 40 or 64 character hex SHA')
                    if kind in ('index','worktree','untracked') and (len(ident) != 64 or not HEX.fullmatch(ident)):
                        v.error('FINGERPRINT',p+'.id','workspace state requires SHA256 fingerprint')
                versions[key] = value
        for key in ('from','to'):
            value = snapshot.get(key)
            if not isinstance(value,str) or value not in versions: v.error('UNKNOWN_VERSION','snapshot.'+key,'unknown version')
        if snapshot.get('from') == snapshot.get('to'): v.error('ENDPOINT','snapshot.to','endpoints must differ')
    else: snapshot = {}
    before_version, after_version = snapshot.get('from'), snapshot.get('to')

    bundle = {}
    if v.obj(sources,'sources',('schema_version','files')):
        if type(sources.get('schema_version')) is not int or sources.get('schema_version') != 1: v.error('VERSION','sources.schema_version','expected 1')
        for i, item in enumerate(v.array(sources.get('files'),'sources.files')):
            p = f'sources.files[{i}]'
            if not v.obj(item,p,('kind','version','path','text')): continue
            kind,version,path,text = (item.get(k) for k in ('kind','version','path','text'))
            valid = v.choice(kind,p+'.kind',('text','metadata')) & v.path(path,p+'.path')
            if not isinstance(version,str) or version not in versions: v.error('UNKNOWN_VERSION',p+'.version','unknown version'); valid=False
            if not isinstance(text,str): v.error('TYPE',p+'.text','expected string'); valid=False
            if valid:
                key=(kind,version,path)
                if key in bundle: v.error('DUPLICATE_SOURCE',p,'duplicate source identity')
                else: bundle[key]=text

    evidence = v.unique(model.get('evidence'),'evidence')
    for i, e in enumerate(v.array(model.get('evidence'),'evidence')):
        p=f'evidence[{i}]'
        if not v.obj(e,p,('id','kind','version','path','start','end','availability','sha256','reason')): continue
        kind,version,path = e.get('kind'),e.get('version'),e.get('path')
        kind_ok = v.choice(kind,p+'.kind',('text','metadata')); path_ok = v.path(path,p+'.path')
        if not isinstance(version,str) or version not in versions: v.error('UNKNOWN_VERSION',p+'.version','unknown version')
        available = e.get('availability'); v.choice(available,p+'.availability',('available','unavailable'))
        v.string(e.get('reason'),p+'.reason',nullable=True)
        start,end=e.get('start'),e.get('end'); digest=e.get('sha256')
        if (start is None) != (end is None) or any(type(x) is not int for x in (start,end) if x is not None):
            v.error('RANGE',p,'range must be two integers or two nulls')
        elif start is not None and (start < 1 or end < start): v.error('RANGE',p,'invalid inclusive range')
        if available == 'unavailable':
            if digest is not None: v.error('DIGEST',p+'.sha256','unavailable evidence requires null digest')
            if not e.get('reason'): v.error('REASON',p+'.reason','unavailable evidence needs reason')
        elif available == 'available':
            key=(kind,version,path) if kind_ok and path_ok and isinstance(version,str) else None
            if key not in bundle: v.error('MISSING_SOURCE',p,'available evidence requires source bundle entry')
            else:
                text=bundle[key]; expected=hashlib.sha256(text.encode('utf-8')).hexdigest(); lines=text.splitlines()
                if digest != expected: v.error('DIGEST',p+'.sha256','source digest mismatch')
                if not lines:
                    if start is not None or end is not None: v.error('RANGE',p,'empty source requires null range')
                elif type(start) is not int or type(end) is not int or start < 1 or end < start or end > len(lines):
                    v.error('RANGE',p,'source range out of bounds')
    units=v.unique(model.get('units'),'units')
    unit_refs={}
    for i,u in enumerate(v.array(model.get('units'),'units')):
        p=f'units[{i}]'
        if not v.obj(u,p,('id','kind','before','after','disposition','reason')): continue
        v.choice(u.get('kind'),p+'.kind',('text','rename','binary','mode','submodule'))
        v.choice(u.get('disposition'),p+'.disposition',('primary','secondary','unavailable'))
        v.string(u.get('reason'),p+'.reason',nullable=True)
        if u.get('disposition') in ('secondary','unavailable') and not u.get('reason'): v.error('REASON',p+'.reason','disposition needs reason')
        for side,version in (('before',before_version),('after',after_version)):
            refs=v.refs(u.get(side),p+'.'+side,evidence,'EVIDENCE')
            for ident in refs:
                if evidence[ident].get('version') != version: v.error('ENDPOINT',p+'.'+side,f'evidence {ident!r} has wrong version')
        if isinstance(u.get('id'),str): unit_refs[u['id']]=u

    groups=v.unique(model.get('groups'),'groups'); seen=set(); covered=set()
    if units and not groups: v.error('MISSING_GROUP','groups','changed units need groups')
    def claim(value,path,version=None):
        if not v.obj(value,path,('text','basis','evidence','limitation')): return
        v.string(value.get('text'),path+'.text'); basis=value.get('basis')
        v.choice(basis,path+'.basis',('source','inference','unverified')); v.string(value.get('limitation'),path+'.limitation',nullable=True)
        refs=v.refs(value.get('evidence'),path+'.evidence',evidence,'EVIDENCE')
        if basis == 'source' and not any(evidence[x].get('availability') == 'available' for x in refs): v.error('SOURCE_REQUIRED',path+'.evidence','source claim needs available evidence')
        if basis in ('inference','unverified') and not value.get('limitation'): v.error('LIMITATION',path+'.limitation','claim needs limitation')
        if version is not None and basis == 'source':
            for ident in refs:
                if evidence[ident].get('version') != version: v.error('ENDPOINT',path+'.evidence',f'evidence {ident!r} has wrong version')
    for i,g in enumerate(v.array(model.get('groups'),'groups')):
        p=f'groups[{i}]'
        if not v.obj(g,p,('id','title','summary','unit_ids','evidence_ids','depends_on','before','after','invariants','checkpoints','limitations')): continue
        for k in ('title','summary'): v.string(g.get(k),p+'.'+k)
        covered.update(v.refs(g.get('unit_ids'),p+'.unit_ids',units,'UNIT'))
        v.refs(g.get('evidence_ids'),p+'.evidence_ids',evidence,'EVIDENCE')
        deps=v.refs(g.get('depends_on'),p+'.depends_on',groups,'GROUP')
        for dep in deps:
            if dep not in seen: v.error('DEPENDENCY_ORDER',p+'.depends_on','dependency must precede this group')
        if isinstance(g.get('id'),str): seen.add(g['id'])
        claim(g.get('before'),p+'.before',before_version); claim(g.get('after'),p+'.after',after_version)
        for j,c in enumerate(v.array(g.get('invariants'),p+'.invariants')): claim(c,f'{p}.invariants[{j}]')
        for k in ('checkpoints','limitations'):
            for j,text in enumerate(v.array(g.get(k),p+'.'+k)): v.string(text,f'{p}.{k}[{j}]')
    for ident,u in units.items():
        if u.get('disposition') == 'primary' and ident not in covered: v.error('ORPHAN_UNIT','units.'+ident,'primary unit is not covered')

    if 'graph' in model:
        graph=model['graph']
        if v.obj(graph,'graph',('nodes','edges','flows')):
            nodes=v.unique(graph.get('nodes'),'graph.nodes'); edges=v.unique(graph.get('edges'),'graph.edges'); v.unique(graph.get('flows'),'graph.flows')
            def presence(item,p):
                delta=item.get('delta'); v.choice(delta,p+'.delta',('added','modified','removed','unchanged'))
                vv=v.refs(item.get('versions'),p+'.versions',versions,'VERSION')
                if before_version in versions and after_version in versions:
                    expected={'added':(False,True),'removed':(True,False),'modified':(True,True),'unchanged':(True,True)}.get(delta) if isinstance(delta,str) else None
                    if expected and (before_version in vv,after_version in vv) != expected: v.error('PRESENCE',p+'.versions','delta does not match endpoint presence')
                refs=v.refs(item.get('evidence_ids'),p+'.evidence_ids',evidence,'EVIDENCE')
                for ident in refs:
                    if evidence[ident].get('version') not in vv:
                        v.error('PRESENCE',p+'.evidence_ids',f'evidence {ident!r} is absent from element versions')
                return vv
            for i,n in enumerate(v.array(graph.get('nodes'),'graph.nodes')):
                p=f'graph.nodes[{i}]'
                if v.obj(n,p,('id','label','delta','versions','evidence_ids')): v.string(n.get('label'),p+'.label'); presence(n,p)
            for i,e in enumerate(v.array(graph.get('edges'),'graph.edges')):
                p=f'graph.edges[{i}]'
                if not v.obj(e,p,('id','from','to','label','delta','versions','basis','evidence_ids','limitation')): continue
                v.string(e.get('label'),p+'.label'); vv=presence(e,p); basis=e.get('basis');v.choice(basis,p+'.basis',('source','inference','unverified'));v.string(e.get('limitation'),p+'.limitation',nullable=True)
                if basis in ('inference','unverified') and not e.get('limitation'): v.error('LIMITATION',p+'.limitation','relationship needs limitation')
                if basis == 'source' and not any(evidence.get(x,{}).get('availability') == 'available' for x in (e.get('evidence_ids') if isinstance(e.get('evidence_ids'),list) else []) if isinstance(x,str)): v.error('SOURCE_REQUIRED',p+'.evidence_ids','source relationship needs available evidence')
                for end in ('from','to'):
                    node=e.get(end)
                    if not isinstance(node,str) or node not in nodes: v.error('UNKNOWN_NODE',p+'.'+end,'unknown node')
                    elif not isinstance(nodes[node].get('versions'),list) or any(x not in nodes[node]['versions'] for x in vv): v.error('PRESENCE',p+'.'+end,'node absent in edge version')
            for i,f in enumerate(v.array(graph.get('flows'),'graph.flows')):
                p=f'graph.flows[{i}]'
                if not v.obj(f,p,('id','title','group_id','version','steps')): continue
                v.string(f.get('title'),p+'.title'); group=f.get('group_id'); version=f.get('version')
                if not isinstance(group,str) or group not in groups: v.error('UNKNOWN_GROUP',p+'.group_id','unknown group')
                if not isinstance(version,str) or version not in versions: v.error('UNKNOWN_VERSION',p+'.version','unknown version')
                v.unique(f.get('steps'),p+'.steps')
                for j,step in enumerate(v.array(f.get('steps'),p+'.steps')):
                    q=f'{p}.steps[{j}]'
                    if not v.obj(step,q,('id','edge_id','explanation')): continue
                    v.string(step.get('explanation'),q+'.explanation'); edge=step.get('edge_id')
                    if not isinstance(edge,str) or edge not in edges: v.error('UNKNOWN_EDGE',q+'.edge_id','unknown edge')
                    elif not isinstance(edges[edge].get('versions'),list) or version not in edges[edge]['versions']: v.error('PRESENCE',q+'.edge_id','edge absent in flow version')
    return v.errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--model',required=True);parser.add_argument('--sources',required=True);args=parser.parse_args()
    try:
        with open(args.model,encoding='utf-8') as stream: model=json.load(stream)
        with open(args.sources,encoding='utf-8') as stream: sources=json.load(stream)
        errors=validate_model(model,sources)
    except (OSError,UnicodeError,ValueError) as error:
        parser.exit(2, f'Input error: {error}\n')
    if errors:
        print(json.dumps(errors,ensure_ascii=False,indent=2));return 1
    print('Valid structure and supplied source bundle; Git, completeness and interpretation were not verified.')
    if not model['inventory_complete']: print('Inventory incomplete: ' + model['inventory_limit'])
    unavailable=[e['id'] for e in model['evidence'] if e['availability']=='unavailable']
    if unavailable: print('Unavailable evidence: ' + ', '.join(unavailable))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
