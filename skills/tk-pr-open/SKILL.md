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

# `pull request` 열기

사용자가 `/tk-pr-open`, `$tk-pr-open`, 또는 호스트 `skill picker`를 선택했을 때
시작하거나, 자연어로 하나의 PR을 준비·열기·업데이트해 달라는 명확한 요청이
있을 때 시작한다. “검증된 commit이 끝났으니 PR을 준비해줘” 같은
`tk-drive` 이후의 `handoff`도 포함한다. 이때 입력은 기존에 검증된 현재 브랜치
commit이며, 구현 작업을 중복하지 않는다. 해당 commit을 재사용하고, 다른 제품
worker를 dispatch하거나 제품 commit을 추가로 만들지 않는다. 자연어 라우팅은
이 `skill`의 로컬 미리보기만 시작하며 발행을 의미하지 않는다. 일반적인 PR
질문, code review, 구현 요청, merge request, 여러 PR 유지보수 요청, 또는 기존
`.tigerkit` 산출물만으로는 절대 활성화하지 않는다.

하나의 `pull request` 초안과 제한된 발행 계획을 소유한다. 로컬 Git/GitHub
상태를 확인하고 `.tigerkit/pr-open.md` 를 작성할 수 있다. 아래 승인 게이트
전에는 제품 코드 수정, 제품 commit 생성, merge, tag, release, publish를 하지 않는다.

## 작업 흐름

1. 실행 저장소, 인증된 GitHub identity, 현재 브랜치, `HEAD`, 변경된 경로, 기준
   브랜치, 해당 브랜치의 기존 PR을 확인한다.
2. 의도한 commit이 존재하는지, 관련 없는 변경 경로가 보존되는지, 제안한 PR이
   기존 PR과 중복되지 않는지 검증한다.
3. PR 본문을 쓰기 전에 대상 저장소의 기본 브랜치에서 GitHub가 지원하는
   `pull_request_template.md` 위치(root, `docs/`, `.github/`)와 각 위치의
   `PULL_REQUEST_TEMPLATE/` 후보를 확인한다. 적용 가능한 템플릿이 하나면
   제목 순서, 체크리스트, HTML 주석과 필수 섹션을 보존해 채운다. 여러 템플릿
   중 선택 근거가 없으면 임의로 고르지 말고 후보와 한 가지 추천을 미리보기에
   표시해 발행 승인 전에 선택받는다. 템플릿을 읽지 못하면 본문을 창작하지 않고
   `Unverifiable`이다. 템플릿이 없을 때만 간결한 기본 본문을 작성한다.
4. 요청 또는 Ready 계약에서 `PR evidence: required | optional | N/A` 를 받는다.
   `required` 를 `evidence_required: true` 로 매핑하고, `tk-browser-verify` 또는
   `tk-prototype`의 유효한 스크린샷 `handoff`만 수집한다. `optional` 이면 승인된
   계획에 명시적으로 포함된 증거만 업로드하고, `N/A` 이면 업로더를 호출하지
   않는다. 계획에 producer, 절대 증거 디렉터리, 스크린샷 경로, 실제 검사,
   criterion을 기록한다. 값이 없으면 한 가지 추천과 함께
   `PR evidence: undecided` 를 표시하고 발행 승인 전에 결정을 받는다. 임의의
   스크린샷이나 브라우저 검증만으로 필수 증거를 추론하지 않는다.
5. 정확한 제목, 본문, base/head 참조, push refspec, 템플릿 출처/준수 상태,
   알려진 제외 사항을 `.tigerkit/pr-open.md` 에 작성한다. PR을 업데이트할 때
   기존 본문 섹션, 체크리스트, 첨부 파일, 사용자 작성 메모를 보존하고 적용
   가능한 템플릿의 누락 섹션만 보강한다.

계획은 다음 필드를 빠짐없이 채운다. 값은 실제 검증 결과로 교체하며, `Push refspec` 은 승인 후 그대로 실행할 명령의 source와 destination을 함께 적는다.

