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

Own a reusable curriculum and self-contained HTML learning course. Reuse the audience, sources,
learning goal and settled choices; ask only material unknowns. tk-teach owns adaptive tutoring,
tk-explain a single explanation, tk-tts file synthesis and tk-video movie assembly. Creation
alone grants no commit, push or publication.

## Six production steps

1. **Set the outcome.** State what the learner will explain, judge or do and what they must already
   know. Research current primary sources, account for supplied materials in sources.md and map
   taught outcomes, prerequisites, worked cases and reasoned transfer checks in curriculum.md.
   Read [readiness](references/readiness.md) only for a material untaught dependency. Never infer
   mastery from playback, quiz scores or manual completion.
2. **Design the explanation.** Read [explanation design](references/lesson-plot.md). Follow a
   supported case through observation, mechanism and consequence, reusing its entities across
   scenes. Choose slides for staged explanation and video for motion or actual input that matters.
   Keep a supplied multi-course plan verbatim at the collection root before authoring its first
   part; read [plans and revisions](references/incremental.md) for a program or existing artifacts.
3. **Plan the scenes.** Record each scene's point, visible evidence, viewing order and connection
   to its neighbors in curriculum.md. Choose representations from that need, before choosing
   components. Read [visual grammar](references/visual-grammar.md) for figures, [chart design](references/chart-design.md)
   for numeric evidence and [slide components](references/slide-components.md) for the selected
   renderer. Inspect requested real screenshots and their reuse scope; text cards or generated
   imitation screens cannot replace them. Missing essential evidence leaves that outcome incomplete.
4. **Build the visuals.** Render a complete fixed 16:9 frame using supported components. Show
   relationships with diagrams, order with timelines, execution with code/output, quantities with
   charts and genuine lists with cards. Preserve image ratios and stable entities between states.
   Split by reasoning/state when needed; never grow a slide into a scrolling document or shrink
   essential detail to fit. Renderer limits are layout constraints, not the teaching outline.
5. **Write and refine the narration.** Read [clear writing](references/clear-writing.md). Reconstruct
   meaning first, then refine expression; reread the full explanation against the visible evidence.
   Explain why the case behaves as shown, rather than reading labels. Then derive sentence/phrase
   captions and cues without losing explanatory steps. Recommend Web Speech API for quickest HTML
   production; preserve selected file audio or no narration. Read [media](references/media.md)
   for the chosen route. File synthesis starts only after the script is corrected. For video,
   hand tk-video the accepted script and observed start state, action/change, deciding visual and
   explanation per scene; tk-video assembles this plan rather than inventing the teaching sequence.
6. **Pilot, review and expand.** Finish one representative explanation with actual visuals and its
   entire script before scaling. Review missing premises, factual support, language and agreement
   between slides, narration and answers; revise its source and carry the accepted case/style into
   later scenes. Greetings, covers, maps and summaries are optional teaching choices, not quotas.
   Delegate bounded independent work only when it lowers total cost without weakening this review;
   pass the real references and decisions, and integrate continuity yourself. Add no routine approval
   checkpoint when the creator already authorized production.

## Build and delivery

Read [authoring](references/authoring.md) before writing course.json and building. Keep authored
content separate from the renderer. Preserve stable IDs, revisions, source accounting and unknown
learner records. Default to ignored .tigerkit/courses/ and settle the shared dist root once, reusing
existing paths. Build with scripts/build_course.py --input <topic>/course.json --output <topic>/build
--dist <courses>/dist. Existing targets use reviewed staging and --previous under incremental editing.
Retain third-party notices and keep setup text, private plans and sharing controls out of learning UI.

Run content review and technical verification separately. A successful build or matching objective
ID is not proof of a comprehensible explanation. Use tk-browser-verify for actual full-frame
readability, caption coverage, cue/seek states, controls, themes, transcript/navigation scrolling,
reclaimed media space on transcript closure and native/fallback fullscreen. Read media for player
acceptance and applicable file/audio checks. Browser voice simulation is not listening evidence;
report unavailable voices and pending pronunciation review. A finished movie retains its own clock
and audio, with no live TTS layered over it.

Return the course and automatically refreshed catalog links, actual verification and material
limits. One course is <dist>/<topic>/index.html; several share the dist folder or build_catalog.py
--dist <dist> --zip output. Do not launch the user's browser. For provenance see [sources](references/sources.md).

<!-- tigerkit:narration-choice -->
## Narration Choice

Before spoken-slide production, offer Web Speech API (recommended for quickest HTML creation),
local generated file audio, supplied audio or no narration. Reuse an answered parent/user choice;
a recommendation is not consent. Browser speech needs no tk-tts setup or file synthesis interview.
Only selected file generation loads tk-tts options/readiness. A narrated movie needs supplied or
synthesized audio files; explain that requirement and resolve only the changed choice. A browser
voice preference does not grant file synthesis, installation, downloads or publication. Playback
mute, unavailable voices and learner fallback remain separate from the creator's production choice.
<!-- /tigerkit:narration-choice -->

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

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
