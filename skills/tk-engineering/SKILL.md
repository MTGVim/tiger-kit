---
name: tk-engineering
description: "[user/auto] 테스트·진단·리뷰·SDD의 공통 기준을 다른 스킬에서 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Engineering Guidance

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
`<package>`, "package-local" and "this package" mean the caller's installed package unless a link names another owner.

## Conditional references

- [diagnosis](references/diagnosis.md): a hard, flaky or performance bug needs diagnosis, or initial reproduction failed.
- [finding quality](references/finding-quality.md): filtering and substantiating exact-scope review findings.
- [project rules](references/project-rules.md): the repository or task names a project rule bundle.
- [react](references/react.md): the exact code review includes React code.
- [review protocol](references/review-protocol.md): conducting a direct, SDD Unit or whole-change independent review.
- [sdd interaction](references/sdd-interaction.md): an approved SDD execution reaches a user interaction point.
- [sdd recovery](references/sdd-recovery.md): resuming an approved interrupted SDD execution.
- [sdd transport](references/sdd-transport.md): transporting an approved SDD unit or review brief to a worker.
- [sdd](references/sdd.md): SDD has already been selected by the preparation owner.
- [security boundaries](references/security-boundaries.md): an engineering or audit investigation reaches a safety or authority boundary.
- [security](references/security.md): the exact code review includes a security-sensitive surface.
- [selection handoff](references/selection-handoff.md): a selected prototype or comparison must inform implementation.
- [test doubles](references/test-doubles.md): the changed test uses a mock, fake, stub or spy.
- [testing](references/testing.md): a source change has observable behavior requiring testing.
- [typescript](references/typescript.md): the exact code review includes TypeScript code.
- [semantic review planning](references/review-planning.md): before final local implementation approval, preserving the review obligations in the Seed or current direct task.
