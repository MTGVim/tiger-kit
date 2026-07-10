---
name: prototype
description: prototype 검증 트리거입니다.
---

# Prototype

검증이 목적이지 production finish가 목적이 아닌 prototype용 skill입니다.

## Goal

- UI 방향이나 state/logic 가설을 빨리 확인합니다.
- production merge 전에 버릴 수 있는 실험 결과를 만듭니다.
- 무엇이 fake인지, 무엇이 실제 연결인지 분리합니다.

## Modes

- `ui`: 레이아웃, interaction, visual flow 확인
- `logic`: state, branching, reducer, parser, adapter 같은 핵심 로직 확인

## Process

1. prototype question을 한 줄로 다시 적습니다.
2. `ui`인지 `logic`인지 먼저 고릅니다.
3. 최소 파일과 최소 코드만 만듭니다.
4. production 추상화, error handling, config generalization에 과투자하지 않습니다.
5. prototype임을 파일명/경로/설명에서 드러냅니다.
6. 끝날 때 아래를 구분해서 보고합니다.
   - 확인된 것
   - 아직 fake인 것
   - production에 옮길 때 필요한 다음 단계

## Boundaries

- no-commit 기본
- throwaway 전제
- 테스트/타입/아키텍처를 production 수준으로 다듬는 데 과투자 금지
- prototype 성공을 곧 merge-ready로 보고하지 않음

## Good use cases

- 모달/폼/플로우 UI 검증
- reducer/state machine 방향 검증
- adapter shape 실험
- 특정 구현 방향이 먹히는지 빨리 확인할 때
