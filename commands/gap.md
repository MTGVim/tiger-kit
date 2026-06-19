---
description: SoT와 현재 구현을 한 번 비교해 누락, 불일치, 과잉 구현, 모호성을 보고합니다.
argument-hint: "[SoT refs or pasted source] [--target <path|area>] [--print-report]"
---

이 명령은 TigerKit Slim `/tk:gap` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 Source of Truth와 Current Implementation 사이의 gap을 한 번 분석하는 lens입니다. workflow를 만들거나 freeze하지 않습니다. launch state, advisor/runner, autopilot, 반복 수렴 전제를 사용하지 않습니다.

```text
gap = SoT ↔ current implementation one-shot gap analysis
```

## Command surface

- plugin slash invocation은 `/tk:gap`입니다.
- 자연어로 “요구사항과 구현 차이 봐줘”, “SoT 기준 gap 봐줘”처럼 요청해도 이 contract를 따릅니다.
- `/tk:gap`은 세션 전체를 장악하지 않습니다.
- `/tk:gap`은 workflow를 생성하지 않습니다.
- `/tk:gap`은 workflow freezing을 하지 않습니다.
- `/tk:gap`은 `/tk:launch`, runner, advisor, autopilot을 호출하지 않습니다.
- 기존 branch-local Spec Patch가 있으면 source material 후보로만 읽을 수 있습니다. repo-wide durable knowledge로 승격하지 않습니다.

## Inputs

가능한 범위에서 아래를 분리합니다.

- `SoT`: 사용자 지시, PRD, design spec, issue, URL, pasted notes, screenshot/export, API docs, source contract, legacy Spec Patch reference.
- `Current`: 현재 repo 파일, diff, rendered output, command output, implementation plan, generated artifact.
- `Unknown`: 접근 불가 reference, 소유자 결정, 모호한 source priority, 확인하지 않은 producer surface.

SoT는 절대적 진실로 부르지 않습니다. 비교에 쓰는 기준 자료로 취급합니다.

## Analysis policy

1. Source refs와 access status를 먼저 고정합니다.
2. SoT에서 확인 가능한 requirement만 추출합니다.
3. Current Implementation은 관측 가능한 evidence로만 기록합니다.
4. 아래 네 가지 gap을 분류합니다.
   - `missing`: SoT 요구가 Current에 없음.
   - `mismatch`: SoT와 Current가 다름.
   - `overbuilt`: SoT 밖 구현이 사용자 영향, 위험, 유지보수 비용을 만듦.
   - `ambiguous`: source conflict, missing owner decision, inaccessible source, producer evidence 부족.
5. 각 finding은 evidence, impact, priority, suggested fix를 포함합니다.
6. producer 부재 claim은 consumer-side evidence만으로 확정하지 않습니다. API contract, schema, serializer, endpoint response, data model, persistence logic, owner confirmation 같은 producer-side evidence가 없으면 `ambiguous` 또는 `missing evidence`로 둡니다.
7. UI copy는 confirmed contract가 exact copy를 요구하면 exact match로 비교합니다.
8. 모호성을 조용히 해결하지 않습니다. 필요한 경우 질문 또는 Patron delegation 후보로 남깁니다.

## Priority

- `P0`: core task 불가능, 권한/보안/데이터 무결성/파괴적 동작 위험.
- `P1`: 핵심 사용자 흐름, business rule, validation, error/loading/empty state, CTA 이해에 큰 영향.
- `P2`: visible consistency, 정보 위계, design-system consistency 약화.
- `P3`: minor polish. 기본 finding에는 넣지 않고 필요하면 Not accepted summary에만 둡니다.

## Default output

기본 출력은 아래 순서를 따릅니다.

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|
| <area> | <basis> | <observed> | <missing|mismatch|overbuilt|ambiguous> | <impact> | <P0|P1|P2|P3> |

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Recommended Next Steps

1. <next step>
```

Findings에는 P0/P1/P2만 넣습니다. P3, duplicate, unverifiable, source conflict, missing evidence는 Findings가 아니라 Ambiguities 또는 Not accepted summary에 둡니다.

## Artifact policy

사용자가 저장을 명시하거나 command contract가 저장을 요구할 때만 branch/workspace-local generated report를 씁니다.

```text
.claude/tigerkit/branches/<scope-key>/gap/GAP-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<scope-key>/gap/current.md
```

이 artifact는 working memory입니다. source of truth나 durable repo rule이 아닙니다.

## 금지

- workflow 생성
- workflow freezing
- `/tk:launch` 또는 runner 호출
- advisor/runner mandatory 구조
- gap autonomous workflow
- finding이 0개가 될 때까지 반복
- 모호한 source를 조용히 병합
- producer-side evidence 없는 producer 부재 확정
- 검증 없는 success 선언
- commit, push, PR, deploy, external write side effect
