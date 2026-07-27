---
name: tk-drive
description: "[user/auto] Orchestrate an explicitly started source through the canonical spec, ticket, and implementation phase owners to verified ticket-level commits, or resume immediately after the user answers this drive's pending decision in the same conversation. Do not start from an ordinary implementation request, generic continuation, or artifact presence."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Drive

Start a new workflow only when the user explicitly selects `tk-drive` in the
current host. `/tk-drive`, `$tk-drive`, and direct selection in a host skill
picker are equivalent explicit starts. The only implicit positive is the
user's answer to the one pending decision left by this active drive in the same
conversation; apply the answer and continue without another invocation when no
blocker remains.

An ordinary code request, generic `continue`, an existing `.tigerkit/`
artifact, an answer to another question, a new session, or a broken
conversation is not an implicit start or resume. For an ordinary implementation
request, leave ownership with the current agent's normal implementation path,
including any commit authority the user granted directly; do not invoke or
simulate this workflow. In a new session, require a new explicit `$tk-drive`
start and reconstruct phases from repository evidence.

## Contract

An explicit start authorizes planning, ticket-level implementation,
verification, review, and verified current-branch unit commits within the
current source scope. It does not authorize push, PR, merge, tag, release,
publish, automatic reflection, history rewriting, or out-of-scope mutation.

The latest explicit source outranks scratch artifacts. Ignore unrelated
artifacts and revalidate stale spec or ticket artifacts against current
evidence. Ask only when task identity or decision reversal cannot be resolved.
Do not create drive-only state, current pointers, archives, global state, or
automatic migration.

Follow [phase invariants](references/phases.md). Drive owns orchestration, not
phase semantics:

- `tk-to-spec` owns the spec;
- `tk-to-tickets` owns ticket decomposition;
- `tk-implement` owns one implementation unit's tests, review, and commit.

The phase-owner allowlist is
`tk-to-spec | tk-to-tickets | tk-implement`. The conditional support allowlist
is `tk-prototype | tk-browser-verify | tk-merge-conflict`. Do not invoke other
planning, learning, reflection, or handoff skills, and do not create a shared
runtime contract.

If a phase skill is unavailable or does not return its required success
receipt, propagate that state and stop at the phase. Never recreate its
semantics inline. Do not intercept a standalone phase request, and do not let a
phase owner take over drive-wide orchestration, aggregate verification, or the
final receipt.

### 🔴 HARD GATE · source UI writing

If user-provided source contains a label, button, heading, guide/help copy,
table or column name, placeholder, validation/error, or status text, freeze an
inventory before spec mutation. Map source location, exact literal, spec R/AC,
optional ticket, and implementation destination.

Unless the user explicitly approves a wording change, prohibit translation,
paraphrase, shortening, correction, typo fixes, and normalization. Mark only
approved changes as `authorized change`. An unreadable literal is
`Unverifiable`; conflicting literals that require a user choice are `Blocked`.

Compare the same inventory exactly in the spec, tickets, implementation,
candidate/staged diff, and rendered UI. Do not commit when any unauthorized
drift or exact-comparison evidence gap remains.

## Workflow

1. `preflight`: resolve source, relevant spec/tickets, repository instructions,
   branch, initial `HEAD`, dirty ownership, drift, task identity, completed
   phases, and unresolved decisions.
2. `inline grill gate`: only for blocking ambiguity, report one `Evidence`,
   `Recommendation`, and `Question`, then stop as `pending` before downstream
   mutation.
3. `spec phase`: explicitly hand current source, confirmed decisions, and
   traceability to `tk-to-spec`; accept only a `Ready` receipt.
4. `ticket decision`: hand the Ready spec to `tk-to-tickets` only when there
   are at least two independently verifiable vertical slices or a ledger adds
   material long-resume value. Otherwise use one no-ticket implementation unit.
5. `prototype branch`: only when unresolved web visual ambiguity affects
   behavior or structure and 2–3 disposable alternatives materially narrow
   one decision.
