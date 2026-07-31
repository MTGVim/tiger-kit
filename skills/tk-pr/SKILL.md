---
name: tk-pr
description: "[user] Own a GitHub pull request lifecycle through explicit open, triage, or respond mode. Draft and inspect safely, delegate review fixes to tk-implement, and require a current-turn publish checkpoint before any remote write."
argument-hint: "open|triage|respond [PR, branch, repository, or profile]"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Pull request lifecycle

Start only when the user selects `/tk-pr`, `$tk-pr`, or the host skill picker
with explicit `open | triage | respond` mode, or answers this skill's pending
decision in the same conversation. Natural-language PR requests without skill
selection, generic code review, implementation, issue management,
merge-conflict repair, and ordinary Git questions do not activate it.

Resolve exactly one mode before acting:

- `open`: prepare or update one draft pull request from verified commits.
- `triage`: inspect pull-request state without local or remote mutation.
- `respond`: map review feedback to resolution units, delegate code changes,
  verify the aggregate result, then publish selected responses.

If intent spans modes, complete the requested mode and report the next explicit
mode instead of silently chaining remote writes.

## Authority

`triage` is read-only. `open` and `respond` may write bounded local evidence to
`.tigerkit/pr.md`, but neither mode may push, create or update a pull request,
post a comment, resolve a thread, request review, or change draft state before
a current-turn publish approval names the exact outbound plan.

An instruction to apply review feedback authorizes only the selected
`tk-implement` resolution units and their verified commits. It does not
authorize any remote write. Past approval, generic continuation, or approval of
a different plan is insufficient.

This skill never edits product code or creates product commits itself. It may
invoke `tk-implement` only from active `respond` with one independently
verifiable resolution unit, exact comment/thread IDs, scope, R/AC, and
verification obligations. It owns cross-unit review state and remote
publication; `tk-implement` owns code mutation, verification, review, and one
unit commit.

## Mode procedures

For `open`, follow [open.md](references/open.md). For `triage`, follow
[triage.md](references/triage.md). For `respond`, follow
[respond.md](references/respond.md). Use the deterministic
[triage script](scripts/triage.mjs) directly when its runtime prerequisites are
available; do not delegate script execution to a subagent.

## Shared gates

Before any mode result, resolve repository identity, authenticated GitHub
identity, current branch when applicable, exact PR identity, and freshness of
all evidence. Never mix comments, authors, branches, checks, or threads across
pull requests. A mismatch between PR author and authenticated account is a
material decision before `respond` mutation or publication.

Before a remote write, render one bounded publish plan containing target
repository and PR, branch/ref, operation order, title/body or reply text,
thread IDs to resolve, reviewers to request, and known exclusions. Recheck
branch, `HEAD`, PR head SHA, open state, author, and review-thread state after
approval and before the first write. Material drift invalidates approval and
returns `Blocked` with a refreshed plan.

Never force-push, rewrite history, merge, delete a branch, publish a release,
resolve an unverified thread, request review from unsupported bots, or hide a
known failing check. Use explicit branch/ref arguments for every push.

## Status and result

Use `Pass` only when the requested mode completed its owned scope. Use
`Pending` while waiting for target selection or publish approval, `Blocked`
for missing authority or conflicting identity/scope, `Fail` for a
change-related execution failure, and `Unverifiable` when required GitHub,
Git, check, or thread evidence cannot establish a verdict.

Lead with `## PR open`, `## PR triage`, or `## PR respond`. Show only
user-relevant state, actions, verification, and remaining risks. For multiple
PRs or review units, use a compact table. Keep full IDs, exact outbound text,
and provenance in `.tigerkit/pr.md`; do not paste raw API payloads or complete
comment histories.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between successful consecutive active procedure invocations.

Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.

Persist provenance only in `.tigerkit/pr.md` or an artifact already owned by the active child workflow. A read-only mode remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
