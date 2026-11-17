#!/usr/bin/env python3
"""TigerKit Mission Control: cooperative, per-worktree rollover (POSIX, Python 3.10+)."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time
import uuid

HOSTS = {'claude': '/exit', 'codex': '/quit', 'hermes': '/exit'}
SECTIONS = ('Mission', 'Current position', 'Milestones', 'Decisions and rationale', 'Failed approaches', 'Future work', 'Evidence and completion')
HANDOFF_FIELDS = ('Goal/Seed', 'Status', 'Repository state', 'Decisions', 'Verification', 'Completed work', 'Remaining work', 'Next step')
STOP = {'completed', 'blocked', 'aborted', 'waiting_user', 'unverifiable'}
MAX = 256_000

class Halt(Exception): pass

def require(ok, message):
    if not ok: raise Halt(message)

def read(p):
    require(p.is_file() and not p.is_symlink(), f'Missing or unsafe file: {p}')
    require(p.stat().st_size <= MAX, f'File too large: {p}')
    return p.read_text(encoding='utf-8')

def load(p):
    return json.loads(read(p))

def digest(p):
    return hashlib.sha256(read(p).encode()).hexdigest()

def section(body, name):
    matches=re.findall(r'^## '+re.escape(name)+r' *\n(.*?)(?=^## |\Z)',body,re.M|re.S)
    require(len(matches)==1 and matches[0].strip(),f'Missing, duplicate or empty section: {name}')
    return matches[0].strip()

def mission_digest(body):
    return hashlib.sha256(section(body,'Mission').encode()).hexdigest()

def atomic(p, data):
    require(not p.is_symlink(), f'Symlink: {p}')
    fd, tmp = tempfile.mkstemp(prefix='.tmp-', dir=p.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, p)
        d = os.open(p.parent, os.O_RDONLY)
        try: os.fsync(d)
        finally: os.close(d)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def save(p, data): atomic(p, json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True, timeout=8).strip()

def repo(root):
    require(Path(git(root, 'rev-parse', '--show-toplevel')).resolve() == root, 'Not the configured worktree root')
    return {'root': str(root), 'head': git(root, 'rev-parse', 'HEAD'), 'branch': git(root, 'rev-parse', '--abbrev-ref', 'HEAD')}

def outside(p, root):
    require(not p.is_relative_to(root), 'State directory must be outside worktree')

class Orca:
    def __init__(self, c): self.c = c
    def call(self, *args, timeout=12, allow_wait=False):
        r = subprocess.run([self.c['orca'], *args, '--environment', 'local', '--json'], cwd=self.c['root'], capture_output=True, text=True, timeout=timeout)
        try: data = json.loads(r.stdout)
        except ValueError: raise Halt(f'Orca returned no valid JSON: {args[:2]}; inspect stderr locally')
        require(data.get('ok') is True and (r.returncode == 0 or allow_wait), f'Orca failure: {args[:2]}')
        require(isinstance(data.get('result'), dict), 'Missing result')
        return data['result']
    def caller(self): return os.environ.get('ORCA_TERMINAL_HANDLE')
    def show(self, h): return self.call('terminal','show','--terminal',h)['terminal']
    def screen(self, h): return self.call('terminal','read','--terminal',h,'--screen')['terminal']
    def wait(self, h, condition):
        return self.call('terminal','wait','--terminal',h,'--for',condition,'--timeout-ms','1000',allow_wait=True)['wait']
    def send(self,h,text):
        return self.call('terminal','send','--terminal',h,'--text',text,'--enter')['send']
    def notify(self,h,request_path):
        return self.call('orchestration','send','--to',h,'--subject','Managed rollover requested','--body',f'Read {request_path} at the next safe boundary and follow the enrolled rollover protocol. Do not interrupt active work or broaden scope.')
    def launch(self,prompt):
        c=self.c
        args=['agent','launch','--agent',c['host'],'--worktree','id:'+c['worktree_id'],'--surface','terminal','--prompt',prompt]
        if c.get('model'): args += ['--model',c['model']]
        if c.get('effort'): args += ['--effort',c['effort']]
        return self.call(*args,timeout=35)

class ExternalAdapter:
    """Local, explicitly prepared executable; JSON on stdin/stdout, no shell."""
    def __init__(self,c): self.c=c
    def call(self,operation,**kwargs):
        p=Path(self.c['adapter'])
        require(p.is_absolute() and p.is_file() and not p.is_symlink(), 'Adapter missing or unsafe')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==self.c['adapter_sha256'],'Adapter changed; stop')
        data={'version':1,'operation':operation,'root':self.c['root'],'host':self.c['host'],
              'worktree_id':self.c.get('worktree_id'),'profile':self.c.get('profile'),
              'model':self.c.get('model'),'effort':self.c.get('effort'),**kwargs}
        r=subprocess.run([sys.executable,str(p)],input=json.dumps(data),cwd=self.c['root'],
                         text=True,capture_output=True,timeout=35)
        require(r.returncode==0,'Adapter failed: '+operation)
        obj=json.loads(r.stdout)
        require(isinstance(obj,dict) and obj.get('ok') is True and 'result' in obj,'Invalid adapter receipt')
        return obj['result']
    def caller(self): return self.call('caller')
    def show(self,h): return self.call('show',handle=h)
    def screen(self,h): return self.call('screen',handle=h)
    def wait(self,h,condition): return self.call('wait',handle=h,condition=condition)
    def send(self,h,text): return self.call('send',handle=h,text=text)
    def notify(self,h,request_path): return self.call('notify',handle=h,request_path=request_path)
    def launch(self,prompt): return self.call('launch',prompt=prompt)

def transport(c):
    return ExternalAdapter(c) if c.get('adapter') else Orca(c)

def run_path(root):
    root=root.resolve()
    repo(root)
    home=Path(os.environ.get('XDG_STATE_HOME') or Path.home()/'.local/state').expanduser()
    require(home.is_absolute(),'XDG_STATE_HOME must be absolute')
    d=home/'tigerkit'/'missions'/hashlib.sha256(os.fsencode(root)).hexdigest()[:24]
    outside(d.resolve(),root)
    return d

def safe_dir(d):
    require(not any(p.is_symlink() for p in (d,*d.parents)), 'Symlink in state path')
    require(d.is_dir() and d.stat().st_uid==os.getuid() and d.stat().st_mode & 0o077==0,'Unsafe state directory')

class Run:
    def __init__(self, directory, orca_factory=transport):
        self.d=directory.resolve(); self.c=load(self.d/'config.json'); self.s=load(self.d/'state.json'); self.root=Path(self.c['root']).resolve()
        outside(self.d,self.root); require(self.d.stat().st_uid==os.getuid() and self.d.stat().st_mode & 0o077 == 0,'State directory must be private (0700)')
        self.o=orca_factory(self.c)
    def persist(self, **kw):
        old=self.s['phase']
        self.s.update(kw)
        if self.s['phase']!=old:
            event={'time':time.time(),'phase':self.s['phase'],'generation':self.s['generation']}
            self.s['events']=(self.s.get('events',[])+[event])[-40:]
        save(self.d/'state.json',self.s)
    def identity(self, h=None, expected=True):
        t=self.o.show(h or self.s['handle'])
        require(t.get('worktreeId')==self.c['worktree_id'] and Path(t['worktreePath']).resolve()==self.root,'Wrong worktree')
        require(t.get('executionHostId')==self.c['execution_host'] and t.get('incarnationId'),'Unverified host or incarnation')
        require(t.get('handle')==(h or self.s['handle']),'Unexpected terminal handle')
        if expected: require(t['incarnationId']==self.s['incarnation'],'Process incarnation changed; inspect manually')
        return t
    def live(self,t):
        require(t.get('agentIdentity')==self.c['host'], 'Agent identity mismatch or unknown')
        require(t.get('connected') is True and t.get('writable') is True and not t.get('orphaned') and t.get('verdict')=='live','Terminal not confirmed live/writable')
    def pressure(self):
        regex=self.c.get('pressure_regex')
        if not regex: return None
        screen=self.o.screen(self.s['handle'])
        if screen.get('source')!='screen' or screen.get('status')!='running': return None
        # Only one fully matched line in the configured footer. No transcript search.
        lines=screen.get('tail',[])[-self.c.get('footer_lines',4):]
        matches=[m for line in lines if (m:=re.fullmatch(regex,line.strip()))]
        if len(matches)!=1: return None
        n=float(matches[0].group('percent'))
        if not 0<=n<=100: return None
        return 100-n if self.c.get('pressure_kind')=='remaining' else n
    def enroll(self):
        require(self.s['phase']=='enrolling','Already enrolled')
        require(self.o.caller()==self.s['handle'],'Enroll from target pane')
        self.live(self.identity()); self.validate_strategy(); self.persist(phase='active',mission_sha256=mission_digest(read(self.d/'strategy.md')))
    def request(self, reason):
        require(self.s['phase']=='active','Not active')
        require(not (self.d/'stop.json').exists() and not self.s.get('paused'),'Run stopped or paused')
        self.live(self.identity()); self.validate_strategy(); current=repo(self.root)
        req={'id':uuid.uuid4().hex,'created':time.time(),'reason':reason,'generation':self.s['generation'],'repository':current}
        # Journal before publication, so a crash cannot create two requests.
        self.persist(phase='publishing',request=req)
        self.publish()
    def publish(self):
        req=self.s['request']; p=self.d/'request.json'
        if p.exists(): require(load(p)==req,'Unexpected request file')
        else: save(p,req)
        self.persist(phase='requested')
        if self.c.get('notify'):
            # The request file is authoritative; mail is a best-effort wake, never retried.
            try: self.o.notify(self.s['handle'],str(p))
            except (Halt,OSError,ValueError,KeyError,subprocess.SubprocessError): print('Notification not confirmed; cooperative polling remains active',file=sys.stderr)
    def paths(self):
        rid=self.s['request']['id']; return [self.d/f'{rid}.{suffix}' for suffix in ('handoff.md','ready.json')]
    def validate_strategy(self):
        if self.c.get('seed'):
            require(digest(Path(self.c['seed']))==self.c['seed_sha256'],'Original Seed changed; new approval required')
        body=read(self.d/'strategy.md')
        for name in SECTIONS: section(body,name)
        if self.s.get('mission_sha256'):
            require(mission_digest(body)==self.s['mission_sha256'],'Mission changed; stop and obtain approval')
        require(len(body)<=24000,'Strategy exceeds 24,000 chars; curate references')
    def validate_ready(self):
        hand,ready=self.paths(); obj=load(ready)
        require(obj.get('request_id')==self.s['request']['id'] and obj.get('generation')==self.s['generation'],'Stale ready receipt')
        require(obj.get('status')=='in_progress' and obj.get('safe_boundary') is True,'Not eligible for rollover')
        require(obj.get('repository')==repo(self.root),'Git identity drift since checkpoint')
        require(obj.get('worktree_digest')==worktree_digest(self.root),'Worktree changed after checkpoint')
        self.validate_strategy()
        require(obj.get('strategy_sha256')==digest(self.d/f'{self.s["request"]["id"]}.strategy.md') and obj.get('strategy_sha256')==digest(self.d/'strategy.md') and obj.get('handoff_sha256')==digest(hand),'Checkpoint hash mismatch')
        require(len(read(hand))<=48000,'Handoff too large')
        return obj
    def checkpoint(self):
        require(self.s['phase']=='requested','No pending request'); self.identity()
        hand,ready=self.paths(); self.validate_strategy(); body=read(hand)
        require(self.o.caller()==self.s['handle'],'Checkpoint must be sealed from the enrolled pane')
        require(all(re.search(r'^'+re.escape(x)+r':',body,re.M) for x in HANDOFF_FIELDS),'Handoff missing required fields')
        require(re.search(r'^Status:\s*in_progress\s*$',body,re.M),'Handoff is not in_progress')
        require(not ready.exists(),'Already sealed')
        require(f'Strategy: {self.d}/{self.s["request"]["id"]}.strategy.md' in body.splitlines(),'Missing exact strategy snapshot reference')
        atomic(self.d/f'{self.s["request"]["id"]}.strategy.md',read(self.d/'strategy.md'))
        save(ready,{'request_id':self.s['request']['id'],'generation':self.s['generation'],'status':'in_progress','safe_boundary':True,'repository':repo(self.root),'worktree_digest':worktree_digest(self.root),'strategy_sha256':digest(self.d/'strategy.md'),'handoff_sha256':digest(hand)})
    def launch_prompt(self):
        hand,_=self.paths(); script=self.c['script']; d=str(self.d)
        skill='$tk-handoff' if self.c['host']=='codex' else '/tk-handoff'
        cmd=shlex.join([self.c['python'],script,'--run',d,'ack'])
        profile=self.c.get('profile')
        verify=(f' Verify your actual provider session ID is fresh (old: {self.s.get("provider_session_id")}) and effective nonsecret profile equals {profile!r}. Append --session-id and --profile with observed values to the ack command. If unverified or different, stop without changes.' if profile else '')
        return (f'Read {self.c["protocol"]!r}, {str(self.d / "strategy.md")!r}, and {str(hand)!r}. Verify the handoff, Seed, repository and owner skill without changing files.'+verify+
                f' Before any work, run {cmd} from this new pane. If the launch receipt is pending, retry only ack after reading status. Wait until status shows active for your own handle. '
                f'Then invoke installed tk-handoff: {skill} --resume {str(hand)!r}. '
                'Preserve goal, approvals, milestones, failed approaches and completion gates. Do not repeat completed work or expand scope. Follow the mission protocol after resume; stop on user decisions or completion.')
    def tick(self):
        phase=self.s['phase']
        if (self.d/'stop.json').exists():
            stop=load(self.d/'stop.json'); require(stop.get('generation')==self.s['generation'] and stop.get('status') in STOP,'Invalid stop marker')
            self.persist(phase='stopped',stop=stop); return 'stopped'
        if phase=='active':
            self.live(self.identity()); p=self.pressure()
            self.persist(last_pressure=p, last_check=time.time())
            if self.s.get('paused'): return 'paused'
            self.validate_strategy()
            if p is not None and p>=self.c['threshold']: self.request(f'context used {p:.1f}%'); return 'requested'
            return 'below threshold or unverified'
        if phase=='publishing': self.publish(); return 'requested'
        if phase=='requested':
            if time.time()-self.s['request']['created']>self.c['request_timeout']: self.persist(phase='blocked',reason='handoff timeout'); return 'blocked'
            if not self.paths()[1].exists(): return 'waiting for cooperative checkpoint'
            self.validate_ready(); self.persist(phase='ready'); return 'ready'
        if phase=='ready':
            if time.time()-self.s['request']['created']>self.c['request_timeout']: self.persist(phase='blocked',reason='safe exit timeout'); return 'blocked'
            self.validate_ready(); t=self.identity()
            # An already exited PTY is acceptable only if Orca explicitly confirms it.
            w=self.o.wait(self.s['handle'],'exit')
            if w.get('satisfied') is True and w.get('status')=='exited' and w.get('exitCode')==0:
                self.persist(phase='exited'); return 'exited'
            if not self.c.get('auto_exit'): return 'waiting for clean exit (manual /exit or /quit)'
            self.live(t); screen=self.o.screen(self.s['handle'])
            if screen.get('source')!='screen' or screen.get('draft') or t.get('agentWait') is not None or 'agentWait' not in t: return 'not safe to send exit'
            w=self.o.wait(self.s['handle'],'tui-idle')
            if w.get('satisfied') is not True or w.get('blockedReason') or w.get('status')!='running': return 'waiting for idle'
            # No automatic retry of a mutation with ambiguous result.
            self.persist(phase='exit_sent',exit_sent_at=time.time())
            r=self.o.send(self.s['handle'],HOSTS[self.c['host']]); require(r.get('accepted') is True,'Exit not accepted; inspect')
            return 'exit sent'
        if phase=='exit_sent':
            self.identity(); w=self.o.wait(self.s['handle'],'exit')
            if w.get('satisfied') is True and w.get('status')=='exited' and w.get('exitCode')==0: self.persist(phase='exited'); return 'exited'
            if time.time()-self.s['exit_sent_at']>self.c['request_timeout']: self.persist(phase='blocked',reason='exit unconfirmed')
            return 'waiting for verified clean exit'
        if phase=='exited':
            self.validate_ready(); self.identity(); w=self.o.wait(self.s['handle'],'exit')
            require(w.get('satisfied') is True and w.get('status')=='exited' and w.get('exitCode')==0,'Old exit not confirmed')
            self.persist(phase='launching')
            r=self.o.launch(self.launch_prompt()); outcome=r.get('outcome',{}); h=outcome.get('handle')
            require(outcome.get('kind')=='terminal' and h and h!=self.s['handle'] and r.get('worktreeId')==self.c['worktree_id'],'Unexpected launch receipt; inspect, never retry blindly')
            new=self.identity(h,False)
            self.persist(phase='await_ack',new_handle=h,new_incarnation=new['incarnationId'],operation_id=r.get('operationId'),launched_at=time.time()); return 'awaiting resume ack'
        if phase=='await_ack':
            p=self.d/f'{self.s["request"]["id"]}.ack.json'
            if not p.exists():
                if time.time()-self.s['launched_at']>self.c['request_timeout']: self.persist(phase='blocked',reason='resume ack timeout')
                return 'waiting for ack'
            a=load(p); require(a.get('request_id')==self.s['request']['id'] and a.get('new_handle')==self.s['new_handle'] and a.get('generation')==self.s['generation']+1,'Wrong ack')
            if self.c.get('profile'):
                require(a.get('profile')==self.c['profile'] and a.get('session_id') and a['session_id']!=self.s.get('provider_session_id'),'Fresh session/profile not verified')
            t=self.identity(self.s['new_handle'],False); self.live(t); self.validate_ready()
            require(t['incarnationId']==self.s['new_incarnation'],'New incarnation changed')
            # Remove only our exact request, after ack. Archive is kept by immutable request id.
            require(load(self.d/'request.json')==self.s['request'],'Request changed')
            self.persist(phase='finalizing',next_incarnation=t['incarnationId'],next_session_id=a.get('session_id')); return self.finalize()
        if phase=='finalizing': return self.finalize()
        return f'{phase}: no automatic action'
    def finalize(self):
        p=self.d/'request.json'
        if p.exists(): require(load(p)==self.s['request'],'Request changed'); p.unlink()
        self.persist(phase='active',handle=self.s['new_handle'],incarnation=self.s['next_incarnation'],provider_session_id=self.s.get('next_session_id'),generation=self.s['generation']+1,request=None,last_pressure=None)
        return 'resumed'
    def ack(self,session_id=None,profile=None):
        require(self.s['phase']=='await_ack','Launch receipt not recorded yet; retry ack only')
        t=self.identity(self.s['new_handle'],False); self.live(t); self.validate_ready()
        require(t['incarnationId']==self.s['new_incarnation'],'New incarnation changed')
        require(self.o.caller()==self.s['new_handle'],'Missing or mismatched caller handle')
        if self.c.get('profile'):
            require(profile==self.c['profile'] and session_id and session_id!=self.s.get('provider_session_id'),'Fresh session/profile not verified')
        save(self.d/f'{self.s["request"]["id"]}.ack.json',{'request_id':self.s['request']['id'],'new_handle':self.s['new_handle'],'generation':self.s['generation']+1,'session_id':session_id,'profile':profile})


def worktree_digest(root):
    # Track staged/unstaged bytes and untracked regular files, not ignored build artifacts.
    h=hashlib.sha256()
    for args in [('diff','--no-ext-diff','--no-textconv','--binary','--cached','HEAD','--'),('diff','--no-ext-diff','--no-textconv','--binary','--'),('ls-files','--others','--exclude-standard','-z')]:
        b=subprocess.check_output(['git','-C',str(root),*args],timeout=12); h.update(b)
        if args[0]=='ls-files':
            for raw in sorted(x for x in b.split(b'\0') if x):
                p=root/os.fsdecode(raw); require(not p.is_symlink() and p.is_file() and p.resolve().is_relative_to(root),'Unsafe untracked file')
                require(p.stat().st_size<=32_000_000,'Untracked file too large for PoC checkpoint')
                h.update(raw); h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()

@contextlib.contextmanager
def lock(d,name='lock'):
    safe_dir(d)
    require(not (d/name).is_symlink(),'Unsafe lock')
    with open(d/name,'a') as f:
        try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise Halt('Another tick is running')
        yield

def stop_run(r,status):
    if not (r.d/'stop.json').exists():
        save(r.d/'stop.json',{'generation':r.s['generation'],'status':status})

def main():
    p=argparse.ArgumentParser(); p.add_argument('--run',type=Path); sub=p.add_subparsers(dest='cmd',required=True)
    path=sub.add_parser('path'); path.add_argument('--root',required=True,type=Path)
    init=sub.add_parser('init'); init.add_argument('--root',type=Path,required=True); init.add_argument('--handle'); init.add_argument('--host',choices=HOSTS,required=True); init.add_argument('--orca',default='orca'); init.add_argument('--adapter',type=Path); init.add_argument('--profile'); init.add_argument('--session-id'); init.add_argument('--model'); init.add_argument('--effort'); init.add_argument('--pressure-regex'); init.add_argument('--pressure-kind',choices=['used','remaining'],default='used'); init.add_argument('--threshold',type=float,default=60); init.add_argument('--seed',type=Path); init.add_argument('--notify',action='store_true'); init.add_argument('--auto-exit',action='store_true'); init.add_argument('--request-timeout',type=int,default=1800)
    for name in ['tick','request','enroll','checkpoint','status','doctor']: sub.add_parser(name)
    ack=sub.add_parser('ack'); ack.add_argument('--session-id'); ack.add_argument('--profile')
    watch=sub.add_parser('watch'); watch.add_argument('--interval',type=float,default=30); watch.add_argument('--plain',action='store_true')
    sub.add_parser('pause'); sub.add_parser('continue')
    st=sub.add_parser('stop'); st.add_argument('--status',choices=sorted(STOP),required=True)
    a=p.parse_args()
    if a.cmd=='path': print(run_path(a.root)); return
    require(a.run is not None,'--run is required')
    d=a.run.expanduser().absolute()
    require(not any(x.is_symlink() for x in (d,*d.parents)),'Symlink in state path')
    d=d.resolve()
    if a.cmd=='init':
        root=a.root.resolve(); repo(root); outside(d,root); require(d==run_path(root).resolve(),'Use the exact path from path --root (one mission per worktree)'); require(not d.exists(),'Run directory already exists; inspect or archive a stopped run'); require(0<a.threshold<100 and a.request_timeout>0,'Invalid limits'); require(not a.effort or a.model,'Effort requires model')
        require(not a.auto_exit or (a.profile and a.session_id and a.pressure_regex),'Automatic exit requires verified profile, session ID and context regex')
        if a.pressure_regex: require('percent' in re.compile(a.pressure_regex).groupindex,'Regex needs named percent group')
        c={'root':str(root),'host':a.host,'orca':a.orca,'threshold':a.threshold,'pressure_regex':a.pressure_regex,'pressure_kind':a.pressure_kind,'auto_exit':a.auto_exit,'notify':a.notify,'request_timeout':a.request_timeout,'model':a.model,'effort':a.effort,'script':str(Path(__file__).resolve()),'python':sys.executable,'protocol':str(Path(__file__).resolve().parents[1]/'references'/'agent-protocol.md'),'profile':a.profile}
        if a.seed:
            seed=a.seed.resolve(); c.update(seed=str(seed),seed_sha256=digest(seed))
        if a.adapter:
            adapter=a.adapter.expanduser().absolute()
            require(adapter.is_file() and not any(x.is_symlink() for x in (adapter,*adapter.parents)),'Unsafe adapter')
            outside(adapter.resolve(),root)
            require(adapter.stat().st_uid==os.getuid() and adapter.stat().st_mode & 0o022==0,'Adapter ownership/mode unsafe')
            c.update(adapter=str(adapter),adapter_sha256=hashlib.sha256(adapter.read_bytes()).hexdigest())
        o=transport(c); h=a.handle or o.caller()
        require(h and o.caller()==h,'Target must be the current agent pane')
        t=o.show(h); require(Path(t['worktreePath']).resolve()==root and t.get('executionHostId') and t.get('incarnationId') and t.get('connected') and t.get('writable'),'Cannot bind target'); require(t.get('handle')==h and t.get('worktreeId') and t.get('agentIdentity')==a.host and t.get('verdict')=='live','Unverified target')
        c.update(worktree_id=t['worktreeId'],execution_host=t['executionHostId'])
        d.parent.mkdir(mode=0o700,parents=True,exist_ok=True); safe_dir(d.parent)
        d.mkdir(mode=0o700); save(d/'config.json',c); save(d/'state.json',{'phase':'enrolling','generation':0,'handle':h,'incarnation':t['incarnationId'],'provider_session_id':a.session_id,'created':time.time(),'events':[]}); print(f'Bind complete. Read {c["protocol"]} and prepare strategy in {d}.'); return
    if a.cmd=='watch':
        require(1<=a.interval<=3600,'Invalid watch interval')
        from mission_tui import watch as run_watch
        with lock(d,'watch.lock'):
            run_watch(d,a.interval,a.plain,Run,lock,stop_run)
        return
    with lock(d):
        r=Run(d)
        if a.cmd=='tick': print(r.tick())
        elif a.cmd=='enroll': r.enroll(); print('enrolled')
        elif a.cmd=='request': r.request('manual'); print('requested')
        elif a.cmd=='checkpoint': r.checkpoint(); print('sealed; stop working')
        elif a.cmd=='ack': r.ack(a.session_id,a.profile); print('acknowledged')
        elif a.cmd=='status': print(json.dumps(r.s,indent=2))
        elif a.cmd=='doctor':
            t=r.identity(); r.live(t)
            keys=('handle','incarnationId','worktreeId','worktreePath','executionHostId','agentIdentity','verdict')
            print(json.dumps({'terminal':{k:t.get(k) for k in keys},'pressure_used':r.pressure(),'repository':repo(r.root)},indent=2))
        elif a.cmd in ('pause','continue'):
            require(r.s['phase']=='active' and not (d/'stop.json').exists(),'Only an active run can pause or continue')
            r.persist(paused=a.cmd=='pause'); print(a.cmd)
        elif a.cmd=='stop': stop_run(r,a.status); print('stop recorded')

if __name__=='__main__':
    try: main()
    except (Halt, OSError, ValueError, KeyError, subprocess.SubprocessError) as e:
        print(f'rollover stopped: {e}',file=sys.stderr); sys.exit(2)
