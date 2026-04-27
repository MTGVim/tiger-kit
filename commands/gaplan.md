---
description: 갭 분석 보고서를 구현 계획과 작업 목록으로 바꿉니다.
---

이 플러그인의 `gaplan` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. TIGAP 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.gap/{branch_name}/analysis/gap-report.md`를 읽고, `.gap/{branch_name}/plan/implementation-plan.md`와 `.gap/{branch_name}/tasks.md`를 작성합니다.

변경 가능한 계획 산출물을 쓰기 전에 브랜치/작업 ID 맥락을 확인합니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면 원천 자료에 맞는 작업 브랜치나 명시적 작업 ID로 계속할 것을 권장합니다. 사용자 승인 없이 브랜치를 만들거나 전환하지 않습니다.

계획 모드를 유지합니다. 명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.
