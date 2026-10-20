#!/usr/bin/env python3
"""Optional Qwen3 narration. Download only with --download; inference is offline."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import tempfile
import urllib.request

MANIFEST = Path(__file__).with_name("qwen3-files.json")


def manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if (data["repository"] != "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
            or data["revision"] != "85e237c12c027371202489a0ec509ded67b5e4b5"
            or data["package"]["version"] != "0.1.1"):
        raise ValueError("unreviewed Qwen3 source")
    for name, digest in data["files"].items():
        if Path(name).is_absolute() or ".." in Path(name).parts or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("invalid pinned file manifest")
    return data


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def safe_directory(root: Path) -> Path:
    root = root.absolute()
    if root.resolve() != root or not root.is_dir():
        raise ValueError("model directory must be a regular nonsymlink directory")
    return root


def verify(root: Path) -> dict:
    root = safe_directory(root)
    data = manifest()
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("snapshot contains a symlink")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != set(data["files"]):
        raise ValueError("snapshot contains missing or unpinned files; preserve it and select a clean snapshot")
    for name, expected in data["files"].items():
        path = root / name
        if path.resolve() != path or digest(path) != expected:
            raise ValueError("mismatched pinned model file: " + name)
    return data


def download(root: Path) -> None:
    root = root.absolute()
    if root.resolve() != root:
        raise ValueError("unsafe model destination")
    root.mkdir(parents=True, exist_ok=True)
    safe_directory(root)
    data = manifest()
    for name, expected in data["files"].items():
        path = root / name
        if path.resolve() != path:
            raise ValueError("unsafe model path")
        if path.exists():
            if not path.is_file() or digest(path) != expected:
                raise ValueError("existing mismatched model file preserved: " + name)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/{data['repository']}/resolve/{data['revision']}/{name}"
        # Stream large weights; interrupted downloads never become accepted snapshot files.
        with tempfile.TemporaryDirectory(prefix="qwen3-download-", dir=root.parent) as directory:
            candidate = Path(directory) / "file"
            with urllib.request.urlopen(url, timeout=60) as response, candidate.open("xb") as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
            if digest(candidate) != expected:
                raise ValueError("download does not match pinned bytes: " + name)
            os.link(candidate, path)
    verify(root)


def trim_leading_silence(audio, rate: int):
    import numpy as np
    samples = np.asarray(audio, dtype=np.float32)
    if samples.ndim != 1 or not samples.size or not np.isfinite(samples).all():
        raise ValueError("invalid narration samples")
    window = max(1, round(rate * .01))
    onset = None
    for start in range(0, len(samples), window):
        if float(np.sqrt(np.mean(samples[start:start + window] ** 2))) >= .003:
            onset = max(0, start - round(rate * .04))
            break
    if onset is None:
        raise ValueError("silent narration")
    return samples[onset:], onset / rate


def synthesize(root: Path, text_file: Path, output: Path, speaker: str = "serena", device: str = "auto") -> dict:
    if speaker not in {"serena", "sohee"}:
        raise ValueError("speaker must be serena or sohee")
    if device not in {"auto", "cpu", "mps", "cuda"}:
        raise ValueError("unsupported device")
    data = verify(root)
    if importlib.metadata.version("qwen-tts") != data["package"]["version"]:
        raise ValueError("use the pinned qwen-tts package in the dedicated virtual environment")
    text_file, output = text_file.absolute(), output.absolute()
    if text_file.resolve() != text_file or not text_file.is_file():
        raise ValueError("script must be a regular nonsymlink UTF-8 file")
    text = text_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("script must be nonempty")
    if output.resolve() != output or output.exists() or not output.parent.is_dir() or output.suffix.lower() != ".wav":
        raise ValueError("audio output must be a new run-owned WAV path")
    # Set before importing HF/Qwen: all nested model/processor loads stay offline too.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    import numpy as np
    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else torch.float16 if device == "cuda" else torch.float32
    model = Qwen3TTSModel.from_pretrained(str(root.absolute()), device_map=device, dtype=dtype,
                                         attn_implementation="eager", local_files_only=True)
    try:
        audio, rate = model.generate_custom_voice(text=text, language="Korean", speaker=speaker)
    finally:
        del model
    if not isinstance(rate, int) or rate <= 0:
        raise ValueError("invalid narration sample rate")
    samples, trimmed = trim_leading_silence(audio[0], rate)
    with tempfile.TemporaryDirectory(prefix="narration-", dir=output.parent) as directory:
        candidate = Path(directory) / "audio.wav"
        sf.write(candidate, samples, rate, subtype="PCM_16")
        decoded, decoded_rate = sf.read(candidate)
        if decoded_rate != rate or not decoded.size or not np.isfinite(decoded).all() or np.max(np.abs(decoded)) < .0001:
            raise ValueError("audio failed decode verification")
        os.link(candidate, output)
    return {"path": str(output), "duration_seconds": len(samples) / rate, "trimmed_leading_seconds": trimmed,
            "speaker": speaker, "device": device, "revision": data["revision"], "human_action": "listen"}


def main() -> int:
    data = manifest()
    cache = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "tigerkit/tts/qwen3"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, default=cache / "snapshots" / data["revision"])
    parser.add_argument("--download", action="store_true", help="Download pinned files after user approval")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--speaker", choices=["serena", "sohee"], default="serena")
    parser.add_argument("--device", choices=["auto", "cpu", "mps", "cuda"], default="auto")
    parser.add_argument("--text-file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.download:
            download(args.model_dir)
        if args.verify:
            result = verify(args.model_dir)
            print(json.dumps({"verified_files": len(result["files"]), "revision": result["revision"]}))
        if args.text_file or args.output:
            if not args.text_file or not args.output:
                raise ValueError("text-file and output are required together")
            print(json.dumps(synthesize(args.model_dir, args.text_file, args.output, args.speaker, args.device)))
        elif not args.verify and not args.download:
            raise ValueError("select verify, download or synthesis")
        return 0
    except Exception as exc:
        # Dependency/network diagnostics may contain local paths or request details.
        print(json.dumps({"narration_status": "unavailable", "error": type(exc).__name__,
                          "detail": str(exc) if isinstance(exc, ValueError) else "narration unavailable; no audio accepted"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
