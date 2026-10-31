---
name: tk-questioning
description: "[user/auto] 질문·승인 라운드와 시각적 질문 기준을 다른 스킬에서 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Questioning

Use this reference-only skill when the caller needs one of the criteria below. Read only the
requested reference under its stated condition; do not preload the whole collection. Return
the relevant criteria and unresolved evidence to the calling workflow. This invocation does
not start that workflow or grant installation, file mutation, secret access, Git or publication
authority. The caller retains its approval gates, authority, evidence and completion duties.

If this skill or a requested resource is missing, stop the affected action and guide the user
to `tk-setup-skills`. Do not substitute remembered guidance or silently install dependencies.
Resolve linked sibling packages in the current host's installed skill collection, never from
a hardcoded home directory. Dependencies are declared in `dependencies.json`.

In moved references, `<package>`, "package-local" and "this package" mean the invoking
workflow's installed package unless an explicit resource link identifies another owner.
Following a resource link reads that resource only; it does not invoke the owner's workflow.

## Conditional references

- [questions](references/questions.md): a user-owned decision, missing approval or unmet prerequisite needs a question.
- [visual questions](references/visual-questions.md): an unresolved layout, navigation or visual choice needs a question aid.
