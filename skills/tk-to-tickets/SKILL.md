---
name: tk-to-tickets
description: "[user/auto] 요청이나 Ready 명세를 독립 검증 가능한 수직 티켓으로 나눌 때 사용합니다. 명확한 decomposition 요청에 적용하고, 명세 작성·원격 issue 생성·구현 요청에는 적용하지 않습니다."
argument-hint: "<명세, 계획 또는 요청> [--output <경로>]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# 티켓 작성

명시 호출 또는 수직 티켓 분해를 요구하는 명확한 자연어 요청에 사용하세요. 명세 작성, 원격 issue 생성, 구현 요청 또는 active `tk-drive` phase에는 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 대화, `.tigerkit/spec.md`, 요청, 관련 코드 순입니다.

## Workflow

1. `source 요구사항 추출`: 입력은 우선순위가 정해진 소스이고, 출력은 요구사항·인수 기준 ID, 원문 위치와 `confirmed | unverified | conflict` 상태입니다.
2. `vertical slice`: 입력은 확인된 요구사항이고, 출력은 초기 `Status: pending`과 독립 목표·범위·동작·테스트를 함께 가진 티켓 후보입니다.
3. `인수 기준·검증`: 입력은 티켓 후보이고, 출력은 관찰 가능한 인수 기준과 실행할 검증 명령 또는 증거입니다.
4. `traceability·의존성`: 입력은 티켓과 source map이고, 출력은 source ID별 coverage, 선행 티켓, 미해결 분할 문제입니다.
5. `checkpoint`: 입력은 분할 근거·traceability·충돌 목록이고, 출력은 쓰기 가능 여부 또는 `Unresolved split report | Blocked | Unverifiable`입니다.
6. `write/verify/receipt`: 입력은 checkpoint를 통과한 티켓과 경로이고, 출력은 작성된 경로와 재검증된 source ID coverage·의존성 또는 report-only receipt입니다.

사용자가 지정한 경로 또는 `.tigerkit/tickets.md`에 `# <Feature> Tickets` 형식으로 작성하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 타임스탬프 아카이브를 생성하거나 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 경고하세요. 구현하거나 원격 트래커에 게시하지 마세요.

## Failure paths

| Trigger | Terminal state | Recovery |
|---|---|---|
| 독립 분할 근거 부족 | `Unresolved split report` | 근거 없는 티켓을 만들지 않고 분할을 막는 요구사항·의존성을 보고 |
| confirmed source 간 충돌 또는 사용자 결정 부재 | `Blocked` | 충돌 ID와 필요한 결정 하나를 특정하고 write하지 않음 |
| 필수 source 접근 실패로 traceability를 만들 수 없음 | `Unverifiable` | 읽지 못한 경로·오류·영향 ID를 기록하고 write하지 않음 |
| checkpoint 이후 source ID·상태 또는 기존 대상이 달라짐 | `Blocked` | 기존 대상을 덮어쓰지 않고 새 evidence로 checkpoint를 다시 실행 |
| write/rename 실패 | `Fail` | 손상되지 않은 기존 대상을 보존하고 이번 실행의 변경만 정확히 복원·재검증 |
| post-write coverage·UI literal·의존성 불일치 | `Fail | Unverifiable` | 완료로 보고하지 않고 추가 write를 중단해 실패 경로와 실제 상태를 receipt에 기록 |

Write/rename 후 파일을 다시 읽어 모든 confirmed source ID가 coverage table과 실제 티켓에 연결되고 의존성이 작성안과 일치하는지 확인하세요. 위 상태들을 서로 대신 사용하지 마세요.

## 계약

요구사항별 source traceability를 남기고 각 티켓을 `Status: pending`, 독립적인 목표, 범위, 인수 기준, 검증을 가진 수직 동작 단위로 구성하세요. Standalone 실행은 구현 진행 상태를 추정하지 않고 모든 새 티켓을 `pending`으로 시작합니다. Source에 requirement/acceptance ID가 있으면 티켓마다 그대로 보존하고 coverage table에서 각 ID가 어느 티켓에 연결되는지 보여주세요. Source에 ID가 없으면 원문 위치를 인용하되 source ID를 발명하지 마세요. 동작의 테스트는 해당 티켓에 포함하며 수평적인 type/API/UI/test-only 티켓을 만들지 마세요. 독립된 동작으로 분할할 근거가 부족하면 억지로 만들지 말고 `Unresolved split report`를 반환하며, 근거 없는 요구사항이나 미해결 충돌은 `Blocked` 또는 `Unverifiable`로 구분하세요. receipt에는 경로, 상태, 티켓 수, source ID별 traceability, 의존성, `증거`, `미검증`, 미해결 분할 문제를 포함하세요.

### 🔴 HARD GATE · source UI writing

사용자가 제공한 source 또는 Ready spec에 UI writing이 있으면 분할 전에 별도 inventory로 고정하세요. Label, button name, heading, guide/help copy, table·column name, placeholder, validation/error, status text마다 source 위치·기존 R/AC ID와 이를 소유할 ticket을 연결하고 원문을 exact literal로 기록하세요.

사용자가 해당 문구 변경을 명시적으로 결정하지 않은 한 spelling, 대소문자, 띄어쓰기, 문장부호, 기호, 숫자, 의미 있는 줄바꿈을 그대로 유지하세요. 티켓 작성 과정에서 번역, 의역, 축약, 교정, typo 수정, normalization하지 마세요. 이미지·스크린샷의 literal을 정확히 판독할 수 없거나 source끼리 문구가 충돌하면 추정하지 말고 `Blocked` 또는 `Unverifiable`로 멈추세요.

write 후 inventory의 모든 UI literal이 coverage와 실제 ticket의 인수 기준·검증에 exact하게 남았는지 다시 대조하세요. 승인되지 않은 drift 또는 대조 evidence 부재가 하나라도 있으면 완료로 보고하거나 구현에 넘기지 마세요. 명시적으로 승인된 문구 변경만 `authorized change`로 표시하고 나머지는 frozen 상태를 유지하세요.

하나의 버그는 reproduction부터 root-cause fix, regression seam, original reproduction 재실행과 cleanup까지 하나의 독립 수직 slice로 유지하세요. UI/API/test 같은 층별 티켓이나 진단/수정/검증의 수평 티켓으로 쪼개지 마세요. Ready spec을 source로 받았다면 R/AC ID를 모두 coverage에 연결하고, spec이 `Draft | Blocked | Unverifiable`이면 쓰지 마세요.

## CHECKPOINT / STOP

티켓 파일에 쓰기 전 독립 분할 근거, source traceability, 미해결 충돌, UI writing inventory를 확인하세요. 근거가 부족하거나 UI literal을 exact 대조할 수 없으면 티켓을 만들거나 덮어쓰지 말고 `Unresolved split report`, `Blocked` 또는 `Unverifiable`로 멈추세요.

## DO NOT / ANTI-PATTERNS

- type/API/UI/test-only 수평 티켓이나 근거 없는 성능 수치를 만들지 마세요.
- 제공된 source의 UI writing을 승인 없이 번역·의역·교정·normalization하거나 exact 대조 없이 구현-ready 티켓으로 만들지 마세요.
- 미해결 요구사항·충돌을 사실처럼 티켓에 고정하거나 독립성 없는 작업을 억지로 나누지 마세요.
- 명세 작성, 구현, 원격 게시, 미확인 source를 통한 traceability를 이 스킬에서 수행하지 마세요.
