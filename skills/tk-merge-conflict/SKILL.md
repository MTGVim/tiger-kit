---
name: tk-merge-conflict
description: "[auto] Resolve active merge or rebase conflicts while preserving both sides intent and verifying the result."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: tigerkit
    relationship: native
---

# Merge Conflict discipline

Confirm an active merge/rebase state, list conflict files and hunks, then trace ours/theirs intent before editing. Preserve both intents where possible; avoid unrelated refactors, formatting churn, and large deletions without intent evidence.

Never run destructive reset, clean, or force-push operations. Resolve only active conflicts and run relevant verification afterward. Report state, conflict files, intent-preserving resolutions, verification, and remaining manual follow-up.
