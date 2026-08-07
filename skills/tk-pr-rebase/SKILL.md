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

Start only via `/tk-pr-rebase`, `$tk-pr-rebase`, or host skill picker. Never
activate for generic rebase, update-branch, conflict, review-response, or
continuation. Only automatic entry: fresh exact-PR handoff from active
`tk-pr-sweep`.

Own one PR's local rebase, `.tigerkit/pr-rebase.md` plan, bounded
force-with-lease publication, rebase-satisfied review replies and thread resolution,
rebase summary, and conditional human re-review. Never implement unrelated
feedback, merge, close, tag, release, or change repository rules.

## Modes

- **Normal:** explicit invocation authorizes local rebase only; keep publication
  question below.
- **Sweep CI:** `--ci` requires active `tk-pr-sweep` handoff freezing exact
  repository, PR, base/head refs and SHAs, and route attempt. After the sweep
  Plan approval, the handoff grants bounded rebase/conflict resolution and
  publication without another question; semantic conflict ambiguity remains
  `Blocked`.

## Workflow

1. Resolve exactly one open PR, repository, authenticated identity, author, head
   repository/ref/SHA, base repository/ref/SHA, local branch, dirty paths, active
   Git operation, checks, reviews, comments, threads, and requested reviewers.
   Stop on ambiguity, identity/ownership mismatch, unsafe fork destination, or
   operation not created by this plan.
2. Fetch exact remote head and latest base. Freeze `old_head`, `base_sha`, current
   review/thread state, and existing requested reviewers. Require clean worktree,
   no unrelated staged paths, local `HEAD == old_head`, and remote PR head
   `== old_head`.
3. Classify findings. Close a thread only when updating PR to frozen base
   satisfies its requested outcome. Keep unrelated, deferred,
   superseded-uncertain, and unverified findings open.
4. Rebase branch onto exact `base_sha`. Normal invocation authorizes local rebase,
   not abort, reset, push, or comment publication. For each conflict iteration,
   use `tk-merge-conflict`; resume only after operation, intent, index, marker,
   and verification gates pass. In Sweep CI, the exact approved maintenance-
   rebase handoff may publish the verified result; never guess or auto-abort.
5. Verify rebase ended; worktree and index clean; `base_sha` ancestors new `HEAD`;
   intended commits and diff remain; relevant tests/checks pass. If branch already
   contains `base_sha` and needs no rewrite, do not force-push.
6. Write `.tigerkit/pr-rebase.md`: frozen refs and SHAs, verification, exact
   `--force-with-lease` expectation/refspec, every outbound reply, thread action,
   intentionally open finding, summary, prior human reviewers, normal and
   reviewer-mention fallback bodies, exclusions. Render PR and review/thread
   references as clickable Markdown links in user-facing output when URLs exist;
   normalize GitHub `<br>`/`<br/>` breaks to real newlines before display. End every external
   reply/comment with `_🤖 본 코멘트는 AI가 작성했습니다._`.
7. Show base, old/new head, verification, exact replies and
   `resolve | keep open` actions, re-review candidates, operation order, risks,
   and one recommendation. Ask one publication question; stop `Pending`.
8. After current-turn approval, re-read every frozen local and remote field. Any
   branch, head, base, identity, dirty-path, review, or thread drift invalidates
   approval; return `Blocked` with refreshed plan.
9. Publish in order: exact
   `--force-with-lease=<full-head-ref>:<old_head>` push; confirm PR names new
   head; post each approved reply; resolve only its verified, successfully
   replied thread. Never use plain `--force` or unfrozen lease.
10. Re-read reviews, requested reviewers, threads, checks, and mergeability after
    push. Observe post-push review state; never guess stale-review dismissal.
    Only with no current actionable, deferred, or unverified finding, re-request
    review from prior humans whose feedback was addressed or approval is invalid
    for new head. Exclude author, authenticated user, bots, and still-valid
    approvers. Prefer formal GitHub request. If GitHub rejects an otherwise
    eligible reviewer, post approved fallback summary mentioning them and report
    `mention fallback`, not formal request. Otherwise post approved normal rebase
    summary after re-review decision.
