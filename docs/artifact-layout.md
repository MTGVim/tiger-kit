# 산출물 구조

권장 프로젝트 로컬 산출물 구조:

```text
.tigerkit/{work_id}/
  inputs/
  requirements.md
  requirements.meta.json
  gap.md
  gap.meta.json
  plan.md
  tasks.md
  close.md
```

`/tk:prep`는 입력 자료와 대화 맥락을 `requirements.md`로 정리합니다. `/tk:gap`은 현재 repo 상태와 `requirements.md`의 차이를 `gap.md`에 기록합니다. `/tk:plan`은 gap 결과를 승인 가능한 실행계획으로 정리합니다. `/tk:breakdown`은 gap 또는 plan을 `tasks.md`로 내립니다. `/tk:state`는 `.tigerkit/{work_id}` 전체 상태를 읽습니다. `/tk:close`는 세션 종료 요약을 필요할 때 `close.md`로 남길 수 있습니다.

`/tk:reflect`는 maintenance alias로 유지되지만 `prep → gap → plan → breakdown → do/do-all → gap → close` 라이프사이클의 필수 단계는 아닙니다.

## 브랜치 이름과 작업 ID

현재 git 브랜치가 진행 중인 작업을 나타낸다면 그 브랜치 이름을 사용할 수 있습니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면 변경 가능한 산출물을 쓰기 전에 다음 중 하나를 우선합니다.

- 사용자 승인 후 작업 브랜치를 만들거나 전환
- 사용자에게 짧은 작업 ID를 묻고 `.tigerkit/{work_id}/` 아래에 사용

브랜치를 자동으로 만들거나 전환하지 않습니다. git 브랜치를 확인할 수 없다면 사용자가 제공한 짧은 작업 ID를 사용합니다.

## 파일 책임

| 파일 | 역할 |
|---|---|
| `inputs/` | `requirements.md`를 만들 때 참고한 원문 자료, 메모, 캡처, 참고 코드 보관 위치 |
| `requirements.md` | 이번 작업의 정규화된 요구사항 기준 문서 |
| `requirements.meta.json` | `requirements.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `gap.md` | 현재 상태와 `requirements.md` 사이의 coverage/gap 분석. `API Contract Drift`를 항상 포함 |
| `gap.meta.json` | `gap.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `plan.md` | 구현 묶음, API Readiness, 선행관계, 검증 순서를 담은 canonical 실행계획 |
| `tasks.md` | 작은 실행 task, API Follow-up Tasks, Clarification Actions, Shared Blockers, 상태, 포함 작업 요약, 완료 기준 |
| `close.md` | 선택적으로 남기는 세션 종료 요약, 남은 gap, 검증 상태, cleanup 후보 |

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `req-needed` | `requirements.md` 없음 | `/tk:prep` 실행 |
| `gap-needed` | `requirements.md`는 있고 `gap.md` 없음 | `/tk:gap` 실행 |
| `plan-needed` | `gap.md`는 있고 `plan.md` 없음 | `/tk:plan` 실행 |
| `tasks-needed` | `plan.md` 또는 `gap.md`는 있고 `tasks.md` 없음 | `/tk:breakdown` 실행 |
| `clarification-needed` | unresolved `Clarification Actions` 있음 | `/tk:grill-me`, targeted question, brainstorming, assumption 선택 |
| `task-ready` | 실행 가능한 `todo` 또는 `in_progress` task 있음 | `/tk:do` 또는 `/tk:do-all` 실행 |
| `blocked` | 실행 가능한 일반 task가 없고 외부 `blocked` 또는 `Shared Blockers`의 `상태=blocked` 항목만 있음 | blocker 해결 또는 API/contract 확인 |
| `re-eval-needed` | 구현 후 gap 재확인 필요 | `/tk:gap` 실행 |
| `close-ready` | gap 재확인까지 끝났고 새 gap, unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목 없음 | `/tk:close` 실행 |

`/tk:state`는 위 상태를 요약해 보여주고, `/tk:next`는 위 상태를 바탕으로 다음 command나 다음 task 1개를 추천합니다. task를 보여줄 때는 task ID만 적지 말고 `포함 작업` 같은 짧은 요약으로 묶인 gap/작업을 함께 보여줍니다. source나 work_id가 불명확하면 추측하지 않고 사용자에게 묻습니다.

## API 의존성 흐름

API나 공식 contract가 없지만 기능을 진행해야 하면 `/tk:plan`은 feature slice 단위 `API Readiness`에서 `mock_api_contract`를 사용할 수 있습니다. 이 상태는 assumed contract와 mock API로 개발/검증을 계속하는 뜻이며 완료나 merge-ready를 뜻하지 않습니다.

`/tk:breakdown`은 `mock_api_contract` slice의 일반 task를 전부 `blocked`로 만들지 않고, 별도 `API Follow-up Tasks`에 공유 API capability별 `TK-API-*` 항목 하나만 둡니다. unresolved `TK-API-*`는 `/tk:close`에서 merge blocker입니다.

## 모호함과 외부 blocker

`spec_unclear`나 모호한 요구사항은 terminal `blocked`가 아닙니다. `tasks.md`의 `Clarification Actions`에 `TK-CLARIFY-<n>` 항목으로 올리고 `/tk:grill-me`, targeted question, brainstorming, assumption 선택 중 다음 행동을 남깁니다. 표에는 `ID`, `상태`, `모호점`, `추천 경로`, `영향 task`, `완료 조건`을 포함합니다. 상태는 `unresolved` 또는 `resolved`로 표시합니다.

`blocked`와 `Shared Blockers`는 외부에서만 풀 수 있는 `api_contract_missing`, `permission_required`, `external_dependency_unavailable`, `human_decision_required` 같은 상태에 사용합니다. 같은 blocker를 공유하는 task는 task별로 복제하지 않고 `Shared Blockers` 항목 하나에 영향 task와 해소 조건을 모읍니다. 표에는 `ID`, `유형`, `상태`, `영향 task`, `해소 조건`, `현재 근거`를 포함합니다. 상태는 `blocked` 또는 `resolved`로 표시합니다.

## task 상태값

`tasks.md`의 상태값은 아래만 사용합니다.

| 상태 | 의미 |
|---|---|
| `todo` | 아직 시작하지 않은 실행 가능 task |
| `in_progress` | 현재 진행 중인 task |
| `blocked` | 외부 결정, 접근 권한, 정보/API, 의존성 때문에 진행 불가 |
| `done` | 완료 기준을 충족한 task |
| `dropped` | 더 이상 진행하지 않기로 한 task |

## 캐시 정책

`/tk:prep`는 입력 자료 해시, prep 지시문 버전, 범위 해시, input identity가 같으면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`가 있으면 다시 생성합니다.

`/tk:gap`은 현재 git commit SHA, `requirements.md` 해시, gap 지시문 버전, 범위 해시가 같고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`가 있으면 다시 분석합니다.

각 명령은 cache hit/miss 이유를 사용자에게 짧게 표시합니다.

## cleanup 경계

`/tk:close`는 archive, branch push, PR 생성, 파일 삭제 같은 cleanup 후보를 제안할 수 있습니다. 하지만 branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.
