---
name: tk-drive
description: "[user] Orchestrate an explicitly started source through conditional decision closure and the canonical spec, ticket, and implementation phase owners to verified ticket-level commits. Use only when selected explicitly; an active invocation may continue after its child phase returns."
disable-model-invocation: true
argument-hint: "<source, request, issue, spec, or tickets>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user selects `/tk-drive`, `$tk-drive`, or the host skill
picker. Within that conversation, keep ownership across the directly
corresponding child answer and continuation receipt; a success receipt advances
to the next required phase in the same turn.

An ordinary request, generic `continue`, artifact presence, unrelated answer,
new session, or broken conversation is not a start or resume. A new session
requires a fresh explicit start and reconstruction from repository evidence.

## Contract

An explicit start authorizes planning, ticket-level implementation,
verification, review, and verified current-branch unit commits within the
current source scope. It does not authorize push, PR, merge, tag, release,
publish, history rewriting, or out-of-scope mutation; it authorizes only the one post-verification `tk-reflect` tail defined in the phase invariants.

Prefer the latest explicit source and revalidate artifacts as defined by the
phase invariants. Do not create drive-only or global state.

Follow [phase invariants](references/phases.md). Drive owns orchestration;
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and `tk-implement` respectively
own decision closure, spec, ticket decomposition, and one implementation unit.
`tk-to-spec` is mandatory on every active drive run before the ticket decision
or implementation. There is no small-task exception; task size and
proportionality affect only whether a ticket ledger is justified.

Invoke only owners allowed by the phase invariants. Propagate an unavailable or
unsuccessful phase and never recreate it inline. Before each handoff, record
`Success state` and one `Outstanding transition`; success must echo
`Return to: tk-drive` and that transition verbatim. A missing or mismatched echo
is receipt drift and `Blocked`; a valid success triggers its same-turn
transition. Keep the active turn live until that transition executes: only initial SSOT ambiguity, a newly evidenced user-owned decision, `Pending | Blocked | Fail | Unverifiable`, receipt drift, an explicit user stop, inaccessible terminal evidence, or the final drive receipt returns control; `Ready | confirmed | Pass`, progress, task size, and partial results never do, and no commentary, summary, confirmation request, receipt echo, or final response may intervene.

### 🔴 HARD GATE · source UI writing

For every string literal rendered in UI, freeze an inventory before spec
mutation; labels, copy, numbers, units, currency, suffixes, and separators are
examples, not an upper bound. Map source location, non-empty source literal,
current rendered/source-path literal, target literal, spec R/AC, optional
ticket, and implementation destination.

Missing source/current evidence is `Unverifiable`. Any source↔current mismatch
makes every row a conflict candidate and prevents `Ready`, `Pass`, or commit without
a user decision. A typo requires rechecking all same-kind tokens; never generalize
source unreliability to adopt current code silently.

Approval covers only the asked axis; option premises remain unconfirmed. Only exact
separately approved wording is an `authorized change`; prohibit all other drift.

Compare the inventory exactly through spec, tickets, implementation,
candidate/staged diff, and rendered UI; drift or evidence gaps block commit.

### 🔴 HARD GATE · risk-based verification profile

During preflight, select material risk signals only from source-located request/repository evidence. Follow the canonical signal-to-obligation mapping and ordering in [phase invariants](references/phases.md); do not use a score, severity ranking, task label, or unsupported possibility as evidence.

With no material signal, keep the baseline path silent: create no risk artifact or profile section and add no reviewer, browser run, compatibility command, or user-facing default. With any material signal, freeze only `Signals`, source-located `Evidence`, derived `Obligations`, and `Unverified` before the spec handoff, then carry that compact profile through existing handoff envelopes.

Drive classifies and reconciles the profile but never chooses a phase owner's commands, browser route, test seam, or review method. Required inaccessible non-user-owned evidence is `Unverifiable` before implementation; only a genuinely user-owned authority or intent gap may use the existing decision owner. Never drop or weaken an obligation to continue.

Reject orchestration shortcuts: invoke owners instead of recreating their work or accepting prose receipts; slice tickets by independently verifiable behavior instead of phases, files, or commands; freeze source-located signals instead of inflating risk; and reconcile current aggregate evidence instead of replaying child evidence.

