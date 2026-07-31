# ADR 0001: Implementation quality gates and optimistic reflection

- Status: Superseded by ADR 0003
- Date: 2026-07-29
- Candidate release: v20.2.0
- Source: MTGVim/tiger-kit issue #200

## Context

TigerKit v20.1.7 already had explicit phase ownership, verified per-ticket
commits, aggregate verification, decision-first output, and compact receipts.
It did not make the pre-mutation repository-fit decision explicit, did not
guarantee a post-GREEN simplification pass, and deliberately stopped before
automatic reflection.

This left three recurring quality gaps:

1. Correct changes could still create parallel helpers, premature shared
   abstractions, pass-through wrappers, or ownership drift.
2. The red/green loop did not guarantee one behavior-preserving structural
   cleanup before review.
3. Verified repository-specific lessons did not feed back into a safe rule
   target at the end of a successful drive.

The v20.1.7 concise-output direction also over-compressed compound results.
`Outcome` is useful as a decision-first heading, but a completion sentence
cannot replace the behavior changes, verified results, dispositions, or next
actions that users need to reconstruct an outcome.

## Decision

### Keep existing owners

No new review, simplify, reflection-orchestration, or ledger skill is added.
`tk-implement` owns unit quality gates, `tk-drive` owns aggregate sequencing,
and `tk-reflect` owns reusable-candidate classification and presentation.
Detailed procedures remain in skill-local references and repo-local scratch.

### Decide repository fit before mutation

Every `tk-implement` unit inspects relevant owners, helpers, direct call sites,
and tests before writing. It chooses one of:

- reuse an existing owner or helper;
- extend an existing owner;
- keep behavior local to the current unit;
- introduce a shared abstraction only when repository conventions, multiple
  real consumers, or a stable cross-cutting invariant provide evidence.

A single consumer is not evidence for a new shared abstraction.

### Simplify once after initial GREEN

After the initial behavior is GREEN, the current agent runs exactly one
behavior-preserving simplify pass before final verification. The pass removes
unnecessary indirection, duplication, wrappers, speculative flexibility, and
ownership drift only within the unit and its direct call sites. If it changes
the candidate, focused verification reruns. A clean candidate records `no-op`;
there is no recursive cleanup or reviewer loop.

Standards review and Spec review remain distinct downstream gates. Simplify is
proactive candidate improvement; review is an independent verdict.

### Preserve bounded implementation evidence

`.tigerkit/implementation.md` records task identity, fit evidence, simplify
disposition, verification, review, commit, and remaining risk. It is
repo/worktree-local scratch, replaced atomically, bounded, and never causes a
consumer `.gitignore` edit.

### Reflect exactly once after product success

`tk-drive` freezes the product verification HEAD only after aggregate product
verification passes. It then invokes one `tk-reflect` tail with this envelope:

```text
Mode: drive-optimistic
Success state: Pass
Outstanding transition: final receipt
Return to: tk-drive
```

Missing or mismatched authority cannot produce a successful tail. Non-Pass
product states never enter optimistic reflection. A successful echo returns
control to drive for the final receipt, and that receipt cannot start another
reflection. This is the fixed point.

### Restrict optimistic mutation

Automatic application is limited to an existing repository-rule target with
high confidence, at least two independent evidence IDs, no counterexample,
stable ownership, and no better prevention owner such as a test, linter,
typecheck, CI check, or existing skill.

The tail never creates or mutates a skill, user/global rule, persistent memory,
vendor/generated file, or a new ignored/local target.

- An eligible tracked rule creates one separate reflection commit. The receipt
  reports the exact `git revert <sha>` rollback.
- An eligible pre-existing ignored/untracked local rule preserves a hash-bound
  before-image under `.tigerkit/reflect-backup/`, applies locally, and creates
  no commit or new local rule file.
- A skill candidate remains a promotion-ready report packet. Only `tk-learn`
  may later create or semantically update a skill under its own approval gate.

