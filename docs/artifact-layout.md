# 산출물 구조

권장 프로젝트 로컬 산출물 구조:

```text
.gap/{work_id}/
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
  archive/
    sources/
    analysis/
    manifest.md
```

## 브랜치 이름과 작업 ID

현재 git 브랜치가 진행 중인 작업을 나타낸다면 그 브랜치 이름을 사용할 수 있습니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면 변경 가능한 산출물을 쓰기 전에 다음 중 하나를 우선합니다.

- 사용자 승인 후 작업 브랜치를 만들거나 전환
- 사용자에게 짧은 작업 ID를 묻고 `.gap/{work_id}/` 아래에 사용

브랜치를 자동으로 만들거나 전환하지 않습니다. git 브랜치를 확인할 수 없다면 사용자가 제공한 짧은 작업 ID를 사용합니다.

## Archive 정책

완료된 기준 자료나 오래된 갭 분석 보고서는 `.gap/{work_id}/archive/` 아래에 보관할 수 있습니다.

Archive는 현재 작업 흐름에서 산출물을 숨기기 위한 구조이며 삭제가 아닙니다.

권장 하위 경로:

- `archive/sources/`: 완료된 자료 스냅샷
- `archive/analysis/`: 더 이상 현재 기준이 아닌 갭 분석 보고서
- `archive/manifest.md`: 언제, 무엇을, 왜 보관했는지 기록

실제 파일 이동이나 정리는 사용자 승인 없이 수행하지 않습니다.

## Git ignore 정책

`.gap/` 산출물은 보통 로컬 작업 노트입니다. Git 저장소에서는 산출물을 만들기 전에 `.gap/`이 ignore 대상인지 또는 의도적으로 추적되는지 확인합니다. 둘 다 아니라면 저장소를 조용히 바꾸지 말고 `.gap/`을 `.gitignore`에 추가하라고 제안합니다.

## 파일 책임

| 파일 | 역할 |
|---|---|
| `source-packet.md` | 이번 작업의 기준 자료 스냅샷 |
| `gap-report.md` | 기준 대비 누락, 모호함, 충돌, 위험, 구현 갭 분석 |

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `prep-needed` | `normalized/source-packet.md` 없음 | `/tigap:prep` 실행 |
| `analysis-needed` | `source-packet.md`는 있고 `analysis/gap-report.md` 없음 | `/tigap:gap` 실행 |
| `analysis-complete` | `gap-report.md` 있음 | 분석 결과를 보고 구현, 보류, 추가 확인 중 선택 |
