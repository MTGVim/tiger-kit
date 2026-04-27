---
description: Turn a gap report into an implementation plan and task list.
---

Use the `gaplan` skill from this plugin.

Goal: read `.gap/{branch_name}/analysis/gap-report.md`, produce `.gap/{branch_name}/plan/implementation-plan.md`, and create `.gap/{branch_name}/tasks.md`.

Before writing mutable planning artifacts, check branch/work-id context. If the current branch is `main`, `master`, `develop`, or the repository default branch, recommend continuing under a source-of-truth-specific work branch or explicit work id. Do not create or switch branches without user approval.

Stay in planning mode. Do not implement code unless explicitly requested.
