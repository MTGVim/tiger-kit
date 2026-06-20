---
description: SoT가 있으면 구현 전에 먼저 고려하는 one-shot gap analysis입니다.
argument-hint: "[SoT refs or pasted source] [--target <path|area>] [--print-report]"
---

이 명령은 TigerKit `/tk:gap` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 Source of Truth와 Current Implementation 사이의 차이를 한 번 분석해 source loss를 줄이는 command입니다. workflow를 만들거나 freeze하지 않습니다.

```text
gap = source of truth ↔ current implementation one-shot comparison
```

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있습니다.
- SoT 없이 진행할 때는 가정과 불확실성을 명시합니다.

## Inputs

가능한 범위에서 아래를 분리합니다.

- `SoT`: 사용자 지시, PRD, design spec, issue, URL, pasted notes, screenshot/export, API docs, source contract.
- `Current`: 현재 repo 파일, diff, rendered output, command output, implementation plan, generated artifact.
- `Unknown`: 접근 불가 reference, 소유자 결정, 모호한 source priority, 확인하지 않은 producer surface.

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
6. 모호한 source를 조용히 병합하지 않습니다.

## Priority

- `P0`: core task 불가능, 권한/보안/데이터 무결성/파괴적 동작 위험.
- `P1`: 핵심 사용자 흐름, business rule, validation, error/loading/empty state, CTA 이해에 큰 영향.
- `P2`: visible consistency, 정보 위계, design-system consistency 약화.
- `P3`: minor polish. 기본 finding에는 넣지 않고 필요하면 Not accepted summary에만 둡니다.

## Output

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

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

## Not accepted summary

- <optional low-priority or rejected note>

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

## 금지

- workflow 생성
- workflow freezing
- advisor/runner/autopilot 구조
- finding이 0개가 될 때까지 반복
- 검증 없는 success 선언
- commit, push, PR, deploy, external write side effect
