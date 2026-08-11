---
name: tk-pr-rebase
description: "[user/auto] 하나의 open GitHub pull request를 정확한 최신 base로 rebase하고, conflict를 해결하고, 승인된 또는 sweep-owned force-with-lease authority로 검증 후 publish합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# `pull request` 리베이스

`/tk-pr-rebase`, `$tk-pr-rebase`, 또는 호스트 `skill picker`를 통해서만 시작한다.
일반적인 rebase, 브랜치 업데이트, 충돌, 리뷰 응답, 계속 작업에는 절대 활성화하지
않는다. 유일한 자동 진입은 활성 `tk-pr-sweep`의 새 정확한 PR `handoff`다.

하나의 PR에 대한 로컬 rebase, 제한된 force-with-lease 발행, rebase로 충족된
리뷰 답변과 스레드 해결, rebase 요약, 조건부 사람 리뷰 재요청을 소유한다.
독립 실행은 `.tigerkit/pr-rebase.md` 를 소유하고, Sweep CI는 하위 Markdown
장부를 작성하지 않으며 간결한 증거를 `.tigerkit/pr-sweep.md` 에 반환한다.
관련 없는 feedback을 구현하거나 merge, close, tag, release를 수행하거나 저장소
규칙을 바꾸지 않는다.

## 모드

- **Normal:** 명시적 `invocation`은 로컬 rebase만 승인한다. 발행 질문은 아래에
  둔다.
- **Sweep CI:** `--ci` 에는 정확한 저장소, PR, base/head 참조와 SHA, 경로 시도,
  새로 격리된 worker/specialist dispatch를 고정한 활성 `tk-pr-sweep`
  `handoff`가 필요하다. Sweep 계획 승인 이후에는 `handoff`가 별도 질문 없이
  제한된 rebase/충돌 해결과 발행을 허용한다. 의미 충돌의 모호함 또는 dispatch
  격리 누락은 `Blocked` 로 남는다.

## 작업 흐름

1. 정확히 하나의 공개 PR, 저장소, 인증된 identity, 작성자, head
   repository/ref/SHA, base repository/ref/SHA, 로컬 브랜치, 변경 경로, 활성
   Git operation, 검사, 리뷰, 댓글, 요청된 reviewer를 확정한다. 모호함,
   identity/소유권 불일치, 안전하지 않은 fork 대상, 또는 이 계획이 만들지 않은
   operation이면 중지한다.
2. 정확한 원격 head와 최신 base를 fetch한다. `old_head`, `base_sha`, 현재
   review/thread 상태, 기존 요청 reviewer를 고정한다. 깨끗한 worktree,
   관련 없는 staged 경로 없음, 로컬 `HEAD == old_head`, 원격 PR head
   `== old_head` 를 요구한다.
3. findings를 분류한다. PR을 고정된 base로 업데이트해 요청된 결과를
   충족할 때만 thread를 닫는다. 관련 없음, 보류, 대체 여부가 불확실함,
   `unverified`인 finding은 열린 상태로 유지한다.
4. 브랜치를 정확한 `base_sha` 위로 rebase한다. Normal `invocation`은 로컬
   rebase만 승인하며 abort, reset, push, 댓글 발행은 승인하지 않는다. 각 충돌
   반복에는 sibling skill을 호출하지 않고 `tk-merge-conflict` 계약을 자체 적용하며,
   operation, intent, index, marker, 검증 게이트가 통과한 뒤에만 재개한다. Sweep
   CI에서는 정확히 승인된 유지보수 rebase `handoff`가 검증된 결과를 발행할 수
   있지만, 절대 추측하거나 자동 abort하지 않는다.
5. rebase가 끝났는지, worktree와 index가 깨끗한지, `base_sha`가 새 `HEAD`의
   ancestor인지, 의도한 commit과 diff가 유지되는지, 관련 test/check가
   통과하는지 검증한다. 브랜치가 이미 `base_sha`를 포함해 rewrite가 필요 없으면
   force-push하지 않는다.
