# Unreleased decision-phase orchestration

The next release keeps all 12 canonical names and the 1 user-invoked /
11 hybrid distribution, but swaps the top-level invocation owner:

```text
user-invoked: tk-drive
hybrid:       the other 11 canonical skills
```

Explicit standalone `tk-grill-me` remains valid. Its automatic positives are
limited to an explicit active-drive decision handoff and the direct answer to
its own pending question. Ordinary ambiguity, artifact presence, generic
continuation, or merely having an active drive does not activate it.

Drive conditionally invokes grill only when a user-owned decision prevents a
Ready spec. A decision-related spec or ticket receipt returns
`User decision: required` to drive; after grill confirms new Decisions, drive
re-runs `tk-to-spec` to Ready before rederiving tickets. The same blocker after
confirmation stops `Blocked`. Spec, tickets, and implementation never invoke
grill or one another.

No `tk-prep` skill, shared runtime contract, migration shim, or new scratch
artifact is added. Existing explicit skill names remain valid; automation that
inspects invocation metadata must update for the swapped user/hybrid kinds.

# TigerKit 20.1.3 Behavior Updates

TigerKit 20.1.3 preserves the 12 canonical skill names, explicit invocation
paths, and Agent Skills distribution for Claude Code, Codex, and Hermes Agent.
It refines the invocation mix from 2 user-invoked / 10 hybrid to 1 user-invoked
/ 11 hybrid while keeping direct `tk-implement` selection valid, and composes
the existing workflow through explicit phase owners without requiring users to
change installation or explicit commands.

## Install

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

Claude Code and Hermes Agent use `/tk-*`; Codex uses `$tk-*` or its picker.

## Invocation changes

```text
user-invoked: tk-grill-me
hybrid:       the other 11 canonical skills
```

`tk-implement` changes from user-invoked to hybrid. Explicit
`/tk-implement`, `$tk-implement`, and picker selection remain valid. Its only
automatic positive is an explicit implementation handoff from active
`tk-drive` that provides one ticket or no-ticket unit and its R/AC. An ordinary
implementation request, artifact presence, generic continuation, or merely
having an active drive does not activate it.

`tk-to-spec` and `tk-to-tickets` retain their standalone automatic triggers and
also accept explicit phase handoffs from active drive. A vague statement that
drive is active is not a handoff.

## Phase ownership

TigerKit 20.1.3 assigns one semantic owner per phase:

```text
spec creation and Ready gate          → tk-to-spec
vertical ticket decomposition         → tk-to-tickets
one unit's implementation/test/review → tk-implement
phase order and aggregate verification → tk-drive
```

`tk-drive` explicitly invokes these owners and consumes their native receipts.
It does not inline a failed or unavailable phase, and a phase owner does not
take over drive-wide orchestration or final reporting.

Standalone phase invocation remains supported. You do not need drive to write
a spec, decompose tickets, or implement one selected unit.

## Commit changes

Earlier TigerKit 20 drive implementations created one final commit. TigerKit
20.1.3 uses:

```text
one ticket = one tk-implement invocation = one commit
one no-ticket single slice = one tk-implement invocation = one commit
```

Standalone `tk-implement` refuses multi-ticket batching before mutation and
asks for one selected ticket or recommends `$tk-drive`.

After all unit commits, drive checks ordered ancestry, complete R/AC coverage,
and cross-ticket interaction, then runs the broadest executable relevant
verification once. It does not create another final commit or repeat each
ticket's line-level Standards/Spec review.

One isolated final change-related regression may create one corrective ticket
and one corrective commit followed by one recheck. Drive never automatically
amends, squashes, rolls back, force-pushes, or otherwise rewrites verified
commits.

## Test and coverage changes

TDD remains conditional, but a durable automated test is now a completion
condition for production behavior. A bug or regression with a meaningful
public seam must observe a failing regression test before the fix and green
after it. New behavior may use no-TDD but still needs a durable public-behavior
test before commit.

Existing repository coverage commands and thresholds run as-is. If no coverage
tooling exists, TigerKit reports `coverage: unavailable`; it does not install
or invent dependencies, instrumentation, thresholds, or percentages.

When production behavior has no meaningful test seam, commit remains blocked
until the user explicitly approves a named exception and deterministic
alternative verification. Copy, documentation, pure configuration, and
mechanical changes may omit a new test with a recorded reason, but still need
relevant verification.

## Contract language

The operational bodies and references for `tk-drive`, `tk-to-spec`,
`tk-to-tickets`, and `tk-implement` use English so handoffs, ledgers, state,
and verification terms remain stable across hosts. User-facing progress and
final receipt prose follows the user's language; canonical status tokens,
IDs, headings, and receipt keys remain unchanged.

## Compatibility

No compatibility shim is needed for canonical skill names or explicit
invocation paths. TigerKit 20.1.3 does not automatically migrate local scratch,
work maps, ledgers, global state, browser profiles, credentials, or evidence.
Revalidate current `.tigerkit/spec.md` and `.tigerkit/tickets.md` against the
refined phase contracts. Keep only current, non-sensitive facts.

Current scratch remains repository/worktree-local `.tigerkit/`. TigerKit does
not modify consumer `.gitignore` files. It does not recreate `CONTEXT.md`,
domain documents, glossaries, or ADRs automatically.

## Removed Skills remain removed

The skills removed before TigerKit 20 remain historical only. Their replacement
mapping is documented in TigerKit 20 changelog and release notes; TigerKit
20.1.3 does not restore those surfaces or the `model-only` invocation kind.
