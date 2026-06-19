# Patron Lifecycle

Patron은 session worker가 아니라 temporary decision policy다.

## Lifecycle

1. Driver가 decision point를 식별한다.
2. Decision type으로 Patron을 고른다.
3. 필요한 context, constraints, evidence만 전달한다.
4. Patron이 scoped decision을 낸다.
5. Driver가 결과를 merge한다.
6. Decision ledger를 기록한다.
7. Patron은 사라진다.

## Selection rule

Patron 선택은 phase가 아니라 question type 기준이다.

| Question type | Patron |
|---|---|
| repo convention / reuse | steward |
| code quality / merge readiness | reviewer |
| verification / test scope | tester |
| security boundary / permissions | security |
| web runtime performance | webperf |
| simplification / scope reduction | simplifier |
| visual explanation / structure map | cartographer |

## Fan-out rule

기본은 decision point당 primary Patron 하나다. Fan-out은 독립 risk axes가 명확할 때만 허용한다.

허용 예:

- permission change가 code quality와 security risk를 동시에 가진 경우: reviewer + security
- frontend migration이 performance와 reuse decision을 독립적으로 가진 경우: steward + webperf

금지:

- always-on council
- Patron-to-Patron call
- Patron debate
- 모든 decision에 full preset 호출

## Driver merge

Driver는 Patron output을 그대로 실행하지 않는다. Driver가 아래를 확인한다.

- user instruction과 conflict 여부
- repo rule과 conflict 여부
- irreversible or external side effect 여부
- confidence와 missing evidence
- user approval gate 필요 여부

## Decision ledger

Ledger는 reflect가 재사용 가능한 decision record다. 내부 사고 전문을 저장하지 않는다.

필수 필드:

```yaml
decision:
  topic: <topic>
trigger:
  - <delegation reason>
patron:
  id: <id>
  source: <source>
  mode: primary | fanout
  temporary: true
context:
  constraints:
    - <constraint>
  evidence:
    - <evidence>
options:
  - id: A
    summary: <option>
decision_result: <selected or blocked>
rationale:
  - <reason>
confidence: low | medium | high
follow_up:
  - <next step>
```

## Guardrails

사용자 승인 없이는 아래를 하지 않는다.

- 배포
- 삭제
- 비용 발생
- 권한 변경
- secrets 변경
- 되돌리기 어려운 destructive action
- repo shared `CLAUDE.md` 직접 수정

Security Patron이 Critical/High risk를 판단하면 사용자 승인 gate로 되돌린다.
