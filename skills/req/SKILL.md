---
name: req
description: 외부 요구사항 소스와 대화 맥락을 이후 계획과 갭 확인의 기준이 되는 requirements.md로 정리합니다. 사용자가 요구사항을 정리하거나, source of truth 후보를 합치거나, gap 분석 전에 기준 문서를 만들려 할 때 반드시 사용합니다.
---

# req

## 목적

Jira 티켓, Confluence 문서, PRD, 사용자 메모, 회의 요약, 기존 요구사항 문서, 앞선 대화 맥락을 갭 확인 가능한 요구사항 기준으로 정리합니다.

이 스킬은 구현 계획을 만들거나 코드를 수정하는 단계가 아닙니다. 무엇을 기준으로 계획하거나 갭을 볼지 먼저 고정합니다.

## 동작 방식

사용자에게 보이는 응답과 작업 산출물은 항상 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

긴 질문지를 던지지 않습니다. 현재 대화에서 추론할 수 있는 내용을 먼저 짧게 요약하고, 부족한 결정만 좁혀서 묻습니다.

## 하지 않는 일

- 요구사항 임의 창작
- 구현 계획 확정
- 파일별 수정 지시
- 코드 패치 작성
- 별도 구현 계획 workflow를 대체하는 task breakdown 생성

## 시작 프롬프트

작업 기준이 아직 고정되지 않았다면 먼저 다음 두 가지를 확인합니다.

```text
현재 대화 기준으로는 “{추론한 스펙명}” 요구사항으로 정리할 수 있어 보입니다.

1. 별도 자료가 있나요?
   - 파일 경로, 기획서 URL, 티켓, 메모, 스크린샷 등
   - 없으면 앞선 대화 맥락만 기준으로 정리합니다.

2. 스펙명/작업 ID는 “{추론한 스펙명}”으로 잡아도 될까요?
```

사용자가 바로 자료를 제공했거나 스펙명을 명시했다면 불필요하게 다시 묻지 말고 확인된 정보로 진행합니다.

## 입력 자료

다음 자료를 요구사항 기준으로 사용할 수 있습니다.

- 앞선 대화 맥락
- 이슈 트래커 티켓
- 지식베이스 문서
- PRD 또는 디자인 문서
- 사용자가 작성한 브리프나 메모
- 스크린샷
- 코드 경로
- 풀 리퀘스트
- 기존 구현 참고 자료

외부 시스템이나 특정 도구 사용을 강제하지 않습니다. 사용자가 제공하거나 가져오라고 지시한 자료만 다룹니다.

## 산출물 디렉터리

가능하면 작업명이나 명시된 작업 ID에서 안전한 slug를 만듭니다.

산출물은 다음 경로 아래에 저장합니다.

```text
.tigerkit/{work_id}/
```

현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면, 산출물 작성 전에 작업 브랜치나 명시적 작업 ID를 권유합니다. 브랜치 생성이나 전환은 사용자 승인 없이 수행하지 않습니다.

## 출력 파일

다음 파일을 생성하거나 갱신합니다.

```text
.tigerkit/{work_id}/requirements.md
```

필요하면 다음 디렉터리도 사용합니다.

```text
.tigerkit/{work_id}/inputs/
```

`requirements.md`는 영구적인 원천소스가 아니라 이번 작업에서 계획과 갭 확인 기준으로 사용할 요구사항 스냅샷입니다.

Git 저장소에서 실행 중이라면 `.tigerkit/`이 ignore 또는 의도적으로 track되는지 확인합니다. 둘 다 아니라면 산출물 생성 전에 `.tigerkit/`을 `.gitignore`에 추가하라고 제안합니다. 사용자 저장소의 ignore 정책은 강제하지 않습니다.

## 캐시 메타데이터

`requirements.md`를 생성하거나 재사용할 때 다음 메타데이터를 함께 관리합니다.

```text
.tigerkit/{work_id}/requirements.meta.json
```

메타데이터에는 최소한 다음을 기록합니다.

- `artifact`: `requirements.md`
- `artifact_hash`: 생성 또는 재사용된 `requirements.md`의 해시
- `input_source_hash`: requirements 생성에 실제 사용한 입력 자료의 해시
- `req_prompt_version`: req 스킬 또는 지시문 버전
- `scope_hash`: 작업 ID, 스펙명, 포함 범위, 제외 범위를 정규화한 해시
- `input_identities`: 사람이 확인할 수 있는 입력 자료 목록
- `created_at`: 메타데이터 작성 시각

