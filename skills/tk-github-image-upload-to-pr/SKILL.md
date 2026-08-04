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

Start only when user selects `/tk-github-image-upload-to-pr`,
`$tk-github-image-upload-to-pr`, explicitly requests local image evidence in
an existing GitHub PR, or active `tk-pr-open` sends an exact handoff with
`evidence_required: true`. Parent handoff is the only automatic trigger. Do
not activate for screenshot capture, generic GitHub help, PR creation, PR
review, or issue triage.

## Scope

Own one bounded upload: local image staging, GitHub attachment upload, minimal
PR body update, and render verification. Default target: PR body.

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
3. Create meaningful run-owned copies in the browser automation workspace,
   not `/tmp` by default. Record pre-existing paths; clean only owned copies.
4. Connect first to an authenticated existing Chrome CDP session, then an
   authenticated persistent CDP/Playwright profile. If neither exists, stop
   with actionable guidance.
5. In visible GitHub composer, use `Attach files` or
   `Paste, drop, or click to add files`. Poll each placeholder until a
   `user-attachments` URL or equivalent image element appears; fixed sleep is
   not success evidence.
6. Detect non-empty pre-existing draft before writing. After asset URL
   collection, clear temporary composer; confirm empty and not submittable.
7. Update only PR body via GitHub API or equivalent. Verify asset URLs in body
   and rendered PR page. GitHub's signed
   `private-user-images.githubusercontent.com` rewrite is normal.
8. Remove owned staging files on every exit path.

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
- Do not bypass `tk-browser-verify`, or use Orca or screen control as an automatic browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or another submit button.
- Do not claim success from a placeholder, fixed delay, or API response without rendered-page evidence.
- Do not log or return signed URL JWTs or query strings.

## Failure handling

Return `Blocked` for a draft or missing user-owned target decision,
`Unverifiable` for missing CDP, authentication, or render evidence, and `Fail`
for upload or cleanup errors. State whether PR body changed and required next
user action.

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

Use latest explicit user language, else current user message language. Preserve
headings, statuses, IDs, commands, paths, code, and exact source literals;
translate only free-form explanatory prose.

## User decision questions

Before browser mutation, ask one self-contained question when repository, PR,
insertion location, comment target, or private runtime identity is ambiguous.
Show only decision-relevant evidence and one `(Recommended)` label. Render
question and options directly in chat; do not call structured question or
input tools.
