---
name: gap
description: SoT gap 분석 트리거입니다.
---

# Gap

구현을 시작하기 전에 Source of Truth와 Current Implementation 사이의 핵심 차이를 드러내는 skill입니다.

## Goal

- SoT가 있으면 구현 전에 차이를 먼저 확인합니다.
- missing / mismatch / overbuilt / ambiguous를 구분합니다.
- plan-only evidence를 구현 완료 증거로 착각하지 않게 합니다.

## Process

1. source ref 목록과 access status를 먼저 고정합니다.
2. SoT에서 확인 가능한 requirement만 뽑습니다.
3. Current evidence를 직접 읽은 파일, 실행 결과, rendered output, diff, generated artifact처럼 evidence type별로 분리합니다.
4. source 우선순위가 불명확하면 조용히 섞지 않고 `ambiguous`로 남깁니다.
5. finding마다 SoT / Current / Evidence / Impact / Priority / Suggested fix를 남깁니다.
6. actionable finding에는 `direct | brainstorm | decision` route를 제안합니다.

## Gap types

- `missing`: SoT 요구가 Current에 없음
- `mismatch`: SoT와 Current가 다름
- `overbuilt`: SoT 밖 구현이 surface 확장이나 유지비를 만든다
- `ambiguous`: source conflict, owner decision 부족, evidence 부족

## Boundaries

- workflow 생성 금지
- autopilot / runner / sealed flow 생성 금지
- finding이 0개 될 때까지 무한 반복 금지
- 검증 없는 success 선언 금지

## Good use cases

- PRD 대비 구현 점검
- spec 대비 branch 상태 점검
- current main/public surface와 target contract 차이 확인
