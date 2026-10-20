#!/usr/bin/env python3
"""Optional, removable ppaso adapter. No inference dependencies import until synthesis."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import types
import urllib.request


MANIFEST = Path(__file__).with_name("ppaso-files.json")


def manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data["repository"] != "akamotaco/ppaso-tts-v1" or data["revision"] != "53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9":
        raise ValueError("unreviewed ppaso source")
    for name, digest in data["files"].items():
        if Path(name).is_absolute() or ".." in Path(name).parts or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("invalid pinned file manifest")
    return data


def verify(root: Path) -> dict:
    root = root.absolute()
    if root.resolve() != root or not root.is_dir():
        raise ValueError("model directory must be a regular nonsymlink directory")
    data = manifest()
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("snapshot contains a symlink")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != set(data["files"]):
        raise ValueError("snapshot contains missing or unpinned files; preserve it and select a clean snapshot")
    for name, digest in data["files"].items():
        path = root / name
        if path.resolve() != path or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("missing, unsafe or mismatched pinned model file: " + name)
    return data


def download(root: Path) -> None:
    root = root.absolute()
    if root.resolve() != root:
        raise ValueError("unsafe model destination")
    root.mkdir(parents=True, exist_ok=True)
    data = manifest()
    for name, digest in data["files"].items():
        path = root / name
        if path.resolve() != path:
            raise ValueError("unsafe model path")
        if path.exists():
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("existing mismatched model file preserved: " + name)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/{data['repository']}/resolve/{data['revision']}/{name}"
        with urllib.request.urlopen(url, timeout=60) as response:
            content = response.read(64 * 1024 * 1024 + 1)
        if len(content) > 64 * 1024 * 1024 or hashlib.sha256(content).hexdigest() != digest:
            raise ValueError("download does not match pinned bytes: " + name)
        with path.open("xb") as target:
            target.write(content)
    verify(root)


def synthesize(root: Path, text_file: Path, output: Path, user_dict: Path | None = None) -> dict:
    verify(root)
    root = root.absolute()
    # The upstream importer uses generic runtime.* names. Never inherit another snapshot's modules.
    if any(name == "runtime" or name.startswith("runtime.") for name in sys.modules):
        raise ValueError("runtime package already loaded; use a fresh narration process")
    sys.dont_write_bytecode = True
    import numpy as np
    import soundfile as sf

    text_file, output = text_file.absolute(), output.absolute()
    if text_file.resolve() != text_file or not text_file.is_file() or not text_file.read_text(encoding="utf-8").strip():
        raise ValueError("script must be a nonempty nonsymlink UTF-8 file")
    if output.resolve() != output or output.exists() or not output.parent.is_dir() or output.suffix.lower() != ".wav":
        raise ValueError("audio output must be a new run-owned WAV path")
    mapping = json.loads(user_dict.read_text(encoding="utf-8")) if user_dict else {}
    if not isinstance(mapping, dict) or any(not isinstance(k, str) or not isinstance(v, str) or not k or not v for k, v in mapping.items()):
        raise ValueError("user_dict must map nonempty terms to pronunciations")
    # Bind the namespace: a regular runtime package elsewhere on sys.path would otherwise win.
    runtime = types.ModuleType("runtime")
    runtime.__path__ = [str(root / "runtime")]
    runtime.__package__ = "runtime"
    sys.modules["runtime"] = runtime
    previous_lexicon = os.environ.get("PPASO_LEXICON")
    os.environ["PPASO_LEXICON"] = str(root / "runtime/dict/korean_mfa.dict")
    try:
        spec = importlib.util.spec_from_file_location("ppaso_tts", root / "example/ppaso_tts.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        tts = module.PpasoTTS(str(root), backend="onnx", user_dict=mapping)
        wav = tts.synthesize(text_file.read_text(encoding="utf-8"))
    finally:
        if previous_lexicon is None:
            os.environ.pop("PPASO_LEXICON", None)
        else:
            os.environ["PPASO_LEXICON"] = previous_lexicon
    if not wav.size or not np.isfinite(wav).all() or float(np.max(np.abs(wav))) < .0001:
        raise ValueError("invalid or silent narration")
    with tempfile.TemporaryDirectory(prefix="narration-", dir=output.parent) as temp:
        candidate = Path(temp) / "audio.wav"
        sf.write(candidate, wav, 22050)
        decoded, rate = sf.read(candidate)
        if rate != 22050 or not decoded.size or not np.isfinite(decoded).all():
            raise ValueError("audio failed decode verification")
        with output.open("xb") as dest:
            dest.write(candidate.read_bytes())
    return {"path": str(output), "duration_seconds": len(wav) / 22050, "revision": manifest()["revision"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--download", action="store_true", help="Explicitly download only the pinned snapshot")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--text-file", type=Path)
    parser.add_argument("--user-dict", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.download:
            download(args.model_dir)
        if args.verify:
            data = verify(args.model_dir)
            print(json.dumps({"verified_files": len(data["files"]), "revision": data["revision"]}))
        if args.text_file or args.output:
            if not args.text_file or not args.output:
                raise ValueError("text-file and output are required together")
            print(json.dumps(synthesize(args.model_dir, args.text_file, args.output, args.user_dict)))
        if not args.verify and not args.text_file:
            raise ValueError("select verification or synthesis")
        return 0
    except Exception as exc:
        print(json.dumps({"narration_status": "omitted", "error": type(exc).__name__,
                          "detail": str(exc) if isinstance(exc, ValueError) else "narration unavailable; continue with captions"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
