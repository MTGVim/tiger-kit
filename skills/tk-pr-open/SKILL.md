---
name: tk-pr-open
description: "[user/auto] 검증된 현재 브랜치 `commit`을 하나의 GitHub `pull request` 또는 필요한 경우 reviewable `stacked PR`로 준비·발행하며, 원격 발행 전 정확한 현재 턴 승인을 요구합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Open PR publication

Start when the intent to create or update PR publication is explicit, such as `/tk-pr-open`, `$tk-pr-open`, selection through the host skill picker, `현재 브랜치로 PR 열어줘`, or a request to split the already-implemented current branch into reviewable stacked PRs.

The input is an already implemented and verified current-branch `commit`.
If a prepared `.tigerkit/seed.md` exists, read the work `goal`, `acceptance`, and `browser evidence requirement`, but the `Seed` itself does not grant publication authority.

Do not repeat implementation, create a `worker`, or add new product changes.
For an approved retrospective stack, this skill may create publication-only branches and commits that reconstruct the already-verified product tree exactly; those commits must not introduce, omit, or repair product behavior.
When template selection or remote publication approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, present the same approval packet in plain chat; do not write remotely before exact current-turn approval.

## Current state

First, verify the following.

- Repository and authenticated GitHub account
- Current branch and `HEAD`
- Base branch
- Target `commit`, tree, commit range, and changed paths
- Whether a `PR` already exists for the same `head`, and its `observed draft | ready` state
- Unrelated dirty/staged paths
- Target repository's `PR template`
- Recent merged `PR` title samples and any established prefix, ticket-position, or release-label convention

If the exact current `commit` cannot be proven or unrelated changes are mixed in, do not broaden scope; return `Blocked`/`Unverifiable`.

## Reviewability preflight

Before choosing one `PR`, inspect `base...HEAD` and choose the publication shape:

```text
single | stacked
```

Do not use a hard LOC threshold. A large diff is only a signal. Prefer `stacked` when the already-verified branch contains two or more independently reviewable concerns that form one coherent linear dependency story, especially when concerns have different reviewer audiences or clear foundation → implementation → integration boundaries.

Generated output, lockfiles, snapshots, vendored artifacts, or mechanical churn do not justify a stack by themselves. Keep one coherent change as `single` even when its raw diff is large.

Retrospective splitting is eligible only for a new publication before a same-`head` PR exists. Do not silently replace or restructure an existing PR with review comments or remote state. If a stack is a credible candidate or the user explicitly requests one, read [retrospective stack split](references/split-to-stack.md) before preparing the publication plan.

One invocation owns one coherent publication story: one PR or one linear stack. If unrelated work would require separate stacks or independent PRs, stop instead of hiding that scope expansion inside one publication.

## `PR template`

Before creating any `PR body`, check supported template locations on the default branch.

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

When a `PR body` or QA table names a user-visible element, verify the exact rendered string from repository evidence before writing it. Do not copy a ticket paraphrase, code identifier, or enum value; quote the label verbatim. If no visible label exists, use the entry path ending in an exact visible title. If ticket, code, and screenshot disagree, preserve the verified source and tell the user about the mismatch; do not present an unverified server-supplied label as fact.

When a title or body materially uses project-specific terminology, lazy-load
[domain context](references/domain-context.md), preserve canonical vocabulary, and never replace verified UI literals with glossary terms.

For a stack, apply the same title/template rules to every layer. Each layer body must explain only that layer's review surface and, when useful, its dependency on the preceding layer rather than duplicating the full feature summary into every PR.

## Evidence

Determine whether `PR evidence` is needed from the prepared `Seed` or the currently verified work.

```text
required | optional | N/A | undecided
```

If a prepared `Seed` marks `tk-browser-verify` screenshot evidence as required for `browser-visible acceptance`, use only validly inspected evidence.
Approved `tk-prototype` evidence may also be used.

