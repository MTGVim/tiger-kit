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

## Branch name

Use the current git branch name when available. If unavailable, use a short user-provided work id.

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
