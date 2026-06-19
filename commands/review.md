---
description: frozen goal/spec과 current implementation을 비교해 closed gaps, remaining gaps, drift, next recommendation을 검증합니다.
argument-hint: "[goal/spec refs or implementation target...] [--analysis-depth <direct|bounded|expanded|exhaustive-capped>] [--spec <SP-ID|path>] [--no-specs] [--print-report] [--maintainer-proof]"
---

이 명령은 TigerKit review command contract를 따릅니다. `/tk:review`는 `/tk:gap --review`와 같은 Contract-based review engine을 사용하는 사용자-facing 진입점입니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:review`는 frozen goal/spec, implementation plan, current implementation을 비교해 gap이 실제로 닫혔는지, regression이나 scope drift가 생겼는지, 다음 행동이 accept/re-run/escalate/abort 중 무엇인지 판단합니다.

```text
review = compare implementation against frozen goal/spec + verify closed gaps + detect drift + recommend next action
```

## Command surface

- plugin slash invocation은 `/tk:review`입니다.
- `/tk:review`는 `/tk:gap --review` compatibility behavior와 같은 review contract를 사용합니다.
- `/tk:review`는 sealed launch workflow를 생성하지 않습니다.
- `/tk:review`는 implementation을 수정하지 않습니다.
- `/tk:review`는 `freeze` 또는 `launch`를 새 user-facing command로 노출하지 않습니다.
- `--maintainer-proof`는 maintainer/self-eval 전용입니다. 일반 사용자 품질 모드나 더 강한 review 옵션처럼 설명하지 않습니다.
- `--lite`와 `--strict`가 전달되면 compatibility flag로만 기록하고 user-facing quality mode로 쓰지 않습니다.

## Inputs

입력 source는 아래를 사용할 수 있습니다.

- user-provided goal/spec text
- issue, URL, ticket, docs, screenshot/export, meeting note
- active confirmed branch-local Spec Patch
- implementation plan
- current implementation target hints
- prior `/tk:gap` or `/tk:launch` artifacts

Frozen goal/spec이 없거나 current implementation target을 확인할 수 없으면 추측하지 않고 `확인 필요` 또는 `미채택 요약`으로 남깁니다.

## Review behavior

1. current workspace root, branch-key, user-provided refs, target hints, current implementation candidates, integration freshness metadata를 bind합니다.
2. Product/Design/Design System/Engineering/QA/Analytics source를 Contract로 normalize합니다.
3. confirmed, non-superseded contract set을 freeze합니다.
4. implementation plan이 있으면 PlanCoverageAgent가 plan gap candidate만 생성합니다.
5. current implementation이 있으면 ImplementationComplianceAgent가 implementation gap candidate만 생성합니다.
6. 모든 candidate는 Candidate Intake Gate를 통과해야 합니다.
7. CriticalRedTeamAgent는 would-be accepted 또는 high-risk gated candidate가 있을 때 targeted verification으로 최대 1회만 실행합니다.
8. JudgeMergerAgent만 final finding, rejected observation, source conflict, clarification을 확정합니다.
9. closed gaps, remaining gaps, drift/risk, next recommendation을 report에 정리합니다.

## Verdict

`/tk:review`는 아래 verdict 중 하나를 출력합니다.

| Verdict | 의미 |
| --- | --- |
| `Pass` | confirmed goal/spec 기준으로 remaining actionable gap이나 blocking clarification이 없습니다. |
| `Partial` | 일부 gap은 닫혔지만 remaining gap 또는 reference-only clarification이 있습니다. |
| `Fail` | 핵심 gap이 닫히지 않았거나 regression, scope drift, blocking clarification이 있습니다. |

Verdict는 JudgeMergerAgent 결과, clarification 상태, regression/drift evidence에만 근거합니다. 내부 의도, 이전 성공, proxy 판단으로 completion을 주장하지 않습니다.

## Output and artifacts

`/tk:review` 기본 산출물은 `/tk:gap --review`와 같은 branch-local review layout을 사용합니다.

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/run.json
```

기본 stdout은 compact receipt입니다.

```text
Review 완료: <GAP-ID>
브랜치 범위: <branch-key>
Verdict: <Pass|Partial|Fail>
결과: P0 <count> / P1 <count> / P2 <count> / 근거 충돌 <count> / 확인 필요 <count>
보고서: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
실행 JSON: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/run.json
다음 행동: <accept|run another gap loop|escalate to human|abort or re-scope>
```

Report H2는 `/tk:gap --review` H2에 review sections를 더해 아래 순서를 사용합니다.

```md
# Review: <GAP-ID>

## Verdict

## 사용한 근거

## What Changed

## Closed Gaps

## Remaining Gaps

## Drift / Risk

## 조치 필요 항목

## 확인 필요

## 미채택 요약

## Next Recommendation
```

## Safety and evidence rules

- basis를 절대적 진실처럼 단정하지 않습니다.
- source conflict를 임의 병합하지 않습니다.
- subagent candidate를 final finding처럼 출력하지 않습니다.
- P3/nit, duplicate, unverifiable, source_conflict는 final finding으로 출력하지 않습니다.
- producer-absence claim에는 producer-side evidence가 필요합니다.
- candidate의 file:line, module-path, rendered output evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- visible UI copy는 confirmed contract와 exact match가 필요합니다.
- finding이 0개가 될 때까지 반복하지 않습니다.
- 사용자가 고치거나 답할 수 없는 proof/debug/self-eval metadata는 기본 stdout에 출력하지 않습니다.

## 다음 추천 action mapping

| 조건 | 추천 |
| --- | --- |
| `Pass`이고 blocking item 없음 | `accept` |
| `Partial`이고 remaining gap이 작고 source가 충분함 | `run another gap loop` |
| 사용자/owner 결정이 필요함 | `escalate to human` |
| source conflict, scope drift, 핵심 requirement 불일치가 큼 | `abort or re-scope` |
