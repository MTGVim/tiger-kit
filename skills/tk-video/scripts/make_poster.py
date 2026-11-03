#!/usr/bin/env python3
"""Extract an offline preview JPEG without changing the video's playback start."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from make_feedback_player import safe_input, safe_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', required=True)
    parser.add_argument('--output', help='default: <video stem>.poster.jpg')
    parser.add_argument('--at', type=float, help='preview frame seconds; never a playback offset')
    args = parser.parse_args()
    try:
        video = Path(safe_input(args.video))
        output = Path(safe_output(args.output or str(video.with_suffix('.poster.jpg'))))
        if output.suffix.lower() not in ('.jpg', '.jpeg') or output.exists():
            raise ValueError('poster must be a new JPEG path')
        ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
        if not ffmpeg or not ffprobe:
            raise ValueError('installed ffmpeg and ffprobe are required; no automatic installation')
        info = subprocess.run([ffprobe, '-v', 'error', '-show_format', '-of', 'json', str(video)],
                              capture_output=True, text=True, check=True)
        duration = float(json.loads(info.stdout)['format']['duration'])
        at = min(.5, duration / 2) if args.at is None else args.at
        if not math.isfinite(duration) or not math.isfinite(at) or not 0 <= at < duration:
            raise ValueError('preview time must be inside the measured video duration')
        with tempfile.TemporaryDirectory(prefix='.poster-', dir=output.parent) as stage:
            image = Path(stage) / 'poster.jpg'
            subprocess.run([ffmpeg, '-v', 'error', '-nostdin', '-n', '-ss', str(at), '-i', str(video),
                            '-frames:v', '1', '-q:v', '2', '-threads', '1', str(image)],
                           capture_output=True, check=True)
            if not image.is_file() or not image.stat().st_size:
                raise ValueError('no preview frame was decoded')
            os.link(image, output)
        print(json.dumps({'path': str(output), 'source': str(video), 'preview_seconds': at,
                          'playback_offset_applied': False}, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print('Poster generation failed; source preserved: ' + type(error).__name__, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
