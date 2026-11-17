#!/usr/bin/env python3
"""Foreground Mission Control; no extra model, daemon or UI dependency."""
import datetime
import re
import sys
import time
import unicodedata

TERMINAL = {'stopped', 'blocked', 'launching'}
TRANSITION = {'publishing','ready','exit_sent','exited','await_ack','finalizing'}

def visible(text, width):
    result=[]; used=0
    for ch in str(text):
        if unicodedata.category(ch).startswith('C'):
            ch=' '
        n=0 if unicodedata.combining(ch) else 2 if unicodedata.east_asian_width(ch) in ('W','F') else 1
        if used+n>width:
            break
        result.append(ch); used+=n
    return ''.join(result)

def strategy_view(body):
    sections={}; current=None
    for line in body.splitlines():
        if line.startswith('## '):
            current=line[3:].strip(); sections[current]=[]
        elif current:
            sections[current].append(line)
    mission=' '.join(x.strip() for x in sections.get('Mission',[]) if x.strip())
    rows=[]
    for line in sections.get('Milestones',[]):
        m=re.match(r'^\s*[-*]\s+\[([ xX])\]\s+(.+)$',line)
        if m:
            rows.append((m[1].lower()=='x',m[2]))
    return mission,rows,sections

def snapshot(r):
    from pathlib import Path
    p=r.d/'strategy.md'
    body=p.read_text(encoding='utf-8') if p.is_file() and not p.is_symlink() and p.stat().st_size<=256000 else ''
    goal,items,sections=strategy_view(body)
    s=dict(r.s); c=r.c
    return {'state':s,'goal':goal,'items':items,'sections':sections,'root':str(r.root),
            'host':c['host'],'profile':c.get('profile'),'threshold':c['threshold'],
            'run':str(r.d),'handoff':str(r.paths()[0]) if s.get('request') else None}

