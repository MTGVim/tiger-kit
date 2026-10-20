# Optional Qwen3 narration

Read only when narration is explicitly selected. The removable front door is
`scripts/narration/qwen3.py`; `mlx_backend.py` is its optional Apple backend. No assembler or verifier
imports either. Removing this directory, this reference/SKILL pointer and the source-only
`scripts/test_qwen3_narration.py` leaves captioned GIF/MP4 usable; retain no-narration regressions.

## Engine, installation and reuse

Native Apple Silicon defaults to `mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-8bit` with
`mlx-audio`; other environments retain official `qwen-tts` with
`Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`. `--engine auto | mlx | pytorch` selects the route explicitly.
Use the versions, revisions, wheel SHA256 and exact snapshot file hashes in `mlx-files.json` or
`qwen3-files.json`; inspect that selected manifest rather than substituting a current package/tag.
The MLX manifest also pins its compatible `mlx` version. The converted model retains Apache-2.0;
retain the model README and package license/attribution. No fork, clone-voice model, Supertonic,
ASR or resident server belongs to this path. A mirror must match the same pinned bytes; do not
publish mirrors or put weights in TigerKit Git history.

Inspect available Python/device/dependencies first. Propose the selected dedicated venv, pinned
wheel/dependencies, model download size and cache location before first installation; reuse
matching user approval. No global pip or automatic installation follows from selecting video.
Use `${XDG_CACHE_HOME:-~/.cache}/tigerkit/tts/mlx/` on Apple Silicon or `tts/qwen3/` for PyTorch,
with `venv`, installation caches and `snapshots/<revision>`. Verify the selected wheel SHA256
before installing it into that venv. Reuse verified disk snapshots offline on later runs; preserve
another run's resources and partial/mismatched files rather than deleting the shared cache.

After download approval, use the selected venv Python with `qwen3.py --download --verify`, adding
`--engine` or `--model-dir` when explicitly selected. Without `--download`, verification and
synthesis do not download. Verify exact nonsymlink snapshot files before inference and pass the
absolute snapshot path, never a repository ID, to model/tokenizer loaders. The adapter sets offline
mode and redirects XDG/HF/Torch/Numba runtime caches into the selected engine's `runtime-cache`.
It compares top-level `~/.cache` and `~/Library/Caches` names before/after and reports new entries
outside the owned cache on success or CLI failure, plus inaccessible scans. This is a limited
inventory, not ownership proof or a recursive audit. Attribute unexpected entries to the run
before cleaning only those exact paths; creation time alone does not prove ownership.

Launch synthesis in a fresh owned process with a bounded deadline and stall check established
before launch. Report completion, error or real stagnation, not every sentence/progress line.
Stop only that process when its limit expires and retain a `timeout` result. For a new runtime or
benchmark variant, finish downloads and pass one representative sentence/decode smoke before
full sequential measurement; retry smoke after a prerequisite failure and exclude it from timing.
No global watcher, benchmark driver or parallel measurement is introduced by this skill.

Report `peak_footprint_bytes` as the primary Mac process-memory figure, `peak_rss_bytes` separately,
and `peak_mlx_active_bytes` as the narrower allocator metric. Kernel peak footprint is read for
the actual synthesis process; if unavailable, retain null and a limitation rather than relabeling
RSS or GPU allocation. Return MLX `cache_limit: 0` and `sentence_count`. Concurrent runs share disk
but load separate model memory. Sentence batching has no verified 7GB upper bound.

## Synthesize and inspect

Write pronunciation-corrected Korean text to run-owned UTF-8 files, one complete sentence per
line. Generate sentences sequentially, trim each measured onset and join accepted audio; do not
send a full long paragraph in one model request or infer a fixed memory ceiling from sentence length. Use
`qwen3.py --text-file <file> --output <new.wav>`; `--speaker serena` is the default and
`--speaker sohee` is the only alternative. The 0.6B model ignores `instruct`; do not offer style
instructions or silently upgrade to 1.7B. The MLX backend uses Metal GPU with `mx.set_cache_limit(0)` before loading/generation and clears
released allocations between sentences. PyTorch `--device auto` selects an available CUDA/MPS/CPU
device; use `--engine pytorch --device <device>` for an explicit PyTorch route. Report failures
without switching engines or silently trying MLX CPU.

Use the parent's resolved `evidenceMedia.voice` when supplied. Otherwise resolve `voice` per field:
current explicit request > `.tigerkit/repository.json` > user
`${XDG_CONFIG_HOME:-~/.config}/tigerkit/settings.json` > team `tigerkit.config.json` > `serena`.
Reject a malformed media preference and use safe defaults without rewriting its file. Pass the
resolved voice explicitly to the adapter; reading a voice default never selects narration itself.

Keep original UI literals in captions/evidence while spelling numbers and foreign terms for speech
in the authored script. Trim measured leading silence before measuring/placing the audio; the
adapter uses short-window energy with a small onset margin and rejects invalid/silent output.
Decode, finite samples and non-silence do not prove pronunciation. Return `human_action: listen`
with the actual sample paths and the proper names, numbers and technical terms to check; retain
meaning, pronunciation and clipped-ending review as pending until the user listens. Do not add
ASR, Whisper or another automatic download. Narrate observed outcomes only as observed, and label
rendered explanation scenes truthfully.

## Fit narration to scenes

For `explainer`, attach frame `audio_path`; measured speech determines presentation holds.
For `evidence`, retain actual timestamps. When an authorized non-mutating scenario is too short,
synthesize each scene first and measure the trimmed WAV. Give the capture owner minimum scene
holds of measured duration plus a small pause; recapture the same scenario and receive its actual
scene starts, final end and final-state facts. Mark deliberate narration-paced waits explicitly;
they are not application latency evidence. Do not stretch old captures or rerun mutating flows.
If safe recapture is unavailable, keep captions and disclose omitted/undelivered narration; do not
silently claim that an explicitly selected voice was delivered.

Pass `scenes: [{start_ms, audio_path}]` in the evidence manifest, using observed scene boundaries,
or an already prepared whole track with `--audio`. The assembler places scene WAVs and silence
without shell-authored filter graphs; clips cannot overlap the next scene or movie end. Never mix
scene audio with a full track, truncate speech or guess duration from character count.
