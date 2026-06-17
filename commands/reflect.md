---
description: branch-local TigerKit memory에서 repo에 보존할 insight만 추출·반영합니다.
argument-hint: "[scope] [--dry-run] [--apply=true|false] [--target <CLAUDE.md|.claude/rules/...>] [--no-meta-feedback|--meta-feedback=false]"
---

이 명령은 TigerKit v8.0 reflect contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 Gap workflow, Launch trace, Gap이 already-grounded source로 채택한 legacy Spec Patch reference에서 repo-wide 가치가 있는 durable insight만 추출해 적절한 durable surface에 직접 반영합니다.

```text
reflect = branch-local gap+launch working memory -> CLAUDE.md/.claude/rules durable reflection
```

## Command surface

- plugin slash invocation은 `/tk:reflect`입니다.
- `tiger-kit reflect` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.

## 핵심 원칙

- gap/launch/verify 산출물과 legacy Spec Patch 자체는 repo-wide durable knowledge가 아닙니다.
- repo에 영구적으로 남길 insight는 reflect를 통해서만 추출합니다.
- `/tk:reflect` 기본 동작은 `apply=true`입니다.
- 반영할 durable insight가 없으면 아무 파일도 수정하지 않는 것이 정상 성공입니다.
- source code는 수정하지 않습니다.
- apply mode의 content write는 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에만 적용합니다.
- branch recency bookkeeping으로 `global-index.json`의 branch entry를 생성하거나 `lastUsedAt`을 갱신할 수 있습니다.
- branch-local specs/gap 산출물이 없다는 사실만으로 세션 관측 패턴을 durable insight 후보로 승격하지 않습니다.
- 같은 insight를 중복 반영하지 않습니다.
- 후보 평가 전 기존 `CLAUDE.md`와 `.claude/rules/**/*.md`를 inventory해 이미 커버되는 guidance를 찾습니다.
- 적용 결과 diff/summary를 출력합니다.
- 기본적으로 reflect 처리 직후 같은 세션에서 `/tk:meta-feedback`을 proposal-only로 함께 제출합니다.
- `--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 meta-feedback 제출을 생략합니다.

## Apply behavior

| Command | 동작 |
| --- | --- |
| `/tk:reflect` | `apply=true` |
| `/tk:reflect --apply=true` | 기본값과 동일 |
| `/tk:reflect --dry-run` | `apply=false`, meta-feedback 기본 제출 |
| `/tk:reflect --apply=false` | dry-run alias, meta-feedback 기본 제출 |
| `/tk:reflect --no-meta-feedback` | reflect만 실행하고 meta-feedback 제출 생략 |
| `/tk:reflect --meta-feedback=false` | `--no-meta-feedback` alias |

v8.0에서는 `--apply=true`가 redundant여도 warning을 내지 않습니다.

## Inputs

Reflect는 current branch scope의 branch-local working memory를 읽습니다.

```text
.claude/tigerkit/branches/<branch-key>/gap/
.claude/tigerkit/branches/<branch-key>/launch/
.claude/tigerkit/branches/<branch-key>/runs/gap/
.claude/tigerkit/branches/<branch-key>/branch-state.json
```

Legacy `.claude/tigerkit/branches/<branch-key>/specs/`는 `/tk:gap`이 source material로 채택해 gap artifact에 trace한 경우에만 간접 evidence로 참고합니다. Reflect가 legacy Spec Patch를 repo-wide rule로 직접 승격하지 않습니다.

읽을 수 있는 evidence class:

- gap artifact에 trace된 legacy Spec Patch reference와 accepted/rejected treatment
- accepted gap finding pattern
- rejected/downgraded observation reason
- source conflict와 resolution 상태
- 사용자 대화에서 명시적으로 확인된 TigerKit 운영 규칙
- current code/worktree context needed to classify repo-wide value

branch-local gap 산출물이 없으면 산출물 기반 후보는 없는 것으로 처리합니다. 이 경우에도 사용자 대화에서 명시적으로 확인된 TigerKit 운영 규칙은 후보가 될 수 있지만, legacy Spec Patch나 실행자 해석만으로 repo-wide durable insight를 만들지 않습니다.

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

후보는 durable target classification 전에 아래 rubric을 모두 통과해야 합니다.

| 기준 | 통과 조건 |
| --- | --- |
| Frequency | 반복됐거나 반복될 가능성이 높음 |
| Cost | 매번 다시 발견하거나 설명하는 비용이 큼 |
| Risk | 누락 시 source loss, decision loss, bug, regression, 오판 가능성이 있음 |
| Stability | 현재 branch에만 묶이지 않고 앞으로도 유지될 규칙임 |
| Coverage | 기존 `CLAUDE.md` 또는 `.claude/rules/**/*.md`가 이미 커버하지 않음 |

통과하지 못한 후보는 `no action`으로 분류합니다. 근거가 부족하지만 후속 확인 가치가 있으면 `Needs more evidence`에 남깁니다.

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
- <no_action> no action

요약:
- <한글 insight summary>

Needs more evidence:
- <확인 필요 항목 또는 None>

Meta Feedback:
- submitted
```

반영할 durable insight가 없을 때:

```text
Reflect 완료
Apply: true
적용 대상:
- 없음

적용 결과:
- 0 added
- 0 updated
- <skipped> skipped as duplicate
- <no_action> no action

요약:
- No durable insight promoted.

Needs more evidence:
- <확인 필요 항목 또는 None>

Meta Feedback:
- submitted
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

Meta Feedback:
- submitted
```

## Procedure

1. current worktree root 계산
2. current branch-key 계산
3. branch scope 초기화
4. branch lock 획득
5. apply mode 계산: `apply = dryRun ? false : apply !== false`
6. branch-local memory 로드
7. 기존 durable guidance inventory로 `CLAUDE.md`와 `.claude/rules/**/*.md`의 coverage 확인
8. durable insight 후보 추출
9. Frequency, Cost, Risk, Stability, Coverage rubric으로 후보 평가
10. 각 후보를 `CLAUDE.md`, `.claude/rules/**/*.md`, `no action`, `needs more evidence`로 분류
11. one-off, superseded, P3/nit, rejected, low-confidence 후보 제거
12. duplicate 제거
13. apply=true이고 적용 대상이 있으면 target rule file 또는 `CLAUDE.md`를 직접 수정하고 `global-index.json`에 branch entry가 없으면 생성한 뒤 `lastUsedAt` 갱신
14. apply=true이지만 적용 대상이 없으면 파일을 수정하지 않고 정상 완료합니다.
15. apply=false이면 preview만 출력하고 저장 없이 종료
16. branch lock 해제
17. `--no-meta-feedback` 또는 `--meta-feedback=false`가 없으면 `/tk:meta-feedback`을 proposal-only로 제출
18. reflect summary, Needs more evidence, meta-feedback 제출 상태를 출력

`--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 `Meta Feedback: skipped by opt-out`으로 출력합니다.

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
