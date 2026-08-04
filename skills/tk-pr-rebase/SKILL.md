---
name: tk-pr-rebase
description: "[user/auto] Rebase one open GitHub pull request onto the exact latest base, resolve conflicts, verify, and publish through approved or sweep-owned force-with-lease authority."
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Rebase pull request

Start only when the user selects `/tk-pr-rebase`, `$tk-pr-rebase`, or the host
skill picker. Do not activate from a generic rebase, update-branch, conflict,
review-response, or continuation request. A fresh exact-PR handoff from active
`tk-pr-sweep` is the only automatic entry.

This skill owns one PR's local rebase, `.tigerkit/pr-rebase.md` plan, bounded
force-with-lease publication, rebase-satisfied review replies and thread
resolution, rebase summary comment, and conditional human re-review request. It
does not implement unrelated review feedback, merge, close, tag, release, or
change repository rules.

## Modes

- **Normal:** explicit invocation authorizes the local rebase only; retain the
  publication question below.
- **Sweep CI:** `--ci` is valid only with an active `tk-pr-sweep` handoff that
  freezes the exact repository, PR, base/head refs and SHAs, and route attempt.
  That handoff is bounded publication authority without another question.

## Workflow

1. Resolve exactly one open PR, repository, authenticated identity, author,
   head repository/ref/SHA, base repository/ref/SHA, local branch, dirty paths,
   active Git operation, checks, reviews, comments, threads, and requested
   reviewers. Stop on ambiguity, identity/ownership mismatch, an unsafe fork
   destination, or an operation not created by this plan.
2. Fetch the exact remote head and latest base. Freeze `old_head`, `base_sha`,
   current review/thread state, and existing requested reviewers. Require a clean
   worktree, no unrelated staged paths, local `HEAD == old_head`, and remote PR
   head `== old_head` before starting.
3. Classify current findings. A thread may be closed by this skill only when its
   requested outcome is satisfied by updating the PR to the frozen base. Keep
   unrelated, deferred, superseded-uncertain, and unverified findings open.
4. Rebase the PR branch onto the exact `base_sha`. A normal explicit invocation
   authorizes this local rebase, not abort, reset, push, or comment publication.
   When conflicts occur, use `tk-merge-conflict` for each active conflict
   iteration and resume only after its operation, intent, index, marker, and
   verification gates pass. Never guess a resolution or auto-abort.
5. Verify that the rebase operation ended, the worktree and index are clean,
   `base_sha` is an ancestor of the new `HEAD`, intended commits and diff remain,
   and relevant tests/checks pass. If the branch already contains `base_sha` and
   no rewrite is needed, do not force-push.
6. Write `.tigerkit/pr-rebase.md` with the frozen refs and SHAs, verification,
   exact `--force-with-lease` expectation/refspec, every outbound reply, thread
   action, intentionally open finding, summary comment, prior human reviewers,
   normal and reviewer-mention fallback summary bodies, and exclusions. Every
   external reply/comment ends with
   `_🤖 본 코멘트는 AI가 작성했습니다._`.
7. Show the user the base and old/new head, verification, exact replies and
   `resolve | keep open` actions, re-review candidates, operation order, risks,
   and one recommendation. Ask one publication question and stop `Pending`.
8. After current-turn approval, re-read every frozen local and remote field.
   Any branch, head, base, identity, dirty-path, review, or thread drift
   invalidates approval and returns `Blocked` with a refreshed plan.
9. Publish in order: exact `--force-with-lease=<full-head-ref>:<old_head>` push;
   confirm the PR now names the new head; post each approved reply; then resolve
   only its verified, successfully replied thread. Never use plain `--force` or
   an unfrozen lease.
10. Re-read reviews, requested reviewers, threads, checks, and mergeability
    after the push. Do not guess whether stale-review dismissal is configured:
    use the observed post-push review state. Only when no current actionable,
    deferred, or unverified finding remains, re-request review from prior human
    reviewers whose feedback was addressed or whose approval is no longer valid
    for the new head. Exclude the author, authenticated user, bots, and reviewers
    with a still-valid approval. Prefer a formal GitHub review request; if GitHub
    rejects an otherwise eligible reviewer, post the approved fallback summary
    that mentions that reviewer and report `mention fallback`, not a formal
    request. Otherwise post the approved normal rebase summary after the
    re-review decision.
11. Re-read the PR once more. Report partial remote writes exactly and never
    claim a reply, resolution, review request, check, or mergeable state that was
    not observed.

## Sweep CI mode

1. Require a fresh active-sweep handoff for one exact open PR and one previously
   unused `(base_sha, old_head)` pair. Missing, ambiguous, direct-only, or repeated
   authority is `Blocked` before rebase or remote write.
2. Run the normal identity, ownership, clean-worktree, exact-base, conflict,
   preservation, and verification gates. Record the pair and verified `new_head`
   in `.tigerkit/pr-rebase.md`; do not create a separate sweep ledger.
3. Skip only the publication question. Immediately before the push and each later
   remote write, re-read the frozen repository, PR, identities, open state,
   base/head refs and SHAs, remote, exact refspec, lease, review/thread targets,
   and local clean state. Any drift is `Blocked`; never refresh the lease to
   overwrite an unexpected head.
4. When a rewrite is required, publish exactly once as
   `git push <remote> <new_head>:<full-head-ref>
   --force-with-lease=<full-head-ref>:<old_head>`. Confirm that the remote PR head
   equals `new_head`, then promote it as the expected head for later reply/thread
   writes. If no rewrite is required, do not push and return the observed head.
5. Apply only rebase-satisfied replies, verified thread resolutions, and
   conditional re-review using the normal order. Defer the PR-level summary to
   `tk-pr-sweep`, return its exact draft/material with `summary budget: unused`,
   and never publish the normal or mention-fallback summary in CI mode. Every
   generated reply ends exactly with `_🤖 본 코멘트는 AI가 작성했습니다._`.
6. Return the exact repository/PR, consumed `(base_sha, old_head)` pair,
   `new_head`, fresh category evidence, remaining open findings, and native
   `Pass | Fail | Blocked | Unverifiable` state to the active sweep. Do not emit a
   user-facing phase summary; the sweep owns aggregate output.

## Publication gate

The plan must freeze the repository, PR, identities, base/head refs and SHAs,
lease, refspec, verification, replies, thread actions, summary body, re-review
candidates, fallback mentions, operation order, and exclusions. Approval covers
only that plan. A failed reply leaves its thread open; any remaining actionable
finding suppresses re-review. Branch protection or permission failure is never
bypassed.

Use `Pass` only after the requested local and remote scope is observed complete,
`Pending` while waiting for publication approval, `Blocked` for unsafe authority
or drift, `Fail` for a change-related or partial-write failure, and
`Unverifiable` when required Git, GitHub, test, review, or thread evidence is
unavailable.

Lead with `## PR rebase`. Keep exact outbound text and full provenance in the
owned artifact.

### 🔴 HARD GATE · terminal user summary

Begin the terminal response with `## PR rebase`. Do not emit a receipt heading,
`Outcome:` label, procedural preamble, or bottom metadata block. Expose exact
IDs, refs, SHAs, and recovery details only when they change the next action.

### 🔴 HARD GATE · response language

Use the latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, refs, and exact source literals stable.

## User decision questions

When identity, scope, conflict intent, or publication blocks progress, ask one
self-contained `Question` before any `Recommendation`, with only
decision-relevant evidence and one recommended option. Render the question and
options directly in chat; do not call structured question or input tools.
Preserve `Pending | Blocked` until the user answers.
