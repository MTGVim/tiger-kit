---
name: tigerkit-release
description: TigerKit 저장소의 버전 갱신, 검증, commit, push, tag, GitHub Release를 안전한 순서로 수행합니다. 사용자가 /tigerkit-release를 명시적으로 호출한 경우에만 사용하세요.
disable-model-invocation: true
allow_implicit_invocation: false
argument-hint: "[patch|minor|major] | promote <remote-branch> [patch|minor|major] | dry-run <scenario>"
metadata:
  internal: true
---

# TigerKit 릴리스

이 저장소에서 사용자가 `/tigerkit-release`를 명시적으로 호출한 경우에만 사용하세요. 기본 bump는 `patch`입니다.

## 모드와 입력

호출은 다음 중 하나여야 합니다.

```text
/tigerkit-release [patch|minor|major]
/tigerkit-release promote <remote-branch> [patch|minor|major]
/tigerkit-release dry-run <scenario>
```

- **Normal release**: 현재 branch에서 최신 안정 release 다음 버전을 준비합니다. `patch|minor|major`를 생략하면 `patch`입니다.
- **Promote**: 사용자가 정확히 지정한 remote branch를 현재 `main`에 승격한 뒤 normal release flow를 같은 실행에서 재개합니다. branch를 자동 발견하거나 추측하지 마세요.
- **Dry-run**: 사용자가 제공한 scenario만 평가하세요. 실제 repository·remote를 조회하거나 `git`, `gh`, 파일 mutation을 실행하지 마세요. scenario가 없거나 서로 충돌하면 `Blocked`입니다.

`resume`은 별도 branch 선택 모드가 아니라, commit·tag·Release 중 일부만 완료된 실행을 첫 번째 누락 단계부터 이어가는 상태입니다.

## 계약

릴리스 기준은 로컬 추측이 아니라 fetch 후 확인한 원격 `main`, semantic version tag, GitHub Release입니다. 현재 요청이 commit, push, tag, release를 명시적으로 승인했다면 같은 범위를 다시 묻지 마세요. 목표 버전, 포함 diff, 원격 상태가 불명확하면 원격 변경 전에 `Blocked`로 중단하고 사용자 결정을 받으세요. 원격 Release와 최종 검증까지 성공한 뒤에는 로컬 `main`으로 복귀해야 합니다.

사용자 변경을 버리거나 force, rebase, hard reset, clean으로 동기화하지 마세요. 기존 tag를 이동·삭제·재사용하지 마세요.

## Normal release preflight

1. `git status`, branch, upstream, remote, 최근 commit과 tag, GitHub Release를 확인하세요.
2. `git fetch --prune origin` 후 현재 branch와 `origin/main`의 차이를 확인하세요.
3. 최신 안정 semantic version tag와 GitHub Release를 확인하고 요청한 bump를 계산하세요.
4. 최신 안정 tag가 `origin/main`의 조상이 아니거나 `origin/main`이 preflight 이후 진전했으면 자동 merge하지 말고 `Blocked`로 중단하세요. 발견한 release tag, candidate branch, commit SHA와 필요한 다음 명령을 보고하고 `promote <remote-branch>`를 제안하세요.
5. 포함할 변경 전체를 읽고 unrelated 파일, secret, credential, `.tigerkit/` runtime scratch가 tracked 또는 staged되지 않았는지 확인하세요.

Normal release는 다른 branch를 자동 탐색하거나 merge하지 않습니다. 기존 release branch를 사용하려면 Promote 모드를 명시적으로 호출해야 합니다.

## Promote flow

`promote <remote-branch>`가 호출되면 다음 순서를 지키세요.

1. 정확한 remote branch가 존재하는지 fetch 후 확인하세요. branch 이름을 추측하거나 가장 최신 branch를 대신 선택하지 마세요.
2. branch tip, `origin/main`, 최신 release tag, 관련 GitHub Release와 각 commit SHA를 확인하세요.
3. `v19.x.y` 이후 branch가 가져올 commit과 diff를 preview하고, `.tigerkit/`, secret, credential이 포함되지 않았는지 확인하세요.
4. `git merge-tree`로 통합 가능성을 확인하세요. conflict가 있으면 파일을 수정하지 말고 `Blocked`로 중단하세요.
5. 충돌이 없고 사용자가 지정한 branch가 기준에 맞으면 `git merge --no-ff --no-edit origin/<remote-branch>`로 통합하세요. rebase, cherry-pick, force push, 자동 conflict 해결은 사용하지 마세요.
6. 통합 후 full verification을 다시 실행하고, 그 결과를 포함 diff의 기준으로 삼으세요.
7. branch에 이미 tag와 GitHub Release가 있다면 이를 완료된 기준점으로 인정하고 같은 artifact를 재생성하지 마세요. 통합 후 새 diff가 있을 때만 다음 semantic version을 계산하세요.
8. 통합 후 normal release의 version, changelog, 검증, commit, push, tag, Release 단계를 계속 진행하세요.

## Partial-success resume

원격 상태를 확인할 때 다음 matrix를 적용하세요.

