---
description: Execute the next TIGAP task narrowly and update progress files.
---

Use the `go` skill from this plugin.

Goal: read `.gap/{branch_name}/tasks.md`, select the next small task, inspect relevant code, implement narrowly, validate, and update `.gap/{branch_name}/execution-log.md` plus task status.

Before changing code or workflow artifacts, check branch/work-id context. If the current branch is `main`, `master`, `develop`, or the repository default branch, recommend moving the work to a source-of-truth-specific branch or explicit work id. Do not create or switch branches without user approval.

Execute one task at a time unless explicitly requested otherwise.
