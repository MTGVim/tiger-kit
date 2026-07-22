# Migrating to TigerKit 20

TigerKit 20 keeps Agent Skills distribution for Claude Code, Codex, and Hermes Agent while changing the next-major source from 13 skills (9 user/4 hybrid) to 12 skills (2 user/10 hybrid). The `model-only` kind remains removed.

## Install

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

Claude Code and Hermes Agent use `/tk-*`; Codex uses `$tk-*` or its picker.

## Removed Skills

```text
tk-grill-with-docs
tk-grilling
tk-domain-modeling
tk-tdd
tk-codebase-design
tk-code-review
tk-diagnosing-bugs
```

Replacement mapping:

```text
tk-grill-with-docs
→ tk-grill-me
→ 필요하면 tk-to-spec
→ 작업 후 tk-reflect

tk-grilling
→ tk-grill-me

tk-domain-modeling
→ 결정 중 용어 구체화: tk-grill-me
→ 확정 내용: tk-to-spec
→ 자동 CONTEXT.md / domain 문서 / ADR mutation 없음

tk-tdd
→ tk-implement ... tdd

tk-codebase-design
→ diff 구조 검토: tk-implement built-in review
→ regression seam 문제: tk-to-spec bug contract + tk-implement investigation

tk-code-review
→ implementation diff: tk-implement built-in Standards/Spec review
→ review-only: 일반 read-only review

tk-diagnosing-bugs
→ bug source: tk-to-spec 또는 tk-to-tickets
→ 원인 불명 구현: tk-implement conditional investigation
```

## Invocation Changes

```text
user-invoked 유지: tk-grill-me, tk-implement
hybrid 전환: tk-to-spec, tk-to-tickets, tk-prototype, tk-reflect, tk-learn, tk-grooming, tk-handoff
hybrid 추가: tk-drive
hybrid 유지: tk-browser-verify, tk-merge-conflict
```

Hybrid skills can be selected directly and can be applied implicitly only in their documented trigger boundary. `tk-drive` is hybrid for same-conversation pending-answer resume, but a new workflow still requires explicit `$tk-drive`. User-invoked skills still require explicit selection.

## Follow-up Work

TigerKit 20 does not require a new skill for every follow-up.

```text
small or obvious feedback → continue current conversation
separate strategy, verification, commit → tk-implement
unknown-cause implementation → tk-implement investigation loop
independent review-only request → ordinary read-only review
reusable lesson → tk-reflect, then optionally tk-learn
```

## Repository Documentation

Feature branches no longer accumulate `CONTEXT.md`, glossary, domain documents, or ADRs automatically. Keep branch-local decisions in conversation, `.tigerkit/spec.md`, `.tigerkit/tickets.md`, commits, PR descriptions, code, and tests.

Request an ADR explicitly only for a long-lived repository constraint with meaningful alternatives and a non-obvious rationale.

## Preserved v18.0.4 Contracts

`tk-implement` keeps:

- non-destructive inspection before strategy approval
- direct/delegated and TDD choice
- non-agent tools available in direct mode
- one-level delegation
- incremental and final verification
- current-branch commit after successful verification
- no commit on change-related failure
- no push, PR, merge, tag, release, or publish

`tk-browser-verify` keeps owned/attached/lazy session ownership, first-run handling without Chrome login or sync, owned-only cleanup, broad process-kill prohibition, runtime evidence, and `Pass | Fail | Unverifiable` verdicts.

## Legacy TigerKit 16 State

Legacy Claude Code plugin state is not migrated. TigerKit does not discover, import, merge, or copy global state, repo keys, ledgers, browser profiles, credentials, or old evidence automatically. Inspect individual files manually and copy only current, non-sensitive facts when needed.

Current scratch remains repo/worktree-local `.tigerkit/`. TigerKit does not modify consumer `.gitignore` files.
