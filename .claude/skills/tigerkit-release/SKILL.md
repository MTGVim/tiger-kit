---
name: tigerkit-release
description: TigerKit의 현재 candidate를 release/main 계보와 의도 기반으로 정합화한 뒤 검증, candidate push, PR merge, tag, GitHub Release까지 안전하게 수행합니다. 사용자가 /tigerkit-release를 명시적으로 호출한 경우에만 사용하세요.
disable-model-invocation: true
allow_implicit_invocation: false
argument-hint: "[patch|minor|major] | promote <remote-branch> [patch|minor|major] | dry-run <scenario>"
metadata:
  internal: true
---

# TigerKit 릴리스

사용자가 `/tigerkit-release`를 명시적으로 호출한 경우에만 사용하세요. 기본 bump는 `patch`입니다. 이 호출은 현재 candidate의 안전한 history rewrite, candidate ref push, PR 생성·merge, tag, GitHub Release를 한 번 승인합니다. 각 단계의 gate를 통과하면 재확인 없이 끝까지 진행하세요.

## 입력

```text
/tigerkit-release [patch|minor|major]
/tigerkit-release promote <remote-branch> [patch|minor|major]
/tigerkit-release dry-run <scenario>
```

- **Normal**: 호출 시점의 현재 `HEAD`를 to-be candidate로 삼습니다. 현재 branch가 `main`이거나 detached이면 목표 버전의 `release/vX.Y.Z` branch를 만들어 candidate를 격리합니다.
- **Promote**: 사용자가 지정한 정확한 `origin/<remote-branch>` tip을 candidate로 삼고 이후에는 Normal과 같은 pipeline을 사용합니다. branch를 추측하지 마세요.
- **Dry-run**: 제공된 scenario만 평가하고 repository·remote 조회나 mutation을 전혀 실행하지 않습니다. scenario가 없거나 모순되면 `Blocked`입니다.
- **Resume**: 별도 모드가 아닙니다. 기존 candidate ref, PR, merge, tag, Release를 exact SHA로 확인하고 첫 누락 checkpoint부터 계속합니다.

## 불변식

- Stable release는 항상 PR로 `main`에 합친 뒤 최종 `origin/main` commit에 tag합니다. `main`에 직접 push하지 마세요.
- current candidate의 동작 의도가 to-be입니다. 최신 release와 remote main의 history·metadata는 보존하되 candidate가 바꾼 동작을 과거 내용으로 되돌리지 마세요.
- 기존 tag를 이동·삭제·재사용하거나 Release를 덮어쓰지 마세요.
- `reset --hard`, `clean`, hook 우회, unbounded force push를 사용하지 마세요.
- `.tigerkit/`, credential, token, browser profile을 commit하지 마세요.
- worktree가 dirty하거나 pre-existing merge/rebase/cherry-pick/revert가 진행 중이면 사용자 상태를 보존하고 `Blocked`로 중단하세요.

## 1. Fixed point와 release base

원격 mutation 전에 다음 증거를 한 묶음으로 기록하세요.

- candidate branch, `HEAD`, tree, upstream과 candidate remote tip
- fetch 후 `origin/main` SHA와 tree
- 최신 안정 semantic tag의 peeled SHA와 GitHub Release target
- 목표 version, 포함 commit·전체 diff, worktree 상태

최신 tag와 `origin/main`을 비교해 **linear release base**를 정하세요.

1. tag가 `origin/main`의 조상이면 base는 `origin/main`입니다.
2. `origin/main`이 tag의 조상이면 base는 peeled tag commit입니다.
3. 둘이 갈라졌지만 candidate가 둘 다 포함하면 candidate history를 유지합니다.
4. 그 외에는 어느 history도 버리지 말고 `Blocked`로 중단합니다.

목표 tag·Release·PR이 이미 존재하면 version과 SHA가 이 fixed point와 정확히 맞는지 확인하세요. 맞으면 완료된 checkpoint로 인정하고, 다르면 원격 artifact를 고치지 말고 `Blocked`입니다.

