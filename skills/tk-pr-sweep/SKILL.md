---
name: tk-pr-sweep
description: "[user] Prepare and execute one approved multi-PR maintenance batch, or report deterministic triage read-only with --report."
argument-hint: "[--report] [--repo owner/name]..."
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Sweep pull requests

Start only via `/tk-pr-sweep`, `$tk-pr-sweep`, or the host skill picker, never
generic PR status, one-PR work, release, or continuation. Sweep is the multi-PR
orchestrator; one-PR Respond and Rebase never invoke each other.

## Deterministic triage and report mode

Run package-local `scripts/triage.mjs` directly for initial, per-route, and final
classification. It resolves identity and explicit `--repo` targets or
`$XDG_CONFIG_HOME/tigerkit/pr-triage.json`, bootstrapping current origin when
missing. Retry once when API failure prevents classification; never merge partial
snapshots or infer approval from missing checks.

`$tk-pr-sweep --report` runs triage once, groups `Act now`, `Review requests`, and
`Waiting` with clickable evidence and one next action, then returns. It asks no
approval and creates no ledger/worktree/commit/route/GitHub write; config bootstrap
is its only permitted state write.

## Authority and invariant

Interactive Sweep owns one plan/approval, `.tigerkit/pr-sweep.md`, isolation,
frozen routes, one summary per PR, aggregate verification, and finalization. It
never authors product changes; nested `tk-pr-respond --ci` uses fresh workers for
all primary/corrective edits. Sweep cannot broaden child authority, merge, close,
create PRs, tag, release, or publish.

```text
Prepare -> Execute -> Close gaps -> Finalize
```

## Prepare

1. Run fresh deterministic triage; ignore supplied queues, cached reports, stale
   ledgers, and cursors. Resolve identity, PR/base/head state, categories,
   checks/providers, reviews, comments, threads, and requested reviewers.
2. Classify every row as actionable, held, or report-only. Use the closed router:

   | Fresh evidence | Bounded route |
   | --- | --- |
   | exact maintenance conflict with same-repository base/head and clean ownership | `tk-pr-rebase --ci` |
   | repository-caused GitHub Actions failure | `tk-pr-respond --ci` |
   | current actionable feedback/reply | `tk-pr-respond --ci` |
   | external/unknown/unverifiable checks, review request, draft, waiting | report-only |

   Hold rows without safe ownership/refspec/scope/route. Product fixes may be
   actionable only with exact scope and a fresh-worker verification route; do not
   retain a routine second “high-risk approval.”
3. Record each reversible material assumption, basis, and behavior-changing
   alternative. Use `tk-grill-me` only when a user-owned decision blocks planning.
4. Freeze repository/PR/head/category/route/scope/risk/verification/actions and
   exclusions. Derive waves; concurrency requires proven independence plus
   host-provided isolation. Serialize uncertainty and build no scheduler.
5. Atomically replace and reread `.tigerkit/pr-sweep.md`, then show one compact
   `## PR sweep plan` containing every actionable, held, and report-only row,
   assumptions/ambiguities, route waves, verification, risks, worktree ownership,
   bounded remote actions, and `No remote changes yet`.

Emit one `🙋 sweep > plan · 응답 필요`, show exactly one
`👍 Recommendation:`, and ask the approval question. Before approval create no
worktree/commit and perform no remote write. The
approval supplies the exact bounded authority to nested Respond/Rebase; they do
not ask again. Material identity, PR head/state/category/scope/route, verifier, or
irreversible-decision drift invalidates the affected plan and returns to Prepare.
Unchanged rows never receive a second routine checkpoint.

## Execute

Process frozen waves. Before each row, rerun triage and prove identity, PR state,
head/category/provider, refspec, threads, and checks. Proven-complete work is
`Skipped: already applied` without child/worktree. External drift returns to
Prepare; sweep-owned verified heads continue only within the approved bound.

Fetch and prove the exact remote head before mutation. Reuse only an exact clean
owned worktree; otherwise prefer Orca and fall back to Git only when unavailable.
Run frozen/immutable setup once; share package cache only, never dependencies.

Invoke exactly one owner per current category. Pass the frozen PR/head/route,
finding IDs, R/AC, scope/exclusions, verification, worktree facts, ledger owner
`tk-pr-sweep`, and summary budget. Nested Respond, Rebase, workers, reviewers, and
verifiers write no child Markdown ledger; they return compact evidence to
`.tigerkit/pr-sweep.md`. Controller and
nested Respond never author product edits; corrections use fresh workers and the
automatic `cheapest | standard | strongest | host-default` tier policy.

After each child result, fresh-triage that exact PR and continue the frozen queue
without asking `continue`. Preserve prompt-local bounds: one rebase per exact
base/head pair, at most three GitHub Actions corrective cycles, and one feedback
response per fresh head plus at most two sweep-owned follow-up heads. Repeated
unchanged or exhausted work becomes `follow-up-queued`, not another mutation.
Post-push `IN_PROGRESS` gets at most three fresh rechecks; if still incomplete,
record `waiting`, retain the worktree, and continue independent rows. Emit
`⏳ sweep · 대기` only when the returned state actually requires an external
check or re-review wait.

Stop later mutation only for shared safety failure such as unresolved identity,
corrupt repository evidence, or unprovable worktree ownership. PR-local `Fail`,
`Blocked`, or `Unverifiable` does not stop proven-independent rows. Remove only a
sweep-created clean worktree whose complete route freshly passes; retain and
report every other worktree.

## Close acceptance gaps and Finalize

Classify each approved row/R/AC `satisfied | missing | partial | unverifiable`.
Check only scope, routes, tests/checks, publication, ancestry/ownership, and
freshness—not general review. Uncertain AC evidence may use one stronger fresh
non-mutating reviewer; every fix still uses a fresh Respond worker.

After every initial row is accounted for, run one final deterministic triage
without growing an unbounded queue. An unexpected newly actionable supported item
is `Blocked`; `waiting` or `follow-up-queued` is `Pending`; otherwise aggregate
`Fail > Blocked > Unverifiable > Pending > Pass`. Report-only unsupported rows do
not become supported successes or failures.

Update only `.tigerkit/pr-sweep.md` with approved snapshot, route/worker/verifier/
commit evidence, consumed bounds, summary budget, worktree disposition, final
triage, gap verdicts, and recovery facts. Store no credentials, transcript, full
logs, or resume cursor. Terminal output begins `## PR sweep`, shows every processed
PR plus remaining report-only/held items, uses one exact
`Status: Pass | Fail | Blocked | Unverifiable | Pending` line, omits child receipts,
and follows the user's language while preserving canonical IDs, statuses,
commands, paths, and exact literals.
