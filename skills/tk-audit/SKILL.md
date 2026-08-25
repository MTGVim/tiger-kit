---
name: tk-audit
description: "[user] 저장소를 읽기 전용으로 감사하고, 다른 실행자나 `tk-prep`이 재사용할 수 있는 우선순위가 있는 근거 기반 `AUD-*` `finding`을 작성합니다."
license: MIT
argument-hint: "[quick|standard|deep] [security|perf|tests|architecture|branch|next]"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: shadcn/improve
    upstream-skill: improve
    relationship: adapted
---

# Audit

Use only when `$tk-audit` or `/tk-audit` is explicitly selected.
This is read-only codebase advising and does not modify source, tests, configuration, or history.
The only owned artifact is repository-local `.tigerkit/audit.md`.

## Invocation

- `bare`: Audit all categories at standard depth.
- `quick | standard | deep`: Change the depth and bounded coverage.
- `security | perf | tests | architecture`: Focus on one category.
- `branch`: Inspect merge-base changes and direct consumers, and mark `introduced | pre-existing`.
- `next`: Separate evidence-backed direction candidates from defect findings.

Modifiers may be combined. Do not implement, write Seeds, publish issues, or create worktrees.
When user-owned clarification is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, ask once in plain chat and preserve the read-only boundary.

## Workflow

1. Read repository instructions, root configuration, verification commands, structure, and relevant Git history.
2. Check the selected categories using [audit-playbook.md](references/audit-playbook.md).
3. Reopen cited evidence to remove duplicates, intended behavior, and incorrect attribution.
4. Sort `finding`s by impact ÷ `effort`, then `confidence`, `fix risk`, and `dependency`.

For a potential architecture finding, read ADR rationale only when it directly owns the observed trade-off. Do not
report a deliberate ADR trade-off as a generic smell. Surface `revisit ADR` only when current evidence shows real
friction or changed constraints, and never scan an unrelated ADR or context tree.

## 🔴 CHECKPOINT · 🛑 STOP · Ledger preflight

Before writing `.tigerkit/audit.md`, freshly recheck the current `HEAD`, requested scope, existing `AUD-*` IDs,
cited evidence, and the audited/unaudited boundary. If any of these changed, conflict, or cannot be read, stop with
`Status: Blocked` or `Status: Unverifiable` and do not write the ledger. Only after the preflight passes, atomically
update the ledger.

5. Atomically update `.tigerkit/audit.md` while preserving stable `AUD-*` IDs and statuses.

## Failure Paths

- If repository instructions, the selected reference, or required evidence is unavailable, stop that scope and record it as unaudited; do not infer coverage.
- If cited evidence cannot be reproduced at the audited `HEAD`, mark the finding unverifiable or stale and do not claim verification.
- If the scope or modifier is invalid, ask one clarifying question before reading beyond the minimum needed to identify the problem.
- If the atomic `.tigerkit/audit.md` update fails, preserve the existing ledger, report the write failure, and do not fall back to an untracked or global copy.

## Finding Contract

Each open finding must contain at least:

- A stable `AUD-*` ID and title
- Category and exact `path/line` or `symbol` evidence
- Impact, `effort`, `fix risk`, and `confidence`
- Relevant entry points and repository conventions
- Verification `baseline`
- A short `fix sketch`
- `dependency/order hint`
- A recommended next route: `prep | investigate | no-action`

A `finding` is only a candidate, not a `Seed`, ticket, implementation plan, or approval.
Never copy a `secret` value; record only its location and credential type.

## Next-Executor Handoff

Apply [executor-handoff.md](references/executor-handoff.md) to every finding.
Include the `audited HEAD`, exact paths/`symbol`s, current evidence, repository rules, `in/out` boundaries,
assumptions, verification commands, and `drift handling` so the next executor can proceed without the audit conversation.

The quality criteria in [plan-template.md](references/plan-template.md) supplement this contract, but
`tk-audit` does not create a separate plan lifecycle.

To prepare actual work, the user may provide the current `finding` as a source, such as `$tk-prep AUD-003`.
`tk-prep` rechecks the `finding` against current repository evidence and prepares an executable `Seed`.
An `Audit finding` alone grants no product-change or remote authority.

## Safety

During a partial audit, do not delete existing findings; mark unaudited scope.
Do not claim verification when the evidence cannot be reproduced at the current HEAD.
`.tigerkit/` is local scratch; do not create a global archive or current pointer.

At completion, concisely summarize the key `finding`s and any unaudited scope.
