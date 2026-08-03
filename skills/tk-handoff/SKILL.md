---
name: tk-handoff
description: "[user/auto] Write a verified handoff artifact or explicitly resume an existing handoff. Do not apply to ordinary summaries, status questions, or generic continuation."
argument-hint: "[goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Handoff

Apply on explicit invocation or a clear handoff write/resume request. Do not
auto-apply to summaries, status questions, or generic continuation, and do not
invoke another skill.

## Workflow

### New handoff

1. `evidence`: map current branch, files, and command results to path-cited
   facts and `verified | unverified`.
2. `schema`: map facts and user approvals to required-section draft and
   `confirmed | pending` decisions.
3. `write`: map approved draft and output path to the actual written file.
4. `receipt`: map write/revalidation results to
   `reported | applied | pending` and evidence locations.

### Resume

1. `state check`: compare existing handoff with current Git/files and list
   matches plus `drift | conflict`.
2. `materiality`: classify through the resume table with evidence.
3. `continue or checkpoint`: follow the table's continuation/stop result.
4. `continue or stop`: use no-drift approval or explicit material-drift
   confirmation to produce the next work or stop reason.

### Resume decision table

| Classification | Evidence | Action |
|---|---|---|
| `none` | branch, goal, decisions, ownership, and verification match current evidence | treat `--resume` as approval and continue without another question |
| `non-material` | timestamp/order differences cannot change outcome | record and continue without another question |
| `material drift` | branch/goal scope, confirmed decisions, changed-file ownership, or verification result differs | ask one required decision; stop `pending | Blocked` |
| `conflict` | handoff and current source require incompatible intent/result | present both evidence sets and choices; stop `Blocked` |
| `unverified` | required Git/file state cannot be checked | do not infer; stop `Unverifiable` |

## Contract

The default write target is `.tigerkit/handoff.md` with:

- `Goal`: goal and scope
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Repository state`: current branch, HEAD, and worktree
- `Handoff path`: exact path written/read
- `Decisions`: only answer/approval-linked decisions are `confirmed`; others
  are `pending`
- `Changed files`: observed paths only
- `Commands`: exact commands actually executed
- `Verification`: per-check result, `verified | unverified`, evidence location
- `Remaining work`: all unfinished work
- `Open questions`: decisions required before progress
- `Risks`: remaining failure/regression risk, separate from questions
- `Next step`: one immediate action selected from Remaining work
- `Resume hints`: only environment/order/commands needed to resume, without
  repeating Next step

`Next step` must be executable without reconstructing conversation and include
an exact target, satisfied prerequisites or section reference, and observable
completion evidence. When an open question blocks work, Next step obtains that
one decision instead of naming downstream execution.

Use `verified` only for evidence checked in this run. Prior handoff claims,
plans, model inference, and unexecuted commands remain `unverified`. Section
ownership is strict: Repository state owns branch/HEAD; Handoff path owns the
path; Commands owns executed command strings only; Verification owns outcomes;
Next step/Resume hints own future commands. The
`reported | applied | pending` is artifact disposition, not work Status.
Use `applied` only after the atomic write and reread agree with current
repository state. Use `reported` only for a verified no-drift resume/report
that required no artifact write. Otherwise use `pending` or the applicable
recovery-table stop state.
The handoff artifact owns disposition and section references. The terminal
summary does not duplicate paths, Git state, commands, results, or future work
and does not append metadata. Omit empty sections and reference existing
spec/ticket/diff content instead of copying it.
Summarize current state, completed work, next action, and blockers in two to
five short bullets when compound; one result may use one to three short lines.
For eight or more underlying items, show the top five to seven and cite the
handoff artifact path that owns the full inventory. These are budgets, not
quotas.

`.tigerkit/handoff.md` is the only resume snapshot. Reference durable R/AC from
`.tigerkit/spec.md` and multi-slice ticket IDs from `.tigerkit/tickets.md`.
Never create `.tigerkit/work-map.md`, an archive, current pointer, or global
state. Treat an existing work-map as legacy scratch; do not modify, migrate, or
delete it.

## CHECKPOINT / STOP

`--resume` explicitly authorizes resume, but continuation follows only the
resume table.

Create scratch parents lazily, write a same-directory temporary file, rename
atomically, and reread it. On failure use the recovery table. Never make
archives/current pointers or edit `.gitignore`; warn when scratch is not
ignored. A requested handoff file does not turn unresolved decisions into
`confirmed`.

On resume, read the handoff and current Git/files, then classify. Preserve
`unverified` for anything without current evidence.

## Failure recovery

| Trigger | First action | If still failing |
|---|---|---|
| handoff missing/unreadable | report path/access and distinguish new write from resume | stop `Unverifiable` when evidence cannot reconstruct resume state |
| temp write/replace failure | preserve existing handoff, clean only run-owned temp, report `pending` | stop further writes `Blocked` if preservation is unknown |
| reread disagrees with schema/current state | do not mark `applied`; return mismatches to `unverified` | stop `Unverifiable` if safe reread is impossible |
| legacy work-map exists | ignore as legacy scratch | use only current handoff/spec/ticket evidence; never mutate it |

Do not copy conversation history, create archive/current pointers, or
automatically commit/publish.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Render the question, recommendation, and options directly in the chat response;
do not call structured question or input tools. Preserve `Pending | Blocked`
until the user answers. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not mark an unexecuted command, check, or decision
  `verified | confirmed`.
- Do not resolve material drift/conflict or continue without confirmation.
- Do not create archives, current pointers, automatic commits, or publication.
