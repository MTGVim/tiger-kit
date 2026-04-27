---
description: Analyze gaps between source material and current implementation.
---

Use the `gap` skill from this plugin.

Goal: collect source material, normalize it into `.gap/{branch_name}/normalized/source-packet.md`, inspect current implementation where possible, and produce `.gap/{branch_name}/analysis/gap-report.md`.

If the user did not provide source material or a source extraction instruction, stop before inspecting the repository or writing artifacts. Explain what source-of-truth is needed and ask the user to provide sources, ask you to fetch/extract sources, or start an interview.

Before writing mutable artifacts, check branch/work-id context. If the current branch is `main`, `master`, `develop`, or the repository default branch, recommend a source-of-truth-specific work branch or explicit work id. Do not create or switch branches without user approval.

Do not implement code during this command unless explicitly requested.
