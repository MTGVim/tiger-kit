---
name: tk-ask-repo
description: "[user] 저장소의 동작, 값의 출처, 존재 여부, 영향 범위, 책임 위치를 읽기 전용으로 조사하고 `path:line` 근거와 함께 자연스럽게 설명하며 마지막에 타팀 공유용 요약을 제공합니다."
disable-model-invocation: true
argument-hint: "<저장소 질문>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Answering Repository Questions

Handle only concrete repository questions explicitly invoked through `/tk-ask-repo`, `$tk-ask-repo`, or host skill selection.

This is a read-only investigation that does not modify source, tests, configuration, artifacts, history, or remote state.
It does not own implementation, closing user decisions, runtime estimation, or real-browser reproduction.

## 🔴 CHECKPOINT · 🛑 STOP · Investigation boundary

Do not implement, mutate, or turn incomplete evidence into a repository claim; when an anchor or evidence path cannot be established, stop with `Status: Unverifiable`.

## User Experience

Keep the internal investigation rigorous, but present the result as a natural explanation rather than a report.

- State the answer to the question first.
- Explain the value or behavior flow in an order that is easy to understand.
- Place `path:line` evidence next to each important repository claim.
- Do not show internal classifications, checkpoints, or search ledgers by default.
- Use short prose or a limited list unless a comparison truly requires a table.
- Explain interactively one step at a time only when the user says “하나씩 따라가며 설명해줘”.

## Investigation Principles

Use the question’s visible string, identifier, path, address, or symbol as the first anchor.
If there is no anchor, briefly explain the searches attempted and the information needed, then end with `Status: Unverifiable`.

Every repository-state claim must have one of the following:

- An exact `path:line` or current-state evidence
- An explicit limitation that the evidence cannot be read
- A clear indication that the explanation is an `inference` when judgment is required

A declaration proves only shape.
When asked about a value’s origin, trace the actual assignment, stored input, transformation, and external boundary.

Do not turn `not found` directly into `absent`.
Check the current baseline, relevant in-progress changes, conditional paths, and possible dynamic connections.

For impact questions, investigate related read and write locations and distinguish:

- Consumers that must change
- Consumers that must not change
- Consumers that cannot be determined due to insufficient evidence

When asked about ownership, check consuming-side transformations, permissions, feature conditions, conditional rendering, and environment differences before blaming the producer.

## Representative Traces

### Value Origin

```text
표시 값
→ 바인딩
→ 소비 표현식
→ 전달 필드
→ 타입/스키마
→ 변환
→ 실제 대입 또는 외부 경계
```

### Structure

```text
진입점
→ 화면/호출자
→ 전달 경계
→ 생산자
→ 저장소 또는 외부 시스템
```

### Existence

현재 기준선, 관련 진행 중 변경과 실제 연결 상태를 근거로
`없음 | 아직 반영되지 않음 | 자리만 있음 | 실제 사용 중` 의미를 구분합니다.

### Impact and Ownership

Check all relevant consumers and explain which parts cause the current issue and which parts must be preserved.

## When the Question Is Out of Scope

Do not keep investigating to force an answer for these requests:

- Code implementation or commits
- User decisions about product behavior
- Real-browser reproduction
- Schedule or day-level estimates
- General knowledge unrelated to the repository

When possible, state the appropriate next action in one sentence.
Route general implementation to the current executor without requiring a specific TigerKit skill.
Use `tk-prep` when the work must first be specified, or `tk-browser-verify` when real-browser evidence is required.

## Response Format

Do not begin with a fixed `Answer`, `Evidence`, `Origin` report.
Put the most direct answer to the question in the first paragraph.

Then explain only as much flow, impact, and limitation as needed.
Place important evidence next to the corresponding explanation.

Always end the response with `## 공유용 요약`.

공유용 요약은:

- `3~10`줄
- 본문에서 이미 검증된 사실만 사용
- 새로운 추론이나 새 결론을 만들지 않음
- 코드 내부 상세보다 결론, 영향, 책임 경계 중심
- 타팀, 기획, 백엔드, 리뷰어에게 그대로 전달할 수 있는 자연스러운 문장

조사가 실패한 경우에도 확인된 사실이 있다면 공유 가능한 범위만 요약하고,
확인되지 않은 내용은 확인되지 않았다고 명시합니다.
