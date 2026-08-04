---
name: tk-pr-respond
description: "[user/auto] Resolve one pull request's selected feedback or GitHub Actions failures through verified tk-implement units and bounded publication."
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Respond to pull-request feedback

Start only via `/tk-pr-respond`, `$tk-pr-respond`, or host skill picker. Never
activate for generic review, implementation, triage, or continuation. Only
automatic entry: fresh exact-PR handoff from active `tk-pr-sweep`.

Own review interpretation, resolution-unit planning, aggregate review state,
and bounded remote publication. Write `.tigerkit/pr-respond.md` evidence, but
never edit product code or create product commits. Delegate each code change to
`tk-implement` as one independently verifiable unit; `tk-implement` owns commit and
verification.

## Modes

- **Normal:** retain selection and publication questions.
- **CI:** explicit `--ci`, direct or through `tk-pr-sweep`, authorizes fresh
  supported scope without questions. It never authorizes another PR, external
  CI, unverifiable checks, force-push, merge, close, tag, release,
  draft-to-`Ready for review` transitions, or publication outside this response.

## Progress

In direct CI mode, emit compact `▶️ Progress` checkpoints after scope selection,
around each unit/check, before publication, and after final fresh read. State
decision, decisive evidence, and result/next action; continue without approval,
`Pending`, or pause. Under `tk-pr-sweep`, return evidence to sweep without
duplicate commentary. Normal mode unchanged.

Use `✅ Pass`, `⏳ Waiting`, `⚠️ Advisory`, `❌ Fail`, `⛔ Blocked`, and
`❓ Unverifiable` for matching outcomes; preserve terminal `Status: <token>`
exactly.

## Workflow

1. Resolve exactly one PR, repository, author, authenticated user, branch, head
   SHA, base, open/draft state, checks, reviews, comments, and threads. Explicit
   comment/thread IDs suffice as discovery anchors: without PR number, search
   current repository and branch and proceed only if all selected IDs resolve to same
   open PR. Complete pagination. Stop before mutation on missing, ambiguous, or
   author/login-mismatched identity.
2. Group current findings by thread; suppress superseded iterations. Preserve
   exact comment/thread IDs, bounded quote, requested outcome, R/AC, scope,
   exclusions, and verification obligations.
3. Before selection, show every current finding in compact table: comment/thread
   ID, reviewer and bounded quote or faithful summary, requested outcome,
   assessment, recommended `apply | reply | defer` plus rationale, expected scope,
   and verification. Include reply draft for `reply`. Group coupled findings into
   numbered resolution units, state one recommended selection, ask one selection
   question. Selection authorizes only units, never remote write.
4. Handoff one unit at a time to `tk-implement` with PR identity and exact
   comment/thread IDs. `Pass` is internal loop signal: without terminal response,
   pause, or confirmation, use CI or sweep progress checkpoint when applicable and
   invoke `tk-implement` for next selected unit. Normal mode adds no intermediate checkpoint. Exit
   only after every selected unit has verified result or bounded non-success.
   Never create empty per-comment commits. Aggregate verified results only; keep
   deferred or unverified threads open.
5. Draft `.tigerkit/pr-respond.md` with exact push refspec, reply body per selected
   current finding, resolvable thread IDs, intentionally open threads, prior
   human reviewers, re-review candidates, and exclusions. End every external
   reply/comment with `_🤖 본 코멘트는 AI가 작성했습니다._`. In Normal mode,
   before approval show second compact table: each selected ID, implementation
   result, verification, exact reply draft, recommended
   `resolve | keep open`; then outbound order and one recommendation. Ask one
   publication question; stop `Pending`. CI never enters this boundary.
6. After approval, recheck branch, local `HEAD`, PR head SHA, open state, author,
   checks, and threads. Drift invalidates approval; return `Blocked`.
7. Publish in order: explicit push; exact reply to each selected current finding;
   verified thread resolution only after reply succeeds; optional approved
   summary; fresh review, requested-reviewer, thread, check, and mergeability
   read; conditional human re-review; applicable approved normal or
   reviewer-mention fallback summary. Failed reply leaves thread open.
