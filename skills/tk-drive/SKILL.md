---
name: tk-drive
description: "[user] Prepare an explicit source and continue automatically through sealed implementation, verified unit commits, aggregate verification, and reflection in one active run. Use only when selected explicitly with a source, or when resuming this skill's pending decision in the same conversation."
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
in the same conversation. An ordinary request, generic continuation, manifest
presence, terminal run, or new session is not a start or resume.

Drive has two explicit internal stages:

```text
Preparing → Executing
```

Preparing may invoke `tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and
`tk-prototype`. Executing may invoke `tk-implement` and the single successful
`tk-reflect` tail. Phase owners never invoke sibling phase owners. Drive owns
every transition between them.

## Contract

An explicit start authorizes preparation, implementation, verification,
review, one verified current-branch unit commit per prepared unit, up to three
corrective unit commits, and the one post-verification reflection tail. It
does not authorize push, PR, merge, tag, release, publish, history rewriting,
or out-of-scope mutation.

Preparing binds the source and task identity, repository/worktree state,
instructions, dirty ownership, resolved decisions, Ready spec, ticket or
no-ticket mode, source UI writing inventory, verification profile, prior-art
dispositions, and cold-start reconstruction evidence. It writes and strictly
rereads the internal worktree-local `.tigerkit/prep.md`, activates it through
the drive-local state script, and continues into Executing in the same active
run. Never ask for another implementation confirmation after Ready.

Use only drive-local [manifest](references/manifest.md) and state scripts.
Never import a script from another skill, create global TigerKit state,
archive manifests, create current pointers, or modify a consumer repository's
`.gitignore`. Warn when `.tigerkit/` is not ignored.

Follow [phase invariants](references/phases.md). Before every child handoff,
record `Success state` and exactly one `Outstanding transition`; consume
success only when it echoes `Return to: tk-drive` and that transition
verbatim. A missing or mismatched echo is receipt drift and cannot authorize
the next transition.

When both `TK_DRIVE_EVENT_RECORDER` and `TK_DRIVE_EVENT_LOG` are present in
an evaluation-owned environment, invoke the recorder immediately before each
allowed phase with
`"$TK_DRIVE_EVENT_RECORDER" phase_invocation <phase>`, then immediately after
each matching successful receipt with
`"$TK_DRIVE_EVENT_RECORDER" phase_receipt <phase> Pass "<Outstanding transition>"`.
The recorder reads the log path from its environment. Do not pass
`TK_DRIVE_EVENT_LOG` as a command argument. Recorder failure makes the live
evidence `Unverifiable`; never fabricate or backfill an event.

### 🔴 HARD GATE · source UI writing

During Preparing, inventory every user-visible source literal and freeze its
`authorized change` in R/AC. During Executing, map every selected literal through
the prepared unit, candidate/staged diff, and rendered UI. Missing current
evidence, an unprepared mismatch, or wording outside the sealed authorization
is `Unverifiable | Blocked` before commit.

### 🔴 HARD GATE · risk-based verification profile

During Preparing, classify the material signals and obligations before
selecting verification. Consume the sealed material profile during Executing
and verify that its exact frozen profile is covered by unit and aggregate
evidence. Drive cannot add unsupported obligations, remove an obligation, or
substitute a weaker signal.

### 🔴 HARD GATE · material strategy preflight

During Preparing and before product mutation, inspect the implementation and
verification strategy. Resolve repository-evidenced and implementation-owned
facts without asking. Ask through `tk-grill-me`, one at a time, only for a
material user-owned choice that can change behavior, scope, acceptance,
verification authority, target environment, permissions, or safe execution.
Do not ask about ordinary tool or implementation details.

For user-visible web UI or browser-relevant behavior, classify browser
evidence as `required | optional | N/A`. When it is required, or optional and
selected, freeze the target URL/environment, Guard/Verdict mode, account role
and tenant, `isolated` or opaque profile hint, authentication expectation,
safe interaction boundary, and unavailable runtime inputs. Persist only
non-identifying hints. Mark an exact account or profile identity that must not
be stored as `intentionally omitted` with `re-request on cold start`; never
persist credentials, cookies, tokens, OTPs, or profile contents. Re-requesting
that confirmed runtime input before browser launch is not a Preparing amendment.
When browser evidence is `N/A`, add no browser question or artifact ceremony.

## Preparing

1. `identify`: bind the complete source, stable task ID and anchors,
   repository root, worktree, branch, base HEAD, applicable instructions, and
   initial dirty inventory. Preserve pre-existing user work as excluded
   ownership.
2. `inspect`: read the source and current repository evidence. Gather at most
   seven task-related prior-art items anchored to the task ID, source
   references, and symbols. Search applicable rules, ADRs, tests, types, lint,
   CI, repository skills, and code invariants. Exclude raw sessions, prior
   implementation or reflection scratch, pending drafts, arbitrary global
   state, unrelated work, and inaccessible host-only rules. No relevant prior
   art is a silent no-op.
3. `strategy/profile`: inspect the material implementation and verification
   strategy, classify conditional browser evidence, and freeze the confirmed
   non-sensitive execution hints, signals, and obligations.
4. `decide`: invoke `tk-grill-me` only for unresolved user-owned decisions.
   Stop on `Pending | Blocked | Unverifiable`; never infer approval.
5. `specify`: invoke `tk-to-spec` with source evidence, decisions, prior-art
   candidates, source writing inventory, and verification profile. Continue
   only from an exact Ready receipt that returns to drive and echoes the
   recorded transition; then reread `.tigerkit/spec.md`.
6. `slice`: decide whether independently verifiable vertical tickets are
   needed. Invoke `tk-to-tickets` when they are; otherwise record one
   no-ticket slice. Invoke `tk-prototype` only when comparison can close a
   remaining design uncertainty, then revalidate the spec.
7. `cold-start gate`: prove that a fresh agent can reconstruct scope, R/AC,
   ownership, obligations, and unit order from repository evidence plus the
   referenced spec and tickets without conversation memory.
8. `seal and activate`: atomically write and strictly reread
   `.tigerkit/prep.md`, validate every digest against current evidence, then
   activate the manifest. Immediately execute the first prepared unit; do not
   emit a terminal Ready summary or ask for confirmation.

## Executing

1. `load units`: freeze the prepared unit order with at most one current
   `in_progress` unit. A no-ticket preparation is exactly one unit.
2. `initial implementation`: hand each unit and its frozen R/AC to
   `tk-implement`. Verify its commit receipt, then execute the next-unit or
   aggregate transition in the same active turn.
3. `aggregate verification`: reconcile all receipts, ordered commit ancestry,
   R/AC, cross-unit behavior, source UI literals, and material obligations;
   run the broadest relevant executable verification once.
4. `corrective cycles`: after the complete initial unit set, permit at most three
   isolated change-related corrections inside frozen R/AC. Each invokes
   one corrective `tk-implement` unit and reruns affected plus aggregate
   verification.
5. `reflection tail`: after product `Pass`, reflect exactly once by invoking
   `tk-reflect` in drive-optimistic mode and reconcile its result without weakening
   product evidence.
6. `finalize`: finalize and strictly reread the internal manifest as
   `completed` only after product and reflection completion; otherwise use
   the evidence-supported `invalid | failed`.

## Late ambiguity

Classify ambiguity discovered during Executing:

1. `Implementation-owned`: it remains inside prepared R/AC; decide and
   continue.
2. `Evidence-resolvable`: investigate repository or runtime evidence and
   continue.
3. `User-owned`: enter one bounded internal Preparing amendment:
   `Executing → tk-grill-me → tk-to-spec revalidation → affected ticket
   rederivation → prep reseal → Executing`.

Allow at most one amendment cycle per run. A repeated equivalent blocker or a
second new user-owned decision is `Blocked`. Never guess a choice that changes
user-visible behavior, scope, acceptance criteria, source interpretation, or
verification authority.

Do not automatically amend, squash, revert, or rewrite verified commits.
Resume only when existing commits remain valid under the resealed R/AC;
otherwise stop `Blocked` and cite the conflicting commit or evidence.

## Correction boundary

The initial implementation consumes zero corrective cycles. Number
post-initial corrections `1`, `2`, and `3` in the implementation ledger. A
correction changes only behavior needed for frozen R/AC. A fourth cycle,
repeated or unisolated failure, new ticket outside the one amendment, or
unresolved decision stops mutation.

## Failure and completion

Missing source, source or identity drift, unresolved preparation, receipt
drift, amendment exhaustion, or out-of-scope work is
`Blocked | Unverifiable` as supported by evidence. A child verification,
commit, correction-limit, aggregate, reflection-restoration, or state-write
failure is `Fail`. Preserve valid diffs and verified commits; never rewrite
history.

Lead with one user-facing result sentence, then `Implemented` with two to seven
behavior-level bullets and `Verification` with one to four aggregate-result
bullets. Include a compact `Ticket | Outcome | Commit` table for multiple
prepared units. Include `Reflection`, `Skill candidates`, and
`Remaining risks` only when meaningful.

Use a sentence when only one user-relevant row exists.

When underlying results exceed these limits, keep only the top five to seven
items ranked by user impact and verification value.

End `Verification` with the single required `Status: Pass` line only after the
manifest rereads `completed`. A non-success result leads with its one status,
reason, and recovery; do not add another status or receipt block.

Return control only with that terminal summary or an explicit phase stop.
Immediately before emitting the terminal user summary, run the transition-debt check.
Terminal output is prohibited while any consumed successful receipt still has
an unexecuted `Outstanding transition`; execute the recorded transition in the
same active turn or return the one evidence-supported non-success state.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks Preparing or the single amendment, ask one
self-contained `Question` before any `Recommendation`. Show only
decision-relevant evidence, two or three mutually exclusive options with
material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`.
