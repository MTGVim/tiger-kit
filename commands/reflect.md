---
description: branch-local TigerKit working memory에서 repo에 영구 보존할 insight만 추출하고 apply=true일 때 CLAUDE.md 또는 .claude/rules/*에 직접 반영합니다.
argument-hint: "[scope] [--dry-run] [--apply=true|false] [--target <CLAUDE.md|.claude/rules/...>]"
---

이 명령은 TigerKit v7.1 reflect contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 branch-local Spec Patch와 Gap Run에서 repo-wide 가치가 있는 durable insight만 추출해 적절한 durable surface에 직접 반영합니다.

```text
reflect = branch-local working memory -> CLAUDE.md/.claude/rules durable reflection
```

## Command surface

- plugin slash invocation은 `/tk:reflect`입니다.
- `tiger-kit reflect` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.

## 핵심 원칙

- spec/gap/verify 산출물 자체는 repo-wide durable knowledge가 아닙니다.
- repo에 영구적으로 남길 insight는 reflect를 통해서만 추출합니다.
- `/tk:reflect` 기본 동작은 `apply=true`입니다.
- source code는 수정하지 않습니다.
- apply mode의 content write는 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에만 적용합니다.
- branch recency bookkeeping으로 `global-index.json`의 `lastUsedAt`은 갱신할 수 있습니다.
- 같은 insight를 중복 반영하지 않습니다.
- 적용 결과 diff/summary를 출력합니다.

## Apply behavior

| Command | 동작 |
| --- | --- |
| `/tk:reflect` | `apply=true` |
| `/tk:reflect --apply=true` | 기본값과 동일 |
| `/tk:reflect --dry-run` | `apply=false` |
| `/tk:reflect --apply=false` | dry-run alias |

v7.1에서는 `--apply=true`가 redundant여도 warning을 내지 않습니다.

## Inputs

Reflect는 current branch scope의 branch-local working memory를 읽습니다.

```text
.claude/tigerkit/branches/<branch-key>/specs/
.claude/tigerkit/branches/<branch-key>/runs/gap/
.claude/tigerkit/branches/<branch-key>/branch-state.json
```

읽을 수 있는 evidence class:

- active/superseded Spec Patch metadata와 confirmed item
- accepted gap finding pattern
- rejected/downgraded observation reason
- source conflict와 resolution 상태
- current code/worktree context needed to classify repo-wide value

## Durable target classification

각 insight candidate는 아래 중 하나로 분류합니다.

| Target | 사용 조건 |
| --- | --- |
| `CLAUDE.md` | 저장소 전반에 항상 적용돼야 하는 상위 작업 규칙, evidence rule, approval gate, language/output 규칙일 때 |
| `.claude/rules/**/*.md` | 특정 review/workflow/domain/path에만 적용되는 scoped rule일 때 |
| `no action` | one-off, duplicate, unresolved, low-confidence, superseded일 때 |

기본 apply는 위 target에 직접 적용합니다. `--target`이 있으면 명시 target을 우선 사용하되 `CLAUDE.md` 또는 `.claude/rules/**/*.md`만 허용합니다. proposal-only preview는 dry-run에서 출력합니다.

## Durable insight 후보

reflect는 아래만 durable insight 후보로 삼습니다.

- 반복적으로 등장한 accepted finding pattern
- branch에서 확정된 product/design decision 중 repo-wide 가치가 있는 것
- design-system 또는 component convention으로 승격할 만한 내용
- source conflict에서 확정된 resolution
- 사용자 대화에 명시적으로 확인된 TigerKit 운영 규칙

reflect는 아래를 durable insight로 만들지 않습니다.

- branch-specific one-off decision
- 임시 Spec Patch 자체
- superseded된 결정
- P3/nit
- rejected finding
- low-confidence observation
- source conflict가 unresolved인 내용
- implementation detail that only applies to this branch

## Dedupe

동일 insight를 중복 반영하지 않습니다.

Dedupe key는 아래를 조합합니다.

```text
normalized insight title + target file + source evidence class
```

이미 target에 같은 insight가 있으면 `중복으로 건너뜀`으로 집계합니다.

## Output

기본 출력:

```text
Reflect 완료
Apply: true
적용 대상:
- CLAUDE.md
- .claude/rules/<path>.md

적용 결과:
- <added> added
- <updated> updated
- <skipped> skipped as duplicate

요약:
- <한글 insight summary>
```

`--dry-run` 또는 `--apply=false`일 때:

```text
Reflect 완료
Apply: false
예상 대상:
- CLAUDE.md
- .claude/rules/<path>.md

미리보기 결과:
- <added> would add
- <updated> would update
- <skipped> skipped as duplicate

요약:
- <한글 preview summary>
```

## Procedure

1. current worktree root 계산
2. current branch-key 계산
3. branch scope 초기화
4. branch lock 획득
5. apply mode 계산: `apply = dryRun ? false : apply !== false`
6. branch-local memory 로드
7. durable insight 후보 추출
8. 각 후보를 `CLAUDE.md`, `.claude/rules/**/*.md`, `no action`으로 분류
9. one-off, superseded, P3/nit, rejected, low-confidence 후보 제거
10. duplicate 제거
11. apply=true이면 target rule file 또는 `CLAUDE.md`를 직접 수정하고 `global-index.json`에 branch `lastUsedAt` 갱신
12. apply=false이면 preview만 출력하고 저장 없이 종료
13. branch lock 해제
14. summary 출력

## Conflict handling

충돌 또는 unresolved source conflict가 있으면 해당 candidate는 적용하지 않습니다. summary에 skipped reason을 적습니다.

## 금지

- source code 수정
- `.claude/tigerkit/` 아래 durable insight 저장
- branch-local Spec Patch 내용을 repo-wide rule처럼 그대로 복사
- P3/nit, rejected finding, low-confidence observation 반영
- unresolved source conflict를 확정 insight처럼 반영
- duplicate insight 중복 append
- `apply=true`인데도 별도 `tigerkit-reflections.md` sidecar를 만드는 것
