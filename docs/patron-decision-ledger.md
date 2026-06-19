# Patron Decision Ledger

Patron decision ledger는 AFK에서 Patron이 호출된 경우 남기는 structured decision record다.

## Purpose

- Driver가 왜 decision을 위임했는지 보존한다.
- Reflect가 reusable learning을 추출할 수 있게 한다.
- 내부 사고 전문 대신 결정, 근거 요약, confidence, follow-up만 남긴다.

## Location

```text
.claude/tigerkit/branches/<scope-key>/afk/decisions/DEC-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<scope-key>/afk/decisions/current.md
```

## Schema

```yaml
decision:
  topic: <topic>
trigger:
  - <delegation reason>
patron:
  id: <id>
  source: source-derived | tigerkit-native
  mode: primary | fanout
  temporary: true
context:
  constraints:
    - <constraint>
  evidence:
    - <evidence ref>
options:
  - id: A
    summary: <option summary>
decision_result: <selected option or blocked>
rationale:
  - <reason summary>
confidence: low | medium | high
follow_up:
  - <next action>
```

## Do not record

- Patron 내부 사고 전문
- secrets
- user private details unrelated to work
- raw session transcript
- unredacted external credentials or tokens
