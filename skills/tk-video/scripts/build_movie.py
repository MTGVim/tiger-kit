#!/usr/bin/env python3
"""Assemble captioned media from observed timestamps or explanatory still holds.

No downloads, recorder, browser control or narration-engine imports occur here.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
from statistics import median
import subprocess
import tempfile
import wave


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


def frame_rate(data: dict, frames: list, kind: str, override: float | None) -> tuple[float, str]:
    if override is not None:
        rate = number(override)
        if not 0 < rate <= 30:
            raise ValueError("fps must be positive and at most 30")
        return rate, "override"
    if kind == ".gif" or data.get("mode", "evidence") == "explainer":
        return 10.0, "default"
    if "source_fps" in data:
        rate = number(data["source_fps"])
        if rate <= 0:
            raise ValueError("source_fps must be positive")
        return min(30.0, rate), "source_fps"
    if len(frames) >= 3:
        # CDP may omit stable frames: exclude the final hold and resist isolated idle gaps.
        interval = median(b[1] - a[1] for a, b in zip(frames, frames[1:]))
        return min(30.0, 1000 / interval), "timestamps"
    return 10.0, "fallback"


def timeline(data: dict, root: Path, ffprobe: str = "ffprobe") -> tuple[list[tuple[Path, float]], float, list[dict]]:
    mode = data.get("mode", "evidence")
    narration_requested = data.get("narration_requested", False)
    if not isinstance(narration_requested, bool):
        raise ValueError("narration_requested must be boolean")
    if mode not in {"evidence", "explainer"}:
        raise ValueError("mode must be evidence or explainer")
    frames = []
    cursor = 0.0
    scene_captions = []
    for row in data["frames"]:
        stamp = number(row["timestamp_ms"]) if mode == "evidence" else cursor
        image = regular(Path(row["path"]), root)
        if image.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            raise ValueError("frames must be PNG/JPEG")
        if stamp < 0 or (frames and stamp <= frames[-1][1]):
            raise ValueError("frame timestamps must strictly increase")
        frames.append((image, stamp))
        if mode == "explainer":
            voice_duration = 0.0
            if row.get("audio_path") is not None:
                voice = regular(Path(row["audio_path"]), root)
                voice_duration = float(probe(voice, ffprobe)["format"]["duration"]) * 1000
                if not math.isfinite(voice_duration) or voice_duration <= 0:
                    raise ValueError("scene audio must have a finite positive duration")
            hold = number(row.get("hold_ms", max(3000, voice_duration + 250)))
            if hold <= 0: raise ValueError("presentation holds must be positive")
            if hold < voice_duration: raise ValueError("scene hold is shorter than accepted narration")
            source = row.get("source_kind", "capture")
            if source not in {"capture", "rendered"}: raise ValueError("source_kind must be capture or rendered")
            caption = row.get("caption", "")
            if not isinstance(caption, str): raise ValueError("scene caption must be text")
            in_picture = row.get("source_in_picture", False)
            if not isinstance(in_picture, bool): raise ValueError("source_in_picture must be boolean")
            if source == "rendered" and not in_picture:
                label = row.get("source_label", "렌더링 장면")
                if not isinstance(label, str) or not label.strip(): raise ValueError("source_label must be nonempty text")
                caption = "[" + label + "] " + caption
            if caption: scene_captions.append({"start_ms": cursor, "end_ms": cursor + hold, "text": caption})
            cursor += hold
    end = number(data["end_ms"]) if mode == "evidence" else cursor
    if not frames or frames[0][1] != 0 or end <= frames[-1][1]:
        raise ValueError("timeline must start at zero and end after its final frame")
    captions = data.get("captions", scene_captions)
    for row in captions:
        start, stop = number(row["start_ms"]), number(row["end_ms"])
        if not 0 <= start < stop <= end or not isinstance(row["text"], str):
            raise ValueError("invalid caption interval/text")
    return frames, end, captions


def load_manifest(path: Path) -> tuple[list[tuple[Path, float]], float, list[dict]]:
    path = regular(path)
    return timeline(json.loads(path.read_text(encoding="utf-8")), path.parent)


def probe(path: Path, ffprobe: str = "ffprobe") -> dict:
    result = subprocess.run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def srt_time(ms: float) -> str:
    value = round(ms)
    return f"{value // 3600000:02}:{value // 60000 % 60:02}:{value // 1000 % 60:02},{value % 1000:03}"


def subtitle_filter(ffmpeg: str = "ffmpeg") -> bool:
    result = subprocess.run([ffmpeg, "-hide_banner", "-filters"], capture_output=True, text=True, check=True)
    return any(len(parts := line.split()) > 1 and parts[1] == "subtitles" for line in result.stdout.splitlines())


def media_tools(override: str | None, captions: bool) -> tuple[str, str, bool]:
    selected = override or os.environ.get("TIGERKIT_FFMPEG")
    ffmpeg = shutil.which(selected or "ffmpeg")
    if not ffmpeg:
        raise ValueError("installed ffmpeg is required; nothing was downloaded")
    burn = captions and subtitle_filter(ffmpeg)
    if captions and not burn and not selected and shutil.which("brew"):
        prefix = subprocess.run(["brew", "--prefix", "ffmpeg-full"], capture_output=True, text=True)
        candidate = Path(prefix.stdout.strip()) / "bin/ffmpeg"
        if prefix.returncode == 0 and candidate.is_absolute() and candidate.is_file() and os.access(candidate, os.X_OK):
            if subtitle_filter(str(candidate)):
                ffmpeg, burn = str(candidate), True
    sibling = Path(ffmpeg).parent / "ffprobe"
    ffprobe = str(sibling) if sibling.is_file() and os.access(sibling, os.X_OK) else shutil.which("ffprobe")
    if not ffprobe:
        raise ValueError("installed ffprobe is required; nothing was downloaded")
    return ffmpeg, ffprobe, bool(burn)


def diagnostic(exc: subprocess.CalledProcessError) -> str:
    raw = exc.stderr or b""
    if isinstance(raw, bytes): raw = raw.decode("utf-8", errors="replace")
    tail = "\n".join(raw.splitlines()[-4:])
    # Redact to the line boundary: paths and header values may contain spaces.
    tail = re.sub(r"(?im)(token|password|authorization|cookie|secret|api[_-]?key)\s*[:=][^\r\n]*", r"\1=<redacted>", tail)
    tail = re.sub(r"https?://[^\r\n]*|(?:[A-Za-z]:)?[/\\][^\r\n]*", "<path-or-url>", tail)
    tail = re.sub(r"(['\"])[^'\"\n]*\1", "<quoted-value>", tail)
    return f"ffmpeg/ffprobe exited {exc.returncode}: " + tail[-600:]


def audio_scenes(data: dict, frames: list, end: float, root: Path, ffprobe: str) -> list[tuple[float, float, Path | None, float]]:
    if data.get("mode", "evidence") == "explainer":
        if "scenes" in data:
            raise ValueError("explainer uses frame audio_path, not evidence scenes")
        rows = [{"start_ms": frame[1], "audio_path": row.get("audio_path")} for row, frame in zip(data["frames"], frames)]
    else:
        if any(row.get("audio_path") is not None for row in data["frames"]):
            raise ValueError("evidence audio belongs in scenes with observed start_ms")
        rows = data.get("scenes", [])
        if not isinstance(rows, list):
            raise ValueError("scenes must be an ordered list")
    result = []
    for i, row in enumerate(rows):
        start = number(row["start_ms"])
        stop = number(rows[i + 1]["start_ms"]) if i + 1 < len(rows) else end
        if not 0 <= start < stop <= end:
            raise ValueError("scene starts must strictly increase inside the observed timeline")
        voice = regular(Path(row["audio_path"]), root) if row.get("audio_path") is not None else None
        duration = 0.0
        if voice:
            info = probe(voice, ffprobe)
            duration = number(float(info["format"]["duration"])) * 1000
            if not any(s.get("codec_type") == "audio" for s in info["streams"]) or not 0 < duration <= stop - start:
                raise ValueError("scene narration overlaps the next scene or exceeds the movie")
        result.append((start, stop, voice, duration))
    return result


def scene_audio(scenes: list, root: Path, stage: Path, env: dict, ffmpeg: str) -> tuple[Path, float]:
    output = stage / "scene-audio.wav"
    speech_end = 0.0
    with wave.open(str(output), "wb") as joined:
        joined.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
        samples_written = 0
        for i, (start, stop, voice, duration) in enumerate(scenes):
            gap = round(start * 22050 / 1000) - samples_written
            while gap > 0:
                count = min(gap, 32768)
                joined.writeframesraw(b"\0" * count * 2)
                samples_written += count
                gap -= count
            cmd = [ffmpeg, "-v", "error", "-nostdin", "-n"]
            if voice is not None:
                speech_end = max(speech_end, start + duration)
                cmd += ["-i", str(voice), "-af", "apad"]
            else:
                cmd += ["-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono"]
            raw = stage / f"scene-{i}.pcm"
            cmd += ["-t", str((stop - start) / 1000), "-ac", "1", "-ar", "22050", "-f", "s16le", str(raw)]
            subprocess.run(cmd, env=env, capture_output=True, check=True)
            with raw.open("rb") as source:
                while block := source.read(65536):
                    joined.writeframesraw(block)
                    samples_written += len(block) // 2
    return output, speech_end


def build(manifest: Path, output: Path, audio: Path | None = None, ffmpeg: str | None = None,
          fps: float | None = None) -> dict:
    manifest = regular(manifest)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    ffmpeg, ffprobe, caption_support = media_tools(ffmpeg, True)
    root = manifest.parent
    frames, end, captions = timeline(data, root, ffprobe)
    mode = data.get("mode", "evidence")
    narration_requested = data.get("narration_requested", False)
    scenes = audio_scenes(data, frames, end, root, ffprobe)
    scene_voices = any(row[2] is not None for row in scenes)
    if scene_voices and audio is not None:
        raise ValueError("scene audio cannot be combined with a separate full track")
    output = output.absolute()
    if output.resolve() != output or output.exists() or not output.parent.is_dir() or not output.is_relative_to(root):
        raise ValueError("output must be a new run-owned path inside the manifest directory")
    kind = output.suffix.lower()
    if kind not in {".mp4", ".gif"}:
        raise ValueError("output must have an .mp4 or .gif suffix")
    selected_fps, fps_source = frame_rate(data, frames, kind, fps)
    rate = Fraction(selected_fps).limit_denominator(100000)
    rate_text = f"{rate.numerator}/{rate.denominator}"
    warnings = []
    if fps_source == "timestamps":
        warnings.append("source fps estimated from median capture intervals; idle/event-driven captures may not expose the original rate")
    elif fps_source == "fallback":
        warnings.append("source fps unavailable: fewer than three frames; using 10fps")
    errors = []
    contact = output.with_name(output.name + ".contact.png")
    if contact.resolve() != contact or contact.exists():
        raise ValueError("contact sheet must be a new run-owned path")
    burn = bool(captions) and caption_support
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
            info = probe(audio, ffprobe)
            duration = float(info["format"]["duration"])
            if not any(s.get("codec_type") == "audio" for s in info["streams"]) or not 0 < duration <= end / 1000:
                raise ValueError("audio does not fit the observed movie duration")
        except (ValueError, KeyError, OSError, subprocess.SubprocessError):
            warnings.append("audio omitted: invalid, unavailable or longer than movie; captions retained")
            audio = None
    audio_duration = duration * 1000 if audio is not None else 0
    with tempfile.TemporaryDirectory(prefix="movie-", dir=output.parent) as directory:
        stage = Path(directory)
        env = dict(os.environ, TMPDIR=directory, XDG_CACHE_HOME=str(stage / "cache"))
        if scene_voices and kind == ".mp4":
            audio, audio_duration = scene_audio(scenes, root, stage, env, ffmpeg)
        elif scene_voices:
            warnings.append("GIF has no audio; scene narration omitted")
        if narration_requested:
            if audio is None: errors.append("narration-missing")
            if not captions:
                errors.append("narration-subtitles-short")
        if audio is not None and captions and max(row["end_ms"] for row in captions) < audio_duration:
            errors.append("narration-subtitles-short")
        lines = ["ffconcat version 1.0"]
        hashes = []
        for i, (image, stamp) in enumerate(frames):
            name = f"frame-{i:06}{image.suffix.lower()}"
            shutil.copyfile(image, stage / name)
            hashes.append(hashlib.sha256((stage / name).read_bytes()).digest())
            stop = frames[i + 1][1] if i + 1 < len(frames) else end
            lines.extend([f"file '{name}'", "option framerate 1000000", f"duration {(stop - stamp) / 1000:.9f}"])
        lines.append(f"file 'frame-{len(frames)-1:06}{frames[-1][0].suffix.lower()}'")
        lines.append("option framerate 1000000")
        if mode == "evidence":
            longest = current = 0.0
            for i, digest in enumerate(hashes):
                stop = frames[i + 1][1] if i + 1 < len(frames) else end
                current = current + stop - frames[i][1] if i and digest == hashes[i - 1] else stop - frames[i][1]
                longest = max(longest, current)
            if len(set(hashes)) == 1 or longest / end >= .8:
                warnings.append("repeated evidence frames dominate the timeline; inspect stable or missing motion")
        (stage / "frames.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        if captions:
            text = "\n\n".join(f"{i+1}\n{srt_time(c['start_ms'])} --> {srt_time(c['end_ms'])}\n" +
                                  c["text"].replace("\r", " ").replace("\n", " ")
                                  for i, c in enumerate(captions))
            (stage / "captions.srt").write_text(text + "\n", encoding="utf-8")
            if sidecar.exists() and sidecar.read_bytes() != (stage / "captions.srt").read_bytes():
                raise ValueError("existing caption sidecar differs; it was preserved")
        # Only generated relative frame names/options enter this private concat file.
        cmd = [ffmpeg, "-v", "error", "-nostdin", "-n", "-threads", "1", "-f", "concat", "-safe", "0", "-i", "frames.txt"]
        if audio is not None:
            cmd += ["-i", str(audio)]
        soft = bool(captions) and not burn and kind == ".mp4"
        if soft:
            cmd += ["-i", "captions.srt"]
        filters = f"fps={rate_text},pad=ceil(iw/2)*2:ceil(ih/2)*2"
        if burn:
            # Evidence frames preserve the complete UI; captions live in an appended band.
            if mode == "evidence":
                filters += ",pad=iw:ceil((ih+max(48\\,ih*0.2))/2)*2:0:0:black"
            filters += ",subtitles=filename=captions.srt:force_style='FontName=Noto Sans CJK KR,FontSize=7,MarginV=5,Alignment=2,Outline=1'"
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
        subprocess.run(cmd, cwd=stage, env=env, capture_output=True, check=True)
        movie = stage / ("movie" + kind)
        info = probe(movie, ffprobe)
        stream = next(s for s in info["streams"] if s["codec_type"] == "video")
        actual_fps = float(Fraction(stream["avg_frame_rate"]))
        # An encoded final frame is quantized to one output-frame interval.
        duration_tolerance = max(.15, 1 / selected_fps)
        if stream["codec_name"] != ("h264" if kind == ".mp4" else "gif") or abs(float(info["format"]["duration"]) - end / 1000) > duration_tolerance:
            raise ValueError("encoded duration/codec differs from the frame timeline")
        if kind == ".mp4" and not math.isclose(actual_fps, float(rate), rel_tol=.001):
            raise ValueError("encoded fps differs from the selected frame rate")
        subprocess.run([ffmpeg, "-v", "error", "-nostdin", "-i", str(movie), "-f", "null", "-"],
                       env=env, capture_output=True, check=True)
        audio_streams = [s for s in info["streams"] if s["codec_type"] == "audio"]
        if audio is not None:
            if not audio_streams or audio_streams[0].get("codec_name") != "aac" or audio_streams[0].get("channels") != 1:
                errors.append("audio-stream-mismatch")
            elif abs(float(audio_streams[0].get("duration", 0)) - end / 1000) > .15:
                errors.append("audio-duration-mismatch")
        if narration_requested and audio_streams:
            measured = subprocess.run([ffmpeg, "-v", "info", "-nostdin", "-i", str(movie),
                "-map", "0:a:0", "-af", "volumedetect", "-f", "null", "-"], env=env,
                capture_output=True, text=True, check=True)
            peak = re.search(r"max_volume:\s*(-?[\d.]+) dB", measured.stderr)
            if peak is None or float(peak.group(1)) <= -80:
                errors.append("narration-silent")
        samples = min(12, max(1, math.ceil(end / 1000)))
        subprocess.run([ffmpeg, "-v", "error", "-nostdin", "-n", "-i", str(movie),
            "-vf", f"fps={samples * 1000 / end},scale=320:-1,tile=3x{math.ceil(samples / 3)}",
            "-frames:v", "1", "-threads", "1", "contact.png"], cwd=stage, env=env,
            capture_output=True, check=True)
        os.link(stage / "contact.png", contact)
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
            "mode": mode, "timing": "observed" if mode == "evidence" else "presentation",
            "fps": actual_fps, "selected_fps": float(rate), "fps_source": fps_source,
            "encoded_duration_ms": float(info["format"]["duration"]) * 1000,
            "audio": audio is not None, "warnings": warnings,
            "ffmpeg_path": ffmpeg, "ffprobe_path": ffprobe,
            "media_status": "failed" if errors else "blocked" if captions and not burn else "ready",
            "media_validation": {"status": "fail" if errors else "pass", "errors": errors},
            "contact_sheet": str(contact),
            "prerequisite": "ffmpeg-subtitles-filter" if captions and not burn else None,
            "subtitles": "hard" if burn else "soft" if soft else "sidecar" if captions else "none",
            "captions_path": str(sidecar) if sidecar else None,
            "verification_status": "not-assessed", "source_frames_preserved": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--ffmpeg", help="Use this installed ffmpeg; overrides TIGERKIT_FFMPEG and discovery")
    parser.add_argument("--fps", type=float, help="Override output fps (positive, at most 30); scene times stay unchanged")
    args = parser.parse_args()
    try:
        result = build(args.manifest, args.output, args.audio, args.ffmpeg, args.fps)
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result["media_status"] == "blocked" else 1 if result["media_status"] == "failed" else 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"media_status": "failed", "error": type(exc).__name__,
                          "detail": str(exc) if isinstance(exc, ValueError) else diagnostic(exc) if isinstance(exc, subprocess.CalledProcessError) else "media assembly failed; input frames preserved"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
