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
2. same repo/scope `gap packet`이 있으면 source set, precedence, ambiguity를 먼저 읽고 재사용합니다.
   - helper surface가 있으면 `read-gap-packet`으로 현재 packet을 읽고, 없으면 packet 없이 진행합니다.
3. source 수정 없이 route만 비교합니다.
4. 가능한 route의 장단점을 짧게 적습니다.
5. 가장 무난한 1안을 고르고 첫 스텝을 제안합니다. 역할/문맥 분리가 route 이유라면 compact delegation plan도 같이 적습니다.
6. `goal-driven`이고 host가 `/goal`을 지원하면 ready-to-run `/goal <추천 목표>`를 같이 제안할 수 있습니다.
7. SoT가 없거나 owner decision이 먼저면 억지 확정 대신 `need-sot` 또는 `decision`으로 남깁니다.

## Decision policy

- `direct`는 순수 기계적 변경이고, file-local이며, 낮은 리스크이고, 의미 있는 설계 판단이 거의 없을 때만 우선 검토합니다.
- diff가 작더라도 아래 조건이면 `subagent-driven`을 우선 검토합니다.
  - 메인 세션이 이미 긴 planning/design을 거쳤고 구현은 깨끗한 brief에서 다시 시작하는 편이 나을 때
  - 병렬 탐색, 독립 검증, reviewer/implementer 분리 이점이 클 때
  - clean implementor context가 중요해서 구현자는 좁은 implementation brief만 받아야 할 때
  - adversarial diff-only review가 regression 탐지에 더 유리할 때
  - behavior, data flow, auth, permissions, billing, migrations, caching, concurrency, error handling 같은 리스크 경로를 건드릴 때
  - 테스트가 약하거나 없어 cold review가 도움이 될 때
  - 더 강한 모델은 설계, 더 빠른 모델은 구현처럼 역할 분리 이점이 있을 때
- multi-step orchestration이 핵심이면 `goal-driven`
- 제품 판단이나 owner 확인이 먼저면 `decision`
- SoT 부족이 먼저면 `need-sot`

## Boundaries

- source 수정 금지
- build/test/network 실행 금지
- approval 우회 문구 유도 금지
- 안 맞는 surface를 억지 추천하지 않음
- `/goal` suggestion은 host가 실제로 그 surface를 지원할 때만 제안
