---
name: tk-drive
description: "[user] Drive an explicit source through decision closure, a Ready spec, conditional tickets, verified unit commits, aggregate verification, and reflection in one continuous run. Use only when selected explicitly with a source, or when resuming this skill's pending decision in the same conversation."
disable-model-invocation: true
argument-hint: "<source, request, issue, or existing Ready spec>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user selects `/tk-drive`, `$tk-drive`, or the host skill
picker with a source. A pending decision answer may resume the same active run
in the same conversation. An ordinary request, generic continuation, scratch
artifact, terminal run, or new session is not a start or resume.

## Authority

An explicit start authorizes Preparing, Executing, aggregate verification,
review, one verified current-branch unit commit per selected unit, at most
three corrective unit commits, and one successful `tk-reflect` tail. It does
not authorize push, PR, merge, tag, release, publish, history rewriting, or
out-of-scope mutation.

Drive owns the workflow and the only active-drive terminal user response.
Participating procedures own their specialist work and pass their native
result state directly to the next applicable node. They do not invoke sibling
phase owners or stop a successful run to ask the caller to resume it.

## Direct procedure graph

```text
tk-drive preflight
  -> tk-grill-me, when material decisions remain
       -> tk-prototype, only when a bounded comparison reduces uncertainty
       -> tk-grill-me
  -> tk-to-spec
  -> tk-to-tickets, only for multiple independently verifiable units
  -> tk-implement, once per selected unit
       -> tk-merge-conflict, only for an active conflict
       -> tk-implement
  -> aggregate verification
       -> tk-browser-verify, only when preflight or changed UI requires it
       -> corrective tk-implement, at most three cycles
  -> tk-reflect, only for a valid reflection handoff
  -> tk-drive finalization
```

Use only exact canonical node names. For every edge, apply the entry, success,
failure, and next-node contract in [references/phases.md](references/phases.md).
A successful node selects and invokes its next applicable node immediately in
the same active turn. A blocked or unverifiable node exposes one actionable
fact and either follows an allowed alternate edge or stops the top-level run.

## Preparing

Before product mutation:

1. Resolve the repository root, applicable instructions, branch, baseline
   HEAD, worktree identity, and dirty-path inventory.
2. Read the complete source. Preserve stable source anchors and exact source UI
   literals.
3. Discover at most seven relevant durable prior-art items from applicable
   rules, ADRs, tests, types, lint, CI, repository skills, and code invariants.
   Exclude raw sessions, prior implementation or reflection scratch, pending
   drafts, arbitrary global state, unrelated work, and inaccessible host-only
   rules.
4. Use `tk-grill-me` only for unresolved material user-owned decisions. When a
   bounded comparison would reduce uncertainty, use `tk-prototype` and feed its
   evidence back into the same decision procedure.
5. Use `tk-to-spec` to create or validate one Ready R/AC contract.
6. Use `tk-to-tickets` only when the Ready work has multiple independently
   verifiable vertical units; otherwise define one no-ticket unit.
7. Freeze the task goal, included and excluded scope, source UI inventory,
   graph route, verification profile, unit order, and browser preflight in
   repo-local `.tigerkit/prep.md`.

Browser preflight is `required | optional | N/A`. Treat a private runtime
identity as a material user-owned decision. Store only an opaque profile hint;
credentials and exact identity are intentionally omitted. On cold start,
re-request identity when current evidence cannot reconstruct it safely.
Re-requesting that runtime input is not a Preparing amendment.

Preparing and Executing are one continuous run. Completing preparation
immediately starts the first `tk-implement` unit in the same active turn.

### 🔴 HARD GATE · source UI writing

During Preparing, inventory every user-visible source literal and freeze its
`authorized change` in R/AC. During Executing, map every selected literal
through the unit, candidate and staged diff, and rendered UI. Missing current
evidence, an unprepared mismatch, or wording outside the frozen authorization
stops mutation before commit.

### 🔴 HARD GATE · risk-based verification profile

During Preparing, classify the material signals and obligations before
selecting verification. Consume the sealed material profile during Executing
and cover its exact frozen profile with unit and aggregate evidence. Drive
cannot add unsupported obligations, remove an obligation, or substitute a
weaker signal.

## Executing

For each selected unit:

1. Map the unit to exact R/AC and inspect its local blast radius.
2. Choose TDD when a meaningful failing test can precede implementation;
   otherwise record the direct strategy and reason.
3. Implement only that unit, simplify it, and run focused verification.
4. Perform the current-agent Standards/Spec review. Large or high-risk work may
   use at most one independent read-only reviewer.
5. Stage only the unit's paths, review the staged candidate, create exactly one
   current-branch commit, and audit hook drift immediately.
6. Continue directly to the next selected unit. After the last unit, continue
   directly to aggregate verification.

Use `tk-merge-conflict` only when an actual merge, rebase, cherry-pick, or
revert conflict becomes active. A successful resolution returns execution to
the interrupted `tk-implement` unit.

## Aggregate verification and correction

After all unit commits, verify R/AC traceability, commit ancestry, unit
boundaries, the frozen verification profile, excluded-scope preservation, and
broad repository checks. Use `tk-browser-verify` only when preflight or changed
UI requires it, then return directly to aggregate verification.

The initial implementation is followed by zero corrective cycles when
aggregate verification passes. Otherwise isolate the smallest affected unit
and permit at most three corrective `tk-implement` cycles. Record cycles
`1`, `2`, and `3`. A fourth cycle, repeated unchanged failure, unisolated
failure, or scope expansion stops mutation with the remaining failing command
and evidence.

One material user-owned decision discovered after execution may use one
amendment through `tk-grill-me`, Ready-spec revalidation, and affected-ticket
rederivation. A second amendment or incompatible committed work stops the run;
never rewrite verified history automatically.

## Reflection and finalization

After product verification succeeds, invoke `tk-reflect` exactly once when a
valid reflection handoff exists. A no-op classification is successful.
Automatic application is allowed only under the reflection containment
contract; otherwise keep it report-only or stop on unsafe restoration.

Then `tk-drive` rereads the current source, spec, tickets when present,
preflight, implementation ledger, commit ancestry, and verification evidence.
Only this finalization node emits the active-drive terminal response.

Lead with one user-facing result sentence. Then render `Implemented` with two
to seven behavior-level bullets and `Verification` with one to four
aggregate-result bullets. For multiple units, include a compact
`Ticket | Outcome | Commit` table. Include `Reflection`, `Skill candidates`,
and `Remaining risks` only when meaningful.

Use a sentence when only one user-relevant row exists. When underlying results
exceed these limits, keep only the top five to seven items ranked by user
impact and verification value.

End `Verification` with the single exact `Status: Pass` line only after every
required artifact and verification result has been reread. A non-success
result leads with its one status, reason, and recovery and stops downstream
invocation.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between successful consecutive active-drive procedure invocations.

Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.

Persist provenance only in an artifact or ledger already owned by the workflow. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks Preparing or the one amendment, ask one
self-contained `Question` before any `Recommendation`. Show only
decision-relevant evidence, two or three mutually exclusive options with
material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve the
supported non-success state.
