---
name: tk-pr-triage
description: "[user] Read-only triage of the executing repository's GitHub pull requests, reviews, checks, replies, and re-review state."
argument-hint: "<repository or current repository>"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Triage pull requests

Start only when the user selects `/tk-pr-triage`, `$tk-pr-triage`, or the host
skill picker. Do not activate from a generic GitHub question, implementation
request, issue triage, or review-response request.

This skill is strictly read-only. It owns no local artifact and must not mutate
files, branches, commits, GitHub issues, pull requests, comments, reviews, or
threads. Resolve the target from an explicit repository argument; otherwise use
the `origin` remote of the executing repository. Never hardcode TigerKit.

## Workflow

1. Resolve the authenticated GitHub login and target repository.
2. Execute `scripts/triage.mjs` directly. It uses paginated REST reads for open
   PRs, direct and team review requests, review decisions, inline comments,
   issue comments, checks, and status. On a nonzero exit or a bounded API
   failure that leaves required evidence unavailable, rerun that repository
   once from a fresh script execution; never merge partial snapshots. Preserve
   a repeated failure and return `Unverifiable` when it prevents classification.
3. Report only actionable items for the authenticated author or requested
   reviewer. Preserve repository, PR number, author, head SHA, and evidence for
   every item; never mix data between repositories or PRs.
4. Classify items as `merge_conflict`, `checks_failed`, `checks_unverifiable`,
   `changes_requested`, `needs_reply`, `review_requested`, `awaiting_re_review`,
   or `draft`. Keep API failures visible as `checks_unverifiable` or in the
   bounded `failures` list; never turn missing evidence into approval.
5. End with one next action per item. Recommendations do not authorize apply,
   reply, resolve, push, merge, or release.

The deterministic script is a reducer, not a remote-write client. Its output
contains a generation time, login, repositories, counts, items, and failures.
If review-thread resolution state is required, `tk-pr-respond` must fetch the
current thread state again before proposing or executing a resolve operation.

Use `Pass` only when collection and classification complete, `Unverifiable` when
required evidence is unavailable, and `Fail` only for a change-related error.
Lead with `## PR triage`; do not write a receipt or imply that a recommendation
was applied.

### 🔴 HARD GATE · terminal user summary

Begin the terminal response with `## PR triage`. Do not emit a remote-write
receipt, `Outcome:` label, or bottom metadata block. Expose exact IDs and paths
only when they change the user's next action.

### 🔴 HARD GATE · response language

Use the latest explicit user language for all free-form user-facing prose.
Keep headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

Triage is read-only. If the next action requires user choice, ask one
self-contained `Question` before any `Recommendation`; do not mutate state.
