---
description: Show the current TIGAP workflow stage and recommend the next action.
---

Inspect `.gap/{branch_name}/` for the current git branch and report the current TIGAP workflow stage.

This command is read-only. Do not create, modify, or delete files.

Use the current git branch name when available. If branch detection is unavailable, ask for the work id or infer a safe short slug from the user's context.

Determine the stage from artifacts in this order:

1. If `.gap/{branch_name}/normalized/source-packet.md` is missing, report `source-needed` and recommend `/tigap:gap <source material or extraction instruction>`.
2. If `source-packet.md` exists but `.gap/{branch_name}/analysis/gap-report.md` is missing, report `analysis-needed` and recommend `/tigap:gap` with the known source material.
3. If `gap-report.md` exists but `.gap/{branch_name}/plan/implementation-plan.md` or `.gap/{branch_name}/tasks.md` is missing, report `plan-needed` and recommend `/tigap:gaplan`.
4. If `tasks.md` exists, inspect it and report:
   - `blocked` when there are unresolved Blocked tasks that prevent ready work
   - `in-progress` when a task is under In Progress
   - `execution-ready` when Ready has unchecked tasks
   - `complete` when all planned tasks are done and none are blocked

When reporting, include:

- current stage
- evidence from existing artifact paths
- the next recommended command or action
- the first Ready or In Progress task when `tasks.md` exists
