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

Start only from explicit `/tk-drive`, `$tk-drive`, or host-picker selection with a source, or from the answer to this drive's pending decision in the same conversation. Ordinary implementation requests, generic continuation, artifacts, or a new session do not start or resume it.

## Authority

One start authorizes Preparing, Executing, aggregate verification, unit review, one verified current-branch commit per selected unit, at most three corrective unit commits, and one successful `tk-reflect` tail. It does not authorize push, PR, merge, tag, release, publish, history rewriting, or out-of-scope mutation.

Drive owns the workflow and the only active-drive terminal response. Child procedures own their specialist result and return it to the graph; they do not stop a successful run to ask the user to invoke drive again.

## Recipe

```text
Preparing
  -> tk-grill-me, only for material user-owned decisions
       -> tk-prototype, only when a bounded comparison helps
       -> tk-grill-me
  -> tk-to-spec
  -> tk-to-tickets, only for multiple independently verifiable units
Executing
  -> tk-implement, once per selected unit
       -> tk-merge-conflict, only for an active conflict
       -> tk-implement
  -> aggregate verification
       -> tk-browser-verify, only when required
       -> corrective tk-implement, at most three cycles
  -> tk-reflect, only for a valid reflection handoff
  -> tk-drive finalization

terminal non-success
  -> freeze product mutation
  -> tk-drive non-success finalization
```

Use the complete edge and state-normalization contract in [phases.md](references/phases.md). A successful node invokes its next applicable node in the same active turn. An allowed recovery edge runs before terminal finalization.

Direct continuation is a prompt-directed instruction, not a durable scheduler or guaranteed cross-turn execution. After a host or process boundary, resume by rereading current artifacts and repository evidence.

## Preparing

Before product mutation:

1. Resolve repository instructions, branch, baseline `HEAD`, worktree, and pre-existing dirty paths.
2. Read the complete source and only relevant durable prior art; exclude raw sessions and old scratch ledgers.
3. Close only material user-owned decisions through `tk-grill-me`; use `tk-prototype` only when evidence will reduce the decision.
4. Produce or validate one Ready R/AC spec with `tk-to-spec`.
5. Use `tk-to-tickets` only when multiple vertical units are independently verifiable; otherwise use one no-ticket unit.
6. Write the compact `.tigerkit/prep.md` snapshot through [preflight.md](references/preflight.md), then start Executing immediately.

Freeze exact source UI literals and their authorized changes in R/AC. Freeze the risk-based verification profile from current evidence; Executing may not weaken it or invent unsupported obligations.

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

After recovery edges are exhausted, normalize the child state through `phases.md`, freeze mutation, and enter the internal read-only finalizer. Follow [non-success-finalization.md](references/non-success-finalization.md). Do not clean the failed unit, invoke another specialist, create a partial status or new ledger, or start an independent unit.

## Success finalization

After aggregate product verification passes, invoke `tk-reflect` exactly once only when a valid handoff exists. A no-op is successful. Then reread source, spec, tickets when present, prep, implementation evidence, ancestry, and verification before emitting one terminal response.

Lead with the result. Use `Implemented`, optional `Ticket | Outcome | Commit`, `Verification`, and only meaningful `Reflection`, `Skill candidates`, or `Remaining risks`. End `Verification` with exactly `Status: Pass`; terminal non-success belongs to the read-only finalizer.

### 🔴 HARD GATE · terminal user summary

Treat progress, internal evidence, and terminal output as different surfaces. Start the terminal response with the canonical result heading or sentence. Do not emit a separator, top-level `Outcome:`, receipt heading, caller-return instruction, duplicate status block, or terminal summary between successful child procedures.

Persist provenance in the owning artifact. Show paths, IDs, commits, or recovery details only when they change user action or the result contract requires them.

### 🔴 HARD GATE · response language

Use the latest explicit language instruction, otherwise the current user's language, for every free-form user-facing sentence. Preserve canonical headings, status tokens, IDs, commands, paths, code, and exact source literals.

## User decisions

When Preparing or the one amendment needs a user-owned decision, ask one self-contained question with two or three mutually exclusive options, material evidence, and one recommendation. Use host-native structured input when available. A failed or rejected structured-input call remains non-success; it is not permission to guess.
