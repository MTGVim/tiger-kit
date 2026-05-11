---
description: 세션 종료 전 남은 gap, task 상태, 검증, cleanup 후보를 짧게 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 현재 세션을 닫기 전에 `.tigerkit/{work_id}/` 산출물, git 상태, 남은 gap/task, 검증 상태, 다음 재진입 포인트를 짧게 정리합니다.

기본 출력은 `Close Report`입니다. 필요하면 사용자의 승인 후 `.tigerkit/{work_id}/close.md`를 작성할 수 있습니다.

확인 항목:
- 남은 gap 또는 blocked task
- unresolved `TK-API-*` follow-up. 남아 있으면 사용자가 mock 포함 merge를 명시적으로 허용하지 않는 한 merge blocker와 incomplete 상태로 표시합니다.
- 완료한 task와 아직 남은 task
- task를 표나 목록으로 보여줄 때는 task ID만 적지 말고, 각 task에 묶인 gap 또는 포함 작업을 한 줄로 함께 적습니다.
- 가능하면 `포함 작업` 또는 유사한 칼럼명을 사용합니다.
- 실행한 검증과 실패한 검증
- tail gap check 필요 여부와 결과
- archive 또는 cleanup 후보
- 다음에 이어갈 명령 1개

branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.

`/tk:close`는 작업 종료 상태 정리용 command입니다. 세션 learning이나 knowledge patch 회고는 `/tk:reflect`가 맡습니다.

종료 전에 task가 모두 끝났고 blocked task가 없는데 tail gap check가 아직 수행되지 않았다면 gap을 한 번만 다시 확인합니다. task 완료와 gap 해소를 같은 뜻으로 취급하지 않습니다. 새 gap이 있으면 `/tk:plan`을 추천하고, 새 gap이 없으면 `다음 추천: 없음`을 표시합니다.
