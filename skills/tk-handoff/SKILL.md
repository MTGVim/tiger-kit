---
name: tk-handoff
description: "[user] Write or resume a verified work handoff. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "[goal or audience] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Handoff

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Default write target: `.tigerkit/handoff.md`. Record Goal, Current state, Decisions, Changed files, Commands run, Verification, Remaining work, Open questions, Risks, Next action, and Do not repeat. Omit empty sections, reference existing spec/ticket/diff paths instead of copying them, and never claim unverified success. Create scratch parents lazily, use temporary-file-plus-rename when possible, do not create archives/current pointers or edit `.gitignore`, and warn if scratch is not ignored.

On resume/continue intent, read the handoff, inspect current Git and file state, show drift, restore the current goal/next action, and continue only within the user's request. For long work, maintain `.tigerkit/work-map.md` with overall goal, current/completed slices, blockers/edges, recent decisions, next concrete action, and resume hints.

Do not copy transcripts, create archives/current pointers, commit, or publish automatically.
