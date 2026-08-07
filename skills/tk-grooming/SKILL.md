---
name: tk-grooming
description: "[user/auto] Audit duplication, scope, placement, and triggers in existing repository or user skills. Default to report-only and never mutate before a literal --apply or current-turn approval."
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Grooming

Apply on explicit invocation or clear audit request for existing rules or
skills. Do not auto-apply to ordinary cleanup or implementation. Implicit mode:
report-only.

## Workflow

1. `scope`: resolve requested scope, literal `--apply`, target paths, and
   allowed mutation. Retain explicit exclusions from active conversation or a
   durable governing source without reconfirmation.
2. `discovery`: read only existing native paths; inventory candidates in
   requested areas.
3. `evidence`: record area-specific observations, paths, verification state,
   and ownership evidence for every candidate.
4. `classification/proposal`: apply the
   [placement rubric](references/repository-placement.md) to skill candidates;
   classify `keep | keep (vendor) | tighten | merge | split | move | deprecate
   | delete | fix`.
5. `🔴 CHECKPOINT · 🛑 STOP`: summarize scope, evidence, proposal, and allowed
   apply in a receipt. Literal initial `--apply` pre-approves only exact passing
   receipt scope; otherwise stop for explicit current-turn approval.
6. `apply/report`: report-only emits proposals/receipt. With authority, reread
   source; mutate only approved receipt scope.
7. `revalidate`: recheck links, duplication, and frontmatter; report results,
   unverified scope, and unresolved items.

Inspect only repository or user skill areas named or implied by request. Use
actual host-native skill paths from [discovery](references/discovery.md). Do not
create missing files or inspect, migrate, or create repository/user rule state
or legacy/global TigerKit state.

Judge repository/user skills by independently normative instruction/workflow,
not whole file. Use `move` only with exact native skill target; use `split` when
one artifact mixes independent outcomes. Use `tighten` only to remove
duplication/ambiguity without changing owner, kind, scope, or meaning. Otherwise
use `keep`. Missing/conflicting path or ownership evidence makes only that area
`Partial/Blocked | Unverifiable`.

Determine ownership from resolved paths and link targets, package-manager
installation locations, updater/version artifacts, and available author
history. Names and conventions are not evidence. Confirmed vendor-managed
candidate is always `keep (vendor)`: report quality finding, never propose or
edit. If ownership is uncertain, stop before edit proposal; ask whether
user-managed or externally installed.

Classification grants no mutation authority. Even with approval, directly own
only meaning-preserving `tighten`, mechanical `move` with exact target,
unreferenced `delete`, and frontmatter/link `fix`. Semantic `merge`,
`deprecate`, workflow `split`, and semantic skill rewrite remain exact proposals
with `pending`; they may feed `tk-learn`, but this skill never invokes it.
Vendor-managed candidates remain report-only in every apply mode.

Apply only after literal initial `--apply` or explicit current-turn approval
names exact scope. Past approval or generic continuation is insufficient.
Before mutation, reread source, search references before deletion, preserve
managed/generated ownership markings, and never mix broad repo/user edits. Do
not invent knowledge or replace skill learning.

An exclusion declared in active conversation remains excluded for later
grooming runs in that conversation. One recorded in a governing repository/user
rule or another requested durable source remains excluded across sessions. Do
not create hidden global state or use `.tigerkit/` to persist exclusions.

Literal `--apply` does not skip checkpoint. It pre-approves matching
evidence/target receipt in same run. Scope, evidence, or target drift stops
`Partial/Blocked` for a new decision.

## Failure paths

- Missing/unreadable path: mark only that area `Unverifiable`, preserve other areas read-only, and report required access.
- Unknown ownership: make no edit proposal or mutation; return `Partial/Blocked` with one ownership question.
- Vendor ownership discovered after classification: replace any edit action with `keep (vendor)`, preserve artifact, and report evidence.
- Conflicting scope/apply authority: make no change; return `Partial/Blocked` with one required decision.
- Referenced delete/move target: do not mutate; change proposal to `keep | tighten` and cite references.
- Target drift after checkpoint: do not mutate; return `Partial/Blocked` with fresh evidence and require new proposal.
- Failed post-apply validation: never claim `Complete`. Restore/revalidate only when this run's delta is exactly reversible; return `Fail` with evidence. If preservation or restoration is uncertain, stop mutation as `Unverifiable`; report check, paths, and observed state.

