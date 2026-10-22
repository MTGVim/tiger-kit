---
name: tk-course
description: "[user] 학습 목표·자료를 바탕으로 그 자체로 완결되는 HTML 학습 코스를 설계·제작하거나 기존 코스를 증분 수정합니다. 여러 주제의 기존 코스를 묶는 홈도 만듭니다. 개인 답변에 따라 이어가는 과외와 짧은 개념·상황 설명에는 사용하지 않습니다."
disable-model-invocation: true
argument-hint: "[topic or existing course] [learning goal] [output path]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit, tobyilee/course-builder
    relationship: adapted
    upstream-skill: course-builder
---

# Build a Complete Learning Course

Own a reusable curriculum and an offline course that a learner can finish without a continuing
conversation. `tk-teach` owns personal tutoring based on observed answers and misconceptions;
`tk-explain` owns one concept/system explanation. Creation grants no commit, push, PR or deployment.
Reuse the user's goal, corpus, audience and prior media decisions; ask only material unknowns.

## Design, then author

Research current primary sources and retain claim-level provenance. Account for every supplied
corpus member as used, partial, unavailable or omitted with reason; unavailable essential material
prevents a complete-corpus claim. Work backward from what a learner should explain, judge or do.
Map prerequisites, ordered lessons, worked examples, transfer practice and reasoned answers in
`curriculum.md`; keep `sources.md` and authored `course.json` beside the output. A completed course
must teach and assess its outcomes without relying on hidden chat context or a tutor's memory.
Never infer mastery from reading, playback, scores or a manually checked completion box.

Choose each lesson's medium from its learning goal. Prefer HTML/SVG slides plus local generated
narration for a staged explanation. Choose video when continuous movement, actual software input
or a physical procedure is itself needed. Do not duplicate every slide deck as a video. Resolve
TTS before production, including available engine/model/voice and readiness from `tk-tts`;
reuse answers rather than asking again. Read [media production](references/media.md) for selected
narration or video. Keep synthesis in `tk-tts` and assembly in `tk-video`; consume ordinary files,
never sibling Python imports or a shared dispatcher. Browser speech is an explicit final playback
fallback, not an exported-audio engine. Preserve an explicit no-narration choice.

Read [clear writing](references/clear-writing.md) for new narration/prose. Introduce what each
slide will explain, connect the visible entities to a worked case, then explain the result and
transition. A script must make sense with its slide; do not read disconnected labels. Read
[visual grammar](references/visual-grammar.md) when choosing a figure and [HTML output](references/html-output.md)
for the offline/theme/escaping contract. The course player is a media layout; document-navigation
rules apply only to document-like notes, not a second rail around the player.

## Build and verify

Read [authoring and build](references/authoring.md), use the packaged components and fixed player,
and run `scripts/build_course.py --input <topic>/course.json --output <topic>/build`.
Default the topic directory to ignored `.tigerkit/courses/<topic>/`; honor explicit destinations.
Keep authored files at the topic root and generated files in its `build/` directory; incremental
versions use a new output directory before reviewed replacement. Keep learning
content separate from renderer code. Do not copy demo content, brand marks, engine setup or
implementation notes into learning screens. Retain third-party notices and the AI footer.
The output includes a single-file `index.html` and independently readable lesson pages.
Keep the home copy on a theme-token surface distinct from the page canvas. The header shows
the course title once; entering a lesson adds its title, and returning home clears that context.

Inspect the actual reading/listening order, objective/prerequisite coverage, source support,
component overflow, captions, notes, question/answer separation and retry feedback. Verify audio
readiness, missing-file recovery, immediate first play, breathing gaps, reveal/seek state,
caption size/opacity (default 50%), light/dark/system themes, settings hit areas, default mute,
volume/rate and progress import/export. A finished video owns its audio, pauses and time axis;
never overlay live TTS. Manual progress belongs to the course and is not tutoring evidence.
Use `tk-browser-verify` for actual runtime checks; static/media doubles are not browser or listening
proof. Report unexecuted checks and pending human listening, never fabricate generated audio.
Return a concise link and actual verification limits. Do not launch the user's browser.
For a single course, mention that `build_catalog.py` can create a shared home once two courses exist.

For existing artifacts or several topics, read [incremental editing and collections](references/incremental.md)
before changing anything. Preserve unrelated courses, learner notes and unknown progress formats.

For attribution and deliberate omissions, see [sources](references/sources.md).

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

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Reuse identical content still in this context; hash-check uncertain copies and reread changed/lost content. Always repeat fresh safety checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:questions -->
## User Questions

Resolve researchable facts and reuse matching authorization before asking.
For an unmet prerequisite or material user-owned decision, read [question rounds and recovery](references/questions.md)
(reuse it if still in context). Ask only answerable decisions in its plain-chat format,
with approval separate. Otherwise continue without confirmation.
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
