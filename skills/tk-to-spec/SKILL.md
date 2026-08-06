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

Use only for explicit implementation-spec artifact request or exact active
`tk-drive` spec handoff. Do not start interview, create tickets, publish remote
issue, or implement.

Source precedence: user-designated source, confirmed decisions, cited
documents/tickets, relevant code, then existing `.tigerkit/spec.md`.

## Workflow

1. **Collect** — read complete selected source; record access failures.
2. **Map** — map each claim to source location and `verified | unverified`.
3. **Separate** — distinguish facts, decisions, assumptions, hypotheses, and
   unresolved conflicts; preserve source IDs or assign stable `R#` and `AC#`.
4. **Prior art** — for each relevant item choose exactly
   `adopted | already-satisfied | not-applicable | conflict`, with evidence,
   semantic reason, and R/AC mapping. A `conflict` prevents `Ready`. Omit
   `## Prior art` when none exists.
5. **Specify** — define problem, goal, included/excluded scope, requirements,
   acceptance criteria, verification, source traceability, and material execution
   strategy. Classify `PR evidence` as `required | optional | N/A`: `required`
   only for confirmed attached-visual-proof requirements or browser-rendered AC
   that code and checks cannot communicate meaningfully; `optional` when
   screenshot merely helps review; `N/A` without browser-visible result. Do not
   promote browser verification alone into required PR evidence.
6. **Slice candidates** — record `Vertical slicing candidate areas` by
   user-visible behavior, R/AC coverage, and coupling evidence. These are inputs,
   not tickets or approved slice boundaries.
7. **Gate and write** — return `Ready | Draft | Blocked | Unverifiable`, write
   only supported state, reread it, verify source map and IDs.

For bugs, separate symptom, current behavior, expected behavior, reproduction,
observed evidence, environment, regression seam, and cause/solution hypothesis.
Unreproduced cause is `unverified`, not decision.

## Ready contract

Use `Ready` only when every required element exists, source traceability is
complete, verification executable or evidence-defined, and no unresolved
conflict remains. Otherwise:

| State | Meaning |
| --- | --- |
| `Draft` | Required content or an assumption remains unresolved |
| `Blocked` | Confirmed sources conflict or a user decision is required |
| `Unverifiable` | Required source or exact comparison evidence is inaccessible |
| `Fail` | Writing or post-write validation produced a known invalid result |

Active-drive non-Ready result passes native state, evidence, and
`User decision: required | none` directly to graph. Do not invoke
`tk-grill-me`, create substitute spec, or choose next node. Ready handoff passes
artifact path and R/AC IDs directly to next applicable graph node.

## Execution strategy

Every Ready spec includes `## Execution strategy` for PR-evidence decision;
include other prerequisites only when material. Preserve confirmed
implementation/verification route and safe recovery conditions.
For selected browser evidence, retain required/optional mode, target environment,
Guard/Verdict, account role or tenant, opaque profile hint, auth expectation,
safe interaction boundary, and `intentionally omitted → re-request on cold
start`. Never store identity, credentials, cookies, tokens, OTPs, or profile
contents.

Every Ready spec records exactly `PR evidence: required | optional | N/A` under
`## Execution strategy`; `required` and `optional` also record one review-facing
criterion. Missing or ambiguous material input prevents `Ready`, never silently
defaults to `N/A`.

## Source UI writing

When source material defines rendered text, freeze source-map inventory before
`Ready`: source location, non-empty source literal, current rendered/source-path
literal, target literal, and owning R/AC. Preserve spelling, case, spacing,
punctuation, symbols, numbers, units, and meaningful line breaks unless user
explicitly authorizes wording change.

Missing source/current evidence is `Unverifiable`; source↔current mismatch is
conflict candidate and blocks `Ready`. Mark only explicitly approved wording as
`authorized change`. Do not translate, paraphrase, normalize, or silently fix
typos.

## Output

Write to `--output`, print only for `--print-only`, otherwise atomically replace
`.tigerkit/spec.md`. Preserve valid decisions for same task; do not create
archives or modify `.gitignore`. Reread result before reporting.

Lead with `Ready | Draft | Blocked | Unverifiable` decision. For a standalone
Ready result, make the non-advancing handoff visible as
`🙋 spec · Ready · 다음 단계 수동`; an active drive owns the parent display
`drive > spec` and immediately consumes a valid Ready handoff. Summarize core
scope, requirements, and exceptions in two to five short bullets; for single
result use one to three short lines. For larger inventory, show top five to seven
items and cite artifact. Artifact owns full R/AC, source map, prior-art
dispositions, candidate areas, conflicts, and verification. Active prep receives
only internal phase/status/path/R/AC handoff.

### 🔴 HARD GATE · terminal user summary

Terminal response excludes progress/internal evidence. Begin with canonical
result heading or sentence; no preamble, receipt heading, `Outcome:` label,
duplicate status, or active-drive child summary. Detailed provenance belongs only
in owned spec artifact.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When progress or a nonterminal status is shown, use these compact markers: `🚗 active work`, `🙋 response/approval needed`, `❓ genuinely ambiguous question`, `⏳ CI/remote/re-review wait`, `🛑 checkpoint/abort stop`, `✅ completed row`, and `❌ actual failure`. Put one space after every emoji marker, omit generic no-op rows, show one legend before tables, and omit duplicate English status text in rows; preserve any required terminal `Status: <token>`.

Use latest explicit user language, else current message's language. Preserve
canonical headings, status tokens, IDs, commands, paths, code, and quoted source
literals exactly. Rewrite free-form language drift before return.

## User decision questions

For material user-owned decision only: ask one self-contained `Question`, then
show `Recommendation`, two or three exclusive options, and exactly one
`(Recommended)` or `(추천)` label. Render directly in chat, never via structured
question/input tool. Preserve `Pending | Blocked` until answer.

## Pitfalls

- Do not mix facts, decisions, assumptions, and hypotheses without source map.
- Do not renumber stable R/AC IDs or reuse deleted IDs.
- Do not mark missing, conflicting, or inaccessible evidence `Ready`.
- Do not create tickets or implement from non-Ready spec.
## Progress

At meaningful work boundaries, standalone output uses `🚗 to-spec · <short state>`; use `🙋 to-spec · 응답 필요` for a question/approval gate, `⏳ to-spec · 대기` for CI/remote/re-review wait, and `🛑 to-spec · 중단` for a checkpoint/abort stop. Omit `tk-` from display names; a parent owns `🚗 parent > to-spec`. Keep terminal `Status: <token>` unchanged.
