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