6. `implementation commits`: keep at most one ticket `in_progress`; hand one
   ticket and its R/AC, or the one no-ticket unit, to `tk-implement`. Mark it
   `verified` only from the matching verified commit receipt, then continue.
7. `aggregate verification`: reconcile all unit receipts, commit ancestry,
   R/AC coverage, and cross-ticket interaction; run the broadest executable
   relevant verification once. Do not repeat each ticket's line-level
   Standards/Spec review.
8. `corrective cycle/report`: for one isolated final change-related regression,
   create at most one corrective ticket through `tk-to-tickets`, run
   `tk-implement` once, and rerun broad verification once. Otherwise stop
   mutating and produce the final receipt.

## 🔴 CHECKPOINT · 🛑 STOP · pending decision and resume

A question covers one blocking ambiguity and reports `Evidence`,
`Recommendation`, and `Question` exactly once. Do not start an exhaustive
interview or invoke `tk-grill-me`. Do not mutate source or downstream spec
before the answer.

When the answer directly resolves the pending decision, update the decision and
source traceability, then continue automatically. If it adds scope or does not
correspond to the pending decision, do not inherit commit authority; report the
drift or require a new explicit `$tk-drive` start.

## Failure and completion

| Trigger | Immediate action | Terminal handling |
|---|---|---|
| Required source, authority, or decision is missing at preflight | Stop before downstream mutation and identify the one needed item | `Blocked`; no commit |
| Phase skill is unavailable or lacks its success receipt | Preserve phase, state, and evidence without inline fallback | End in the one evidence-supported state: `Blocked`, `Fail`, or `Unverifiable` |
| Unit candidate/staged diff differs from handoff scope, source inventory, or verified snapshot | Propagate `tk-implement` state and reconcile drift | `Blocked`; preserve valid diff and commits |
| Ticket/unit verification fails | Record command, observation, and affected unit; stop the next handoff | `Fail`; preserve earlier verified commits |
| Final broad verification has a change-related failure | Isolate the cause and run at most one corrective ticket/commit cycle | `Fail` if isolation or re-verification fails; never rewrite history |
| Final broad verification has a pre-existing failure | Separate prior evidence from current commits; do not mutate | `Fail`; no corrective ticket |
| Final broad verification has an environment failure | Separate environment evidence and attempt one reproducible check | `Unverifiable`; no corrective ticket |
| Verification ran but its result evidence cannot be obtained | Attempt one reproducible evidence capture | `Unverifiable`; no commit |
| `tk-implement` commit command fails | Stop handoffs and preserve output, branch, `HEAD`, and index | `Fail`; clean only temporary artifacts owned by this run |
| Receipt `HEAD` or ancestry differs from the expected handoff | Stop handoffs and reread branch, `HEAD`, and index | `Blocked`; preserve valid commits and identify re-verification scope |

The final receipt owns `Status`, `Source`, `Phases`, `Tickets`,
`Verification`, `Integration review`, `Commits`, `Remaining risks`, and
`Reusable candidate`. `Commits` maps unit/ticket IDs to commit SHAs and marks a
corrective commit. Report only whether a reusable candidate exists; do not
automatically invoke `tk-reflect`. Do not duplicate child evidence.

Write user-facing progress updates and the final receipt in the user's language,
while preserving canonical status and receipt field names.

## DO NOT / ANTI-PATTERNS

- Do not start from an ordinary request, artifact, or generic continuation.
- Do not extend commit authority from an unrelated answer.
- Do not force tickets for a small single slice or trust stale ticket status.
- Do not duplicate phase-owner semantics or bypass a phase failure inline.
- Do not let drive stage/commit source or repeat `tk-implement`'s ticket-level
  code review.
- Do not amend, squash, roll back, or otherwise rewrite verified unit commits,
  and do not run a second corrective cycle.
- Do not invoke skills outside the allowlists, nest delegation, or
  automatically reflect, hand off, or learn.
