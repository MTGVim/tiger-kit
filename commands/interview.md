---
description: 흐릿한 아이디어를 brainstorming과 deep interview로 좁혀 requirements.md 기준 또는 queue 반영 후보로 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자의 머릿속에만 있거나 아직 흐릿한 아이디어를 공동 설계형 brainstorming과 ambiguity reduction interview로 좁혀, 이후 `/tk:gap`의 기준이 되는 `.tigerkit/{work_id}/requirements.md`로 정리합니다. 이미 진행 중인 task queue를 바꿔야 한다면 직접 갱신하지 않고 `/tk:plan`에서 반영할 queue 변경 후보만 정리합니다.

`/tk:prep`는 이미 있는 source of truth를 정규화합니다. `/tk:interview`는 source가 아직 대화 속에 있을 때 질문과 대안 비교로 source를 만들어냅니다.

## 기본 원칙

- 구현하지 않습니다.
- 계획이나 task를 확정하지 않습니다.
- 한 응답에는 material question을 최대 하나만 둡니다.
- 사용자 답변이 필요한 질문은 일반 prose로 섞지 말고 `AskUserQuestion` 또는 동등한 사용자 질의 메커니즘으로 묻습니다.
- 질문하지 않아도 진행 가능한 낮은 리스크의 세부사항은 묻지 않고 명시적 가정으로 기록한 뒤 계속 진행합니다.
- 질문 전 맥락 설명이 필요하면 내부 상태 레이블이 아니라 자연스러운 1~2문장으로만 설명합니다.
- 코드베이스를 읽어서 답할 수 있는 사실은 사용자에게 묻기 전에 확인합니다.
- 사용자의 free-text 답변은 압축해 의미를 잃지 말고 결정 로그에 반영합니다.
- 모호함을 terminal `blocked`로 만들지 않고, 확인해야 할 판단 또는 `Clarification Actions` 후보로 둡니다.
- `현재 가정`, `남은 모호함`, `다음 질문` 같은 내부 상태 레이블을 사용자-facing 진행 출력에 그대로 노출하지 않습니다.

## work_id 결정

1. 사용자가 work_id 또는 `.tigerkit/{work_id}/` 경로를 지정했으면 그것을 사용합니다.
2. 현재 대화에서 자연스러운 작업명이 명확하면 후보 work_id를 제안합니다.
3. 기존 `.tigerkit/` 상태와 이어지는 작업이면 해당 work_id를 확인합니다.
4. 후보가 없거나 여러 개면 추측하지 말고 work_id를 물어봅니다.

## 진행 방식

1. 입력을 한 문장으로 재진술합니다.
2. 현재 repo나 기존 `.tigerkit/{work_id}/`에서 확인 가능한 사실을 짧게 확인합니다.
3. 문제가 넓으면 2~3개 접근안을 제시하고 trade-off와 추천 기본값을 밝힙니다.
4. 사용자가 방향을 고르거나 수정하면 가장 큰 모호함 하나를 질문합니다.
5. 답변마다 아래 ledger를 갱신합니다.
   - `결정`: 사용자가 확정한 것
   - `근거`: code, user, research, assumption 중 어디서 왔는지
   - `제약`: 반드시 지킬 조건
   - `제외 범위`: 하지 않을 것
   - `미해결`: 다음 질문 후보
6. 모호함이 줄었지만 아직 material decision이 남아 있으면 계속 질문합니다.
7. 종료 전에 요구사항을 짧게 재진술하고 사용자에게 맞는지 확인합니다.
8. 사용자가 승인하면 상황에 맞는 산출물 또는 queue 변경 후보를 만듭니다.

## 질문 기준

우선순위:

1. 목표가 무엇인지
2. 성공 기준이 무엇인지
3. 제외 범위가 무엇인지
4. 사용자 결정이 필요한 trade-off가 무엇인지
5. 외부 blocker나 API/contract 확인이 필요한지
6. 기존 task나 plan을 바꿔야 하는지

질문은 1~2문장으로 유지합니다. 가능하면 선택지를 줍니다.

묻지 않아도 되는 항목:
- 기존 convention으로 합리적으로 추론 가능한 구현 세부사항
- reversible한 naming, helper 구조, file placement
- 지금 결정하지 않아도 요구사항 기준 정리에 영향이 작은 low-risk detail

## 산출물 결정

기본 산출물:
- `.tigerkit/{work_id}/requirements.md`
- `.tigerkit/{work_id}/requirements.meta.json`

