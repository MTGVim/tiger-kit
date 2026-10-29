#!/usr/bin/env python3
"""Pinned Supertonic 3 Korean narration, CPU/F1 only. Setup requires prior approval."""
from __future__ import annotations

import argparse
import contextlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

import qwen3 as common


def manifest():
    data = json.loads(Path(__file__).with_name('supertonic3-files.json').read_text(encoding='utf-8'))
    if (data['repository'] != 'supertone-oss-archive/supertonic-3'
            or data['revision'] != 'aafc6e32416a594460b32413efc49d7fe4ce6d46'
            or data['code_revision'] != '1e9799e964ea4c0dad7cde993b65c3c813a7b373'):
        raise ValueError('unreviewed Supertonic 3 source')
    for name, digest in data['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('invalid pinned Supertonic 3 file manifest')
    base = f"https://raw.githubusercontent.com/supertone-oss-archive/supertonic/{data['code_revision']}"
    if data['file_urls'] != {'runtime/helper.py': base + '/py/helper.py', 'runtime/LICENSE': base + '/LICENSE'}:
        raise ValueError('unreviewed Supertonic 3 runtime URLs')
    return data


def verify_runtime(data):
    for name in ['numpy', 'soundfile', 'cffi', 'onnxruntime']:
        if importlib.util.find_spec(name) is None:
            raise ModuleNotFoundError(name=name)
    for name, expected in data['dependencies'].items():
        actual = importlib.metadata.version(name)
        if actual != expected:
            raise ValueError(f'use pinned {name}: actual={actual}, expected={expected}; restore with this venv Python -m pip install {name}=={expected} after installation approval')


def load_runtime(root):
    # Only the already hash-verified snapshot helper may execute, never a parent runtime.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('_tigerkit_supertonic3_runtime', root / 'runtime/helper.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthesize(root, text_file, output):
    data = common.verify(root, manifest())
    verify_runtime(data)
    rows, output = common.script_inputs(text_file, output)
    before, limits = common.cache_inventory()
    cache = common.configure_runtime(root)
    import numpy as np
    import soundfile  # Check native audio dependencies before loading model weights.

    helper = load_runtime(root)
    model = helper.load_text_to_speech(str(root / 'onnx'), use_gpu=False)
    if any(session.get_providers() != ['CPUExecutionProvider'] for session in
           [model.dp_ort, model.text_enc_ort, model.vector_est_ort, model.vocoder_ort]):
        raise ValueError('Supertonic 3 requires CPUExecutionProvider only')
    rate = model.sample_rate
    if rate != 44100:
        raise ValueError('invalid Supertonic 3 sample rate')
    style = helper.load_voice_style([str(root / 'voice_styles/F1.json')])
    parts, trimmed, chunk_count = [], 0.0, 0
    for row in rows:
        chunks = []
        for chunk in helper.chunk_text(row, max_len=120):
            audio, duration = model.batch([chunk], ['ko'], style, total_step=8, speed=1.05)
            samples = np.asarray(audio, dtype=np.float32)
            duration = np.asarray(duration).reshape(-1)
            if (samples.ndim != 2 or samples.shape[0] != 1 or not np.isfinite(samples).all()
                    or duration.size != 1 or not np.isfinite(duration[0]) or duration[0] <= 0):
                raise ValueError('invalid Supertonic 3 audio or duration')
            frames = int(float(duration[0]) * rate)
            if not 0 < frames <= samples.shape[1]:
                raise ValueError('Supertonic 3 duration exceeds decoded audio or is empty')
            if chunks:
                chunks.append(np.zeros(round(.3 * rate), dtype=np.float32))
            # Crop each native chunk before joining, so decoder padding cannot truncate later speech.
            chunks.append(samples[0, :frames])
            chunk_count += 1
        if not chunks:
            raise ValueError('Supertonic 3 produced no text chunks')
        samples, removed = common.trim_leading_silence(np.concatenate(chunks), rate)
        parts.append(samples)
        trimmed += removed
    samples = np.concatenate(parts)
    common.write_audio(samples, rate, output)
    return {'path': str(output), 'duration_seconds': len(samples) / rate,
            'trimmed_leading_seconds': trimmed, 'engine': 'supertonic3-onnx', 'device': 'cpu',
            'speaker': 'F1', 'sentence_count': len(rows), 'native_chunk_count': chunk_count,
            'total_step': 8, 'speed': 1.05, 'revision': data['revision'],
            'code_revision': data['code_revision'], 'human_action': 'listen',
            'disclosure_required': True, 'disclosure_notice': data['disclosure_notice'],
            **common.memory_metrics(), **common.cache_report(before, limits, cache)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-dir', type=Path)
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--text-file', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    before, limits = common.cache_inventory()
    owned = None
    try:
        data = manifest()
        cache = Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))) / 'tigerkit/tts/supertonic3'
        root = args.model_dir or cache / 'snapshots' / data['revision']
        owned = common.runtime_cache(root)
        if args.verify or args.text_file or args.output:
            verify_runtime(data)
        if args.download:
            common.download(root, data)
        if args.verify:
            common.verify(root, data)
            print(json.dumps({'verified_files': len(data['files']), 'revision': data['revision']}))
        if args.text_file or args.output:
            if not args.text_file or not args.output:
                raise ValueError('text-file and output are required together')
            with contextlib.redirect_stdout(sys.stderr):
                result = synthesize(root, args.text_file, args.output)
            print(json.dumps(result, ensure_ascii=False))
        elif not args.verify and not args.download:
            raise ValueError('select verify, download or synthesis')
        return 0
    except Exception as exc:
        detail = str(exc) if isinstance(exc, ValueError) else 'Supertonic 3 unavailable; no audio accepted'
        if isinstance(exc, ModuleNotFoundError) and isinstance(exc.name, str) and re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*', exc.name, flags=re.ASCII):
            detail = 'missing runtime module: ' + exc.name
        print(json.dumps({'narration_status': 'unavailable', 'error': type(exc).__name__,
                          'detail': detail, **common.cache_report(before, limits, owned)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
