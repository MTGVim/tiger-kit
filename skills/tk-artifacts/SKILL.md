---
name: tk-artifacts
description: "[user/auto] 파일 산출물 경로·비밀 입력·인증 보존 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Artifact Safety

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
`<package>`, "package-local" and "this package" mean the caller's installed package unless a link names another owner.

## Conditional references

- [artifact paths](references/artifact-paths.md): before an authorized artifact or temporary input is written.
- [authentication](references/authentication.md): approved application authentication input or renewal is needed.
