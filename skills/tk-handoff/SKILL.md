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

Apply on explicit invocation or clear handoff write/resume request. Do not
auto-apply to summaries, status questions, or generic continuation; do not
invoke another skill.

## Workflow

### New handoff

1. `evidence`: map current branch, files, and command results to path-cited
   facts and `verified | unverified`.
2. `schema`: map facts and user approvals to required-section draft and
   `confirmed | pending` decisions.
3. `write`: map approved draft and output path to written file.
4. `receipt`: map write/revalidation results to
   `reported | applied | pending` and evidence locations.

### Resume

1. `state check`: compare existing handoff with current Git/files; list matches
   plus `drift | conflict`.
2. `materiality`: classify via resume table with evidence.
3. `continue or checkpoint`: follow table continuation/stop result.
4. `continue or stop`: use no-drift approval or explicit material-drift
   confirmation to produce next work or stop reason.

### Resume decision table

| Classification | Evidence | Action |
|---|---|---|
| `none` | branch, goal, decisions, ownership, and verification match current evidence | treat `--resume` as approval and continue without another question |
| `non-material` | timestamp/order differences cannot change outcome | record and continue without another question |
| `material drift` | branch/goal scope, confirmed decisions, changed-file ownership, or verification result differs | ask one required decision; stop `pending | Blocked` |
| `conflict` | handoff and current source require incompatible intent/result | present both evidence sets and choices; stop `Blocked` |
| `unverified` | required Git/file state cannot be checked | do not infer; stop `Unverifiable` |

## Contract

Default target `.tigerkit/handoff.md` contains:

- `Goal`: goal and scope
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Repository state`: current branch, HEAD, and worktree
- `Handoff path`: exact path written/read
- `Decisions`: only answer/approval-linked decisions are `confirmed`; others are `pending`
- `Changed files`: observed paths only
- `Commands`: exact commands actually executed
- `Verification`: per-check result, `verified | unverified`, evidence location
- `Remaining work`: all unfinished work
- `Open questions`: decisions required before progress
- `Risks`: remaining failure/regression risk, separate from questions
- `Next step`: one immediate action selected from Remaining work
- `Resume hints`: only environment/order/commands needed to resume, without repeating Next step

`Next step` must be executable without reconstructing conversation: exact
target, satisfied prerequisites or section reference, and observable completion
evidence. When an open question blocks work, Next step obtains that decision,
not downstream execution.

Use `verified` only for evidence checked this run. Prior handoff claims, plans,
model inference, and unexecuted commands stay `unverified`. Strict ownership:
Repository state owns branch/HEAD; Handoff path owns path; Commands owns only
executed command strings; Verification owns outcomes; Next step/Resume hints
own future commands. `reported | applied | pending` is artifact disposition,
not work Status. Use `applied` only after atomic write and reread agree with
current repository state. Use `reported` only for verified no-drift
resume/report needing no artifact write. Otherwise use `pending` or applicable
recovery-table stop state.

Handoff artifact owns disposition and section references. Terminal summary does
not duplicate paths, Git state, commands, results, or future work; no metadata.
Omit empty sections; reference existing spec/ticket/diff instead of copying.
Summarize current state, completed work, next action, and blockers in two to
five short bullets when compound; one result may use one to three short lines.
For eight or more underlying items, show top five to seven and cite artifact
path owning full inventory. Budgets, not quotas.

`.tigerkit/handoff.md` is the only resume snapshot. Reference durable R/AC and
multi-unit IDs from `.tigerkit/drive.md` when Drive owns the source run.
Never create `.tigerkit/work-map.md`, archive, current pointer, or global state.
Treat existing work-map as legacy scratch; do not modify, migrate, or delete.

## CHECKPOINT / STOP

`--resume` authorizes resume; continuation follows only resume table.

Create scratch parents lazily, write same-directory temporary file, rename
atomically, and reread. On failure use recovery table. Never create
archives/current pointers or edit `.gitignore`; warn when scratch is not
ignored. Requested handoff file does not make unresolved decisions `confirmed`.

On resume, read handoff and current Git/files, then classify. Preserve
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

## DO NOT / ANTI-PATTERNS

- Do not mark an unexecuted command, check, or decision `verified | confirmed`.
- Do not resolve material drift/conflict or continue without confirmation.
- Do not create archives, current pointers, automatic commits, or publication.
