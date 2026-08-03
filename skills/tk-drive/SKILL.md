---
name: tk-drive
description: "[user] Drive an explicit source through decision closure, a Ready spec, conditional tickets, verified unit commits, aggregate verification, and finalization in one continuous run. Use only when selected explicitly with a source, or when resuming this skill's pending decision in the same conversation."
disable-model-invocation: true
argument-hint: "<source, request, issue, or existing Ready spec>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user selects `/tk-drive`, `$tk-drive`, or the host skill picker with a source, or answers this drive's pending decision in the same conversation. Ordinary implementation requests, generic continuation, artifacts, or a new session do not start or resume it.

## Authority

One start authorizes Preparing, Executing, aggregate verification, unit review, one verified current-branch commit per selected unit, and at most three corrective unit commits. It does not authorize push, PR, merge, tag, release, publish, history rewriting, or out-of-scope mutation.

Drive owns the workflow and the only active-drive terminal response. Child procedures own their specialist work and pass their native result state directly to the next applicable node. They do not stop a successful run to ask the user to invoke drive again.

## Direct procedure graph

```text
tk-drive preflight
  -> tk-grill-me, only for material user-owned decisions
       -> tk-prototype, only when a bounded comparison helps
       -> tk-grill-me
  -> tk-to-spec
  -> tk-to-tickets, only for multiple independently verifiable units
  -> tk-implement, once per selected unit
       -> tk-merge-conflict, only for an active conflict
       -> tk-implement
  -> aggregate verification
       -> tk-browser-verify, only when required
       -> corrective tk-implement, at most three cycles
  -> tk-drive finalization

terminal non-success
  -> freeze product mutation
  -> tk-drive non-success finalization
```

Use the complete edge and state-normalization contract in [phases.md](references/phases.md). For every edge, apply its entry, success, failure, and next-node contract. A successful node invokes its next applicable node in the same active turn. An allowed recovery edge runs before terminal finalization.

Direct continuation is a prompt-directed instruction, not a durable scheduler or guaranteed cross-turn execution. After a host or process boundary, resume by rereading current artifacts and repository evidence.

## Preparing

Before product mutation:

1. Resolve repository instructions, branch, baseline `HEAD`, worktree, and pre-existing dirty paths.
2. Read the complete source. Discover at most seven relevant durable prior-art items from applicable rules, ADRs, tests, types, lint, CI, repository skills, and code invariants. Exclude raw sessions, prior implementation scratch, pending drafts, arbitrary global state, unrelated work, and inaccessible host-only rules.
3. Close only material user-owned decisions through `tk-grill-me`; use `tk-prototype` only when evidence will reduce the decision.
4. Produce or validate one Ready R/AC spec with `tk-to-spec`.
5. Use `tk-to-tickets` only when multiple vertical units are independently verifiable; otherwise use one no-ticket unit.
6. Write the compact `.tigerkit/prep.md` snapshot through [preflight.md](references/preflight.md), then start Executing immediately.

### 🔴 HARD GATE · source UI writing

Freeze every user-visible source literal and its `authorized change` in R/AC before mutation. Executing must compare the source, current value, candidate/staged diff, and rendered result. Missing evidence, an unresolved mismatch, or wording outside the frozen authorization stops before commit.

### 🔴 HARD GATE · risk-based verification profile

During Preparing, classify material signals and obligations from current evidence. Consume the sealed material profile during Executing. Drive cannot add unsupported obligations, remove an obligation, or substitute weaker evidence.

Classify PR evidence separately as `required | optional | N/A` and seal it in
the Ready spec and preflight with a criterion whenever applicable. Use
`required` only when a confirmed source requires attached visual proof or a
browser-rendered acceptance criterion cannot be meaningfully reviewed from
code and checks alone; use `optional` when a screenshot would help review but
is not acceptance-critical; use `N/A` when no browser-visible result exists.
Browser verification being `required` does not by itself make PR evidence
`required`. Return a material ambiguity to Preparing instead of guessing.

Browser preflight is `required | optional | N/A`. A private runtime identity is material user-owned input. Store only an opaque profile hint and an `intentionally omitted` marker; re-request missing identity on cold start. Runtime rehydration is not a Preparing amendment.

## Executing

For each unit:

1. pass its exact R/AC, scope, order, and verification profile to `tk-implement`;
2. accept only a verified one-unit commit or its bounded non-success handoff;
3. preserve pre-existing user changes and audit commit ancestry;
4. continue directly to the next selected unit.

Use `tk-merge-conflict` only for a real merge, rebase, cherry-pick, or revert conflict, then return to the interrupted unit.

## Aggregate verification

After all unit commits, verify R/AC traceability, ancestry, unit boundaries, excluded scope, the frozen profile, and broad repository checks. Use `tk-browser-verify` when preflight or changed UI requires runtime evidence.

A passing initial implementation uses zero corrective cycles. An isolated implementation defect may use at most three corrective `tk-implement` cycles. A fourth cycle, repeated unchanged failure, unisolated failure, or scope expansion freezes mutation.

One late material user-owned decision may use one amendment through `tk-grill-me`, Ready-spec revalidation, affected-ticket rederivation, and prep refresh. A second amendment or incompatible committed work is terminal `Blocked`; never rewrite verified history automatically.

## Non-success

After recovery edges are exhausted, normalize the child state through `phases.md`, freeze mutation, and enter the internal read-only finalizer. Follow [non-success finalization](references/non-success-finalization.md). It has no outgoing edge. Do not clean the failed unit, invoke another specialist, create a partial status or new ledger, or start an independent unit.

## Success finalization

After aggregate product verification passes, finish directly. Reread source, spec, tickets when present, prep, implementation evidence, ancestry, and verification before emitting one terminal response. TigerKit does not own a post-session reflection or persistent-memory phase.

Lead with one user-facing result sentence. Then render `Implemented` with two to seven behavior-level bullets and `Verification` with one to four aggregate-result bullets. For multiple units, include a compact `Ticket | Outcome | Commit` table. Use a sentence when only one user-relevant row exists. When underlying results exceed these limits, keep only the top five to seven items ranked by user impact and verification value. Include `Remaining risks` only when meaningful. End `Verification` with exactly `Status: Pass`; terminal non-success belongs to the read-only finalizer.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between successful consecutive active-drive procedure invocations.

Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.

Persist provenance only in an artifact or ledger already owned by the workflow. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks Preparing or the one amendment, ask one self-contained `Question` before any `Recommendation`. Show only decision-relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex `request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only when none is exposed. A failed or rejected call is not absence; preserve `Pending | Blocked`.
