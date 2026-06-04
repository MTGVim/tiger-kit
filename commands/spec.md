---
description: 현재 세션의 지시·결정·회의 메모를 branch-local Spec Patch로 저장합니다.
argument-hint: "<instruction?> [--status active|draft] [--title <title>] [--origin <origin>] [--supersedes <item-id>] [--out <path>] [--no-index] [--print-body]"
---

이 명령은 TigerKit v7.1 branch-scoped Spec Patch contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:spec`은 raw instruction을 현재 브랜치 전용 Product/Design Spec Patch로 정규화해 gap 분석 source로 저장합니다.

```text
spec = branch-local requirement patch creation
```

## Command surface

- plugin slash invocation은 `/tk:spec`입니다.
- 자연어로 “방금 결정된 요구사항을 gap 기준으로 저장해줘”처럼 요청해도 같은 contract를 따릅니다.
- `tiger-kit spec` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.

## 기본 저장 위치

반드시 current worktree root 아래에 저장합니다.

```text
.claude/tigerkit/branches/<branch-key>/specs/
```

금지 저장 위치:

- `$GIT_COMMON_DIR/.claude/tigerkit`
- `.git/worktrees/*`
- user home global path
- `/tmp`
- current worktree root 밖 경로

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

## Branch key

브랜치명을 디렉터리명으로 직접 쓰지 않습니다.

Normal branch:

1. `worktreeRoot = git rev-parse --show-toplevel`
2. `branchName = git symbolic-ref --quiet --short HEAD`
3. `fullRefName = refs/heads/<branchName>`
4. branch slug는 `/`, `\`, 공백, `:`, `*`, `?`, `"`, `<`, `>`, `|`를 `-`로 바꾸고 연속 `-`를 하나로 줄입니다.
5. 앞뒤 `-`를 제거하고 빈 값이면 `unknown`을 씁니다.
6. `shortHash = sha256(fullRefName).slice(0, 6)`
7. `branchKey = <branch-slug>--<shortHash>`

Detached HEAD:

```text
branchKey = detached-<shortHeadSha7>--<sha256(worktreeRoot).slice(0, 6)>
```

Detached 상태면 summary에 branch scope가 detached임을 알립니다.

## ID formats

Timestamp는 local timezone 기준 `YYYYMMDD-HHmmss`입니다. Random suffix는 crypto random 2 bytes를 uppercase hex 4자리로 씁니다.

- Spec Patch ID: `SP-YYYYMMDD-HHmmss-RAND`
- Product Spec Item: `P-SP-YYYYMMDD-HHmmss-RAND-NN`
- Design Spec Item: `D-SP-YYYYMMDD-HHmmss-RAND-NN`
- Design System Spec Item: `DS-SP-YYYYMMDD-HHmmss-RAND-NN`
- Engineering Constraint: `E-SP-YYYYMMDD-HHmmss-RAND-NN`
- QA Acceptance Criteria: `QA-SP-YYYYMMDD-HHmmss-RAND-NN`
- Analytics Contract: `A-SP-YYYYMMDD-HHmmss-RAND-NN`

## Input

입력 source는 인자 또는 stdin에서 수집합니다.

허용 origin:

- `ad_hoc_instruction`
- `brainstorming_note`
- `meeting_note`
- `chat_decision`
- `reviewer_comment`
- `pm_decision`
- `qa_feedback`
- `design_feedback`

기본 origin은 `ad_hoc_instruction`입니다.

## Spec Patch status

허용 값:

- `active`: current branch gap 분석 기본 참조 대상
- `draft`: 아직 확정되지 않음
- `superseded`: 다른 Spec Patch가 대체함
- `archived`: 과거 기록
- `conflict`: 기존 source와 충돌

기본값은 `active`입니다.

## Spec Item status

허용 값:

- `confirmed`: final finding evidence로 사용 가능
- `draft`: 초안, final finding evidence로 사용 금지
- `assumed`: 추정, final finding evidence로 사용 금지
- `unclear`: 불명확, final finding evidence로 사용 금지
- `conflict`: source conflict 존재, final finding evidence로 사용 금지
- `superseded`: 대체됨, final finding evidence로 사용 금지

확정성 판정:

- `방금 정해졌는데`, `결정됐는데`, `최종적으로`, `PM이 confirmed`, `디자인에서 확정`, `해야 된대`, `must`, `should be changed to`는 confirmed 후보입니다.
- `아마`, `같음`, `나을 듯`, `고민 중`, `어떨까`, `maybe`, `probably`, `could`, `might`는 draft 또는 assumed로 둡니다.
- `적당히`, `예쁘게`, `자연스럽게`, `알아서`, `비슷하게`는 unclear로 둡니다.
- `기존처럼`은 기존 source가 명확하게 제공될 때만 confirmed가 될 수 있습니다.

## Spec Patch Markdown template

생성 파일은 아래 섹션을 반드시 포함합니다.

```md
# Spec Patch: <SPEC_PATCH_ID>

## Metadata

- Title: <title>
- Origin: <origin>
- Status: <status>
- Branch Key: <branch-key>
- Created At: <iso-local-time>
- Updated At: <iso-local-time>
- Source Text: <raw input text>

## Supersedes

- None

## Product Spec Items

- None

## Design Spec Items

- None

## Design System Spec Items

- None

## Engineering Constraints

- None

## QA Acceptance Criteria

- None

## Analytics Contracts

- None

## Clarification Needed

- None
```

각 item은 아래 필드를 사용합니다.

```md
### <ITEM_ID>

Type: <type>
Status: <status>
Expected: <expected result>
Verification: <verification method>
Severity Hint: <P0|P1|P2|P3>
Notes: <notes>
```

## Supersede policy

기존 요건이 바뀌면 기존 파일을 조용히 수정하지 않습니다.

- 새 Spec Patch를 만듭니다.
- `## Supersedes`에 기존 item ID를 기록합니다.
- `specs/index.json`의 `itemSupersedes`에 `oldItemId -> newItemId`를 기록합니다.
- 기존 Spec Patch 전체를 자동 superseded로 바꾸지 않습니다.
- `/tk:gap`은 superseded item을 무시합니다.

## Index files

기본적으로 아래 파일을 atomic write로 갱신합니다.

```text
.claude/tigerkit/branches/<branch-key>/specs/index.json
.claude/tigerkit/branches/<branch-key>/branch-state.json
.claude/tigerkit/global-index.json
```

`branch-state.json`에는 `lastSpecPatchId`를 기록합니다. `global-index.json`에는 branch `lastUsedAt`을 갱신합니다.

`--no-index`가 있으면 Spec Patch 파일만 만들고 index와 branch-state 갱신은 생략합니다. 이 경우 summary에 index 미등록을 명시합니다.

## Lock and write safety

branch scope 작업 전 `.claude/tigerkit/branches/<branch-key>/.lock`을 exclusive create로 획득합니다.

- lock 내용에는 `pid`, `command`, `createdAt`을 기록합니다.
- 30분 미만 lock이 있으면 중단합니다.
- 30분 이상 lock은 stale warning 후 제거할 수 있습니다.
- `TIGERKIT_FORCE_LOCK=1`이면 즉시 override할 수 있습니다.

Atomic write 대상:

- `specs/index.json`
- `branch-state.json`
- `global-index.json`

절차:

1. `target.tmp.<pid>.<rand>`에 씁니다.
2. 가능하면 fsync합니다.
3. rename으로 target을 교체합니다.
4. 실패 시 tmp 파일을 삭제합니다.

## Path safety

`--out` 경로는 normalize 후 current worktree root 내부이면서 `.claude/tigerkit/branches/<branch-key>/specs/` 아래여야 합니다. `--no-index`가 있어도 branch-local specs directory 밖으로 쓰지 않습니다. worktree root 밖이거나 branch-local specs directory 밖이면 중단하고 아래 메시지를 사용합니다.

```text
Tiger Kit does not read or write files outside the current worktree by default.
```

## 금지

- 구현 분석
- current code 평가
- gap finding 생성
- final severity 확정
- implementation fix 제안
- source conflict 임의 해결
- Spec Patch 전체 본문을 기본 stdout으로 출력

## 출력

기본 stdout은 summary만 출력합니다.

```text
Spec Patch 생성: <SP-ID>
Branch Scope: <branch-key>
경로: .claude/tigerkit/branches/<branch-key>/specs/<SP-ID>-<slug>.md
Items:
- <ITEM-ID>
```

`--print-body`가 있을 때만 Spec Patch 본문도 함께 출력합니다.
