---
name: tk-domain
description: "[user/auto] repository 고유 용어의 canonical vocabulary를 근거로 정하고 root CONTEXT.md를 필요할 때만 생성·정제하며, 실제 bounded context가 입증된 경우에만 승인 후 CONTEXT-MAP.md로 확장합니다."
disable-model-invocation: false
argument-hint: "<domain term, vocabulary evidence, or context scope>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Repository Domain Language

Use this skill only to create or refine repository-owned ubiquitous language. It is not a generic memory store,
rules corpus, architecture document, implementation guide, or troubleshooting archive.

## Evidence

Investigate repository source, product material, and supplied conversation evidence for one concrete project-specific
term. Confirm the canonical spelling, meaning, and useful alternatives. If the meaning claims code behavior, ground it
in current source. Ask the user only when canonical vocabulary is a genuine product/domain decision that evidence cannot
resolve.

Do not create an artifact before the first real term is confirmed. Respect an existing repository glossary convention
instead of duplicating it.

## Artifact

For one context, create or refine root `CONTEXT.md` with the smallest useful form:

```md
# Domain Context

## Language

**<canonical term>**
<short project-specific meaning>
_Avoid_: <misleading synonym>, <unwanted translation>
```

`_Avoid_` is optional. Preserve Korean/English spelling, acronyms, casing, and spacing exactly when they are part of
the canonical term.

Exclude file paths, classes/functions/tables, debugging tips, generic programming vocabulary, transient values,
task acceptance criteria, general engineering rules, and long product specifications. Move behavioral invariants to
their repo-native owner instead of the glossary.

## Optional Multi-Context Escalation

Default to root `CONTEXT.md`. A monorepo or multiple packages alone is not evidence for splitting. Propose
`CONTEXT-MAP.md` only when actual bounded contexts exist, such as one term having different meanings, unrelated
vocabularies repeatedly mixing, or workers rarely needing another context's language. This structural change requires
explicit current-turn approval.

The map contains only relevant context paths and relationships; it never duplicates glossary entries. After approval,
place each glossary at the natural bounded-context path and verify every mapped path.

## 🔴 CHECKPOINT · 🛑 STOP

Before any write, present the term, evidence, exact target path, proposed wording, exclusions, and whether this is a
root refinement or approved multi-context change. Require current-turn approval for the exact mutation. Evidence or
scope drift invalidates approval.

After approval, write the minimum artifact atomically, reread it, and verify that canonical terms and `_Avoid_` values
are exact and that no excluded implementation/rule content entered the glossary. Do not create central TigerKit state,
host-specific memory, a learning corpus, or automatic repository scanning.

Return the changed path, canonical terms, evidence basis, verification, and one actual status:
`Pass | Blocked | Unverifiable | Fail`.
