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
- [Supertonic 3 archived model](https://huggingface.co/supertone-oss-archive/supertonic-3/tree/aafc6e32416a594460b32413efc49d7fe4ce6d46)
  and [official Python helper/example](https://github.com/supertone-oss-archive/supertonic/tree/1e9799e964ea4c0dad7cde993b65c3c813a7b373/py):
  keep CPUExecutionProvider, Korean/F1, native chunking, eight steps and speed 1.05. Adapt pinned
  offline loading and crop each decoded chunk before concatenation. Inspect helper, example,
  requirements, model card and both licenses at these revisions; model/runtime SHA256 values
  and platform wheel metadata live in `supertonic3-files.json`. Keep OpenRAIL-M Attachment A(e)
  disclosure as user guidance and receipt fields, not a downstream labeling claim. The code
  upstream is archived with development/support ended. Omit SDK/server, auto-download, cloning,
  other languages/presets and video validators. Source inspection and adapter tests do not prove
  acoustic quality; report native smoke and human listening separately.
- The supplied 2026-10-21/22 user experiment chose Qwen5bit and ppaso after one listener and one
  sample per sentence. This informs support policy, not a universal quality ranking. Its actual
  model revisions were absent; do not label these latest source pins as benchmark-tested pins.
- [NeMo Korean cardinal and counter normalization](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/taggers/cardinal.py#L277-L374)
  and its [cardinal fixtures](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/tests/nemo_text_processing/ko/data_text_normalization/test_cases_cardinal.txt):
  adapt context-based quantity/digit/counter distinctions to authored spoken-script preparation.
  Keep source literals and raw benchmark inputs; do not copy its fixed zero/separator rules.
- NeMo at the same revision, [measure implementation](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/taggers/measure.py)
  and [measure fixtures](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/tests/nemo_text_processing/ko/data_text_normalization/test_cases_measure.txt):
  adapt separate numeric/unit interpretation. Its [unit lexicon](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/data/measure/unit.tsv)
  lacks `ms` and `GB`; do not infer support for those examples. Omit external normalizers,
  WFST runtime, Cloud calls, SSML and global replacement rules. Source/comments/fixtures were
  read at the verified 2026-10-23 main revision; upstream tests and acoustic A/B were not run.

Keep longest-input/equal-cache smoke and actual/expected runtime diagnostics. Omit automatic ASR,
model/engine fallback, untested short-utterance retry rules and a new blind-gallery skill.
Actual model synthesis/listening on target hardware must be reported separately from mocked
adapter tests, source/pin inspection and missing-runtime diagnostics.


## Setup transparency (2026-10-29)

Inspected the current package-local `ppaso-files.json` core dependency/wheel hashes and
`list_options.py` discovery behavior at TigerKit `e672abcc0fedc8b91766266c8117a21496f02cbe`.
Keep the five core pins; disclose the absence of a complete transitive lock rather than inventing
hashes or claiming full reproducibility. Adapt the supplied macOS arm64/Python 3.12 observation
(about 406MB venv plus model) as a clearly attributed footprint reference; it is not a fresh native
installation measurement. Omit model/runtime upgrades, hidden engine exclusion and automatic
setup merely to obtain a size. Option discovery remains offline and imports no engine.