```text
Repository: <owner/repo>
PR operation: create | update #<number>
Base: <base-branch>
Head: <head-branch>@<head-sha>
Push refspec: <remote> <head-branch>:<head-branch>
Title: <exact-title>
Body: <exact-body>
Template source: <repository path | none>
Template compliance: <Pass | Pending | Unverifiable>
PR evidence: required | optional | N/A
Evidence producer: <tk-browser-verify | tk-prototype | N/A>
Evidence directory: <absolute-path | N/A>
Evidence paths: <absolute-paths | N/A>
Known exclusions: <none | exact exclusions>
```

승인된 `Push refspec` 의 실행 형태는 `git push <remote> <head-branch>:<head-branch>` 이며, 실제 값이 브랜치·`HEAD` 재검증 결과와 다르면 실행하지 않는다.
6. 승인 요청 전에 다음 순서로 미리보기를 보여준다: 포함 변경 사항, 템플릿
   출처/준수 상태와 정확한 PR 제목/본문, base/head와 검사/증거 상태, 제외
   사항/위험, 한 가지 발행 추천. refspec, identity, provenance는 결정에 중요하지
   않으면 산출물에 남긴다. 승인 질문은 하나만 하고 `Pending` 으로 멈춘다.
   일반적인 “go ahead”는 다른 계획이나 오래된 계획을 승인하지 않는다.
7. 현재 턴 승인 후 브랜치, `HEAD`, PR identity, 공개 상태와 템플릿 출처를 다시
   확인한다. 템플릿이 바뀌거나 정확한 본문이 템플릿 구조를 빠뜨리면 승인을
   무효화한다. 명시적 refspec만 push하고, 지정된 PR만 create/update한다. 필수
   증거가 유효하면 PR이 존재한 뒤 `tk-github-image-upload-to-pr` 로 인계한다.
8. 원격 PR을 다시 읽고 URL, head SHA, operation 결과, 템플릿 준수 상태, 남은
   검사를 보고한다. 필수 증거가 없거나 업로드가 실패하면 PR 결과는 유지하되
   최종 완료 상태는 `Blocked` 로 반환한다. merge하거나 release를 요청하지 않는다.

## 🔴 체크포인트 / 중지 · 발행 게이트

계획에는 저장소, PR 생성/업데이트 대상, 기준 브랜치, 작업 브랜치, 정확한 push
refspec, 제목, 본문, 템플릿 출처/준수 상태, 증거 요구/상태, 작업 순서, 제외
사항을 명시해야 한다.

| 조건 | 첫 조치 | 미해결 시 |
|---|---|---|
| 정확한 현재 턴 승인 대기 | 원격 쓰기를 하지 않는다 | `Pending` |
| 브랜치/PR head, identity, 변경 경로, 본문, 대상이 바뀜 | 승인을 무효화하고 계획을 갱신한다 | `Blocked` |
| 적용 가능한 템플릿을 읽지 못했거나 본문이 템플릿 구조를 누락함 | create/update를 하지 않고 출처와 누락을 보고한다 | `Unverifiable` |
| 필수 Git 또는 GitHub 증거를 사용할 수 없음 | 시도한 검사/증거 누락을 기록한다 | `Unverifiable` |
| Push, create, update가 실패하거나 계획 일부만 적용됨 | 원격 PR을 다시 읽고 정확한 적용 상태를 보고한다 | `Fail` |
| PR 생성 후 필수 업로드가 없거나 실패함 | PR을 유지하고 증거 복구 조건을 보고한다 | `Blocked` |
| 요청된 PR 작업과 필수 증거가 검증됨 | 새 URL과 head SHA를 보고한다 | `Pass` |

`## PR open` 으로 시작하고 사용자에게 중요한 상태, 검증, 남은 위험만 보여준다.
전체 provenance는 `.tigerkit/pr-open.md` 에 보관한다.
