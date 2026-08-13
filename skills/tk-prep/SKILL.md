---
name: tk-prep
description: "[user] 명시적인 작업 원천을 저장소 근거와 자연스러운 대화로 구체화해, 새 세션이나 더 낮은 수준 실행자가 원 대화 없이 사용할 수 있는 `.tigerkit/seed.md`를 준비합니다."
disable-model-invocation: true
argument-hint: "<요청 | 이슈 | 버그 | 리뷰 원천>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 작업 준비

`/tk-prep`, `$tk-prep`, 또는 호스트의 명시적 스킬 선택으로만 시작합니다.
현재 작업을 구현하지 않고 저장소 근거와 사용자 결정을 하나의 실행 가능한 `.tigerkit/seed.md`로 준비합니다.
한 번 시작한 인터뷰는 같은 대화에서 자연스럽게 이어가며 매 답변마다 스킬을 다시 호출하게 하지 않습니다.

**대화는 자연스럽게, 상태는 엄격하게.** 내부 점수·단계·분류를 기본 UI로 덤프하지 않습니다.
이미 확인된 내용을 다시 묻지 않고, 중요한 판단은 계획과 이유를 설명해 사용자가 대화 중 수정할 수 있게 합니다.
소스, 테스트, 설정, Git, 원격 상태는 수정하지 않습니다.

## 근거와 질문

작업 원천, 저장소 지침, 관련 코드·테스트·검증 명령, 현재 branch/HEAD를 필요한 만큼 읽습니다.
새로 만들기 전에 기존 component/hook/helper/token/type/schema/client/UX pattern과 저장소 관례를 찾습니다.
근거 없는 사실은 만들지 않고 material한 저장소 주장은 가능한 경우 `path:line`, 명령 결과, current state에 연결합니다.

사용자에게 직접 묻는 것은 다음뿐입니다.

1. 제품 동작·범위·우선순위·비즈니스 규칙처럼 사용자 소유인 결정
2. 보안·권한·데이터·호환성처럼 위험하거나 되돌리기 어려운 결정
3. 충분히 개선했지만 엔지니어링 준비도를 더 올릴 수 없는 예외 승인

소스가 이미 결과를 정했다면 다시 선택 질문으로 만들지 않습니다.
한 번에 가장 영향이 큰 결정 하나만 묻고, 그 전에 현재 이해·추천안·추천 근거를 짧게 설명합니다.

## 이해 준비도

내부적으로 다음 여섯 축을 평가합니다.

| 축 | 가중치 |
| --- | ---: |
| 목표 | 20% |
| 맥락 | 20% |
| 범위 | 15% |
| 결정 | 15% |
| 수용 조건 | 15% |
| 검증 | 15% |

점수는 `0.00 | 0.25 | 0.50 | 0.75 | 1.00`만 사용합니다.
`0.00`은 근거 없음, `0.25`는 일부 단서, `0.50`은 중요한 공백, `0.75`는 실행 가능, `1.00`은 충분히 닫힌 상태입니다.

```text
ambiguity = 1 - (
  goal*0.20 + context*0.20 + scope*0.15 +
  decisions*0.15 + acceptance*0.15 + verification*0.15
)
```

다음을 모두 만족하기 전에는 인터뷰를 끝내지 않습니다.

```text
ambiguity <= 0.20
every dimension >= 0.75
material blockers == 0
unresolved material conflicts == 0
```

이 기준은 user override 불가입니다. 사용자가 점수나 계속 질문하는 이유를 물을 때만 진단을 간결하게 보여줍니다.

## 엔지니어링 준비도

다음 다섯 축은 평균으로 상쇄하지 않고 각각 평가합니다.

- **재사용** — existing primitive와 convention을 조사했는가
- **단순성** — 현재 AC에 불필요한 speculative branch, 미래 abstraction, dependency, dead code를 피했는가
- **테스트** — regression, bug reproduction, 새 non-trivial behavior와 기존 integration check를 계획했는가
- **보안** — auth/authz/input/secret/upload/redirect/storage 등 applicable boundary를 안전하게 다뤘는가
- **사용자 경험** — user-facing 변경의 responsive/state/keyboard/focus/semantic/a11y/visual fidelity를 고려했는가

