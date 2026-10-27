#!/usr/bin/env python3
"""Resolve optional durable explanation and learning paths for one Git repository."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile


def settings_path():
    return Path(os.environ.get('XDG_CONFIG_HOME') or Path.home()/'.config')/'tigerkit'/'settings.json'


def safe_path(value):
    if not isinstance(value,str) or not value.strip(): raise ValueError('path must be a nonempty string')
    if value.startswith('~') and value != '~' and not value.startswith('~/'): raise ValueError('only the current user home may be expanded')
    expanded=os.path.expanduser(value)
    if not os.path.isabs(expanded): raise ValueError('path must be absolute or start with ~/')
    if '..' in Path(expanded).parts: raise ValueError('parent traversal is not allowed')
    path=Path(os.path.abspath(expanded))
    if path.resolve(strict=False)!=path: raise ValueError('path must not traverse a symlink')
    return path


def checked_settings():
    path=safe_path(str(settings_path()))
    if not path.exists(): return path,{},None
    info=path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1: raise ValueError('settings must be a regular unshared file')
    data=path.read_bytes()
    try: value=json.loads(data.decode('utf-8'))
    except (UnicodeError,ValueError): raise ValueError('settings are unreadable or malformed') from None
    if not isinstance(value,dict): raise ValueError('settings must be an object')
    return path,value,data


def status():
    try:
        _,data,_=checked_settings()
        if 'artifacts' not in data:return {'status':'missing','needs_choice':True}
        if not isinstance(data['artifacts'],dict):raise ValueError('artifacts must be an object')
        options=data['artifacts']
        if 'durableRoot' not in options:return {'status':'missing','needs_choice':True}
        value=options['durableRoot']
        if value is None or isinstance(value,str) and not value.strip():return {'status':'disabled','needs_choice':False}
        root=safe_path(value)
        if root.exists() and not root.is_dir():raise ValueError('durable root must be a directory')
        return {'status':'configured','needs_choice':False,'root':str(root)}
    except (OSError,ValueError) as error:
        return {'status':'invalid','needs_choice':False,'warning':str(error)}


def git(repo,*args):
    result=subprocess.run(['git','-C',str(repo),*args],capture_output=True,check=False)
    if result.returncode:raise ValueError('cannot identify repository: '+result.stderr.decode('utf-8','replace').strip())
    return result.stdout


def repository(repo):
    repo=Path(repo).absolute()
    top=Path(os.fsdecode(git(repo,'rev-parse','--show-toplevel')).strip()).resolve()
    common_text=os.fsdecode(git(top,'rev-parse','--git-common-dir')).strip()
    common=Path(common_text)
    if not common.is_absolute():common=top/common
    common=common.resolve()
    name=common.parent.name if common.name=='.git' else common.name
    name=re.sub(r'[^a-zA-Z0-9._-]+','-',name).strip('.-') or 'repository'
    digest=hashlib.sha256(os.fsencode(str(common))).hexdigest()[:8]
    raw=git(top,'worktree','list','--porcelain','-z')
    worktrees=[Path(os.fsdecode(part[len(b'worktree '):])).resolve() for part in raw.split(b'\0') if part.startswith(b'worktree ')]
    return top,common,name+'-'+digest,worktrees


def outside(root,top,common,worktrees):
    if any(root==p or root.is_relative_to(p) for p in (top,common,*worktrees)):
        raise ValueError('durable root must be outside every worktree and common Git directory')


def make_private_directory(path):
    path=safe_path(str(path))
    missing=[]; current=path
    while not current.exists():missing.append(current);current=current.parent
    if not current.is_dir():raise ValueError('directory parent is not a directory')
    for item in reversed(missing):
        try:item.mkdir(mode=0o700)
        except FileExistsError:pass
        if item.is_symlink() or not item.is_dir():raise ValueError('unsafe directory during creation')
        if item in missing and stat.S_IMODE(item.stat().st_mode) & 0o077:
            raise ValueError('new directory permissions are not private')
    safe_path(str(path))


def choose(value=None,disable=False,repo='.'):
    if (value is None)==(not disable): raise ValueError('choose a path or disable')
    path,data,original=checked_settings()
    if 'artifacts' in data and not isinstance(data['artifacts'],dict):raise ValueError('artifacts must be an object')
    options=data.setdefault('artifacts',{})
    if 'durableRoot' in options:raise ValueError('durableRoot already has a choice; preserve it')
    if disable: selected=None
    else:
        selected=value; root=safe_path(value);top,common,_,worktrees=repository(repo);outside(root,top,common,worktrees)
    options['durableRoot']=selected
    make_private_directory(path.parent)
    payload=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    mode = stat.S_IMODE(path.stat().st_mode) if original is not None else 0o600
    fd,tmp=tempfile.mkstemp(prefix='.settings-',dir=path.parent)
    try:
        os.fchmod(fd,mode)
        with os.fdopen(fd,'wb') as stream:stream.write(payload);stream.flush();os.fsync(stream.fileno())
        if original is None:
            os.link(tmp,path,follow_symlinks=False)
        else:
            _,_,current=checked_settings()
            if current!=original:raise ValueError('settings changed while recording the choice')
            os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return status()


def check_slug(slug):
    if (not isinstance(slug,str) or not slug.strip() or slug in ('.','..') or
        '/' in slug or '\\' in slug or any(ord(c)<32 or ord(c)==127 for c in slug)):
        raise ValueError('slug must be one safe path component')
    return slug


def resolve(repo,kind,slug,explicit=None,create=False):
    if kind not in ('explanations','study'):raise ValueError('unsupported artifact kind')
    top,common,key,worktrees=repository(repo)
    setting=status()
    if explicit is not None:
        expanded=os.path.expanduser(explicit)
        raw=Path(expanded) if os.path.isabs(expanded) else top/expanded
        cursor=Path(raw.anchor)
        for part in raw.parts[1:]:
            if part == '..': cursor=cursor.parent
            else:
                cursor=cursor/part
                if cursor.is_symlink():raise ValueError('explicit path must not traverse a symlink')
        target=safe_path(os.path.abspath(str(raw)))
        if raw.resolve(strict=False)!=target:raise ValueError('explicit path must not traverse a symlink')
        return {'path':str(target),'source':'explicit','settings':setting}
    check_slug(slug)
    if setting['status']=='configured':
        try:
            root=safe_path(setting['root']);outside(root,top,common,worktrees)
            base=root/key/('explanations' if kind=='explanations' else 'study')
            safe_path(str(base));source='durable'
        except (ValueError,OSError) as error:
            setting={'status':'invalid','needs_choice':False,'warning':str(error)}
    if setting['status']!='configured':
        base=top/'.tigerkit'/('explanations' if kind=='explanations' else 'teach');source='repository'
    candidate=base/(slug+'.html' if kind=='explanations' else slug)
    number=2
    while candidate.exists() or candidate.is_symlink():
        candidate=base/(f'{slug}-{number}.html' if kind=='explanations' else f'{slug}-{number}');number+=1
    if source=='durable' and create:
        make_private_directory(candidate.parent)
        if kind=='study':
            while True:
                try: candidate.mkdir(mode=0o700); break
                except FileExistsError:
                    candidate=base/f'{slug}-{number}';number+=1
        safe_path(str(candidate))
    return {'path':str(candidate),'source':source,'repo_key':key,'settings':setting}


def resume_homes(repo,slug=None):
    if slug is not None:check_slug(slug)
    top,common,key,worktrees=repository(repo);result=[];warnings=[];setting=status();parents=[]
    if setting['status']=='configured':
        try:
            root=safe_path(setting['root']);outside(root,top,common,worktrees)
            parents.append(safe_path(str(root/key/'study')))
        except (OSError,ValueError) as error: setting={'status':'invalid','needs_choice':False,'warning':str(error)}
    parents.extend(top/'.tigerkit'/parent for parent in ('teach','study'))
    for parent in parents:
        try:
            if safe_path(str(parent)) != parent or not parent.is_dir():continue
            candidates=[parent/slug] if slug is not None else sorted(parent.iterdir())
            for candidate in candidates:
                if candidate.is_dir() and not candidate.is_symlink() and safe_path(str(candidate)) == candidate:
                    result.append(str(candidate))
        except (OSError,ValueError) as error:
            warnings.append(str(parent)+': '+str(error))
    return {'homes':result,'repo_key':key,'settings':setting,'warnings':warnings}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    sub.add_parser('status')
    c=sub.add_parser('choose');group=c.add_mutually_exclusive_group(required=True);group.add_argument('--root');group.add_argument('--disable',action='store_true');c.add_argument('--repo',default='.')
    r=sub.add_parser('resolve');r.add_argument('--repo',default='.');r.add_argument('--kind',choices=('explanations','study'),required=True);r.add_argument('--slug');r.add_argument('--explicit');r.add_argument('--create',action='store_true')
    h=sub.add_parser('resume');h.add_argument('--repo',default='.');h.add_argument('--slug')
    args=parser.parse_args()
    try:
        if args.action=='status': result=status()
        elif args.action=='choose':result=choose(args.root,args.disable,args.repo)
        elif args.action=='resolve':result=resolve(args.repo,args.kind,args.slug,args.explicit,args.create)
        else:
            result=resume_homes(args.repo,args.slug)
        print(json.dumps(result,ensure_ascii=False));return 0
    except (OSError,ValueError) as error:parser.exit(1,str(error)+'\n')

if __name__=='__main__':raise SystemExit(main())
