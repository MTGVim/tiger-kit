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

Parent continuation is mandatory: a `tk-implement` result is an internal receipt,
even when the host renders the child output. After every child result, emit one
parent-owned continuation checkpoint naming the next `respond` phase and continue
in the same turn. Never stop, wait, ask the user to say “continue,” or return the
child result as terminal output. Only this skill's publication checkpoint or
terminal response is a user boundary.

## Modes

- **Normal:** retain selection and publication questions.
- **CI:** explicit `--ci`, direct or through `tk-pr-sweep`, authorizes fresh
  supported scope without questions. It never authorizes another PR, external
  CI, unverifiable checks, force-push, merge, close, tag, release,
  draft-to-`Ready for review` transitions, or publication outside this response.
  A sweep handoff marked `test-only` additionally forbids production source,
  configuration, dependency, lockfile, security/data/performance, or weakened
  assertion changes; if the selected finding needs any of those, return
  `Blocked` before invoking `tk-implement`.

## Progress

In direct CI mode, emit one compact line at scope/unit/publication boundaries,
such as `🤹 respond > implement 1/2 · next unit` or `🤹 respond > publish ·
reply/resolve/re-review/summary`. Omit `tk-`,
receipts, reasoning, logs, and repeated checks. Under sweep, return evidence
without duplicate commentary; in standalone Normal mode mark selection or
publication as `🙋 respond · 응답 필요`. Actual names/contracts keep `tk-`.

Use `⏳ 대기` only when waiting is the next action; preserve terminal
`Status: <token>` as the only final outcome marker.

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
   comment/thread IDs while tracking the numbered selected-unit list and current
   index. `Pass` is internal. A unit-local `Fail` may advance only after clean
   worktree, identity, ref, and head evidence remain valid; `Blocked`,
   `Unverifiable`, scope/freshness/identity drift, or shared-safety failure
   freezes the remaining units. Otherwise record the result and, while any
   selected unit remains, emit one parent-owned `🤹 respond > implement
   <index>/<total> · <next>` checkpoint before invoking the next unit in the
   same turn without terminal output, pause, or confirmation. A host-visible
   child result is still only an internal receipt, never a user boundary. After
   the last unit, emit the next parent phase and continue the contract; do not
   wait for a user nudge. Exit only after every selected unit has a verified result or a
   justified bounded stop. Never create empty per-comment commits; keep
   deferred or unverified threads open. A failed unit remains open and is
   excluded from reply/resolve; the final aggregate remains `Fail` even when
   later independent units pass.
5. Draft `.tigerkit/pr-respond.md` with exact push refspec, reply body per selected
   current finding, resolvable thread IDs, intentionally open threads, prior
   human reviewers, re-review candidates, exclusions, and one PR-level review
   summary draft covering every selected unit, reply, verified resolution, open
   thread, and next re-review action. End every external reply/comment with
   `_🤖 본 코멘트는 AI가 작성했습니다._`. In Normal mode, before approval show
   the second compact table with each selected clickable thread link or ID, implementation result,
   verification, exact reply draft, and `resolve | keep open` recommendation,
   then the exact summary draft and outbound order; ask one publication
   question and stop `Pending`. CI never enters this boundary.
6. After approval, recheck branch, local `HEAD`, PR head SHA, open state, author,
   checks, and threads. Drift invalidates approval; return `Blocked`.
7. Publish in order: explicit push; exact reply to each selected current finding;
   verified thread resolution only after reply succeeds; fresh review,
   requested-reviewer, thread, check, and mergeability read; conditional human
   re-review under step 8's exclusions and its fresh result; exactly one required
   PR-level review summary
   comment containing the final review/fallback outcome. If a parent sweep has
   consumed its shared summary budget, return this content to the parent and do
   not publish it here. Otherwise put any mention fallback in this one summary,
   or use it only as the approved replacement; never publish a second summary.
   If no supported remote write occurs because all work is deferred, no-op, or
   report-only, keep only the draft and publish no summary comment. Failed reply
   leaves its thread open.
8. Apply these rules to the conditional re-review before step 7 publishes its
   summary: request review only with no current actionable, deferred, or
   unverified finding. Use observed post-push state; never guess stale-review
   settings.
   Request prior humans whose feedback was addressed or approval is invalid for
   new head. Exclude PR author, authenticated user, bots, and still-valid
   approvers. Prefer formal GitHub request. If GitHub rejects an otherwise
   eligible reviewer, mention them only in approved fallback summary and report
   `mention fallback`, not formal request.
9. Re-read PR; report partial writes as `Fail`. Never force-push, merge, close
   unrelated threads, request bot review, mark draft ready for review, tag,
   release, or publish release.

