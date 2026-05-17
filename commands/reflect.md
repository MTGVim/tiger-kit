---
description: 현재 session 전체를 branch-local .tigerkit/branches/{escaped-branch}/reflect.md에 재구성하고 CLAUDE.md/MEMORY.md/DESIGN.md/reuse-map.md 격상 후보를 제안합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, URL, commit hash, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:reflect`는 현재 대화 context를 먼저 재구성해 derived repo knowledge를 유지합니다. `.tigerkit/branches/{escaped-branch}/reflect.md`에 reflection을 남기고, `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` escalation 후보를 제안합니다.

```text
reflect = session-wide reconstruction and repo knowledge maintenance
```

## 기본 산출물

- `.tigerkit/branches/{escaped-branch}/reflect.md`

Escalation 후보:

- `CLAUDE.md`
- `MEMORY.md`
- `DESIGN.md`
- `reuse-map.md`

`reflect.md`는 branch-local working material입니다. Escalation 대상은 durable guidance 또는 derived repo-level knowledge입니다.

## branch safety rule

reflect 기록 전에 현재 branch를 확인합니다.

- detached HEAD이면 기록하지 않고 branch switch/create를 요청합니다.
- `main`, `master`, `develop`이면 기록하지 않고 feature branch switch/create를 요청합니다.
- root-level `.tigerkit/reflect.md`는 deprecated artifact이며 migration 후보로만 표시합니다.

## review inputs

입력 우선순위는 아래와 같습니다.

1. 현재 대화 context
2. explicit user confirmation
3. `.tigerkit/branches/{escaped-branch}/requirements.md`
4. `.tigerkit/branches/{escaped-branch}/gap.md`
5. `.tigerkit/branches/{escaped-branch}/handoff.md`, if present
6. 최근 diff 또는 commit
7. `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md`, if present

현재 대화 context가 primary source입니다. artifact와 git evidence는 보조 근거입니다. 대화 context에 없는 내용은 추측하지 말고 `확인 불가`로 둡니다.

## reflect 대상

- repeated failure patterns
- durable learnings
- one-off corrections
- proposed updates to `CLAUDE.md`
- proposed updates to `MEMORY.md`
- proposed updates to `DESIGN.md`
- proposed updates to `reuse-map.md`

one-off correction을 durable rule로 승격하지 않습니다. future work에 영향을 줘야 한다는 evidence가 있을 때만 durable learning으로 분리합니다.

## escalation gate

`reflect.md` 갱신과 durable artifact 반영을 반드시 분리합니다.

1. 먼저 `.tigerkit/branches/{escaped-branch}/reflect.md`를 기록합니다.
2. 다음 대상별 escalation candidate를 분류합니다.
   - `CLAUDE.md`: repo instruction 또는 TigerKit managed section에 넣을 future-facing rule. managed section이 없으면 실제 반영을 강하게 추천할 고우선 후보로 취급
   - `MEMORY.md`: 사용자 preference, project direction, reference, feedback으로 유지할 내용
   - `DESIGN.md`: architecture, boundary, data flow, stable design decision
   - `reuse-map.md`: inspect한 component/hook/util/API/pattern 재사용 정보
3. 사용자에게 실제 반영할지 묻습니다.
4. 승인된 파일만 수정합니다.
5. 승인 전에는 durable artifact를 수정하지 않습니다.

Receipt에는 아래 상태를 명시합니다.

- `recorded only`: `reflect.md`만 갱신
- `applied`: 실제 반영한 durable artifact 목록
- `pending escalation`: 반영 후보 목록
- `skipped`: 파일 없음, 사용자 미승인, evidence 부족 같은 이유

## CLAUDE.md

`CLAUDE.md`는 repo instruction입니다. TigerKit이 durable workflow rule을 발견하면 managed section 추가 또는 갱신 후보를 제안할 수 있습니다. 특히 managed section이 없으면 약한 참고가 아니라 실제 반영을 강하게 추천해야 할 고우선 escalation candidate로 다룹니다.

Marker:

```md
<!-- TIGERKIT:START -->
<!-- TIGERKIT:END -->
```

`CLAUDE.md`가 없으면 새로 만들지 않습니다. 사용자 승인 없이 marker 밖 내용을 수정하지 않습니다.

## MEMORY.md

`MEMORY.md`는 Claude Code memory index입니다. 사용자 preference, project direction, reference, feedback으로 유지할 내용만 escalation candidate가 됩니다.

`MEMORY.md`와 개별 memory file 수정은 사용자 승인 후에만 수행합니다. One-off correction은 durable evidence가 없으면 memory candidate로 만들지 않습니다.

## DESIGN.md

`DESIGN.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다.

