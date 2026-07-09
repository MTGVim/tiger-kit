---
description: 현재 대화나 요구사항을 draft-only PRD로 정리합니다.
argument-hint: '"<goal|scope>" [--output <path>] [--print-only] [--publish]'
---

이 문서는 TigerKit `/tk:to-prd` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:to-prd`는 현재 대화나 요구사항을 implementation 전에 읽기 쉬운 PRD draft로 정리하는 surface입니다.

canonical skill:

```text
skills/to-prd/SKILL.md
```

## Core boundary

- default draft-only
- no-publish 기본
- approval 전 외부 tracker/doc system 반영 금지
- no interview by default
- acceptance criteria 포함 필수

## Default output target

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py` helper가 계산합니다.

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
To-PRD 완료 | To-PRD 미리보기 | To-PRD 중단
Goal:
- <what the PRD covers>
Output mode:
- draft file | inline preview
[Output path:
- <path>]
Includes:
- problem / goal / user value / non-goals / requirements / acceptance criteria / risks / open questions
Publish:
- disabled by default
Next step:
- <review draft | convert to issues | revise scope>
```

## Non-goals

- publish 기본값
- 구현 완료 보고
- acceptance criteria 없는 vague spec
