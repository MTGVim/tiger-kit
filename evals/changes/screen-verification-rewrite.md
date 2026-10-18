# 화면 검증 선택과 과정 재작성 범위 복원

- F1: 저장된 선호의 부재와 실행 준비 실패를 구별합니다. 승인된 브라우저 검증에서 문서화된 안전한 일회성 실행은 선택 질문 없이 진행하고, 영구 선호 저장은 명시적 요청에만 수행합니다. 기존 명시적 선택, 앱 선택, 설치·외부 변경 권한, `headless`·소유권의 실제 증명과 실패 상태를 보존합니다.
- F2: 기존 과정의 `index`와 관련 형식 설명을 먼저 읽어 현재 강의·일부 샘플·과거 대안을 구별합니다. 기존 `curriculum/profile`을 사용하며 모든 형식의 재생성이나 새 형식 장부를 요구하지 않습니다.
- F3: `no change`. OS별 인용·명령·검색 방법과 모델이 현장에서 해결할 실행 문제는 설치 명세에 추가하지 않습니다.
- 소유권: `provider` 선택 정본은 `skills/tk-browser-verify/references/provider-selection.md`이며 `scripts/verification_policy.py`가 앱 패키지로 복사합니다. `tk-teach`의 상태 복원 본문이 재작성 절차를 소유하므로 공통 형식 라우팅 정본에는 중복 지침을 추가하지 않습니다.
- `README: no public change`. `skills/tk-browser-verify/SKILL.md`, `skills/tk-teach/SKILL.md`와 패키지 참조의 내부 절차만 변경하며 이름·호출·공개 카탈로그는 유지합니다.

## 근거와 채택

2026-10-18 제공된 회고는 구체적인 기존 선택 의무와 실제 중단의 일치를 보여 줍니다. 새로운 실행 성공의 인과 증거는 아닙니다. 기준 원본은 `dc94fd51ab8ffb8987098b5d6391606d5db66abf`입니다.
현재 공식 [`Playwright launch` API](https://playwright.dev/docs/api/class-browsertype#browser-type-launch)와 [`Chrome Headless` 문서](https://developer.chrome.com/docs/automation-and-testing/headless)를 대조했습니다(2026-10-18).
`keep`: 실행 준비·실제 `headless`·소유권 검증. `adapt`: 제공된 사례의 일회성 선택과 영구 선호 결정 분리. `omit`: 특정 OS 명령, 제공자별 새 실행기와 기본값, 설정 자동 저장. 공식 문서는 실행 API의 근거이며 TigerKit의 권한 정책 자체를 정당화하지는 않습니다.

## 검증 범위

저장 선호 없음/안전한 일회성 경계, 실행 파일만 발견됨, `bootstrap` 후 소유권 미확인, 영구 설정·설치 필요, 사용자 요청 선호 결정, 일반 재작성의 부분 만화 샘플, 명시적 만화 재작성 사례를 평가 계약에 추가하거나 명시적으로 이관합니다. 기존 저장 선호 실패·사용자 프로필 거부 사례는 유지합니다. 문서 계약 검사와 독립 검수는 실제 브라우저 실행이나 독립 모델 행동 재현을 대신하지 않습니다.
