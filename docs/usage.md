# Usage

## 1. Gap analysis

Run with source material or a source extraction instruction:

```text
/tigap:gap <source references or extraction instruction>
```

Examples:

```text
/tigap:gap GitHub issues를 가져와서 분석해.
/tigap:gap docs/spec.md와 현재 구현을 비교해.
/tigap:gap 인터뷰 방식으로 요구사항부터 정리해.
```

If no source is provided, the command should stop before analysis and ask for one of these paths:

- provide source references directly
- ask Claude to fetch or extract sources
- start an interview to collect requirements

Valid source references include:

- issue tracker ticket
- knowledge-base page
- PRD
- design document
- user-written brief
- screenshot
- code path
- existing implementation reference

The skill should produce:

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

## 2. Planning

Run:

```text
/tigap:gaplan
```

The skill reads the gap report, then creates:

```text
.gap/{branch_name}/plan/implementation-plan.md
.gap/{branch_name}/tasks.md
```

It should bias toward plan-mode style behavior: inspect, reason, split, then defer implementation until the task list is clear.

## 3. Execution

Run:

```text
/tigap:go
```

The skill reads `tasks.md`, picks the next small task, inspects relevant code, implements narrowly, validates, then updates the task status.

## Suggested command language

```text
/tigap:gap 이 브랜치 기준으로 source of truth 요청부터 시작해.
/tigap:gaplan 갭 분석 결과를 바탕으로 plan mode처럼 구현계획 짜줘.
/tigap:go tasks.md 기준으로 다음 task 하나만 진행해.
```
