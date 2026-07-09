---
description: boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only 구조 리뷰입니다.
argument-hint: '"<scope|goal|area>" [--target <path|area>] [--print-checklist]'
---

이 문서는 TigerKit `/tk:arch-review` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:arch-review`는 코드베이스의 구조적 문제를 바로 리팩터링으로 밀지 않고, boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only surface입니다.

canonical skill:

```text
skills/arch-review/SKILL.md
```

## Core boundary

- report-only
- source 수정 금지
- auto refactor 금지
- auto rename 금지
- auto docs rewrite 금지
- architecture polish를 implemented work처럼 보고하지 않음
- 막연한 "다 갈아엎자" 대신 가장 작은 다음 스텝을 제안

## Review lens

1. boundary leak: module/service/layer 경계가 새는가
2. ownership confusion: 어느 파일/컴포넌트가 책임을 가져야 하는지 흐려졌는가
3. coupling hotspot: 바뀔 때마다 여러 파일이 같이 흔들리는 축이 있는가
4. repeated pain: 같은 종류의 수정/버그/충돌이 반복되는가
5. migration shape: 큰 공사 대신 단계적 정리가 가능한가

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Arch Review 완료 | Arch Review 중단
📍 Scope:
- <target area>
💪 Strengths:
- <what is already clean>
🔥 Hotspots:
- <confirmed architectural hotspots>
⚠️ Boundary risks:
- <where ownership/coupling leaks>
🔎 Evidence:
- <file / behavior / repeated pain evidence>
🧭 Suggested direction:
- <smallest safe architectural direction>
▶️ First step:
- <one concrete next step>
```

## Non-goals

- 구현 완료 보고
- 근거 없는 대수술 제안
- source write 없는 척하면서 사실상 리팩터링 강행
- README/RFC 작성만으로 구조 문제가 해결됐다고 주장
