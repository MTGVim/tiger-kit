# TigerKit 21.0.0 single-drive preparation and focus mode

TigerKit 21 expands the catalog to 15 canonical skills: 3 user-invoked and
12 hybrid. Installations gain the explicit user-invoked `tk-focus`; no
model-only skill is added.

The orchestration entry point stays singular:

```text
old: /tk-drive <source>
new: /tk-drive <source>
```

Use the equivalent `$tk-drive <source>` selection in Codex. The behavioral
change is internal:

```text
Preparing → Executing
```

The one active `tk-drive` owns decision closure, Ready spec, ticket/no-ticket
choice, verification profile, bounded task-anchored prior-art intake, and the
atomic worktree-local `.tigerkit/prep.md`. Once Ready, it validates and claims
that internal manifest and starts the first implementation unit without a
second command or confirmation. Executing permits one bounded late Preparing
amendment and at most three post-initial corrective cycles.

Existing `.tigerkit/` scratch is not migrated. There is no archive, current
pointer, global state, `CONTEXT.md`, or automatic legacy conversion. A later
fully Ready run may replace a terminal manifest; an active manifest allows
only its matching one-amendment reseal. Direct standalone `tk-implement`
remains valid, with one ticket and one verified commit per unit.

`tk-focus` adapts `ayghri/i-have-adhd` as an explicit persistent output mode.
It never activates from an ordinary request or an ADHD mention. It stays
active until `stop focus mode`, `stop adhd mode`, or `normal mode`, while
safety, ambiguity, and host constraints continue to outrank brevity.

## Removed Skills

No previously released canonical skill is removed. The proposed separate
preparation command is intentionally not a public skill; preparation remains
an internal `tk-drive` stage. Phase ownership remains with the existing
hybrid grill, spec, ticket, prototype, implementation, and reflection skills.

Reflection now classifies a preferred prevention owner and host dependency.
The next related prep discovers at most seven durable task-related items from
repository evidence. `tk-to-spec` owns semantic
`adopted | already-satisfied | not-applicable | conflict` disposition and R/AC
mapping; no relevant item produces no `## Prior art`, while conflict blocks
Ready.

# TigerKit 20.3.1 terminal transition-debt gate

The 14 canonical skill names and the 2 user-invoked / 12 hybrid split remain
unchanged. Consumers only need to refresh the installed package.

`tk-drive` now performs one explicit transition-debt check immediately before
terminal `---` output. A successful child receipt with an unexecuted
`Outstanding transition` continues in the same active turn or returns the one
evidence-supported non-success state; it is never exposed as a terminal
response boundary.

Every skill now embeds the same actionable-output presentation gate while
keeping its existing canonical headings, tables, status tokens,
result budgets, approval boundaries, and response-language contract. The first
available free-form prose slot leads with the answer, outcome, or action;
continuing work exposes current state and the next transition; completed work
does not invent another action.

Every terminal user response now begins after one standalone Markdown `---`
separator. Bottom receipt blocks and the repeated `Outcome:` label are no
longer rendered to the user. Active-drive phase receipts remain internal
handoff envelopes, and durable provenance stays in the existing artifact or
ledger already owned by the skill.

There is no `tk-adhd`, `tk-remind`, persistent mode, toggle, shared runtime
file, universal receipt ledger, read-only write expansion, or consumer state
migration.

# TigerKit 20.2.0 implementation quality and optimistic reflection

TigerKit 20.2.0 keeps all 14 canonical skill names, the 2 user-invoked /
12 hybrid split, and the existing installation commands. Consumers only need
to refresh the installed skill package; no runtime migration is required.

`tk-implement` now records an evidence-backed repository-fit decision before
mutation and runs exactly one behavior-preserving simplify pass after initial
GREEN. Detailed fit, simplify, verification, and review evidence lives in the
repo-local `.tigerkit/implementation.md` scratch ledger.

