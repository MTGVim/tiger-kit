---
name: tk-ask-repo
description: "[user] Answer an inbound question about this repository with source-located evidence — where a value comes from, how a flow works, whether something exists, what a change breaks, or which layer owns a problem. Use when a question arrives from outside the codebase and answering it requires investigation. Do not use to implement, to close decisions, or to estimate effort."
disable-model-invocation: true
argument-hint: "<the inbound question, pasted verbatim>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Ask Repo

Read-only investigation desk for questions that arrive from outside the
codebase. Classify the question, apply the matching traversal, enforce one
evidence contract, and hand off anything this skill does not own.

Never edit source, spec, tickets, or commits. Never invoke a sibling phase
owner. When the answer requires a user decision, name the decision and stop.
When the answer is settled and an artifact is wanted, name the next owner.

## Contract

**Every claim carries `path:line`, or is marked `unavailable` with the
reason.** An unsourced statement about repository state is not an answer.

**A declaration is not an origin.** A type, schema, column, or interface says a
value exists; it does not say what the value means or how it is produced.
Descend to the expression that assigns it.

**Preserve the asker's wording.** Quote the reported symptom, label, or term
verbatim before normalizing it. The exact string is usually the only reliable
search anchor, and rewording it loses the anchor.

**Never report an unverified state as absent.** "Not found by my search" and
"does not exist" are different claims. Report the first; earn the second.

**Sweep before reporting** (families A, D, E). A fix list without an explicit
`Must not change` section is invalid — state `none found` rather than omitting
it.

## Workflow

1. `classify`: assign the question to A/B/C/D/E below. Mixed questions
   decompose; answer each part and say which is blocking. Out of scope
   (implementation, decision, effort estimate, general knowledge) → name the
   right owner and stop.
2. `anchor`: recover a concrete starting point from the asker's own words — a
   visible string, identifier, route, endpoint, or symbol. No anchor found →
   report the searches attempted as `Unverifiable`; do not guess a synonym and
   proceed as if it matched.
3. `traverse`: run the family's traversal below. Each hop records `path:line`.
4. `sweep` (A, D, E): find every consumer of the value or symbol across all
   surfaces — other screens, notifications, exports, reports, jobs, tests.
   Classify each `must change | must not change | unclear`. Never silently
   include or exclude.
5. `attribute` (A, E): decide ownership from what the transport already
   carries.
   - correct value **already present** in the response or payload → consuming
     side only; no producer change
   - correct value **absent**, or the assignment itself is wrong → producer
     change; name the type and the field
   - both → split, state which blocks the other
6. `verify`: before reporting, record the refs and anchor/query variants
   searched, verify any matching semantics used for scope, and confirm every
   traversal hop is cited. For A/D/E, also record sweep exclusions and any
   dynamic-dispatch coverage.
7. `report`: emit the output contract. Do not propose a diff.

### Family traversals

**A · Value** — anchor (visible string) → bound identifier (column id, key,
prop) → the expression producing it on the consuming side → transport field →
declaring type → **assignment site**. At the assignment site, read siblings and
comments: when an adjacent field on the same record holds the intended value,
that sibling is the likely answer, and its comment is often the only written
record of the distinction. Recurse when the assignment reads another computed
value; stop at a literal, a stored column, or an external input.

**B · Structure** — anchor (entry point) → each hop in order, naming the
boundary crossed (view→transport, transport→producer, producer→store,
producer→external). Report the path, not a narrative. Mark hops that are
dynamically dispatched.

**C · Existence** — search the *current* base ref directly, not a local checkout
that may lag. Then search in-flight work (open changesets, unmerged branches)
before concluding absence. Distinguish four states, which look alike and are
not: absent · present but unreleased to this environment · present but
returning empty or placeholder data · present and live. For "since when", trace
the introducing change and quote it.

**D · Impact** — anchor (symbol, field, or pattern) → all readers and writers →
classify as in `sweep`. Count with a tool whose matching semantics you have
verified on this host; a count that decides scope must not come from a pattern
you have not sanity-checked. State what the count excludes.

**E · Attribution** — trace the consuming side to its end *before* attributing
to the producer; an intermediate transform on the consuming side is the most
common false attribution. For environment-dependent symptoms, compare the
same code path across environments before treating it as a code defect. For
"why is this not visible", check permission, feature gating, and conditional
rendering before concluding the element is missing.

## Failure paths

| Trigger | Action | Still unresolved |
|---|---|---|
| anchor string not found | try its parts, message/i18n catalogs, and the identifier the asker quoted | `Unverifiable` listing the searches run |
| source unreadable | record path + reason as `unavailable` | answer only what readable sources prove; do not infer across the gap |
| two candidate answers, both defensible | present both with evidence and stop | `Blocked` — one decision, named owner |
| sweep finds an unclear consumer | list under Remaining concerns | never silently include or exclude |
| question is really a decision, a build request, or an estimate | name the owner and stop | do not partially perform it |
| asker's premise contradicts the code | report the contradiction; do not answer the premise as stated | `Blocked` |

## Output contract

Lead with `Answer`. For one result, use one to three short paragraphs. For two to seven results, use compact bullets or one question-family table. For eight or more, show the top five to seven and cite the evidence paths that own the remainder; never invent an artifact. Add only the non-empty evidence
sections needed for the question family: `Evidence`, `Origin`, `Sibling
fields`, `Path`, `State`, `Attribution`, `Must change`, `Must not change`, and
`Remaining concerns`. Evidence cites `path:line`; unavailable sources include
the reason. For A/D/E, `Must not change` is required and says `none found` when
empty.

For multiple meaningful fields, consumers, or candidates, use one compact table with question-family columns. Use a sentence when only one user-relevant row exists; rows never represent files, commands, or raw evidence. These are
budgets, not quotas.

Do not echo the inbound question or repeat evidence across sections. `Receipt`
starts with `Outcome: <one user-facing sentence>`; remaining fields are `reported | Blocked | Unverifiable`, next owner, and section references.
It indexes status/provenance, never answer or result rows.

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, receipt keys, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose receipt value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or receipt. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required schema field repeats a result already stated, keep the field but make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, summary, or receipt, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose receipt value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, receipt keys, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

Normal investigation does not make this skill the decision owner: name the
decision and stop as `Blocked`. Only when an authorized caller separately
makes this skill the user-decision owner, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
