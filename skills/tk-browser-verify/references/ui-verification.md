# 선제 UI Verification

Browser 도구를 호출하거나 검증용 server를 실행하기 전에 현재 작업에 해당하는 항목만 적용하세요. 이 문서는 도구 고유 함정을 피하는 router이며 `Pass | Fail | Blocked | Unverifiable` 판정 계약을 정의하지 않습니다.

Guard mode는 적용하지 않은 항목의 N/A receipt를 만들지 않습니다. Verdict mode는 이 checklist와 `SKILL.md`의 전체 계약을 함께 따릅니다. Provider 고유 동작은 현재 도구와 버전에서 확인된 경우에만 적용하고 일반 browser 표준처럼 추정하지 마세요.

| 적용 조건 | 확인할 함정 | 상세 |
|---|---|---|
| 항상 | P1 정확히 식별한 control만 조작하고 유사 타겟을 순회하지 않음 | [동작](behavior.md) |
| 항상 | P3 trusted pointer·keyboard 입력만 상호작용 증거로 사용 | [동작](behavior.md) |
| 항상 | P8 현재 실행이 소유한 page, context, browser, PID만 정리 | [세션 수명주기](session-lifecycle.md) |
| 시각적 성공 주장 | P1 실제 screenshot과 필요한 computed 상태를 함께 확인 | [시각](visual.md) |
| CDP 연결 | P2 실제 endpoint, process, port, 격리 profile을 확인 | [환경](environment.md), [세션 수명주기](session-lifecycle.md) |
| Component·primitive migration | P4 baseline 전체 style 축과 full-width 소비처를 비교 | [시각](visual.md), [디자인](design.md) |
| API-gated 상태·native dialog | P5 정확한 response envelope mock과 사전 dialog handler 사용 | [동작](behavior.md), [안전](safety.md) |
| Screenshot 저장 | P6 도구 workspace root에 저장하고 repo 잔재를 정리 | [환경](environment.md) |
| Breakpoint·hover | P7 실제 `innerWidth`와 trusted hover 상태를 확인 | [시각](visual.md) |
| Animation·transition | P9 trigger 전 event timeline을 준비 | [동작](behavior.md) |
| 값 있는 field 비우기 | P10 실제 빈 value를 저장 전에 재확인 | [동작](behavior.md) |
| 검증용 server 실행 | Runner별 auto-open 비활성화 방법을 확인 | [환경](environment.md) |
