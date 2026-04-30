---
name: gap
description: requirements.md와 현재 구현, 문서, 테스트, 관찰 가능한 동작 사이의 차이를 분석합니다. .tigerkit/{work_id}/requirements.md가 준비된 뒤 요구사항 coverage, remaining gaps, 확인 불가 항목, ship blocker를 확인할 때 반드시 사용합니다.
---

# gap

## 목적

`prep` 단계에서 정리한 `requirements.md`를 바탕으로 현재 상태와의 갭을 분석합니다.

중간 점검과 최종 검산을 별도 skill로 나누지 않습니다. 남은 gap이 있으면 아직 작업 중이고, 확인 가능한 기준에서 gap이 없고 확인 불가 항목도 없으면 출고 가능 후보입니다.

이 스킬은 구현 계획을 만들거나 코드를 수정하는 단계가 아닙니다. 사용자가 이 스킬 밖에서 명시적으로 요청하지 않는 한 구현 계획, task breakdown, 파일별 수정 지시, 코드 변경을 하지 않습니다.

## 동작 방식

사용자에게 보이는 응답과 작업 산출물은 항상 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

이 스킬은 어떤 경우에도 코드를 구현하지 않습니다. 구현 요청은 이 스킬을 끝낸 뒤 별도 task나 별도 workflow로 다룹니다.

이 스킬은 자료 수집이나 requirements 작성을 담당하지 않습니다. 다음에 집중합니다.

1. 요구사항 기준 확인
2. 캐시 확인
3. 현재 상태 확인
4. coverage/gap 분석
5. 짧은 다음 행동 정리

## 필수 입력

다음 파일이 있어야 합니다.

```text
.tigerkit/{work_id}/requirements.md
```

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 않고 `/tk:prep`로 요구사항 기준을 먼저 정리하라고 안내합니다.

저장소를 임의로 기준 자료로 삼아 분석하지 않습니다.

## 출력 파일

다음 파일을 생성하거나 갱신합니다.

```text
.tigerkit/{work_id}/gap.md
```

## 캐시 메타데이터

`gap.md`를 생성하거나 재사용할 때 다음 메타데이터를 함께 관리합니다.

```text
.tigerkit/{work_id}/gap.meta.json
```

메타데이터에는 최소한 다음을 기록합니다.

- `artifact`: `gap.md`
- `artifact_hash`: 생성 또는 재사용된 `gap.md`의 해시
- `git_commit_sha`: 분석 기준 git commit SHA
- `working_tree_dirty`: 작업 트리에 커밋되지 않은 변경이 있었는지 여부
- `requirements_hash`: `requirements.md`의 해시
- `gap_prompt_version`: gap 스킬 또는 지시문 버전
- `scope_hash`: 분석 범위를 정규화한 해시
- `checked_paths`: 실제로 확인한 주요 파일 경로
- `created_at`: 메타데이터 작성 시각

## 진행 절차

### 1. 요구사항 기준 확인

`requirements.md`에서 다음을 확인합니다.

- Source Inputs
- Normalized Requirements
- Acceptance Signal
- Scope Boundary
- Conflicts / Ambiguities
- Assumptions
- Unknowns
- Gap Check Basis

Unknowns, assumptions, conflicts가 coverage 판단에 영향을 주면 보고서에 명시합니다.

### 2. 캐시 확인

`--force`가 명시되지 않았고 기존 `gap.md`와 `gap.meta.json`이 있으면 캐시를 확인합니다.

다음 조건을 모두 만족할 때만 기존 `gap.md`를 재사용합니다.

- 현재 `gap.md`의 해시가 메타데이터의 `artifact_hash`와 같음
- 현재 git commit SHA가 메타데이터의 `git_commit_sha`와 같음
- 현재 작업 트리에 커밋되지 않은 변경이 없음
- 메타데이터의 `working_tree_dirty`가 `false`임
- `requirements_hash`가 현재 `requirements.md` 해시와 같음
- `gap_prompt_version`이 같음
- `scope_hash`가 같음

dirty 상태에서 생성된 캐시는 이후 조건이 맞아 보여도 재사용하지 않습니다. 하나라도 다르거나 현재 작업 트리가 dirty이면 gap 분석을 다시 실행합니다.

사용자에게 cache hit/miss 여부와 이유를 한 문장으로 알려줍니다. `--force`가 명시되면 기존 캐시를 무시하고 다시 분석합니다.

### 3. 현재 상태 확인

캐시 hit이면 이 단계를 건너뛰고 기존 `gap.md`를 재사용합니다.

캐시 miss이거나 `--force`이면 requirements에 코드 경로, 현재 구현, 비교 대상, 문서 경로가 포함된 경우에만 관련 파일을 확인합니다.

요구사항에 비교 대상이 충분히 없으면 저장소 전체를 임의로 훑지 말고 `Unable to Verify` 또는 확인 질문으로 남깁니다.

