---
name: tk-browser-verify
description: "[user/auto] 런타임 증거로 브라우저 UI, 동작, 환경 차이, 디자인 충실도를 검증합니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 브라우저 검증

직접 사용하거나 관련 구현 중에 사용하세요. 별도 설정 없이 작업하세요. 요청을 이해하고, 실행 가능한 환경을 찾고, 사용 가능한 네이티브 브라우저, Playwright 호환 드라이버, MCP 또는 CDP 드라이버를 선택하고, 탐색하고, 상호작용하고, 관찰하세요. 프로필은 선택 사항입니다.

새 브라우저를 시작하면 [세션 수명주기](references/session-lifecycle.md)를 따르세요. 브라우저 자체의 최초 실행·로그인·동기화 안내는 가능한 실행 옵션으로 억제하고, 남아 있으면 로그인하지 말고 안전하게 건너뛰거나 닫으세요. 검증 종료 시 이번 실행이 직접 만든 브라우저·컨텍스트·창만 정리하고 기존 사용자 세션은 건드리지 마세요.

관련 관점을 선택하세요. [시각](references/visual.md), [동작](references/behavior.md), [환경](references/environment.md) 또는 [디자인](references/design.md)을 사용하고 [안전](references/safety.md)을 따르세요. 합성 이벤트보다 신뢰할 수 있는 포인터/키보드 상호작용을 우선하세요.

변경 작업에는 UI 전환, 네트워크 요청/응답, 최종 UI 상태가 모두 필요합니다. 토스트나 국소적인 DOM 변경만으로는 충분하지 않습니다. 위험하고 되돌릴 수 없는 작업에 안전한 환경이나 명시적 권한이 없으면 `Unverifiable`을 반환하세요.

유용한 증거만 `.tigerkit/browser-verify/runs/<run-id>/` 아래에 저장하고, 빈 파일은 만들지 마세요. 가능하면 `YYYYMMDD-HHmmss-<short-slug>`를 사용하세요. 확인된 민감하지 않은 사실은 필요할 때 `.tigerkit/browser-verify/env.md` 또는 `.tigerkit/browser-verify/screens/<screen>.md`에 기록하세요. 상위 스크래치 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, `.gitignore`를 절대 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. `login.local.md`를 자동으로 만들지 마세요. 사용자가 명시적으로 요청하면 내용을 출력하지 말고 가능하면 모드 `0600`을 사용하세요. 레거시 전역 TigerKit 상태를 검사하거나 마이그레이션하지 마세요.

프로덕션 코드를 편집하거나 증거를 규칙/스킬로 승격하지 마세요. `## Verdict` (`Pass | Fail | Unverifiable`), `## Verified`, `## Findings`, `## Evidence`, `## Unverified`를 출력하고 빈 섹션은 생략하세요.
