---
name: tk-to-tickets
description: "[user] 요청이나 명세를 독립적으로 검증 가능한 수직 티켓으로 나눕니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<명세, 계획 또는 요청> [--output <경로>]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# 티켓 작성

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 대화, `.tigerkit/spec.md`, 요청, 관련 코드 순입니다.

## Workflow

1. `source 요구사항 추출`: 입력은 우선순위가 정해진 소스이고, 출력은 요구사항별 원문 위치와 `confirmed | unverified | conflict` 상태입니다.
2. `vertical slice`: 입력은 확인된 요구사항이고, 출력은 독립 목표·범위·동작·테스트를 함께 가진 티켓 후보입니다.
3. `인수 기준·검증`: 입력은 티켓 후보이고, 출력은 관찰 가능한 인수 기준과 실행할 검증 명령 또는 증거입니다.
4. `traceability·의존성`: 입력은 티켓과 source map이고, 출력은 요구사항 연결, 선행 티켓, 미해결 분할 문제입니다.
5. `checkpoint`: 입력은 분할 근거·traceability·충돌 목록이고, 출력은 쓰기 가능 여부 또는 `Unresolved split report | Blocked | Unverifiable`입니다.
6. `write/report receipt`: 입력은 checkpoint를 통과한 티켓과 경로이고, 출력은 작성된 경로 또는 report-only receipt입니다.

사용자가 지정한 경로 또는 `.tigerkit/tickets.md`에 `# <Feature> Tickets` 형식으로 작성하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 타임스탬프 아카이브를 생성하거나 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 경고하세요. 구현하거나 원격 트래커에 게시하지 마세요.

## 계약

요구사항별 source traceability를 남기고 각 티켓을 독립적인 목표, 범위, 인수 기준, 검증을 가진 수직 동작 단위로 구성하세요. 동작의 테스트는 해당 티켓에 포함하며 수평적인 type/API/UI/test-only 티켓을 만들지 마세요. 독립된 동작으로 분할할 근거가 부족하면 억지로 만들지 말고 `Unresolved split report`를 반환하며, 근거 없는 요구사항이나 미해결 충돌은 `Blocked` 또는 `Unverifiable`로 구분하세요. receipt에는 경로, 상태, 티켓 수, 요구사항별 traceability, 의존성, `증거`, `미검증`, 미해결 분할 문제를 포함하세요.

## Failure paths

- If 필수 source를 읽을 수 없으면 traceability를 채우지 말고 `Unverifiable`로 종료합니다.
- If 요구사항이 미확정이거나 충돌하면 티켓에 고정하지 말고 `Blocked`로 종료합니다.
- If 독립 vertical slice 근거가 부족하면 수평 티켓을 만들지 말고 `Unresolved split report`를 반환합니다.
- If type/API/UI/test-only 분할만 남으면 동작 단위로 억지로 나누지 말고 `Unresolved split report`를 반환합니다.
- If write 또는 후속 검증이 실패하면 `applied`로 보고하지 말고 `Fail`과 경로·미검증 항목을 보고합니다.

## CHECKPOINT / STOP

티켓 파일에 쓰기 전 독립 분할 근거, source traceability, 미해결 충돌을 확인하세요. 근거가 부족하면 티켓을 만들거나 덮어쓰지 말고 `Unresolved split report`, `Blocked` 또는 `Unverifiable`로 멈추세요.

## DO NOT / ANTI-PATTERNS

- type/API/UI/test-only 수평 티켓이나 근거 없는 성능 수치를 만들지 마세요.
- 미해결 요구사항·충돌을 사실처럼 티켓에 고정하거나 독립성 없는 작업을 억지로 나누지 마세요.
- 구현, 원격 게시, 미확인 source를 통한 traceability를 이 스킬에서 수행하지 마세요.
