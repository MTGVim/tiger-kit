# Prepared-drive invariants

These gates apply only after explicit `tk-drive` selection without a source.
Preparation semantics belong to `tk-prep`; drive consumes one sealed manifest
and never reconstructs preparation from conversation.

The phase-owner allowlist is `tk-implement | tk-reflect (drive-optimistic tail
only)`. The conditional support allowlist is
`tk-browser-verify | tk-merge-conflict`. Drive does not invoke
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, or `tk-prototype`.

Prepared drive may invoke only `tk-implement` and the single allowed
`tk-reflect` tail.
It must not invoke `tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, or
`tk-prototype` during initial or corrective execution.

## Prepared input and authority

The only start artifact is worktree-local `.tigerkit/prep.md` with
`schema_version: tigerkit.prep/v1` and `status: ready`. Raw source text,
another path, copied JSON, an in-memory header, conversation history, a
terminal manifest, or an active manifest grants no authority.

Preparation binds task ID and anchors, repository root, worktree, branch, base
HEAD, source, dirty inventory, instructions, spec, tickets/no-ticket mode, and
verification profile. Drive rechecks every binding with
`scripts/prep_state.py claim`. It must pass current canonical inventories, not
values copied back from the header merely to satisfy equality.

The script uses the `.tigerkit` directory lock, strict parsing, canonical
digests, and atomic mode-0600 replacement. A successful claim changes exactly
`ready → active`, adds claim identity and `claimed_at`, preserves prep/task
identity and all digests, and strictly rereads while locked. A freshness
failure changes a valid Ready manifest to `invalid`; malformed or missing
state remains untouched. Two claim attempts cannot both succeed.

No product mutation, child handoff, or implementation ledger transition may
precede a successful claim. Record the returned `prep_id`, `claim_id`, and
active-state reread in the implementation ledger.

## Frozen execution

Read `.tigerkit/spec.md` and `.tigerkit/tickets.md` only through references
validated by the manifest. A no-ticket prep is one frozen unit. Ticket mode
uses the exact prepared order and dependencies. Keep at most one unit
`in_progress`; each prepared unit is handed to `tk-implement` at most once
before any corrective cycle.

Drive may reconcile repository evidence needed to execute frozen R/AC, but
cannot:

- add or remove R/AC, units, tickets, source literals, or profile obligations;
- seek or incorporate a new product decision;
- reinterpret dirty ownership or task identity;
- rerun preparation owners;
- silently accept drift because the implementation seems safe.

Any such need makes the run `invalid | Blocked` and requires a new
`/tk-prep <source>`.

## Handoff envelope

Every implementation handoff records prep and claim IDs, task identity,
prepared unit/ticket ID, stable R/AC, branch, initial/current HEAD, dirty
ownership, source UI inventory, and material verification obligations. Before
invocation, drive records the native `Success state` and exactly one
`Outstanding transition`: the next prepared unit, aggregate verification,
next corrective cycle, reflection, or finalization.

An active-drive owner must echo `Return to: tk-drive` and the exact
`Outstanding transition`. Drive consumes only:

- `tk-implement` `Status: Pass` with the expected unit/ticket ID and commit;
- `tk-reflect` `Status: Pass` with the expected drive-optimistic tail echo.

When both `TK_DRIVE_EVENT_RECORDER` and `TK_DRIVE_EVENT_LOG` are present in
an evaluation-owned environment, drive invokes the recorder immediately
before each allowed phase with `phase_invocation <phase>` and immediately
after its matching successful receipt with
`phase_receipt <phase> Pass <Outstanding transition>`. A recorder failure is
`Unverifiable`; drive never fabricates, delays, or backfills an event and does
not record outside that conditional evaluation environment.

Unavailable skills, `Pending | Blocked | Fail | Unverifiable`, mismatched IDs,
missing commits, ancestry drift, or receipt drift stop the transition. A child
cannot add scope or route a decision owner; it returns the native non-success
state and drive finalizes or preserves state according to evidence.

## Receipt liveness

Consuming a success receipt creates transition debt; it is not completion. In
the same active turn, drive must execute exactly one recorded next action:

1. the next prepared implementation unit;
2. aggregate verification;
3. one numbered corrective unit within the frozen R/AC;
4. the single reflection tail;
5. terminal manifest finalization; or
6. an evidence-supported non-success terminal result.

Progress commentary and receipt summaries do not discharge transition debt.
No user-facing text occurs between a matching success receipt and its recorded
transition.

Before returning control, verify that every consumed receipt has one recorded
outgoing transition. A receipt with no executable transition is `Blocked`;
never ask the user to invoke drive again to continue the same run.
Immediately before emitting terminal `---`, run the transition-debt check.
Terminal output is prohibited while any consumed successful receipt still has
an unexecuted `Outstanding transition`; execute the recorded transition in the
same active turn or return the one evidence-supported non-success state.

The closed stop set is: raw/missing input, claim or identity failure, receipt
drift, explicit user stop, inaccessible required evidence,
`Pending | Blocked | Fail | Unverifiable`, corrective exhaustion, state-write
failure, or the final terminal summary.

## Implementation owner

`tk-implement` alone owns direct/delegated strategy, TDD/no-TDD, production
tests, focused and affected verification, ticket-level Standards/Spec review,
staging, and one current-branch unit commit. It receives the frozen
verification profile and owns the exact regression, compatibility,
side-effect/recovery, browser, and bounded review methods required for its
unit.

Before the next handoff, drive verifies the receipt's prepared unit ID, commit
SHA, branch, ancestry, R/AC evidence, and dirty ownership. It never batches
prepared units or creates a separate drive commit.

## Aggregate verification

After the complete initial unit set:

- verify every frozen R/AC maps to a matching unit receipt and commit;
- verify ordered commit ancestry and current HEAD;
- reconcile source UI literals and every material profile obligation;
- inspect cross-unit behavior and cumulative side effects;
- run the broadest relevant executable tests, build, integration, package,
  and browser verification once;
- classify each failure as `change-related | pre-existing | environment |
  unverifiable`.

Freeze the successful product verification HEAD before reflection. A later tracked
reflection commit changes final HEAD but not product evidence.

## Corrective cycles

Initial implementation is not a corrective cycle. Only an isolated
change-related defect inside frozen R/AC can start a correction. Record cycle
`1`, `2`, or `3`, invoke `tk-implement` for one independently verifiable
corrective unit, then rerun affected and aggregate verification.

The initial implementation consumes zero corrective cycles.
At most three post-initial corrective cycles are permitted inside frozen R/AC;
a fourth cycle or any scope, ticket, or decision expansion stops mutation.

Do not create a corrective ticket, add scope, ask a product decision, amend or
squash a verified commit, or reset the cycle count after a different symptom.
A fourth cycle, repeated failure, unisolated cause, new R/AC, new ticket, or
new decision ends product mutation in the one evidence-supported terminal
state.

## Reflection tail

After aggregate product `Pass`, hand off exactly once to `tk-reflect`:

```text
Mode: drive-optimistic
Success state: Pass
Outstanding transition: final receipt
Return to: tk-drive
```

The handoff cites prep/claim IDs, product verification HEAD, implementation ledger,
spec/tickets, ordered commits, aggregate evidence, branch, initial HEAD, and
dirty ownership. A no-op is successful. A verified-restored reflection failure
may preserve product `Pass`, but terminal status and remaining risk must record
the reflection outcome. Unrestored or indeterminate state is
`Blocked | Unverifiable`.

The `final receipt` transition begins by finalizing and strictly rereading the
manifest; no user-facing text may precede that state mutation.

## Terminal state

The same claim owner calls:

`prep_state.py finalize .tigerkit/prep.md --claim-id <id> --status <completed|invalid|failed> --finished-at <UTC>`

Use `completed` only when the prepared product and required reflection tail
complete. Use `invalid` for identity, scope, or preparation invalidation and
`failed` for verified execution failure. If terminal evidence is inaccessible,
leave `active` rather than fabricate a transition and report exact recovery.

Strictly reread terminal state before chat output. A terminal manifest remains
at the same path for diagnosis and cannot authorize another run. Do not
archive, rename, delete, migrate, or create a pointer.

## Final summary

Report behavior, unit-to-commit mapping when useful, aggregate verification,
reflection only when meaningful, remaining risks, and the one terminal status.
The artifact owns prep/claim provenance; the implementation ledger owns
detailed receipts. Do not copy either into chat or automatically push, open a
PR, tag, release, publish, or begin another preparation.
