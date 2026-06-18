---
description: frozen goal/spec과 launch 결과를 대조해 통과·부분통과·실패 verdict와 다음 loop 결정을 생성합니다.
argument-hint: "[review target|--latest] [--against <workflow|spec|handoff|path>] [--print-report]"
---

이 명령은 TigerKit vNext GAP → Launch → Review loop의 review contract를 따릅니다. `/tk:gap --review`는 v7 Contract-based Gap Review compatibility mode로 계속 유지하며, `/tk:review`는 launch 이후 구현 결과를 frozen goal/spec 또는 sealed workflow에 맞춰 검증하는 별도 command입니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:review`는 구현이 frozen goal/spec 또는 latest sealed workflow의 requirements와 verification gate를 실제로 만족했는지 확인하고, 남은 gap·drift·risk를 분리한 뒤 다음 결정을 제안합니다.

```text
review = compare frozen target + observed implementation + verification evidence -> Pass | Partial | Fail
```

## Command surface

- plugin slash invocation은 `/tk:review`입니다.
- `/tk:review`는 기본적으로 current branch scope의 최신 TigerKit artifact를 읽습니다.
- 자연어로 “리뷰해줘”, “검증해줘”, “launch 결과 맞는지 봐줘”처럼 요청해도 이 contract를 따릅니다.
- `/tk:review`는 새 요구사항을 만들거나 launch workflow를 실행하지 않습니다.
- `/tk:gap --review`는 Product/Design Spec 대비 current implementation을 검사하는 v7 compatibility mode입니다. `/tk:review`는 GAP → Launch 이후의 frozen target verification입니다.

## Inputs to inspect

가능한 범위에서 아래를 읽습니다.

- current worktree/workspace root
- current branch key 또는 workspace scope key
- `.claude/tigerkit/global-index.json`
- `.claude/tigerkit/branches/<branch-key>/branch-state.json`
- latest GAP workflow/status: `.claude/tigerkit/branches/<branch-key>/gap/current.md`
- latest launch receipt: `.claude/tigerkit/branches/<branch-key>/launch/current.md`
- explicit `--against` target 또는 명시 path
- latest handoff/current.md에 남은 frozen goal 또는 pending verification
- current git status/diff when git is available
- user-provided review target/context

Missing artifacts are not fatal by themselves. Treat them as review scope evidence or `REVIEW_BLOCKED` reason.

## Review target resolution

우선순위:

1. 명시 `--against <path>` 또는 command argument의 repo-local path
2. latest launch receipt가 참조하는 `workflow_path`
3. latest GAP `gap/current.md`의 sealed `tigerkit-launch-workflow`
4. latest handoff의 `Mission`, `Key Decisions`, `Pending Work`, `Validation`
5. 사용자 메시지의 explicit goal/spec

위 항목이 모두 없으면 `REVIEW_BLOCKED`로 끝내고 필요한 source를 짧게 적습니다.

## Comparison policy

Review는 source와 관측값을 분리합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or source contract
Suggestion = proposed, not confirmed
```

검증 절차:

1. frozen target의 confirmed requirements, non-goals, verification gates를 추출합니다.
2. latest launch receipt가 있으면 task 결과, failed gate, abort code, commit status, reflect trace를 읽습니다.
3. current implementation은 파일, diff, rendered output, command output 등 관측 가능한 evidence로만 평가합니다.
4. claimed closed gap은 해당 requirement와 verification evidence를 모두 대조합니다.
5. scope drift는 workflow/goal 밖 변경, non-goal 침범, 새로운 user-facing surface를 기준으로 분리합니다.
6. 새 source decision이 필요하면 추측하지 않고 `REVIEW_BLOCKED` 또는 `REVIEW_PARTIAL`로 남깁니다.

## Verdict rules

`/tk:review`는 정확히 하나의 최종 상태로 끝납니다.

```text
REVIEW_PASS
- frozen target의 required requirements와 verification gates가 통과했고, blocking drift가 없습니다.

REVIEW_PARTIAL
- 일부 gap은 닫혔지만 remaining gap, failed optional verification, 또는 non-blocking drift가 있습니다.

REVIEW_FAIL
- required requirement, required verification gate, safety rule, 또는 non-goal이 실패했습니다.

REVIEW_BLOCKED
- 검증에 필요한 frozen target, implementation evidence, command capability, 또는 human decision이 없습니다.
```

사용자-facing verdict label은 `Pass`, `Partial`, `Fail`, `Blocked`를 유지할 수 있지만 주변 설명은 한글로 씁니다.

## Safety rules

`/tk:review` must not:

