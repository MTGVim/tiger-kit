---
description: TigerKit의 권장 primary workflow와 command 선택 기준을 짧게 안내합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자가 TigerKit에서 무엇부터 실행해야 하는지 빠르게 고를 수 있도록 primary workflow, advanced command, specialist command를 짧게 소개합니다.

기본 출력은 `TigerKit Help`입니다.

반드시 포함할 primary workflow:

```text
/tk:start      # 아이디어나 source에서 requirements 기준 만들기
/tk:auto       # 현재 상태에서 안전한 1 cycle 진행
/tk:next       # 다음 command 또는 다음 task 1개 추천
/tk:state      # .tigerkit 전체 상태 요약
/tk:close      # 종료 정리
```

advanced command:

```text
/tk:do         # task 1건 수동 구현/검증
/tk:grill-me   # 고위험 모호함 압박 질문
/tk:gap        # requirements 기준 gap 분석
/tk:plan       # gap 기준 실행계획 정리
/tk:breakdown  # plan/gap을 tasks.md로 분해
```

specialist / utility:

```text
/tk:mwhat      # 긴 답변 해독. 자연어 trigger는 `뭣?`만
/tk:prototype  # FE UI prototype variants
/tk:review     # 구현 직후 또는 merge 전 review brief
/tk:review-fix # review feedback 검증 후 반영
/tk:caveman    # 응답 초압축 skill alias
```

legacy note:

```text
/tk:interview, /tk:prep  # `/tk:start` 내부 mode 또는 legacy 진입점
```

새 skill 작성이나 기존 skill 경량화 요청은 `write-a-skill` skill이 맡는다고 짧게 안내할 수 있습니다.

마지막 줄에는 현재 상황별 다음 추천 1개를 제안합니다.

예:
- 요구사항 기준이 없고 아이디어가 흐릿하면 `다음 추천: /tk:start`
- source 문서나 메모가 있으면 `다음 추천: /tk:start`
- `requirements.md`만 있으면 `다음 추천: /tk:auto`
- `gap.md`가 있으면 `다음 추천: /tk:plan`
- `tasks.md`가 있고 실행 가능 task가 있으면 `다음 추천: /tk:auto` 또는 `/tk:do`
- task를 모두 끝냈으면 `다음 추천: /tk:gap`
- gap 재확인까지 끝났으면 `다음 추천: /tk:close`

명시적으로 요청받지 않는 한 파일을 수정하지 않습니다.
