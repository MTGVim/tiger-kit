---
name: tk-pr-open
description: "[user/auto] 검증된 current-branch commit으로 하나의 GitHub pull request를 열거나 업데이트하며, remote publication 전 exact current-turn approval을 요구합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# PR 열기

`/tk-pr-open`, `$tk-pr-open`, host skill picker 또는 “현재 브랜치로 PR 열어줘”처럼
하나의 PR create/update 의도가 명확할 때 시작합니다.

입력은 이미 구현·검증된 current branch commit입니다.
Ready `.tigerkit/seed.md`가 있으면 task goal, acceptance, browser evidence requirement를 읽을 수 있지만
Seed 자체가 publication authority는 아닙니다.

구현을 다시 수행하거나 worker를 만들거나 product commit을 추가하지 않습니다.

## Fresh state

먼저 다음을 확인합니다.

- repository와 authenticated GitHub identity
- current branch와 HEAD
- base branch
- intended commits와 changed paths
- 기존 같은 head PR 존재 여부
- unrelated dirty/staged paths
- target repository의 PR template

정확한 current commit을 입증할 수 없거나 unrelated change가 섞이면 범위를 넓히지 않고 `Blocked`/`Unverifiable`입니다.

## PR template

PR body를 만들기 전에 default branch의 지원되는 template 위치를 확인합니다.

- root
- `docs/`
- `.github/`
- 각 위치의 `PULL_REQUEST_TEMPLATE/`

적용 가능한 template이 하나면 heading 순서, checklist, HTML comment, 필수 section을 보존합니다.
여러 template 중 선택 근거가 없으면 후보와 한 가지 추천을 설명하고 publication 승인 전에 선택받습니다.
template을 읽을 수 없으면 body를 지어내지 않습니다.

## Evidence

Ready Seed 또는 현재 verified work에서 PR evidence 필요 여부를 확인합니다.

```text
required | optional | N/A | undecided
```

browser-visible acceptance에서 Ready Seed가 `tk-browser-verify` screenshot evidence를 required로 정했다면
유효한 inspected evidence만 사용합니다.
`tk-prototype` evidence도 승인된 경우 사용할 수 있습니다.

실제 secret-bearing screenshot이나 검증되지 않은 capture를 업로드하지 않습니다.
이미지가 필요하면 PR이 존재한 뒤 `tk-github-image-upload-to-pr`에 exact evidence path를 넘깁니다.

## Publication plan

`.tigerkit/pr-open.md`는 이 스킬의 standalone publication plan으로 유지합니다.
다음 exact 정보를 기록하고 reread합니다.

```text
Repository
PR operation: create | update
Base
Head ref + SHA
Push refspec
Title
Body
Template source/compliance
PR evidence requirement/state
Evidence producer/path
Known exclusions
```

이 artifact는 현재 PR publication plan만 소유하며 product task planning이나 worker state를 소유하지 않습니다.

사용자에게는 파일을 직접 열어야 이해되는 식으로 숨기지 말고 다음을 자연스럽게 보여줍니다.

- 포함되는 변경 요약
- 정확한 title/body 또는 중요한 template section
- base/head
- checks/evidence 상태
- exclusions/risks
- 한 가지 publication recommendation

그 뒤 exact current-turn approval 하나를 받습니다.
자연어 “PR 열어줘” 자체는 publication 승인으로 보지 않습니다.

## Publish

승인 뒤 repository, identity, branch, HEAD, base, existing PR, template source를 다시 확인합니다.
material drift가 있으면 승인을 무효화합니다.

승인된 exact refspec만 push하고 지정된 PR만 create/update합니다.
merge, close, tag, release를 하지 않습니다.

PR 생성/업데이트 후 remote PR을 fresh-read해 URL, head SHA, template compliance, evidence state를 확인합니다.
required evidence가 있으면 PR 존재 후 image uploader를 사용합니다.
PR 자체는 생성됐지만 required evidence upload가 실패하면 실제 remote state는 보존하고 완료 상태는 `Blocked`로 보고합니다.

## 완료

사용자에게 중요한 결과만 보여줍니다.

- PR URL
- create/update 여부
- current head
- verification/evidence 결과
- 남은 blocker

provenance dump나 product implementation receipt는 보여주지 않습니다.
