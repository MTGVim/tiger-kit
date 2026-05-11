---
description: requirements.md와 현재 상태 사이의 요구사항 coverage와 남은 gap을 분석합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md`에 정리된 요구사항 기준을 읽고, 필요한 범위에서 현재 구현, 문서, 테스트, 관찰 가능한 동작을 확인한 뒤 요구사항 coverage와 남은 gap을 정리한 분석 결과를 작성합니다.

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 말고, source 문서나 메모가 있으면 `/tk:prep`, 아이디어가 흐릿하면 `/tk:interview`로 요구사항 기준과 작업 대상을 먼저 정리하라고 안내합니다.

보고서는 `판정`, `요구사항 커버리지`, `남은 갭`, `API 계약 차이`, `확인 불가`, `메모`를 포함합니다. `판정` 값은 `GAPS_FOUND`, `NO_GAPS_FOUND`, `UNVERIFIABLE` 중 하나를 사용합니다. 확인 불가 요구사항이 하나라도 있으면 `NO_GAPS_FOUND`로 판정하지 않습니다.

`요구사항 커버리지`, `남은 갭`, `API 계약 차이`, `확인 불가`는 항상 Markdown 표로 작성합니다. 해당 항목이 없더라도 헤더를 유지하고 `없음` 행을 남깁니다. mock 또는 assumed contract 흔적이 있고 실제 API나 공식 contract를 관찰할 수 있으면 contract mismatch와 implementation gap을 구분합니다.

요구사항에 API 의존성이 있는데 현재 repo에서 실제 API나 공식 contract를 확인할 수 없으면 `확인 불가`에 외부 API/문서 확인 필요를 남깁니다. 기존 `mock_api_contract` 또는 `TK-API-* blocked`가 있거나 API 부재가 계속 관찰되면, 사용자가 이번 범위 밖이라고 명시하지 않은 한 채팅 응답 끝에서 실제 API나 공식 contract가 준비됐는지 cross-check 질문을 합니다. 단 `/tk:auto` 내부에서 호출된 경우에는 질문으로 멈추지 않고 API/contract 확인 필요를 follow-up으로 기록합니다.

## Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다.

- repo 내부 coverage와 영향 범위 탐색이 넓으면 Claude Code 내장 `Explore`를 사용합니다.
- API 부재, official contract 확인, `mock_api_contract` 흔적과 실제 API drift 비교가 필요하면 `tk-sif-muna`를 사용합니다.
- screenshot, PDF, diagram 같은 시각 자료가 요구사항 근거면 `tk-ashenzari`를 사용합니다.
- gap 판정이 architecture나 correctness 판단에 크게 의존하면 `tk-ru`로 second opinion을 받을 수 있습니다.

agent 결과는 근거로만 쓰고, 최종 `gap.md` 작성과 Verdict 책임은 이 명령을 실행하는 main agent가 가집니다.

기본 산출물:
- `.tigerkit/{work_id}/gap.md`
- `.tigerkit/{work_id}/gap.meta.json`

`gap.meta.json`에는 cache 판단에 필요한 git commit, requirements hash, gap 지시문 버전, 범위를 남깁니다. 같은 git commit, requirements 해시, gap 지시문 버전, 범위이고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`가 있으면 다시 분석합니다.

명시적으로 요청받지 않는 한 이 명령에서는 코드를 구현하거나 새로운 구현 계획을 만들지 않습니다.

채팅 응답 마지막에는 기본적으로 `다음 추천: /tk:plan`을 표시합니다. 실제 API나 공식 contract 확인이 선행되어야 하면 그 확인 요청을 먼저 짧게 밝힌 뒤 `/tk:plan`을 안내합니다.
