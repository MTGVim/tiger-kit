#!/usr/bin/env python3
"""Measure Korean sentence speech rate and optionally write bounded atempo copies."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import wave


def duration(path):
    path = Path(path).absolute()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 500_000_000:
        raise ValueError('use regular nonsymlink WAV inputs; copy reused clips')
    with wave.open(str(path)) as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getcomptype() != 'NONE':
            raise ValueError('expected mono PCM16 WAV')
        frames, rate = wav.getnframes(), wav.getframerate()
        if not frames or not rate or len(wav.readframes(frames)) != frames * 2:
            raise ValueError('empty or truncated WAV')
    return frames / rate


def plan(sentences):
    if not isinstance(sentences, list) or not 1 <= len(sentences) <= 10000:
        raise ValueError('input must contain 1-10000 sentences')
    rows, ids = [], set()
    for s in sentences:
        if not isinstance(s, dict) or not isinstance(s.get('id'), str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', s['id']) or s['id'] in ids:
            raise ValueError('sentence ids must be unique safe ASCII names')
        ids.add(s['id'])
        text = s.get('spoken_text', s.get('text'))
        if not isinstance(text, str) or len(text) > 20000 or re.search(r'[0-9A-Za-z]', text):
            raise ValueError('supply spoken_text with numbers, units and Latin tokens written as actually spoken Hangul')
        count = len(re.findall('[가-힣]', text))
        if not count:
            raise ValueError('sentence has no countable Hangul syllables')
        seconds = duration(s['wav'])
        rows.append({'id': s['id'], 'wav': str(Path(s['wav']).absolute()), 'syllables': count,
                     'seconds': seconds, 'rate': count / seconds})
    baseline = statistics.median(r['rate'] for r in rows)
    for row in rows:
        short = row['seconds'] < 3.6
        target = baseline * .92 if short else baseline
        factor = max(.88, min(1., target / row['rate'])) if short or row['rate'] > baseline * 1.03 else 1.
        # Round upward, preserving the 12% cap and avoiding excess slowing.
        row.update(factor=math.ceil(factor * 1000000) / 1000000,
                   pause_after_s=.6 if short else .3)
    return baseline, rows


def run(sentences, output=None, ffmpeg='ffmpeg'):
    baseline, rows = plan(sentences)
    if output is not None:
        output = Path(output).absolute()
        if output.is_symlink() or output.exists() or not output.parent.is_dir():
            raise ValueError('use a new output directory with an existing parent')
        executable = shutil.which(ffmpeg)
        if not executable:
            raise ValueError('FFmpeg is required; no installation attempted')
        output.mkdir()
        for row in rows:
            if row['factor'] == 1.:
                row['out'] = row['wav']
                continue
            dst = output / (row['id'] + '.slow.wav')
            subprocess.run([executable, '-v', 'error', '-nostdin', '-n', '-i', row['wav'],
                            '-af', f"atempo={row['factor']}", '-c:a', 'pcm_s16le', str(dst)],
                           capture_output=True, check=True, timeout=300)
            row['out'] = str(dst)
        for row in rows:
            row['after_seconds'] = duration(row['out'])
            row['after_rate'] = row['syllables'] / row['after_seconds']
    remaining = sum(r.get('after_rate', r['rate']) > baseline * 1.03 for r in rows)
    return {'baseline_median_syllables_per_s': baseline, 'sentences': rows,
            'remaining_fast_sentences': remaining, 'applied': output is not None,
            'human_action': 'listen; renormalize changed clips and realign scene/caption timing',
            'limitation': 'Rate uses supplied spoken text and trimmed WAV duration, not automatic speech alignment.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--ffmpeg', default='ffmpeg')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        result = run(data, args.out_dir, args.ffmpeg)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 1 if result['remaining_fast_sentences'] or (args.out_dir is None and any(r['factor'] < 1 for r in result['sentences'])) else 0
    except (ValueError, KeyError, TypeError, OSError, wave.Error, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'failed', 'detail': str(exc) if isinstance(exc, ValueError) else 'speech-rate processing failed; originals preserved'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
