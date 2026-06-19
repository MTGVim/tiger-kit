---
description: 설계, 계획, 변경안을 작은 질문 렌즈로 압박 검증합니다.
argument-hint: "[proposal or target] [--target <path|area>] [--patron <id>]"
---

이 명령은 TigerKit Slim `/tk:grill` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:grill`은 설계, 계획, 변경안, reviewer 판단을 작은 분석 렌즈로 압박 검증하는 optional micro command입니다. workflow를 만들거나 freeze하지 않습니다. launch state, advisor/runner, autopilot, 반복 수렴 전제를 사용하지 않습니다.

```text
grill = proposal or review context ↔ evidence ↔ sharp questions
```

## Command surface

- plugin slash invocation은 `/tk:grill`입니다.
- 자연어로 “이 계획 구멍 찾아줘”, “리뷰 관점에서 질문 뽑아줘”, “설계 압박 검증해줘”처럼 요청해도 이 contract를 따릅니다.
- `/tk:grill`은 세션 전체를 장악하지 않습니다.
- `/tk:grill`은 workflow를 생성하지 않습니다.
- `/tk:grill`은 workflow freezing을 하지 않습니다.
- `/tk:grill`은 `/tk:launch`, runner, advisor, autopilot을 호출하지 않습니다.
- 코드, 문서, diff, 기존 rule에서 답할 수 있는 질문은 먼저 직접 조사합니다.
- 사용자나 owner 결정이 필요한 질문만 남깁니다.

## Inputs

가능한 범위에서 아래를 분리합니다.

- `Proposal`: 설계, 계획, PR 설명, review 판단, 사용자 아이디어, pasted notes.
- `Evidence`: 현재 repo 파일, diff, docs, rules, command contract, 검증 output, 접근 가능한 external reference.
- `Unknown`: 접근 불가 reference, owner decision, source conflict, 확인하지 않은 producer surface.

## Analysis policy

1. Proposal과 target surface를 고정합니다.
2. 공개 contract, repo rule, docs, current implementation evidence를 먼저 확인합니다.
3. 질문을 아래 유형으로 분류합니다.
   - `missing-evidence`: 판단 근거가 부족합니다.
   - `contract-risk`: 공개 contract와 충돌 가능성이 있습니다.
   - `scope-risk`: 필요 이상 확장되거나 빠진 범위가 있습니다.
   - `review-risk`: reviewer가 오판하거나 놓칠 수 있는 merge readiness 이슈가 있습니다.
   - `owner-decision`: 사용자, PM, Design, BE owner, QA 같은 owner 결정이 필요합니다.
4. 코드나 문서에서 답할 수 있는 질문은 확인 결과와 함께 닫습니다.
5. 남은 질문은 actionability, impact, 추천 next step을 포함합니다.
6. 중대하거나 불확실한 owner decision은 `/tk:afk` Patron 위임 후보로 표시할 수 있습니다.

## Default output

기본 출력은 아래 순서를 따릅니다.

```md
## Grill Summary

| Area | Proposal | Evidence checked | Risk | Question | Recommendation |
|---|---|---|---|---|---|

## Closed Questions

| Question | Answer | Evidence |
|---|---|---|

## Open Questions

### 1. <question title>
- Type:
- Evidence checked:
- Why it matters:
- Recommendation:
- Patron candidate: <none|reviewer|tester|security|webperf|steward|simplifier|cartographer>

## Recommended Next Steps

1. <next step>
```

## Reviewer loop policy

- `/tk:review`는 active command surface가 아닙니다.
- reviewer loop에서 설계나 계획을 압박 검증해야 하면 `/tk:grill`을 사용합니다.
- merge readiness 결정을 위임해야 하면 `/tk:afk --patron reviewer`를 사용합니다.
- `/tk:grill` 결과는 confirmed defect가 아니라 질문/리스크 목록입니다. PR comment로 옮길 때는 direct evidence와 required change를 다시 확인합니다.

## Artifact policy

사용자가 저장을 명시하거나 command contract가 저장을 요구할 때만 branch/workspace-local generated report를 씁니다.

```text
.claude/tigerkit/branches/<scope-key>/grill/GRILL-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<scope-key>/grill/current.md
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
- 확인하지 않은 질문을 defect로 승격
- 검증 없는 success 선언
- commit, push, PR, deploy, external write side effect
