---
name: tk-pr-respond
description: "[user/auto] 하나의 pull request의 review feedback 또는 지원 가능한 GitHub Actions 실패를 fresh state로 읽고, 자연스러운 해결 계획을 합의한 뒤 필요 시 `seed.md`를 사용해 수정·검증·제한된 publication까지 처리합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 하나의 PR 리뷰 대응

`/tk-pr-respond`, `$tk-pr-respond`, 호스트의 명시적 선택, 또는 활성 `tk-pr-sweep`이 넘긴
정확한 PR 작업에 적용합니다. 일반 코드 수정, 단순 리뷰 요약, 여러 PR 작업에는 적용하지 않습니다.

이 스킬은 하나의 PR에서 현재 feedback을 이해하고, 해결 방향을 사용자에게 자연스럽게 설명하고,
승인된 범위 안에서 수정·검증·push·reply·resolve·필요한 재검토 요청을 수행합니다.

**대화는 자연스럽게, 상태는 엄격하게.**

내부 `apply | reply | defer`, worker 배치, GitHub 상태를 그대로 보고서처럼 노출하지 않습니다.
사용자가 알아야 하는 것은 “리뷰가 무엇을 뜻하는지, 어떻게 대응할지, 왜 그 방법인지, 무엇을 검증할지”입니다.

## Fresh state

시작할 때 정확히 하나의 open PR을 fresh-read합니다.

- repository와 authenticated identity
- PR author, base/head ref와 SHA
- checks와 실패한 GitHub Actions 근거
- reviews, inline thread, conversation comment
- unresolved thread
- requested reviewer
- 정확한 push 대상

필요한 pagination을 끝까지 읽습니다. cached 목록이나 이전 Markdown 장부를 현재 truth로 사용하지 않습니다.
identity, exact PR/head, remote authority가 모호하면 mutation 전에 `Blocked`로 멈춥니다.

## Feedback 이해

현재 feedback을 내부적으로 다음 의미로 분류할 수 있습니다.

- 코드 변경이 필요한 의견
- 코드 변경 없이 근거 있는 답변이 적절한 의견
- 현재 PR 범위를 벗어나거나 추가 결정이 필요한 의견

하지만 사용자에게는 분류 토큰보다 의미를 설명합니다.

예:

```text
리뷰 3건 확인했어요. 첫 번째는 실제 모바일 깨짐이라 수정이 필요합니다.
두 번째는 현재 구현이 이미 요구사항을 만족해서 코드 변경 없이 근거를 설명하는 게 맞아 보여요.
마지막 건은 제품 동작 자체를 바꾸는 의견이라 이것만 확인이 필요합니다.
```

리뷰 문구가 요구 결과를 이미 명시했다면 같은 내용을 다시 질문하지 않습니다.
저장소 근거로 결정 가능한 재사용, 단순화, 테스트, 보안, 사용자 경험 판단은 스스로 조사해 추천과 이유를 설명합니다.

사용자에게 직접 묻는 것은 다음뿐입니다.

- 제품 동작이나 범위를 실제로 바꾸는 사용자 소유 결정
- 보안·권한·데이터·호환성처럼 위험하거나 되돌리기 어려운 결정
- 충분히 개선했지만 검증 준비도를 더 높일 수 없는 예외 승인

## 해결 계획과 승인

mutation 전에는 현재 feedback에 대한 해결 계획을 자연스럽게 설명합니다.

최소 의미:

- 어떤 feedback을 수정하고 어떤 것은 답변만 할지
- 구현 접근과 재사용할 기존 코드
- 불필요한 복잡성을 피하는 방법
- 회귀/신규 테스트 계획
- 보안·사용자 경험에서 특별히 확인할 점
- browser-visible이면 `tk-browser-verify` 계획
- push/reply/resolve/re-review의 bounded publication 범위
- 실행 형태와 모델 수준에 대한 추천

모델 추천은 “중간급 coding model”, “더 강한 final review”, “독립 작업 fan-out 권장”처럼
사람 친화적인 조언으로만 표현합니다. provider selector, model class, reasoning effort, `session.md`를 만들지 않습니다.
이 기능이 없다고 작업을 `Blocked` 처리하지 않습니다.

현재 계획에 대한 사용자 승인 하나를 받습니다. 같은 계획의 publication을 별도 두 번째 질문으로 쪼개지 않습니다.
다만 승인 후 PR head/thread/check/identity가 material하게 변하면 기존 승인을 무효화하고 달라진 내용만 다시 설명합니다.

## 코드 변경과 Seed

