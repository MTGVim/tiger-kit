---
description: 현재 branch 작업 맥락, TigerKit artifact map, gap 상태, ambiguity 상태, 다음 safe action을 .tigerkit/branches/{escaped-branch}/handoff.md에 기록합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, URL, commit hash, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:handoff-write`는 다음 모델이나 다음 세션이 source-loss 없이 이어받을 수 있도록 branch-local operational handoff를 작성합니다.

```text
handoff-write = continuation contract + artifact map + baseline checkpoint
```

## 기본 산출물

- `.tigerkit/branches/{escaped-branch}/handoff.md`

## branch safety rule

handoff 작성 전에 현재 branch를 확인합니다.

- detached HEAD이면 기록하지 않고 branch switch/create를 요청합니다.
- `main`, `master`, `develop`이면 기록하지 않고 feature branch switch/create를 요청합니다.
- working tree 상태와 HEAD commit hash를 handoff에 기록합니다.

## inputs

아래를 확인합니다.

1. 현재 대화 context
2. explicit user confirmation
3. `.tigerkit/branches/{escaped-branch}/requirements.md`, if present
4. `.tigerkit/branches/{escaped-branch}/gap.md`, if present
5. `.tigerkit/branches/{escaped-branch}/reflect.md`, if present
6. `CLAUDE.md`, if present
7. `DESIGN.md`, if present
8. `IMPLEMENTATION_POLICY.md`, if present
9. `COMPONENT_REUSE_MAP.md`, if present
10. `reuse-map.md`, legacy alias/migration candidate로만, if present
11. 최근 diff 또는 commit

## handoff shape

```md
# TigerKit Handoff

## Current Goal

## Write-Time Context

- Branch:
- HEAD:
- Working tree:
- Last verification:

## TigerKit Artifact Map

### Requirements Index

- Path:
- Status:
- Relevant entries:

### Gap Records

- Path:
- Status:
- Open gaps:
- Resolved gaps:

### Reflection

- Path:
- Status:
- Escalation candidates:

## Decisions

## Evidence

## Interpretation

## Not Confirmed

## Ambiguities

## Open Questions

## 이어서 확인할 안전한 행동

## Do Not Do

## Key Files To Read First
```

## classification rule

항상 구분합니다.

```text
Decision = 사용자 또는 SOT가 확정
Evidence = 직접 관찰
Interpretation = evidence에서 추론
Not Confirmed = 아직 확인하지 않음
Ambiguity = 확인했지만 source가 결론을 지지하지 않거나 source끼리 충돌
```

모호하지 않은 항목을 ambiguity로 승격하지 않습니다. 아직 확인하지 않은 항목은 `Not Confirmed`로 둡니다.

## 금지

- implementation, commit, push, PR 생성, merge, deploy
- handoff를 task queue로 바꾸기
- source가 지지하지 않는 결론을 decision으로 저장
- `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md` root artifact를 새로 쓰기

## 출력

```text
handoff 기록했습니다.
- 기록: `.tigerkit/branches/feature__example/handoff.md`
- baseline: `abc1234`
- artifact map: requirements/gap/reflect 상태 포함
- open gaps: 2
- ambiguity: 1

해야 할 일: 이어받는 세션에서는 handoff 내용을 먼저 확인하고 baseline이 stale하지 않은지 점검하세요.
```
