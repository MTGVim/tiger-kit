---
description: 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 repo-local handoff를 만듭니다.
argument-hint: '"<goal or scope>" [--output <repo-local path>] [--print-only]'
---

이 문서는 TigerKit `/tk:handoff` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:handoff`는 다음 세션이나 다른 에이전트가 바로 이어서 실행할 수 있는 handoff artifact를 만드는 surface입니다.

canonical skill:

```text
skills/handoff/SKILL.md
```

## Core boundary

- 기본은 repo-local write
- 대화 전문 복붙 금지
- 이미 있는 PRD/ADR/issue/diff는 경로/링크 참조 우선
- unverifed success를 handoff에 넣지 않음

## Required sections

아래 항목은 빠지면 안 됩니다.

- Goal
- Current state
- Decisions made
- Changed files
- Commands run
- Verification status
- Remaining tasks
- Open questions
- Risks
- Suggested next skills/commands
- Do-not-repeat context

## Default write target

```text
<git-root>/.claude/tigerkit/worktrees/<worktree-key>/handoffs/current.md
```

## Output contract

```text
Handoff 완료 | Handoff 미리보기 | Handoff 중단
Goal:
- <one-line goal>
Output:
- <path or NONE>
Includes:
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context
Verification:
- <verified / partially verified / unverified>
Next step:
- <what the next agent should do first>
```

## Non-goals

- chat log dump
- vague diary text
- 이미 artifact에 있는 내용을 장문 복붙
