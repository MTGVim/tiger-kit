---
name: to-issues
description: issue 분해 트리거입니다.
---

# To Issues

plan/PRD를 바로 구현 가능한 issue draft 묶음으로 쪼개는 skill입니다.

## Goal

- 병렬로 잡아갈 수 있는 작업 단위를 만듭니다.
- layer별 분해가 아니라 user value 기준 vertical slice로 나눕니다.
- publish 전에 draft를 먼저 만듭니다.

## Process

1. source plan/PRD에서 목표와 제약을 읽습니다.
2. layer별 분해를 피하고 vertical slice 후보를 먼저 만듭니다.
3. 각 issue draft에 아래를 넣습니다.
   - title
   - user value / outcome
   - scope
   - acceptance criteria
   - blocked-by / order dependency
4. 독립적으로 집을 수 없는 조각은 합치거나 다시 자릅니다.
5. 기본은 markdown draft만 만들고 외부 publish는 하지 않습니다.

## Boundaries

- default draft-only
- no-publish 기본
- no layer slicing
- task spam 금지
- 독립 실행이 안 되는 issue 쪼개기 금지

## Good use cases

- 병렬 agent 실행 전 issue slicing
- PRD를 GitHub/Linear draft로 옮기기 전 정리
- 구현 순서와 dependency를 명시적으로 나눌 때