## Workflow

1. `preflight`: resolve the complete source per phase invariants, relevant
   artifacts/instructions, Git and dirty ownership, task identity, completed
   phases, unresolved decisions, and the evidence-based verification profile.
2. `decision phase`: when any unresolved user-owned decision prevents a Ready
   spec, explicitly hand current source, evidence, confirmed decisions, and
   open decisions to `tk-grill-me`. Skip this phase when the source is already
   sufficient. Continue only from its `confirmed` receipt.
3. `spec phase`: explicitly hand current source, confirmed decisions, and
   traceability to `tk-to-spec`; accept only a `Ready` receipt, then make the
   ticket decision in the same active turn. Run this phase for every task,
   including trivial and single-slice work.
4. `ticket decision`: use `tk-to-tickets` only for at least two independent
   vertical slices or material ledger value. Otherwise create no ticket/ledger
   and carry task identity plus Ready R/AC as one no-ticket unit.
5. `prototype branch`: only when unresolved web visual ambiguity affects
   behavior or structure and 2–3 disposable alternatives materially narrow
   one decision.
6. `implementation commits`: keep at most one ticket `in_progress`; hand one
   ticket and its R/AC, or the one no-ticket unit, to `tk-implement`. Mark it
   `verified` only from the matching verified commit receipt, then hand off the
   next unit or enter aggregate verification.
7. `aggregate verification`: reconcile all unit receipts, commit ancestry,
   R/AC coverage, cross-ticket interaction, and every frozen material
   verification obligation; run the broadest executable relevant verification
   once. Do not repeat each ticket's line-level Standards/Spec review.
8. `corrective cycle`: for one isolated final change-related regression,
   create at most one corrective ticket through `tk-to-tickets`, run
   `tk-implement` once, and rerun broad verification once. Otherwise stop
   product mutation.
9. `reflection tail/report`: after product `Pass`, follow the phase invariant to reflect exactly once and report product versus final HEAD.

At any downstream phase, only a native receipt with
`User decision: required` and a newly identified user-owned decision returns
control to drive. Hand it to `tk-grill-me`; after `confirmed`, re-run
`tk-to-spec` to `Ready` before tickets. A repeated or equivalent blocker after
that confirmation is `Blocked`, not another automatic loop.

## 🔴 CHECKPOINT · 🛑 STOP · decision handoff

Drive does not reproduce grill questions. A non-confirmed grill receipt stops;
`confirmed` merges only cited Decisions and resumes at the spec gate. An
unrelated answer gains no commit authority and requires a new explicit start.

## Failure and completion

Missing source/authority, receipt drift, or a decision that cannot be routed is
`Blocked`. A child verification or commit failure is `Fail`; inaccessible
evidence is `Unverifiable`. Preserve valid diffs and verified commits, stop the
next handoff, and never rewrite history. Only an isolated final
change-related regression permits the one corrective cycle defined in the
phase invariants.

Lead with `Outcome: <one user-facing sentence>`, then `Implemented` with two to seven behavior-level bullets and `Verification` with one to four aggregate-result bullets; these are budgets, not quotas. If there are eight or more results, show the top five to seven and cite the owning spec, ticket, implementation, or reflection ledger. Include `Reflection`, `Skill candidates`, and `Remaining risks` only when meaningful; omit reflection no-op, zero candidates, empty risks, skipped phases, and no-ticket placeholders.

For multiple tickets, place a compact `Ticket | Outcome | Commit` table before a compact Receipt. Use a sentence when only one user-relevant row exists; rows are vertical slices, never phases/files/commands. Receipt starts with the Outcome sentence and owns required `Status`, `Source`, phase/ticket IDs, product and reflection commits, ledger paths, and provenance without replacing or repeating result rows. Use `Status: Pass` only after every completion gate.

Return control only with that final receipt or an explicit phase-stop receipt;
first assert that every consumed success receipt has its next transition.
Reference child receipts instead of copying their evidence; never expose a child handoff envelope or invoke reflection outside the successful drive tail.

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, receipt keys, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose receipt value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or receipt. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required schema field repeats a result already stated, keep the field but make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, summary, or receipt, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose receipt value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, receipt keys, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