코드 변경이 필요한 Respond 작업은 해당 checkout/worktree의 `.tigerkit/seed.md`를 현재 작업 계약으로 사용합니다.
`pr-respond.md` lifecycle 장부는 만들지 않습니다.

Seed에는 최소한 다음 PR 맥락이 들어갑니다.

- exact repository/PR/head
- 처리 대상 feedback과 reviewer가 요구한 결과
- 코드 변경/답변/보류에 대한 확정 판단
- 작업 배경과 목적
- 범위와 변경 금지 사항
- 사용자 결정
- 구현 접근과 repository evidence
- Reuse / Simplicity / Tests / Security / Experience 판단
- acceptance criteria와 각 verification path
- browser verification plan
- publication boundary
- lower-capability executor에게 필요한 구현 안내

이미 활성 Ready Seed가 같은 PR 작업과 정확히 일치하면 재작성하거나 같은 결정을 다시 묻지 않습니다.
새 feedback이나 fresh state가 Seed의 goal/scope/decision/AC를 material하게 바꾸면 `Pending`으로 다시 열고 해당 부분만 재승인합니다.

코드 변경 없이 reply만 하는 경우에는 새 Seed를 만들 필요가 없습니다.

## 실행

승인 뒤 현재 호스트가 제공하는 안전한 방식으로 실행합니다.

- 독립 작업과 안전한 격리가 있으면 subagent fan-out을 사용할 수 있습니다.
- 격리가 없으면 순차 실행합니다.
- 특정 모델 선택이 불가능하면 host default를 사용합니다.
- parent가 실행 세부사항을 Markdown routing state로 영속화하지 않습니다.

각 구현자는 Ready Seed와 자기 책임 범위를 읽습니다. parent가 전체 대화나 세부 계획을 다시 복사하지 않습니다.

필수 순서:

```text
implementation
→ focused tests/checks
→ acceptance 기준 review
→ browser-visible이면 tk-browser-verify
→ 필요한 gap correction
→ verified commit
```

browser 검증에 개발 서버가 필요하면 `tk-browser-verify`에 정확한 command/cwd/URL/auth/readiness를 넘기고,
서버 시작·준비 확인·정리는 verifier가 소유합니다.

같은 실패를 무한 반복하지 않습니다. 3회의 유의미한 corrective attempt 뒤에도 같은 blocker가 남으면
남은 증거와 함께 `Fail` 또는 `Unverifiable`로 멈춥니다.

## Publication

remote write 직전에 exact repository, authenticated identity, open PR, fresh remote head,
local ancestry, thread/check 상태와 승인 범위를 다시 확인합니다.

그 뒤 승인된 범위만 다음 순서로 처리합니다.

1. 검증된 commit을 exact branch로 push합니다.
2. 각 feedback에 정확한 reply를 게시합니다.
3. reply가 성공하고 해결이 실제로 검증된 thread만 resolve합니다.
4. reviews/threads/checks를 fresh-read합니다.
5. 필요한 사람 reviewer에게만 재검토를 요청합니다.
6. PR 수준 summary comment는 최대 하나만 작성합니다.

unresolved inline thread가 하나라도 남으면 완료로 주장하지 않습니다.
deferred, unverifiable, failed feedback은 open으로 유지합니다.

모든 생성 GitHub comment는 `_🤖 본 코멘트는 AI가 작성했습니다._`로 끝냅니다.
merge, close, tag, release, plain force push, unrelated thread resolve는 하지 않습니다.

## Sweep 아래에서 실행

활성 `tk-pr-sweep`에서 넘어온 exact PR이면 parent가 이미 승인받은 material decision을 다시 묻지 않습니다.
child는 PR fresh state와 parent-approved scope를 확인하고, 같으면 바로 진행합니다.

새 feedback/head drift가 승인 범위를 material하게 바꾸면 그 PR만 parent에 다시 올립니다.
`pr-sweep.md`, `pr-respond.md`, worker receipt Markdown을 만들지 않습니다.
코드 변경 PR이면 해당 isolated worktree의 `seed.md`만 task context로 사용할 수 있습니다.

## 완료 응답

정상 protocol receipt를 출력하지 않습니다.

예:

```text
리뷰 3건 처리했습니다. 2건은 코드 수정 후 검증했고 1건은 근거를 설명해 답변했습니다.
모바일 변경은 browser verification까지 통과했고 관련 thread는 모두 resolve됐어요.
이제 reviewer 재확인만 기다리면 됩니다.
```

문제가 남은 경우에만 해당 blocker와 다음 행동을 자세히 설명합니다.
마지막 상태는 실제 결과에 따라 `Status: Pass | Pending | Blocked | Unverifiable | Fail` 중 하나만 사용합니다.
