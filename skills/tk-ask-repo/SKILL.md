---
name: tk-ask-repo
description: "[user] 이 저장소로 들어온 질문에 source-located evidence를 근거로 답한다: origin, flow, existence, impact, 또는 ownership. 외부 질문에 코드 조사가 필요할 때 사용한다. 구현, decision close, runtime behavior 재현, effort estimate는 하지 않는다."
disable-model-invocation: true
argument-hint: "<수신 질문을 원문 그대로 붙여넣기>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 저장소 질의

외부 codebase 질문을 read-only로 조사한다. source, artifact, ticket, Git history를 절대 수정하지 않고 sibling skill도 invoke하지 않는다. 답변에 decision 또는 implementation이 필요하면 owner를 지정하고 중단한다.

## 호출

사용자가 `/tk-ask-repo`, `$tk-ask-repo`를 선택하거나 host skill picker에서
구체적인 repository 질문을 지정했을 때만 시작한다. 이 skill은
user-invoked-only다. `disable-model-invocation: true`와
`allow_implicit_invocation: false`가 authoritative host flags이므로, 명시적
선택이 없는 자연어 질문으로는 시작하지 않는다.

## 증거 계약

- 모든 repository-state 주장은 `path:line`을 인용하거나, 이유와 함께
  `unavailable`이라고 명시한다.
- 질문자의 정확한 symptom, label, 또는 identifier를 첫 search anchor로 사용한다.
- Declaration은 shape는 증명하지만 origin은 증명하지 않는다. 값을 생성한
  assignment, 저장된 input, literal, 또는 external boundary까지 추적한다.
- `Not found`는 `absent`가 아니다. 먼저 current base와 관련 in-flight work를
  검색한다.
- value, impact, attribution 질문에서는 모든 consumer를
  `must change | must not change | unclear`로 분류한다. `Must not change`는
  필수이며, 비어 있으면 `none found`라고 쓴다.

## 작업 흐름

1. **Classify**를 `value | structure | existence | impact | attribution` 중 하나로
   정한다. 여러 질문이 섞였으면 나누고 blocker를 식별한다.
2. **Anchor**를 보이는 string, identifier, route, endpoint, 또는 symbol에 둔다.
   구체적인 anchor가 남지 않으면 시도한 query를 보고하고 `Unverifiable`로
   중단한다.
3. **Traverse**를 아래의 해당 경로로 수행하고, 각 hop에 `path:line`을 기록한다.
4. **Sweep**로 관련 reader/writer를 value, impact, attribution 관점에서
   조사하고, 범위를 결정하는 count의 search semantics를 검증한다.
5. **Attribute**를 evidence로 판단한다.
   - payload에 올바른 value가 있음 → consuming side;
   - value가 없거나 잘못됨 → producer와 정확한 field;
   - 둘 다 해당함 → responsibility를 나누고 서로를 막는 쪽을 명시한다.
6. **Verify**에서 current ref, 검색한 variant, dynamic-dispatch gap, exclusion,
   그리고 인용한 모든 hop을 확인한다.

## 추적 경로

- **Value**: visible string → bound key/prop/column → consuming expression →
  transport field → declaring type → assignment site. 의미를 판단하기 전에 sibling
  assignment와 comment를 읽는다.
- **Structure**: entry point → ordered boundary, 예: view → transport → producer →
  store/external. dynamic dispatch를 표시한다.
- **Existence**: current base ref → open/unmerged work → environment state.
  `absent | unreleased here | present but empty/placeholder | present and live`를
  구분한다. "since when"을 확인하기 위해 introducing change를 추적한다.
- **Impact**: symbol/field/pattern → 모든 reader/writer → 모든 consumer를 분류하고
  search exclusion을 명시한다.
- **Attribution**: producer를 탓하기 전에 consuming-side trace를 끝낸다.
  transform, permission, feature gate, conditional rendering, 같은 path의
  environment 차이를 확인한다.

## 실패 경계

| Condition | Result |
| --- | --- |
| exact 및 component search 뒤에도 anchor가 없음 | 실행한 query와 함께 `Unverifiable` |
| 필요한 source를 읽을 수 없음 | gap을 인용하고 그 너머를 추론하지 않음 |
| 가능한 답이 두 개 남음 | 둘 다와 decision owner를 적은 `Blocked` |
| 불명확한 consumer가 남음 | 나열하되 조용히 포함하거나 제외하지 않음 |
| premise가 current code와 모순됨 | premise가 아니라 contradiction을 보고함 |
| request가 implementation, decision, runtime reproduction, estimate, general knowledge임 | 올바른 owner를 지정하고 중단 |

## 결과

`Answer`로 시작한다. 결과가 하나면 짧은 문단 1~3개를 사용하고, 2~7개면
간결한 bullet 또는 한 종류의 table 하나를 사용하며, 더 많으면 상위 5~7개와
나머지를 소유한 evidence path를 제시한다.

관련 있고 비어 있지 않은 section만 포함한다.
`Evidence | Origin | Sibling fields | Path | State | Attribution |
Must change | Must not change | Remaining concerns`.

질문을 되풀이하거나, evidence를 반복하거나, diff를 제안하거나, artifact를
만들어내거나, receipt/provenance block을 덧붙이지 않는다. 실행 가능한 경우에만
`Blocked | Unverifiable`, next owner, 또는 recovery action 하나를 명시한다.
