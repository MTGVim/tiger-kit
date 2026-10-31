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

- [provider knowledge](references/provider-knowledge.md): the caller requires selected-provider integration knowledge before discovery/interaction, or a diagnosed and reverified provider limitation may need a bounded troubleshooting note.
- [provider selection](references/provider-selection.md): selecting a verification provider or interpreting its supported preferences.
- [publication evidence](references/publication-evidence.md): preparing verification evidence for an authorized publication owner.
- [verification](references/verification.md): establishing verification scope, evidence and result status.
