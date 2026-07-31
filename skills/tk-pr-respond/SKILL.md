---
name: tk-pr-respond
description: "[user] Resolve selected GitHub pull-request feedback through verified tk-implement units and an exact current-turn publication plan."
argument-hint: "<pull request or repository>"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Respond to pull-request feedback

Start only when the user selects `/tk-pr-respond`, `$tk-pr-respond`, or the host
skill picker. Do not activate from generic review, implementation, triage, or
continuation requests.

This skill owns review interpretation, resolution-unit planning, aggregate
review state, and bounded remote publication. It writes `.tigerkit/pr-respond.md`
as evidence, but it never edits product code or creates product commits itself.
Each code change is delegated to `tk-implement` as one independently verifiable
unit; `tk-implement` owns the unit commit and verification.

## Workflow

1. Resolve exactly one PR, repository, author, authenticated user, branch, head
   SHA, base, open/draft state, checks, reviews, comments, and review threads.
   Complete pagination and stop on author/login mismatch before mutation.
2. Group current review findings by thread and suppress superseded iterations.
   Preserve exact comment/thread IDs, a bounded quote, requested outcome, R/AC,
   scope, exclusions, and verification obligations.
3. Show numbered resolution units and wait for the user's selection. Selection
   authorizes only those units; it does not authorize a remote write.
4. Handoff one unit at a time to `tk-implement` with the PR identity and exact
   comment/thread IDs. Do not create empty per-comment commits. Aggregate only
   verified unit results and keep deferred or unverified threads open.
5. Draft `.tigerkit/pr-respond.md` with exact push refspec, reply bodies,
   resolvable thread IDs, intentionally open threads, reviewers, and exclusions.
   Stop with `Pending` for current-turn publication approval.
6. After approval, recheck branch, local `HEAD`, PR head SHA, open state, author,
   checks, and thread state. Drift invalidates approval and returns `Blocked`.
7. Publish in this order: explicit push, exact replies, verified thread
   resolution, optional summary comment, and selected human re-review requests.
   Re-read the PR and report partial writes as `Fail`. Never force-push, merge,
   close unrelated threads, request bot review, tag, release, or publish a
   release.

Use `Pass` only when the requested response scope is complete, `Pending` while
waiting for selection or publication approval, `Blocked` for authority,
identity, or freshness conflicts, `Fail` for a change-related failure, and
`Unverifiable` when required GitHub, Git, check, or thread evidence is missing.
Lead with `## PR respond` and keep exact outbound text and provenance in the
owned artifact.

### 🔴 HARD GATE · terminal user summary

Begin the terminal response with `## PR respond`. Do not emit a receipt heading,
`Outcome:` label, or bottom metadata block. Expose exact IDs, paths, commits,
and recovery details only when they change the user's next action.

### 🔴 HARD GATE · response language

Use the latest explicit user language for all free-form user-facing prose.
Keep headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

When selection, identity, scope, or publication blocks progress, ask one
self-contained `Question` before any `Recommendation`, with one recommended
option. A failed structured-input call preserves `Pending` or `Blocked`.
