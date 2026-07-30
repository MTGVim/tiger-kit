---
name: tk-to-spec
description: "[user/auto] Turn confirmed decisions and evidence into a Ready implementation spec. Apply to an explicit standalone spec-artifact request or an explicit spec handoff from active tk-drive Preparing; do not apply to ticket decomposition, interviews, remote issues, or implementation requests."
argument-hint: "<conversation, source, or request> [--output <path>|--print-only]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# Write a spec

Use only for an explicit implementation-spec artifact request or an exact active
`tk-drive` spec handoff. Do not start an interview, create tickets, publish a
remote issue, or implement.

Source precedence is user-designated source, confirmed decisions, cited
documents/tickets, relevant code, then an existing `.tigerkit/spec.md`.

## Workflow

1. **Collect** — read the complete selected source and record access failures.
2. **Map** — map each claim to a source location and `verified | unverified`.
3. **Separate** — distinguish facts, decisions, assumptions, hypotheses, and
   unresolved conflicts; preserve source IDs or assign stable `R#` and `AC#`.
4. **Prior art** — for each relevant item choose exactly
   `adopted | already-satisfied | not-applicable | conflict`, with evidence,
   semantic reason, and R/AC mapping. A `conflict` disposition prevents `Ready`.
   When no relevant prior art exists, omit `## Prior art`.
5. **Specify** — define problem, goal, included/excluded scope, requirements,
   acceptance criteria, verification, source traceability, and material execution
   strategy.
6. **Slice candidates** — record `Vertical slicing candidate areas` by
   user-visible behavior, R/AC coverage, and coupling evidence. They are inputs,
   not tickets or approved slice boundaries.
7. **Gate and write** — return `Ready | Draft | Blocked | Unverifiable`, write
   only the supported state, reread it, and verify source map and IDs.

For a bug, keep symptom, current behavior, expected behavior, reproduction,
observed evidence, environment, regression seam, and any cause/solution
hypothesis separate. An unreproduced cause is `unverified`, not a decision.

## Ready contract

Use `Ready` only when every required element is present, source traceability is
complete, verification is executable or evidence-defined, and no unresolved
conflict remains. Otherwise:

| State | Meaning |
| --- | --- |
| `Draft` | Required content or an assumption remains unresolved |
| `Blocked` | Confirmed sources conflict or a user decision is required |
| `Unverifiable` | Required source or exact comparison evidence is inaccessible |
| `Fail` | Writing or post-write validation produced a known invalid result |

An active-drive non-Ready result passes its native state, evidence, and
`User decision: required | none` directly to the graph. Do not invoke
`tk-grill-me`, create a substitute spec, or choose the next node. A Ready handoff
passes artifact path and R/AC IDs directly to the next applicable graph node.

## Execution strategy

Include `## Execution strategy` only when material prerequisites exist. Preserve
the confirmed implementation/verification route and safe recovery conditions.
For selected browser evidence, retain required/optional mode, target environment,
Guard/Verdict, account role or tenant, opaque profile hint, auth expectation,
safe interaction boundary, and `intentionally omitted → re-request on cold
start`. Never store identity, credentials, cookies, tokens, OTPs, or profile
contents.

## Source UI writing

When source material defines rendered text, freeze a source-map inventory before
`Ready`: source location, non-empty source literal, current rendered/source-path
literal, target literal, and owning R/AC. Preserve spelling, case, spacing,
punctuation, symbols, numbers, units, and meaningful line breaks unless the
user explicitly authorizes a wording change.

Missing source/current evidence is `Unverifiable`; a source↔current mismatch is
a conflict candidate and blocks `Ready`. Mark only explicitly approved wording
as `authorized change`. Do not translate, paraphrase, normalize, or silently fix
typos.

## Output

Write to `--output`, print only for `--print-only`, otherwise atomically replace
`.tigerkit/spec.md`. Preserve valid decisions for the same task; do not create
archives or modify `.gitignore`. Reread the result before reporting.

Lead with the `Ready | Draft | Blocked | Unverifiable` decision. Summarize core
scope, requirements, and exceptions in two to five short bullets; for a single
result use one to three short lines. For a larger inventory, show the top five
to seven items and cite the artifact. The artifact owns full R/AC, source map,
prior-art dispositions, candidate areas, conflicts, and verification. Active
prep receives only its internal phase/status/path/R/AC handoff.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of the terminal user response.
Begin with the canonical result heading or sentence. Emit no ceremonial
preamble, receipt heading, `Outcome:` label, duplicate status, or active-drive
child summary. Put detailed provenance only in the owned spec artifact.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current message's language.
Preserve canonical headings, status tokens, IDs, commands, paths, code, and
quoted source literals exactly. Rewrite free-form language drift before return.

## User decision questions

Ask one self-contained `Question` only for a material user-owned decision, then
show a `Recommendation`, two or three mutually exclusive options, and exactly
one `(Recommended)` or `(추천)` label. Use native `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`; plain text is allowed only when
none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`.

## Pitfalls

- Do not mix facts, decisions, assumptions, and hypotheses without a source map.
- Do not renumber stable R/AC IDs or reuse deleted IDs.
- Do not mark missing, conflicting, or inaccessible evidence `Ready`.
- Do not create tickets or implement from a non-Ready spec.
