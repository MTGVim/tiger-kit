---
description: 세션 handoff를 만듭니다.
argument-hint: '"[goal or audience]" [--output <path>] [--print-only]'
flow: [handon, next]
---

이 문서는 TigerKit `/tk:handoff` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:handoff`는 다음 세션이나 다른 에이전트가 바로 이어서 실행할 수 있는 handoff artifact를 만드는 surface입니다.

related wrapper skill:

```text
skills/handoff/SKILL.md
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- 기본은 repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first write
- 대화 전문 복붙 금지
- 이미 있는 PRD/ADR/issue/diff는 경로/링크 참조 우선
- unverifed success를 handoff에 넣지 않음

## Required sections

아래 항목은 빠지면 안 됩니다.

- Goal
- Current state
- Decisions made
- Changed files
- Commands run
- Verification status
- Remaining tasks
- Open questions
- Risks
- Suggested next skills/commands
- Do-not-repeat context

## Default write target

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py` helper가 계산합니다.

같은 current handoff를 다시 읽으려면 `/tk:handon`을 사용합니다.

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Handoff 완료 | Handoff 미리보기 | Handoff 중단
🎯 Goal:
- <one-line goal>
🧭 Output mode:
- draft file | inline preview
[📁 Output path:
- <path>]
📝 Includes:
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context
✅ Verification:
- <verified / partially verified / unverified>
▶️ Next step:
- <what the next agent should do first>
```
