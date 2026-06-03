---
description: 다음 세션 또는 다른 작업자가 이어받을 수 있도록 .claude/handoffs/current.md handoff 문서를 작성합니다.
argument-hint: "[task title] [archive=true]"
---

이 명령은 기존 TigerKit continuation command이며 v7.1에서도 active command로 유지합니다.

사용자에게는 한글로 답합니다. 코드, 파일 경로, URL, ticket, commit, hash, identifier, error는 원문 그대로 유지할 수 있습니다.

목표: `/tk:handoff`는 다음 세션이나 다른 작업자가 안전하게 이어받을 수 있도록 구조화된 handoff 문서를 작성합니다.

```text
handoff = continuation context + reader guide + next safe actions
```

## 기본 산출물

- 기본 위치: `.claude/handoffs/current.md`
- `archive=true` 또는 사용자의 명시 archive 요청이 있으면 dated copy도 함께 생성합니다.
  - 예: `.claude/handoffs/2026-06-03-tigerkit-v7-gap.md`

`archive=true` 또는 사용자의 명시 요청이 없으면 dated archive를 만들지 않습니다.

## v7.2 branch-local context

최신 branch-local TigerKit artifact가 관측되면 handoff에 참조할 수 있습니다.

- 최신 Spec Patch: `.claude/tigerkit/branches/<branch-key>/specs/SP-*.md`
- 최신 Gap Run: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md`
- branch state: `.claude/tigerkit/branches/<branch-key>/branch-state.json`

handoff는 branch-local artifact 자체를 durable rule로 승격하지 않습니다. 다음 작업자가 읽을 continuation 요약만 작성합니다.

## 읽는 방식

별도 `handoff-read` 명령은 없습니다. 이어받는 사람이 지켜야 할 reader guide는 handoff 문서 내부에 포함합니다.

`/tk:handoff`는 write command입니다. 기존 handoff를 읽어 이어받고 싶다면 아래 재개 프롬프트를 사용합니다.

```text
.claude/handoffs/current.md 읽고 Next Actions부터 이어가.
```

## 작성 절차

1. task title을 인자에서 확인합니다. 없으면 현재 작업을 가장 짧게 설명하는 제목을 사용합니다.
2. `.claude/handoffs/` 디렉터리가 없으면 생성합니다.
3. 현재 대화, 현재 repo 상태, 직접 확인한 파일, 사용자 결정, 검증 결과를 근거별로 분리합니다.
4. 최신 branch-local Spec Patch와 Gap Run이 있으면 Relevant Files 또는 Validation에 경로와 상태를 기록합니다.
5. `.claude/handoffs/current.md`를 아래 template으로 작성합니다.
6. `archive=true` 또는 사용자 명시 요청이 있으면 같은 내용을 dated copy로도 작성합니다.
7. 출력에는 작성 위치, archive 생성 여부, 핵심 next action만 보고합니다.

## handoff template

아래 섹션 제목을 정확히 유지합니다.

```md
# Handoff: <task title>

## Reader Guide

- 현재 branch와 HEAD를 확인한 뒤 편집하세요.
- 파일 경로와 가정을 확인한 뒤 편집하세요.
- 파일 변경 전 현재 `CLAUDE.md`와 관련 `.claude/rules/**/*.md`를 읽으세요.
- branch-local TigerKit artifact가 있으면 최신 `branch-state.json`과 report path를 먼저 확인하세요.
- 아래 `Failed Attempts / Do Not Repeat`에 적힌 실패 시도를 반복하지 마세요.
- 사용자가 더 최신 지시를 주지 않았다면 `Next Actions`부터 이어가세요.
- handoff 내용이 현재 코드와 충돌하면 현재 코드를 신뢰하고 충돌을 보고하세요.
- handoff 작성 이후 repo rules 또는 `CLAUDE.md`가 바뀌었다면 더 최신 규칙을 적용하세요.

## Mission

## Current State

## Key Decisions

## Relevant Files

## Basis / References

## Completed Work

## Pending Work

## Known Risks / Unknowns

## Failed Attempts / Do Not Repeat

## Validation

## Next Actions

## Resume Prompt
```

## classification rule

항상 아래 분류를 구분합니다.

```text
Fact = directly observed
Decision = confirmed by user or source contract
Interpretation = inferred from fact
Unknown = not verified
Risk = possible failure mode
```

- 직접 확인한 사항만 `Fact`로 기록합니다.
- 사용자 또는 source contract가 확정한 사항만 `Decision`으로 기록합니다.
- 관찰한 사실에서 추론한 내용은 `Interpretation`으로 기록합니다.
- 확인하지 못한 내용은 `Unknown`으로 둡니다.
- 가능한 실패 모드나 주의점은 `Risk`로 기록합니다.

## 금지

- handoff를 generic task queue로 바꾸기
- 검증되지 않은 가정을 decision처럼 쓰기
- branch-local artifact를 durable rule로 승격하기
- `archive=true` 또는 사용자의 명시 요청 없이 dated archive 만들기

## 출력

```text
handoff 작성했습니다.
- 기록: `.claude/handoffs/current.md`
- archive: 없음
- next action: `.claude/handoffs/current.md` 읽고 Next Actions부터 이어가.
```

`archive=true`가 사용된 경우:

```text
handoff 작성했습니다.
- 기록: `.claude/handoffs/current.md`
- archive: `.claude/handoffs/YYYY-MM-DD-task-name.md`
- next action: `.claude/handoffs/current.md` 읽고 Next Actions부터 이어가.
```
