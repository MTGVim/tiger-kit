---
name: tk-pr-sweep
description: "[user] 설정된 repository들의 open pull request를 deterministic fresh triage로 읽고, 지금 처리할 일과 기다릴 일을 자연스럽게 브리핑한 뒤 한 번 승인된 범위에서 bounded multi-PR maintenance를 수행합니다."
disable-model-invocation: true
argument-hint: "[--report] [--recover-publication] [--repo <owner/name>]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 여러 PR 정리

명시적으로 `/tk-pr-sweep`, `$tk-pr-sweep`, 또는 호스트 스킬 선택으로만 시작합니다.
일반적인 “열린 PR 정리해줘”, 한 PR 리뷰 대응, 일반 CI 수정에는 자동 적용하지 않습니다.

Sweep는 여러 PR의 **fresh 상태를 읽고 정리하는 controller**입니다.
장기 작업 상태를 Markdown ledger로 복제하지 않습니다. GitHub와 Git의 현재 상태가 truth입니다.

**대화는 자연스럽게, 상태는 엄격하게.**

사용자에게 `actionable`, `held`, backend, routing state, worker receipt를 기본 출력하지 않습니다.
대신 “지금 할 것 / 기다릴 것 / 왜 그런지 / 어떻게 처리할지”를 사람이 이해하기 쉽게 브리핑합니다.

## 대상 repository

기본 repository 범위는 다음 user-level 설정을 사용합니다.

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

이 설정은 장기간 유지되는 repository 목록만 소유합니다.
model mapping, selector, effort, worker routing, fan-out preference, task state는 저장하지 않습니다.

설정이 없으면 현재 checkout의 origin을 안전하게 확인할 수 있을 때만 bootstrap할 수 있습니다.
명시적 `--repo owner/name`은 해당 실행의 범위를 제한합니다.

## Deterministic triage

`skills/tk-pr-sweep/scripts/triage.mjs`를 canonical fresh inventory로 사용합니다.

최소 확인 대상:

- open PR
- author / requested review
- exact base/head와 SHA
- mergeability/conflict
- GitHub Actions와 외부 check 구분
- review decision
- unresolved review thread
- 최신 actionable feedback과 author response

cached user supplied list나 이전 `.tigerkit/pr-sweep.md`를 current truth로 사용하지 않습니다.

## `--report`

`--report`는 순수 읽기 전용입니다.

예:

```text
지금 처리할 PR은 3개예요.
#121 — 리뷰 대응 필요
#124 — GitHub Actions 수정 필요
#128 — rebase 필요

#130, #132는 사람 리뷰 대기이고 #135는 외부 CI 대기라 지금 손댈 필요 없습니다.
```

기본 출력은 짧은 briefing입니다. lifecycle Markdown, Seed, worktree, commit, push, reply, resolve를 만들지 않습니다.
실패한 repository가 있으면 성공한 repository 결과와 분리해 어떤 상태를 읽지 못했는지 설명합니다.

## 실행 계획

실행 모드에서는 fresh triage를 바탕으로 지금 처리 가능한 PR만 계획합니다.

각 PR에 대해 사용자가 이해해야 할 수준으로 설명합니다.

- 왜 지금 처리 가능한지
- 어떤 종류의 작업인지
- 코드 변경이 필요한지
- 필요한 검증
- 위험하거나 사용자 결정이 필요한지
- 서로 독립적인지

예:

```text
PR 8개를 봤는데 지금 손댈 건 4개예요.
#121은 리뷰 수정, #124는 repository-caused Actions 실패, #128은 rebase,
#130은 코드 변경 없이 답변만 하면 됩니다.

#121/#124는 서로 독립적이라 격리된 subagent 병렬 처리가 가능하고,
#128은 별도 rebase로 두는 걸 추천해요. 끝나면 전체 상태를 다시 확인하겠습니다.
```

실행 모델은 “중간급 coding model”, “충돌은 더 강한 reasoning model” 같은 recommendation만 할 수 있습니다.
구체 provider selector, tier, reasoning effort, `session.md`를 만들지 않습니다.
이 제어를 사용할 수 없다는 이유로 전체 Sweep을 `Blocked` 처리하지 않습니다.

