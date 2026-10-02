<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/sdd.md -->

# High-fidelity private SDD procedure

This document is the private behavioral canonical source shared by `tk-prep` and
`tk-pr-respond`. Only a controller that actually selected SDD reads it. Do not create a
public skill, global scheduler, or provider-routing state.

## Entry conditions and `Seed` grammar

SDD requires an approved Ready `.tigerkit/seed.md` whose current task identifier
matches. Use the following grammar exactly once outside code fences.

```md
## Execution

Execution shape: SDD

### Global constraints
...

### Unit 1: <non-empty name>
- Goal
- Scope
- Dependencies
- Expected files/interfaces
- Behavior/test protection
- Expected RED
- Acceptance criteria
```

For a behavior-preserving refactoring Unit, keep the `Expected RED` field and state that RED is not applicable,
with the pre-edit GREEN command, protected invariants, and matching post-edit verification required by [testing](testing.md).
This records the normal refactoring path, not a testing waiver.

`## Execution` and `Execution shape: SDD` must each occur exactly once.
`### Global constraints` must occur exactly once before `Unit` 1. `Unit` numbering must
start at 1, be unique and contiguous, and each unit ends at the next `Unit` or next
level-two heading. Ignore fake headings inside code fences. On duplicates, numbering
gaps, empty names, or missing obligations, return `Blocked` before dispatch and repair
the `Seed`.

Keep Unit content decision-dense within this unchanged grammar: exact interfaces, spec-fixed values,
invariants, dependencies, test assertions, acceptance and verification commands/results. Reference
current paths/symbols instead of duplicating ordinary implementation bodies or another Unit's code.
Retain minimal algorithm/ordering structure only when it is itself an approved material decision.
Before finalizing Execution, compare it with the issue/spec and compress code-dominated, unusually
expanded or repeated implementation prose while preserving self-contained scope, identity, BASE and
recovery obligations. Use no fixed size ratio, new reviewer or artifact. Executors reread current
source; ordinary detail drift does not trigger reapproval, but approved-contract drift still does.

Group small same-shape changes into one `Unit` when they need no separate judgment,
testing, or review surface. Split work only when interfaces, risk, testing obligations,
or independent judgment genuinely differ. If two proposed Units would receive the same
implementation/test/review judgment, keep them in one Unit instead of creating review
ceremony.

When natural behavior slices exist, prefer vertical `Unit`s that can be reviewed and
verified independently. This is `vertical-first`, not `vertical-only`. Do not force a
`Cross-cutting refactor` or `wide migration` into artificial behavior slices.

When safe, divide a `Wide migration` into `expand → migrate batch(es) → contract`, and
size migration batches by `blast radius` and verifiability. Keep every stage `green`.
Only when independent `green` is structurally impossible, state the integration and
final-verification boundary in the `Seed`; do not turn that into a general exception.

## Controller and leaf roles

Only the controller owns `Unit` dispatch, review dispatch, remediation-loop routing,
`Ruling:`, and recovery state. Controller-to-controller delegation is allowed, but
implementers, reviewers, and re-reviewers are leaves; no helper or review agent
redispatches. Do not run multiple implementers concurrently.

When host-native multi-agent execution is unavailable, perform the same `Unit` and
review sequence serially in the current isolated execution checkout while preserving
role-specific evidence and exact scope. Do not silently downgrade SDD semantics into
direct execution.

