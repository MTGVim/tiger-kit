---
name: route
description: 지금 작업을 direct, subagent-driven, goal-driven 중 어떤 경로로 가져갈지 얇게 정리합니다.
---

# Route

지금 이 작업을 어떤 구현 경로로 가져가야 하는지 짧고 실용적으로 고르는 skill입니다.

## Goal

- direct로 바로 갈지
- subagent-driven으로 나눌지
- goal-driven orchestration이 맞는지
- 아니면 SoT/decision이 먼저인지
를 정합니다.

## Canonical routes

- `direct`
- `subagent-driven`
- `goal-driven`
- `decision`
- `need-sot`

## Process

1. task 범위와 현재 제약을 읽습니다.
2. source 수정 없이 route만 비교합니다.
3. 가능한 route의 장단점을 짧게 적습니다.
4. 가장 무난한 1안을 고르고 첫 스텝을 제안합니다.
5. SoT가 없거나 owner decision이 먼저면 억지 확정 대신 `need-sot` 또는 `decision`으로 남깁니다.

## Decision policy

- file-local이고 범위가 작으면 `direct`
- 병렬 탐색/독립 검증/역할 분리가 이득이면 `subagent-driven`
- multi-step orchestration이 핵심이면 `goal-driven`
- 제품 판단이나 owner 확인이 먼저면 `decision`
- SoT 부족이 먼저면 `need-sot`

## Boundaries

- source 수정 금지
- build/test/network 실행 금지
- approval 우회 문구 유도 금지
- 안 맞는 surface를 억지 추천하지 않음
