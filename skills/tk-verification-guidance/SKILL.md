---
name: tk-verification-guidance
description: "[user/auto] 앱·브라우저 검증의 제공자 선택·근거·설정 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Verification Guidance

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
`<package>`, "package-local" and "this package" mean the caller's installed package unless a link names another owner.

## Conditional references

- [provider knowledge](references/provider-knowledge.md): the caller requires selected-provider integration knowledge before discovery/interaction, or a diagnosed and reverified provider limitation may need a bounded troubleshooting note.
- [provider selection](references/provider-selection.md): selecting a verification provider or interpreting its supported preferences.
- [publication evidence](references/publication-evidence.md): preparing verification evidence for an authorized publication owner.
- [verification](references/verification.md): establishing verification scope, evidence and result status.
