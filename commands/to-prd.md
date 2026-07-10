---
description: draft PRD를 작성합니다.
argument-hint: '"<goal or requirement>" [--output <path>] [--print-only]'
flow: [to-issues, route, next]
---

이 문서는 TigerKit `/tk:to-prd` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:to-prd`는 현재 대화나 요구사항을 implementation 전에 읽기 쉬운 PRD draft로 정리하는 surface입니다.

related wrapper skill:

```text
skills/to-prd/SKILL.md
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- default draft-only
- no-publish 기본
- approval 전 외부 tracker/doc system 반영 금지
- no interview by default
- acceptance criteria 포함 필수

## Interview mode

- `--interview`는 opt-in 입니다.
- 한 번에 한 질문만 던집니다.
- 아키텍처를 바꿀 질문, 경계/owner를 가르는 질문을 우선합니다.
- `grill`처럼 기존 계획을 압박 검증하는 surface가 아니라, 아직 비어 있는 요구를 수집하는 surface입니다.

## Reference slot

PRD에는 optional reference slot을 둘 수 있습니다.

- reference implementation
- mockup / screenshot / URL
- similar code / prior artifact

장문 요구보다 reference가 더 강한 guide면 그것을 먼저 적고, reference가 어디까지 binding인지 같이 남깁니다.

## Default output target

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py` helper가 계산합니다.

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
To-PRD 완료 | To-PRD 미리보기 | To-PRD 중단
🎯 Goal:
- <what the PRD covers>
🧭 Output mode:
- draft file | inline preview
[🧪 Interview mode:
- off | on]
[📁 Output path:
- <path>]
📝 Includes:
- problem / goal / user value / non-goals / requirements / acceptance criteria / risks / open questions
[📝 References:
- <reference implementation | mockup | URL | prior artifact>]
📝 Publish:
- disabled by default
▶️ Next step:
- <review draft | convert to issues | revise scope>
```
