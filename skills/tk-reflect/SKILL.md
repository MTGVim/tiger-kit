---
name: tk-reflect
description: "[user] Extract reusable rule or skill candidates from evidence. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<conversation, correction, diff, result, or source>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Reflect

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Read the current conversation, corrections, diff, implementation/test/review results, relevant `.tigerkit/` artifacts, and user-designated sources. Classify on exactly four axes: `repo rule`, `repo skill`, `user rule`, `user skill`; choose `propose | update | merge | no-op | discard`.

A rule is short standing guidance. A skill has a trigger, repeatable steps, inputs/outputs, and independent value. Repo targets are codebase/domain/tool/team specific; user targets recur across repositories. Separate observed evidence from interpretation.

Default report-only: do not modify files, create ledgers/IDs, invoke another user skill, scan legacy global state, elevate raw credentials/logs/screenshots, or generalize one-off workarounds. Prefer merge/no-op for duplicates.

For each non-empty candidate report Target, Action, Learning, Evidence, Why this target, and Draft.
