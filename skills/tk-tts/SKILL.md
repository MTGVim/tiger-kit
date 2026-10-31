---
name: tk-tts
description: "[user/auto] 원고를 로컬 음원으로 생성하거나 지원 TTS 모델·목소리·설치 준비 상태를 확인할 때 사용합니다. 코스·영상 제작에서는 선택된 음성 합성을 맡습니다. 브라우저 발화, 영상 조립, 받아쓰기나 목소리 복제에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[script or options] [engine/model/voice] [output WAV]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Generate Local Narration

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

Own script-to-WAV synthesis, pinned models/runtime, approved cache reuse and audio validation.
`tk-video` owns scenes/encoding; the teaching caller owns lesson content. Return ordinary audio and
measured duration; do not import or modify sibling packages. Creation grants no publication.

Run `scripts/list_options.py` for supported local routes without importing engines. Compare the
actual device/dependencies/cache before proposing options: Qwen3 0.6B CustomVoice MLX 5bit is the
Apple Silicon recommendation, ppaso ONNX CPU the lightweight Korean option; retain explicit
Qwen MLX 8bit and official PyTorch. Discovery is not runtime/model readiness or a quality ranking.
Supertonic 3 ONNX CPU/F1 is an explicit alternative, not a new default. Its upstream is archived.
When selected, tell the user that AI-synthesis disclosure is required and return the receipt's
`disclosure_required` and `disclosure_notice`; do not claim the audio/video was automatically labeled.
Present every `list_options.py` route with its device/platform, voices and dependency/cache setup
status; past evaluations affect recommendations only, never which engines are shown. Reuse the
ordinary-chat question rounds and retain unsupported/uninstalled routes with their limits.
Read [installation and pins](references/installation.md) before verification, download or synthesis.
Reuse verified setup and matching approval. Resolve material engine/voice choices before work;
never silently switch engines after a failure or install into a global environment.

Read [synthesis and inspection](references/synthesis.md) for selected synthesis. Use authored UTF-8
pronunciation-corrected text, complete sentences, sequential requests and a new WAV path. Keep
captions/UI literals faithful separately. Run only the selected local adapter in a fresh owned
process with a bounded deadline/stall check. Decode and reject invalid/nonfinite/silent audio;
return measured duration, engine/model revision, sentence/cache/memory facts and
`human_action: listen`. Actual meaning, pronunciation, proper names/numbers and clipped endings
remain pending until heard. Non-silence is not intelligibility. Do not add ASR, voice cloning,
paid/cloud synthesis, a resident server or an automatic engine fallback.

For multi-clip narration, read [audio postprocessing](references/postprocessing.md) before delivery.
Normalize the batch into new files, preserve raw WAVs and return the measured treatment/limits.

Report unavailable prerequisites with safe module or actual/expected version details and the
approved recovery route. Preserve original audio/cache bytes and clean only proven run-owned
transients. Return concise paths and actual validation/remaining listening limits. Existing
explicit narration choices need no second question; a voice preference alone does not select TTS.

For source provenance and deliberate omissions, see [sources](references/sources.md).

## Artifact Paths

Before authorized artifact writes, checkout/transport/ignore setup or temporary-input consumption,
read [artifact paths](../tk-artifacts/references/artifact-paths.md). Use safe owned nonsymlink paths
and proven Git exclusion for repository scratch; failed checks stop that file branch. Preserve
explicit final destinations and owner-specific defaults. Prefilled input is not completed input.
Cleanup targets only recorded literal resolved absolute run-owned paths, never cwd-relative paths or globs.
