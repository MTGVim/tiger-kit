---
name: tk-github-image-upload-to-pr
description: "[user/auto] 기존 GitHub PR body 또는 지정된 comment에 local evidence image를 업로드합니다. 명시적 이미지 요청이나 정확한 evidence handoff에만 사용합니다."
disable-model-invocation: false
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR Image Upload

Handle explicit local-image evidence requests for an existing GitHub PR or an exact
`tk-pr-open` handoff with `evidence_required: true`. Only the parent handoff is an
automatic trigger.
When route selection or pre-installation confirmation is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, ask for the same choice in plain chat and do not mutate before selection.

## Scope

Handle one bounded upload: validate and stage local images, upload
repository-scoped GitHub attachments, minimally update the PR body or selected
comment, and verify source/render output. The default target is the PR body.

For `tk-pr-open`, accept only producer evidence handoffs from `tk-browser-verify`
or `tk-prototype` with `evidence_required: true`. If required evidence is missing
or invalid, mark the evidence handoff `Blocked`; do not revert an already-created
`tk-pr-open` PR.

Use [references/gh-attach.md](references/gh-attach.md) to classify and run the
extension route. Read [references/cdp-fallback.md](references/cdp-fallback.md)
only after CDP is selected or the extension route cannot use target write
capability. Use `tk-browser-verify` for browser-controlled runtime verification.

## 🔴 CHECKPOINT · 🛑 STOP · Upload mutation boundary

Before any upload or PR body/comment update, reverify the explicitly selected target, valid local evidence or producer handoff, authenticated route, and requested write scope; stop as `Blocked` or `Unverifiable` when those preconditions cannot be established.

## Workflow

1. Confirm `origin`, the current PR, and the executing repository from regular
   local image file(s) or a valid producer evidence handoff. Read the existing PR
   body.
2. Reuse the existing `## 스크린샷` heading. If absent, insert it before the AI
   footer or append it at the end. Preserve unrelated body content.
3. Select and execute an eligible route using
   [gh-attach](references/gh-attach.md), or read
   [CDP fallback](references/cdp-fallback.md) only after CDP is selected.
   Repository visibility is not a routing signal, and a route that may have created
   remote state cannot silently fall back to the other route.
4. Update only the requested body or comment through the GitHub API or equivalent.
   Before `Pass`, verify the source Markdown, rendered HTML/page evidence, every
   asset link, and the upload ref.
5. Remove only owned staging files on every exit path.

## Execution Receipt · Single Evidence Record

Record every upload attempt in the single receipt below. It is not a separate lifecycle
output; it is the sole evidence record used for the `## GitHub image upload` result and
approval/verification decisions. Use `none` or `unavailable` for absent values; never guess.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: <source body/comment | rendered HTML/page | unavailable>
Changed: <body/comment changed | unchanged | unknown>
Cleanup: <owned staging path removed | failed | not applicable>
Status: Pass | Fail | Pending | Blocked | Unverifiable
```

## Producer Evidence Handoff

When `evidence_required: true`, require all of the following:

- `producer` is either `tk-browser-verify` or `tk-prototype`.
- Every artifact has a non-empty image, absolute path, and run-owned evidence directory.
- Every image is marked inspected and preserves its criterion or caption.
- A `tk-browser-verify` artifact comes from a `Pass` result.
- A `tk-prototype` artifact includes a tested screenshot path and actual image inspection,
  without claiming an official runtime verdict.

Reject arbitrary screenshots, missing paths, `Unverifiable` results, and artifacts not tied
to the current run. If required evidence is missing or invalid, return `Blocked` before upload.

## Prohibitions

- Do not create or merge a PR, change reviewers, publish a release, or insert a
  comment unless the user explicitly selected that comment target.
- Do not bypass `tk-browser-verify` or use Orca or screen control as an automatic
  browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or
  any other submit button.
- Do not choose a route based on public/private visibility or claim success from
  only a placeholder, Markdown presence, fixed delay, or unrendered API response.
- Do not log or return a signed URL JWT or query string.

## Failure Handling

Return `Pending` while waiting for an absent-extension or unreviewed-upstream
choice. Return `Blocked` for `unknown` provenance, a draft, or a rejected
installation without a selected CDP route. Return `Unverifiable` if neither route
has authentication or render evidence, and `Fail` for upload, remote ref
verification, or cleanup errors. State whether the selected body/comment changed
and whether an upload ref may remain.

For `tk-pr-open`, preserve the separate PR operation result and return the
evidence state as `uploaded` or `blocked`. While required evidence remains
blocked, the parent cannot claim full completion.

## Result

Start the terminal response with `## GitHub image upload`. Include `## Uploaded`,
`## Verification`, and `## Cleanup` when applicable. End the result-owning section with exactly
one `Status: Pass|Fail|Pending|Blocked|Unverifiable` line. Expose asset URLs only when safe and
redact signed parameters.
