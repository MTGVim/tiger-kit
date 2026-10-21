#!/usr/bin/env python3
"""List supported local TTS routes without importing engines, installing or downloading."""
import importlib.util,json,platform
from pathlib import Path
R=Path(__file__).resolve().parent

def options():
    apple=platform.system()=='Darwin' and platform.machine()=='arm64';rows=[]
    for id,file,device,modules,speakers in [
        ('qwen3-mlx-5bit','mlx-files.json','Apple Silicon / Metal',['mlx','mlx_audio','soundfile'],['sohee','serena']),
        ('ppaso-onnx','ppaso-files.json','CPU',['onnxruntime','mecab','soundfile'],['model voice']),
        ('qwen3-mlx-8bit','mlx-8bit-files.json','Apple Silicon / Metal',['mlx','mlx_audio','soundfile'],['sohee','serena']),
        ('qwen3-pytorch','qwen3-files.json','CUDA / MPS / CPU',['torch','qwen_tts','soundfile'],['sohee','serena'])]:
        d=json.loads((R/file).read_text());missing=[]
        for name in modules:
            try:found=importlib.util.find_spec(name) is not None
            except (ModuleNotFoundError,ValueError):found=False
            if not found:missing.append(name)
        rows.append({'id':id,'model':d['repository'],'revision':d['revision'],'device':device,'platform_supported':apple if 'mlx' in id else True,'missing_modules':missing,'runtime_verified':False,'speakers':speakers,'recommended':id==('qwen3-mlx-5bit' if apple else 'qwen3-pytorch'),'network_for_synthesis':False,'installation_or_model_download':'requires prior approval; inspect selected manifest and cache'})
    return rows
if __name__=='__main__':print(json.dumps({'options':options(),'note':'Module discovery is not runtime, model, pronunciation or license verification. Browser speech is a playback fallback, not an exported-audio engine.'},ensure_ascii=False,indent=2))