담을 수 있는 것:

- architecture overview
- feature boundaries
- data flow
- UI conventions
- API integration patterns
- stable constraints
- non-goals
- repo-specific design decisions

prep 단계에서 업데이트하지 않습니다. reflection을 통해 제안하거나, escalation gate에서 사용자 승인 후 적용합니다.

`DESIGN.md`가 없으면 새로 만들지 않습니다. `DESIGN.md`에 넣을 만한 derived design knowledge가 생겼는데 파일이 없으면, `.tigerkit/branches/{escaped-branch}/reflect.md`와 채팅 receipt에 `DESIGN.md` 초기화가 필요하다고 알립니다. `DESIGN.md`는 외부 도구나 사용자 선택으로 먼저 초기화되는 파일입니다.

## reuse-map.md

`reuse-map.md`는 LLM이 기존 코드를 재발명하지 않도록 돕는 derived leverage map입니다.

담을 수 있는 것:

- reusable components
- hooks
- utilities
- API clients
- form patterns
- validation patterns
- UI composition patterns
- test helpers
- deprecated patterns to avoid

구체 reference를 선호합니다.

```md
## Components

### Button

Path:
- src/components/Button.tsx

Use when:
- Standard button UI가 필요할 때.

Known variants:
- primary
- secondary
- ghost

Example usage:
- src/features/example/ExampleForm.tsx
```

inspect하지 않은 capability, prop, behavior를 만들지 않습니다.

## 절차

1. 현재 branch를 확인합니다.
2. detached HEAD 또는 protected branch이면 branch switch/create를 요청하고 멈춥니다.
3. 현재 대화 context에서 evidence, interpretation, decision, suggestion을 먼저 분리합니다.
4. 대화 context에 없는 내용은 `확인 불가`로 표시합니다.
5. branch-local requirements/gap/handoff artifact가 있으면 보조 근거로 읽습니다.
6. 최근 diff/commit이 있으면 보조 근거로 사용합니다.
7. durable learning과 one-off correction을 분리합니다.
8. `.tigerkit/branches/{escaped-branch}/reflect.md`를 갱신합니다.
9. `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` escalation candidates를 제안합니다. `CLAUDE.md` managed section이 없으면 강한 반영 추천 상태를 분명히 표시합니다.
10. 사용자 승인 전에는 durable artifact를 수정하지 않습니다.

## 금지

- artifact나 git evidence를 현재 대화 context보다 우선하기
- 대화 context에 없는 내용 추측
- one-off correction을 durable rule로 과승격
- external SOT를 `DESIGN.md`로 대체
- `DESIGN.md`가 없을 때 새로 생성
- inspect하지 않은 재사용 capability 추측
- 사용자 승인 없이 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` 수정
- implementation, commit, push, PR 생성, merge, deploy

## 출력

```text
reflection 기록했습니다.
- 기록: `.tigerkit/branches/feature__example/reflect.md`
- primary source: current conversation context
- recorded only: `reflect.md`
- pending escalation: `CLAUDE.md` managed section 추가 강한 추천, `reuse-map.md`

질문: 위 후보를 실제 반영할까요?
```