## 2. Candidate 격리와 의도 기반 rebase

먼저 포함 diff에서 unrelated 파일, secret, runtime scratch를 제외할 수 있는지 확인하세요. Normal이 `main`/detached에서 시작했다면 기존 ref와 충돌하지 않는 `release/vX.Y.Z` branch를 current `HEAD`에 생성하세요. Promote는 fetch한 exact remote tip을 local tracking branch로 attach합니다.

Linear release base가 candidate의 조상이 아니면 candidate-only commits를 그 base에 rebase하세요. 실행 전에 old head/tree, old fork, new base, candidate가 바꾼 paths와 삭제를 기록하고 rebase plan을 preview합니다.

Conflict는 다음 의도 순서로 hunk별 해결하세요.

1. candidate가 의도적으로 바꾼 동작·삭제
2. 최신 안정 release의 version·CHANGELOG·release history
3. candidate가 건드리지 않은 remote-main 변경

`ours`/`theirs` 이름이나 `-X ours|theirs`에 의존하지 말고 base, replay 중인 commit, target base의 실제 내용을 읽으세요. 명백한 해법과 검증 seam이 있을 때만 release-owned rebase를 계속합니다. 의도가 모호하거나 unrelated commit을 버려야 하면 `git rebase --abort` 후 원래 branch·tree를 확인하고 `Blocked`입니다.

Rebase 뒤에는 `range-diff`, old/new full diff, candidate-owned paths, version history를 대조하고 관련 검증을 실행하세요. non-conflicting legacy 내용도 살아남을 수 있으므로 conflict가 없었다는 사실만으로 성공 처리하지 마세요. 결과가 candidate의 to-be와 release base 둘 다 보존한다는 증거가 없으면 push하지 않습니다.

## 3. Version candidate와 전체 검증

1. 최신 안정 version에 요청한 bump를 적용하고 version, CHANGELOG, 필요한 현재-version 표기만 기존 형식대로 갱신하세요. 과거 release 기록을 일괄 치환하지 마세요.
2. 저장소 지침의 validator, links, regression tests, packaging smoke test와 `git diff --check`를 실행하세요. 실패를 우회하지 마세요.
3. 특정 파일만 stage하고 staged diff, `.tigerkit/`, secret·credential을 다시 검사하세요.
4. 새 release-preparation commit을 만드세요. 기존 commit을 amend하지 마세요.

## 🔴 CHECKPOINT · candidate push 전

fixed point가 stale하지 않고, reconciliation ledger와 포함 diff가 설명되며, 전체 검증과 staged 검사에 성공했고, worktree가 clean이며, branch가 `main`이 아닌 경우에만 push합니다.

- remote candidate ref가 없으면 exact local branch를 `-u`로 생성합니다.
- remote tip이 local의 조상이면 fast-forward push합니다.
- 이 실행의 rebase가 기존 candidate ref만 rewrite했고 recorded remote tip에 unseen commit이 없을 때만 `--force-with-lease=<ref>:<recorded-sha>`를 그 ref에 한정해 사용할 수 있습니다.
- lease가 실패하거나 remote candidate에 unseen commit이 있으면 fetch 후 fixed point부터 다시 판단합니다. `main`, tag, 다른 ref에는 force하지 마세요.

Push 뒤 remote candidate SHA가 local release-preparation commit과 같은지 확인하세요.

## 4. Exact PR과 PR-head evidence

`base=main`, `head=<candidate ref>`, 목표 version으로 open PR을 하나만 생성하거나 재사용하세요. 기존 PR의 base, head ref/SHA, version 또는 포함 diff가 다르면 새 PR로 우회하지 말고 `Blocked`입니다.

Exact PR head SHA에서 다음을 모두 통과시키세요.

- blocking `validate` workflow
- 최신 안정 tag를 baseline으로 명시한 `skill-evals` workflow dispatch와 성공
- 변경 종류에 필요한 packaging/canary 검증

Pending, skipped, failed, `Unverifiable`, 다른 SHA의 성공은 merge 권한이 아닙니다.

