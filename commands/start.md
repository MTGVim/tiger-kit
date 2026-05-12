---
description: 아이디어나 source 문서에서 requirements 기준을 만드는 TigerKit primary entry command입니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 아이디어가 흐릿하든 source 문서가 이미 있든 사용자가 시작할 때 `/tk:start` 하나로 requirements 기준 또는 이어서 진행할 다음 행동을 정하게 합니다.

동작 원칙:
- 아이디어가 흐릿하면 `interview mode`로 동작합니다.
- 문서, 메모, 티켓, URL, 파일 경로 같은 source가 있으면 `prep mode`로 동작합니다.
- 기존 work item이 있으면 현재 상태를 짧게 요약하고 이어갈지 안내합니다.
- 요구사항 기준이 이미 충분하면 바로 `/tk:auto` 또는 `/tk:gap`을 추천합니다.
- 질문이 필요하면 하나의 material question만 AskUserQuestion 또는 동등한 사용자 질의 메커니즘으로 묻습니다.

기본 산출물:
- `.tigerkit/{work_id}/requirements.md`
- `.tigerkit/{work_id}/requirements.meta.json`

출력은 receipt-first로 유지합니다.

```text
요구사항 기준을 만들었습니다.
- 기준 파일: `.tigerkit/{work_id}/requirements.md`
- 확인 필요: ...
다음 추천: /tk:auto
```

명시적으로 요청받지 않는 한 구현, commit, push, PR 생성은 하지 않습니다.
