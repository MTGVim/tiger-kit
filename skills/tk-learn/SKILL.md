---
name: tk-learn
description: "Create a reusable repo or user skill from supplied experience or material. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<conversation, notes, path, URL, workflow, or reflect candidate>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Learn

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Accept conversation, notes, files/directories, URLs, workflows, or a reflect candidate in the current conversation. Create a `repo skill` or `user skill`; rule creation is out of scope.

Collect evidence, extract repeatable behavior, search for duplicates, classify user-invoked/model-invoked/hybrid, propose a name, then write the smallest self-contained skill. Add references/scripts only when needed. Review positive/negative triggers and add a minimal example or eval. Follow [skill quality](references/skill-quality.md).

If target/apply intent is unclear, draft under `.tigerkit/skill-drafts/<skill-name>/`. Apply to an actual host-native skill surface only when the user explicitly specifies repo/user target and application. For drafts, create parents lazily, use atomic replacement when practical, do not archive automatically or edit `.gitignore`, and warn if scratch is not ignored. Do not create a skill when a rule suffices, evidence is one-off, an equivalent exists, default model ability is enough, or no trigger can be stated.

Report Skill name/kind/target, Created paths, Validation, and Remaining concerns.
