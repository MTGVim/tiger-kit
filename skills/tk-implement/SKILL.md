---
name: tk-implement
description: "[user/auto] Implement, test, review, and create one current-branch commit for one independently verifiable unit. Apply only on explicit standalone selection or an explicit implementation handoff from an active tk-drive; never auto-trigger from an ordinary implementation request."
argument-hint: "<request, ticket, or spec> [direct|delegated] [tdd|no-tdd]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: implement
    relationship: adapted
---

# Implement

Use only for explicit `/tk-implement`, `$tk-implement`, host-picker selection,
or an explicit implementation handoff in which an active `tk-drive` provides
one ticket or no-ticket unit and its R/AC. Do not auto-activate from an ordinary
implementation request, generic continuation, artifact presence, or merely
because drive is active.

## Contract

The user's explicit instructions outrank defaults and recommendations. Do not
weaken, expand, replace, or reconfirm scope, method, prohibitions,
`direct|delegated`, `tdd|no-tdd`, verification, or commit instructions. Ask for
one decision only when instructions conflict or cannot be executed safely.

Never report a source as read or a verification as passed unless it was
actually read or executed.

One invocation owns one independently verifiable implementation unit and
creates one commit after review. With tickets:
`one ticket = one unit = one commit`. Without tickets, the complete explicit
single-slice request or Ready spec is one unit. If standalone input contains
multiple tickets, stop before mutation and ask the user to select one or use
`$tk-drive`. Do not recreate drive orchestration with a batch loop or by
creating tickets.

Standalone execution and drive handoff use the same implementation, test,
review, and commit contract. For a drive handoff, preserve task identity,
ticket/R/AC, initial `HEAD`, and ownership; return phase, unit/ticket ID,
commit SHA, and verification/review evidence. The handoff also supplies
`Success state` and `Outstanding transition`. On `Pass`, include
`Return to: tk-drive` and echo the parent-supplied `Outstanding transition`
verbatim without choosing or executing it. A missing or mismatched
`Success state` or transition cannot produce a successful active-drive
receipt; return `Blocked`. Do not take ownership of drive-wide cross-ticket
verification or its final receipt.

### Terminal-state contract

| Status | Trigger | Required action | Commit |
|---|---|---|---|
| `Pass` | Unit scope is complete and test/coverage gates plus change-related verification/review evidence match the candidate/staged snapshot | Report ID-mapped change and verification references plus remaining risk | Allow exactly one commit when the unit diff can be safely separated from pre-existing user changes |
| `Fail` | Change-related failure, invalid browser evidence, unauthorized UI-writing drift, or commit failure | Preserve failed command/observation, actual `HEAD`, and uncommitted state | Prohibited |
| `Blocked` | Required input, authority, or user decision is missing; safety boundaries conflict; or drift follows the verified snapshot | Stop further mutation and identify the decision or re-verification scope | Prohibited |
| `Unverifiable` | Verification was attempted but environment, tooling, or evidence limitations prevent a verdict | Separate executed scope from unavailable evidence | Prohibited |

Source precedence is: current request, confirmed conversation decisions,
relevant `.tigerkit/tickets.md`, relevant `.tigerkit/spec.md`, repository
instructions, code/tests. Existing files are not automatically relevant.

At scope start, freeze all requirement or acceptance IDs from the relevant
spec/ticket. In the final receipt, map each ID to changed behavior and
verification evidence. If the source has no IDs, do not invent them; record the
source location used.

## Workflow

1. `understand/inspect`: resolve the standalone request or drive handoff,
   related source, unit/ticket ID, scope, constraints, R/AC, initial `HEAD`,
   branch, pre-existing dirty inventory, and unresolved decisions.
2. `resolve strategy`: from code/test evidence, choose `direct | delegated`,
   `tdd | no-tdd`, conditional bug investigation, and whether one independent
   reviewer is permitted.
3. `implement/incremental verification`: implement the smallest coherent
   vertical slice and run focused verification after each slice.
4. `final unit verification`: bind final evidence and failure classification
   to the current branch, `HEAD`, and verified diff/path scope.
5. `review/commit`: run current-agent Standards/Spec review against the
   candidate/staged snapshot, optionally use one bounded independent reviewer,
   confirm no drift, and create one unit commit or stop.
6. `report`: return non-duplicated output sections and an ID-mapped receipt
   tied to the final branch, `HEAD`, commit, and verification evidence.

## CHECKPOINT / STOP

Complete investigation and strategy before source mutation. If requirements
conflict, authority is unsafe, UI intent conflicts, or a required decision
remains, do not implement; stop as `Blocked` with the evidence.

