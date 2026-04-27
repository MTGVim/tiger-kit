---
name: next
description: 현재 TIGAP 산출물을 읽어 workflow 단계와 다음 행동을 판단합니다. 상태 확인, 단계 판정, 진행률 보고, 다음 명령 추천이 필요할 때 반드시 사용합니다. 이 스킬은 읽기 전용이어야 하며 파일, 브랜치, git 상태를 변경하지 않습니다.
---

# next

## 목적

`.gap/{branch_name}/` 산출물을 읽어 현재 TIGAP 단계와 다음 행동을 보고합니다.

사용자가 “지금 어디까지 왔어?”, “다음에 뭐 하면 돼?”, “현재 TIGAP 상태 알려줘”, “tasks 진행률 알려줘”처럼 상태 확인을 요청할 때 이 스킬을 사용합니다.

## 읽기 전용 원칙

사용자에게 보이는 응답은 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

이 스킬은 항상 읽기 전용입니다.

- 파일을 만들거나 수정하거나 삭제하지 않습니다.
- 브랜치를 만들거나 전환하지 않습니다.
- git 상태를 바꾸는 명령을 실행하지 않습니다.
- 산출물이 없어도 임의로 `.gap/` 파일을 생성하지 않습니다.

## 산출물 위치

가능하면 현재 git 브랜치 이름을 사용합니다.

```text
.gap/{branch_name}/
```

브랜치를 확인할 수 없거나 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면, 작업 ID 맥락이 있는지 확인합니다. 다음 행동이 변경 가능한 작업이라면 작업 브랜치나 명시적 작업 ID를 먼저 정하라고 권장만 하고, 직접 만들거나 전환하지 않습니다.

## 단계 판정 순서

다음 순서로 현재 단계를 판단합니다.

1. `normalized/source-packet.md`가 없으면 `source-needed`
2. `source-packet.md`는 있지만 `analysis/gap-report.md`가 없으면 `analysis-needed`
3. `gap-report.md`는 있지만 `plan/implementation-plan.md`가 없으면 `plan-needed`
4. `implementation-plan.md`는 있지만 `tasks.md`가 없거나 계획 검토 대기 상태이면 `plan-review-needed`
5. `tasks.md`가 있으면 작업 상태로 판단
   - 해결되지 않은 Blocked 작업이 있고 Ready 작업이 없으면 `blocked`
   - In Progress 작업이 있으면 `in-progress`
   - Ready에 cleanup 작업만 남았거나 일반 작업이 끝나고 archive 정리가 필요하면 `cleanup-needed`
   - Ready에 미완료 작업이 있으면 `execution-ready`
   - 계획된 작업과 cleanup이 모두 끝났고 차단 사유가 없으면 `complete`

## tasks.md 진행률

`tasks.md`가 있으면 체크박스 작업을 다음 기준으로 세어 보고합니다.

- `Done`: 완료된 작업
- `In Progress`: 진행 중인 작업
- `Ready`: 실행 가능한 다음 작업
- `Blocked`: 차단된 작업

첫 `In Progress` 작업이 있으면 이어서 끝낼 작업으로 보고합니다. `In Progress`가 없고 `Ready` 작업이 있으면 첫 Ready 작업을 다음 작업으로 보고합니다.

## 보고 형식

응답에는 다음을 포함합니다.

- 현재 단계
- 현재 브랜치 또는 작업 ID 맥락
- 기반 브랜치로 보이는지 여부
- 근거가 되는 기존 산출물 경로
- 다음 추천 명령 또는 행동
- 읽기 전용으로 확인했으며 파일 생성, 수정, 삭제와 git 상태 변경을 하지 않았다는 안전 확인
- `plan-review-needed`라면 검토할 `implementation-plan.md` 경로와 승인 후 `tasks.md` 생성이 필요하다는 안내
- 다음 행동이 변경 가능한 작업이고 현재 맥락이 기반 브랜치라면 브랜치/작업 ID 권장 사항
- `tasks.md`가 있으면 Done/In Progress/Ready/Blocked 진행률
- `tasks.md`가 있으면 첫 In Progress 또는 Ready 작업

## 추천 명령

단계별 추천은 다음을 기본으로 합니다.

```text
source-needed       -> /tigap:gap <원천 자료 또는 자료 추출 지시>
analysis-needed     -> /tigap:gap
plan-needed         -> /tigap:gaplan
plan-review-needed  -> 구현 계획 검토와 승인
execution-ready     -> /tigap:go
in-progress         -> /tigap:go
cleanup-needed      -> /tigap:go
blocked             -> 차단 사유 해소
complete            -> 리뷰 후 마무리
```

## 완료 기준

이 스킬은 파일이나 git 상태를 바꾸지 않고 현재 단계, 근거, 다음 행동, 읽기 전용 안전 확인을 한글로 보고하면 완료됩니다.
