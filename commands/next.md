---
description: 현재 TIGAP 워크플로우 단계와 다음 행동을 안내합니다.
---

현재 git 브랜치 기준으로 `.gap/{branch_name}/`을 확인하고 현재 TIGAP 워크플로우 단계를 보고합니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

이 명령은 읽기 전용입니다. 파일이나 브랜치를 만들거나, 수정하거나, 삭제하지 않습니다.

가능하면 현재 git 브랜치 이름을 사용합니다. 브랜치를 확인할 수 없다면 작업 ID를 묻거나 사용자 맥락에서 안전한 짧은 slug를 추론합니다.

다음 순서로 단계를 판단합니다.

1. `.gap/{branch_name}/normalized/source-packet.md`가 없으면 `source-needed`로 보고하고 `/tigap:gap <원천 자료 또는 자료 추출 지시>`를 추천합니다.
2. `source-packet.md`는 있지만 `.gap/{branch_name}/analysis/gap-report.md`가 없으면 `analysis-needed`로 보고하고, 확인된 원천 자료로 `/tigap:gap`을 이어가라고 추천합니다.
3. `gap-report.md`는 있지만 `.gap/{branch_name}/plan/implementation-plan.md`가 없으면 `plan-needed`로 보고하고 `/tigap:gaplan`을 추천합니다.
4. `implementation-plan.md`는 있지만 `.gap/{branch_name}/tasks.md`가 없거나, `tasks.md`가 계획 검토 대기 상태이면 `plan-review-needed`로 보고하고 계획 검토 또는 승인을 추천합니다.
5. `tasks.md`가 있으면 내용을 확인해 다음처럼 보고합니다.
   - 해결되지 않은 Blocked 작업이 Ready 작업을 막고 있으면 `blocked`
   - In Progress 작업이 있으면 `in-progress`
   - Ready에 cleanup 작업만 남았거나 일반 작업이 끝나고 archive 정리가 필요하면 `cleanup-needed`
   - Ready에 미완료 작업이 있으면 `execution-ready`
   - 계획된 작업과 cleanup이 모두 끝났고 차단 사유가 없으면 `complete`

보고에는 다음을 포함합니다.

- 현재 단계
- 현재 브랜치 또는 작업 ID 맥락
- 현재 맥락이 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치로 보이는지 여부
- 근거가 되는 기존 산출물 경로
- 다음 추천 명령 또는 행동
- `plan-review-needed` 단계라면 검토할 `implementation-plan.md` 경로와 승인 후 `tasks.md` 생성이 필요하다는 안내
- 현재 맥락이 기반 브랜치이고 다음 행동이 변경 가능한 작업이라면 브랜치/작업 ID 권장 사항
- `tasks.md`가 있으면 `Done`, `In Progress`, `Ready`, `Blocked` 기준 진행률
- `tasks.md`가 있으면 첫 Ready 또는 In Progress 작업

읽기 전용을 유지합니다. 파일이나 브랜치를 만들거나, 수정하거나, 삭제하지 않습니다.