## Strategy

Before editing, inspect relevant code, tests, scripts, and state
non-destructively. Do not create, edit, or delete files, run an implementor, or
commit during this inspection. Non-agent tools such as context-mode, MCP,
search, sandboxes, and test runners are not delegation. Browser tools still
cannot bypass the `tk-browser-verify` precondition below.

After inspection, choose any unspecified execution mode and TDD mode, briefly
state the reason, and implement without an approval question. Prefer `direct`
for small changes, shared files, or tight implementation-verification loops.
Use `delegated` only when scope and completion criteria are independently
transferable and isolation adds material value. Choose TDD when a public
behavior seam, test infrastructure, and regression risk are clear. Choose
no-TDD for copy, configuration, mechanical changes, or when no useful test seam
exists.

Honor user-selected modes and decide only missing modes. Ask only when meaning
branches into materially different outcomes or requires risky irreversible
authority. Do not turn strategy choice into an approval gate.

`delegated` also requires a current-host capability for exactly one bounded
autonomous implementor. If delegation was inferred and that capability is
unavailable, fall back to `direct` and record the reason. If the user explicitly
requires delegation and the capability is unavailable, stop `Blocked` before
any edit.

Example:

```text
Implementation strategy: direct, no TDD — this is a copy-only change with no
useful public test seam. Proceeding with implementation and verification.
```

See [delegation](references/delegation.md) for the bounded delegation contract.

When Figma, a screenshot, or a design specification defines expected UI, apply
hybrid `tk-browser-verify` design-intent preflight before source mutation or any
browser-tool call. Follow its `Blocked` boundary on conflict or ambiguity.

## Implementation and verification

### Execution ownership and investigation

In `direct`, the current agent implements the smallest coherent slices and
repeats focused verification. In `delegated`, give one implementor the scope
and completion criteria, then have the current agent inspect the diff and
evidence. Never nest delegation or let a subagent invoke a user-invoked
TigerKit skill. The implementor does not call browser tools; final browser
verification belongs to the current agent.

For an unknown-cause bug, intermittent failure, or performance regression,
apply the [investigation loop](references/investigation.md) before mutation. Do
not guess-patch without a reproducible red-capable signal. Do not impose the
full hypothesis procedure when the cause is already established. An ordinary
diagnose-only request remains read-only and receives no commit authority.

### Test and coverage

When TDD is selected, choose a meaningful public behavior seam and write one
focused vertical-slice test. Run it and observe red, implement the minimum
change to make it green, and rerun that test plus related verification. Repeat
for another slice when needed. The required loop is `red → green`; refactor is
not mandatory in every cycle. Before implementation, confirm that red is caused
by the expected missing behavior rather than a setup, syntax, fixture, or mock
failure; repair invalid test evidence and rerun until the expected red is
observed. Exercise real behavior and collaborators where practical; mock only
unavoidable external side-effect boundaries, not the behavior under test. Do
not call post-hoc tests TDD, claim an already passing test was red, test private
implementation details, or distort a production API for tests. If the user
requires TDD but no useful seam exists, do not silently switch to no-TDD;
present the seam gap and options for a user decision. In automatic mode, do not
select TDD without a useful seam.

TDD is a strategy, but a durable automated test is a completion condition for
production behavior. For a bug or regression with a meaningful public seam,
run a failing regression test and observe red before the fix, then green after
it. Protect new production behavior with a new or updated public-behavior test
before commit even when TDD was not selected. Only non-runtime changes such as
copy, documentation, pure configuration, or mechanical edits may omit a new
test with a recorded reason; always run relevant verification.

Run existing repository coverage commands and thresholds as-is. Treat a
change-related regression or threshold miss as failure. If coverage tooling
does not exist, do not install or invent a dependency, instrumentation, or
percentage; report `coverage: unavailable`. Missing coverage numbers neither
replace nor fail the durable public-behavior test requirement.

### 🔴 CHECKPOINT · 🛑 STOP · testless production behavior

When production behavior has no meaningful test seam, never grant a silent
testless `Pass`. Present a seam-addition option and deterministic alternative
verification, then stop before commit for the user's decision. Only an
explicitly approved, named exception permits the alternative verification.
After success, record the exception basis, unverified scope, and residual risk
in the receipt. Silence, schedule pressure, and an existing no-TDD choice are
not exception approval.

### 🔴 HARD GATE · source UI writing