Before every child dispatch or resumed action with changed access/environment, apply
[delegation permissions](review-protocol.md#delegation-permissions) to implementers, reviewers,
verifiers, diagnostic leaves, and delegated controllers. Include the verified boundary in the brief.

### User interaction ownership

The root controller owns intent, scope/AC, Seed changes and new authority. Ordinary approved
non-interactive tool calls and reversible leaf decisions proceed locally. Before any child asks
for user input or continues a host interaction, read [child interaction](sdd-interaction.md):
verify the supported route, request binding, same-or-narrower permissions and safe continuation.
Unknown capability stops only that interaction and returns it to the controller. Never answer
for the user, collect secrets in a handoff or treat authentication as new task authority.
Every child brief must carry these boundaries, known capability evidence (or its unknown state),
the exact accessible path to that reference with its before-input read condition, and the controller
fallback for unsupported input. An isolated child must read it before any elicitation or continuation.

## Failure diagnosis routing

During a `Unit` check or binding verification, keep an obvious failure with an exact RED seam owned by the
current `Unit` in the existing implementer/testing path. If the cause is unknown, intermittent/flaky,
environment-dependent, or appears outside the current `Unit`, the controller records only the exact symptom,
failing evidence, and observed scope, then dispatches one fresh diagnostic leaf that follows
[Difficult bug diagnosis](diagnosis.md) through cause, ownership, and red-capable seam discovery. The leaf
returns those findings without product remediation or redispatch; the controller decides whether to route them
to current-Unit remediation or back to preparation/reapproval. Do not create diagnosis state merely for this
branch.

## Recovery state

Seed, current context and local commits are the normal recovery sources; create no routine ledger.
Before enabling durable recovery, resuming an interrupted run, or handling an empty/malformed/unbound
terminal child return, read [recovery](sdd-recovery.md). Until identity, prior mutations and child lifecycle
are reconciled, never replay work, assume success/failure, advance or replace an implementer. A pending
child is not a terminal empty result. Unknown outcomes remain `Blocked | Unverifiable`.
Read that same reference before updating or deleting an active recovery ledger; retain uniquely owned
material rulings and preserve all remaining review/verification obligations.

## Artifact transport

Prefer faithful direct host payloads and child returns. Only when a file path or bounded file transport
is actually required, read [artifact transport](sdd-transport.md) before writing. Keep it run-owned and
ignored under `.tigerkit/`, with no secrets or external temporary fallback; transport grants no new authority.

## Evidence-backed preflight

Before `Unit` 1, read the Seed once and check:

- every producer/consumer `Unit` pair sharing files or interfaces, and whether they agree;
- internal consistency among requested files, code, tests, and AC for each `Unit`;
- conflicts between global constraints and each `Unit`;
- unresolved findings and decision rationale.

Keep this in controller state by default. Record only unresolved or recovery-relevant
items when a durable ledger is actually active; do not create a table or ledger to say
that everything is clean. A conflict that changes the goal, scope, approved decisions,
ACs, security, or required verification returns to the preparation owner and reapproval.
The controller may resolve only reversible engineering ambiguity with a `Ruling:` that
includes the cost if wrong.

When the approved runtime verification plan requires a pre-edit baseline, invoke its planned verifier
(`tk-browser-verify` or `tk-app-verify`) before the first
Unit implementation. A successful baseline result must carry `phase: baseline`, `baseline_capture: Pass`,
`verification_complete: false`, `resume_parent: required`, the run/replay identity, and `next_required`, after which the controller resumes
Unit 1 in the same approved execution. It is never a completed Unit or completed SDD result.
After the implementation Units, obtain the matching after comparison before whole-change review,
binding verification, or completion. Pause only on the approved limitation and safety boundaries.

## Host and semantic routing

The `Seed` may contain only semantic recommendations such as
`cheap/mechanical | standard integration/debugging | strong architecture/final review`. Do not store
provider model IDs or reasoning intensity in durable artifacts.

On a host that supports child dispatch, read the current allowlist and capabilities and
use explicit controls for every role. When Codex supports `model` and
`reasoning_effort`, specify both and use isolated context through `fork_turns: "none"`
or the current equivalent. Do not inject only one. Do not invent a reasoning-intensity
control for Claude or Hermes when none exists. Use long bounded event-driven waits,
not short polling loops.

## `Unit` implementer

Immediately before dispatch, record `BASE = git rev-parse HEAD`; persist the active-dispatch
identity first when the optional recovery ledger is active, as specified in [recovery](sdd-recovery.md). Give the implementer:

- the task-local `Unit` summary as direct content, or its path only when file transport is required;
- binding global constraints and prior interface decisions;
- a short return contract, plus a report path only when durable/file transport is required;
- the rule that the implementer is a leaf with no subagents;
- approved local mutation and commit boundaries.

The implementer changes only the summary scope and follows [Behavior-first testing](testing.md):
RED → GREEN → REFACTOR for changed behavior, or pre-edit GREEN → refactor → matching GREEN for preserved behavior. It runs focused tests and required
related suites, performs self-review and mutation checks, then creates a local commit.
Self-review removes unnecessary abstraction or indirection, speculative flexibility,
dead or redundant branches, custom logic replacing repository-native helpers, and
production API expansion used only by tests.
The return/report records implementation, changed files, commit, concerns, test commands
and output, and applicable RED/GREEN evidence. Remote publication is forbidden.

## Exact `Unit` review

After implementation, record `HEAD` and always review the complete `BASE..HEAD`. Do not
assume `HEAD~1`. Provide the commit list, change statistics, and full net diff with
enough context directly when possible; materialize a bundle only when transport requires
it.

The one fresh Unit discovery seat first receives:

- the `Unit` summary and binding global constraints;
- the original incident or expected scenario, approved decisions and AC, and relevant test/runtime/browser evidence;
- the exact `BASE..HEAD` evidence.

Do not include the implementer report in that initial payload. After the seat records its blind observations, resume the
same read-only leaf with the implementer report as an untrusted retro claim bundle. The seat then confirms or falsifies
its material claims without replacing the blind observations.

The read-only leaf reviewer records two independent verdicts in one review surface. A
clean verdict on either axis never offsets a failure on the other:

1. **Spec/AC**: omissions, excess, misunderstanding, and exact acceptance compliance;
2. **Quality/Standards**: correctness, maintainability, structure, testing/TDD
   protection, mutation gaps, scope, agreement between listed files and changes, and
   the same unnecessary-complexity or test-only production-API risks required by
   implementer self-review.

Apply [independent review protocol](review-protocol.md) and [finding quality](finding-quality.md) to every `Unit` and
whole-change review. Read
[TypeScript](typescript.md), [React](react.md), and [security](security.md) only when the reviewed scope meets those
references' conditions. A conditional lens does not add a reviewer or pass.

An SDD Unit uses this one fresh discovery seat for both axes and both walks. Aggregate its candidates and send every
candidate that could be reported as `Critical | Important` to a separate fresh verifier before remediation or reporting.

Do not sweep the whole repository without a specifically named risk or unconditionally
rerun suites already present in the report. Re-read available evidence before concluding
that claimed evidence is absent, and run only focused checks for concrete doubts.

## Remediation loop

Handle `Critical`/`Important` findings or confirmed real gaps for at most five rounds.

- Rounds 1–3: resume the same implementer.
- Rounds 4–5: use a fresh implementer with stronger available semantic capability.
- Evidence-only responses at an unchanged reviewed target follow the [review protocol](review-protocol.md#evidence-only-response-to-a-reported-finding). Accepted counter-evidence closes only that finding as `DISPROVED`; it does not manufacture a fix round.
- Every code-change round: record `FIX_BASE = git rev-parse HEAD`, provide open findings, rerun
  protection tests for remediation code, update the return/report, and provide the exact
  `FIX_BASE..HEAD` evidence directly or through file transport only when required.
- Scoped re-review: read the original open findings, remediation diff, and only unchanged
  caller/callee or producer/consumer contracts that the remediation can directly affect, then
  classify each original finding as `ADDRESSED | NOT ADDRESSED`. Reuse the review protocol's
  change-risk walk for that affected boundary; do not restart broad discovery.
- Add only new `Critical`/`Important` findings causally attributable to the remediation to
  the open list, whether the evidence is in the diff or its directly affected unchanged boundary.

If findings remain after round five, stop dispatch and have the controller judge each
one. A material `Seed` conflict returns for reapproval; a reversible residual issue may
be deferred or accepted only with an explicit `Ruling:` and risk. Do not repeat the same
failure indefinitely.

## Completion

Each `Unit` is complete only with a clean work review and recorded commit. After all `Unit`s, construct a whole-change
implementation retro from the Unit returns and exact final diff, then perform exactly one whole-change review using two
context-isolated discovery seats under [independent review protocol](review-protocol.md). Withhold the retro until each
seat records its blind pass. Both seats record independent `Spec/AC` and `Quality/Standards` verdicts and inspect:

- cross-`Unit` integration and full AC/specification scope;
- changed-behavior protection and mutation gaps;
- accidental scope expansion and cross-cutting risk;
- preservation of UI strings that must remain verbatim.

Aggregate the union of both result sets and send every reportable candidate to a separate fresh verifier. A clean seat
cannot cancel another seat's candidate. Missing host support for the required independent contexts is `Unverifiable`, not
a silently downgraded single-review success.

Then run binding verification. For browser-visible targets, obtain `tk-browser-verify`
execution evidence separately from automated regression protection. When the
`tk-pr-respond` SDD path completed this final whole-change review, do not repeat a
generic second review. Clean up only run-owned optional ledger/transport artifacts that satisfy the [recovery](sdd-recovery.md) retention rule. No SDD or local commit expands `push`, `merge`, or publication authority.
