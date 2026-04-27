# 산출물 구조

권장 프로젝트 로컬 산출물 구조:

```text
.gap/{branch_name}/
  sources/
    issue-tracker/
    knowledge-base/
    prd/
    brief/
    code/
  normalized/
    source-packet.md
  analysis/
    gap-report.md
  plan/
    implementation-plan.md
  tasks.md
  execution-log.md
  review-checklist.md
  archive/
    sources/
    plans/
    tasks/
    logs/
    manifest.md
```

## 브랜치 이름과 작업 ID

현재 git 브랜치가 진행 중인 작업을 나타낸다면 그 브랜치 이름을 사용합니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면 변경 가능한 워크플로우 산출물을 쓰기 전에 다음 중 하나를 우선합니다.

- 사용자 승인 후 원천 자료 전용 작업 브랜치를 만들거나 전환
- 사용자에게 짧은 작업 ID를 묻고 `.gap/{work_id}/` 아래에 사용

브랜치를 자동으로 만들거나 전환하지 않습니다. git 브랜치를 확인할 수 없다면 사용자가 제공한 짧은 작업 ID를 사용합니다.

## Archive 정책

완료된 원천 자료, 오래된 계획, 완료된 작업 목록, 실행 로그 스냅샷은 `.gap/{branch_name}/archive/` 아래에 보관할 수 있습니다.

Archive는 현재 작업 흐름에서 산출물을 숨기기 위한 구조이며 삭제가 아닙니다.

권장 하위 경로:

- `archive/sources/`: 완료된 원천 자료 스냅샷
- `archive/plans/`: 더 이상 현재 작업 대상이 아닌 계획 초안
- `archive/tasks/`: 완료되었거나 교체된 작업 목록
- `archive/logs/`: 오래된 실행 로그 스냅샷
- `archive/manifest.md`: 언제, 무엇을, 왜 보관했는지 기록

실제 파일 이동이나 정리는 사용자 승인 없이 수행하지 않습니다. `/tigap:go`는 cleanup 작업에서 archive 대상과 목적을 먼저 보고합니다.

## Git ignore 정책

`.gap/` 산출물은 보통 로컬 워크플로우 노트입니다. Git 저장소에서는 산출물을 만들기 전에 `.gap/`이 ignore 대상인지 또는 의도적으로 추적되는지 확인합니다. 둘 다 아니라면 저장소를 조용히 바꾸지 말고 `.gap/`을 `.gitignore`에 추가하라고 제안합니다.

## 파일 책임

| 파일 | 역할 |
|---|---|
| `source-packet.md` | 정규화된 원천 자료 요약 |
| `gap-report.md` | 누락, 모호함, 충돌, 위험 영역 |
| `implementation-plan.md` | 검토 가능한 구현 계획 초안 |
| `tasks.md` | 계획 검토 후 생성되는 실행용 체크박스 작업 목록 |
| `execution-log.md` | 작업 실행 중 남기는 진행 기록 |
| `review-checklist.md` | 리뷰 전 검증 목록 |

## 워크플로우 단계

`/tigap:next`는 다음 산출물을 기준으로 현재 단계를 판단합니다.

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `source-needed` | `normalized/source-packet.md` 없음 | `/tigap:gap <원천 자료 또는 자료 추출 지시>` 실행 |
| `analysis-needed` | `source-packet.md`는 있고 `analysis/gap-report.md` 없음 | `/tigap:gap` 이어서 실행 |
| `plan-needed` | `gap-report.md`는 있고 `plan/implementation-plan.md` 없음 | `/tigap:gaplan` 실행 |
| `plan-review-needed` | `implementation-plan.md`는 있지만 `tasks.md`가 없거나 계획 검토 대기 상태 | 구현 계획 검토와 승인 |
| `execution-ready` | `tasks.md`에 미완료 Ready 작업 있음 | `/tigap:go` 실행 |
| `in-progress` | `tasks.md`에 In Progress 작업 있음 | 진행 중인 작업 완료 또는 차단 해소 |
| `cleanup-needed` | 일반 작업은 끝났고 cleanup 작업 또는 archive 정리가 남음 | `/tigap:go`로 cleanup 실행 |
| `blocked` | `tasks.md`에 해결되지 않은 차단 작업이 있고 Ready 작업 없음 | 차단 사유 해소 |
| `complete` | 계획된 작업과 cleanup이 모두 끝남 | 리뷰 후 마무리 |
