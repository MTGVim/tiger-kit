#!/usr/bin/env python3
"""Sample a clean rendered video for empty narration, edge ink and content bounds."""
from __future__ import annotations
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import tempfile


def cues(path):
    text = Path(path).read_text(encoding='utf-8-sig')
    ts = r'(\d+):(\d{2}):(\d{2})[,.](\d{3})'
    rows = []
    for m in re.finditer(ts + r'\s*-->\s*' + ts, text):
        g = list(map(int, m.groups()))
        a, b = (g[0]*3600+g[1]*60+g[2]+g[3]/1000, g[4]*3600+g[5]*60+g[6]+g[7]/1000)
        if not 0 <= a < b or (rows and a < rows[-1][1]):
            raise ValueError('SRT must contain ordered nonoverlapping cues')
        rows.append((a,b))
    if not rows:
        raise ValueError('no valid SRT cues')
    return rows


def runs(flags, fps):
    result, start = [], None
    for index, value in enumerate([*flags, False]):
        if value and start is None:
            start = index / fps
        elif not value and start is not None:
            result.append((start, index/fps)); start = None
    return result


def scan(video, captions, fps=2., top=0., bottom=.80, threshold=.004, min_seconds=1., edge_px=12, ffmpeg='ffmpeg', ffprobe='ffprobe'):
    if not all(math.isfinite(x) for x in (fps,top,bottom,threshold,min_seconds)) or not (0 < fps <= 10 and 0 <= top < bottom <= 1 and 0 <= threshold < 1 and min_seconds > 0):
        raise ValueError('invalid scan sampling or body-band parameters')
    spoken = cues(captions)
    probe = subprocess.run([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,check=True,timeout=30)
    data = json.loads(probe.stdout)
    stream = next(s for s in data['streams'] if s['codec_type']=='video')
    width,height = int(stream['width']),int(stream['height'])
    duration = float(data['format']['duration'])
    if not 0 < duration <= 7200 or width*height > 40_000_000 or not 0 < edge_px <= width/4:
        raise ValueError('scan budget or edge width exceeded')
    y = int(height*top)//2*2
    h = int(height*(bottom-top))//2*2
    if h < 2 or y+h > height:
        raise ValueError('body band must contain at least two rows')
    # Explicit even crop height and output geometry avoid raw-frame stride drift.
    scaled_w = min(width,640)//2*2
    scaled_h = max(2,round(h*scaled_w/width/2)*2)
    size = scaled_w*scaled_h
    edge = max(1,math.ceil(edge_px*scaled_w/width))
    ink, edge_flags, bounds = [], [], []
    with tempfile.TemporaryFile() as errors:
        proc = subprocess.Popen([ffmpeg,'-v','error','-nostdin','-i',str(video),'-an','-vf',
            f'fps={fps},crop={width}:{h}:0:{y},scale={scaled_w}:{scaled_h},format=gray',
            '-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=errors)
        try:
            while True:
                raw = bytearray()
                while len(raw) < size:
                    chunk = proc.stdout.read(size-len(raw))
                    if not chunk: break
                    raw.extend(chunk)
                if not raw: break
                if len(raw) != size:
                    raise ValueError('raw frame byte count is not a frame-size multiple')
                if len(ink) > math.ceil(7200*fps):
                    raise ValueError('decoded sample budget exceeded')
                bg = Counter(raw[::97]).most_common(1)[0][0]
                pixels = [i for i,v in enumerate(raw) if abs(v-bg)>24]
                ink.append(len(pixels)/size)
                edge_flags.append(any(i%scaled_w < edge or i%scaled_w >= scaled_w-edge for i in pixels))
                if pixels:
                    xs,ys = [i%scaled_w for i in pixels],[i//scaled_w for i in pixels]
                    bounds.append({'time_s':(len(ink)-1)/fps,'top_px':y+min(ys)*h/scaled_h,
                                   'bottom_px':y+(max(ys)+1)*h/scaled_h,
                                   'center_px':y+(min(ys)+max(ys)+1)/2*h/scaled_h})
            if proc.wait(timeout=30):
                raise ValueError('FFmpeg sampling failed')
        finally:
            if proc.poll() is None:
                proc.kill();proc.wait()
            proc.stdout.close()
    blanks = []
    for a,b in runs([v<threshold for v in ink],fps):
        overlap=sum(max(0,min(b,e)-max(a,s)) for s,e in spoken)
        if overlap >= min_seconds:
            blanks.append({'start_s':a,'end_s':min(b,duration),'narrated_s':overlap})
    if not ink:
        raise ValueError('video yielded no sampled frames')
    return {'frames':len(ink),'fps':fps,'body_band_px':[y,y+h],
            'blank_narrated_runs':blanks,'edge_ink_runs':[{'start_s':a,'end_s':min(b,duration)} for a,b in runs(edge_flags,fps)],
            'content_bounds':bounds,'median_center_px':statistics.median(r['center_px'] for r in bounds) if bounds else None,
            'limitation':'Background/ink heuristic; inspect candidates and use beat-end samples for layout approval.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video',type=Path,required=True);p.add_argument('--captions',type=Path,required=True)
    for name,default in [('fps',2.),('top',0.),('bottom',.80),('threshold',.004),('min-seconds',1.)]:
        p.add_argument('--'+name,type=float,default=default)
    p.add_argument('--edge-px',type=int,default=12);p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe')
    a=p.parse_args()
    try:
        result=scan(a.video,a.captions,a.fps,a.top,a.bottom,a.threshold,a.min_seconds,a.edge_px,a.ffmpeg,a.ffprobe)
        print(json.dumps(result,allow_nan=False))
        return 1 if result['blank_narrated_runs'] or result['edge_ink_runs'] else 0
    except (ValueError,KeyError,TypeError,StopIteration,OSError,subprocess.SubprocessError) as exc:
        print(json.dumps({'status':'failed','detail':str(exc) if isinstance(exc,ValueError) else 'visual scan failed'}));return 2


if __name__=='__main__':raise SystemExit(main())
