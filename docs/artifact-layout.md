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

`/tk:prep`는 입력 자료와 대화 맥락을 `requirements.md`로 정리합니다. `/tk:gap`은 현재 repo 상태와 `requirements.md`의 차이를 `gap.md`에 기록합니다. `/tk:plan`은 요구사항 또는 gap 결과를 승인 가능한 실행계획으로 정리합니다. `/tk:breakdown`과 `/tk:tasks`는 실행 단위와 상태를 `tasks.md`에 둡니다. `/tk:close`는 세션 종료 요약을 필요할 때 `close.md`로 남길 수 있습니다.

`/tk:reflect`는 maintenance alias로 유지되지만 `prep → gap → plan → breakdown → tasks/next → close` 라이프사이클의 필수 단계는 아닙니다.

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
| `gap.md` | 현재 상태와 `requirements.md` 사이의 coverage/gap 분석 |
| `gap.meta.json` | `gap.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `plan.md` | 구현 묶음, 선행관계, 검증 순서를 담은 실행계획 |
| `tasks.md` | 작은 실행 task, 상태, 완료 기준, blocker 목록 |
| `close.md` | 선택적으로 남기는 세션 종료 요약, 남은 gap, 검증 상태, cleanup 후보 |

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `req-needed` | `requirements.md` 없음 | `/tk:prep` 실행 |
| `gap-needed` | `requirements.md`는 있고 `gap.md` 없음 | `/tk:gap` 실행 |
| `plan-needed` | `gap.md`는 있고 `plan.md` 없음 | `/tk:plan` 실행 |
| `tasks-needed` | `plan.md` 또는 `gap.md`는 있고 `tasks.md` 없음 | `/tk:breakdown` 실행 |
| `task-ready` | 실행 가능한 `todo` 또는 `in_progress` task 있음 | `/tk:next` 실행 |
| `close-needed` | 세션 종료 전 상태 정리 필요 | `/tk:close` 실행 |

## task 상태값

`tasks.md`의 상태값은 아래만 사용합니다.

| 상태 | 의미 |
|---|---|
| `todo` | 아직 시작하지 않은 실행 가능 task |
| `in_progress` | 현재 진행 중인 task |
| `blocked` | 외부 결정, 정보, 선행 작업 때문에 진행 불가 |
| `done` | 완료 기준을 충족한 task |
| `dropped` | 더 이상 진행하지 않기로 한 task |

## 캐시 정책

`/tk:prep`는 입력 자료 해시, prep 지시문 버전, 범위 해시, input identity가 같으면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`가 있으면 다시 생성합니다.

`/tk:gap`은 현재 git commit SHA, `requirements.md` 해시, gap 지시문 버전, 범위 해시가 같고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`가 있으면 다시 분석합니다.

각 명령은 cache hit/miss 이유를 사용자에게 짧게 표시합니다.

## cleanup 경계

`/tk:close`는 archive, branch push, PR 생성, 파일 삭제 같은 cleanup 후보를 제안할 수 있습니다. 하지만 branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.
