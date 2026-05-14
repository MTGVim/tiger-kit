---
description: source-of-truth reference와 사용자 인터뷰 원문을 .tigerkit/requirements.md에 인덱싱합니다. pseudo-requirement를 만들지 않습니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:prep`은 TigerKit의 source-loss prevention 진입점입니다. 요구사항을 새로 쓰는 명령이 아니라 source-of-truth 위치를 인덱싱하고, 현재 세션에서 사용자가 직접 말한 내용만 원문에 가깝게 보존합니다.

```text
prep = index sources, preserve interview, avoid source loss
```

## 기본 산출물

- `.tigerkit/requirements.md`

기본 위치는 repository root 기준 `.tigerkit/requirements.md`입니다.

## 핵심 원칙

`requirements.md`는 source of truth가 아닙니다. source of truth를 가리키는 index입니다.

외부 source는 reference만 저장합니다.

- URL
- file path
- ticket link
- Figma link
- PRD link
- issue link
- API docs link
- source code path
- commit hash

외부 source 내용을 local requirement text로 복사, 요약, 정규화, 재작성하지 않습니다. 중요한 wording이 있으면 짧은 exact excerpt 또는 section pointer만 남기고, 원문 위치를 우선합니다.

현재 세션의 직접 사용자 인터뷰 내용만 local text로 저장할 수 있습니다. 가능한 한 사용자 wording을 보존하고, `Raw`와 `Derived Interpretation`을 분리합니다.

## 권장 구조

```md
# TigerKit Requirements Index

## External Sources

- PRD: https://...
- Figma: https://...
- GitHub Issue: https://...
- Source Code: src/...
- Commit: abc1234

## Interviewed Requirements

### Raw

> 사용자 원문에 가까운 내용

### Derived Interpretation

- 명시적으로 파생 해석임을 표시

## Ambiguities

- 확인되지 않은 점과 확인이 필요한 source
```

## 절차

1. 사용자가 제공한 source를 external reference와 direct interview text로 분리합니다.
2. 외부 source는 pointer만 기록합니다.
3. 사용자 인터뷰 내용은 raw quote에 가깝게 기록합니다.
4. 파생 해석은 `Derived Interpretation` 아래에 표시합니다.
5. source가 conclusion을 지지하지 않으면 추측하지 말고 ambiguity로 남깁니다.
6. 지정된 source index 외의 산출물을 만들지 않습니다.

## ambiguity rule

source가 결론을 지지하지 않으면 silent choice를 하지 않습니다.

```text
source does not specify X
→ ambiguity 기록
→ 필요하면 사용자에게 확인
```

## 금지

- 실행 대기열이나 진행 상태 파일 생성
- external source를 local requirement처럼 요약/재작성
- 여러 source를 하나의 synthetic requirement로 병합
- `DESIGN.md` 또는 `reuse-map.md` 직접 업데이트
- implementation, commit, push, PR 생성, merge, deploy

## 출력

receipt-first로 짧게 보고합니다.

```text
source index 갱신했습니다.
- 기록: `.tigerkit/requirements.md`
- external sources: reference만 저장
- interview: raw와 interpretation 분리
- ambiguity: 확인 필요 항목 기록

다음 추천: /tk:gap
```