Any failed application must restore the verified pre-reflection state.
Verified restoration preserves the product Pass and reports reflection
failure. Indeterminate or failed restoration makes the overall drive
`Blocked` or `Unverifiable`.

### Separate product and final HEADs

The product verification HEAD remains the evidence anchor. A tracked reflection
commit may advance the final HEAD, but it does not recursively invalidate or
rerun product verification. A local ignored-rule application leaves Git HEAD
unchanged. Final receipts name both anchors when they differ.

### Use cardinality-aware result summaries

All 14 canonical skills keep decision-first ordering and apply bounded output:

- one result: one to three short paragraphs or bullets;
- two to seven results: compact bullets or a readable table;
- eight or more: the top five to seven plus the owning artifact, ledger, or
  evidence paths.

Skill-specific budgets may be narrower. Budgets are ceilings, not padding
quotas. Empty risks, zero candidates, default no-op sections, raw logs, full
diffs, and repeated evidence remain omitted. Receipt records status and
provenance; it never substitutes for result rows.

For `tk-reflect`, every non-no-op result retains the readable
`ID | Candidate | Action | Target | Why` Disposition table. `Action` and `Why`
must tell a person what happens next and why; RF codes alone are not a result.

## Alternatives considered

### Add separate review or simplify skills

Rejected. These gates have no independent user-facing artifact or invocation
boundary and would fragment one implementation unit across micro-skills.

### Require an independent reviewer for every unit

Rejected. It adds cost and coordination without evidence of universal benefit.
The existing large/high-risk conditional reviewer boundary remains sufficient.

### Auto-promote skill candidates

Rejected. Skill mutation has a broader distribution and compatibility boundary
than a repository rule and requires `tk-learn` evidence, evals, and approval.

### Store a permanent lessons database

Rejected. Repo-local bounded ledgers provide traceability without inventing
global state, migration, archival, or cleanup semantics.

### Keep reflection fully manual

Rejected for proven repository rules after successful drive work. The narrow
eligibility and rollback model safely closes the feedback loop while keeping
all broader candidates report-only.

### Keep strict one-line results

Rejected. It optimizes token count at the cost of user comprehension and makes
Receipt carry prose it should only index.

## Consequences

Positive consequences:

- implementation structure is decided and evidenced before mutation;
- one cleanup opportunity is guaranteed without recursive review;
- high-confidence repository lessons can prevent recurrence immediately;
- product verification remains stable across a separate reflection commit;
- compound results are readable while evidence stays bounded in artifacts;
- canonical skill count, invocation paths, and distribution remain unchanged.

Costs and risks:

- skills and evals carry more explicit output and rollback contracts;
- optimistic eligibility is intentionally conservative and will often no-op;
- tracked reflection may add one commit after product commits;
- local-rule rollback depends on verified ownership, before-image, and target
  stability, so any uncertainty must stop mutation.

## Verification obligations

Changes to this decision require regression coverage for:

- reuse/extend/local/shared fit selection;
- exactly-one simplify ordering and behavior preservation;
- post-Pass-only reflection, exact transition echo, and no second tail;
- tracked and local rollback, restoration failure, and target drift;
- product versus final HEAD reporting;
- skill-candidate report-only behavior;
- bounded result cardinality and nonduplicative receipts;
- the full readable `tk-reflect` Disposition table.

Local skill/link validation, projection sync, Python tests, catalog discovery,
API-free eval dry-runs, and clean Claude Code/Codex/Hermes Agent smoke installs
remain the release verification path.

## Supersession

A later decision supersedes this ADR only by adding a new ADR that:

1. names ADR 0001 as superseded in whole or in a precise section;
2. explains the new ownership, mutation, rollback, fixed-point, and output
   boundaries;
3. updates affected skill contracts, behavior evals, migration notes, and
   validation evidence together.

Editing this file in place for a semantic reversal is not sufficient. Minor
clarifications that do not change those boundaries may amend this ADR with a
dated note.
