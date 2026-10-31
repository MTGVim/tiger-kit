---
name: tk-pr-guidance
description: "[user/auto] PR 시각 자료·다중 PR 전달·rebase 준비 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared PR Guidance

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
`<package>`, "package-local" and "this package" mean the caller's installed package unless a link names another owner.

## Conditional references

- [github visuals](references/github-visuals.md): preparing visual evidence for a PR.
- [multi pr delivery](references/multi-pr-delivery.md): the approved delivery is intentionally split across multiple PRs.
- [rebase readiness](references/rebase-readiness.md): preparing an exact PR rebase or handing it to the rebase owner.
