---
name: tk-prep
description: "[user] Prepare an explicit source into one sealed, cold-start-capable TigerKit manifest after decision, spec, ticket, and verification gates close. Use only when selected explicitly; never implement or consume the prepared work."
disable-model-invocation: true
argument-hint: "<source, request, issue, or existing Ready spec>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Prepare

Start only when the user selects `/tk-prep`, `$tk-prep`, or the host skill
picker with a source. An ordinary planning request, artifact presence, generic
continuation, or a raw `/tk-drive <source>` request is not a preparation start.

This skill owns preparation only. It may invoke `tk-grill-me`, `tk-to-spec`,
`tk-to-tickets`, and `tk-prototype` when their documented gates require them.
It never implements, commits, aggregate-verifies, reflects, pushes, publishes,
or invokes `tk-drive`.

## Contract

Produce exactly one sealed `.tigerkit/prep.md` only after the source and task
identity, repository/worktree state, instructions, dirty ownership, decisions,
Ready spec, conditional ticket decision, verification profile, and cold-start
evidence are complete. Use the skill-local
`scripts/prep_manifest.py create` command for the final atomic write and
strictly reread the resulting document.

The existing manifest is durable runtime state:

- A pending, blocked, failed, or unverifiable preparation writes no manifest.
- An existing `active` manifest blocks replacement.
- A terminal manifest remains diagnostic until a later fully Ready
  preparation atomically replaces it.
- Never archive, rename, or create a current pointer for the manifest.
- Never modify a consumer repository's `.gitignore`; warn when `.tigerkit/`
  is not ignored.

See [Manifest contract](references/manifest.md) for the exact schema and
writer interface. Never replace the local script with a shared runtime.

## Workflow

1. `identify`: bind the explicit source, stable task ID and anchors, repository
   root, worktree, branch, base HEAD, applicable instruction files, and the
   complete initial dirty inventory. Preserve pre-existing user work as
   excluded ownership.
2. `inspect`: read the complete source and current repository evidence. Gather
   only task-anchored prior art allowed by the preparation contract; do not use
   global memory, raw conversation, or unrelated implementation scratch.
3. `profile`: classify material verification signals and obligations before
   selecting verification. Keep this profile stable through preparation.
4. `decide`: invoke `tk-grill-me` only for unresolved user-owned decisions.
   Stop on `pending | Blocked | Unverifiable`; never infer approval.
5. `specify`: invoke `tk-to-spec` with task identity, evidence, decisions,
   prior-art candidates, source writing inventory, and verification profile.
   Continue only from an exact Ready result and reread `.tigerkit/spec.md`.
6. `slice`: decide whether independently verifiable vertical tickets are
   needed. Invoke `tk-to-tickets` when they are; otherwise record the sealed
   no-ticket single-slice mode. Invoke `tk-prototype` only when comparison can
   close a remaining design uncertainty, then update the spec evidence.
7. `cold-start gate`: prove that a new agent can reconstruct scope, R/AC,
   ownership, verification obligations, and unit order from repository
   evidence plus the referenced spec and tickets without conversation memory.
8. `seal`: canonicalize the dirty, instruction, and verification inventories;
   call the skill-local writer with a UTC timestamp; then run its `validate`
   command against `.tigerkit/prep.md`.
9. `return`: expose only the compact Ready result. Do not copy the machine
   header, phase handoffs, provenance, or preparation history into chat.

## Ready and stop gates

Ready requires every item below:

- the source reference and at least one stable task anchor;
- repository root, worktree, branch, and 40-hex base HEAD;
- complete dirty and applicable-instruction inventories;
- a `Status: Ready` spec and either `Status: Pass` tickets or an explicit
  no-ticket single slice;
- a material verification profile with non-empty signals and obligations;
- resolved decisions and cold-start reconstruction evidence;
- a generated manifest that passes strict reread validation.

If any item is absent, return the one evidence-supported
`Pending | Blocked | Unverifiable | Fail` state and preserve the prior
manifest byte-for-byte. A failed atomic replace is `Fail`; never claim Ready
from an in-memory header or temporary file.

## Result

On success, emit exactly:

`Status: Ready`
`Prep: <prep-id>`
`Path: .tigerkit/prep.md`
`Next: /tk-drive`

For non-success, lead with `Status: Pending | Blocked | Unverifiable | Fail`,
then one concise reason and one concrete recovery when available. Use one to
four short lines for a simple result, two to seven preparation findings when
several gates matter, and the top five to seven plus the owning artifact for a
larger set. These are budgets, not quotas. Do not add a receipt heading,
`Outcome:` label, or bottom metadata block.

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

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not write a manifest before every preparation gate passes.
- Do not replace an active manifest or destroy a terminal manifest on failure.
- Do not copy the spec, tickets, source, or prior-art evidence into the
  Markdown body; reference their owners.
- Do not implement, commit, aggregate-verify, reflect, push, tag, or release.
- Do not depend on conversation memory or a shared runtime after sealing.
