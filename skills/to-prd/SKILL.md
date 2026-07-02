---
name: to-prd
description: 현재 대화나 요구사항을 draft-only PRD로 정리합니다.
---

# To PRD

대화나 메모를 바로 구현으로 밀기 전에, 기능 요구를 PRD draft로 압축 정리하는 skill입니다.

## Goal

- 요구사항을 기능 문서로 정리합니다.
- acceptance criteria를 명시합니다.
- issue publish나 외부 반영 없이 draft를 먼저 만듭니다.

## Process

1. 현재 대화와 명시된 요구를 읽습니다.
2. 이미 정해진 범위와 아직 열린 질문을 분리합니다.
3. 아래 항목을 갖춘 PRD draft를 만듭니다.
   - problem / goal
   - user value
   - non-goals
   - requirements
   - acceptance criteria
   - risks / open questions
4. 기본은 인터뷰를 길게 끌지 않고, 부족한 점만 최소 질문합니다.
5. 외부 publish 없이 draft artifact만 만듭니다.

## Boundaries

- default draft-only
- no-publish 기본
- approval 전 tracker 반영 금지
- 문서 생성이 구현 완료를 뜻하지 않음

## Good use cases

- 구현 전 요구를 고정해야 할 때
- plan 전에 acceptance criteria를 먼저 세우고 싶을 때
- issue 분해 전 PRD 형태가 필요한 때