## 🔴 CHECKPOINT · PR merge 전

다시 fetch하고 다음이 모두 fixed point와 맞을 때만 PR을 merge하세요.

- PR head가 검증된 exact candidate SHA
- `origin/main`이 reconciliation 이후 예상한 SHA이며 candidate가 그 내용을 포함함
- 목표 tag와 Release가 여전히 비어 있거나 exact resume artifact임
- PR이 mergeable이고 필수 review/check가 충족됨
- candidate tree, 포함 diff, secret 검사 결과가 변하지 않음

`origin/main`이나 PR head가 진전했으면 merge하지 말고 reconciliation과 exact-SHA 검증을 새로 수행합니다.

PR은 merge commit 방식으로 합쳐 candidate ancestry를 보존하세요. repository가 merge queue/auto-merge만 허용하면 exact head를 고정한 채 그 경로를 사용하고 완료를 기다립니다. squash/rebase merge로 commit identity를 바꾸지 마세요. merge 후 fetch한 `origin/main`이 candidate를 조상으로 포함하고 그 tree가 candidate tree와 같은지 확인합니다.

## 5. Final main evidence, tag, Release

1. merge된 exact `origin/main` SHA에서 blocking `validate` 성공을 기다립니다.
2. 같은 final main SHA를 candidate로 `skill-evals`를 다시 dispatch하고 최신 안정 tag baseline 대비 성공을 확인합니다.
3. 두 workflow의 SHA, fetched `origin/main`, 목표 version과 tree가 모두 맞을 때만 annotated tag를 만들고 push합니다.
4. remote tag의 peeled SHA를 확인한 뒤에만 GitHub Release를 생성합니다.
5. `origin/main`, peeled tag, GitHub Release tag target, 성공한 final-main CI SHA가 모두 같은지 확인합니다.

Tag나 Release가 중간에 이미 생겼다면 exact version/SHA만 완료 checkpoint로 인정합니다. 불일치는 삭제·이동·덮어쓰기 없이 `Blocked`; 인증·CI·network 실패는 이미 성공한 artifact를 보존하고 `Partial`입니다.

## 6. 로컬 `main` 복귀

원격 artifact와 최종 equality가 모두 성공한 뒤 worktree가 clean일 때만 local `main`으로 전환하고 `origin/main`까지 fast-forward합니다. local `main`에 unique commit이 있거나 전환/fast-forward가 불가능하면 reset, stash, clean하지 말고 artifact를 보존한 `Partial`로 보고합니다. 최종 branch가 `main`이고 clean해야 `Released`입니다.

## Resume matrix

| Exact 상태 | 재개 지점 |
| --- | --- |
| candidate commit만 local | candidate ref push |
| candidate ref는 exact, PR 없음 | PR 생성 |
| PR open, head evidence 완료 | merge 전 stale check |
| PR merged, tag 없음 | final-main evidence |
| tag exact, Release 없음 | Release 생성 |
| tag·Release exact, local branch가 main 아님 | local main 복귀 |
| 어느 artifact든 version/SHA 불일치 | `Blocked`, destructive repair 금지 |

각 단계 직전에 remote state를 다시 읽고, 증거가 없는 성공을 추정하지 마세요.

## Receipt

`Released`는 final `origin/main`·peeled tag·Release target·final-main CI SHA equality와 local clean `main`이 모두 확인된 경우에만 사용하세요.

- **Mode / candidate:** normal 또는 promote, source와 remote ref
- **Reconciliation:** old head/base, new base/head, intent resolution과 resume 지점
- **Version / diff:** 이전·새 version, 주요 동작, staged files
- **PR / validation:** PR URL, head SHA, 실행한 검증과 결과
- **Git / Release:** merge SHA, tag SHA, CI SHA, Release URL
- **Branch:** 시작 branch와 최종 branch
- **미완료:** 실패·미실행 단계와 안전한 resume 지점
- **상태:** `Released | Blocked | Failed | Partial`

정적 상태 fixture는 [behavior-cases.yaml](references/behavior-cases.yaml)에 유지합니다.