8. Re-request review only with no current actionable, deferred, or unverified
   finding. Use observed post-push state; never guess stale-review settings.
   Request prior humans whose feedback was addressed or approval is invalid for
   new head. Exclude PR author, authenticated user, bots, and still-valid
   approvers. Prefer formal GitHub request. If GitHub rejects an otherwise
   eligible reviewer, mention them only in approved fallback summary and report
   `mention fallback`, not formal request.
9. Re-read PR; report partial writes as `Fail`. Never force-push, merge, close
   unrelated threads, request bot review, mark draft ready for review, tag,
   release, or publish release.

## CI mode

1. From fresh read freeze repository, authenticated identity, PR author, open
   state, base, head ref/SHA, exact push refspec, checks, findings, and requested
   reviewers. Direct `--ci` and sweep handoff grant same authority. Stop
   `Blocked` before mutation on identity, repository, ref, or head drift.
2. For `changes_requested` or `needs_reply`, select every fresh actionable
   finding, create minimum independently verifiable units, run normal
   `tk-implement` loop without selection question. Each unit `Pass` is internal.
   After last verified unit, continue same active flow through freshness recheck
   and publication; no terminal response, `Pending`, or Normal publication
   question.
3. For `checks_failed`, resolve each failure provider. Automate GitHub Actions
   only. Read current run, job, step, annotation, and bounded log evidence;
   external-provider failures stay report-only. Before creating unit,
   distinguish repository cause from queued, cancelled, flaky, infrastructure,
   or inaccessible evidence. Never invoke interactive `gh-fix-ci` as automatic
   child. If no supported repository-caused failure remains, create no unit or push;
   return `Unverifiable` with observed unsupported or unavailable state.
4. After every feedback unit has verified result, or one repository-caused
   Actions fix returns `Pass`, render direct CI progress or return evidence to
   active sweep, then immediately re-read repository, authenticated identity,
   open state, remote head/ref; verify all local unit commits descend from frozen
   head. Mismatch is `Blocked`; otherwise push only frozen head refspec before
   replies or resolution. Never stop after unit commit or request approval. For
   repository-caused Actions fix, fetch new exact head and fresh check state. If
   head equals just-pushed commit, promote it to expected head and ancestry
   baseline for next cycle. Maximum three corrective cycles. Repeated unchanged
   failure, exhausted third cycle, or unverifiable post-push checks stops without
   fourth mutation.
5. Publish exact per-finding replies, resolve only freshly verified threads, and
   conditionally request human re-review in normal order and exclusions. Publish at
   most one PR-level summary combining CI-fix and supplied rebase outcomes. Every
   generated reply/comment ends exactly with
   `_🤖 본 코멘트는 AI가 작성했습니다._`.
6. Re-read PR after all writes. Return `Pass` only when selected feedback and
   supported GitHub Actions failures complete on observed head. External CI is
   report-only; missing evidence is `Unverifiable`, drift `Blocked`, and
   change-related or partial-write failure `Fail`.

Use `Pass` only when requested response scope is complete; `Pending` awaiting
selection or publication approval; `Blocked` for authority, identity, or freshness
conflicts; `Fail` for change-related failure; `Unverifiable` when required
GitHub, Git, check, or thread evidence is missing. Lead with `## PR respond`;
keep exact outbound text and provenance in owned artifact.

### 🔴 HARD GATE · terminal user summary

Begin terminal response with `## PR respond`. No receipt heading, `Outcome:`
label, or bottom metadata block. Expose exact IDs, paths, commits, and recovery
details only when they change user's next action.

### 🔴 HARD GATE · response language

Use latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

When selection, identity, scope, or publication blocks progress, ask one
self-contained `Question` before any `Recommendation`, with one recommended
option. Render question and options directly in chat; never call structured
question or input tools. Preserve `Pending | Blocked` until user answers.
