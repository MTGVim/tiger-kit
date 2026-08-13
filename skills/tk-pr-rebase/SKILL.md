---
name: tk-pr-rebase
description: "[user/auto] 하나의 `open` GitHub `pull request`를 정확한 최신 `base`로 `rebase`하고 `conflict`를 해결한 뒤, `standalone` 승인 또는 `active` `Sweep`의 `bounded authority`로 검증된 `force-with-lease publication`을 수행합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 하나의 PR 리베이스

`/tk-pr-rebase`, `$tk-pr-rebase`, 호스트 스킬 선택기, 또는 활성 `tk-pr-sweep`의 정확한 `PR handoff`로만 시작합니다.
일반 브랜치 `rebase`, 단순 `conflict marker edit`, 리뷰 응답에는 자동 적용하지 않습니다.

한 PR의 정확한 `base/head rebase`, `conflict resolution`, `verification`, 제한된 `force-with-lease`를 소유합니다.
`merge`, `close`, `tag`, `release`, 무관한 피드백 구현은 하지 않습니다.

## Fresh identity

시작할 때 다음을 fresh-read합니다.

- repository와 authenticated identity
- open PR number
- head repository/ref/SHA
- base repository/ref/SHA
- local branch/HEAD/worktree
- active Git operation
- review/thread/check 상태

identity/ownership이 모호하거나 fork publication boundary가 안전하게 입증되지 않으면 mutation 전에 `Blocked`입니다.

exact remote head와 latest base를 fetch하고 다음을 고정합니다.

```text
old_head
base_sha
full head ref
remote
expected force-with-lease
```

local `HEAD == old_head`, remote PR head `== old_head`, clean worktree를 요구합니다.

## Rebase와 conflict

정확한 `base_sha` 위로 rebase합니다.
conflict가 나면 `tk-merge-conflict`의 intent/index/marker/verification contract를 적용합니다.
semantic ambiguity를 임의 선택하지 않습니다.

rebase 뒤에는 다음을 검증합니다.

- Git operation 종료
- worktree/index clean
- `base_sha`가 새 HEAD의 ancestor
- intended commit/diff 보존
- relevant tests/checks 통과

rewrite가 필요 없으면 force-push하지 않습니다.

## Standalone publication

명시적 standalone invocation은 local rebase까지만 자동 권한을 줍니다.
remote publication 전에는 `.tigerkit/pr-rebase.md`에 exact PR/base/head, old/new SHA,
verification, exact lease/refspec, reply/thread action, exclusions를 기록하고 reread합니다.

사용자에게는 전체 ledger를 읽으라고 던지지 말고, 무엇이 바뀌었고 어떤 검증을 했으며
어떤 exact publication을 하려는지 자연스럽게 요약한 뒤 현재 턴 승인 하나를 받습니다.

승인 뒤 remote write 직전에 repository/identity/open state/base/head/refspec/lease를 다시 확인합니다.
하나라도 material drift면 승인을 무효화합니다.

publish는 exact `--force-with-lease=<full-head-ref>:<old_head>`만 허용합니다.
plain `--force`는 금지합니다.

## Sweep 아래에서 실행

활성 `tk-pr-sweep`이 exact repository/PR/base/head와 rebase route를 이미 승인했다면 publication 질문을 반복하지 않습니다.

Sweep child는 `.tigerkit/pr-sweep.md`나 `.tigerkit/pr-rebase.md`를 만들지 않습니다.
parent에 다음 compact evidence만 반환합니다.

- repository/PR
- consumed `base_sha` / `old_head`
- verified `new_head`
- tests/checks
- exact lease/refspec
- remaining conflict/finding
- status

child가 실행되기 직전 exact PR/base/head를 다시 확인합니다.
parent 승인 뒤 head/base가 material하게 변했으면 해당 PR만 `Blocked`로 parent에 반환합니다.

## Publication 후

remote PR head가 `new_head`인지 확인합니다.
rebase로 실제 충족된 review thread만 reply/resolve할 수 있습니다.
모든 thread/review/check를 fresh-read하고 unresolved finding을 완료로 숨기지 않습니다.

필요한 경우 기존 human reviewer에게 재검토를 요청할 수 있지만 author, authenticated user, bot, 여전히 유효한 approver는 제외합니다.
생성 GitHub comment는 `_🤖 본 코멘트는 AI가 작성했습니다._`로 끝냅니다.

## 상태

| 상태 | 의미 |
| --- | --- |
| `Pass` | exact rebase와 필요한 publication이 fresh evidence로 확인됨 |
| `Pending` | standalone publication 승인을 기다림 |
| `Blocked` | identity, authority, semantic conflict, freshness가 안전하게 닫히지 않음 |
| `Unverifiable` | 필요한 Git/GitHub evidence를 읽을 수 없음 |
| `Fail` | 일부 local/remote operation이 실패했고 적용 상태를 정확히 보고해야 함 |

관찰하지 않은 reply/resolve/review/check 상태를 성공으로 주장하지 않습니다.