For every string literal rendered in UI, freeze a UI-writing inventory before
mutation. Labels, copy, numbers, units, currency, suffixes, and separators are
examples, not an upper bound. Each row maps source location, non-empty source
literal, current rendered/source-path literal, target literal, and
implementation destination.

Missing source/current evidence is `Unverifiable`. Any source↔current mismatch
makes every row a conflict candidate and prevents `Pass` or commit without a
user decision. A typo requires rechecking all same-kind tokens; never
generalize source unreliability to adopt current code silently.

Unless the user explicitly requests a wording change, preserve spelling, case,
spacing, punctuation, symbols, numbers, and meaningful line breaks. Prohibit
translation, paraphrase, shortening, correction, typo fixes, and repository
normalization.

After implementation, compare all three literal columns and include them in
candidate/staged review; a code before/after table cannot replace the source
column. Unauthorized drift is `Fail`; missing exact-comparison evidence is
`Unverifiable`. Mark only explicitly approved wording as `authorized change`.

### 🔴 HARD GATE · browser tools

When scope includes visible UI, layout, styling, responsive behavior,
interaction, navigation, form submission, or browser network/final state,
apply hybrid `tk-browser-verify` as the active verification contract **before
the first browser-tool or verification-server call**. Execute its mode
selection, launch configuration, and safety checkpoint first. Mentioning the
skill or wrapping later evidence in its format is not application.

`tk-implement` must not directly select or call Chrome MCP, Playwright, CDP, or
a native browser. Those tools are available only inside a
`tk-browser-verify` contract that passed the precondition. A browser call made
before the gate is invalid evidence and causes `Fail`. If browser verification
is prohibited or the skill cannot be applied, do not substitute direct tools;
use `Unverifiable`. DOM, accessibility tree, unit tests, or build success do
not replace runtime screenshots and actual image inspection.

### Final verification and review

After each slice, run focused tests plus affected static checks, build, and
required browser/integration verification. After the unit is complete, run the
broadest relevant verification affected by that unit on the cumulative branch.
Drive owns the final cross-ticket broad verification after collecting all unit
receipts. Classify failures as `change-related`, `pre-existing`, `environment`,
or `unverifiable`, then apply the terminal-state contract.

Record final verification with the branch, `HEAD`, and verified diff/path
scope. Immediately before commit, confirm current branch, `HEAD`, and staged
diff still match. On unexpected drift or unverified staged changes, do not
commit; preserve user changes and rerun affected verification or report
`Blocked`. If commit itself fails, do not retry with broad staging or a bypass;
record actual `HEAD` and uncommitted state in a `Fail` receipt.

Every unit runs the current agent's [built-in review](references/review-boundary.md)
regardless of size or risk. Review owns the current unit/ticket diff and R/AC;
it does not repeat drive's aggregate traceability review. Permit one independent
reviewer only for `large` work or high-risk authentication, payment, privacy,
authorization, dependency, migration/data-loss, concurrency, or public API
changes. Bound the flow to one review, one fix, and one regression verification.
An important finding, drift, or unverified coverage prevents commit.

## Commit and report

Create exactly one current-branch unit commit only when status is `Pass` and
the user did not prohibit commit. An implementor never commits; the current
agent verifies the staged diff and commits. For a drive handoff, return commit
SHA and unit/ticket ID so drive does not create another commit.

Immediately after commit, audit the committed diff against the frozen reviewed
candidate using [post-commit drift rules](references/review-boundary.md).
Unclassified or semantic hook drift means the commit is not a verified `Pass`.

An ordinary review-only request is a read-only agent task and grants no source
mutation or commit authority. Review inside this skill owns only the explicit
implementation scope and candidate diff.

Without a separate request, do not push, create a PR, merge, tag, release, or
publish. Do not automatically invoke another user-invoked skill.

Lead with `## Changed`, then `## Verification`, optional
`## Remaining risks`, and `## Receipt`. Add `## Strategy` only for an explicit
choice, exception, or plan deviation. Do not add a separate `## Commit`;
`Receipt` owns the commit SHA/message or why no commit exists.

Describe user-visible or unit behavior, not only files. Summarize commands and
results; never paste logs or narrate review mechanics. `Verification` owns
coverage, failure classification, and
`hook drift: none | format-only | reverted-semantic`. `Receipt` owns phase,
unit/ticket ID, status (`Pass | Fail | Blocked | Unverifiable`), commit,
unverified items, and R/AC references without repeating the body. Omit
`Remaining risks` when empty.

Write user-facing progress and report prose in the user's language. Preserve
the canonical headings, status tokens, IDs, and receipt keys above.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
