---
name: tk-implement
description: "[user] 하나의 fresh Ready ticket과 .tigerkit/implement.md를 검증한 뒤 정확한 범위만 구현하고, 독립 review·검증을 통과할 때만 하나의 commit과 receipt를 만듭니다."
disable-model-invocation: true
argument-hint: "<Ready ticket 또는 tickets.md 경로>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Ready ticket 구현

명시적으로 `/tk-implement` 또는 `$tk-implement` 을 선택한 경우에만 실행한다.
현재 checkout의 repository root를 `git rev-parse --show-toplevel`로 resolve한 뒤
`<repository-root>/.tigerkit/tickets.md` 에서 정확히 하나의 `Status: Ready` ticket과
`<repository-root>/.tigerkit/implement.md` 의 지시를 읽는다. 입력이 없거나 문서가
없으면 `Status: Unverifiable` 로 멈춘다.
Pending, stale, lineage mismatch, unresolved `model`/`effort` 는 각각 정확히
`Status: Blocked` 로 멈추고 변경·stage·commit·receipt를 만들지 않는다.

## 절차

1. ticket의 fresh lineage, exact owned paths, Scope, R/AC, Verification, symbolic
   `model` 과 `effort` 가 모두 resolved인지 확인한다. Delegated 실행이면 `model`을
   spawn 전에 정하고 `general-purpose` implementer의 brief/report path를 준비한다. 구현 전 git status --porcelain=v1과
   .tigerkit/implement.md의 존재·바이트를 snapshot하고, 사용자 변경·index·기존 receipt의 기존 바이트는 byte-for-byte 보존하고
   성공 commit 뒤에만 append한다. owned path 밖은 읽기만 한다.
2. bounded low-risk standalone이면 direct를 추천하고, risk·scope·isolation·fresh
   context가 필요하면 delegated를 사용한다. delegated가 mandatory인 경우 direct로
   조용히 fallback하지 않는다. 어떤 delegated 실행이든 required worker를 dispatch할 수 없으면
   정확히 `Status: Blocked` 로 종료하고 변경·stage·commit·receipt를 만들거나 수정하지 않는다.
   `general-purpose` label은 의도된 worker role이며, 반환 label로 model/tier를
   사후 판정하지 않는다. 구현 후에는 fresh `general-purpose` reviewer가 `Spec
   compliance`와 `Task quality`를 확인하기 전 commit을 성공으로 처리하지 않는다.
3. 구현자는 정확한 owned path만 수정하고 focused checks를 먼저 실행한다.
4. implementer 이상 capability의 독립 reviewer가 `Spec/AC` 및
   `Standards/Style` 을 검사한다. verbatim 또는 style 불일치는 `Blocking` 이다.
5. 검증·review에서 gap이 나오면 매번 bounded fresh corrective worker로 수정하고
   다시 검증한다. 실패하면 `Status: Fail`/`Blocked` 로 종료하며 stage·commit·성공
   receipt를 만들지 않는다.
6. 모든 검증과 review가 성공한 경우에만 현재 branch에 정확히 한 commit을 만들고,
   그 뒤 implement.md에 unit/ticket, changed paths, check/review/gap evidence,
   commit/ancestry, `unresolved: none` receipt를 append한다. push, publish, 다른
   workflow/skill invoke는 금지한다.

출력은 receipt의 absolute path와 `Status: Pass`/`Status: Blocked`/`Status: Fail`/`Status: Unverifiable`만 간결히 보고한다. receipt 내부 evidence를 chat에 복사하지 않는다.
