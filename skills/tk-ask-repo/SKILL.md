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

외부 코드베이스 질문을 읽기 전용으로 조사한다. 소스, 산출물, 티켓, Git 이력을 절대 수정하지 않고 인접 스킬도 호출하지 않는다. 답변에 결정 또는 구현이 필요하면 소유자를 지정하고 중단한다.

## 호출

사용자가 `/tk-ask-repo`, `$tk-ask-repo` 를 선택하거나 호스트 스킬 picker에서
구체적인 저장소 질문을 지정했을 때만 시작한다. 이 스킬은
명시적 호출 전용이다. `disable-model-invocation: true` 와
`allow_implicit_invocation: false` 가 호스트의 권위 있는 flag이므로, 명시적
선택이 없는 자연어 질문으로는 시작하지 않는다.

## 증거 계약

- 모든 저장소-상태 주장은 `path:line` 을 인용하거나, 이유와 함께
  `unavailable` 이라고 명시한다.
- 질문자의 정확한 증상, label, 또는 식별자를 첫 검색 기준점로 사용한다.
- Declaration은 형태는 증명하지만 origin은 증명하지 않는다. 값을 생성한
  대입, 저장된 입력, 리터럴, 또는 외부 경계까지 추적한다.
- `Not found` 는 `absent` 가 아니다. 먼저 현재 base와 관련 in-flight work를
  검색한다.
- value, 영향, 귀속 질문에서는 모든 소비자를
  `must change | must not change | unclear` 로 분류한다. `Must not change` 는
  필수이며, 비어 있으면 `none found`라고 쓴다.

## 작업 흐름

1. **분류**를 `value | structure | existence | impact | attribution` 중 하나로
   정한다. 여러 질문이 섞였으면 나누고 blocker를 식별한다.
2. **기준점**을 보이는 문자열, 식별자, 경로, endpoint, 또는 symbol에 둔다.
   구체적인 기준점이 남지 않으면 시도한 query를 보고하고 `Unverifiable` 로
   중단한다.
3. **추적**을 아래의 해당 경로로 수행하고, 각 hop에 `path:line` 을 기록한다.
4. **전수 조사**로 관련 reader/writer를 value, 영향, 귀속 관점에서
   조사하고, 범위를 결정하는 count의 검색 의미를 검증한다.
5. **귀속**을 근거로 판단한다.
   - payload에 올바른 value가 있음 → 소비 측;
   - value가 없거나 잘못됨 → 생산자와 정확한 필드;
   - 둘 다 해당함 → 책임을 나누고 서로를 막는 쪽을 명시한다.
6. **검증**에서 현재 ref, 검색한 variant, dynamic-dispatch gap, exclusion,
   그리고 인용한 모든 hop을 확인한다.

## 🔴 CHECKPOINT / STOP · 조사 경계

`🔴 CHECKPOINT` 에서 정확한 질문, 첫 검색 기준점, 현재 ref와 읽기 전용 범위를
확인한 뒤에만 추적/전수 조사를 시작한다. 기준점이 없거나 소스를 읽을 수 없거나
가능한 답이 두 개 남으면 남으면 더 진행하지 않는다. anchor가 없으면 아래 실패
경계의 `Unverifiable`, 가능한 답이 두 개 남으면 `Blocked` 를 반환하며, 소스를
읽을 수 없으면 gap을 인용하고 그 너머를 추론하지 않는다.

`🛑 STOP` — 요청이 구현, 결정, 런타임 재현, 추정 또는
일반 지식로 판명되면 저장소를 계속 조사하지 않고 올바른 소유자를 지정한다.
이 스킬은 소스, 산출물, 티켓, Git 이력을 수정하거나 인접 스킬을 호출하지
않는다.

## 추적 경로

- **값**: 표시되는 문자열 → bound key/prop/column → consuming expression →
  transport 필드 → declaring type → 대입 지점. 의미를 판단하기 전에 인접
  assignment와 comment를 읽는다.
- **구조**: entry point → ordered boundary, 예: view → transport → 생산자 →
  store/외부. dynamic dispatch를 표시한다.
- **존재**: 현재 base ref → open/unmerged work → 환경 상태.
  `absent | unreleased here | present but empty/placeholder | present and live` 를
  구분한다. "since when"을 확인하기 위해 introducing change를 추적한다.
- **영향**: symbol/필드/pattern → 모든 reader/writer → 모든 소비자를 분류하고
  검색 제외을 명시한다.
- **귀속**: 생산자를 탓하기 전에 소비 측 추적를 끝낸다.
  transform, permission, feature gate, conditional rendering, 같은 경로의
  환경 차이를 확인한다.

## 실패 경계

| 조건 | 결과 |
| --- | --- |
| 정확한 및 component 검색 뒤에도 anchor가 없음 | 실행한 query와 함께 `Unverifiable` |
| 필요한 소스를 읽을 수 없음 | gap을 인용하고 그 너머를 추론하지 않음 |
| 가능한 답이 두 개 남음 | 둘 다와 결정 소유자를 적은 `Blocked` |
| 불명확한 소비자가 남음 | 나열하되 조용히 포함하거나 제외하지 않음 |
| premise가 현재 code와 모순됨 | premise가 아니라 contradiction을 보고함 |
| 요청이 구현, 결정, 런타임 재현, 추정, 일반 지식임 | 올바른 소유자를 지정하고 중단 |

## 결과

`Answer` 로 시작한다. 결과가 하나면 짧은 문단 1~3개를 사용하고, 2~7개면
간결한 bullet 또는 한 종류의 table 하나를 사용하며, 더 많으면 상위 5~7개와
나머지를 소유한 근거 경로를 제시한다.

관련 있고 비어 있지 않은 section만 포함한다.
`Evidence | Origin | Sibling 필드 | Path | State | Attribution |
Must change | Must not change | Remaining concerns`.

질문을 되풀이하거나, 근거를 반복하거나, diff를 제안하거나, 산출물을
만들어내거나, receipt/provenance block을 덧붙이지 않는다. 실행 가능한 경우에만
`Blocked | Unverifiable`, 다음 소유자, 또는 복구 조치 하나를 명시한다.
