---
name: tk-prototype
description: "[user] 가설을 검증하기 위한 일회용 UI 또는 로직 프로토타입을 만듭니다. 사용자가 명시적으로 호출했을 때만 사용하세요."
disable-model-invocation: true
argument-hint: "<아이디어, 스크린샷, 명세, 티켓, 코드 또는 디자인 참고 자료>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 프로토타입

사용자가 이 스킬을 명시적으로 호출했을 때만 사용하세요. 자동으로 활성화하지 마세요.

프롬프트, 아이디어, 스크린샷, 명세, 티켓, 코드 또는 디자인 참고 자료를 입력으로 받으세요. 실행 가능한 임시 라우트 또는 하네스가 더 유용하지 않다면 `.tigerkit/prototypes/<slug>/` 아래에 저장하세요. 임시 작업용 상위 디렉터리는 필요할 때만 만들고, 가능하면 원자적으로 교체하며, 자동으로 보관하거나 `.gitignore`를 편집하지 마세요. 생성된 임시 작업물이 버전 관리에서 제외되지 않으면 경고하세요.

Workflow: `가설·성공 기준 → 임시 경로와 fake/real 경계 → variants/harness → 실행 → 비교 → receipt`.

정답이 정해지지 않은 UI 디자인이나 비교 요청에는 실질적으로 다른 렌더링 변형안 2–3개와 전환 수단을 만드세요. 색상만 바꾸지 말고 정보 구조, 흐름, 계층, 탐색 또는 피드백을 달리하세요. 로직에는 실제 예시 입력/출력과 최소한의 어댑터를 갖춘 작은 순수 하네스를 우선하세요.

기본적으로 커밋하지 마세요. 프로덕션용 추상화와 오류 처리에는 투자하지 마세요. 결과물이 프로덕션에 사용할 준비가 되었다고 절대 부르지 말고, 자동으로 승격하거나 다른 사용자 스킬을 호출하지도 마세요.

## 🔴 CHECKPOINT · 🛑 STOP 실행 전·후 판정 경계

실행 전에 임시 경로, 가짜 데이터 또는 실제 연동, 검증할 질문을 확정하세요. 실행 환경이 없거나 범위가 프로덕션 변경으로 번지면 만들거나 승격하지 말고 `Blocked` 또는 `Unverifiable`로 멈추세요.

실행 결과를 보고하기 전에 명령, 실제 출력 또는 screenshot, 가짜/실제 경계, 미검증 항목을 대조하세요. 이 네 항목 중 하나라도 없거나 실행이 실패하면 `Complete`로 진행하지 말고 `Fail`, `Blocked` 또는 `Unverifiable`로 멈추세요.

## 계약

프로토타입을 실제 실행하고 명령과 결과를 기록하세요. 실패하거나 확인할 수 없으면 성공으로 보고하지 말고 `Fail`, `Blocked` 또는 `Unverifiable`로 구분하며, 가짜 데이터/연동과 실제 연결을 분리하세요. receipt에는 `상태: Complete | Fail | Blocked | Unverifiable`, 실행 명령/결과, `증거`, `미검증`, `미해결 항목`, `가짜/실제 구분`, 변형 또는 하네스, `폐기/반복/후속 판단`을 포함하고 `## Tested`, `## Variants or harness`, `## Confirmed`, `## Still fake`, `## Production implication`에 매핑하세요.

## DO NOT / ANTI-PATTERNS

- prototype을 production-ready라고 부르거나 자동 승격·commit하지 마세요.
- 가짜 연동을 실제 연결로 보고하거나 실행 증거 없이 성공을 주장하지 마세요.
- 색상만 바꾼 변형, 불필요한 production abstraction, 다른 user-invoked skill 호출을 추가하지 마세요.
