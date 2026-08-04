---
name: tk-pr-triage
description: "[user/auto] Read-only triage of configured GitHub pull requests, reviews, checks, replies, and re-review state."
argument-hint: "<repository or current repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Triage pull requests

Start only when the user selects `/tk-pr-triage`, `$tk-pr-triage`, or the host
skill picker. Do not activate from a generic GitHub question, implementation
request, issue triage, or review-response request. A fresh configured-repository
handoff from active `tk-pr-sweep` is the only automatic entry.

This skill is read-only for repositories and GitHub: it must not mutate project
files, branches, commits, issues, pull requests, comments, reviews, or threads.
Its only owned state is `$XDG_CONFIG_HOME/tigerkit/pr-triage.json` (falling back
to `~/.config/tigerkit/pr-triage.json`), which contains a `repositories` array.
Explicit repository arguments are one-run overrides. Without arguments, read
that config; if it is missing, bootstrap it with the executing repository's
`origin` and report the created path. Never hardcode TigerKit.

## Workflow

1. Resolve the authenticated GitHub login and repository targets from explicit
   arguments or the triage config. If a missing config cannot be bootstrapped
   because `origin` is unavailable, stop `Unverifiable` with the exact remedy.
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
5. Render user-facing results before any question. First group by `Act now`,
   `Review requests`, and `Waiting`, then group by repository inside each status;
   omit empty groups. For each item show priority, PR, plain-language current
   state, why it needs attention, and one recommended next action; keep raw
   category and provenance as supporting detail rather than making the user
   decode them. Do not ask a question by default. Recommendations do not
   authorize apply, reply, resolve, push, merge, or release.

The deterministic script is a reducer, not a remote-write client. Its output
contains a generation time, login, config source, repositories, counts, items,
and failures.
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

### 🔴 CHECKPOINT / STOP · Read-only handoff

Triage is read-only. If the next action requires user choice, ask one
self-contained `Question` before any `Recommendation`; render it directly in
the chat response and do not call structured question or input tools. Do not
mutate state. Any action that would reply, resolve, push, merge, release, or
edit stops here for a separately authorized owner.
