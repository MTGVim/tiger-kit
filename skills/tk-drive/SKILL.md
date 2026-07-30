---
name: tk-drive
description: "[user] Consume one sealed TigerKit preparation and orchestrate its frozen implementation units through verified commits, aggregate verification, reflection, and terminal prep state. Use only when selected explicitly without a raw source."
disable-model-invocation: true
argument-hint: "<no source; consumes .tigerkit/prep.md>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user selects `/tk-drive`, `$tk-drive`, or the host skill
picker without a source argument. An active invocation may continue across its
direct child receipts in the same conversation.

When the invocation contains a raw source, request, issue, spec, ticket, or
other preparation input, stop without reading it as drive authority and emit
exactly:

`Status: Blocked`
`Reason: tk-drive consumes a sealed TigerKit prep, not a raw source.`
`Next: /tk-prep <source>`

Use the same result when `.tigerkit/prep.md` is missing. An ordinary request,
generic continuation, terminal or active manifest, unrelated answer, new
session, or broken conversation is not a start or resume.

## Contract

An explicit prepared start authorizes implementation, verification, review,
and one verified current-branch unit commit per sealed unit. It authorizes
only the one post-verification `tk-reflect` tail defined in
[phase invariants](references/phases.md). It does not authorize preparation,
new decisions or scope, push, PR, merge, tag, release, publish, history
rewriting, or out-of-scope mutation.

Before implementation, use the skill-local `scripts/prep_state.py claim`
command to strictly validate freshness and atomically change the exact
manifest from `ready` to `active`. Never import or invoke a script from
`tk-prep`; the drive-local script alone owns validate, claim, and finalize.
Only the successful claim identity may execute or finalize the run.

Drive consumes the sealed spec, tickets/no-ticket mode, verification profile,
task identity, R/AC, dirty ownership, and unit order. It does not invoke
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, or `tk-prototype` for initial or
corrective preparation, and it never recreates their work inline. Any new
scope, ticket, user decision, source amendment, or preparation drift ends this
run and requires a new `/tk-prep <source>`.

