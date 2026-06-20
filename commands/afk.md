---
description: 현재 세션의 불확실한 의사결정을 temporary Patron에게 위임합니다.
argument-hint: "[decision topic or context] [--patron <id>] [--preset <name>] [--ledger <path>]"
---

이 명령은 TigerKit Slim `/tk:afk` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:afk`는 background async 작업이 아니라, 현재 세션에서 Driver가 계속 작업하는 동안 중대하거나 불확실한 decision point를 temporary Patron에게 위임하는 모드입니다.

```text
afk = driver keeps working + temporary Patron decides scoped decision point + decision ledger records outcome
```

## Default

- 설치 직후 AFK default는 off입니다.
- `/tk:afk` 명시 호출 시에만 켜집니다.
- `/tk:setup afk default on|off|status`가 default 상태를 관리합니다.
- config state가 source of truth입니다. user `CLAUDE.md` bridge는 activation aid입니다.
- 명시적 사용자 지시가 AFK default보다 항상 우선합니다.

## Driver policy

- 명확한 결정은 Driver가 직접 처리합니다.
- 중대하거나 불확실한 결정은 Patron에게 위임합니다.
- Patron 호출은 decision point 단위이며 temporary입니다.
- Patron은 판단 후 사라집니다.
- Patron output은 Driver가 merge합니다.
- Patron끼리 토론하지 않습니다.
- Patron은 다른 Patron을 호출하지 않습니다.
- 기본은 decision point당 primary Patron 하나입니다.
- fan-out은 독립 risk axes가 명확할 때만 허용합니다.

## Patron selection

| Decision type | Patron |
|---|---|
| repo convention / reuse | steward |
| code quality / merge readiness | reviewer |
| verification / test scope | tester |
| security boundary / permissions | security |
| web runtime performance | webperf |
| simplification / scope reduction | simplifier |
| visual explanation / structure map | cartographer |

## Guardrails

아래는 사용자 승인 없이는 수행하지 않습니다.

- deploy
- delete
- cost-incurring action
- permission change
- secrets change
- destructive or hard-to-revert action
- repo shared `CLAUDE.md` direct edit

Security Patron이 Critical/High risk를 판단하면 사용자 승인 gate로 되돌립니다.

## Decision ledger

Patron이 호출되면 structured ledger를 남깁니다. 기본 위치는 branch/workspace-local working memory입니다.

```text
.claude/tigerkit/branches/<scope-key>/afk/decisions/DEC-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<scope-key>/afk/decisions/current.md
```

Ledger 최소 schema:

```yaml
decision:
  topic: <decision topic>
trigger:
  - <why delegated>
patron:
  id: <patron id>
  source: <source-derived|tigerkit-native>
  mode: primary | fanout
  temporary: true
context:
  constraints:
    - <constraint>
  evidence:
    - <evidence ref>
options:
  - id: A
    summary: <option>
decision_result: <selected option or blocked>
rationale:
  - <reason>
confidence: low | medium | high
follow_up:
  - <next step>
```

Ledger는 내부 사고 전문이 아니라 reflect가 재사용 가능한 decision record여야 합니다.

## Output

```text
AFK 결정 위임 완료: <DEC-ID>
Patron: <id>
결정: <selected|blocked>
근거: <한글 1-3줄>
Ledger: .claude/tigerkit/branches/<scope-key>/afk/decisions/<DEC-ID>.md
다음 행동: <driver next step>
```

시각화가 유용하면 flowchart, layer map, before/after 구조를 포함할 수 있습니다.