`requirements.meta.json`에는 `source_type: "interview"`, `interview_prompt_version`, `scope_hash`, `conversation_or_decision_hash`, `input_identities`, `provenance`를 남깁니다. `/tk:interview`의 metadata는 cache 재사용보다 결정 출처와 범위 추적이 기본 목적입니다. `source_type == "interview"`, `interview_prompt_version`, `scope_hash`, `conversation_or_decision_hash`, `input_identities`가 모두 일치할 때만 기존 `requirements.md`를 재사용할 수 있습니다. 사용자가 새 답변을 추가하거나 `--force`를 붙이면 다시 정리합니다.

아래 상황이면 파일을 바로 쓰지 않고 queue 변경 후보만 제안합니다.

- 이미 `tasks.md`가 있고 특정 task의 완료 기준만 바꾸면 충분함
- 새로 발견된 문제가 작은 task 하나로 명확함
- 기존 task를 split, merge, blocked, dropped, revised 처리해야 함
- 외부 의존, 권한, API/contract, human decision 때문에 `Shared Blockers` 후보가 필요함
- 요구사항 모호함만 남아 `Clarification Actions` 후보가 적절함

queue 변경 후보는 `/tk:plan`에서 반영할 wording으로만 정리합니다. 기존 `tasks.md`의 insertion, revision, split, merge, blocked, dropped 판단을 이 명령에서 확정하지 않습니다.

- `Task insertion`
- `Task revision`
- `Clarification Action`
- `Shared Blocker`

## requirements.md 형식

`requirements.md`를 작성할 때는 아래 섹션을 포함합니다.

- 배경
- 문제
- 목표
- 비목표
- 요구사항
- 수용 신호
- 제약
- 열린 질문
- 출처 메모

`요구사항` 섹션은 가능하면 stable requirement ID와 적용 방식을 함께 기록합니다.

| ID | Type | Requirement | Source | Application |
|---|---|---|---|---|
| R-001 | behavior/copy/UI/... | 요구사항 본문 | user/research/doc/code | `verbatim` / `semantic` / `flexible` / `assumption` |

- `verbatim`: 문구, 값, 형태를 그대로 사용해야 함
- `semantic`: 의미를 지키면 구현은 유연함
- `flexible`: 구현자 재량 허용. 단 결정 기록 필요
- `assumption`: 임시 가정. 추후 확인 필요

`열린 질문`이 남아 있으면 각 항목에 다음 행동을 적습니다. 실제 API나 공식 contract가 없고 이번 범위 밖이라고 명시되지 않았다면, API/contract 확인 필요를 남깁니다.

## 완료 조건

아래가 모두 충족되면 interview를 멈출 수 있습니다.

- 목표를 한 문장으로 설명할 수 있음
- 성공 기준이 관찰 가능함
- 제외 범위가 명시됨
- 주요 trade-off의 선택 또는 기본 가정이 기록됨
- 외부 blocker와 요구사항 모호함이 분리됨
- 사용자가 최종 재진술을 승인함

사용자가 `done`, `됐어`, `그만`처럼 말해도 위 조건이 부족하면 부족한 항목 하나만 짚고 계속할지, 현재 상태를 초안으로 저장할지 물어봅니다.

## 출력

진행 중 사용자에게 질문해야 하면 `AskUserQuestion` 또는 동등한 사용자 질의 메커니즘을 사용합니다.

질문 문구는 사람과 협업하듯 자연스럽게 작성합니다. 필요한 맥락은 1~2문장으로만 설명하고, 가능한 경우 선택지를 제공합니다.

내부 상태는 decision ledger와 metadata에 남기되, 사용자-facing 진행 출력에서는 `현재 가정`, `남은 모호함`, `다음 질문` 같은 블록을 그대로 노출하지 않습니다.

완료 시에는 아래만 짧게 보고합니다.

- 생성/제안한 산출물
- 확정된 핵심 요구사항 3개 이내
- 남은 열린 질문 또는 queue 변경 후보
- `requirements.md`를 만들었으면 `다음 추천: /tk:gap`, queue 변경 후보만 제안했으면 `다음 추천: /tk:plan`

## 안전 경계

- 구현, commit, push, PR 생성은 하지 않습니다.
- `tasks.md`는 직접 수정하지 않습니다. queue 변경은 후보 wording만 제안하고 `/tk:plan`으로 넘깁니다.
- branch 생성이나 전환은 사용자 승인 없이 하지 않습니다.
- 긴 design doc을 만들지 않습니다.
