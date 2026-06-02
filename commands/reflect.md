---
description: branch-local TigerKit working memory에서 repo에 영구 보존할 insight만 추출하고 기본 apply=true로 durable target에 반영합니다.
argument-hint: "[--dry-run] [--apply=true|false] [--target <path>]"
---

이 명령은 TigerKit v7 reflect contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 branch-local Spec Patch, Gap Run, Verify Run에서 repo-wide 가치가 있는 durable insight만 추출해 durable insight target에 반영합니다.

```text
reflect = branch-local working memory -> durable insight extraction
```

## Command surface

- plugin slash invocation은 `/tk:reflect`입니다.
- `tiger-kit reflect` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.

## 핵심 원칙

- spec/gap/verify 산출물 자체는 repo-wide durable knowledge가 아닙니다.
- repo에 영구적으로 남길 insight는 reflect를 통해서만 추출합니다.
- `/tk:reflect` 기본 동작은 apply=true입니다.
- source code는 수정하지 않습니다.
- apply mode의 content write는 durable insight target만 수정합니다.
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

v7에서는 `--apply=true`가 redundant여도 warning을 내지 않습니다. v2 이후 warning은 별도 검토 대상입니다.

## Inputs

Reflect는 current branch scope의 branch-local working memory를 읽습니다.

```text
.claude/tigerkit/branches/<branch-key>/specs/
.claude/tigerkit/branches/<branch-key>/runs/gap/
.claude/tigerkit/branches/<branch-key>/runs/verify/
.claude/tigerkit/branches/<branch-key>/branch-state.json
```

읽을 수 있는 evidence class:

- active/superseded Spec Patch metadata와 confirmed item
- accepted gap finding pattern
- rejected/downgraded observation reason
- source conflict와 resolution 상태
- verify-before-stop checklist evidence
- current code/worktree context needed to classify repo-wide value

## Durable insight target

기본 target:

```text
.claude/tigerkit-reflections.md
```

`--target <path>`가 있으면 current worktree root 내부의 durable insight file만 허용합니다. 권장 target은 `.claude/tigerkit-reflections.md` 또는 `docs/tigerkit-reflections.md`입니다.

허용 target 조건:

- current worktree root 내부 path
- filename이 `tigerkit-reflections.md`
- `.claude/tigerkit/` 아래가 아님
- source code path가 아님

금지 target:

- `.claude/tigerkit/**`
- source code path
- command file path
- rule file path
- arbitrary docs file such as `.tigerkit/docs/usage.md`
- current worktree root 밖 path
- `/tmp`
- user home global path

프로젝트가 `.claude/` 전체를 ignore하면 warning을 출력합니다. `.claude/tigerkit/`만 ignore하는 것은 정상입니다.

## Durable insight 후보

reflect는 아래만 durable insight 후보로 삼습니다.

- 반복적으로 등장한 accepted finding pattern
- branch에서 확정된 product/design decision 중 repo-wide 가치가 있는 것
- design-system 또는 component convention으로 승격할 만한 내용
- verify-before-stop에서 반복적으로 필요한 checklist
- source conflict에서 확정된 resolution

reflect는 아래를 durable insight로 만들지 않습니다.

- branch-specific one-off decision
- 임시 Spec Patch 자체
- superseded된 결정
- P3/nit
- rejected finding
- low-confidence observation
- source conflict가 unresolved인 내용
- implementation detail that only applies to this branch

## Classification

각 insight candidate는 아래 중 하나로 분류합니다.

| Target | 사용 조건 |
| --- | --- |
| `.claude/tigerkit-reflections.md` | v7 기본 durable insight target |
| `.claude/rules/**/*.md` proposal | repo convention rule로 승격할 가치가 있으나 직접 수정 대상이 아닐 때 |
| `CLAUDE.md` proposal | 저장소 전반 운영 규칙 후보지만 직접 수정 대상이 아닐 때 |
| no action | one-off, duplicate, unresolved, low-confidence일 때 |

v7 기본 apply는 durable insight target에만 적용합니다. `.claude/rules/*`, `CLAUDE.md`, source code는 제안으로만 다룹니다.

## Dedupe

동일 insight를 중복 반영하지 않습니다.

Dedupe key는 아래를 조합합니다.

```text
normalized insight title + target surface + source evidence class
```

이미 target에 같은 insight가 있으면 `skipped as duplicate`로 집계합니다.

## Output

기본 출력:

```text
Reflect Complete
Apply: true
Target: .claude/tigerkit-reflections.md

Applied Insights:
- <added> added
- <updated> updated
- <skipped> skipped as duplicate

Summary:
- <one-line insight summary>
```

`--dry-run` 또는 `--apply=false`일 때:

```text
Reflect Complete
Apply: false
Target: .claude/tigerkit-reflections.md

Preview Insights:
- <added> would add
- <updated> would update
- <skipped> skipped as duplicate

Summary:
- <one-line preview summary>
```

## Durable target format

`.claude/tigerkit-reflections.md`는 한글로 작성합니다. 각 insight는 evidence class와 scope를 분리합니다.

```md
# TigerKit Reflection 기록

## <insight title>

- 상태: active
- 출처: branch-local TigerKit memory
- 근거 분류: accepted_finding_pattern | verify_checklist | source_conflict_resolution | repo_wide_decision
- 범위: repo-wide | design-system | component-convention | workflow
- 인사이트: <durable insight>
- 적용 방법: <short operational rule>
```

## Procedure

1. current worktree root 계산
2. current branch-key 계산
3. branch scope 초기화
4. branch lock 획득
5. apply mode 계산: `apply = dryRun ? false : apply !== false`
6. durable insight target resolve
7. branch-local memory 로드
8. durable insight 후보 추출
9. one-off, superseded, P3/nit, rejected, low-confidence 후보 제거
10. duplicate 제거
11. apply=true이면 durable target을 수정하고 `global-index.json`에 branch `lastUsedAt` 갱신
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
- default를 proposal-only로 유지
