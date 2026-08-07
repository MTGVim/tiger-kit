---
name: tk-drive
description: "[user] Drive an explicit product-change source through one prepared approval, fresh-worker execution, acceptance-gap closure, verified unit commits, and finalization."
disable-model-invocation: true
argument-hint: "<source, request, issue, or approved active run>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user explicitly selects `/tk-drive`, `$tk-drive`, or the host
skill picker with a source. A no-source re-invocation resumes one approved or
pending run in the same conversation only after current source, ledger, Git, and
repository evidence identify it unambiguously. Ordinary requests, artifacts, and
new sessions do not start or resume Drive.

## Authority and invariant

One approved plan authorizes preparation, fresh-worker mutation, required verification,
one verified current-branch commit per approved unit, up to three corrective rounds,
aggregate verification, and finalization. It excludes push, PR, merge, tag, release,
publish, and history rewriting.

Drive is a controller: **it never authors product, test, or configuration
changes**. Every primary and corrective mutation goes to a fresh worker with one
bounded unit. Mechanical Git bookkeeping may be controller-owned only after the
final candidate passes. If the host cannot dispatch a usable worker, stop
`Blocked`; never fall back to controller edits. Workers may not orchestrate or
invoke another user-owned TigerKit workflow.

## Lifecycle

```text
Prepare -> Execute -> Close gaps -> Finalize
```

Drive owns this lifecycle; child receipts are internal and never require `continue`,
`/clear`, model switching, or a second invocation. After a host/process boundary,
derive the next action from fresh evidence, not a cursor or lifecycle claim.

## Prepare

1. Read the complete source and applicable repository instructions. Record branch,
   baseline `HEAD`, worktree, pre-existing dirty paths, and at most seven relevant
   durable prior-art items.
2. Resolve reversible ambiguity from evidence and safe defaults. Record every
   material controller choice, basis, and behavior-changing alternative. Invoke
   `tk-grill-me` only when a user-owned decision prevents a safe executable plan;
   use `tk-prototype` only when a bounded comparison can close that decision.
3. Write Ready requirements and acceptance criteria with source anchors, scope,
   exclusions, frozen user-visible literals, and verification obligations.
4. Derive `1..N` independently verifiable units, their dependency graph and waves.
   Serialize coupled or uncertain units. Parallelize only proven-independent units
   when the host already provides isolated checkouts/worktrees; do not build a
   scheduler or let workers share a mutable worktree concurrently.
5. Classify tests/checks and browser verification. For browser-visible AC, plan
   exact scenarios, target, non-sensitive auth mode, prerequisites, and limitations;
   otherwise record `not-required`. Unavailable required headless auth is
   `Unverifiable` before mutation.
6. Select the least-sufficient tier per dispatch using
   [worker-dispatch.md](references/worker-dispatch.md).
7. Atomically replace and reread `.tigerkit/drive.md` using
   [ledger.md](references/ledger.md), then present one compact approval surface:
   goal/source, included/excluded scope, R/AC, units/waves, verification, risks,
   assumptions/ambiguities, and any bounded external actions.

The approval question is the action surface: emit one `🙋 drive · 응답 필요` line,
show exactly one `👍 Recommendation:`, and do not add a redundant `Next:` line.
Approval covers only the displayed snapshot. Material source, scope, branch/head,
remote-state, verifier-prerequisite, or irreversible-decision drift invalidates it
and returns to Prepare; unchanged plans never receive a second routine approval.

## Execute

For each dependency wave, dispatch a fresh worker per unit with only its ID/goal,
exact R/AC, scope/exclusions, relevant paths, verification obligations, and
branch/head/diff ownership. The worker inspects current evidence, implements only
that unit, runs focused checks, performs one bounded behavior-preserving
simplify/reuse pass, and returns changed paths, candidate evidence, and unresolved
items. Use this invariant:

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

Required verifiers run against the final candidate before commit. Stage only
proven owned paths and preserve pre-existing user changes. On isolated gaps,
dispatch a fresh corrective worker and rerun affected obligations; prefer at most
three rounds. Missing context is supplied without a tier upgrade. Demonstrated
reasoning failure gets one fresh worker at the next tier. Repeated unchanged,
unisolated, conflicting, or scope-expanding failure stops mutation.

An integration conflict disproves independence. Serialize or re-prepare affected
units; workers never invent semantic merges. Drive owns isolation, integration
order, stale-base/conflict detection, and cleanup.

## Close gaps

For every approved R/AC classify observed evidence as `satisfied`, `missing`,
`partial`, or `unverifiable`. Check only acceptance-relevant scope/exclusions,
units, verifiers, externally visible behavior, commit/ancestry, dirty-path
ownership, and evidence freshness. This is not a general code review.

When evidence cannot support a confident verdict, dispatch at most one stronger
fresh non-mutating reviewer with the same narrow R/AC brief. Use an available
built-in or third-party reviewer only when user/repository policy requires
independent review. Required-but-unavailable review is `Unverifiable`. Every fix
still goes to a fresh corrective worker.

## Finalize

After all verified unit commits, rerun aggregate R/AC traceability, repository
checks, ancestry, exclusions, and freshness. Update `.tigerkit/drive.md` with unit
commits, verifier/gap evidence, corrective rounds, aggregate result, and recovery
facts. On non-success, freeze mutation and follow
[non-success-finalization.md](references/non-success-finalization.md).

On success, emit one concise behavior result, useful unit commits, one to four
aggregate verification bullets, and exactly `Status: Pass`. Do not claim broad
review coverage; suggest broader review once only when useful.

### 🔴 HARD GATE · terminal user summary

Only Drive emits the active run's terminal response. Start directly with the
canonical result sentence or heading; omit receipts, phase-success tokens,
provenance blocks, raw logs, worker tiers, and progress markers. Use one exact
`Status: Pass | Fail | Blocked | Unverifiable` line. Add `Next:` only when a
concrete user action remains.

### 🔴 HARD GATE · response language

Use the user's latest explicit language, otherwise the current message language,
for free-form user-facing prose. Preserve canonical statuses, IDs, commands,
paths, code, and source literals. Progress is limited to meaningful `🤹`
orchestration boundaries, `🙋` user input, and `⏳` external waits; terminal
responses contain none.

## User decision questions

Ask one self-contained question only when a user-owned decision blocks safe
planning. Show two or three mutually exclusive options and exactly one
`(Recommended)` or `(추천)` after `👍 Recommendation:`. Render it in chat, keep
the run pending, and perform no downstream mutation until answered.
