#!/usr/bin/env python3
"""List supported local TTS routes without importing engines, installing or downloading."""
import argparse,importlib.util,json,platform
from pathlib import Path
R=Path(__file__).resolve().parent

ROUTES = [
        ('qwen3-mlx-5bit','mlx-files.json','Apple Silicon / Metal',['mlx','mlx_audio','soundfile'],['sohee','serena']),
        ('ppaso-onnx','ppaso-files.json','CPU',['onnxruntime','mecab','soundfile'],['model voice']),
        ('supertonic3-onnx','supertonic3-files.json','CPU',['onnxruntime','numpy','soundfile','cffi'],['F1']),
        ('qwen3-mlx-8bit','mlx-8bit-files.json','Apple Silicon / Metal',['mlx','mlx_audio','soundfile'],['sohee','serena']),
        ('qwen3-pytorch','qwen3-files.json','CUDA / MPS / CPU',['torch','qwen_tts','soundfile'],['sohee','serena'])]

def options(preferred=None):
    if preferred is not None and preferred not in {row[0] for row in ROUTES}:
        raise ValueError('unsupported preferred TTS engine')
    apple=platform.system()=='Darwin' and platform.machine()=='arm64';rows=[]
    for id,file,device,modules,speakers in ROUTES:
        d=json.loads((R/file).read_text());missing=[]
        for name in modules:
            try:found=importlib.util.find_spec(name) is not None
            except (ModuleNotFoundError,ValueError):found=False
            if not found:missing.append(name)
        rows.append({'id':id,'model':d['repository'],'revision':d['revision'],'device':device,'platform_supported':apple if 'mlx' in id else True,'missing_modules':missing,'dependency_status':'missing' if missing else 'modules-present-unverified','model_cache_status':'not-inspected','runtime_verified':False,'speakers':speakers,'recommended':id=='supertonic3-onnx','preferred':id==preferred,'network_for_synthesis':False,'installation_or_model_download':'requires prior approval; inspect selected manifest and cache'})
        if id=='supertonic3-onnx':
            rows[-1].update({'disclosure_required':True,'disclosure_notice':d['disclosure_notice'],'upstream_status':'archived','maintenance_notice':'Upstream is archived; maintenance and security fixes are unavailable.','selection_notice':'이 경로를 고르면 영상 전체에 작은 AI 합성 고지가 들어갑니다.'})
    return rows
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preferred',choices=[row[0] for row in ROUTES],help='Caller-resolved engine preference; does not select, install or download an engine')
    args=parser.parse_args()
    print(json.dumps({'options':options(args.preferred),'note':'Module discovery is not runtime, model, pronunciation or license verification. Browser speech is a playback fallback, not an exported-audio engine.'},ensure_ascii=False,indent=2))
