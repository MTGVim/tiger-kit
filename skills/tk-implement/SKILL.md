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

Use only for explicit `/tk-implement`, `$tk-implement`, host-picker selection, or an exact active `tk-drive` handoff containing one ticket or no-ticket unit and its R/AC. Ordinary implementation requests, generic continuation, artifacts, or drive presence alone do not activate it.

## Unit contract

One invocation owns one independently verifiable unit and, after verification and review, exactly one current-branch commit. With tickets: `one ticket = one unit = one commit`. Standalone multi-ticket input must select one ticket or use `$tk-drive`; do not recreate drive orchestration.

Explicit user instructions outrank defaults. Do not weaken or reconfirm settled scope, method, prohibitions, strategy, verification, or commit instructions. Ask only when instructions conflict or safe execution requires a material user decision. Never claim a source was read or a check passed unless it was actually read or executed.

For active drive, preserve task identity, ticket/R/AC, initial `HEAD`, pre-existing dirty paths, and the frozen verification profile. Return the unit ID, native status, commit when present, and verification/review evidence to the graph. Do not emit a terminal user result or take ownership of cross-unit verification or finalization.

| Status | Meaning | Commit |
| --- | --- | --- |
| `Pass` | Unit behavior, required tests/checks, and review match the final candidate | Exactly one, when separable from user changes |
| `Fail` | Change-related failure, invalid evidence, unauthorized UI drift, or commit failure | None |
| `Blocked` | Required input/authority/decision is missing or safe ownership conflicts | None |
| `Unverifiable` | Required verification was attempted but cannot establish a verdict | None |

A drive non-success handoff includes actual branch/`HEAD`, changed or uncommitted paths, executed and unavailable verification, blocker/failure, and one recovery condition. It grants no cleanup, continuation, commit, downstream specialist, or finalization authority.

## Workflow

1. **Inspect** — resolve source, unit, R/AC or source anchors, branch, initial `HEAD`, relevant code/tests/instructions, and pre-existing dirty paths.
2. **Choose strategy** — use `direct` by default; use `delegated` only when one bounded implementor can own a transferable unit and isolation adds value. Choose TDD only with a meaningful public-behavior seam.
3. **Implement** — change only the unit, prove coherent behavior slices, and reach initial green.
4. **Simplify** — run exactly one behavior-preserving reuse/simplicity/ownership pass through [review-boundary.md](references/review-boundary.md).
5. **Verify and review** — apply the relevant sections of [execution-gates.md](references/execution-gates.md), then the Standards/Spec review.
6. **Commit and report** — recheck branch, `HEAD`, staged ownership, and evidence; commit once only for `Pass`; update `.tigerkit/implementation.md` and return the bounded result.

## Strategy

Inspect before mutation. Decide unspecified `direct | delegated` and `tdd | no-tdd` without an approval ceremony.

- Prefer `direct` for small changes, shared files, or tight edit/verification loops.
- Use `delegated` only with exactly one bounded implementor; load [delegation.md](references/delegation.md). If inferred delegation is unavailable, fall back to direct. If the user required it, return `Blocked`.
- For unknown-cause bugs, intermittent failures, or performance regressions, load [investigation.md](references/investigation.md). Do not guess-patch; skip the full investigation loop when the cause is already established.
- Do not nest delegation or let an implementor invoke a user-invoked TigerKit skill. The current agent owns final evidence, review, staging, and commit.

## Applicable gates

Load [execution-gates.md](references/execution-gates.md) selectively:

- **Tests/coverage** for behavior changes, bugs, regressions, and repository thresholds.
- **Source UI writing** when source material defines exact user-visible text.
- **Browser verification** for visible UI, interaction, navigation, responsive behavior, or browser final state.
- **Final review/commit** for every unit.

Before mutation and after initial green, use [review-boundary.md](references/review-boundary.md) for design fit, one simplify pass, fixed candidate/staged evidence, implementation ledger ownership, Standards/Spec review, and post-commit hook drift.

## CHECKPOINT / STOP

Before editing, stop `Blocked` when requirements conflict, authority is unsafe, exact UI intent is unresolved, or a required user decision remains. During execution, apply the status table without converting unavailable evidence into `Pass`.

## Commit and result

Commit exactly once only when status is `Pass` and commit is not prohibited. Stage only this unit's paths; preserve pre-existing user changes. Never broaden staging, bypass hooks for convenience, push, create a PR, merge, tag, release, or publish without a separate request.

For standalone success, lead with `## Changed`, then `## Verification`, and optional `## Strategy` or `## Remaining risks` only when meaningful. Describe behavior, summarize checks, and report the commit once. Keep logs, detailed mappings, and provenance in `.tigerkit/implementation.md`.

For active drive, return only the internal unit ID, status (`Pass | Fail | Blocked | Unverifiable`), commit, R/AC references, verification/review evidence, and unverified items.

### 🔴 HARD GATE · terminal user summary

Treat progress, internal evidence, and terminal output as separate surfaces. Start with the canonical result heading. Do not emit a separator, top-level `Outcome:`, receipt heading, caller-return instruction, duplicate provenance block, or terminal user result during an active drive handoff.

### 🔴 HARD GATE · response language

Use the latest explicit language instruction, otherwise the current user's language, for every free-form user-facing sentence. Preserve canonical headings, status tokens, IDs, commands, paths, code, and exact source literals.

## User decisions

When a material user-owned decision blocks progress, ask one self-contained question with two or three mutually exclusive options, relevant evidence, and one recommendation. Use host-native structured input when available; a failed or rejected call remains non-success and never authorizes guessing.
