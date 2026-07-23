---
name: tk-drive
description: "[user/auto] 명시적 $tk-drive로 시작한 source-to-verified-commit workflow를 진행하거나, 같은 대화에서 이 skill이 남긴 pending decision의 답변 직후 재개할 때만 사용합니다. ordinary 구현·generic continue·artifact 존재만으로는 시작하지 않습니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 드라이브

새 workflow는 명시적 `$tk-drive` 호출만 시작합니다. 유일한 implicit positive는 같은 대화에서 활성 drive가 직전에 남긴 pending decision 하나에 사용자가 답한 경우입니다. 답변을 반영하고 blocker가 없으면 재호출이나 추가 승인 없이 다음 phase로 계속하세요.

Ordinary code request, generic `계속`, 기존 `.tigerkit/` artifact, 다른 질문의 답변, 새 세션 또는 끊긴 대화는 implicit start/resume가 아닙니다. 새 세션에서는 사용자가 `$tk-drive`를 다시 호출한 뒤 repository evidence로 phase를 재구성하세요.

## 계약

명시 호출은 현재 source 범위의 계획, 구현, 검증, 내장 review와 검증된 current-branch commit 하나를 승인합니다. Push, PR, merge, tag, release, publish, 자동 reflection 또는 범위 밖 mutation은 승인하지 않습니다.

현재 명시 source가 기존 scratch artifact보다 우선합니다. 관련 없는 artifact는 무시하고, 같은 작업의 stale spec/tickets는 current evidence로 재검증하세요. 작업 정체성이나 decision reversal이 불명확할 때만 질문합니다. Drive 전용 state, current pointer, archive, global state 또는 자동 migration을 만들지 마세요.

모든 phase는 [phase invariants](references/phases.md)를 따릅니다. Sibling skill body나 shared runtime contract를 읽거나 복제하지 마세요. 자동 nested-skill allowlist는 `tk-prototype | tk-browser-verify | tk-merge-conflict`로 닫고 그 밖의 planning, learning, reflection 또는 handoff skill을 호출하지 마세요.

## Workflow

1. `preflight`: source, relevant spec/tickets, repository instructions, branch, initial `HEAD`, dirty ownership과 drift를 읽고 task identity·완료 phase·미결정을 출력합니다.
2. `inline grill gate`: blocking ambiguity가 있을 때만 evidence, 권고안, 질문 하나를 제시하고 downstream mutation 전에 `pending`으로 멈춥니다.
3. `spec phase`: confirmed decision과 source traceability로 Ready spec을 작성·재검증하거나 이미 유효한 Ready spec을 채택합니다.
4. `ticket decision`: 독립 검증 가능한 vertical slice가 2개 이상이거나 long-resume 관리 가치가 있을 때만 tickets ledger를 작성합니다. 그 외에는 spec에서 바로 구현합니다.
5. `prototype branch`: web visual ambiguity가 evidence로 해소되지 않고 비교가 결정을 줄일 때만 disposable 2–3안으로 질문 하나를 좁힌 뒤 같은 resume gate로 돌아옵니다.
6. `implementation`: 가장 작은 vertical slice를 구현하고 focused verification을 반복합니다. Visible UI/browser behavior에서는 browser 도구나 검증 server 전에 `tk-browser-verify`를 활성화합니다. Ticket이 있으면 한 번에 하나를 `in_progress`로 두고 evidence가 있는 것만 `verified`로 바꿉니다.
7. `verification/review`: 전체 R/AC, candidate/staged inventory, Standards/Spec 축과 drift를 확인하고 조건부 independent reviewer를 최대 한 명만 사용합니다.
8. `commit/report`: 모든 범위가 verified일 때 소유 diff만 stage하여 최종 commit 하나를 만들고 receipt를 출력합니다.

## 🔴 CHECKPOINT · 🛑 STOP · Pending decision과 재개

질문은 blocking ambiguity 하나만 다루고 `Evidence`, `Recommendation`, `Question`을 각각 한 번만 출력하세요. Exhaustive interview를 시작하거나 `tk-grill-me`를 호출하지 마세요. 답변 전에는 source/spec downstream mutation을 하지 않습니다.

답변이 pending decision에 직접 대응하면 decision과 source traceability를 갱신하고 다음 phase로 자동 진행하세요. 답변이 새 scope를 추가하거나 pending decision과 대응하지 않으면 commit 권한을 승계하지 말고 drift를 구체적으로 보고하거나 새 명시 `$tk-drive` 호출을 요청하세요.

## 실패와 완료

| Trigger | Immediate action | Fallback / stop |
|---|---|---|
| 변경 관련 검증 실패 | `Fail`로 표시하고 유효한 source diff는 rollback하지 않은 채 uncommitted로 보존 | 이번 실행이 소유한 temporary artifact만 정리하고 실패 evidence를 보고하며 commit하지 않음 |
| 필요한 입력·권한·결정 부재 | 누락 항목을 특정하고 `Blocked`로 멈춤 | downstream mutation과 commit을 하지 않음 |
| 실행했지만 evidence를 확보하지 못함 | 실행 결과와 evidence gap을 분리해 `Unverifiable`로 표시 | 검증된 것으로 승격하거나 commit하지 않음 |

Final receipt는 `Status`, `Source`, `Phases`, `Tickets`, `Verification`, `Review`, `Commit`, `Remaining risks`, `Reusable candidate`를 소유합니다. `Reusable candidate`는 존재 여부만 알리고 `tk-reflect`를 자동 실행하지 않습니다. 같은 evidence를 여러 섹션에 복사하지 마세요.

## DO NOT / ANTI-PATTERNS

- 명시 start 없이 ordinary 요청·artifact·generic continue로 workflow를 시작하지 마세요.
- pending decision과 무관한 답변에 commit 권한을 이어 붙이지 마세요.
- 작은 single-slice 작업에 tickets를 강제하거나 stale ticket status를 그대로 신뢰하지 마세요.
- phase마다 commit하거나 partial failure에서 valid diff를 되돌리지 마세요.
- allowlist 밖 skill, nested delegation, 자동 reflect/handoff/learn을 실행하지 마세요.
