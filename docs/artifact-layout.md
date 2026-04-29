# 산출물 구조

권장 프로젝트 로컬 산출물 구조:

```text
.gap/{work_id}/
  inputs/
  to-be.md
  to-be.meta.json
  gap.md
  gap.meta.json
```

`/tigap:prep`은 입력 자료와 대화 맥락을 `to-be.md`로 정리합니다. `/tigap:gap`은 현재 repo/as-is와 `to-be.md`의 차이를 `gap.md`에 기록합니다.

## 브랜치 이름과 작업 ID

현재 git 브랜치가 진행 중인 작업을 나타낸다면 그 브랜치 이름을 사용할 수 있습니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면 변경 가능한 산출물을 쓰기 전에 다음 중 하나를 우선합니다.

- 사용자 승인 후 작업 브랜치를 만들거나 전환
- 사용자에게 짧은 작업 ID를 묻고 `.gap/{work_id}/` 아래에 사용

브랜치를 자동으로 만들거나 전환하지 않습니다. git 브랜치를 확인할 수 없다면 사용자가 제공한 짧은 작업 ID를 사용합니다.

## Git ignore 정책

`.gap/` 산출물은 보통 로컬 작업 노트입니다. Git 저장소에서는 산출물을 만들기 전에 `.gap/`이 ignore 대상인지 또는 의도적으로 추적되는지 확인합니다. 둘 다 아니라면 저장소를 조용히 바꾸지 말고 `.gap/`을 `.gitignore`에 추가하라고 제안합니다.

## 파일 책임

| 파일 | 역할 |
|---|---|
| `inputs/` | `to-be.md`를 만들 때 참고한 원문 자료, 메모, 캡처, 참고 코드 보관 위치 |
| `to-be.md` | 이번 작업의 목표 상태이자 갭 분석 기준 |
| `to-be.meta.json` | `to-be.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `gap.md` | 현재 repo/as-is와 `to-be.md` 사이의 누락, 모호함, 충돌, 위험, 구현 갭 분석 |
| `gap.meta.json` | `gap.md` 재사용 여부를 판단하는 캐시 메타데이터 |

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `prep-needed` | `to-be.md` 없음 | `/tigap:prep` 실행 |
| `analysis-needed` | `to-be.md`는 있고 `gap.md` 없음 | `/tigap:gap` 실행 |
| `analysis-complete` | `gap.md` 있음 | 분석 결과의 `Next Move`를 보고 구현, 보류, 추가 확인 중 선택 |

## 캐시 정책

`/tigap:prep`은 입력 자료 해시, prep 지시문 버전, 범위 해시, input identity가 같으면 기존 `to-be.md`를 재사용합니다. 하나라도 다르거나 `--force`가 있으면 다시 생성합니다.

`/tigap:gap`은 현재 git commit SHA, `to-be.md` 해시, gap 지시문 버전, 범위 해시가 같고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`가 있으면 다시 분석합니다.

각 명령은 cache hit/miss 이유를 사용자에게 짧게 표시합니다.
