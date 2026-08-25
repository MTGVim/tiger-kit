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
testing, or review surface. Split work when interfaces, risk, testing obligations, or
independent judgment differ.

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

An active SDD keeps at most one ignored `.tigerkit/sdd.md` in the repository. Its
minimum record is:

- Ready `Seed` identifier and content hash;
- preflight results;
- current `Unit` and completed commit SHAs;
- review and remediation rounds plus open findings;
- `Ruling: decision — reason — cost if wrong`;
- temporary artifact identifiers and paths required for recovery.

Do not resume a ledger with a different `Seed` identifier/hash or one from completed
work. If it does not match the current `Seed` exactly, return `Blocked` before new
dispatch and return to the preparation owner. When all `Unit`s, final review, and
binding acceptance are clean, delete `sdd.md` and run-owned temporary artifacts.

## Artifact transport

Place work summaries, implementer reports, `BASE..HEAD` review bundles, and remediation
bundles in an operating-system temporary path first. Trust that path only after running
a behavioral probe before the first dispatch in which a child reads an arbitrary value
written by the parent and the parent reads a confirmation value written by the child
on the current host.

If the probe fails or the host has no child filesystem, use only a flat ignored
`.tigerkit/sdd-tmp/` as fallback. Do not create per-run or per-plan hierarchies. Use
unique filenames containing the `Seed` identifier, `Unit`, and scope. Clean up only
run-owned files and never delete unrelated files. Do not put secrets in artifacts.

## Evidence-backed preflight

Before `Unit` 1, read the `Seed` once and record this table in `sdd.md`:

- every producer/consumer `Unit` pair sharing files or interfaces, and whether they agree;
- internal consistency among requested files, code, tests, and AC for each `Unit`;
- conflicts between global constraints and each `Unit`;
- unresolved findings and decision rationale.

Do not replace the table with one “clean” line. A conflict that changes the goal, scope,
approved decisions, ACs, security, or required verification returns to the preparation
owner and reapproval. The controller may resolve only reversible engineering ambiguity
with a `Ruling:` that includes the cost if wrong.

## Host and semantic routing

The `Seed` may contain only semantic recommendations such as
`cheap/mechanical | standard integration/debugging | strong architecture/final review`. Do not store
provider model IDs or reasoning intensity in the `Seed` or ledger.

On a host that supports child dispatch, read the current allowlist and capabilities and
use explicit controls for every role. When Codex supports `model` and
`reasoning_effort`, specify both and use isolated context through `fork_turns: "none"`
or the current equivalent. Do not inject only one. Do not invent a reasoning-intensity
control for Claude or Hermes when none exists. Use long bounded event-driven waits,
not short polling loops.

## `Unit` implementer

Immediately before dispatch, record `BASE = git rev-parse HEAD`. Give the implementer
the following rather than the full conversation or `Seed`:

- the path to a task-local `Unit` summary that is the requirements canonical source;
- binding global constraints and prior interface decisions;
- report path and short return contract;
- the rule that the implementer is a leaf with no subagents;
- approved local mutation and commit boundaries.

The implementer changes only the summary scope and performs applicable RED → GREEN →
REFACTOR from [Behavior-first testing](testing.md). It runs focused tests and required
related suites, performs self-review and mutation checks, then creates a local commit.
Self-review removes unnecessary abstraction or indirection, speculative flexibility,
dead or redundant branches, custom logic replacing repository-native helpers, and
production API expansion used only by tests.
The report records implementation, changed files, commit, concerns, test commands and
output, and applicable RED/GREEN evidence; the parent receives only a short status.
Remote publication is forbidden.

## Exact `Unit` review

After implementation, record `HEAD` and always review the complete `BASE..HEAD`. Do not
assume `HEAD~1`. The review bundle contains the commit list, change statistics, and the
full net diff with enough context.

Reviewer input is:

- the `Unit` summary and binding global constraints;
- the implementer report and its untrusted claims;
- the exact `BASE..HEAD` bundle.

The read-only leaf reviewer judges:

1. specification and AC compliance: omissions, excess, and misunderstanding;
2. testing and TDD quality, changed-behavior protection, and mutation gaps;
3. correctness, maintainability, structure, scope, and the same unnecessary-complexity
   or test-only production-API risks required by implementer self-review;
4. agreement between listed files and changes for a bundled `Unit`.

Do not sweep the whole repository without a specifically named risk or unconditionally
rerun suites already present in the report. Re-read artifacts before concluding that
claimed evidence is absent, and run only focused checks for concrete doubts.

## Remediation loop

Handle `Critical`/`Important` findings or confirmed real gaps for at most five rounds.

- Rounds 1–3: resume the same implementer.
- Rounds 4–5: use a fresh implementer with stronger available semantic capability.
- Every round: record `FIX_BASE = git rev-parse HEAD`, provide open findings, rerun
  protection tests for remediation code, append the report, and create the exact
  `FIX_BASE..HEAD` bundle.
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
`Unit`s, perform exactly one whole-change review for:

- cross-`Unit` integration and full AC/specification scope;
- changed-behavior protection and mutation gaps;
- accidental scope expansion and cross-cutting risk;
- preservation of UI strings that must remain verbatim.

Then run binding verification. For browser-visible targets, obtain `tk-browser-verify`
execution evidence separately from automated regression protection. When the
`tk-pr-respond` SDD path completed this final whole-change review, do not repeat a
generic second review. No SDD or local commit expands `push`, `merge`, or publication
authority.