Prepared drive may invoke only `tk-implement` and the single allowed
`tk-reflect` tail.
It must not invoke `tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, or
`tk-prototype` during initial or corrective execution.

Follow [phase invariants](references/phases.md). `tk-implement` owns one
implementation or corrective unit. `tk-reflect` owns the single successful
tail. Before each child handoff, record `Success state` and exactly one
`Outstanding transition`; consume success only when it echoes
`Return to: tk-drive` and that transition verbatim. A missing or mismatched
echo is receipt drift and cannot authorize the next transition.

When both `TK_DRIVE_EVENT_RECORDER` and `TK_DRIVE_EVENT_LOG` are present in
an evaluation-owned environment, invoke the recorder immediately before each
allowed phase with `phase_invocation <phase>`, then immediately after each
matching successful receipt with
`phase_receipt <phase> Pass <Outstanding transition>`. Recorder failure makes
the live evidence `Unverifiable`; never fabricate or backfill an event. Do not
record outside that conditional evaluation environment.

### 🔴 HARD GATE · source UI writing

Consume the sealed source UI writing inventory from the Ready spec. Do not
reconstruct, weaken, or extend it. Map every selected literal through its
frozen R/AC, prepared unit, implementation destination, candidate/staged diff,
and rendered UI. Missing current evidence, an unprepared mismatch, or wording
outside the sealed authorized change is `Unverifiable | Blocked` before
commit. Approval remains limited to the exact axis and literal recorded by
preparation; only the sealed `authorized change` may differ.

### 🔴 HARD GATE · risk-based verification profile

Consume the sealed material profile and verify that its exact obligations are
covered by unit and aggregate evidence. Do not select signals, add unsupported
obligations, remove an obligation, create a new profile artifact, or choose a
phase owner's commands, tests, browser route, or review method. A missing,
drifted, or inaccessible required obligation is `Unverifiable`; a baseline
profile adds no user-facing ceremony.

## Workflow

1. `prepared preflight`: reject any raw input; locate the exact manifest;
   inspect branch, HEAD, worktree, instructions, dirty inventory, referenced
   spec/tickets, and verification profile; invoke the drive-local claim command
   with current canonical inventories. Do not mutate product files before a
   successful claim.
2. `load units`: reread the now-`active` manifest and referenced artifacts.
   Freeze the prepared unit order and one current `in_progress` unit. A
   no-ticket prep is exactly one unit.
3. `initial implementation`: hand each prepared unit and its frozen R/AC to
   `tk-implement`. Mark it verified only from the matching commit receipt,
   then execute the next-unit or aggregate transition in the same active turn.
4. `aggregate verification`: reconcile all receipts, commit ancestry, R/AC,
   cross-unit behavior, source UI inventory, and material obligations; run the
   broadest relevant executable verification once.
5. `corrective cycles`: after the complete initial implementation, permit at
   most three corrective cycles. Each cycle must isolate one change-related
   defect inside the frozen R/AC, hand one corrective unit to `tk-implement`,
   and rerun affected plus aggregate verification. A fourth cycle, repeated or
   unisolated failure, new scope, new ticket, or user decision stops mutation.
6. `reflection tail`: after product `Pass`, invoke `tk-reflect` exactly once
   in drive-optimistic mode and reconcile its result without weakening product
   evidence.
   Drive must reflect exactly once and never enter this tail before product
   `Pass`.
7. `finalize`: while owning the same claim, call the drive-local state script
   with `completed` only after product and reflection completion; otherwise
   use the evidence-supported `invalid | failed`. Strictly reread terminal
   state before any user summary.
8. `report`: emit the compact behavior and verification result. Never append
   the machine header, child handoff envelope, phase provenance, or a bottom
   metadata block.

## Correction boundary

The initial implementation does not consume a corrective cycle. Number
post-initial corrections `1`, `2`, and `3` in the implementation ledger. A
correction may change only files and behavior needed to satisfy already
frozen R/AC. It cannot add an R/AC, ticket, migration choice, product decision,
or new feature.

The initial implementation consumes zero corrective cycles.
At most three post-initial corrective cycles are permitted inside frozen R/AC;
a fourth cycle or any scope, ticket, or decision expansion stops mutation.

Stop after cycle three even when another fix appears obvious. Finalize
`failed` for a verified change-related product failure, `invalid` for scope,
identity, or preparation drift, and preserve `active` only when terminal
evidence is inaccessible and changing it would fabricate state. Report the
one recovery action: prepare the revised source or inspect the retained run.

## Failure and completion

Missing/raw input, non-Ready state, claim loss, identity drift, or out-of-scope
work is `Blocked` or `Unverifiable` as supported by evidence. A child
verification, commit, corrective-limit, aggregate, reflection-restoration, or
state-write failure is `Fail`. Preserve valid diffs and verified commits,
never rewrite history, and finalize whenever terminal evidence is available.

Lead with one user-facing result sentence, then `Implemented` with two to seven
behavior-level bullets and `Verification` with one to four aggregate-result
bullets; these are budgets, not quotas. If there are eight or more results,
show the top five to seven and cite the owning spec, ticket, implementation, or
reflection ledger. Include `Reflection`, `Skill candidates`, and
`Remaining risks` only when meaningful.

For multiple units, place a compact `Ticket | Outcome | Commit` table before
`Verification`. Use a sentence when only one user-relevant row exists; rows
are prepared vertical slices, never phases, files, or commands. End
`Verification` with the single required `Status: Pass` line only after the
manifest rereads `completed`. A non-success result leads with its one status,
reason, and recovery; do not add another status or receipt block.

Return control only with that terminal summary or an explicit phase-stop
result; first assert that every consumed success receipt has its next
transition.
Immediately before emitting terminal `---`, run the transition-debt check.
Terminal output is prohibited while any consumed successful receipt still has
an unexecuted `Outstanding transition`; execute the recorded transition in the
same active turn or return the one evidence-supported non-success state.
Reference child receipts internally instead of copying their evidence; never
expose a child handoff envelope or invoke reflection outside the successful
drive tail.

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose result value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or result. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required field repeats a result already stated, make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Before the first line of every terminal user-facing response, emit exactly one standalone `---` line, then begin immediately with the skill's canonical result heading or result sentence. Do not emit this separator in progress commentary or between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

In prepared drive, a new product decision never reaches this question
surface: finalize the run as `invalid`, return `Blocked`, and route recovery
through `/tk-prep <source>`.

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