현재 상태 확인은 coverage 판단에 필요한 증거 수집까지만 수행합니다. 구현 방안 설계, 수정 순서 작성, 패치 작성은 하지 않습니다.

### 4. gap.md 작성

보고서는 아래 구조를 그대로 사용합니다. `Requirement Coverage`, `Remaining Gaps`, `Unable to Verify`는 모두 표 섹션이며, 해당 항목이 0개여도 섹션과 표 헤더를 생략하지 않습니다.

```md
# Gap Report

## Verdict
GAPS_FOUND / NO_GAPS_FOUND / UNVERIFIABLE

## Requirement Coverage
| Requirement ID | Status | Evidence | Gap |
|---|---|---|---|
| REQ-001 | Covered / Partial / Missing / Unverified | 확인한 파일, 문서, 테스트, 동작 증거 | 남은 gap 또는 `없음` |

## Remaining Gaps
| Gap ID | Requirement ID | Severity | Description | Suggested Next Move |
|---|---|---|---|---|
| GAP-001 | REQ-001 | High / Medium / Low | 남은 gap 설명 | 한 문장 수준의 다음 행동 |

## Unable to Verify
| Requirement ID | Reason | Needed Evidence |
|---|---|---|
| REQ-001 | 확인 불가 이유 | 필요한 파일, 실행 결과, 권한, 사용자 확인 |

## Notes
-
```

표 작성 규칙:

- `Requirement Coverage`에는 `requirements.md`의 모든 normalized requirement를 한 행씩 포함합니다.
- `Remaining Gaps`에 남은 gap이 없으면 표 헤더 아래에 `| 없음 | - | - | 현재 확인 가능한 기준에서 남은 gap 없음 | - |` 한 행을 씁니다.
- `Unable to Verify`에 확인 불가 항목이 없으면 표 헤더 아래에 `| 없음 | - | - |` 한 행을 씁니다.
- 표 대신 bullet list나 문단으로 대체하지 않습니다.
- 표 셀 안에서 줄바꿈을 만들지 말고, 여러 증거는 `<br>` 대신 `;`로 구분합니다.

Requirement Coverage의 `Status`는 다음 중 하나를 사용합니다.

- `Covered`: 요구사항과 acceptance signal을 현재 증거로 충족한다고 볼 수 있음
- `Partial`: 일부만 충족하거나 edge case, 문서, 테스트, 동작 증거가 부족함
- `Missing`: 요구사항을 충족하는 구현, 문서, 테스트, 관찰 가능한 동작을 찾지 못함
- `Unverified`: 확인에 필요한 경로, 실행 환경, 자료, 권한, 관찰 증거가 부족함

Verdict 규칙은 다음 우선순위로 적용합니다.

1. 확인된 gap이 하나라도 있으면 `GAPS_FOUND`를 사용합니다.
2. 확인된 gap은 없지만 검증이 막힌 requirement가 하나라도 있으면 `UNVERIFIABLE`을 사용합니다.
3. 확인된 gap이 없고 unverified requirement도 없을 때만 `NO_GAPS_FOUND`를 사용합니다.

`NO_GAPS_FOUND`는 “현재 확인 가능한 기준에서는 남은 gap 없음”이라고 표현합니다.

Remaining Gaps의 `Suggested Next Move`는 한 문장 수준의 다음 행동 후보만 적습니다. 구현 계획이나 세부 작업 목록으로 확장하지 않습니다.

## 사용자 인계

전체 보고서를 채팅에 길게 출력하지 않습니다.

사용자 응답에는 다음만 포함합니다.

- 생성 또는 재사용 여부와 cache hit/miss 이유
- Verdict
- `gap.md` 파일 경로
- 핵심 gap 1~3개
- 확인 불가 항목이 있으면 그 수와 가장 중요한 이유
- 다음 행동 1개

상세 내용은 `gap.md`에 남겼다고 안내하고 마무리합니다.

## 완료 기준

이 스킬은 다음 조건을 만족하면 완료됩니다.

- `requirements.md`를 작업 기준으로 확인함
- 가능한 범위에서 현재 구현, 문서, 테스트, 관찰 가능한 동작을 확인함
- cache hit이면 기존 `gap.md`를 재사용하고 이유를 알림
- cache miss 또는 `--force`이면 `gap.md`와 `gap.meta.json`이 갱신됨
- Verdict, Requirement Coverage, Remaining Gaps, Unable to Verify, Notes가 포함됨
- Requirement Coverage, Remaining Gaps, Unable to Verify가 모두 Markdown 표로 작성되고, 빈 표도 생략되지 않음
- 확인 불가 requirement가 있으면 `NO_GAPS_FOUND`를 사용하지 않음
- 구현 계획이나 코드 변경 없이 coverage/gap 결과만 인계함
