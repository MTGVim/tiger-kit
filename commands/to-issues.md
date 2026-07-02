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
<git-root>/.claude/tigerkit/issues/ISSUES-YYYYMMDD-HHmmss.md
```

## Output contract

```text
To-Issues 완료 | To-Issues 미리보기 | To-Issues 중단
Source:
- <plan|prd|scope>
Output:
- <path or NONE>
Issue count:
- <N>
Rules applied:
- vertical slice only
- no layer slicing
- draft-only by default
Dependencies:
- <blocked-by summary or NONE>
Publish:
- disabled by default
Next step:
- <review drafts | revise slicing | publish explicitly>
```

## Non-goals

- publish 기본값
- layer별 ticket 폭증
- 독립 실행 불가능한 issue 쪼개기
