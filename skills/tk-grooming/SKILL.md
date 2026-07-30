---
name: tk-grooming
description: "[user/auto] Audit duplication, scope, placement, and triggers in existing repository/user rules or skills. Default to report-only and never mutate before a literal --apply or current-turn approval."
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Grooming

Apply on explicit invocation or a clear audit request for existing rules or
skills. Do not auto-apply to ordinary cleanup or implementation. Implicit mode
is report-only.

## Workflow

1. `scope`: resolve requested scope, literal `--apply`, target paths, and
   allowed mutation. Carry forward explicit exclusions from the active
   conversation or a durable governing source without reconfirmation.
2. `discovery`: read only existing native paths and inventory candidates in the
   requested areas.
3. `evidence`: record area-specific observations, paths, verification state,
   and ownership evidence for every candidate.
4. `classification/proposal`: apply the
   [placement rubric](references/repository-placement.md) to repository
   candidates and classify each as
   `keep | keep (vendor) | tighten | merge | split | move | convert | deprecate
   | delete | fix`.
5. `🔴 CHECKPOINT · 🛑 STOP`: summarize scope, evidence, proposal, and allowed
   apply in a receipt. A literal initial `--apply` pre-approves only the exact
   passing receipt scope; otherwise stop for explicit current-turn approval.
6. `apply/report`: report-only emits proposals/receipt. With authority, reread
   source and mutate only the approved receipt scope.
7. `revalidate`: recheck links, duplication, and frontmatter; report results,
   unverified scope, and unresolved items.

Inspect only the areas named or implied by the request. Inspect all four areas
—repository rules, repository skills, user rules, and user skills—only for a
catalog-wide audit. Use actual host-native paths from
[discovery](references/discovery.md). Do not create missing files or inspect,
migrate, or create legacy/global TigerKit state.

Judge repository rules/skills by independently normative instruction/workflow,
not whole file. Use `convert` when kind changes, `move` when root versus nested
rule placement changes, and `split` when one artifact mixes independent
outcomes. Use `tighten` only to remove duplication/ambiguity without changing
owner, kind, scope, or meaning. Otherwise use `keep`. Missing or conflicting
path/count/threshold evidence makes only that area
`Partial/Blocked | Unverifiable`.

Determine ownership from resolved paths and link targets, package-manager
installation locations, updater/version artifacts, and available author
history. Names and naming conventions are never ownership evidence. A confirmed
vendor-managed candidate is always `keep (vendor)`: report the quality finding,
but do not propose or perform an edit. If ownership is uncertain, stop before
an edit proposal and ask whether the artifact is user-managed or externally
installed.

Classification is not mutation authority. Even after apply approval, this
skill directly owns only meaning-preserving `tighten`, mechanical `move` with
an exact target, unreferenced `delete`, and frontmatter/link `fix`. Semantic
`merge`, `deprecate`, rule-to-skill `convert`, workflow `split`, and semantic
skill rewrite remain exact proposals with `pending`; they may feed `tk-learn`,
but this skill never invokes it. Vendor-managed candidates remain report-only
under every apply mode.

Apply only after literal initial `--apply` or explicit current-turn approval
names an exact scope. Past approval or generic continuation is insufficient.
Before mutation reread source, search references before deletion, preserve
managed/generated ownership markings, and never mix broad repo/user edits.
This skill does not invent knowledge or replace reflection/learning.

An exclusion explicitly declared in the active conversation remains excluded
for later grooming runs in that conversation. An exclusion recorded in a
governing repository/user rule or another requested durable source remains
excluded across sessions. Do not create hidden global state or use
`.tigerkit/` to persist exclusions.

Literal `--apply` does not skip the checkpoint. It pre-approves a matching
evidence/target receipt in the same run. Scope, evidence, or target drift stops
`Partial/Blocked` for a new decision.

## Failure paths

- Missing/unreadable path: mark only that area `Unverifiable`, preserve other
  areas read-only, and report required access.
- Unknown ownership: make no edit proposal or mutation; return
  `Partial/Blocked` with one ownership question.
- Vendor ownership discovered after classification: replace any edit action
  with `keep (vendor)`, preserve the artifact, and report the evidence.
- Conflicting scope/apply authority: make no change and return
  `Partial/Blocked` with one required decision.
- Referenced delete/move target: do not mutate; change proposal to
  `keep | tighten` and cite references.
- Target drift after checkpoint: do not mutate; return `Partial/Blocked` with
  fresh evidence and require a new proposal.
- Failed post-apply validation: never claim `Complete`. Restore/revalidate only
  when this run's delta is exactly reversible, then return `Fail` with the
  revalidation evidence. If preservation or restoration is uncertain, stop
  mutation as `Unverifiable` and report the check, paths, and observed state.

## Contract

Evidence records actual path/content for each area; missing required evidence
makes that area `Unverifiable`. Any blocked area prevents an overall completed
claim; use `Complete | Fail | Partial/Blocked | Unverifiable`.

## Output contract

Assign `GR-01`, `GR-02`, ... once in first-identification order to each
independent normative instruction/workflow. Lead with one `## Disposition`
table:

| ID | Item | Action | Target | Basis |
| --- | --- | --- | --- | --- |
| GR-01 | `<short name>` | `<classification>` | `<target>` | `<evidence refs>` |

Use the same ID for applied changes and verification. Add `## Exceptions` only
for evidence gaps, ownership conflicts, unresolved scope, or failed
verification. Add `## Applied` and `## Verification` only after mutation.
Show two to seven findings as table rows. For eight or more, show the top five
to seven and group the remainder behind their audited target paths; do not add
an artifact or lifecycle behavior solely to hold output. These are budgets,
not quotas.
Record overall `report-only | applied` disposition in `## Disposition` without
repeating the table or appending metadata. With no item, emit one
`— | None | keep | — | no finding` row. Vendor rows use `keep (vendor)`.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## CHECKPOINT / STOP

Do not start `--apply` mutation before the audit receipt identifies evidence
and allowed scope. Ambiguous scope or missing reference evidence for
delete/move stops `Partial/Blocked | Unverifiable`.

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

- Do not mutate without apply authority or skip reference checks for
  delete/move.
- Do not silently mix unrequested repository/user files.
- Do not infer ownership from a name, propose edits for unknown ownership, or
  mutate vendor-managed artifacts even with `--apply`.
- Do not inspect or migrate legacy/global TigerKit state.
- Do not apply semantic convert/split/rewrite or invoke `tk-learn`.
- Do not omit, reuse, or renumber item IDs, or omit Summary.
