---
name: tk-repository-guidance
description: "[user/auto] 저장소 맥락·도메인 문서·외부 계약의 조사 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Repository Guidance

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
`<package>`, "package-local" and "this package" mean the caller's installed package unless a link names another owner.

## Conditional references

- [domain context](references/domain-context.md): repository-owned vocabulary or domain meaning informs the task.
- [external contracts](references/external-contracts.md): a version-sensitive external contract cannot be established locally.
- [repository context](references/repository-context.md): tracker identity, repository configuration or verification-data policy matters.
