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

Produce the selected MP4 or GIF from observed software states or explicitly labeled explanatory
cards. Existing-video editing and unrelated filmmaking are outside this skill. A movie communicates
a flow; it does not establish application correctness, latency, performance or reader understanding.

## Plan and collect

Resolve the audience, claim, selected format and available scene sources. Prefer stills when
motion itself is not the claim. A short flow around ten seconds often fits GIF; longer explanation
fits MP4. Reuse supplied material and approved choices without another routine question.

List each scene's source, caption, optional narration and hold or observed timestamp. Label rendered
cards in the picture/caption; never reenact unavailable software behavior or present a diagram as a
capture. Keep claims, source versions and unverified intervals explicit. For real browser states,
invoke `tk-browser-verify` with `phase: media-capture` for a demo or explanation without acceptance
criteria; an explicitly requested acceptance check retains its verification contract and optional
motion-evidence supplement. For native windows invoke `tk-app-verify`. Those owners retain provider,
authentication, test data, actual input/capture and resource lifecycle. Return to this skill with
ordered, publication-safe frame paths and provenance. Do not import a sibling skill's script path.
If that owner is unavailable, report the missing capture; do not invent a replacement.

Create cards with an already available renderer, retaining their authored source. HTML cards may
use an already approved headless rendering boundary; installed plotting/rendering tools are also
eligible. No dependency installation or user-profile attachment follows from choosing video.

## Assemble and inspect

Read [assembly](references/assembly.md) for the scene/capture manifest, owned paths and command.
Use `explainer` holds for presentation and preserve actual timestamps in `evidence` mode. Keep
assertion screenshots unchanged and independent from the movie. Use H.264 MP4 at the capture's
frame rate capped at 30fps, with optional mono 48kbps AAC; GIF and explainer stills default to
10fps. Use the assembler's rate selection/override contract. Follow prerequisite recovery for unavailable tools.
If hard-caption support is missing after installed-tool discovery, present the `tk-wizard`
installation-guidance question before returning the blocked result. Do not implement a frame-compositing workaround.

When narration is explicitly selected, read [narration](references/narration.md). Its isolated
engine is removable: assembly accepts ordinary audio and requires no TTS imports. Use authored
pronunciation corrections; do not add ASR or another automatic download.

Run the finished-media checks and inspect the generated contact sheet plus representative decoded
frames, including the initial/final state and every material caption or scene transition. Return
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
transients after accepted outputs decode. Release capture resources through their owning verifier.

Generation authorizes no publication. Hand selected attachments to `tk-pr-media` only when upload
is separately authorized. This skill changes no application source, Git state, global settings,
credentials. It creates only the requested movie, scene sources and run-owned evidence, plus the
dedicated narration cache only under the installation approval described in the narration reference.

Design sources and deliberate omissions are recorded in [sources](references/sources.md).

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

For a reusable incident, retain minimal non-secret evidence and suggest `tk-retro`.
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
