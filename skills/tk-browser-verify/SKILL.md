---
name: tk-browser-verify
description: "Verify browser UI, behavior, environment differences, and design fidelity with runtime evidence."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser Verify

Use directly or during relevant implementation. Work zero-config: understand the request, discover a runnable environment, choose any available native browser, Playwright-compatible, MCP, or CDP driver, navigate, interact, and observe. A profile is optional.

Select the relevant lenses: [visual](references/visual.md), [behavior](references/behavior.md), [environment](references/environment.md), or [design](references/design.md). Follow [safety](references/safety.md). Prefer trusted pointer/keyboard interactions over synthetic events.

For a mutation, require UI transition, network request/response, and final UI state. A toast or isolated DOM change is insufficient. If a dangerous irreversible action lacks a safe environment or explicit permission, return `Unverifiable`.

Store useful evidence only under `.tigerkit/browser-verify/runs/<run-id>/`; do not create empty files. Use `YYYYMMDD-HHmmss-<short-slug>` when practical. Lazily record confirmed non-sensitive facts in `.tigerkit/browser-verify/env.md` or `.tigerkit/browser-verify/screens/<screen>.md`. Create scratch parents lazily, use atomic replacement when practical, never edit `.gitignore`, and warn if scratch is not ignored. Never create `login.local.md` automatically; if the user explicitly requests it, avoid printing its content and use mode `0600` when possible. Do not inspect or migrate legacy global TigerKit state.

Do not edit production code or promote evidence into rules/skills. Output `## Verdict` (`Pass | Fail | Unverifiable`), `## Verified`, `## Findings`, `## Evidence`, and `## Unverified`, omitting empty sections.