`req_prompt_version`은 현재 req 스킬 지시문의 안정 식별자로, `skills/req/SKILL.md` 내용 해시나 수동으로 올린 지시문 버전을 사용합니다.

전체 대화가 아니라 requirements 생성에 실제 사용한 입력만 해시합니다.

## requirements.md 구조

```md
# Requirements

## Source Inputs
| Source | Type | Role | Status | Notes |
|---|---|---|---|---|

## Normalized Requirements
| ID | Requirement | Priority | Source | Acceptance Signal |
|---|---|---|---|---|

## Scope Boundary
### In Scope
-

### Out of Scope
-

## Conflicts / Ambiguities
| ID | Issue | Sources | Impact | Suggested Resolution |
|---|---|---|---|---|

## Assumptions
| ID | Assumption | Reason | Risk |
|---|---|---|---|

## Unknowns
| ID | Question | Impact | Suggested Next Step |
|---|---|---|---|

## Gap Check Basis
- `tk:gap`은 이 문서의 Normalized Requirements와 Acceptance Signal을 기준으로 현재 상태의 차이를 확인한다.
```

## 진행 절차

### 1. 기준 선택

앞선 대화 맥락만으로 정리할지, 별도 자료를 추가할지 확인합니다.

아이디어가 흐릿하면 다음 범위만 짧게 좁힙니다.

- 해결하려는 문제
- 원하는 완료 상태
- 반드시 지켜야 할 제약
- 이번에 제외할 범위
- 검증 방법 또는 acceptance signal

### 2. 캐시 확인

`--force`가 명시되지 않았고 기존 `requirements.md`와 `requirements.meta.json`이 있으면 캐시를 확인합니다.

다음 값이 모두 같으면 기존 `requirements.md`를 재사용합니다.

- `input_source_hash`
- `req_prompt_version`
- `scope_hash`
- `input_identities`

하나라도 다르면 `requirements.md`를 다시 생성합니다.

사용자에게 cache hit/miss 여부와 이유를 한 문장으로 알려줍니다. `--force`가 명시되면 기존 캐시를 무시하고 다시 생성합니다.

### 3. 요구사항 정리

캐시 hit이면 이 단계를 건너뛰고 기존 `requirements.md`를 재사용합니다.

캐시 miss이거나 `--force`이면 모든 자료를 하나의 요구사항 기준으로 정규화합니다.

다음을 분리해서 기록합니다.

- Source Inputs
- Normalized Requirements
- Scope Boundary
- Conflicts / Ambiguities
- Assumptions
- Unknowns
- Gap Check Basis

확인된 사실과 추정을 섞지 않습니다. 두 자료가 충돌하면 조용히 합치지 말고 충돌을 명시합니다.

### 4. 저장과 인계

`requirements.md`를 작성하거나 재사용한 뒤, 다음에 `/tk:gap`으로 요구사항 대비 갭을 확인하거나 별도 구현 계획 workflow에서 이 문서를 기준으로 계획을 세울 수 있다고 안내합니다.

사용자 응답에는 다음만 포함합니다.

- 생성 또는 재사용 여부와 cache hit/miss 이유
- `requirements.md` 파일 경로
- 외부 요구사항 소스 수
- 정규화된 요구사항 수
- 모호점 또는 충돌 수
- 다음 단계 한 문장

전체 `requirements.md` 내용을 채팅에 길게 출력하지 않습니다.

## 완료 기준

이 스킬은 다음 조건을 만족하면 완료됩니다.

- 작업 기준 이름이 정해짐
- cache hit이면 기존 `requirements.md`를 재사용하고 이유를 알림
- cache miss 또는 `--force`이면 요구사항 기준이 `requirements.md`에 정리되고 메타데이터가 갱신됨
- 확인된 사실, 충돌/모호점, 추정, unknowns가 분리됨
- 다음 단계가 `/tk:gap` 또는 별도 구현 계획 workflow로 명확함
- 사용자 응답이 파일 경로와 짧은 요약 중심으로 정리됨
