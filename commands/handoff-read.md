---
description: branch-local handoff를 읽고 현재 branch, baseline, TigerKit artifact map, durable docs 상태를 검증한 뒤 safe next action을 제시합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, URL, commit hash, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:handoff-read`는 handoff 소비 전용 명령입니다. handoff를 source of truth처럼 맹신하지 않고, 현재 repo 상태와 artifact freshness를 확인한 뒤 이어받기 준비 상태를 보고합니다.

```text
handoff-read = verify continuation contract before acting
```

## 기본 입력

- `.tigerkit/branches/{escaped-branch}/handoff.md`

## branch safety rule

handoff 읽기 전에 현재 branch를 확인합니다.

- detached HEAD이면 진행하지 않고 branch switch/create를 요청합니다.
- `main`, `master`, `develop`이면 진행하지 않고 feature branch switch/create를 요청합니다.
- handoff에 기록된 branch/HEAD와 현재 branch/HEAD를 비교합니다.

## required intake

아래를 읽거나 상태를 확인합니다.

1. 현재 branch와 HEAD
2. working tree status
3. `.tigerkit/branches/{escaped-branch}/handoff.md`
4. handoff의 Artifact Map에 있는 requirements/gap/reflect path
5. `CLAUDE.md`, if present
6. `DESIGN.md`, if present
7. `IMPLEMENTATION_POLICY.md`, if present
8. `COMPONENT_REUSE_MAP.md`, if present
9. `reuse-map.md`, legacy alias/migration candidate로만, if present

## verification rule

handoff 내용을 그대로 실행하지 않습니다. 먼저 아래를 분리합니다.

- matched: handoff와 현재 repo 상태가 일치
- stale: handoff baseline 이후 변경 가능성 있음
- missing: handoff가 가리키는 artifact가 없음
- conflict: handoff decision과 현재 evidence가 충돌
- needs user confirmation: 사용자 답 없이는 진행 위험

## classification rule

handoff의 분류를 존중하되 현재 evidence로 검증합니다.

```text
Decision = 사용자 또는 SOT가 확정
Evidence = 직접 관찰
Interpretation = evidence에서 추론
Not Confirmed = 아직 확인하지 않음
Ambiguity = 확인했지만 source가 결론을 지지하지 않거나 source끼리 충돌
```

모호하지 않은 항목을 새 ambiguity로 만들지 않습니다. 아직 확인하지 않은 항목은 `Not Confirmed`로 유지합니다.

## CLAUDE.md TigerKit section check

`CLAUDE.md`가 있으면 TigerKit managed section 존재 여부를 확인합니다.

Marker:

```md
<!-- TIGERKIT:START -->
<!-- TIGERKIT:END -->
```

없으면 추가 후보로 제안만 합니다. `/tk:handoff-read`는 `CLAUDE.md`를 직접 수정하지 않습니다.

## 금지

- implementation, commit, push, PR 생성, merge, deploy
- handoff를 읽자마자 코드 변경
- stale handoff를 current truth로 취급
- missing artifact를 추측으로 보완

## 출력

```text
handoff 읽었습니다.
- handoff: `.tigerkit/branches/feature__example/handoff.md`
- baseline match: yes
- artifact map: requirements/gap/reflect 확인
- stale risk: 없음
- 확인 필요: 1개

해야 할 일: 사용자 확인 후 GAP-001 관련 파일을 inspect하세요.
```
