---
description: plan이나 PRD를 independently grabbable vertical-slice issue draft로 분해합니다.
argument-hint: '"<plan|prd>" [--output <path>] [--print-only] [--publish]'
---

이 문서는 TigerKit `/tk:to-issues` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:to-issues`는 plan/PRD를 independently grabbable vertical-slice issue draft로 분해하는 surface입니다.

canonical skill:

```text
skills/to-issues/SKILL.md
```

## Core boundary

- default draft-only
- no-publish 기본
- vertical slice only
- no layer slicing
- blocked-by / order dependency 명시

## Default output target

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/issues/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py` helper가 계산합니다.

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
To-Issues 완료 | To-Issues 미리보기 | To-Issues 중단
Source:
- <plan|prd|scope>
Output mode:
- draft file | inline preview
[Output path:
- <path>]
Issue count:
- <N>
Rules applied:
- vertical slice only
- no layer slicing
- draft-only by default
Dependencies:
- <blocked-by summary>
Publish:
- disabled by default
Next step:
- <review drafts | revise slicing | publish explicitly>
```

## Non-goals

- publish 기본값
- layer별 ticket 폭증
- 독립 실행 불가능한 issue 쪼개기
