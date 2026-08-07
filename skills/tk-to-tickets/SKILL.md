---
name: tk-to-tickets
description: "[user/auto] Decompose a request or Ready spec into independently verifiable vertical tickets. Apply to a clear standalone decomposition request or an explicit ticket handoff from active tk-drive Preparing; do not apply to spec writing, remote issue creation, or implementation."
argument-hint: "<spec, plan, or request> [--output <path>]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# Write tickets

Use only for explicit vertical-ticket decomposition request or exact active
`tk-drive` handoff containing Ready source and decision that tickets are needed.
Do not write spec, publish remote issues, or implement.

Source precedence: user-designated source, current confirmed decisions,
`.tigerkit/spec.md`, selected `.tigerkit/audit.md` `AUD-*` findings, request,
then relevant code.

## Workflow

1. **Extract** — collect source R/AC IDs or source locations; classify
   `confirmed | unverified | conflict`.
2. **Slice** — derive user-visible vertical behaviors. Treat spec candidate areas
   as evidence, not preapproved slices or ticket IDs.
3. **Prove independence** — each ticket needs independently observable goal,
   scope, acceptance criteria, verification, and supported entry points.
4. **Map** — cover every source ID; record predecessors, coupling, and unresolved
   split problems.
5. **Gate** — return writable tickets or
   `Unresolved split report | Blocked | Unverifiable`.
6. **Handoff** — apply [executor-handoff.md](references/executor-handoff.md)
   to each ticket; a ticket must be executable from its own evidence with no
   hidden parent or sibling context.
7. **Write and verify** — atomically write ledger, reread it, verify coverage,
   dependencies, and ticket contents.

## Ticket contract

Each ticket begins `Status: pending` and is executable from artifact and cited
sources without hidden conversation context. Preserve R/AC IDs; when none exist,
cite source locations instead of inventing IDs.

Use core fields in order: `Status`, `Goal`, `Coverage`, `Scope`, `Entry
points`, `Dependencies`, and `Verification`. `Coverage` names every owned R/AC or source
location; independent ticket writes `Dependencies: none` instead of implicit
dependency state.

A selected `AUD-*` finding is source evidence only. Preserve its ID, exact
evidence, confidence, route hint, and verification baseline; do not turn a
finding into a ticket until its boundary is independently proven. A ticket is
vertical behavior unit: keep behavior, tests, and verification
together. Do not split into type/API/UI/test layers or diagnose/fix/verify stages.
Keep one bug as one slice from reproduction through root-cause fix, regression
seam, original reproduction, and cleanup.

This skill alone assigns ticket IDs and owns ticket shape, coverage, dependencies,
mutable status, commit receipts, and resume state. It does not re-own whether
ledger is needed.

| State | Meaning |
| --- | --- |
| `Unresolved split report` | Evidence cannot support independent boundaries |
| `Blocked` | Confirmed conflict, missing decision, or post-checkpoint drift |
| `Unverifiable` | Required source access or traceability evidence is unavailable |
| `Fail` | Writing or post-write validation produced a known invalid result |

Do not write from `Draft | Blocked | Unverifiable`. On active-drive non-success,
pass native state, exact evidence, and `User decision: required | none` directly
to graph; do not invoke `tk-grill-me` or edit Ready spec.

## Failed-attempt ownership

Preserve completed receipts and unrelated pending tickets. When exact ledger and
current incomplete ticket exist, `tk-drive non-success finalization` is sole
downstream writer for bounded `Last attempt`, `Evidence`, and `Recovery` fields.
It never invokes this skill again. `Dependency blocked`, `Not attempted`, and
`Unverified` are terminal presentation classifications, not durable ticket
statuses.

## Source UI writing

When source or Ready spec defines rendered text, freeze source location, source
literal, current rendered/source-path literal, target literal, R/AC, and owning
ticket before decomposition. Preserve exact spelling, case, spacing, punctuation,
symbols, numbers, units, and meaningful line breaks unless wording change is
explicitly authorized.

Missing source/current evidence is `Unverifiable`; source↔current mismatch is
conflict and prevents handoff. Mark only approved wording as `authorized change`.
Do not translate, paraphrase, normalize, or silently fix typos.

## Output

Write to `--output` or atomically replace `.tigerkit/tickets.md`. Create parents
lazily; do not archive or modify `.gitignore`; never publish remotely.

User-facing output uses ticket table for multiple or one result sentence when
singular; artifact owns ticket bodies, status, coverage, dependencies, evidence,
and unresolved split detail. For multiple tickets, use
`Ticket | User-visible slice`. Use sentence for one user-relevant row. Show two
to seven tickets; for more, show top five to seven, include compact
coverage/blocker summary, and cite ledger. Active prep receives only internal
path, ticket IDs, coverage, and state handoff.

### 🔴 HARD GATE · terminal user summary

Terminal response excludes progress/internal evidence. Begin with canonical
result heading or sentence; no preamble, receipt heading, `Outcome:` label,
duplicate status, or active-drive child summary. Detailed provenance belongs only
in owned tickets artifact.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language, else current message's language. Preserve
canonical headings, status tokens, IDs, commands, paths, code, and quoted source
literals exactly. Rewrite free-form language drift before return.

## User decision questions

For material user-owned decision only: ask one self-contained `Question`, then
show `Recommendation`, two or three exclusive options, and exactly one
`(Recommended)` or `(추천)` label. Render directly in chat, never via structured
question/input tool. Preserve `Pending | Blocked` until answer.

## Pitfalls

- Do not force non-independent work into separate tickets.
- Do not invent exact paths, code, IDs, or unsupported performance numbers.
- Do not alter source UI writing or hide essential context.
- Do not implement, publish, or repair non-success state inline.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 to-tickets · 응답 필요` only for a user decision/approval, `⏳ to-tickets · 대기` only when external waiting is next, and `🚗 to-tickets · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > to-tickets`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.

## Next-action handoff

Whenever this skill hands control back to the user for a question, `Pending`,
`Blocked`, `Unverifiable`, bounded wait, or an actionable terminal result, end
the visible handoff with exactly one `Next:` line naming the recommended action
or next skill and its condition. Do not leave only a child receipt or generic
“continue”; omit `Next:` only for a terminal success with no follow-up action.
