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

Start only via `/tk-pr-triage`, `$tk-pr-triage`, or host skill picker. Never
activate for generic GitHub question, implementation, issue triage, or
review-response. Only automatic entry: fresh configured-repository handoff from
active `tk-pr-sweep`.

Read-only for repositories and GitHub: never mutate project files, branches,
commits, issues, pull requests, comments, reviews, or threads. Only owned state:
`$XDG_CONFIG_HOME/tigerkit/pr-triage.json` (fallback
`~/.config/tigerkit/pr-triage.json`), containing `repositories` array. Explicit
repository arguments override for one run. Without arguments, read config; if
missing, bootstrap with executing repository's `origin` and report created path.
Never hardcode TigerKit.

## Workflow

1. Resolve authenticated GitHub login and repository targets from explicit
   arguments or triage config. If missing config cannot bootstrap because
   `origin` unavailable, stop `Unverifiable` with exact remedy.
2. Execute `scripts/triage.mjs` directly. It uses paginated REST reads for open
   PRs, direct and team review requests, review decisions, inline comments, issue
   comments, checks, and status. On nonzero exit or bounded API failure leaving
   required evidence unavailable, rerun that repository once from fresh script
   execution; never merge partial snapshots. Preserve repeated failure; return
   `Unverifiable` when classification is prevented.
3. Report only actionable items for authenticated author or requested reviewer.
   Preserve repository, PR number, author, head SHA, and evidence per item; never
   mix repositories or PRs.
4. Classify as `merge_conflict`, `checks_failed`, `checks_unverifiable`,
   `changes_requested`, `needs_reply`, `review_requested`,
   `awaiting_re_review`, or `draft`. Keep API failures visible as
   `checks_unverifiable` or bounded `failures`; never turn missing evidence into
   approval.
5. Render results before any question. Group first by `Act now`,
   `Review requests`, and `Waiting`, then by repository within each; omit empty
   groups. Render each PR as a Markdown link using its `url`, and each actionable
   review/thread evidence as a Markdown link when its URL is available; never
   expose raw URLs in the user-facing table. Per item show priority, PR,
   plain-language current state, attention reason, and one recommended next
   action. Normalize GitHub `<br>`/`<br/>` breaks to real newlines before display.
   Keep raw category and provenance as support; never make user decode them. Ask
   no question by default.
   Recommendations never authorize apply, reply, resolve, push, merge, or
   release.

Deterministic script is reducer, not remote-write client. Output contains raw
generation time for machine comparison and a labeled local generation time for
user display, plus login, config source, repositories, counts, items, and failures.
If review-thread resolution state is needed, `tk-pr-respond` must refetch current
thread state before proposing or executing resolve.

Use `Pass` only when collection and classification complete, `Unverifiable` when
required evidence unavailable, `Fail` only for change-related error. Lead with
`## PR triage`; never write receipt or imply recommendation was applied.

### 🔴 HARD GATE · terminal user summary

Begin terminal response with `## PR triage`. No remote-write receipt, `Outcome:`
label, or bottom metadata block. Expose exact IDs and paths only when they change
user's next action.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

### 🔴 CHECKPOINT / STOP · Read-only handoff

Triage is read-only. If next action requires user choice, ask one self-contained
`Question` before any `Recommendation`; render directly in chat, never call
structured question or input tools. Never mutate state. Reply, resolve, push, merge,
release, or edit stops here for separately authorized owner.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 pr-triage · 응답 필요` only for a user decision/approval, `⏳ pr-triage · 대기` only when external waiting is next, and `🚗 pr-triage · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > pr-triage`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.