- implementation을 수정합니다.
- `/tk:launch`를 대신 실행합니다.
- sealed workflow가 필요한 구현을 `/tk:gap → /tk:launch` 없이 우회합니다.
- missing requirement를 임의 해석합니다.
- 새 backlog를 confirmed requirement로 승격합니다.
- verification 없이 `REVIEW_PASS`를 선언합니다.
- commit, push, PR, merge, release, deploy, GitHub issue write 같은 외부 side effect를 수행합니다.
- `/tk:gap --review` compatibility artifact를 `/tk:review` artifact처럼 덮어씁니다.

`/tk:review` may:

- repo/workspace 파일과 generated TigerKit artifacts를 읽습니다.
- read-only verification command를 실행합니다.
- `.claude/tigerkit/branches/<branch-key>/review/` 아래에 generated review report를 작성합니다.
- `.claude/tigerkit/global-index.json`과 `branch-state.json`에 latest review pointer를 기록합니다.
- next action으로 `/tk:gap`, `/tk:launch`, `/tk:reflect`, `/tk:handoff`, 또는 human decision을 추천합니다.

## Artifact policy

기본 receipt 위치:

```text
.claude/tigerkit/branches/<branch-key>/review/RVW-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<branch-key>/review/current.md
```

Plain workspace fallback도 같은 `branches/<scope-key>/review/` layout을 사용하고 receipt에 `범위 종류: workspace`를 표시합니다.

Review report는 generated branch-local working memory입니다. durable repo rule이나 source of truth가 아닙니다.

## Report content

`review/current.md`는 사람용 H2와 machine-readable block을 함께 포함합니다.

````md
# Review Report: <RVW-ID>

## 요약
## Review Target
## Verification Evidence
## Closed Gaps
## Remaining Gaps
## Drift / Risk
## Verdict
## Next Recommendation

```tigerkit-review-report
version: 1
review_id: RVW-YYYYMMDD-HHmmss-RAND
scope_kind: git_branch | git_detached | git_no_remote | workspace
scope_key: <branch-key-or-workspace-key>
status: REVIEW_PASS | REVIEW_PARTIAL | REVIEW_FAIL | REVIEW_BLOCKED
verdict: Pass | Partial | Fail | Blocked
target:
  source: workflow | launch | handoff | user | path | none
  ref: <path#section or none>
requirements_checked: []
verification:
  passed: []
  failed: []
  blocked: []
closed_gaps: []
remaining_gaps: []
drift_risks: []
next_action: <one sentence or 없음>
```
````

## 기본 stdout

```text
✅ Review 완료: <RVW-ID>
브랜치 범위: <branch-key>
결과: REVIEW_PASS | REVIEW_PARTIAL | REVIEW_FAIL | REVIEW_BLOCKED
Verdict: Pass | Partial | Fail | Blocked
대상: <workflow|launch|handoff|user|path|none>:<ref>

검증: <passed>/<total> 통과, <failed> 실패, <blocked> 차단
닫힌 gap: <count>
남은 gap: <count>
Drift/Risk: <none|count>

보고서: .claude/tigerkit/branches/<branch-key>/review/<RVW-ID>.md
최신본: .claude/tigerkit/branches/<branch-key>/review/current.md

다음 행동: <없음|/tk:gap 재실행|/tk:launch 재실행|human decision 필요|/tk:handoff>
```

상태 기호:

- `✅` = `REVIEW_PASS`
- `⚠️` = `REVIEW_PARTIAL`
- `🛑` = `REVIEW_FAIL` 또는 `REVIEW_BLOCKED`

## 다음 행동 추천

- `REVIEW_PASS`: 구현을 받아들이거나 `/tk:reflect`로 durable insight 후보를 정리합니다.
- `REVIEW_PARTIAL`: remaining gap이 작고 source가 충분하면 `/tk:gap`으로 새 sealed workflow를 만듭니다.
- `REVIEW_FAIL`: 실패한 verification gate나 non-goal 침범을 먼저 수정할 수 있도록 `/tk:gap` 재실행 또는 abort handoff를 추천합니다.
- `REVIEW_BLOCKED`: missing frozen target, missing source, unavailable verification, 또는 human decision을 먼저 요청합니다.

## 금지

- `REVIEW_PASS`를 단순 diff 존재나 launch receipt의 성공 문자열만으로 선언하지 않습니다.
- `/tk:gap --review`의 finding table을 `/tk:review` verdict로 혼동하지 않습니다.
- 별도 브랜드나 별도 command surface를 추가하지 않습니다.
- `freeze`를 사용자-facing command로 노출하지 않습니다. Freeze는 frozen target/assumption을 가리키는 내부 review 개념입니다.
