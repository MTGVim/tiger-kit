#!/usr/bin/env python3
"""Normalize a narration batch into a new directory without modifying source WAVs."""
from __future__ import annotations
import argparse,json,math,re,shutil,subprocess,tempfile,wave
from array import array
from pathlib import Path

TARGET_I=-18
TARGET_TP=-1.5
TARGET_LRA=7

def inspect(path):
    if path.resolve()!=path.absolute() or not path.is_file():raise ValueError('use regular nonsymlink WAV inputs')
    if path.stat().st_size>500_000_000:raise ValueError('narration exceeds the per-file budget')
    with wave.open(str(path),'rb') as wav:
        if wav.getnchannels()!=1 or wav.getsampwidth()!=2 or wav.getcomptype()!='NONE':raise ValueError('expected mono PCM16 WAV')
        rate=wav.getframerate();frames=wav.getnframes();raw=wav.readframes(frames)
    if not frames or len(raw)!=frames*2:raise ValueError('empty or truncated narration')
    samples=array('h',raw);peak=max(abs(x) for x in samples)/32768
    if peak==0:raise ValueError('silent narration')
    rms=math.sqrt(sum(x*x for x in samples)/len(samples))/32768
    return {'rate':rate,'seconds':frames/rate,'peak_db':20*math.log10(peak),'rms_db':20*math.log10(rms)}

def measured(stderr):
    blocks=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',stderr)
    if not blocks:raise ValueError('FFmpeg returned no loudness measurements')
    return json.loads(blocks[-1])

def normalize(inputs,output):
    paths=[Path(p).absolute() for p in inputs];output=Path(output).absolute()
    if not paths or len(set(paths))!=len(paths):raise ValueError('supply unique WAV inputs')
    if output.exists() or output.resolve()!=output or not output.parent.is_dir():raise ValueError('use a new safe output directory')
    info=[inspect(p) for p in paths]
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg:raise ValueError('FFmpeg is required for loudness normalization; do not install implicitly')
    base=f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}'
    rows=[]
    with tempfile.TemporaryDirectory(prefix='.normalize-',dir=output.parent) as folder:
        stage=Path(folder)/'normalized';stage.mkdir()
        for n,(source,before) in enumerate(zip(paths,info),1):
            common=[ffmpeg,'-hide_banner','-nostdin','-i',str(source),'-map','0:a:0']
            first=subprocess.run([*common,'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True,timeout=300)
            stats=measured(first.stderr)
            finite=all(math.isfinite(float(stats[key])) for key in ('input_i','input_tp','input_lra','input_thresh','target_offset'))
            if finite:
                filter=base+':linear=true:print_format=json'+''.join(':'+key+'='+stats[value] for key,value in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
                mode='ebu-r128-two-pass';limitation=None
            else:
                gain=min(-20-before['rms_db'],TARGET_TP-before['peak_db'],20)
                filter=f'volume={gain:.6f}dB';mode='rms-fallback';limitation='Clip has no finite gated loudness; bounded RMS/peak matching is not a LUFS measurement.'
            name=f'{n:03d}-{source.name}';target=stage/name
            second=subprocess.run([*common,'-af',filter,'-ac','1','-ar',str(before['rate']),'-c:a','pcm_s16le',str(target)],capture_output=True,text=True,check=True,timeout=300)
            after=inspect(target)
            if abs(before['seconds']-after['seconds'])>.1:raise ValueError('normalized audio duration drift exceeds 0.1 seconds')
            row={'source':str(source),'path':str(output/name),'mode':mode,'before':before,'after':after,'limitation':limitation}
            if finite:row['loudness']=measured(second.stderr)
            rows.append(row)
        if output.exists() or output.resolve()!=output:raise ValueError('output was replaced during normalization')
        stage.rename(output)
    return {'target_lufs':TARGET_I,'true_peak_db':TARGET_TP,'lra':TARGET_LRA,'files':rows,'human_action':'listen'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--inputs',nargs='+',type=Path,required=True);parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args()
    try:print(json.dumps(normalize(args.inputs,args.output_dir),ensure_ascii=False,allow_nan=False));return 0
    except (ValueError,OSError,wave.Error,subprocess.SubprocessError) as exc:print(json.dumps({'status':'failed','detail':str(exc)}));return 1
if __name__=='__main__':raise SystemExit(main())