6. Normal 모드에서는 먼저 `.tigerkit/pr-rebase.md` 에 고정된 refs와 SHA,
   검증, 정확한 `--force-with-lease` 예상값/refspec, 모든 외부 답변, thread
   조치, 의도적으로 열린 finding, 요약, 기존 사람 reviewer, 일반 및 reviewer
   언급 대체 본문, 제외 사항을 전체 계획으로 기록한다. 같은 디렉터리의 임시
   파일로 원자적으로 교체한 뒤 다시 읽어 저장된 내용과 대상 PR/base/head를
   검증한다. 저장 또는 재읽기가 실패하면 발행 체크포인트로 진행하지 않고
   `Blocked` 로 멈춘다.
   Sweep CI에서는 Markdown 장부를 작성하지 않고 이 간결한 사실을 상위 실행에
   반환한다. URL이 있으면 사용자 출력의 PR 및 review/thread 참조를 클릭 가능한
   Markdown 링크로 렌더링한다. 표시 전에 GitHub의 `<br>`/`<br/>` 줄바꿈을
   실제 개행으로 정규화한다. 모든 외부 reply/comment는
   `_🤖 본 코멘트는 AI가 작성했습니다._` 로 끝낸다.
   Normal 장부는 작업 `Status` 와 별도로 `Disposition: reported | applied | pending` 을
   저장한다. 원자적 쓰기/재읽기가 현재 대상과 일치하면 `Disposition: applied`여도
   발행 전 작업 `Status: Pending` 은 유지한다. 누락/오래됨/재읽기 불일치면
   `Status: Blocked`, `Disposition: pending` 으로 멈추고 발행, 답변, 해결,
   재검토를 수행하지 않는다.
7. Normal 모드의 채팅 출력은 산출물 우선의 간결한 보고만 사용한다. 반드시
   절대 산출물 경로, `Status`, `Disposition`, 대상 PR/base/head, 답변/조치 개수,
   `Recommendation`, 단 하나의 발행 질문만 표시한다. 정확한 외부 답변/조치
   본문, 대체 본문, 전체 작업 계획은 채팅에 복사하지 않는다.
   사용자는 표시된 산출물을 열어 정확한 리터럴을 검토한다. 산출물 경로와
   짧은 상태 보고 외에 전체 계획을 먼저 채팅에 덤프하지 않는다. 발행 질문은
   하나만 하고 `Pending` 으로 멈춘다.

### 🔴 체크포인트 / 중지 · 발행 승인

`🔴 CHECKPOINT` 에서 산출물 경로와 `Status`, `Disposition`, 대상 PR/base/head, 검증,
답변/조치 개수, `Recommendation`, 단 하나의 발행 질문을 보여준다. 정확한 답변,
thread 조치, 재검토 후보, 작업 순서와 위험은 `.tigerkit/pr-rebase.md` 에서만
소유한다. 사용자는 산출물을 열어 정확한 리터럴을 검토한다. 사용자의 정확한
현재 턴 승인 전에는 push, 답변, thread 해결, 재검토 요청 또는 요약을 수행하지
않는다. 로컬 rebase는 Normal 모드의 로컬 전용 권한 안에서만 허용한다.

`🛑 STOP` — 승인이 없으면 `Pending` 으로 멈춘다. 승인 뒤 고정된 branch, head,
base, identity, 변경 경로, review 또는 thread에 드리프트가 생기면 다시 쓰지 말고
갱신된 계획과 함께 `Blocked` 를 반환한다. Sweep CI는 정확히 승인된 `handoff`가
있을 때만 이 질문을 건너뛴다.

8. 현재 턴 승인 후 모든 고정된 로컬 및 원격 필드를 다시 읽는다. 브랜치, head,
   base, identity, 변경 경로, review, thread 중 하나라도 드리프트하면 승인은
   무효이며, 갱신된 계획과 함께 `Blocked` 를 반환한다.
9. 다음 순서로 publish한다: 정확한
   `--force-with-lease=<full-head-ref>:<old_head>` push, PR이 새 head를 가리키는지
   확인, 승인된 각 reply 게시, 검증하고 성공적으로 답변한 thread만 resolve한다.
   일반 `--force`나 고정되지 않은 lease는 절대 사용하지 않는다.
10. push 후 reviews, 요청된 reviewer, threads, checks, mergeability를 다시 읽는다.
    push 후 리뷰 상태를 관찰하며 오래된 리뷰를 추측해 닫지 않는다. 현재 처리할
    finding, 보류 finding, `unverified` finding이 하나도 없을 때만, feedback이
    처리됐거나 새 head에서 승인이 무효가 된 기존 사람에게 review를 다시 요청한다.
    author, 인증된 사용자, bots, 여전히 유효한 approver는 제외한다. 정식 GitHub
    요청을 우선한다. GitHub가 자격 있는 reviewer를 거부하면 해당 reviewer를
    언급한 승인된 대체 요약을 게시하고 정식 요청이 아닌 `mention fallback`으로
    보고한다. 그 외에는 재검토 결정 후 승인된 일반 rebase 요약을 게시한다.
