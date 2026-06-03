---
description: 작업 종료 전 현재 branch-local gap/spec 상태를 검증하고 evidence를 저장합니다.
argument-hint: "[--run-id <VFY-ID>] [--no-save] [--print-report]"
---

이 명령은 TigerKit v7.1 branch-local verification evidence contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:verify-before-stop`은 Stop hook이 자동 확인할 verification evidence를 사용자가 미리 준비하거나 보완하는 수동 command입니다. 작업 종료 전 최신 branch-local Spec Patch와 Gap Run을 기준으로 검증 evidence를 저장합니다.

```text
verify-before-stop command = manual preparation
Stop hook = automatic guard
```

## Command surface

- plugin slash invocation은 `/tk:verify-before-stop`입니다.
- `tiger-kit verify-before-stop` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.
- Stop hook 자체를 대체하지 않습니다. Stop 직전 검증 receipt를 branch-local memory로 남기는 command입니다.

## Branch-local storage

기본 저장 위치:

```text
.claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/
```

필수 파일:

```text
checklist.md
evidence.json
report.md
```

검증 저장 후 아래 파일을 함께 갱신합니다.

```text
.claude/tigerkit/branches/<branch-key>/branch-state.json
.claude/tigerkit/global-index.json
```

`branch-state.json`에는 `lastVerifyRunId`를 기록합니다. `global-index.json`에는 branch `lastUsedAt`을 갱신합니다.

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

금지 저장 위치:

- `$GIT_COMMON_DIR/.claude/tigerkit`
- `.git/worktrees/*`
- user home global path
- `/tmp`
- current worktree root 밖 경로

## ID format

Verify Run ID:

```text
VFY-YYYYMMDD-HHmmss-RAND
```

Timestamp는 local timezone 기준입니다. Random suffix는 crypto random 2 bytes를 uppercase hex 4자리로 씁니다.

## Options

- `--run-id <VFY-ID>`: run ID를 명시합니다.
- `--no-save`: debugging 용도. 파일 저장과 branch-state 갱신을 생략하고 summary만 출력합니다.
- `--print-report`: 저장 또는 생성한 report.md 본문을 stdout에도 출력합니다.

기본은 항상 저장입니다.

## Lock and write safety

저장 모드에서는 branch scope 작업 전 `.claude/tigerkit/branches/<branch-key>/.lock`을 exclusive create로 획득합니다.

- lock 내용에는 `pid`, `command`, `createdAt`을 기록합니다.
- 30분 미만 lock이 있으면 중단합니다.
- 30분 이상 lock은 stale warning 후 제거할 수 있습니다.
- `TIGERKIT_FORCE_LOCK=1`이면 즉시 override할 수 있습니다.

Atomic write 대상:

- `evidence.json`
- `branch-state.json`
- `global-index.json`

`checklist.md`와 `report.md`도 같은 run directory에 완성된 내용으로 쓴 뒤 summary를 출력합니다.

## Default checks

아래 check를 수행합니다.

| ID | Title | 기준 |
| --- | --- | --- |
| CHK-001 | No unresolved P0/P1 gap findings | 최신 gap report에 unresolved P0/P1 accepted finding이 없어야 함 |
| CHK-002 | Source conflicts handled | 최신 gap report의 source_conflict가 해결 또는 명시 보류되어야 함 |
| CHK-003 | Required changes completed | 최신 gap report의 requiredChange가 구현계획 또는 완료 근거로 커버되어야 함 |
| CHK-004 | Active specs reviewed | active/confirmed Spec Patch item이 최신 gap run contracts에 참조되어야 함 |
| CHK-005 | Explicit user requests covered | 현재 세션 또는 작업 요청의 명시 작업이 누락되지 않아야 함 |

Check status 허용 값:

- `passed`
- `failed`
- `skipped`
- `unknown`

## Missing latest gap behavior

최신 gap run이 없으면 CHK-001, CHK-002, CHK-003은 `unknown` 또는 `skipped`로 둡니다.

이 상황은 command 실패가 아닙니다. 전체 status는 `unknown`으로 둡니다.

stdout에는 아래 메시지를 포함합니다.

```text
No gap run found for this branch scope. Verification status is unknown.
```

## evidence.json

형식:

```json
{
  "version": 1,
  "runId": "VFY-YYYYMMDD-HHmmss-RAND",
  "branchKey": "<branch-key>",
  "createdAt": "<iso-local-time>",
  "checks": [
    {
      "id": "CHK-001",
      "title": "No unresolved P0/P1 gap findings",
      "status": "passed",
      "evidence": [
        "Latest gap report <GAP-ID> has no unresolved P0/P1 findings."
      ]
    }
  ],
  "status": "passed|failed|unknown"
}
```

Overall status rule:

- all meaningful checks passed or skipped -> `passed`
- any check failed -> `failed`
- no latest gap or insufficient evidence prevents pass/fail judgment -> `unknown`

## checklist.md

`checklist.md`는 CHK-001부터 CHK-005까지 현재 status와 필요한 evidence를 사람이 읽을 수 있게 기록합니다.

## report.md

형식:

```md
# Tiger Kit Verify Report: <VFY-ID>

## Summary

- Branch: <branch-name>
- Branch Key: <branch-key>
- Status: <passed|failed|unknown>

## Checks

### CHK-001: No unresolved P0/P1 gap findings

Status: <status>

Evidence:
- <evidence>
```

## Output

기본 stdout은 summary만 출력합니다.

```text
Verification 완료: <VFY-ID>
Branch Scope: <branch-key>
상태: <passed|failed|unknown>
Report: .claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/report.md
```

`--no-save`일 때:

```text
Verification 완료: <VFY-ID>
Branch Scope: <branch-key>
상태: <passed|failed|unknown>
Report: not saved (--no-save)
```

`--print-report`가 있을 때만 report.md 본문을 함께 출력합니다.

## 금지

- 최신 gap run이 없다는 이유만으로 failed 처리
- `/tmp`에 verification evidence 저장
- repo-wide durable rule 또는 source code 수정
- default stdout에 전체 report 출력
- 검증되지 않은 항목을 passed로 기록
