#!/usr/bin/env python3
"""Optional Qwen3 narration. Download only with --download; inference is offline."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import tempfile
import urllib.request

try:
    import resource
except ImportError:
    resource = None

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


def verify(root: Path, data: dict | None = None) -> dict:
    root = safe_directory(root)
    data = manifest() if data is None else data
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


def download(root: Path, data: dict | None = None) -> None:
    root = root.absolute()
    if root.resolve() != root:
        raise ValueError("unsafe model destination")
    root.mkdir(parents=True, exist_ok=True)
    safe_directory(root)
    data = manifest() if data is None else data
    cache = local_hub_cache() / ("models--" + data["repository"].replace("/", "--"))
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
            cached = cache / "snapshots" / data["revision"] / name
            # HF snapshots may link into blobs. Copy only regular bytes inside this repository's cache.
            resolved = cached.resolve()
            if resolved.is_relative_to(cache.resolve()) and resolved.is_file():
                shutil.copyfile(resolved, candidate)
            if not candidate.is_file() or digest(candidate) != expected:
                with urllib.request.urlopen(url, timeout=60) as response, candidate.open("wb") as target:
                    while block := response.read(1024 * 1024):
                        target.write(block)
            if digest(candidate) != expected:
                raise ValueError("download does not match pinned bytes: " + name)
            os.link(candidate, path)
    verify(root, data)


def local_hub_cache() -> Path:
    xdg = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    home = Path(os.environ.get("HF_HOME", str(xdg / "huggingface")))
    return Path(os.environ.get("HF_HUB_CACHE", os.environ.get("HUGGINGFACE_HUB_CACHE", str(home / "hub")))).expanduser()


def verify_runtime(engine: str, data: dict) -> None:
    modules = ["numpy", "soundfile", "cffi"] + (["mlx", "mlx_audio"] if engine == "mlx" else ["torch", "qwen_tts"])
    for name in modules:
        if importlib.util.find_spec(name) is None:
            raise ModuleNotFoundError(name=name)
    packages = {data["package"]["name"]: data["package"]["version"],
                "soundfile": data["dependencies"]["soundfile"]["version"]}
    if engine == "mlx":
        packages["mlx"] = data["mlx_version"]
    for name, version in packages.items():
        actual = importlib.metadata.version(name)
        if actual != version:
            raise ValueError(f"use pinned {name} in the dedicated virtual environment: actual={actual}, expected={version}; restore with this venv Python -m pip install {name}=={version} after installation approval")


def selected_engine(engine: str) -> str:
    if engine not in {"auto", "pytorch", "mlx"}:
        raise ValueError("unsupported narration engine")
    apple = platform.system() == "Darwin" and platform.machine() == "arm64"
    if engine == "mlx" and not apple:
        raise ValueError("MLX narration requires native Apple Silicon")
    return ("mlx" if apple else "pytorch") if engine == "auto" else engine


def mlx_adapter():
    spec = importlib.util.spec_from_file_location("tigerkit_mlx_narration", Path(__file__).with_name("mlx_backend.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sentences(text: str) -> list[str]:
    # Prefer authored sentence-per-line scripts; preserve decimal points and punctuation.
    return [row.strip() for row in re.split(r'(?<=[.!?。！？])\s+|\n+', text.strip()) if row.strip()]


def script_inputs(text_file: Path, output: Path) -> tuple[list[str], Path]:
    text_file, output = text_file.absolute(), output.absolute()
    if text_file.resolve() != text_file or not text_file.is_file():
        raise ValueError("script must be a regular nonsymlink UTF-8 file")
    rows = sentences(text_file.read_text(encoding="utf-8"))
    if not rows:
        raise ValueError("script must be nonempty")
    if output.resolve() != output or output.exists() or not output.parent.is_dir() or output.suffix.lower() != ".wav":
        raise ValueError("audio output must be a new run-owned WAV path")
    return rows, output


def runtime_cache(root: Path) -> Path:
    base = root.absolute().parent
    if base.name == "snapshots":
        base = base.parent
    return base / "runtime-cache"


def configure_runtime(root: Path) -> Path:
    cache = runtime_cache(root)
    if cache.resolve() != cache:
        raise ValueError("unsafe runtime cache path")
    cache.mkdir(parents=True, exist_ok=True)
    for key, suffix in {"XDG_CACHE_HOME": "xdg", "HF_HOME": "huggingface",
                        "HF_HUB_CACHE": "huggingface/hub", "HUGGINGFACE_HUB_CACHE": "huggingface/hub",
                        "TRANSFORMERS_CACHE": "huggingface/hub", "TORCH_HOME": "torch",
                        "NUMBA_CACHE_DIR": "numba"}.items():
        os.environ[key] = str(cache / suffix)
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    return cache


def cache_inventory() -> tuple[set[str], list[str]]:
    entries, unavailable = set(), []
    for root in [Path.home() / ".cache", Path.home() / "Library/Caches"]:
        try:
            if root.exists():
                entries.update(str(path) for path in root.iterdir())
        except OSError:
            unavailable.append(str(root))
    return entries, unavailable


def cache_report(before: set[str], scan_limits: list[str], owned: Path | None) -> dict:
    after, limits = cache_inventory()
    return {"new_cache_entries": sorted(path for path in after - before if owned is None or not owned.is_relative_to(Path(path))),
            "cache_scan_unavailable": sorted(set(scan_limits + limits))}


def memory_metrics() -> dict:
    darwin = platform.system() == "Darwin"
    result = {"peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * (1 if darwin else 1024) if resource else None,
              "peak_footprint_bytes": None, "memory_scope": "narration-process"}
    if darwin:
        # Apple rusage_info_v4: UUID[16], 35 uint64 counters; lifetime peak is counter 28.
        import ctypes
        class RUsageV4(ctypes.Structure):
            _fields_ = [("uuid", ctypes.c_uint8 * 16), ("counters", ctypes.c_uint64 * 35)]
        try:
            library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
            call = library.proc_pid_rusage
            call.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
            call.restype = ctypes.c_int
            usage = RUsageV4()
            if call(os.getpid(), 4, ctypes.byref(usage)) != 0:
                raise OSError("proc_pid_rusage unavailable")
            result["peak_footprint_bytes"] = int(usage.counters[28])
        except (AttributeError, OSError):
            result["memory_limitation"] = "peak footprint unavailable; RSS is not a substitute"
    return result


def write_audio(samples, rate: int, output: Path) -> None:
    import numpy as np
    import soundfile as sf
    with tempfile.TemporaryDirectory(prefix="narration-", dir=output.parent) as directory:
        candidate = Path(directory) / "audio.wav"
        sf.write(candidate, samples, rate, subtype="PCM_16")
        decoded, decoded_rate = sf.read(candidate)
        if decoded_rate != rate or not decoded.size or not np.isfinite(decoded).all() or np.max(np.abs(decoded)) < .0001:
            raise ValueError("audio failed decode verification")
        os.link(candidate, output)


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


def synthesize(root: Path, text_file: Path, output: Path, speaker: str = "sohee", device: str = "auto") -> dict:
    if speaker not in {"serena", "sohee"}:
        raise ValueError("speaker must be serena or sohee")
    if device not in {"auto", "cpu", "mps", "cuda"}:
        raise ValueError("unsupported device")
    data = verify(root)
    verify_runtime("pytorch", data)
    rows, output = script_inputs(text_file, output)
    before, scan_limits = cache_inventory()
    cache = configure_runtime(root)
    import numpy as np
    import soundfile  # Check libsndfile/CFFI before loading model weights.
    import torch
    from qwen_tts import Qwen3TTSModel

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else torch.float16 if device == "cuda" else torch.float32
    model = Qwen3TTSModel.from_pretrained(str(root.absolute()), device_map=device, dtype=dtype,
                                         attn_implementation="eager", local_files_only=True)
    parts, trimmed = [], 0.0
    rate = None
    try:
        for text in rows:
            audio, current_rate = model.generate_custom_voice(text=text, language="Korean", speaker=speaker)
            if not isinstance(current_rate, int) or current_rate <= 0 or (rate is not None and rate != current_rate):
                raise ValueError("invalid or inconsistent narration sample rate")
            rate = current_rate
            samples, removed = trim_leading_silence(audio[0], rate)
            parts.append(samples); trimmed += removed
    finally:
        del model
    samples = np.concatenate(parts)
    write_audio(samples, rate, output)
    return {"path": str(output), "duration_seconds": len(samples) / rate, "trimmed_leading_seconds": trimmed,
            "speaker": speaker, "device": device, "engine": "pytorch", "sentence_count": len(rows),
            "revision": data["revision"], "human_action": "listen", **memory_metrics(),
            **cache_report(before, scan_limits, cache)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=["auto", "pytorch", "mlx"], default="auto")
    parser.add_argument("--quantization", type=int, choices=[5, 8], default=5)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--download", action="store_true", help="Download pinned files after user approval")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--speaker", choices=["serena", "sohee"], default="sohee")
    parser.add_argument("--device", choices=["auto", "cpu", "mps", "cuda"], default="auto")
    parser.add_argument("--text-file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    before, scan_limits = cache_inventory()
    owned_cache = None
    try:
        engine = selected_engine(args.engine)
        backend = mlx_adapter() if engine == "mlx" else None
        data = backend.manifest(args.quantization) if backend else manifest()
        cache = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "tigerkit/tts" / ("mlx" if backend else "qwen3")
        model_dir = args.model_dir or cache / "snapshots" / data["revision"]
        owned_cache = runtime_cache(model_dir)
        if args.verify or args.text_file or args.output:
            verify_runtime(engine, data)
        if args.download:
            download(model_dir, data)
        if args.verify:
            result = verify(model_dir, data)
            print(json.dumps({"verified_files": len(result["files"]), "revision": result["revision"]}))
        if args.text_file or args.output:
            if not args.text_file or not args.output:
                raise ValueError("text-file and output are required together")
            with contextlib.redirect_stdout(sys.stderr):
                if backend:
                    if args.device != "auto":
                        raise ValueError("MLX uses Metal GPU; select --engine pytorch for an explicit PyTorch device")
                    result = backend.synthesize(model_dir, args.text_file, args.output, args.speaker, sys.modules[__name__], args.quantization)
                else:
                    result = synthesize(model_dir, args.text_file, args.output, args.speaker, args.device)
            print(json.dumps(result))
        elif not args.verify and not args.download:
            raise ValueError("select verify, download or synthesis")
        return 0
    except Exception as exc:
        # Dependency/network diagnostics may contain local paths or request details.
        detail = str(exc) if isinstance(exc, ValueError) else "narration unavailable; no audio accepted"
        if isinstance(exc, ModuleNotFoundError) and isinstance(exc.name, str) and re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", exc.name, flags=re.ASCII):
            detail = "missing runtime module: " + exc.name
        print(json.dumps({"narration_status": "unavailable", "error": type(exc).__name__,
                          "detail": detail,
                          **cache_report(before, scan_limits, owned_cache), **memory_metrics()}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
