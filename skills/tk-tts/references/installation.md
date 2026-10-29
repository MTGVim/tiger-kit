# Installation and Pinned Models

Inspect current Python/device/dependencies first; `scripts/list_options.py` does no installation
or network access. Before first setup propose the selected dedicated venv, exact manifest,
platform wheel hashes, model/cache size, location and text-egress policy; reuse matching approval.
Selecting video/TTS is not approval for a global pip install, extra model or paid call.

Qwen MLX uses `qwen3.py --engine mlx --quantization 5` by default on native Apple Silicon;
`--quantization 8` preserves the previous model/cache. Other devices keep official `--engine
pytorch` with explicit auto/cpu/mps/cuda selection. `mlx-files.json`, `mlx-8bit-files.json` and
`qwen3-files.json` own exact model revisions, package/wheel hashes and compatible versions.
`ppaso.py` uses pinned ONNX CPU only, with `ppaso-files.json` owning the model/runtime file and
wheel metadata. Do not carry 8bit weight hashes to 5bit or confuse CustomVoice with Base.

Use `${XDG_CACHE_HOME:-~/.cache}/tigerkit/tts/mlx/`, `tts/qwen3/` or `tts/ppaso/`, with a dedicated
venv, installation cache and `snapshots/<revision>`. Select compatible wheels from the manifest,
verify SHA256 before installing into the approved venv and retain dependency/lexicon notices.
Qwen5bit's two weights total about 1.76GB; ppaso's eight ONNX/external-data files about 38.50MB.
These are model-file sizes, not full install or memory figures. The model card's conversion-time
mlx-audio version is not proof of compatibility with the current pinned runtime.

## Installation footprint and dependency scope

Before setup, distinguish model bytes, compressed wheel/download bytes, expanded venv/runtime,
retained installation cache and peak temporary/headroom needs. Model size alone is never the
installation estimate. Select wheels for the actual OS, architecture and Python version; sum their
metadata sizes and include transitive dependencies plus expanded files in the estimate. State the
basis and uncertainty, not an invented exact total. If metadata/sizes are unavailable, label that
part unknown and use a comparable environment observation rather than the model-only number.
Do not download/install merely to estimate without the corresponding authority.

A supplied installation observation (2026-10-29, macOS arm64, Python 3.12, ppaso ONNX dedicated
venv plus model) was about 406MB, versus about 38.50MB of model files. It is a user-reported
measurement, not a native measurement performed by this skill or a cross-platform guarantee.
For a comparable setup, use roughly 0.4GB as the observed installed-footprint reference and add
separate wheel-cache/temporary headroom; do not advertise a 38.50MB total installation. Other
engines need their selected platform's own wheel/dependency estimate; do not reuse ppaso's total.
After approved installation, measure venv/model/cache separately on that host and report actual
bytes and environment, comparing them with the plan instead of silently changing its meaning.

The current `ppaso-files.json` fixes versions/hashes for five core runtime packages, not a complete
transitive lock. Installation plans must explicitly disclose `하위 의존성은 해시 고정이 없습니다`.
Resolve/list transitive versions and their wheel sources in the approved plan; do not claim
`--require-hashes` completeness or deterministic full-environment reproduction. Preserve all
existing core/model pins; never invent unverified transitive hashes to silence this disclosure.

After approved installation/download, use the selected venv Python:

```bash
python -B scripts/qwen3.py --engine mlx --quantization 5 --download --verify
python -B scripts/qwen3.py --engine mlx --quantization 8 --verify
python -B scripts/qwen3.py --engine pytorch --verify
python -B scripts/ppaso.py --download --verify
```

Resolve paths from this package, not the caller's working directory. `--model-dir` accepts an
explicit regular snapshot. `--download` first copies matching local HF snapshot bytes to regular
owned files and hashes them; it preserves cache symlinks/originals, partial/mismatched files and
other runs. Without that flag verification/synthesis never download. No automatic inference
follows from download. Verify the exact file set and all hashes before importing/loading model
code. Reject extra files, symlinks or unsafe paths. Configure owned runtime caches and offline
model loading before third-party imports. ppaso imports only hash-verified code under its snapshot;
it does not search a parent runtime or honor an external lexicon override.

Both models declare Apache-2.0. Preserve their model/license/readme and relevant G2P/lexicon
attributions; the manifests exclude ppaso sample avatars/VRM, RKNN, Vocos and lipsync assets.
Core ppaso needs NumPy, soundfile, python-mecab-ko with its pinned dictionary and onnxruntime; use the pinned manifest, not
upstream's unbounded requirements. Do not bundle weights in TigerKit Git history.

`--verify` checks module availability, actual pinned versions and snapshot hashes, not native
synthesis quality. Report actual/expected mismatches and a venv restoration command without
weakening the pin. A new runtime/model needs representative and longest planned input/decode
smoke before accepting it; unexecuted synthesis or listening stays explicit.