| 확인된 상태 | 재개 동작 |
| --- | --- |
| commit이 remote에 없음 | 검증된 commit push 단계부터 재개 |
| commit은 있지만 tag가 없음 | remote commit SHA를 확인한 뒤 tag 단계부터 재개 |
| tag는 올바른 commit을 가리키고 Release가 없음 | tag를 이동하지 않고 Release 단계만 재개 |
| tag와 Release가 모두 올바름 | 해당 단계를 건너뛰고 다음 단계 또는 완료 상태를 보고 |
| commit·tag·Release는 올바르지만 현재 branch가 `main`이 아님 | artifact를 재생성하지 않고 post-release `main` 복귀 단계부터 재개 |
| tag·Release가 다른 version 또는 commit을 가리킴 | 덮어쓰지 말고 `Blocked` |

이미 완료된 artifact를 재생성하지 말고, 각 단계 전에 remote 상태를 다시 확인하세요. 이전 단계가 성공했는지 증거가 없으면 성공으로 추정하지 마세요.

## 검증과 mutation 순서

다음 순서를 지키세요.

1. version과 CHANGELOG, 필요한 version 표기를 기존 형식에 맞춰 갱신하세요. 과거 release 기록의 version을 일괄 치환하지 마세요.
2. 저장소 지침의 전체 검증, 회귀 테스트, `git diff --check`를 실행하세요. 실패를 우회하거나 hook을 건너뛰지 마세요.
3. 특정 파일만 stage하고 staged diff와 `.tigerkit`·secret·credential 포함 여부를 다시 확인하세요.
4. 새 commit을 만드세요. 기존 commit을 amend하지 마세요.
5. commit을 remote branch에 push하고 remote commit SHA를 확인하세요.
6. remote commit 확인 후 기존 저장소 형식으로 tag를 만들고 push하세요. tag가 이미 있으면 대상 commit을 검증하고 이동하지 마세요.
7. tag가 remote에 존재하는지 확인한 뒤 `gh release create`로 GitHub Release를 만드세요. Release가 이미 있으면 내용을 덮어쓰지 말고 현재 URL과 상태를 보고하세요.
8. 마지막으로 remote `main`, tag, Release URL, worktree와 전체 검증 결과를 확인하세요.
9. 8번의 모든 검증과 artifact 확인이 성공한 뒤에만 post-release 정리를 수행하세요.

## 릴리즈 후 `main` 복귀

`commit push`, remote tag, GitHub Release URL, 최종 검증이 모두 확인된 뒤에만 실행하세요.

1. `git status --porcelain`이 비어 있는지 확인하세요. 사용자 변경이나 미추적 파일이 있으면 stash, `reset`, `clean`으로 건드리지 말고 현재 branch와 상태를 보고 `Partial`로 중단하세요.
2. worktree가 깨끗하면 `git switch main`으로 로컬 `main`에 복귀하세요. 로컬 `main`이 없거나 전환이 실패하면 파일과 artifact를 되돌리지 말고 정확한 오류와 현재 branch를 보고 `Partial`로 중단하세요.
3. `git branch --show-current`가 `main`인지, worktree가 깨끗한지, remote `main`·tag·Release가 기대한 commit/version을 가리키는지 다시 확인하세요.

post-release `main` 복귀까지 성공해야 최종 상태를 `Released`로 보고합니다. artifact는 완성됐지만 복귀에 실패한 경우 artifact를 재생성하지 말고 `Partial` 상태에서 `main` 복귀 단계만 재개하세요.

검증 실패, 원격 branch 진전, 기존 tag/Release 충돌, 인증 실패가 있으면 다음 원격 단계를 실행하지 마세요. 부분 성공이면 이미 생성된 commit, tag, Release를 삭제하거나 덮어쓰지 말고 정확한 상태와 resume 지점을 보고하세요.

## 금지

- force push, rebase, `reset --hard`, `clean`, hook 우회
- Promote/normal preflight에서 지정하지 않은 branch 자동 선택·자동 merge (단, 성공한 릴리즈 뒤 로컬 `main` 복귀는 필수 정리 단계입니다)
- 기존 tag 이동·삭제·재사용 또는 기존 Release 덮어쓰기
- 실패한 검증을 성공으로 처리
- `.tigerkit/`, credential, token, browser profile 포함
- commit 전 tag 또는 tag 확인 전 GitHub Release 생성
- dry-run 중 실제 repository·remote 조회나 mutation

## 완료 gate와 receipt

`Released`는 commit push, remote tag, GitHub Release URL, 전체 검증 증거, post-release 로컬 `main` 복귀가 모두 확인됐을 때만 사용하세요. 다음을 보고하세요.

- **Mode:** normal 또는 `promote <remote-branch>`
- **Reconciliation:** merge한 branch, 기존 tag/Release, resume 지점
- **버전:** 이전 버전과 새 버전
- **포함 변경:** 주요 동작과 staged 파일
- **검증:** 실행 명령과 결과
- **Git:** commit SHA, branch push, tag
- **Branch:** 릴리즈 직전 branch와 최종 branch (`main`)
- **Release:** URL
- **미완료:** 실패하거나 실행하지 못한 단계
- **상태:** `Released | Blocked | Failed | Partial`

정적 상태 fixture는 [behavior-cases.yaml](references/behavior-cases.yaml)에 유지합니다.
