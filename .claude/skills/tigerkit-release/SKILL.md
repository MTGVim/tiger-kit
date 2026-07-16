---
name: tigerkit-release
description: TigerKit 저장소의 버전 갱신, 검증, commit, push, tag, GitHub Release를 안전한 순서로 수행합니다. 사용자가 /tigerkit-release를 명시적으로 호출한 경우에만 사용하세요.
disable-model-invocation: true
allow_implicit_invocation: false
argument-hint: "[patch|minor|major]"
metadata:
  internal: true
---

# TigerKit 릴리스

이 저장소에서 사용자가 `/tigerkit-release`를 명시적으로 호출한 경우에만 사용하세요. 기본 bump는 `patch`입니다.

## 계약

릴리스 기준은 로컬 추측이 아니라 fetch 후 확인한 원격 `main`, semantic version tag, GitHub Release입니다. 현재 요청이 commit, push, tag, release를 명시적으로 승인했다면 같은 범위를 다시 묻지 마세요. 목표 버전, 포함 diff, 원격 상태가 불명확하면 원격 변경 전에 `Blocked`로 중단하고 사용자 결정을 받으세요.

사용자가 `dry-run`, 가상 시나리오 또는 명령 미실행을 요청하면 제공된 상태를 평가 입력으로 사용하세요. 실제 repository나 원격을 조회·수정하지 말고 현재 작업 트리의 우연한 상태를 시나리오에 섞지 마세요. 실행할 버전, 순서, 중단 조건, 예상 receipt만 보고하세요.

다음 순서를 지키세요.

1. `git status`, branch, upstream, remote, 최근 commit과 tag, GitHub Release를 확인하세요.
2. `git fetch` 후 현재 branch와 `origin/main`의 차이를 확인하세요. 사용자 변경을 버리거나 force, hard reset, clean으로 동기화하지 마세요.
3. 최신 안정 semantic version에서 요청한 bump를 계산하고 같은 tag와 GitHub Release가 없는지 확인하세요.
4. 포함할 변경 전체를 읽고 unrelated 파일, secret, credential, `.tigerkit/` runtime scratch가 tracked 또는 staged되지 않았는지 확인하세요.
5. 기존 형식에 맞춰 `CHANGELOG.md`와 필요한 버전 표기를 갱신하세요. 과거 릴리스 기록의 버전은 일괄 치환하지 마세요.
6. 저장소 지침의 전체 검증, 회귀 테스트, `git diff --check`를 실행하세요. 실패를 우회하거나 hook을 건너뛰지 마세요.
7. 특정 파일만 stage하고 staged diff를 다시 확인한 뒤 새 commit을 만드세요. 기존 commit을 amend하지 마세요.
8. commit을 원격 branch에 push하세요.
9. 원격 commit이 확인된 뒤 기존 저장소 형식으로 tag를 만들고 push하세요.
10. tag가 원격에 존재하는지 확인한 뒤 `gh release create`로 GitHub Release를 만들고 결과 URL을 확인하세요.

검증 실패, 원격 branch 진전, 기존 tag/release 충돌, 인증 실패가 있으면 다음 원격 단계를 실행하지 마세요. 부분 성공이면 이미 생성된 commit, tag, release를 삭제하거나 덮어쓰지 말고 정확한 상태와 재개 지점을 보고하세요.

## 금지

- force push, `reset --hard`, `clean`, hook 우회
- 기존 tag 이동·삭제·재사용
- 실패한 검증을 성공으로 처리
- `.tigerkit/`, credential, token, browser profile 포함
- commit 전 tag 또는 tag 확인 전 GitHub Release 생성

## 완료 gate와 receipt

`Released`는 commit push, 원격 tag, GitHub Release URL, 전체 검증 증거가 모두 있을 때만 사용하세요. 다음을 보고하세요.

- **버전:** 이전 버전과 새 버전
- **포함 변경:** 주요 동작과 staged 파일
- **검증:** 실행 명령과 결과
- **Git:** commit SHA, branch push, tag
- **Release:** URL
- **미완료:** 실패하거나 실행하지 못한 단계
- **상태:** `Released | Blocked | Failed | Partial`
