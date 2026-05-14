---
description: indexed source-of-truth reference와 reproducible code baseline을 비교해 evidence-based gap을 .tigerkit/gap.md에 기록합니다. 실행 대기열로 변환하지 않습니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `/tk:gap`은 TigerKit의 중심 명령입니다. `.tigerkit/requirements.md`에 인덱싱된 SOT reference와 특정 code baseline을 비교하고, 증거 기반 차이를 `.tigerkit/gap.md`에 기록합니다.

```text
gap = SOT reference vs commit/code comparison
```

## 기본 산출물

- `.tigerkit/gap.md`

## baseline rule

gap 분석 전에 code baseline을 식별합니다.

필수 baseline:

```text
clean working tree + HEAD commit hash
```

working tree가 clean하지 않으면 gap 기록을 시작하지 않습니다. 먼저 commit하거나 변경을 정리해 reproducible baseline을 만듭니다.

## gap shape

각 gap은 아래 항목을 포함합니다.

- compared SOT
- compared code baseline
- inspected files
- evidence
- finding
- interpretation, if any
- resolution
- required resolution

권장 형식:

```md
## GAP-001 — Tooltip copy mismatch

Type: mismatch
Resolution: open

### Compared SOT

- Source: PRD
- Reference: https://...
- Section: Tooltip copy

### Compared Code

- Baseline: abc1234
- Files inspected:
  - src/...

### Evidence

SOT:
> short exact excerpt or pointer

Code:
> short exact excerpt or pointer

### Finding

PRD copy와 구현 tooltip copy가 다릅니다.

### Interpretation

implementation drift로 보입니다. source ambiguity는 아닙니다.

### Required Resolution

사용자 확인 또는 code update 필요.
```

## evidence rule

중요 claim은 아래 중 하나에 근거해야 합니다.

- external SOT reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- derived artifact clearly marked as derived

항상 분리합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or SOT
Suggestion = proposed, not confirmed
```

## ambiguity rule

source가 결론을 지지하지 않으면 추측하지 않습니다.

1. ambiguity를 gap으로 기록합니다.
2. 필요하면 사용자에게 질문합니다.
3. resolved처럼 구현하거나 decision으로 저장하지 않습니다.

## 절차

1. `.tigerkit/requirements.md`에서 비교할 SOT reference를 확인합니다.
2. working tree 상태와 HEAD commit을 확인해 baseline을 정합니다.
3. working tree가 clean하지 않으면 commit 또는 정리를 요청하고 멈춥니다.
4. 관련 code file을 읽고 inspected files에 기록합니다.
5. exact excerpt나 pointer 중심으로 evidence를 남깁니다.
6. finding과 interpretation을 분리합니다.
7. required resolution을 해결 기준으로 적습니다.
8. `.tigerkit/gap.md`를 갱신합니다.

## 금지

- gap을 실행 대기열로 변환
- ambiguity silent resolution
- external source 요약을 official requirement처럼 저장
- `DESIGN.md` 또는 `reuse-map.md` 직접 업데이트
- implementation, commit, push, PR 생성, merge, deploy

## 출력

```text
gap 기록했습니다.
- baseline: `abc1234`
- inspected files: source 비교에 필요한 파일
- recorded: `GAP-001`, `GAP-002`
- 기록: `.tigerkit/gap.md`

다음 추천: /tk:reflect
```
