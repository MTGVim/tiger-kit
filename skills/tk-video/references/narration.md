# Optional Qwen3 narration

Read only when narration is explicitly selected. Use `scripts/narration/qwen3.py` and
`qwen3-files.json`; no assembler or verifier imports this adapter. Removing them and this reference/
SKILL pointer leaves captioned GIF/MP4 and screenshot verification usable. Source-only regression
coverage lives in `scripts/test_qwen3_narration.py`; retain the no-narration assembly regression.

## Installation and reuse

Use `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` revision
`85e237c12c027371202489a0ec509ded67b5e4b5` with `qwen-tts==0.1.1`. The manifest pins every snapshot
file's SHA256 and the PyPI wheel hash. The official code is `QwenLM/Qwen3-TTS` (Apache-2.0);
PyPI 0.1.1 lists the older `Qwen/Qwen3-TTS` project URL. Do not fork or substitute an unreviewed
model/package. Preserve the model README and the wheel's license/attribution. A mirror must match
the same pinned hashes; do not publish a mirror or put weights in TigerKit Git history.

Inspect available Python/device/dependencies first. Propose the dedicated venv, exact pinned
wheel and dependencies, model download size and cache location before the first installation;
reuse matching user approval. No global pip or automatic installation follows from selecting video.
Use `${XDG_CACHE_HOME:-~/.cache}/tigerkit/tts/qwen3/` for `venv`, installation caches and
`snapshots/<revision>`. Download the pinned wheel to this cache, verify its SHA256 from the manifest,
then install it with its dependencies into that venv. Keep a single shared disk installation;
reuse a hash-verified snapshot offline on later runs without requesting reinstall approval.
Preserve another run's resources and partial/mismatched files; do not delete the shared cache.

After download approval, use the venv Python to run `qwen3.py --download --verify` (or supply
`--model-dir <snapshot>`). Without `--download`, verification and synthesis perform no download.
The adapter verifies the exact nonsymlink snapshot file set and all bytes before inference, sets
HF/Transformers offline mode and passes the absolute snapshot directory, never a repository ID,
to `from_pretrained`. This avoids nested tokenizer/processor Hub lookups. Start a fresh process
for synthesis and exit after the requested scene batch; no resident server. Concurrent processes
share disk files but each loads its own model memory. Do not promise one shared memory instance.

## Synthesize and inspect

Write pronunciation-corrected Korean text to run-owned UTF-8 files. Use
`qwen3.py --text-file <file> --output <new.wav>`; `--speaker serena` is the default and
`--speaker sohee` is the only alternative. The 0.6B model ignores `instruct`; do not offer style
instructions or silently upgrade to 1.7B. `--device auto` selects an available CUDA/MPS/CPU device;
report the actual device and failure rather than claiming an untested host works.

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
