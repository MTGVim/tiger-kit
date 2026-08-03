---
name: tk-github-image-upload-to-pr
description: "[user/auto] Upload local evidence images into an existing GitHub PR body or explicitly requested comment through an authenticated CDP browser. Use on explicit selection, a clear local-image insertion request, or an exact evidence_required handoff from active tk-pr-open; do not apply to generic PR, screenshot, or GitHub requests."
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub image upload to PR

Start only when the user selects `/tk-github-image-upload-to-pr`,
`$tk-github-image-upload-to-pr`, explicitly asks to insert local image
evidence into an existing GitHub PR, or when active `tk-pr-open` sends an exact
handoff with `evidence_required: true`. The parent handoff is the only automatic
trigger. Do not activate for screenshot capture, generic GitHub help, PR
creation, PR review, or issue triage.

## Scope

This skill owns one bounded upload: local image staging, GitHub attachment
upload, a minimal PR body update, and render verification. It does not create
PRs, submit comments, merge, change reviewers, or publish releases. Comment
insertion is allowed only when the user explicitly requests it. The default
target is the PR body.

When called from `tk-pr-open`, accept only a producer evidence handoff from
`tk-browser-verify` or `tk-prototype` with `evidence_required: true`.
Missing or invalid required evidence blocks the evidence handoff but does not
undo a PR that `tk-pr-open` already created.

Use [references/upload-workflow.md](references/upload-workflow.md) for the
operational contract. Use `tk-browser-verify` for browser-controlled runtime
verification; do not bypass its browser boundary.

## Workflow

1. Resolve the executing repository from `origin`, the current PR, and one or
   more regular local image files or a valid producer evidence handoff. Read
   the existing PR body before editing.
2. Use an existing `## 스크린샷` heading when present; otherwise insert before
   the AI footer or append at the end. Preserve all unrelated body content.
3. Create meaningful run-owned copies inside the browser automation workspace,
   never in `/tmp` by default. Record pre-existing paths and clean only owned
   copies.
4. Connect to an authenticated existing Chrome CDP session first, then an
   authenticated persistent CDP/Playwright profile. Stop with actionable
   guidance when neither is available. Never use Orca or screen control as an
   automatic fallback.
5. In the visible GitHub composer, use `Attach files` or
   `Paste, drop, or click to add files`. Poll each placeholder until it
   becomes a `user-attachments` URL or equivalent image element; fixed sleep
   alone is not success evidence.
6. Detect a non-empty pre-existing draft before writing. Do not overwrite it.
   After collecting asset URLs, clear the temporary composer and confirm it is
   empty and not submittable. Never click comment, close-with-comment, or any
   submit button.
7. Update only the PR body through the GitHub API or equivalent, then verify
   the asset URLs in the body and on the rendered PR page. Treat GitHub's
   signed `private-user-images.githubusercontent.com` rewrite as normal.
8. Remove owned staging files on every exit path. Do not log or return signed
   URL JWTs or query strings.

## Producer evidence handoff

Require all of the following when `evidence_required: true`:

- `producer` is exactly `tk-browser-verify` or `tk-prototype`;
- each artifact is a non-empty image with an absolute path and run-owned
  evidence directory;
- each image was actually inspected, with its criterion or caption preserved;
- `tk-browser-verify` artifacts come from a `Pass` result;
- `tk-prototype` artifacts include the tested screenshot path and actual
  image inspection, without being presented as an official runtime verdict.

Reject arbitrary screenshots, missing paths, `Unverifiable` results, and
artifacts that cannot be tied to the current run. Return `Blocked` before
upload when required evidence is absent or invalid.

## Failure handling

Return `Blocked` for a draft or missing user-owned target decision,
`Unverifiable` for missing CDP, authentication, or render evidence, and
`Fail` for upload or cleanup errors. State whether the PR body was changed
and what the user must do next. Never claim an upload succeeded from a
placeholder, fixed delay, or API response alone.

When called from `tk-pr-open`, preserve the separate PR operation result and
return the evidence state as `uploaded` or `blocked`; the parent must not
claim full completion while required evidence remains blocked.

## Result

Begin the terminal response with `## GitHub image upload`. Include
`## Uploaded`, `## Verification`, and `## Cleanup` as applicable. End the
owning result section with exactly one `Status: Pass|Fail|Blocked|Unverifiable`
line. Expose an asset URL only when it is safe and redact signed parameters.

### 🔴 HARD GATE · terminal user summary

The terminal response is the only active result surface. Do not emit a receipt
heading, `Outcome:`, caller-return instruction, or bottom provenance block.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current user message's
language. Preserve headings, statuses, IDs, commands, paths, code, and exact
source literals; translate only free-form explanatory prose.

## User decision questions

Ask one self-contained question before browser mutation when the repository,
PR, insertion location, comment target, or private runtime identity is
ambiguous. Show only decision-relevant evidence and put one
`(Recommended)` label on the recommended option.
