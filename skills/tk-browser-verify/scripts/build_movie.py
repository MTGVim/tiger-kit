#!/usr/bin/env python3
"""Assemble optional captioned media from timestamped, run-owned PNG/JPEG frames.

No downloads, recorder, browser control or narration-engine imports occur here.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def regular(path: Path, root: Path | None = None) -> Path:
    path = path.absolute()
    if path.resolve() != path or not path.is_file() or path.stat().st_size == 0:
        raise ValueError("input must be a nonempty regular nonsymlink file")
    if root is not None and not path.is_relative_to(root):
        raise ValueError("input must remain inside the manifest's run directory")
    return path


def number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("timestamps must be finite numbers")
    return float(value)


def load_manifest(path: Path) -> tuple[list[tuple[Path, float]], float, list[dict]]:
    path = regular(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    frames = []
    for row in data["frames"]:
        stamp = number(row["timestamp_ms"])
        image = regular(Path(row["path"]), path.parent)
        if image.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            raise ValueError("frames must be PNG/JPEG")
        if stamp < 0 or (frames and stamp <= frames[-1][1]):
            raise ValueError("frame timestamps must strictly increase")
        frames.append((image, stamp))
    end = number(data["end_ms"])
    if not frames or frames[0][1] != 0 or end <= frames[-1][1]:
        raise ValueError("timeline must start at zero and end after its final frame")
    captions = data.get("captions", [])
    for row in captions:
        start, stop = number(row["start_ms"]), number(row["end_ms"])
        if not 0 <= start < stop <= end or not isinstance(row["text"], str):
            raise ValueError("invalid caption interval/text")
    return frames, end, captions


def probe(path: Path) -> dict:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def srt_time(ms: float) -> str:
    value = round(ms)
    return f"{value // 3600000:02}:{value // 60000 % 60:02}:{value // 1000 % 60:02},{value % 1000:03}"


def subtitle_filter() -> bool:
    result = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, check=True)
    return any(len(parts := line.split()) > 1 and parts[1] == "subtitles" for line in result.stdout.splitlines())


def diagnostic(exc: subprocess.CalledProcessError) -> str:
    raw = exc.stderr or b""
    if isinstance(raw, bytes): raw = raw.decode("utf-8", errors="replace")
    tail = "\n".join(raw.splitlines()[-4:])
    # Redact to the line boundary: paths and header values may contain spaces.
    tail = re.sub(r"(?im)(token|password|authorization|cookie|secret|api[_-]?key)\s*[:=][^\r\n]*", r"\1=<redacted>", tail)
    tail = re.sub(r"https?://[^\r\n]*|(?:[A-Za-z]:)?[/\\][^\r\n]*", "<path-or-url>", tail)
    tail = re.sub(r"(['\"])[^'\"\n]*\1", "<quoted-value>", tail)
    return f"ffmpeg/ffprobe exited {exc.returncode}: " + tail[-600:]


def build(manifest: Path, output: Path, audio: Path | None = None) -> dict:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("installed ffmpeg and ffprobe are required; nothing was downloaded")
    frames, end, captions = load_manifest(manifest)
    root = manifest.absolute().parent
    output = output.absolute()
    if output.resolve() != output or output.exists() or not output.parent.is_dir() or not output.is_relative_to(root):
        raise ValueError("output must be a new run-owned path inside the manifest directory")
    kind = output.suffix.lower()
    if kind not in {".mp4", ".gif"}:
        raise ValueError("output must have an .mp4 or .gif suffix")
    warnings = []
    burn = bool(captions) and subtitle_filter()
    sidecar = output.with_suffix(".srt") if captions else None
    if sidecar and (sidecar.resolve() != sidecar or (sidecar.exists() and not sidecar.is_file())):
        raise ValueError("caption sidecar must be a regular run-owned file")
    if captions and not burn:
        warnings.append("ffmpeg lacks the subtitles filter; hard captions blocked, soft captions retained")
    if kind == ".gif" and audio is not None:
        warnings.append("GIF has no audio; narration omitted")
        audio = None
    if audio is not None:
        try:
            audio = regular(audio, root)
            info = probe(audio)
            duration = float(info["format"]["duration"])
            if not any(s.get("codec_type") == "audio" for s in info["streams"]) or not 0 < duration <= end / 1000:
                raise ValueError("audio does not fit the observed movie duration")
        except (ValueError, KeyError, OSError, subprocess.SubprocessError):
            warnings.append("audio omitted: invalid, unavailable or longer than movie; captions retained")
            audio = None
    with tempfile.TemporaryDirectory(prefix="movie-", dir=output.parent) as directory:
        stage = Path(directory)
        lines = ["ffconcat version 1.0"]
        for i, (image, stamp) in enumerate(frames):
            name = f"frame-{i:06}{image.suffix.lower()}"
            shutil.copyfile(image, stage / name)
            stop = frames[i + 1][1] if i + 1 < len(frames) else end
            lines.extend([f"file '{name}'", f"duration {(stop - stamp) / 1000:.9f}"])
        lines.append(f"file 'frame-{len(frames)-1:06}{frames[-1][0].suffix.lower()}'")
        (stage / "frames.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        if captions:
            text = "\n\n".join(f"{i+1}\n{srt_time(c['start_ms'])} --> {srt_time(c['end_ms'])}\n" +
                                  c["text"].replace("\r", " ").replace("\n", " ")
                                  for i, c in enumerate(captions))
            (stage / "captions.srt").write_text(text + "\n", encoding="utf-8")
            if sidecar.exists() and sidecar.read_bytes() != (stage / "captions.srt").read_bytes():
                raise ValueError("existing caption sidecar differs; it was preserved")
        cmd = ["ffmpeg", "-v", "error", "-nostdin", "-n", "-threads", "1", "-f", "concat", "-safe", "1", "-i", "frames.txt"]
        if audio is not None:
            cmd += ["-i", str(audio)]
        soft = bool(captions) and not burn and kind == ".mp4"
        if soft:
            cmd += ["-i", "captions.srt"]
        filters = "fps=10,pad=ceil(iw/2)*2:ceil(ih/2)*2"
        if burn:
            filters += ",subtitles=filename=captions.srt"
        if kind == ".mp4":
            cmd += ["-map", "0:v:0"]
            if audio is not None: cmd += ["-map", "1:a:0"]
            if soft: cmd += ["-map", f"{2 if audio is not None else 1}:0", "-c:s", "mov_text"]
            cmd += ["-vf", filters, "-t", str(end / 1000), "-c:v", "libx264", "-threads", "1", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
            cmd += ["-af", "apad", "-c:a", "aac", "-ac", "1", "-b:a", "48k"] if audio is not None else ["-an"]
        else:
            cmd += ["-filter_complex", filters + ",split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    "-t", str(end / 1000), "-loop", "0", "-an"]
        cmd.append("movie" + kind)
        env = dict(os.environ, TMPDIR=directory)
        subprocess.run(cmd, cwd=stage, env=env, capture_output=True, check=True)
        movie = stage / ("movie" + kind)
        info = probe(movie)
        stream = next(s for s in info["streams"] if s["codec_type"] == "video")
        if stream["codec_name"] != ("h264" if kind == ".mp4" else "gif") or abs(float(info["format"]["duration"]) - end / 1000) > .15:
            raise ValueError("encoded duration/codec differs from the frame timeline")
        subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(movie), "-f", "null", "-"],
                       env=env, capture_output=True, check=True)
        if sidecar:
            try:
                os.link(stage / "captions.srt", sidecar)
            except FileExistsError:
                if sidecar.resolve() != sidecar or not sidecar.is_file() or sidecar.read_bytes() != (stage / "captions.srt").read_bytes():
                    raise ValueError("caption sidecar appeared during encoding; it was preserved") from None
        # Exclusive create preserves unrelated files even if output appeared during encoding.
        try:
            os.link(movie, output)
        except FileExistsError:
            raise ValueError("output appeared during encoding; it was preserved") from None
    if kind == ".gif" and output.stat().st_size > 5 * 1024 * 1024:
        warnings.append("GIF exceeds the 5MiB target; retained locally with an oversize warning")
    return {"path": str(output), "media_type": "video/mp4" if kind == ".mp4" else "image/gif", "duration_ms": end,
            "fps": 10, "audio": audio is not None, "warnings": warnings,
            "media_status": "blocked" if captions and not burn else "ready",
            "prerequisite": "ffmpeg-subtitles-filter" if captions and not burn else None,
            "subtitles": "hard" if burn else "soft" if soft else "sidecar" if captions else "none",
            "captions_path": str(sidecar) if sidecar else None,
            "verification_status": "not-assessed", "source_frames_preserved": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    args = parser.parse_args()
    try:
        result = build(args.manifest, args.output, args.audio)
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result["media_status"] == "blocked" else 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"media_status": "failed", "error": type(exc).__name__,
                          "detail": str(exc) if isinstance(exc, ValueError) else diagnostic(exc) if isinstance(exc, subprocess.CalledProcessError) else "media assembly failed; input frames preserved"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
