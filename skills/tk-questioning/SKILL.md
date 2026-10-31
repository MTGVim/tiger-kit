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

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
Resource links name the installed owner; visual-question theme assets belong to `tk-writing`.

## Conditional references

- [questions](references/questions.md): a user-owned decision, missing approval or unmet prerequisite needs a question.
- [visual questions](references/visual-questions.md): an unresolved layout, navigation or visual choice needs a question aid.
