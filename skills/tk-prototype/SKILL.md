---
name: tk-prototype
description: "Build a throwaway UI or logic prototype to test a hypothesis. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Prototype

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Accept a prompt, idea, screenshot, spec, ticket, code, or design reference. Save under `.tigerkit/prototypes/<slug>/` unless an executable temporary route or harness is more useful. Create scratch parents lazily, use atomic replacement when practical, do not archive automatically or edit `.gitignore`, and warn when generated scratch is not ignored.

For open UI design or requested comparison, build 2–3 materially different rendered variants with a switch. Vary information architecture, flow, hierarchy, navigation, or feedback—not only color. For logic, prefer a small pure harness with real example inputs/outputs and minimal adapters.

Default no-commit. Separate fake data/integration from real connections. Avoid production abstractions and error-handling investment; never call the result production-ready or automatically promote it or invoke another user skill.

Report `## Tested`, `## Variants or harness`, `## Confirmed`, `## Still fake`, and `## Production implication`.