사용자가 batch 계획을 한 번 승인하면 그 exact PR/head/작업 유형/publication 범위에 대한 authority가 생깁니다.
child마다 같은 내용을 다시 승인받지 않습니다.

## 실행 격리

여러 PR을 동시에 변경하려면 checkout isolation이 입증되어야 합니다.
호스트가 isolated worktree/subagent를 제공하면 사용할 수 있습니다.
안전한 병렬 격리가 없으면 PR을 순차 처리합니다.

한 PR을 안전하게 현재 checkout에 결속할 수 없는 경우 그 PR만 hold하고 다른 독립 PR을 계속할 수 있습니다.
worker/model control 부재 자체는 blocker가 아닙니다.

## PR별 처리

각 PR을 실제 처리하기 직전에 fresh triage와 exact PR state를 다시 읽습니다.

대표 route:

- review feedback / repository-caused GitHub Actions → `tk-pr-respond` 절차
- merge conflict / base drift → `tk-pr-rebase` 절차
- 외부 CI, queued/flaky/infrastructure, 사람 리뷰 대기 → 지금은 기다림
- 지원하지 않는 상태 → report-only

parent가 승인한 exact PR/head와 해결 방향이 그대로면 child가 같은 결정을 다시 묻지 않습니다.
새 feedback, head drift, scope 변화처럼 material하게 달라졌을 때만 해당 PR을 사용자에게 다시 올립니다.

## PR별 Seed

Sweep 전체를 하나의 giant Seed로 만들지 않습니다.

코드 변경이 필요한 각 PR은 자기 isolated checkout/worktree의 `.tigerkit/seed.md`를 사용할 수 있습니다.
그 Seed는 해당 PR의 feedback, 목적, 결정, 접근, AC, verification, publication boundary를 self-contained하게 담습니다.

reply-only나 순수 rebase처럼 별도 구현 context가 필요하지 않은 작업에는 억지로 Seed를 만들지 않습니다.

`pr-sweep.md`, `pr-respond.md`, worker receipt Markdown은 만들지 않습니다.

## Publication

각 child의 remote write 전 exact repository/PR/head/identity/refspec/thread/check를 fresh-read합니다.
parent 승인 범위 안의 push/reply/resolve/re-review만 허용합니다.

일부 publication이 permission 문제로 차단되면 이미 검증된 local commit과 exact remote state를 보존해 보고합니다.
같은 실행에서 exact target과 refspec을 다시 검증할 수 있으면 안전하게 재시도할 수 있습니다.
별도 세션의 `--recover-publication`은 local commit/remote head/approved target을 fresh evidence로 재구성할 수 있을 때만 허용하며,
그렇지 않으면 `Unverifiable`로 멈춥니다. plain force나 추정 refspec은 사용하지 않습니다.

## Queue 진행

한 PR의 local failure가 다른 독립 PR을 자동 중단시키지 않습니다.
다만 identity/권한 오염, repository 범위 불명확, triage 자체 신뢰 불가처럼 systemic failure면 전체 Sweep을 중단합니다.

각 PR 성공/실패 뒤 그 PR을 다시 triage하여 실제 상태가 바뀌었는지 확인합니다.
모든 planned row가 끝나면 configured repositories 전체를 final fresh triage합니다.

## 완료 응답

내부 category/receipt를 덤프하지 않습니다.

예:

```text
이번 Sweep에서는 4개 중 3개를 처리했습니다.
#121과 #124는 수정·검증·push 완료, #130은 답변 완료입니다.
#128은 새 conflict가 확인돼 보류했고, 나머지는 사람/외부 CI 대기 상태입니다.
```

정상 처리 항목은 짧게, 문제 있는 PR만 필요한 만큼 자세히 설명합니다.
마지막 상태는 실제 결과에 따라 `Status: Pass | Pending | Blocked | Unverifiable | Fail` 중 하나만 사용합니다.
