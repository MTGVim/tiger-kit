---
description: Analyze gaps between source material and current implementation.
---

Use the `gap` skill from this plugin.

Goal: collect source material, normalize it into `.gap/{branch_name}/normalized/source-packet.md`, inspect current implementation where possible, and produce `.gap/{branch_name}/analysis/gap-report.md`.

If the user did not provide source material or a source extraction instruction, stop before inspecting the repository or writing artifacts. Explain what source-of-truth is needed and ask the user to provide sources, ask you to fetch/extract sources, or start an interview.

Do not implement code during this command unless explicitly requested.