각 축은 같은 점수 단위와 다음 한국어 상태를 사용합니다.

`준비됨 | 보완 필요 | 개선 한계 | 예외 승인 | 해당 없음`

`준비됨`은 `0.75+`입니다. `해당 없음`에는 이유가 필요합니다.
미달 축은 먼저 추가 조사 → 접근 개선 → 재평가합니다. 그래도 더 올릴 수 없을 때만 `개선 한계`와 gap·이유·완화책을 설명하고 사용자 예외 승인을 받습니다.
예외 승인 뒤에도 원래 점수를 높이지 않습니다.

## 브라우저 검증

browser-visible AC가 있으면 Seed 전에 다음 전략을 닫습니다.

- target URL/environment와 Pass 조건
- `headless` 여부와 viewport/state
- auth 필요 여부와 안전한 session/token/non-interactive login 경로
- dev server command/cwd/readiness
- inspected screenshot evidence와 sensitive capture/redaction
- `tk-browser-verify` 사용 여부

기본은 `headless`입니다. username/password/token/OTP/cookie/session secret value는 Seed나 채팅에 저장하지 않고 실행 시 ephemeral input으로만 다룹니다.
dev server가 필요하면 start/readiness/cleanup은 `tk-browser-verify`가 소유하도록 계획합니다.

## Seed 계약

저장소 루트의 `.tigerkit/seed.md` 하나만 현재 task context로 사용합니다.
최종 Seed는 원 대화 없는 fresh lower-capability executor가 “진행해”라는 지시만으로 올바른 작업을 시작할 수 있어야 합니다.

필요한 의미를 self-contained하게 보존합니다.

- 작업 원천·목표·배경과 current branch/HEAD 또는 exact PR head
- 현재 상태, 주요 entry point, relevant repository evidence와 convention
- 포함/제외/변경 금지 범위
- 모든 user-approved material decision과 이유
- 합의한 구현 접근, reuse/simplicity/tests/security/experience 판단
- AC와 각 AC의 verification path
- browser verification plan과 engineering waiver
- 낮은 수준 executor에게 필요한 implementation guidance, 함정, 금지 접근
- 실행 형태와 모델 수준에 대한 추천
- unresolved item

대화 transcript, worker/wave/progress, provider selector, model ID, reasoning effort, receipt, secret value는 넣지 않습니다.
실행 추천은 “독립 작업 fan-out 가능”, “중간급 coding model 권장”, “더 강한 final review 권장” 수준의 advisory입니다.
실제 실행 형태는 host/agent가 정하지만 AC와 Verification은 normative입니다.

## Ready와 진화

인터뷰 중 Seed는 `Status: Pending`입니다. 다음을 모두 만족하고 사용자가 마지막 자연어 요약을 승인한 뒤에만 `Status: Ready`로 바꿉니다.

```text
Understanding Gate pass
Engineering Gate pass or valid user waiver
no material blocker
user final approval
seed write + reread + self-contained check
```

Ready Seed를 구현 편의로 바꾸지 않습니다. 실행·검증 중 새 evidence가 goal/scope/decision/AC/required verification을 material하게 깨면 `tk-prep`으로 재진입해 영향 부분만 갱신하고 재승인합니다.
반복될 repository pitfall은 test/type/schema/policy/code invariant 같은 repo-native owner 개선 후보로만 제안하고 자동 승격하지 않습니다.
TigerKit skill 자체의 반복 실패는 `tk-skill-diagnose`/`tk-learn` 후보이며 별도 persistent pitfall corpus를 만들지 않습니다.

완료 시 Seed 경로와 핵심 합의·검증·실행 추천을 짧게 알려주고 구현을 자동 시작하지 않습니다.