def watch(d, interval, plain, Run, lock, stop_run, Busy):
    def poll():
        with lock(d):
            r=Run(d)
            if r.s['phase']=='enrolling':
                raise RuntimeError('Enroll the current agent before starting the controller')
            message=r.tick()
            return snapshot(r),message
    def action(key):
        with lock(d):
            r=Run(d)
            if key=='q':
                stop_run(r,'aborted')
                return 'Stopped; current agent is not terminated'
            if r.s['phase']!='active' or (d/'stop.json').exists():
                return 'Action is available only in an active mission'
            if key=='p':
                r.persist(paused=not r.s.get('paused'))
                return 'Paused' if r.s['paused'] else 'Monitoring resumed'
            if key=='r':
                if r.s.get('paused'):
                    return 'Continue monitoring before requesting a rollover'
                r.request('manual from controller')
                return 'Rollover requested'
        return ''
    def next_delay(v):
        return min(interval,2) if v['state']['phase'] in TRANSITION else interval
    if plain or not (sys.stdin.isatty() and sys.stdout.isatty()):
        while True:
            try: v,msg=poll()
            except Busy:
                time.sleep(1); continue
            s=v['state']
            print(f'{datetime.datetime.now().isoformat(timespec="seconds")} {s["phase"]} generation={s["generation"]} context={s.get("last_pressure")} {msg}',flush=True)
            if s['phase'] in TERMINAL: return
            time.sleep(next_delay(v))
    else:
        import curses
        def ui(stdscr):
            try: curses.curs_set(0)
            except curses.error: pass
            stdscr.keypad(True); stdscr.timeout(200)
            palette={}
            if curses.has_colors():
                curses.start_color()
                try: curses.use_default_colors(); bg=-1
                except curses.error: bg=curses.COLOR_BLACK
                for i,(name,color) in enumerate([('cyan',curses.COLOR_CYAN),('green',curses.COLOR_GREEN),('yellow',curses.COLOR_YELLOW),('red',curses.COLOR_RED)],1):
                    curses.init_pair(i,color,bg); palette[name]=curses.color_pair(i)
            v=None; msg='Starting'; deadline=0; details=False; scroll=0
            def draw():
                stdscr.erase(); height,width=stdscr.getmaxyx()
                def line(y,text,style=0):
                    if 0<=y<height and width>2:
                        try: stdscr.addstr(y,0,visible(text,width-1),style)
                        except curses.error: pass
                if not v:
                    line(0,msg); stdscr.refresh(); return
                s=v['state']; phase=s['phase']; p=s.get('last_pressure')
                elapsed=int(max(0,time.time()-s.get('created',time.time())))
                hh,rem=divmod(elapsed,3600); mm,ss=divmod(rem,60)
                color=palette.get('red' if phase in TERMINAL else 'yellow' if s.get('paused') or phase!='active' else 'green',0)
                line(0,' TIGERKIT / MISSION CONTROL',curses.A_BOLD|palette.get('cyan',0))
                line(1,f' {phase.upper()}{" / PAUSED" if s.get("paused") else ""}   G{s["generation"]+1:02d}   {hh:02d}:{mm:02d}:{ss:02d}',curses.A_BOLD|color)
                line(2,f' {v["host"]} | {v["root"]}')
                line(3,f' Target: {s["handle"]} | Rollovers: {s["generation"]}')
                line(4,f' Profile: {v["profile"] or "unverified"}')
                bar=max(8,min(32,width-32))
                filled=int(bar*float(p)/100) if isinstance(p,(int,float)) and 0<=p<=100 else 0
                label=f'{p:.1f}%' if isinstance(p,(int,float)) else 'unverified'
                line(5,f' Context (last) [{"#"*filled+"."*(bar-filled)}] {label} / {v["threshold"]:g}%',palette.get('yellow' if isinstance(p,(int,float)) and p>=v['threshold'] else 'cyan',0))
                line(6,' '+('-'*max(0,width-2)),curses.A_DIM)
                line(7,' MISSION',curses.A_BOLD)
                line(8,' '+(v['goal'] or 'Strategy not available'))
                body=[]
                if details:
                    body.append((' HANDOFF / STRATEGY',curses.A_BOLD))
                    body.append((' '+(v['handoff'] or 'No pending handoff'),0))
                    body.append((' Run: '+v['run'],0))
                    for name,lines in v['sections'].items():
                        if name!='Mission':
                            body.append((' '+name,curses.A_BOLD))
                            body.extend((' '+x,0) for x in lines if x.strip())
                else:
                    items=v['items']; done=sum(x[0] for x in items)
                    body.append((f' STRATEGY  {done}/{len(items)} milestones' if items else ' STRATEGY  no structured milestones',curses.A_BOLD))
                    for completed,name in items:
                        body.append((' '+('[x] ' if completed else '[ ] ')+name,palette.get('green',0) if completed else 0))
                    body.append((' EVENT LOG',curses.A_BOLD))
                    for e in reversed(s.get('events',[])):
                        stamp=datetime.datetime.fromtimestamp(e['time']).strftime('%H:%M:%S')
                        body.append((f' {stamp} G{e["generation"]+1:02d} {e["phase"]}',0))
                rows=max(0,height-13); offset=max(0,min(scroll,max(0,len(body)-rows)))
                for y,(txt,sty) in enumerate(body[offset:offset+rows],10): line(y,txt,sty)
                line(height-3,' '+msg,palette.get('yellow',0))
                line(height-2,' [H] Details  [R] Rollover  [P] Pause/continue  [Q] Stop  [↑↓] Scroll',curses.A_DIM)
                line(height-1,' Ctrl+C or close: stop controller, never force-kill the agent',curses.A_DIM)
                stdscr.refresh()
            while True:
                if time.monotonic()>=deadline:
                    try:
                        v,msg=poll(); deadline=time.monotonic()+next_delay(v)
                    except Busy:
                        msg='Another mission operation is running'; deadline=time.monotonic()+1
                draw()
                if v and v['state']['phase'] in TERMINAL:
                    return msg
                k=stdscr.getch()
                if k in (ord('h'),ord('H')):
                    details=not details; scroll=0
                elif k in (ord('r'),ord('R'),ord('p'),ord('P'),ord('q'),ord('Q')):
                    try: msg=action(chr(k).lower())
                    except Busy:
                        msg='Another mission operation is running; retry the key'; continue
                    if chr(k).lower()=='q': return msg
                    deadline=0
                elif k==curses.KEY_DOWN: scroll+=1
                elif k==curses.KEY_UP: scroll=max(0,scroll-1)
        result=curses.wrapper(ui)
        print(result,flush=True)
