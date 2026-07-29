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

Use only non-empty sections. `Must not change` is always present for A/D/E.

- `Question`: the inbound question verbatim, and its family
- `Answer`: the conclusion, in one to three sentences, before any detail
- `Evidence`: `path:line` per claim; `unavailable` entries with reasons
- `Origin` (A): assignment site and what the value actually means
- `Sibling fields` (A): same-record alternatives and their documented meanings
- `Path` (B): ordered hops with boundaries named
- `State` (C): absent | unreleased | empty | live, with the refs searched
- `Attribution` (A, E): which side owns it, and the evidence for that
- `Must change`: table of `path:line` · identifier · current → intended
- `Must not change`: consumers already correct, and why. `none found` when
  empty.
- `Remaining concerns`: unclear consumers, unreadable sources, open decisions
- `Receipt`: `reported | Blocked | Unverifiable`, and the next owner

Write user-facing prose in the user's language; keep identifiers and status
tokens as-is.

## Related

The related rules own axis-specific traps; this skill owns the intake desk,
classification, routing, shared evidence contract, and consumer sweep:

- [Producer-existence verification](https://github.com/MTGVim/tiger-kit/issues/196#%EA%B8%B0%EC%A1%B4-%EC%9E%90%EC%82%B0%EA%B3%BC%EC%9D%98-%EA%B4%80%EA%B3%84)
- [Response-field type and nullability verification](https://github.com/MTGVim/tiger-kit/issues/196#%EA%B8%B0%EC%A1%B4-%EC%9E%90%EC%82%B0%EA%B3%BC%EC%9D%98-%EA%B4%80%EA%B3%84)
- [Consumer-chain attribution](https://github.com/MTGVim/tiger-kit/issues/196#%EA%B8%B0%EC%A1%B4-%EC%9E%90%EC%82%B0%EA%B3%BC%EC%9D%98-%EA%B4%80%EA%B3%84)

## User decision questions

Normal investigation does not make this skill the decision owner: name the
decision and stop as `Blocked`. Only when an authorized caller separately
makes this skill the user-decision owner, ask exactly one question at a time.
Render `Question` before `Recommendation` and the proposals. Offer
two or three mutually exclusive proposals and state the material tradeoff of
each. Make `Question` self-contained: summarize the
evidence-derived context, decision impact, and unresolved axis in user-facing
language before asking. It must not require the user to decode raw `Evidence`.
Mark exactly one best recommendation by ending its label with a localized marker such as
`(Recommended)` or `(추천)`. A host-generated custom or Other choice does not
count as an authored proposal.

When the active question tool exposes
option previews, prototype cards, or equivalent rich choice surfaces and a concrete preview can clarify the
decision, use it proactively. Do not invent unsupported fields or use this
presentation rule to bypass existing prototype or phase boundaries.

If the current execution context exposes a native structured user-input tool,
the skill must call that tool. Plain-text questions are allowed only when no
such tool is exposed. A failed or rejected tool call is not tool absence: report
the failure and preserve the pending or blocked state instead of silently
downgrading to prose. Host examples:

- Claude Code: `AskUserQuestion`
- Codex: `request_user_input`
- Hermes Agent: `clarify`

This contract changes question presentation only. It does not grant new
decision authority or weaken any existing stop, approval, or phase boundary.

## DO NOT / ANTI-PATTERNS

- Do not edit source, create a spec, ticket, commit, or open a branch.
- Do not treat a type or schema declaration as an origin.
- Do not report absence from one search, or a count from an unverified pattern.
- Do not report for A/D/E before the sweep, or omit `Must not change`.
- Do not resolve a two-candidate ambiguity yourself.
- Do not estimate effort or schedule; report scale (sites, files) only.
- Do not invoke another user-invoked skill; name the next owner instead.
