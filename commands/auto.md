---
description: requirements.md가 준비된 뒤 gap -> plan -> breakdown -> do-all -> gap 1사이클을 자율주행합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 테스트 이름, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md`가 준비된 상태에서 `gap -> plan -> breakdown -> do-all -> gap` 1사이클만 자율주행으로 처리합니다.

## 시작 조건

- work_id가 명확해야 합니다.
- `requirements.md`가 있어야 합니다.
- worktree나 작업 브랜치 경계가 필요한 경우 먼저 사용자 승인을 따릅니다.

`requirements.md`가 없으면 자동으로 인터뷰를 시작하지 않고 `/tk:prep`를 추천하고 멈춥니다.

## 1사이클 범위

정확히 아래만 수행합니다.

1. `/tk:gap`에 준해 gap 분석
2. `/tk:plan`에 준해 실행계획 정리. API나 공식 contract를 확인할 수 없고 사용자가 범위 밖이라고 명시하지 않았으면 기본값 `mock_api_contract`로 진행합니다.
3. `/tk:breakdown`에 준해 task 분해. `mock_api_contract` slice는 일반 task를 계속 만들고 `TK-API-*` follow-up만 blocked로 둡니다.
4. `/tk:do-all`에 준해 실행 가능한 task 처리. 코드 수정이 포함된 task는 task별 검증 통과 후 local commit으로 남깁니다.
5. `/tk:gap`으로 재평가 1회

## TDD와 실행 방식

각 task 구현은 `/tk:do` 규칙을 따릅니다.

- behavior/API/business logic/bug fix/regression risk면 TDD 추천
- docs/prompt/manifest/config/copy 변경은 TDD 생략 가능
- 작은 task는 inline, 큰 독립 task는 sub-agent 방식을 스스로 판단
- agent routing은 `/tk:do-all` 규칙을 따릅니다. Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다. API/contract 확인은 `tk-sif-muna`, bounded implementation은 `tk-trog`, cleanup/docs hygiene은 `tk-elyvilon`, UI/prototype은 `tk-nemelex-xobeh`, visual artifact 분석은 `tk-ashenzari`, review/risk 판단은 `tk-ru`를 우선 고려합니다.

## 중단 조건

아래 상황이면 즉시 멈추고 보고합니다.

- work_id 불명확
- `requirements.md` 부재
- 외부 blocker 존재. 단 `mock_api_contract`에 따른 `TK-API-* blocked`만 있으면 일반 task 진행은 멈추지 않고 merge blocker로 보고합니다.
- 요구사항 모호함. 이 경우 `blocked`로 만들지 않고 `Clarification Actions`와 다음 clarification 경로를 보고합니다.
- 검증 실패 반복
- 기반 브랜치에서 변경 승인이 필요함
- 새 gap이 생겨 계획 재합의가 필요함

새 gap이 생기면 1사이클에서 멈춥니다. 자동으로 2사이클째 구현으로 들어가지 않습니다.

## 출력

짧게 아래만 포함합니다.

- 사용한 work_id
- 수행한 단계
- 완료 task 수와 blocked 수
- 검증 결과
- 생성한 commit 수와 commit hash
- 마지막 gap 재확인 결과
- unresolved `TK-API-*`가 있으면 API/contract 확인 필요 여부
- `다음 추천: /tk:plan`, `/tk:do-all`, `/tk:next`, 또는 `/tk:close`
