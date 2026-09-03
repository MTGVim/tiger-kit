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

`## Execution` and `Execution shape: SDD` must each occur exactly once.
`### Global constraints` must occur exactly once before `Unit` 1. `Unit` numbering must
start at 1, be unique and contiguous, and each unit ends at the next `Unit` or next
level-two heading. Ignore fake headings inside code fences. On duplicates, numbering
gaps, empty names, or missing obligations, return `Blocked` before dispatch and repair
the `Seed`.

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

## Recovery state

The Ready Seed, current controller context, and local commits are the normal recovery
sources. Do not create a progress ledger merely because execution shape is SDD.

Create at most one ignored `.tigerkit/sdd.md` only when execution is likely to outlive
the current controller context, the host cannot reliably retain Unit/review state, or an
interrupted run actually needs durable recovery. When a ledger is needed, keep only:

- Ready `Seed` identifier and content hash;
- preflight conflicts or rulings that are not already preserved in the Seed;
- current `Unit` and completed commit SHAs;
- open review findings and remediation round when active;
- temporary artifact identifiers and paths that are required for recovery.

Do not copy stable Seed content or completed reports into the ledger. Do not resume a
ledger with a different Seed identifier/hash or one from completed work. If it does not
match the current Seed exactly, return `Blocked` before new dispatch and return to the
preparation owner. Delete a run-owned ledger when binding acceptance is clean.

## Artifact transport

Prefer direct host payloads and child return values for Unit summaries, reports, and
exact diffs. Do not materialize an artifact merely to pass information that the active
host can transport faithfully.

Use a flat `.tigerkit/sdd-tmp/` only when a child requires a file path, an exact bundle
cannot be transported reliably through the host surface, or bounded context size makes
file transport necessary. Before the first write, prove with `git check-ignore -v` that
Git's effective ignore rules cover `.tigerkit/` and verify that `git ls-files -- .tigerkit/`
returns no tracked paths. Per-directory `.gitignore`, `.git/info/exclude`, and configured
user-level exclude sources are all valid. If required file transport is not ignored,
writable, or visible to the child, do not edit `.gitignore` or fall back to an
operating-system temporary path; return `Blocked | Unverifiable` before dispatch.

Do not create per-run or per-plan hierarchies. Use unique filenames containing the
Seed identifier, `Unit`, and scope. Clean up only run-owned files and never delete
unrelated files. Do not put secrets in artifacts.

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

Immediately before dispatch, record `BASE = git rev-parse HEAD`. Give the implementer:

- the task-local `Unit` summary as direct content, or its path only when file transport is required;
- binding global constraints and prior interface decisions;
- a short return contract, plus a report path only when durable/file transport is required;
- the rule that the implementer is a leaf with no subagents;
- approved local mutation and commit boundaries.

The implementer changes only the summary scope and performs applicable RED → GREEN →
REFACTOR from [Behavior-first testing](testing.md). It runs focused tests and required
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

Reviewer input is:

- the `Unit` summary and binding global constraints;
- the implementer report/return and its untrusted claims;
- the exact `BASE..HEAD` evidence.

The read-only leaf reviewer records two independent verdicts in one review surface. A
clean verdict on either axis never offsets a failure on the other:

1. **Spec/AC**: omissions, excess, misunderstanding, and exact acceptance compliance;
2. **Quality/Standards**: correctness, maintainability, structure, testing/TDD
   protection, mutation gaps, scope, agreement between listed files and changes, and
   the same unnecessary-complexity or test-only production-API risks required by
   implementer self-review.

Apply [finding quality](finding-quality.md) to every `Unit` and whole-change review. Read
[TypeScript](typescript.md), [React](react.md), and [security](security.md) only when the reviewed scope meets those
references' conditions. A conditional lens does not add a reviewer or pass.

One reviewer or one serial review may judge both axes. Do not add a mandatory second
reviewer or parallel reviewer fan-out.

Do not sweep the whole repository without a specifically named risk or unconditionally
rerun suites already present in the report. Re-read available evidence before concluding
that claimed evidence is absent, and run only focused checks for concrete doubts.

## Remediation loop

Handle `Critical`/`Important` findings or confirmed real gaps for at most five rounds.

- Rounds 1–3: resume the same implementer.
- Rounds 4–5: use a fresh implementer with stronger available semantic capability.
- Every round: record `FIX_BASE = git rev-parse HEAD`, provide open findings, rerun
  protection tests for remediation code, update the return/report, and provide the exact
  `FIX_BASE..HEAD` evidence directly or through file transport only when required.
- Scoped re-review: read only the original open findings and remediation diff, then
  classify each finding as `ADDRESSED | NOT ADDRESSED`.
- Add only new `Critical`/`Important` findings introduced by the remediation diff to
  the open list.

If findings remain after round five, stop dispatch and have the controller judge each
one. A material `Seed` conflict returns for reapproval; a reversible residual issue may
be deferred or accepted only with an explicit `Ruling:` and risk. Do not repeat the same
failure indefinitely.

## Completion

Each `Unit` is complete only with a clean work review and recorded commit. After all
`Unit`s, perform exactly one whole-change review and again record independent `Spec/AC`
and `Quality/Standards` verdicts for:

- cross-`Unit` integration and full AC/specification scope;
- changed-behavior protection and mutation gaps;
- accidental scope expansion and cross-cutting risk;
- preservation of UI strings that must remain verbatim.

Then run binding verification. For browser-visible targets, obtain `tk-browser-verify`
execution evidence separately from automated regression protection. When the
`tk-pr-respond` SDD path completed this final whole-change review, do not repeat a
generic second review. Clean up only run-owned optional ledger/transport artifacts. No
SDD or local commit expands `push`, `merge`, or publication authority.
