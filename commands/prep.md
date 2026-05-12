---
description: 외부 요구사항 소스를 정제해 이후 계획과 갭 확인의 기준이 되는 requirements.md로 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: Jira 티켓, Confluence 문서, PRD, 사용자 메모, 회의 요약, 기존 요구사항 문서 같은 source of truth 후보를 중복 제거, 충돌/모호점 표시, acceptance signal, scope boundary 중심으로 정규화해 이후 계획과 갭 확인의 기준이 되는 요구사항 기준 문서로 정리합니다.

먼저 앞선 대화에서 추론한 스펙명 또는 작업 ID를 제안하고, 그 이름으로 `.tigerkit/{work_id}/`에 정리해도 되는지 확인합니다.

아이디어가 아직 퍼져 있거나 추상적이면 바로 문서화를 강행하지 말고 `/tk:interview`를 추천하거나, 범위, 성공 조건, 제외 범위를 먼저 좁혀서 정리합니다.

기본 산출물:
- `.tigerkit/{work_id}/requirements.md`
- `.tigerkit/{work_id}/requirements.meta.json`
- 필요 시 `.tigerkit/{work_id}/inputs/`

`requirements.meta.json`에는 cache 판단에 필요한 `input_source_hash`, `prep_prompt_version`, `scope_hash`, `input_identities`를 남깁니다. 같은 입력 자료, prep 지시문 버전, 범위, input identity로 다시 실행하면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`가 있으면 기존 cache를 우회하고 다시 생성합니다.

`requirements.md`의 `요구사항` 섹션은 가능하면 stable requirement ID와 적용 방식을 함께 기록합니다.

| ID | Type | Requirement | Source | Application |
|---|---|---|---|---|
| R-001 | behavior/copy/UI/... | 요구사항 본문 | user/research/doc/code | `verbatim` / `semantic` / `flexible` / `assumption` |

사용자-visible copy가 source에 명시되어 있으면 기본적으로 `verbatim`으로 취급합니다.

## Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다.

- source가 screenshot, PDF, diagram, UI capture 같은 visual artifact면 `tk-ashenzari`로 관찰 결과를 먼저 구조화할 수 있습니다.

agent를 사용해도 최종 `requirements.md`, metadata, scope boundary 판단은 이 명령을 실행하는 main agent가 책임집니다.

기존 `tasks.md`가 있고 새 입력이 task insertion, task revision, clarification, shared blocker 수준의 course correction이면 `requirements.md`를 덮어쓰지 말고 queue 변경 후보만 제안한 뒤 `/tk:plan`으로 넘깁니다.

명시적으로 요청받지 않는 한 이 명령에서는 구현 계획을 최종 확정하거나 코드를 수정하지 않습니다.

채팅 응답 마지막에는 source가 충분히 정리되어 `requirements.md`를 만들었거나 재사용했으면 `다음 추천: /tk:gap`을 표시합니다. 아이디어가 아직 흐리거나 source 기준이 부족하면 `requirements.md`를 만들지 말고 `다음 추천: /tk:interview`를 표시합니다. 기존 task queue에 반영할 course correction 후보만 정리했다면 `다음 추천: /tk:plan`을 표시합니다.
