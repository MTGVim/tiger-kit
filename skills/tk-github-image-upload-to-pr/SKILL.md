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