## Contract

Evidence records actual path/content for each area. Missing required evidence
makes that area `Unverifiable`. Any blocked area prevents overall completed
claim; use `Complete | Fail | Partial/Blocked | Unverifiable`.

## Output contract

Assign `GR-01`, `GR-02`, ... once in first-identification order to each
independent normative instruction/workflow. Lead with one `## Disposition`
table:

| ID | Item | Action | Target | Basis |
| --- | --- | --- | --- | --- |
| GR-01 | `<short name>` | `<classification>` | `<target>` | `<evidence refs>` |

Reuse ID for applied changes and verification. Add `## Exceptions` only for
evidence gaps, ownership conflicts, unresolved scope, or failed verification.
Add `## Applied` and `## Verification` only after mutation. Show two to seven
findings as rows. For eight or more, show top five to seven and group remainder
behind audited target paths; do not create artifact/lifecycle behavior solely
for output. Budgets, not quotas.

Record overall `report-only | applied` disposition in `## Disposition` without
repeating table or appending metadata. With no item, emit one
`— | None | keep | — | no finding` row. Vendor rows use `keep (vendor)`.

### 🔴 HARD GATE · terminal user summary

Keep progress commentary, internal handoff envelopes, and terminal response
distinct. Start every terminal user-facing response directly with canonical
result heading or, when schema owns none, canonical result sentence. No
standalone separator, ceremonial preamble, or progress recap. Do not emit a
terminal user-summary opening between successful phase receipt and next
active-drive phase invocation.

Do not render receipt heading, `Outcome:` label, or terminal provenance/status
block. If host or skill requires terminal status, emit one exact
`Status: <token>` line in owning result section, not bottom metadata. Expose
path, ID, commit, or recovery detail only when it changes user action or schema
requires it. Keep phase receipts internal: when active parent requires phase,
status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return
only to parent workflow; never echo in terminal summary.

Persist provenance only in skill-owned artifact or ledger. Do not create one
solely for receipt; read-only remains read-only. Never require a shared runtime
reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Before user-facing progress, question, or summary, choose latest explicit user
language; else current user message language. Write all free-form user-facing
sentences and prose result values in it. Do not switch to English due to
sources, skill bodies, tools, or code. Preserve headings, status tokens, IDs,
commands, paths, code, and exact quoted/source literals byte-stable; explain in
chosen language. Before return, scan and fix language drift.

## CHECKPOINT / STOP

Do not start `--apply` mutation before audit receipt identifies evidence and
allowed scope. Ambiguous scope or missing reference evidence for delete/move
stops `Partial/Blocked | Unverifiable`.

## User decision questions

When user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Render question, recommendation, and options directly in chat; do not call
structured question or input tools. Preserve `Pending | Blocked` until user
answers. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not mutate without apply authority or skip reference checks for delete/move.
- Do not silently mix unrequested repository/user files.
- Do not infer ownership from a name, propose edits for unknown ownership, or mutate vendor-managed artifacts even with `--apply`.
- Do not inspect or migrate legacy/global TigerKit state.
- Do not apply semantic convert/split/rewrite or invoke `tk-learn`.
- Do not omit, reuse, or renumber item IDs, or append a duplicate summary after the `## Disposition` result.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 grooming · 응답 필요` only for a user decision/approval, `⏳ grooming · 대기` only when external waiting is next, and `🚗 grooming · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > grooming`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.

## Next-action handoff

Whenever this skill hands control back to the user for a question, `Pending`,
`Blocked`, `Unverifiable`, bounded wait, or an actionable terminal result, end
the visible handoff with exactly one `Next:` line naming the recommended action
or next skill and its condition. Before rendering any user-facing `Question` or
publication/approval plan, emit exactly one nonterminal hand-raise checkpoint
in this skill's `🙋 ... · 응답 필요` form; a parent may own the display in
orchestration. Do not use only a `🤹` or `🚗` boundary marker for a user
decision. Mark the single recommended option with `👍 Recommendation:`.
Do not leave only a child receipt or generic “continue”; omit `Next:` only for
a terminal success with no follow-up action.
