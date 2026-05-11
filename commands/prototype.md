---
description: FE 화면 설계를 커밋 전에 검증하는 throwaway UI prototype을 만듭니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, 식별자, UI taxonomy는 원문 그대로 유지할 수 있습니다.

목표: FE 화면이나 interaction 결정을 production 코드로 확정하기 전에, 사용자가 브라우저에서 직접 비교할 수 있는 throwaway UI prototype을 만듭니다.

이 명령은 UI prototype 전용입니다. business logic, state machine, data model을 손으로 눌러보는 terminal prototype은 이 command 범위 밖입니다.

## 핵심 원칙

prototype은 오래 남길 코드가 아니라 질문 하나에 답하기 위한 throwaway code입니다.

반드시 먼저 답할 질문을 한 줄로 적습니다.

예:

```text
기존 `/settings` 화면에서 billing section 배치를 세 가지 variant로 비교한다.
```

## Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다.

UI/UX 판단, variant 설계, responsive layout, visual polish가 핵심이면 `tk-nemelex-xobeh`를 사용합니다. screenshot, PDF, 기존 화면 capture를 해석해야 하면 먼저 `tk-ashenzari`로 관찰을 구조화합니다. business logic, state machine, data model 결정은 prototype agent routing 대상이 아닙니다.

## route 선택

기본은 기존 화면에 붙이는 방식입니다.

### A. 기존 page에 붙이기, 기본값

이미 관련 route가 있으면 그 route를 유지합니다.
기존 data fetching, params, auth는 유지하고 rendering subtree만 variant별로 바꿉니다.

새 section이나 card라도 자연스럽게 들어갈 기존 page가 있으면 기존 page 안에 붙입니다.

### B. 새 prototype route, 최후 수단

기존 page에 붙일 곳이 없을 때만 throwaway route를 만듭니다.
프로젝트 routing convention을 따르고, path나 filename에 `prototype`을 넣어 production code가 아님을 드러냅니다.

## variant 규칙

기본 variant 수는 3개입니다. 최대 5개를 넘기지 않습니다.

각 variant는 구조적으로 달라야 합니다.

좋은 차이:
- layout 차이
- information hierarchy 차이
- primary affordance 차이
- navigation/flow 차이

나쁜 차이:
- 색만 다름
- copy만 다름
- 같은 card grid를 조금 바꿈

각 variant는 명확한 이름을 둡니다.

예:

```text
VariantA: Table-first layout
VariantB: Sidebar summary layout
VariantC: Timeline layout
```

## 연결 방식

하나의 route에서 `?variant=` URL search param으로 variant를 전환합니다.

예시 흐름:

```tsx
const variant = searchParams.get('variant') ?? 'A';

return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A', 'B', 'C']} current={variant} />
  </>
);
```

기존 page에 붙이는 경우 data fetching은 switcher 위에 그대로 두고, rendered subtree만 바꿉니다.

## floating switcher

화면 하단 중앙에 prototype 전용 switcher를 둡니다.

필수 동작:
- 왼쪽 화살표: 이전 variant로 순환
- 현재 variant label 표시
- 오른쪽 화살표: 다음 variant로 순환
- URL search param 업데이트
- reload 후에도 같은 variant 유지
- `←`, `→` 키로 전환
- input, textarea, contenteditable focus 중에는 arrow key를 가로채지 않음
- production build에서는 숨김

switcher는 평가용 UI임을 알 수 있게 page 디자인과 시각적으로 구분합니다.

## 금지

- prototype에서 real mutation을 기본값으로 연결하지 않습니다.
- real DB persistence를 기본값으로 쓰지 않습니다.
- test, abstraction, production-grade error handling을 추가하지 않습니다.
- variant끼리 layout을 과하게 공유하지 않습니다.
- prototype code를 그대로 production으로 승격하지 않습니다.

## handoff

완료 후 사용자에게 다음만 짧게 줍니다.

- 실행 명령 또는 URL
- variant key 목록
- 비교해야 할 질문
- cleanup 기준

## cleanup

답이 나오면 winner와 이유만 남깁니다.

- 기존 page에 붙인 prototype: loser variant와 switcher 삭제, winner를 production 코드로 다시 정리
- 새 prototype route: winner를 실제 route로 옮기고 throwaway route 삭제

명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.
