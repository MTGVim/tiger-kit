---
description: merge 또는 rebase conflict를 ours/theirs 의도 기준으로 해결합니다.
argument-hint: '[--target <file|path>] [--print-plan]'
---

이 문서는 TigerKit `/tk:merge-conflict` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:merge-conflict`는 merge/rebase conflict를 단순 ours/theirs 선택이 아니라 양쪽 intent 기준으로 정리하는 surface입니다.

canonical skill:

```text
skills/merge-conflict/SKILL.md
```

## Core boundary

- 현재 merge/rebase 상태 확인 필수
- 충돌 파일과 hunk 목록화 필수
- ours/theirs 의도 추적 필수
- 가능한 검증 명령 실행 필수
- `git reset --hard` 금지
- `git clean` 금지
- force push 금지
- 의도 확인 없는 대규모 삭제 금지

## Output contract

```text
Merge conflict 분석 | Merge conflict 해결 | Merge conflict 중단
State:
- <merge|rebase|none>
Conflict files:
- <file list or NONE>
Hunks:
- <summary>
Resolution:
- <how each intent was reconciled>
Verification:
- <commands run and result or NONE>
Next step:
- <continue merge/rebase | manual follow-up>
```

## Non-goals

- unrelated refactor
- formatting-only churn
- conflict 상태를 숨기고 success 선언
