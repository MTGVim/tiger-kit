---
name: tk-video
description: "[user/auto] 소프트웨어나 개념의 데모·튜토리얼·설명 MP4 또는 GIF 제작에 사용합니다. 검증 판정, 기존 영상 편집, 일반 영상 제작이나 PR 업로드에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<software/concept, audience, scenes or capture manifest>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Explain Through Video

Produce the selected MP4 or GIF from observed software states, labeled explanatory cards or
authored Manim renders. Arbitrary existing-video editing and unrelated filmmaking are outside this skill. A movie communicates
a flow; it does not establish application correctness, latency, performance or reader understanding.

## Plan and collect

Resolve the audience, claim, selected format and available scene sources. Prefer stills when
motion itself is not the claim. A short flow around ten seconds often fits GIF; longer explanation
fits MP4. Reuse supplied material and approved choices without another routine question.
For authored explainers, answer an opening question immediately with the main claim/reason and
necessary condition in both screen copy and narration, then demonstrate why with changing visuals.
Keep an explicitly selected discovery-led structure instead; do not infer improved learning from style alone.
When authored geometry or algorithm/state transitions carry the explanation, recommend Manim
over HTML-to-image slides; preserve explicitly selected stills, HTML and observed-UI routes.
Only when Manim is selected, read [Manim dependency and rendering](references/manim.md), verify
and load the external `manim-composer` and `manimce-best-practices` skills unchanged. Native
ManimCE and an existing Docker runtime are alternatives, never universal prerequisites. Keep
their continuous render as video, not extracted stills; slide theme and 10fps defaults do not apply.
Before production, read [media choices](references/media-preferences.md): resolve saved fields,
ask unresolved narration/presentation and the default-save offer in one ordinary-chat round,
and pass answered choices through parent/child phases. Reuse selections; save only explicitly
approved fields through that reference's atomic merge/readback contract. Give captions reading time and measured narration
at least 800ms of breathing room. For captures, plan each selected crop and highlight its region before zooming in.

List each scene's source, caption, optional narration and hold or observed timestamp. Label rendered
cards with a corner source tag in the audience's language and declare `source_in_picture: true`
in each tagged frame; otherwise retain a localized caption label. Never reenact unavailable
software behavior or present a diagram as a capture. Keep claims, source versions and unverified intervals explicit. For real browser states,
invoke `tk-browser-verify` with `phase: media-capture` for a demo or explanation without acceptance
criteria; an explicitly requested acceptance check retains its verification contract and optional
motion-evidence supplement. For native windows invoke `tk-app-verify`. Those owners retain provider,
authentication, test data, actual input/capture and resource lifecycle. Return to this skill with
ordered, publication-safe frame paths and provenance. Do not import a sibling skill's script path.
If that owner is unavailable, report the missing capture; do not invent a replacement.

For authored cards, read [slide authoring](references/slide-authoring.md) before rendering;
retain the full scene-copy list and author-check result in inspection evidence. Use the resolved
slide theme (light fallback), in-slide emphasis unless another treatment was selected, and keep
assembler zoom off by default. Create cards with an already available renderer, retaining their authored source. HTML cards may
use an already approved headless rendering boundary; installed plotting/rendering tools are also
eligible. No dependency installation or user-profile attachment follows from choosing video.

## Assemble and inspect

Read [assembly](references/assembly.md) for the scene/capture manifest, owned paths and command.
Use `explainer` holds for presentation and preserve actual timestamps in `evidence` mode. Keep
assertion screenshots unchanged and independent from the movie. Use H.264 MP4 at the capture's
frame rate capped at 30fps, with optional mono 48kbps AAC; GIF and explainer stills default to
10fps. Animation MP4 instead retains its measured source rate, dimensions and duration, including
rates above 30; existing embedded audio is retained. Its captions default to selectable tracks
and sidecars; burn them only on explicit selection. Hard captions alone do not select a letterbox or appended band: preserve the animation canvas with an in-frame overlay unless the user separately selects a band. Protect moving diagrams and labels across each caption interval; shorten/split captions or reauthor a safe region rather than silently adding padding. An explicitly selected `band` adds height; report it. MP4 defaults to CRF 18; use the assembler's quality/rate overrides and preserve source
resolution. Follow prerequisite recovery for unavailable tools.
If hard-caption support is missing after installed-tool discovery, present the `tk-wizard`
installation-guidance question before returning the blocked result. Do not implement a frame-compositing workaround.

For selected generated narration, invoke `tk-tts` through supported skill loading/handoff;
read [narration](references/narration.md) for measured audio-to-scene alignment. Reuse supplied
audio when selected. Assembly consumes ordinary WAV files and imports no TTS engine. Selecting
TTS requires actual accepted non-silent audio; missing synthesis is not a voiced silent preview.

Run the finished-media checks and inspect the generated contact sheet plus representative decoded
frames, including the initial/final state and every material caption or scene transition.
For narrated video also inspect interval samples (for example every two seconds) and beat
boundaries, including just before each beat ends. Review intervals with narration and prolonged
unchanged or irrelevant visuals; record sample count, candidate intervals and disposition in the
inspection receipt. The assembler's capped contact sheet alone may not provide this coverage. Return
`human_action: listen` with the names/numbers/terms to check and relevant sample paths for selected
narration; retain it as pending until the user confirms meaning, pronunciation and clipping.
A decode pass is not visual or pronunciation
inspection. Distinguish uninspected intervals and report real limitations. Repair a defective cut
and rerun affected checks; never edit the receipt to make the movie pass.

## Return

Return ready media with its absolute path, mode/timing, sources, caption/audio state, media checks,
inspection limits and publication selection. Report blocked or failed quality separately from
application verification. Missing hard-caption support retains the soft-caption fallback, not a
claim of completed burned captions. Preserve inputs and failure evidence; clean only known owned
transients only after the user confirms the selected result and its decode/inspection completes.
Until then preserve reusable frames/audio/manifests and report retained frame bytes.
Release capture resources through their owning verifier.

Generation authorizes no publication. Hand selected attachments to `tk-pr-media` only when upload
is separately authorized. This skill changes no application source, Git state or credentials; its only settings write
is the explicitly approved media-preference merge. It creates only the requested movie, scene sources and run-owned evidence, plus the
selected audio artifacts. `tk-tts` owns its separately approved installation and model cache.

Design sources and deliberate omissions are recorded in [sources](references/sources.md).

<!-- tigerkit:narration-choice -->
## Narration Choice

Ask the creator to choose TTS, supplied audio or no narration before any video or spoken-slide
production. Reuse an answered parent/user choice; video or a voice preference is not TTS consent.
Show current tk-tts model/voice/device/setup options before synthesis/assembly. Preserve no
narration; offer MP4 for GIF sound. Static HTML/text needs no unrelated voice interview.
Installation/download/publication require their own authority; playback mute/fallback are separate.
<!-- /tigerkit:narration-choice -->

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit or the eligible durable-root branch applies. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

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
