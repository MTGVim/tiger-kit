---
description: 현재 session 전체를 재구성해 durable learning과 one-off correction을 분리하고 기존 DESIGN.md/reuse-map.md 업데이트 또는 초기화 필요를 제안합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, URL, commit hash, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:reflect`는 현재 대화 context를 먼저 재구성해 derived repo knowledge를 유지합니다. `.tigerkit/reflect.md`에 reflection을 남기고, 필요할 때만 기존 `DESIGN.md`와 `reuse-map.md` 업데이트를 제안하거나 적용합니다.

```text
reflect = session-wide reconstruction and repo knowledge maintenance
```

## 기본 산출물

- `.tigerkit/reflect.md`
- 필요 시 기존 `DESIGN.md`
- 필요 시 `reuse-map.md`

`.tigerkit/reflect.md`는 TigerKit working material입니다. `DESIGN.md`와 `reuse-map.md`는 repo-level derived artifact입니다. `DESIGN.md` 초기화 알림은 derived design knowledge가 있고 파일이 없을 때만 표시합니다.

## review inputs

입력 우선순위는 아래와 같습니다.

1. 현재 대화 context
2. explicit user confirmation
3. `.tigerkit/requirements.md`
4. `.tigerkit/gap.md`
5. 최근 diff 또는 commit

현재 대화 context가 primary source입니다. artifact와 git evidence는 보조 근거입니다. 대화 context에 남아 있지 않은 내용은 추측하지 말고 `확인 불가`로 둡니다.

## reflect 대상

- repeated failure patterns
- durable learnings
- one-off corrections
- proposed updates to `DESIGN.md`
- proposed updates to `reuse-map.md`

one-off correction을 durable rule로 승격하지 않습니다. future work에 영향을 줘야 한다는 evidence가 있을 때만 durable learning으로 분리합니다.

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

prep 단계에서 업데이트하지 않습니다. reflection을 통해 제안하거나 적용합니다.

`DESIGN.md`가 없으면 새로 만들지 않습니다. `DESIGN.md`에 넣을 만한 derived design knowledge가 생겼는데 파일이 없으면, `.tigerkit/reflect.md`와 채팅 receipt에 `DESIGN.md` 초기화가 필요하다고 알립니다. `DESIGN.md`는 외부 도구나 사용자 선택으로 먼저 초기화되는 파일입니다.

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

1. 현재 대화 context에서 evidence, interpretation, decision, suggestion을 먼저 분리합니다.
2. 대화 context에 없는 내용은 `확인 불가`로 표시합니다.
3. `.tigerkit/requirements.md`와 `.tigerkit/gap.md`가 있으면 보조 근거로 읽습니다.
4. 최근 diff/commit이 있으면 보조 근거로 사용합니다.
5. durable learning과 one-off correction을 분리합니다.
6. `.tigerkit/reflect.md`를 갱신합니다.
7. `DESIGN.md`가 있으면 변경을 제안하거나, 사용자가 허용한 범위에서만 적용합니다.
8. `DESIGN.md`가 없고 넣을 derived design knowledge가 있으면 생성하지 말고 사용자에게 초기화 필요를 알립니다.
9. `reuse-map.md` 변경은 제안하거나, 사용자가 허용한 범위에서만 적용합니다.

## 금지

- artifact나 git evidence를 현재 대화 context보다 우선하기
- 대화 context에 없는 내용 추측
- one-off correction을 durable rule로 과승격
- external SOT를 `DESIGN.md`로 대체
- `DESIGN.md`가 없을 때 새로 생성
- inspect하지 않은 재사용 capability 추측
- implementation, commit, push, PR 생성, merge, deploy

## 출력

```text
reflection 정리했습니다.
- 기록: `.tigerkit/reflect.md`
- primary source: current conversation context
- durable learning: evidence 있는 항목만 분리
- one-off correction: session 한정으로 유지
- design note: 조건부 표시. `DESIGN.md`가 없고 넣을 derived design knowledge가 있을 때만 초기화 필요 알림

다음 추천: 제안된 derived knowledge 검토
```
