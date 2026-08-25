---
name: tk-pr-open
description: "[user/auto] 검증된 현재 브랜치 `commit`으로 하나의 GitHub `pull request`를 열거나 업데이트하며, 원격 발행 전 정확한 현재 턴 승인을 요구합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Open a PR

Start when the intent to create or update one `PR` is explicit, such as `/tk-pr-open`, `$tk-pr-open`, selection through the host skill picker, or `현재 브랜치로 PR 열어줘`.

The input is an already implemented and verified current-branch `commit`.
If a prepared `.tigerkit/seed.md` exists, read the work `goal`, `acceptance`, and `browser evidence requirement`, but the `Seed` itself does not grant publication authority.

Do not repeat implementation, create a `worker`, or add product `commit`s.
When template selection or remote publication approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, present the same approval packet in plain chat; do not write remotely before exact current-turn approval.

## Current state

First, verify the following.

- Repository and authenticated GitHub account
- Current branch and `HEAD`
- Base branch
- Target `commit` and changed paths
- Whether a `PR` already exists for the same `head`, and its `observed draft | ready` state
- Unrelated dirty/staged paths
- Target repository's `PR template`
- Recent merged `PR` title samples and any established prefix, ticket-position, or release-label convention

If the exact current `commit` cannot be proven or unrelated changes are mixed in, do not broaden scope; return `Blocked`/`Unverifiable`.

## `PR template`

Before creating the `PR body`, check supported template locations on the default branch.

- Root
- `docs/`
- `.github/`
- `PULL_REQUEST_TEMPLATE/` under each location

If exactly one template applies, preserve its heading order, checklists, HTML comments, and required sections.
If multiple templates exist and there is no basis for choosing one, explain the candidates with one recommendation and ask the user to choose before publication approval.
If the template cannot be read, do not invent a body.

Derive the title convention from recent merged `PR` titles, not from template guidance alone. If the
merged history establishes a convention, follow it. If template title guidance conflicts with that
history, prefer the verified merged-history convention and surface the mismatch. If no convention is
observed, preserve the existing title behavior.

When the `PR body` or a QA table names a user-visible element, verify the exact rendered string from repository evidence before writing it. Do not copy a ticket paraphrase, code identifier, or enum value; quote the label verbatim. If no visible label exists, use the entry path ending in an exact visible title. If ticket, code, and screenshot disagree, preserve the verified source and tell the user about the mismatch; do not present an unverified server-supplied label as fact.

## Evidence

Determine whether `PR evidence` is needed from the prepared `Seed` or the currently verified work.

```text
required | optional | N/A | undecided
```

If a prepared `Seed` marks `tk-browser-verify` screenshot evidence as required for `browser-visible acceptance`, use only validly inspected evidence.
Approved `tk-prototype` evidence may also be used.

Do not upload actual secret-bearing screenshots or unverified captures.
If an image is required, pass the exact evidence path to `tk-github-image-upload-to-pr` after the `PR` exists.

## Publication plan

Maintain `.tigerkit/pr-open.md` as this skill's independent publication plan.
Record and reread the following exact information.

```text
Repository
PR operation: create | update
PR state: draft | ready
Base
Head ref + SHA
Push refspec
Title
Title convention basis: <merged-title evidence | none observed>
Body
Template source/compliance
PR evidence requirement/state
Evidence producer/path
Known exclusions
```

This artifact owns only the current `PR` publication plan, not the product work plan or `worker` state.
Create a new `PR` as `draft` only when the user explicitly requests `draft`; otherwise preserve the existing `ready` behavior.
For an existing same-`head` `PR`, preserve its fresh-read state unless a state change was requested.

Present the following naturally to the user instead of hiding information behind a file they must open.

- Summary of included changes
- Exact title/body or important template sections
- Title-convention evidence and any mismatch with template guidance
- Base/head
- Valid `PR state`
- Check/evidence state
- Exclusions/risks
- One publication recommendation

## 🔴 CHECKPOINT · 🛑 STOP · Publication boundary

Before any remote write, reread the plan and obtain one exact current-turn approval; do not treat the natural-language request `PR 열어줘` itself as publication approval. The approval must include a valid `PR state`.
STOP if the plan, approved `commit`, template/evidence state, or current repository state cannot be reverified.

## Publication

After approval, recheck the repository, account, branch, `HEAD`, base, existing `PR`, and template source.
Invalidate approval when an existing `PR`'s `actual state` materially differs from the approved `plan`.
Invalidate the approval if any material `drift` exists.

`push` only the exact approved `refspec`, and create or update only the specified `PR`.
For `create`, apply the approved `PR state`; for `update`, change state only when explicitly approved.
Do not `merge`, `close`, `tag`, or `release`.

After creating or updating the `PR`, reread the remote `PR` and verify its URL, `head SHA`, actual `draft | ready` state, template compliance, and evidence state.
If evidence is required, use the image uploader after the `PR` exists.
If the `PR` was created but the required evidence upload fails, preserve the actual remote state and report completion as `Blocked`.

## Completion

Show only results important to the user.

- `PR` URL
- Whether it was created or updated
- Current `head`
- Current `PR state`
- Verification/evidence result
- Remaining blockers

Do not show provenance dumps or product implementation receipts.
