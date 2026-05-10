---
description: TigerKit의 권장 loop와 command 선택 기준을 짧게 안내합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자가 TigerKit에서 무엇부터 실행해야 하는지 빠르게 고를 수 있도록 권장 loop와 보조 command/skill을 짧게 소개합니다.

기본 출력은 `TigerKit Help`입니다.

반드시 포함할 권장 loop:

```text
/tk:prep       # source -> requirements.md
/tk:gap        # requirements.md -> gap.md
/tk:plan       # gap.md -> plan.md
/tk:breakdown  # gap.md 또는 plan.md -> tasks.md
/tk:do         # task 1건 구현/검증
/tk:do-all     # 남은 task 전체 구현
/tk:gap        # 구현 후 재평가
... 반복
/tk:close      # 종료 정리
```

상태 확인/보조 command:

```text
/tk:state      # .tigerkit 전체 상태
/tk:next       # 다음 command 또는 다음 task 1개 추천
/tk:auto       # gap -> plan -> breakdown -> do-all -> gap 1사이클 자율주행
```

보조 기능도 짧게 표시합니다.

```text
/tk:mwhat      # 긴 답변 해독. 자연어 trigger는 `뭣?`만
/tk:grill-me   # prep/plan에서 deep interview 보조
/tk:caveman    # 응답 초압축 skill alias
/tk:prototype  # FE UI prototype variants
/tk:reflect    # maintenance 회고. 종료 루틴은 /tk:close 우선
/tk:improve    # knowledge layer audit
```

마지막 줄에는 현재 상황별 다음 추천 1개를 제안합니다.

예:
- 요구사항 기준이 없으면 `다음 추천: /tk:prep`
- `requirements.md`만 있으면 `다음 추천: /tk:gap`
- `gap.md`가 있으면 `다음 추천: /tk:plan`
- `tasks.md`가 있고 실행 가능 task가 있으면 `다음 추천: /tk:do`
- task를 모두 끝냈으면 `다음 추천: /tk:gap`
- gap 재확인까지 끝났으면 `다음 추천: /tk:close`

명시적으로 요청받지 않는 한 파일을 수정하지 않습니다.