Do not upload actual secret-bearing screenshots or unverified captures.
If an image is required, pass the exact evidence path to `tk-github-image-upload-to-pr` after the owning `PR` exists.
For a stack, attach evidence to the layer that owns the browser-visible acceptance; do not copy the same evidence to unrelated lower layers.

## Publication plan

Maintain `.tigerkit/pr-open.md` as this skill's independent publication plan.
Record and reread the following exact information.

```text
Repository
Publication shape: single | stacked
PR operation: create | update
PR state: draft | ready
Base
Original head ref + SHA + tree
Template source/compliance
PR evidence requirement/state
Evidence producer/path
Known exclusions

Single publication:
Head ref + SHA
Push refspec
Title
Title convention basis: <merged-title evidence | none observed>
Body

Stacked publication:
See the required plan fields in [retrospective stack split](references/split-to-stack.md).
```

This artifact owns only the current PR publication plan, not the product work plan or `worker` state.
Create new PRs as `draft` only when the user explicitly requests `draft`; otherwise preserve the existing `ready` behavior.
For an existing same-`head` PR, preserve its fresh-read state unless a state change was requested.

Present the following naturally to the user instead of hiding information behind a file they must open.

- Summary of included changes
- Recommended `single | stacked` publication shape and why
- Exact title/body or important template sections for every PR being created or updated
- Title-convention evidence and any mismatch with template guidance
- Base/head; for a stack also present the exact bottom-to-top branches and preserved original tree invariant
- Valid `PR state`
- Check/evidence state
- Exclusions/risks
- One publication recommendation

## 🔴 CHECKPOINT · 🛑 STOP · Publication boundary

Before any stack reconstruction or remote write, reread the plan and obtain one exact current-turn approval; do not treat the natural-language request `PR 열어줘` itself as publication approval. The approval must include a valid `PR state` and the exact `single | stacked` publication shape.

For `stacked`, the same approval also authorizes only the exact local publication-history reconstruction in the approved layer plan. It does not authorize product edits, rewriting the source branch, extra layers, or unrelated branch cleanup.
STOP if the plan, approved `commit`, template/evidence state, stack tooling provenance, or current repository state cannot be reverified.

## Publication

After approval, recheck the repository, account, source branch, `HEAD`, base, existing `PR`, template source, and any stack branch-name collisions.
Invalidate approval when an existing `PR`'s `actual state` materially differs from the approved `plan`.
Invalidate the approval if any material `drift` exists.

For `single`, push only the exact approved `refspec`, and create or update only the specified `PR`.
For `create`, apply the approved `PR state`; for `update`, change state only when explicitly approved.

For `stacked`, follow [retrospective stack split](references/split-to-stack.md). Preserve the source branch, reconstruct only the approved layers beside it, verify every layer and the final tree invariant, then submit the exact chain with verified `github/gh-stack`. Use the approved state for every newly created layer and edit auto-generated PR metadata to the exact approved title/body after submit.

Do not `merge`, `close`, `tag`, `release`, delete the preserved source branch, or clean up unrelated refs.

After creating or updating publication, reread the remote state. For `single`, verify its URL, `head SHA`, actual `draft | ready` state, template compliance, and evidence state. For `stacked`, use machine-readable stack state and reread every PR URL, head/base relation, state, exact title/body, template compliance, and evidence state.
If evidence is required, use the image uploader after the owning PR exists.
If any PR was created but required metadata/evidence publication fails, preserve the actual remote state and report completion as `Blocked` rather than hiding partial publication.

## Completion

Show only results important to the user.

- `PR` URL, or bottom-to-top stack PR URLs
- Whether publication was created or updated
- Current source `head`; for a stack, the preserved source branch and stack tip
- Current `PR state`
- Verification/evidence result
- For a stack, whether stack-tip tree equals the original tree
- Remaining blockers or partial remote state

Do not show provenance dumps or product implementation receipts.
