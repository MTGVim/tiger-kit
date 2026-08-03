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
   Explicit comment or thread IDs are sufficient discovery anchors: when the PR
   number is omitted, search the current repository and branch and proceed only
   if every selected ID resolves to the same open PR. Complete pagination and
   stop on missing, ambiguous, or author/login-mismatched identity before mutation.
2. Group current review findings by thread and suppress superseded iterations.
   Preserve exact comment/thread IDs, a bounded quote, requested outcome, R/AC,
   scope, exclusions, and verification obligations.
3. Before asking for a selection, show every current finding in a compact table:
   comment/thread ID, reviewer and bounded quote or faithful summary, requested
   outcome, assessment, recommended `apply | reply | defer` disposition with
   rationale, expected change scope, and verification. Include a reply draft for
   `reply` recommendations. Group coupled findings into numbered resolution
   units, state one recommended selection, then ask one selection question.
   Selection authorizes only those units; it does not authorize a remote write.
4. Handoff one unit at a time to `tk-implement` with the PR identity and exact
   comment/thread IDs. Do not create empty per-comment commits. Aggregate only
   verified unit results and keep deferred or unverified threads open.
5. Draft `.tigerkit/pr-respond.md` with exact push refspec, a reply body for
   every selected current finding, resolvable thread IDs, intentionally open
   threads, prior human reviewers, re-review candidates, and exclusions. Every
   external reply/comment ends with `_🤖 본 코멘트는 AI가 작성했습니다._`.
   Before publication approval, show a second compact table with each selected
   ID, implementation result, verification, exact reply draft, and recommended
   `resolve | keep open` thread action, followed by the outbound operation order
   and one recommendation. Then ask one publication question and stop with
   `Pending`.
6. After approval, recheck branch, local `HEAD`, PR head SHA, open state, author,
   checks, and thread state. Drift invalidates approval and returns `Blocked`.
7. Publish in this order: explicit push; exact reply to every selected current
   finding; verified thread resolution only after its reply succeeds; optional
   approved summary comment; fresh review, requested-reviewer, thread, check,
   and mergeability read; conditional human re-review requests; then the
   applicable approved normal or reviewer-mention fallback summary comment. A
   failed reply leaves its thread open.
8. Re-request review only when no current actionable, deferred, or unverified
   finding remains. Use the observed post-push state rather than guessing stale
   review settings. Request prior human reviewers whose feedback was addressed
   or whose approval is no longer valid for the new head; exclude the PR author,
   authenticated user, bots, and reviewers with a still-valid approval. Prefer
   a formal GitHub review request. If GitHub rejects an otherwise eligible
   reviewer, use only the approved fallback summary comment to mention them and
   report `mention fallback`, not a formal request.
9. Re-read the PR and report partial writes as `Fail`. Never force-push, merge,
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
option. Render the question and options directly in the chat response; do not
call structured question or input tools. Preserve `Pending | Blocked` until the
user answers.