After aggregate product verification passes, `tk-drive` runs one
`drive-optimistic` reflection tail. Only proven existing repository rules may
be applied automatically. Tracked rules use a separate reflection commit with
`git revert` rollback; pre-existing ignored/local rules use a hash-bound
before-image. Skill candidates remain report-only promotion packets.

User-facing results are no longer forced into one completion sentence. Each
skill uses its own bounded result budget, cites an owning artifact for large
result sets, and keeps Receipt limited to status and provenance. Existing
decision-first ordering and one-question user decision turns remain unchanged.
`tk-reflect` continues to show the readable
`ID | Candidate | Action | Target | Why` table for non-no-op results.

All 14 skills now resolve the response language from the latest explicit user
instruction, falling back to the current user message. Free-form progress,
questions, summaries, and receipt values stay in that language even when the
source is English. Canonical headings, receipt keys, status tokens, IDs,
commands, paths, code, and exact source literals remain byte-stable.

`tk-drive` now freezes a compact verification profile only when exact
source/repository evidence shows material risk. The profile derives existing
regression, compatibility, browser, recovery, and bounded independent-review
obligations without adding a score, lifecycle, or risk artifact. Low-risk
flows remain silent and unchanged; inaccessible required evidence stops with
the existing non-success contract before implementation.

See
[`docs/adr/0001-implementation-quality-and-optimistic-reflection.md`](docs/adr/0001-implementation-quality-and-optimistic-reflection.md)
for the durable decision and supersession rules.

# TigerKit 20.1.7 repository answers and concise receipts

TigerKit 20.1.7 expands the catalog from 13 to 14 canonical skills:
2 user-invoked and 12 hybrid. The new user-invoked `tk-ask-repo` skill is a
read-only investigation desk for inbound repository questions; existing skill
names and phase-owner invocation paths remain valid.

`tk-drive` now requires a Ready spec for every run and carries each successful
child receipt's next transition in the same turn. Output is decision-first,
multi-item results use compact behavior-level tables, and receipt-bearing
skills start receipts with one localized `Outcome` sentence before canonical
status and provenance fields.

No runtime framework, plugin surface, shared contract, or new scratch artifact
is added. Consumers only need to refresh the installed skill package.

# TigerKit 20.1.6 structured user decision questions

TigerKit 20.1.6 preserves all 13 canonical skills and their invocation
boundaries. Every skill now uses the same presentation contract when it owns a
user decision: one question at a time, two or three mutually exclusive
proposals, and exactly one localized recommendation marker.

The `Question` field now appears before `Recommendation` and explains the
evidence-derived context, decision impact, and unresolved axis in readable
user-facing prose. Raw `Evidence` remains available for traceability but is no
longer required reading to understand the choice.

When the active host exposes a native structured user-input tool, the skill
must use it. The canonical examples are Claude Code `AskUserQuestion`, Codex
`request_user_input`, and Hermes Agent `clarify`. Plain-text fallback is
allowed only when no equivalent tool is exposed. Supported option previews or
prototype cards should be used when they materially clarify the choice.

No skill name, phase ownership rule, explicit invocation path, runtime surface,
or installation command changes in this release. Consumers only need to
refresh the installed skill package.

# TigerKit 20.1.5 empirical diagnosis and catalog refinement

This release expands the catalog from 12 to 13 canonical skills:
1 user-invoked and 12 hybrid. The added `tk-skill-diagnose` hybrid owns
empirical reproduction and failure-plane isolation for observed Agent Skill
incidents. It does not replace `tk-grooming`, `tk-reflect`, `tk-learn`, or
Darwin-style broad optimization, and it never writes canonical skills.

Eval consumers may opt into the separate diagnostic pass with `--diagnose`.
Without that flag, normal eval prompts, metrics, summary fields, and records
remain unchanged. Diagnostic records are written only to the existing required
output directory outside the repository.

No existing skill name or explicit invocation path is removed. Canonical skill
bodies and operational references are English; progress and receipts continue
to follow the user's language. Consumers only need to refresh the installed
skill package to receive the new catalog and eval contracts.

# TigerKit 20.1.4 decision-phase orchestration

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
