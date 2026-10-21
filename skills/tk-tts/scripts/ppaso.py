#!/usr/bin/env python3
"""Pinned ppaso ONNX CPU narration. Installation and download require prior approval."""
from __future__ import annotations
import argparse,contextlib,importlib,importlib.util,json,os,re,sys,types
from pathlib import Path
import qwen3 as common

def manifest():
    d=json.loads(Path(__file__).with_name('ppaso-files.json').read_text())
    if d['repository']!='akamotaco/ppaso-tts-v1' or d['revision']!='53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9':raise ValueError('unreviewed ppaso source')
    for name,digest in d['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts or not re.fullmatch('[0-9a-f]{64}',digest):raise ValueError('invalid pinned ppaso file manifest')
    return d

def verify_runtime(d):
    for name in ['numpy','soundfile','cffi','mecab','onnxruntime']:
        if importlib.util.find_spec(name) is None:raise ModuleNotFoundError(name=name)
    for name,expected in d['dependencies'].items():
        actual=importlib.metadata.version(name)
        if actual!=expected:raise ValueError(f'use pinned {name}: actual={actual}, expected={expected}; restore with this venv Python -m pip install {name}=={expected} after installation approval')

def load_runtime(root):
    # Import only hash-verified code under a unique package name; never search parent runtimes.
    sys.dont_write_bytecode=True
    alias='_tigerkit_ppaso_runtime'
    if any(k==alias or k.startswith(alias+'.') for k in sys.modules):raise ValueError('use a fresh owned process for ppaso synthesis')
    package=types.ModuleType(alias);package.__path__=[str(root/'runtime')];sys.modules[alias]=package
    os.environ['PPASO_LEXICON']=str(root/'runtime/dict/korean_mfa.dict')
    g2p=importlib.import_module(alias+'.data.g2p_mfa');phones=importlib.import_module(alias+'.data.phoneme_mfa')
    spec=importlib.util.spec_from_file_location('_tigerkit_ppaso_model',root/'example/ppaso_tts.py')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    module._import_runtime_g2p=lambda _: (g2p.text_to_phones_with_special,phones.PHONEME_TO_ID_MFA)
    return module.PpasoTTS

def synthesize(root,text_file,output):
    d=common.verify(root,manifest());verify_runtime(d);rows,output=common.script_inputs(text_file,output)
    before,limits=common.cache_inventory();cache=common.configure_runtime(root)
    import numpy as np
    import soundfile
    factory=load_runtime(root);model=factory(root,backend='onnx',device='cpu')
    rate=22050;parts=[];trimmed=0
    for row in rows:
        samples,removed=common.trim_leading_silence(model.synthesize(row,chunked=True),rate)
        parts.append(samples);trimmed+=removed
    samples=np.concatenate(parts);common.write_audio(samples,rate,output)
    return {'path':str(output),'duration_seconds':len(samples)/rate,'trimmed_leading_seconds':trimmed,'engine':'ppaso-onnx','device':'cpu','sentence_count':len(rows),'revision':d['revision'],'human_action':'listen',**common.memory_metrics(),**common.cache_report(before,limits,cache)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model-dir',type=Path);p.add_argument('--download',action='store_true');p.add_argument('--verify',action='store_true');p.add_argument('--text-file',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    before,limits=common.cache_inventory();owned=None
    try:
        d=manifest();cache=Path(os.environ.get('XDG_CACHE_HOME',str(Path.home()/'.cache')))/'tigerkit/tts/ppaso'
        root=a.model_dir or cache/'snapshots'/d['revision'];owned=common.runtime_cache(root)
        if a.verify or a.text_file or a.output:verify_runtime(d)
        if a.download:common.download(root,d)
        if a.verify:common.verify(root,d);print(json.dumps({'verified_files':len(d['files']),'revision':d['revision']}))
        if a.text_file or a.output:
            if not a.text_file or not a.output:raise ValueError('text-file and output are required together')
            with contextlib.redirect_stdout(sys.stderr):result=synthesize(root,a.text_file,a.output)
            print(json.dumps(result))
        elif not a.verify and not a.download:raise ValueError('select verify, download or synthesis')
        return 0
    except Exception as exc:
        detail=str(exc) if isinstance(exc,ValueError) else 'ppaso unavailable; no audio accepted'
        if isinstance(exc,ModuleNotFoundError) and isinstance(exc.name,str) and re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',exc.name,flags=re.ASCII):detail='missing runtime module: '+exc.name
        print(json.dumps({'narration_status':'unavailable','error':type(exc).__name__,'detail':detail,**common.cache_report(before,limits,owned)}));return 1
if __name__=='__main__':raise SystemExit(main())
