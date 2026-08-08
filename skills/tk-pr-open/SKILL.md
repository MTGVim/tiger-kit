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

# Pull request 열기

사용자가 `/tk-pr-open`, `$tk-pr-open`, 또는 host skill picker를 선택했을 때 시작하거나, 자연어로 하나의 PR을 준비·열기·업데이트해 달라는 명확한 요청이 있을 때 시작한다. “검증된 commit이 끝났으니 PR을 준비해줘” 같은 post-`tk-drive` handoff도 포함한다. 이때 입력은 기존 verified current-branch commit이며, 구현 작업을 중복하지 않는다. 해당 commit을 재사용하고, 다른 product worker를 dispatch하거나 product commit을 추가로 만들지 않는다. 자연어 routing은 이 skill의 local preview만 시작하며 publication을 의미하지 않는다. 일반적인 PR 질문, code review, implementation request, merge request, multi-PR maintenance request, 또는 기존 `.tigerkit` artifact만으로는 절대 활성화하지 않는다.

하나의 pull-request draft와 bounded publication plan을 소유한다. local Git/GitHub state를 inspect하고 `.tigerkit/pr-open.md`를 작성할 수 있다. 아래 approval gate 전에는 product code 수정, product commit 생성, merge, tag, release, publish를 하지 않는다.

## 작업 흐름

1. 실행 repository, authenticated GitHub identity, current branch, `HEAD`, dirty paths, base branch, 해당 branch의 existing PR을 확인한다.
2. intended commits가 존재하는지, unrelated dirty paths가 보존되는지, proposed PR이 existing PR을 중복하지 않는지 검증한다.
3. 요청 또는 Ready contract에서 `PR evidence: required | optional | N/A`를 받는다. `required`를 `evidence_required: true`로 매핑하고, `tk-browser-verify` 또는 `tk-prototype`의 유효한 screenshot handoff만 수집한다. `optional`이면 approved plan에 명시적으로 포함된 evidence만 upload하고, `N/A`이면 uploader를 호출하지 않는다. plan에 producer, absolute evidence directory, screenshot paths, actual inspection, criterion을 기록한다. 값이 없으면 한 가지 추천과 함께 `PR evidence: undecided`를 표시하고 publication approval 전에 decision을 받는다. 임의의 screenshot이나 browser verification만으로 required evidence를 추론하지 않는다.
4. exact title, body, base/head refs, push refspec, evidence state, known exclusions를 `.tigerkit/pr-open.md`에 작성한다. PR을 업데이트할 때 existing body sections, checklists, attachments, user-authored notes를 보존한다.

계획은 다음 필드를 빠짐없이 채운다. 값은 실제 검증 결과로 교체하며, `Push refspec`은 승인 후 그대로 실행할 명령의 source와 destination을 함께 적는다.

```text
Repository: <owner/repo>
PR operation: create | update #<number>
Base: <base-branch>
Head: <head-branch>@<head-sha>
Push refspec: <remote> <head-branch>:<head-branch>
Title: <exact-title>
Body: <exact-body>
PR evidence: required | optional | N/A
Evidence producer: <tk-browser-verify | tk-prototype | N/A>
Evidence directory: <absolute-path | N/A>
Evidence paths: <absolute-paths | N/A>
Known exclusions: <none | exact exclusions>
```

승인된 `Push refspec`의 실행 형태는 `git push <remote> <head-branch>:<head-branch>`이며, 실제 값이 branch·`HEAD` 재검증 결과와 다르면 실행하지 않는다.
5. approval request 전에 다음 순서로 preview를 보여준다: included changes; exact PR title/body; base/head와 check/evidence state; exclusions/risks; one publish recommendation. refspec, identity, provenance는 decision-relevant하지 않으면 artifact에 남긴다. approval question은 하나만 하고 `Pending`으로 멈춘다. 일반적인 “go ahead”는 다른 plan이나 stale plan을 승인하지 않는다.
6. current-turn approval 후 branch, `HEAD`, PR identity, open state를 다시 확인한다. explicit refspec만 push하고, 지정된 PR만 create/update한다. required evidence가 유효하면 PR이 존재한 뒤 `tk-github-image-upload-to-pr`로 handoff한다.
7. remote PR을 다시 읽고 URL, head SHA, operation result, evidence state, remaining checks를 보고한다. required evidence가 없거나 upload가 실패하면 PR result는 유지하되 final completion은 `Blocked`로 반환한다. merge하거나 release를 요청하지 않는다.

## 🔴 CHECKPOINT / STOP · 발행 게이트(Publication gate)

Plan에는 repository, PR/create target, base branch, head branch, exact push refspec, title, body, evidence requirement/state, operation order, exclusions를 명시해야 한다.

| Trigger | First action | If unresolved |
|---|---|---|
| exact current-turn approval 대기 | Make no remote write | `Pending` |
| Branch/PR head, identity, dirty paths, body, target가 변경됨 | Invalidate approval; refresh plan | `Blocked` |
| Required Git 또는 GitHub evidence를 사용할 수 없음 | Record attempted check/evidence gap | `Unverifiable` |
| Push, create, update가 실패하거나 plan 일부만 적용됨 | Reread remote PR; report exact applied state | `Fail` |
| PR 생성 후 required upload가 없거나 실패함 | Keep PR; report evidence recovery condition | `Blocked` |
| Requested PR operation과 required evidence가 검증됨 | Report fresh URL and head SHA | `Pass` |

`## PR open`으로 시작하고 user-relevant state, verification, remaining risks만 보여준다. full provenance는 `.tigerkit/pr-open.md`에 보관한다.
