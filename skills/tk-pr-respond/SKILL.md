---
name: tk-pr-respond
description: "[user/auto] Resolve one pull request's selected feedback or supported GitHub Actions failures through one approved plan, fresh-worker units, acceptance verification, and bounded publication."
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Respond to one pull request

Start only via `/tk-pr-respond`, `$tk-pr-respond`, the host skill picker, or a
fresh exact-PR handoff from active `tk-pr-sweep`. Never activate for generic
review, implementation, triage, continuation, or more than one PR.

Respond owns one PR's feedback/supported-CI plan, fresh-worker execution,
acceptance verification, and bounded push/reply/resolve/re-review/summary. It is
a controller: **never author product, test, or configuration changes**. Every
primary or corrective edit goes to a fresh worker with one bounded resolution
unit. Mechanical staging and one verified commit per unit may be controller-owned
only after required verification and gap closure pass. No usable worker means
`Blocked`, never direct fallback.

## Authority and ledger

Standalone Respond atomically replaces and rereads `.tigerkit/pr-respond.md`.
Record the PR/repository/head/refspec, current finding IDs, R/AC, scope and
exclusions, controller-resolved assumptions and basis, units/waves, verification,
approved publication actions, worker/correction/commit evidence, thread actions,
and final observed PR state. Store no secret, transcript, or full log.

When invoked under Sweep, write **no** `pr-respond.md`, child ledger, or
other Markdown lifecycle file. Return compact evidence to the owning
`.tigerkit/pr-sweep.md`. Artifact presence grants no authority.

## Lifecycle

```text
Prepare -> Execute -> Close gaps -> Finalize
```

### Prepare

1. Fresh-read exactly one open PR: repository, authenticated user, author,
   branch/base, head ref/SHA, draft state, checks, reviews, comments, threads,
   requested reviewers, and exact push refspec. Complete pagination. Missing,
   mixed-PR, author/login-mismatched, or ambiguous identity is `Blocked` before
   mutation.
2. Suppress superseded iterations and classify each current finding or supported
   GitHub Actions failure as `apply | reply | defer`. Preserve exact IDs, bounded
   quote/summary, requested outcome, R/AC, scope, exclusions, reply draft, and
   verification. External/unknown-provider CI is report-only; queued, cancelled,
   flaky, infrastructure, or inaccessible failures never justify code changes.
3. Resolve ordinary reversible ambiguity from evidence. Record every material
   assumption, its basis, and a behavior-changing alternative. Use `tk-grill-me`
   only when a user-owned decision prevents a safe executable plan.
4. Derive independently verifiable resolution units and dependency waves.
   Serialize coupled or uncertain work. Concurrent units require host-provided
   isolated checkouts/worktrees and proven independence; do not build a scheduler.
5. Select the least-sufficient worker tier per dispatch: `cheapest` for mechanical
   local work, `standard` for ordinary multi-file/debugging work, `strongest` for
   design-heavy, unknown-cause, broad-reasoning, or security/data-sensitive work,
   and `host-default` when per-spawn choice is unavailable. Never expose model
   configuration or provider/model mappings.
6. Prepare one compact approval surface containing goal/PR/head, included and
   excluded findings, apply/reply/defer decisions, R/AC, units/waves,
   verification, exact bounded `push`/reply/resolve/re-review/summary actions,
   risks, and assumptions/ambiguities. This is the only normal approval.

Emit one `🙋 respond · 응답 필요`, show exactly one `👍 Recommendation:`, and ask
the approval question. Before approval perform no worker dispatch, commit, or
remote write. Approval authorizes only the displayed
snapshot and Respond's existing bounded authority; it also authorizes the listed
publication, so **never ask a second publication question**.

`--ci` skips the interactive checkpoint only when its explicit invocation or
parent Sweep handoff already supplies an equivalent exact PR/head/finding/route,
verification, and publication bound. A Sweep `test-only` route permits only the
repository's existing test layout and forbids production, configuration,
dependency/lockfile, security/data/performance, and weakened-assertion changes.
Out-of-bound work is `Blocked` before worker dispatch.

Material PR head/thread/check/identity/refspec, source, scope, verifier, or
irreversible-decision drift invalidates approval and returns to Prepare. An
unchanged plan never receives another routine checkpoint.

### Execute

For each dependency wave, dispatch a fresh worker per unit with only its ID/goal,
exact PR finding and R/AC IDs, scope/exclusions, relevant paths, verification, and
Git ownership facts. The worker inspects current evidence, implements only its
unit, runs focused checks, performs one bounded behavior-preserving simplify/reuse
pass, and returns changed paths, candidate evidence, and unresolved items.

Use this invariant:

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

Required verifiers run on the final uncommitted candidate. A gap fix always uses a
new worker. Supply missing context before escalation; demonstrated reasoning
failure gets a fresh worker one tier higher. Prefer at most three corrective
rounds and never retry unchanged failure indefinitely. Stage only proven owned
paths and preserve pre-existing user changes.

An integration conflict disproves independence: stop concurrent integration and
serialize or return to Prepare. Workers never invent a semantic merge.

For repository-caused GitHub Actions, one fresh failure read and fix is one cycle.
After an exact push, promote only the freshly observed just-pushed head and rerun
all relevant checks. Stop after three corrective cycles. Never invoke interactive
CI workflows as automatic children.

### Close gaps

Classify every approved finding/R/AC as `satisfied`, `missing`, `partial`, or
`unverifiable`. Check only approved scope/exclusions, skipped units, externally
visible behavior, required verifier evidence, commit ancestry/ownership, and
freshness. This is not general code review. If the verdict cannot be established,
use at most one stronger fresh non-mutating reviewer with the same narrow brief;
required-but-unavailable independent review is `Unverifiable`. Corrections still
go to fresh workers.

### Finalize and publish

After all selected units close their gaps, fresh-read repository identity, local
`HEAD`, PR head/ref/open state, checks, and threads. Publish only unchanged,
already-approved actions in this order:

1. exact branch push when a verified commit exists;
2. exact reply per current finding;
3. resolve only a freshly verified thread after its reply succeeds;
4. fresh review/thread/check/mergeability read;
5. conditional human re-review, excluding author, authenticated user, bots, and
   still-valid approvers;
6. at most one PR summary.

Under Sweep, consume its one-summary budget or return the draft when already
consumed. Every generated external comment ends exactly
`_🤖 본 코멘트는 AI가 작성했습니다._`. A failed reply leaves its thread open.
Deferred, failed, partial, or unverifiable findings stay open. Never force-push,
merge, close unrelated threads, request bot review, mark a draft ready, tag,
release, or publish a release.

Fresh-read the final PR. Partial remote writes are `Fail`; missing required
evidence is `Unverifiable`; authority/identity/freshness conflict is `Blocked`;
complete approved scope is `Pass`. A nested run returns only compact evidence to
Sweep. Standalone output begins `## PR respond`, includes one exact
`Status: Pass | Fail | Blocked | Unverifiable | Pending` line, omits worker
receipts and raw logs, and uses the user's language while preserving canonical
IDs, statuses, commands, paths, and exact literals.
