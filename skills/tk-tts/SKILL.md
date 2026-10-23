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

Own script-to-WAV synthesis, pinned models/runtime, approved cache reuse and audio validation.
`tk-video` owns scenes/encoding; `tk-course` owns curriculum/playback. Return ordinary audio and
measured duration; do not import or modify sibling packages. Creation grants no publication.

Run `scripts/list_options.py` for supported local routes without importing engines. Compare the
actual device/dependencies/cache before proposing options: Qwen3 0.6B CustomVoice MLX 5bit is the
Apple Silicon recommendation, ppaso ONNX CPU the lightweight Korean option; retain explicit
Qwen MLX 8bit and official PyTorch. Discovery is not runtime/model readiness or a quality ranking.
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

Report unavailable prerequisites with safe module or actual/expected version details and the
approved recovery route. Preserve original audio/cache bytes and clean only proven run-owned
transients. Return concise paths and actual validation/remaining listening limits. Existing
explicit narration choices need no second question; a voice preference alone does not select TTS.

For source provenance and deliberate omissions, see [sources](references/sources.md).

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Reuse identical content still in this context; hash-check uncertain copies and reread changed/lost content. Always repeat fresh safety checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:questions -->
## User Questions

Investigate facts; reuse authorization. For user-owned decisions read
[question rounds](references/questions.md); otherwise proceed.
Plain chat, even one approval: standalone `---`, then
`❓ **Q<n> · <title>**: <question>` and `➡️ <recommendation>` per item.
Ask only settled-prerequisite questions; separate approval.
Questions come last; put status, risks and plans before them.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->
