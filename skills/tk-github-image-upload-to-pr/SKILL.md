---
name: tk-github-image-upload-to-pr
description: "[user/auto] Upload local evidence images into an existing GitHub PR body or explicitly requested comment through the reviewed gh-attach extension or an authenticated CDP browser. Use on explicit selection, a clear local-image insertion request, or an exact evidence_required handoff from active tk-pr-open; do not apply to generic PR, screenshot, or GitHub requests."
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub image upload to PR

Start only when user selects `/tk-github-image-upload-to-pr`,
`$tk-github-image-upload-to-pr`, explicitly requests local image evidence in
an existing GitHub PR, or active `tk-pr-open` sends an exact handoff with
`evidence_required: true`. Parent handoff is the only automatic trigger. Do
not activate for screenshot capture, generic GitHub help, PR creation, PR
review, or issue triage.

## Scope

Own one bounded upload: local image validation and staging, repository-scoped
GitHub attachment upload, minimal PR body or selected comment update, and
source/render verification. Default target: PR body.

From `tk-pr-open`, accept only a producer evidence handoff from
`tk-browser-verify` or `tk-prototype` with `evidence_required: true`. Missing
or invalid required evidence blocks the evidence handoff, not an already
created `tk-pr-open` PR.

Use [references/upload-workflow.md](references/upload-workflow.md) for the
operational contract. Use `tk-browser-verify` for browser-controlled runtime
verification.

## Workflow

1. Resolve executing repository from `origin`, current PR, and regular local
   image file(s) or valid producer evidence handoff. Read existing PR body.
2. Reuse an existing `## 스크린샷` heading; otherwise insert before the AI
   footer or append. Preserve unrelated body content.
3. Probe `gh attach --help`, authenticated `gh` access, and target
   repository write capability; repository visibility is not a routing signal.
4. If available, use the reviewed extension without `--comment` and capture
   only its generated Markdown. If absent, ask before any browser mutation:
   recommend the exact pinned `MTGVim/gh-attach` install or offer CDP.
5. When CDP is selected or target write capability is unavailable, stage
   meaningful run-owned copies outside `/tmp`, protect any existing composer
   draft, poll upload placeholders, and clear only run-owned composer content.
6. Update only the requested body or comment through GitHub API or equivalent.
   Verify source Markdown, rendered HTML/page evidence, every asset link, and
   the upload ref before `Pass`.
7. Remove only owned staging files on every exit path. Never silently switch
   routes after an upload attempt may have created remote state.

## Producer evidence handoff

With `evidence_required: true`, require:

- `producer` exactly `tk-browser-verify` or `tk-prototype`;
- each artifact: non-empty image, absolute path, run-owned evidence directory;
- each image inspected, retaining criterion or caption;
- `tk-browser-verify` artifacts from a `Pass` result;
- `tk-prototype` artifacts include tested screenshot path and actual image
  inspection, without claiming an official runtime verdict.

Reject arbitrary screenshots, missing paths, `Unverifiable` results, and
artifacts not tied to current run. Return `Blocked` before upload when required
evidence is absent or invalid.

## Do not

- Do not create a PR, merge, change reviewers, publish a release, or insert a comment unless the user explicitly selected that comment target.
- Do not install, update, or substitute a GitHub CLI extension without explicit user approval; the reviewed command is `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`.
- Do not bypass `tk-browser-verify`, or use Orca or screen control as an automatic browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or another submit button.
- Do not route by public/private visibility or claim success from a placeholder, Markdown presence, fixed delay, or unrendered API response.
- Do not log or return signed URL JWTs or query strings.

## Failure handling

Return `Blocked` for a draft, rejected installation without a selected CDP
route, or another missing user-owned decision; `Unverifiable` when neither
route has authentication or render evidence; and `Fail` for upload, remote
ref verification, or cleanup errors. State whether the selected body/comment
changed and whether an upload ref may remain. After a started `gh attach`
failure, do not silently retry through CDP.

From `tk-pr-open`, preserve separate PR operation result; return evidence state
as `uploaded` or `blocked`. Parent cannot claim full completion while required
evidence remains blocked.

## Result

Begin terminal response with `## GitHub image upload`. Include `## Uploaded`,
`## Verification`, and `## Cleanup` as applicable. End owning result section
with exactly one `Status: Pass|Fail|Blocked|Unverifiable` line. Expose asset URL
only when safe; redact signed parameters.

### 🔴 HARD GATE · terminal user summary

Terminal response is the only active result surface. Do not emit a receipt
heading, `Outcome:`, caller-return instruction, or bottom provenance block.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language, else current user message language. Preserve
headings, statuses, IDs, commands, paths, code, and exact source literals;
translate only free-form explanatory prose.

## User decision questions

Before browser mutation, ask one self-contained question when repository, PR,
insertion location, comment target, private runtime identity, or extension
installation is unresolved. Ask the missing-extension question before browser
identity or mutation gates; recommend the reviewed pinned fork and show CDP as
the alternative with its dedicated-profile/login cost. Show only
decision-relevant evidence and one `(Recommended)` label. Render question and
options directly in chat; do not call structured question or input tools.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 github-image-upload-to-pr · 응답 필요` only for a user decision/approval, `⏳ github-image-upload-to-pr · 대기` only when external waiting is next, and `🚗 github-image-upload-to-pr · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > github-image-upload-to-pr`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.

## Next-action handoff

Whenever this skill hands control back to the user for a question, `Pending`,
`Blocked`, `Unverifiable`, bounded wait, or an actionable terminal result, end
the visible handoff with exactly one `Next:` line naming the recommended action
or next skill and its condition. Before rendering any user-facing `Question` or
publication/approval plan, emit exactly one nonterminal hand-raise checkpoint
in this skill's `🙋 ... · 응답 필요` form; a parent may own the display in
orchestration. Do not use only a `🤹` or `🚗` boundary marker for a user
decision. Mark the single recommended option with `👍 Recommendation:`.
Do not leave only a child receipt or generic “continue”; omit `Next:` only for
a terminal success with no follow-up action.
