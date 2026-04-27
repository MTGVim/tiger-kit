# Artifact Layout

Recommended project-local artifact tree:

```text
.gap/{branch_name}/
  sources/
    issue-tracker/
    knowledge-base/
    prd/
    brief/
    code/
  normalized/
    source-packet.md
  analysis/
    gap-report.md
  plan/
    implementation-plan.md
  tasks.md
  execution-log.md
  review-checklist.md
```

## Branch name and work id

Use the current git branch name when it represents the work being done. If the current branch is a base branch such as `main`, `master`, `develop`, or the repository default branch, prefer one of these before writing mutable workflow artifacts:

- create or switch to a source-of-truth-specific work branch after user approval
- ask the user for a short work id and use it under `.gap/{work_id}/`

Do not create or switch branches automatically. If git branch detection is unavailable, use a short user-provided work id.

## Git ignore policy

`.gap/` artifacts are usually local workflow notes. In a git repository, check whether `.gap/` is ignored or intentionally tracked before creating artifacts. If it is neither ignored nor tracked, suggest adding `.gap/` to `.gitignore` instead of silently changing the repository.

## File responsibilities

| File | Purpose |
|---|---|
| `source-packet.md` | Normalized source-of-truth summary |
| `gap-report.md` | Missing, ambiguous, conflicting, and risky areas |
| `implementation-plan.md` | Ordered implementation plan |
| `tasks.md` | Checkbox task list for execution |
| `execution-log.md` | Running notes while executing tasks |
| `review-checklist.md` | Pre-review verification list |

## Workflow stages

`/tigap:next` infers the current stage from these artifacts:

| Stage | Evidence | Recommended next action |
|---|---|---|
| `source-needed` | `normalized/source-packet.md` is missing | Run `/tigap:gap <source material or extraction instruction>` |
| `analysis-needed` | `source-packet.md` exists and `analysis/gap-report.md` is missing | Continue `/tigap:gap` |
| `plan-needed` | `gap-report.md` exists and plan/tasks are missing | Run `/tigap:gaplan` |
| `execution-ready` | `tasks.md` has unchecked Ready tasks | Run `/tigap:go` |
| `in-progress` | `tasks.md` has an In Progress task | Finish or unblock that task |
| `blocked` | `tasks.md` has unresolved blocking tasks and no ready work | Resolve the blocker |
| `complete` | All planned tasks are done | Review and finalize |