11. Re-read PR again. Report partial remote writes exactly; claim no unobserved
    reply, resolution, review request, check, or mergeable state.

## Sweep CI mode

1. Require fresh active-sweep handoff for one exact open PR and unused
   `(base_sha, old_head)` pair. Missing, ambiguous, direct-only, or repeated
   authority is `Blocked` before rebase or remote write.
2. Run normal identity, ownership, clean-worktree, exact-base, conflict,
   preservation, and verification gates. Record pair and verified `new_head` in
   `.tigerkit/pr-rebase.md`; no separate sweep ledger.
3. Skip only publication question. Immediately before push and every later
   remote write, re-read frozen repository, PR, identities, open state, base and head
   refs and SHAs, remote, exact refspec, lease, review and thread targets, and local clean
   state. Drift is `Blocked`; never refresh lease over unexpected head.
4. When rewrite required, publish exactly once as
   `git push <remote> <new_head>:<full-head-ref>
   --force-with-lease=<full-head-ref>:<old_head>`. Confirm remote PR head equals
   `new_head`, then use it as expected head for later reply/thread writes. With no
   rewrite, do not push; return observed head.
5. Apply only rebase-satisfied replies, verified thread resolutions, and
   conditional re-review in normal order. Defer PR-level summary to
   `tk-pr-sweep`; return exact draft/material with `summary budget: unused`.
   Never publish normal or mention-fallback summary in CI mode. Every generated
   reply ends exactly with `_🤖 본 코멘트는 AI가 작성했습니다._`.
6. Return exact repository/PR, consumed `(base_sha, old_head)` pair, `new_head`,
   fresh category evidence, remaining open findings, and native
   `Pass | Fail | Blocked | Unverifiable` state to active sweep. No user-facing
   phase summary; sweep owns aggregate output.

## Publication gate

Plan freezes repository, PR, identities, base and head refs and SHAs, lease, refspec,
verification, replies, thread actions, summary body, re-review candidates,
fallback mentions, order, and exclusions. Approval covers only that plan. Failed
reply leaves thread open; remaining actionable finding suppresses re-review.
Never bypass branch protection or permission failure.

Use `Pass` only after requested local and remote scope is observed complete;
`Pending` awaiting publication approval; `Blocked` for unsafe authority or drift;
`Fail` for change-related or partial-write failure; `Unverifiable` when required
Git, GitHub, test, review, or thread evidence is unavailable.

Lead with `## PR rebase`. Keep exact outbound text and full provenance in owned
artifact.

### 🔴 HARD GATE · terminal user summary

Begin terminal response with `## PR rebase`. No receipt heading, `Outcome:`
label, procedural preamble, or bottom metadata block. Expose exact IDs, refs,
SHAs, and recovery details only when they change next action.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, refs, and exact source literals stable.

## User decision questions

When identity, scope, conflict intent, or publication blocks progress, ask one
self-contained `Question` before any `Recommendation`, with only
decision-relevant evidence and one recommended option. Render question and options
directly in chat; never call structured question or input tools. Preserve
`Pending | Blocked` until user answers.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 pr-rebase · 응답 필요` only for a user decision/approval, `⏳ pr-rebase · 대기` only when external waiting is next, and `🚗 pr-rebase · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > pr-rebase`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.

## Next-action handoff

Whenever this skill hands control back to the user for a question, `Pending`,
`Blocked`, `Unverifiable`, bounded wait, or an actionable terminal result, end
the visible handoff with exactly one `Next:` line naming the recommended action
or next skill and its condition. Before rendering any user-facing `Question` or
publication/approval plan, emit exactly one nonterminal hand-raise checkpoint
in this skill's `🙋 ... · 응답 필요` form; a parent may own the display in
orchestration. Do not use only a `🤹` or `🚗` boundary marker for a user
decision. Mark the single recommended option with `👍 Recommendation:`.
Do not leave only a child receipt or generic “continue”; omit `Next:` only for
a terminal success with no follow-up action.