## CI mode

When the sweep handoff is `test-only`, inspect the complete selected finding
before invoking `tk-implement`. Permit only paths in the repository's existing
test layout (`test/`, `tests/`, `spec/`, `*.test.*`, `*.spec.*`, or documented
test fixtures); mixed, unknown, production, configuration, dependency,
lockfile, security/data/performance, or weakened-assertion work is `Blocked`.
That scope violation blocks the whole response: no unit, commit, push, reply,
thread resolution, re-review, or summary.

1. From fresh read freeze repository, authenticated identity, PR author, open
   state, base, head ref/SHA, exact push refspec, checks, findings, and requested
   reviewers. Direct `--ci` and sweep handoff grant same authority. Stop
   `Blocked` before mutation on identity, repository, ref, or head drift.
2. For `changes_requested` or `needs_reply`, select every fresh actionable
   finding, create minimum independently verifiable units, and track the
   remaining-unit count. Run the `tk-implement` loop without a selection
   question; after each unit `Pass` or unit-local `Fail` with clean evidence,
   immediately invoke the next unit. Do not enter freshness recheck or publication until the
   remaining-unit count is zero; no terminal response, `Pending`, or Normal
   publication question may occur between units. A unit-local `Fail` advances
   only with clean identity/ref/head evidence; `Blocked`, `Unverifiable`, or
   shared-safety failure stops the remaining units. A failed unit remains open
   and is excluded from reply/resolve; a final aggregate `Fail` is not promoted
   to `Pass` by later successful units.
3. For `checks_failed`, resolve each failure provider. Automate GitHub Actions
   only. Read current run, job, step, annotation, and bounded log evidence;
   external-provider failures stay report-only. Before creating unit,
   distinguish repository cause from queued, cancelled, flaky, infrastructure,
   or inaccessible evidence. Never invoke interactive `gh-fix-ci` as automatic
   child. If no supported repository-caused failure remains, create no unit or push;
   return `Unverifiable` with observed unsupported or unavailable state. One
   repository-caused Actions fix is one cycle, not completion: after each cycle
   fresh-read all failures, keep any supported remaining count, and repeat only
   within the maximum three cycles.
4. After the last feedback unit has a verified result, or one
   repository-caused Actions fix returns `Pass`, render direct CI progress or
   return evidence to active sweep, then immediately re-read repository,
   authenticated identity,
   open state, remote head/ref; verify all local unit commits descend from frozen
   head. Mismatch is `Blocked`; otherwise push only frozen head refspec before
   replies or resolution. Never stop after unit commit or request approval. For
   repository-caused Actions fix, fetch new exact head and fresh check state. If
   head equals just-pushed commit, promote it to expected head and ancestry
   baseline for next cycle. Maximum three corrective cycles. Repeated unchanged
   failure, exhausted third cycle, or unverifiable post-push checks stops without
   fourth mutation.
5. Publish exact per-finding replies, resolve only freshly verified threads, and
   fresh-read the PR state. When supported remote response work was published,
   conditionally request human re-review in normal order and exclusions, fresh-
   read its result, then publish exactly one required PR-level review summary
   combining selected feedback, verification, remaining open threads, and
   rebase/CI outcomes. If the path is external/report-only, deferred, or has no
   supported remote write, publish no summary comment. Under sweep,
   `summary budget: unused` lets this response consume and return the budget as
   consumed; `summary budget: consumed` makes it return the draft without
   publishing. Every generated reply/comment ends exactly with
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

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🤹 meaningful boundary` only for long-running orchestration work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

When selection, identity, scope, or publication blocks progress, ask one
self-contained `Question` before any `Recommendation`, with one recommended
option. Render question and options directly in chat; never call structured
question or input tools. Immediately before that user-facing question or a
publication-plan approval request, emit the nonterminal checkpoint
`🙋 respond · 응답 필요`; do not substitute a `🤹` boundary marker or omit the
checkpoint. Mark the single recommended option with `👍 Recommendation:` so it
is visually prominent. Preserve `Pending | Blocked` until user answers.

Whenever `tk-pr-respond` hands control back to the user for selection,
publication approval, `Pending`, `Blocked`, `Unverifiable`, bounded wait, or an
actionable terminal result, end the visible handoff with exactly one `Next:` line
naming the recommended action and condition. Use one concrete action such as
answering the shown question, re-invoking `$tk-pr-respond` after a host boundary,
or approving this response's publication plan; never leave only a child receipt
or generic “continue.” Do not recommend `tk-pr-open` unless the user separately
asks to open a new PR.
