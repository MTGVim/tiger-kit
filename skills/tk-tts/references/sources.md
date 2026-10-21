# TTS Sources and Distillation

- TigerKit `68b14419cdef1ac9c2c93766c3926f0a192e2098`: extract existing Qwen CLI, pinning,
  MLX/PyTorch, cache/offline, decode and non-silence contracts without duplicating engines.
- [Qwen CustomVoice MLX 5bit](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-5bit/tree/ea57eb1094e142071162f79568581c9315dfd2e7):
  adapt as Apple Silicon recommendation. Small-file SHA256 computed from pinned bytes; large
  weight hashes from official LFS metadata. Retain explicit 8bit compatibility at
  `049ef77fe8816b536193c0c25f9a214d17921282` and official PyTorch pins.
- [ppaso](https://huggingface.co/akamotaco/ppaso-tts-v1/tree/53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9):
  adapt its ONNX CPU/core Korean synthesis only. Keep exact model/runtime/lexicon bytes and
  Apache/MIT/BSD notices. Omit sample avatars, optional graphics, RKNN, lipsync and server.
- The supplied 2026-10-21/22 user experiment chose Qwen5bit and ppaso after one listener and one
  sample per sentence. This informs support policy, not a universal quality ranking. Its actual
  model revisions were absent; do not label these latest source pins as benchmark-tested pins.

Keep longest-input/equal-cache smoke and actual/expected runtime diagnostics. Omit automatic ASR,
model/engine fallback, untested short-utterance retry rules and a new blind-gallery skill.
Actual model synthesis/listening on target hardware must be reported separately from mocked
adapter tests, source/pin inspection and missing-runtime diagnostics.
