"""Pinned optional MLX CustomVoice backend; qwen3.py owns the CLI and shared checks."""
from __future__ import annotations

import contextlib
import json
from pathlib import Path
import re
import sys


def manifest(bits: int = 5) -> dict:
    if bits not in (5, 8):
        raise ValueError("supported MLX quantization: 5 or 8")
    filename = "mlx-files.json" if bits == 5 else "mlx-8bit-files.json"
    data = json.loads(Path(__file__).with_name(filename).read_text(encoding="utf-8"))
    revisions = {5: "ea57eb1094e142071162f79568581c9315dfd2e7", 8: "049ef77fe8816b536193c0c25f9a214d17921282"}
    if (data["repository"] != f"mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-{bits}bit"
            or data["revision"] != revisions[bits]
            or data["package"]["version"] != "0.6.1" or data["mlx_version"] != "0.32.4"):
        raise ValueError("unreviewed MLX source")
    for name, digest in data["files"].items():
        if Path(name).is_absolute() or ".." in Path(name).parts or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("invalid pinned MLX file manifest")
    return data


def synthesize(root: Path, text_file: Path, output: Path, speaker: str, common, bits: int = 5) -> dict:
    common.selected_engine("mlx")
    if speaker not in {"serena", "sohee"}:
        raise ValueError("speaker must be serena or sohee")
    data = common.verify(root, manifest(bits))
    common.verify_runtime("mlx", data)
    rows, output = common.script_inputs(text_file, output)
    before, scan_limits = common.cache_inventory()
    cache = common.configure_runtime(root)
    # Offline/cache boundaries must precede all third-party imports and nested tokenizer loads.
    import numpy as np
    import soundfile  # Check libsndfile/CFFI before loading model weights.
    import mlx.core as mx
    from mlx_audio.tts.utils import load_model

    if not mx.metal.is_available():
        raise ValueError("MLX Metal GPU unavailable; no automatic CPU or engine fallback")
    mx.set_default_device(mx.gpu)
    mx.set_cache_limit(0)
    mx.reset_peak_memory()
    parts, trimmed, rate = [], 0.0, None
    # The upstream loader prints diagnostics; keep stdout available for the single JSON receipt.
    with contextlib.redirect_stdout(sys.stderr):
        model = load_model(root.absolute())
        try:
            for text in rows:
                chunks = []
                for result in model.generate_custom_voice(text=text, speaker=speaker, language="Korean",
                                                          verbose=False, stream=False):
                    current_rate = result.sample_rate
                    if not isinstance(current_rate, int) or current_rate <= 0 or (rate is not None and rate != current_rate):
                        raise ValueError("invalid or inconsistent MLX narration sample rate")
                    rate = current_rate
                    chunks.append(np.array(result.audio, dtype=np.float32, copy=True))
                    del result
                if not chunks:
                    raise ValueError("MLX returned no sentence audio")
                samples, removed = common.trim_leading_silence(np.concatenate(chunks), rate)
                parts.append(samples); trimmed += removed
                mx.clear_cache()
        finally:
            del model
            mx.clear_cache()
    samples = np.concatenate(parts)
    common.write_audio(samples, rate, output)
    return {"path": str(output), "duration_seconds": len(samples) / rate, "trimmed_leading_seconds": trimmed,
            "speaker": speaker, "device": "metal", "engine": "mlx", "quantization_bits": bits,
            "cache_limit": 0, "sentence_count": len(rows), "revision": data["revision"],
            "human_action": "listen", "peak_mlx_active_bytes": int(mx.get_peak_memory()),
            **common.memory_metrics(), **common.cache_report(before, scan_limits, cache)}
