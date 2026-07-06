---
name: handoff
description: 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다.
---

# Handoff

세션 기록을 늘어놓는 대신, 다음 실행자가 바로 이어서 움직일 수 있는 handoff를 만드는 skill입니다.

## Goal

- 다음 사람이나 다음 세션이 맥락 복구에 시간을 쓰지 않게 합니다.
- 이미 있는 artifact는 복붙 대신 경로로 참조합니다.
- 남은 작업과 리스크를 실행 가능한 형태로 남깁니다.

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

## Process

1. 현재 작업 목표를 한 문장으로 고정합니다.
2. 현재 branch/state/핵심 파일을 적습니다.
3. 뒤집히면 안 되는 결정을 분리해서 적습니다.
4. 실제로 바뀐 파일과 실행한 명령만 적습니다.
5. 검증 완료/미완료를 숨기지 않고 분리합니다.
6. 남은 작업은 다음 실행자가 바로 시작할 순서로 적습니다.
7. 이미 있는 PRD/ADR/issue/diff는 경로 또는 링크로 참조합니다.

## Default artifact target

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py` helper가 계산합니다.

## Boundaries

- repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first write 기본
- 대화 전문 복붙 금지
- 감상문 금지
- 이미 문서화된 내용을 중복 장문 서술 금지
- unverifed success를 handoff에 넣지 않음

## Good use cases

- 세션 마감 전 상태 인계
- 다른 agent로 작업 넘길 때
- 긴 구현 작업 중간 checkpoint
- 실패/보류 상태를 정확히 넘겨야 할 때