11. PR을 다시 읽는다. 일부 원격 쓰기는 정확히 보고하며, 관찰하지 않은 답변,
    해결, review request, 검사, mergeable 상태를 주장하지 않는다.

## Sweep CI 모드

1. 하나의 정확한 공개 PR과 사용하지 않은 `(base_sha, old_head)` pair에 대한 새
   active-sweep `handoff`, 그리고 Sweep이 이 경로를 새로 격리된
   worker/specialist로 dispatch했다는 증거를 요구한다. `handoff`가 없거나
   모호하거나 inline/direct-only이거나 권한이 반복되면 rebase 또는 원격
   쓰기 전에 `Blocked` 로 처리하고 controller 실행으로 대체하지 않는다.
2. 일반 identity, 소유권, 깨끗한 worktree, 정확한 base, 충돌, 보존, 검증
   게이트를 실행한다. pair, 검증된 `new_head`, 간결한 검증 증거를
   `.tigerkit/pr-sweep.md` 에 반환하며, `.tigerkit/pr-rebase.md` 또는 다른
   하위 Markdown 장부는 만들지 않는다.
3. 발행 질문만 건너뛴다. push와 이후 모든 원격 쓰기 직전에 고정된 저장소, PR,
   identity, 공개 상태, base 및 head refs와 SHA, remote, 정확한 refspec, lease,
   review 및 thread 대상, 로컬 청결 상태를 다시 읽는다. 드리프트는 `Blocked` 이며,
   예기치 않은 head 위로 lease를 갱신하지 않는다.
4. rewrite가 필요하면 다음 형태로 정확히 한 번 publish한다.
   `git push <remote> <new_head>:<full-head-ref>
   --force-with-lease=<full-head-ref>:<old_head>`. 원격 PR head가 `new_head`와
   같은지 확인한 뒤 이를 이후 답변/thread 쓰기의 기준 head로 사용한다.
   rewrite가 없으면 push하지 않고 관찰된 head를 반환한다.
5. rebase로 충족된 replies, 검증된 thread 해결, 조건부 재검토만 정상 순서로
   적용한다. PR 수준 요약은 `tk-pr-sweep` 에 위임하고, 정확한 초안/자료와
   `summary budget: unused` 를 반환한다. CI 모드에서는 일반 또는
   mention-fallback 요약을 절대 publish하지 않는다. 생성하는 모든 reply는
   정확히 `_🤖 본 코멘트는 AI가 작성했습니다._` 로 끝낸다.
6. 정확한 repository/PR, 소비한 `(base_sha, old_head)` pair, `new_head`, 새
   category 증거, 남은 열린 finding, 기본
   `Pass | Fail | Blocked | Unverifiable` 상태를 active sweep에 반환한다.
   사용자에게 보이는 단계 요약은 작성하지 않으며 집계 출력은 sweep가 소유한다.

## 발행 게이트

계획은 repository, PR, identity, base 및 head refs와 SHA, lease, refspec,
검증, replies, thread 조치, 요약 본문, 재검토 후보, 대체 언급, 순서, 제외
사항을 고정한다. 승인은 해당 계획만 포괄한다. reply가 실패하면 thread는 열린
상태로 남기며, 처리할 finding이 남아 있으면 재검토를 보내지 않는다. 브랜치
보호나 권한 실패를 절대 우회하지 않는다.

요청된 로컬 및 원격 범위가 완료됐음을 관찰한 뒤에만 `Pass` 를 사용한다.
발행 승인 대기는 `Pending`, 안전하지 않은 권한 또는 드리프트는 `Blocked`,
변경 관련 또는 부분 쓰기 실패는 `Fail`, 필수 Git, GitHub, test, review,
thread 증거를 사용할 수 없으면 `Unverifiable` 이다.

## 출력 계약

Normal 모드에서 산출물을 성공적으로 다시 읽은 뒤에만 간결한 보고를 출력한다.
보고의 `Recommendation` 은 산출물의 recommendation과 동일해야 하며, 단일
발행 질문은 사용자의 현재 턴 승인을 묻는 문장 하나여야 한다. 절대 경로는
한국어 조사나 문장부호와 붙이지 않고 code span으로 격리한다. 정확한 외부
텍스트와 전체 provenance는 독립 소유 산출물에 보관하고, Sweep CI에서는 기존
간결한 상위 증거에 보관한다. Sweep CI의 하위 장부, 전체 계획 덤프, 별도 발행
질문은 만들거나 출력하지 않는다.

`## PR rebase` 로 시작한다.
