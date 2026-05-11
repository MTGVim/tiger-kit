---
description: 구현 직후나 merge 전에 review에 필요한 맥락을 정리하고 코드 리뷰를 요청합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, SHA, reviewer 이름은 원문 그대로 유지할 수 있습니다.

목표: 방금 구현한 task, feature, 또는 현재 diff를 기준으로 review에 필요한 맥락을 정리하고, 사용 가능한 review surface가 있으면 코드 리뷰를 요청합니다.

## 언제 쓰나

- task 하나 끝난 직후
- major feature 끝난 직후
- merge 전
- 복잡한 bug fix 후
- 큰 refactor 전후

## 준비할 것

- 무엇을 구현했는지
- 어떤 requirements/gap/task를 기준으로 했는지
- review 범위: current diff / 특정 task / 특정 commit range
- 가능한 경우 `BASE_SHA`, `HEAD_SHA`
- reviewer가 특히 봐야 할 risk 1~3개

## 기본 규칙

- reviewer에게 세션 히스토리를 통째로 넘기지 않습니다.
- 현재 산출물, diff, requirements, task만 기준으로 review 맥락을 만듭니다.
- task 단위 개발이면 task마다 review를 권장합니다.
- 단순 변경이라도 risk가 있으면 생략하지 않습니다.

## 출력

기본 출력은 `Review Brief`입니다.

반드시 포함:
- Review scope
- What changed
- Expected behavior
- Files or diff range
- Verify command or manual check
- Open questions for reviewer

사용 가능한 review mechanism이 있으면 그 surface로 연결합니다. 없으면 `Review Brief`만 남기고 멈춥니다.

## Agent routing

사용 가능한 외부 review surface가 없거나, 코드베이스 내부 맥락을 먼저 정리해야 하면 `tk-ru`를 reviewer로 사용합니다. API readiness, assumed contract, `TK-API-*` 잔여 risk가 review 핵심이면 `tk-sif-muna` 결과를 함께 참고합니다. UI/UX review는 `tk-nemelex-xobeh`, screenshot 기반 review는 `tk-ashenzari`를 사용할 수 있습니다.

reviewer에게 세션 히스토리를 통째로 넘기지 말고 current diff, 관련 task, requirements/gap/plan 경로, 검증 결과만 전달합니다.

## 처리 후

- Critical/Important issue는 다음 구현 전 우선 처리합니다.
- Minor issue는 따로 모아둘 수 있습니다.
- reviewer가 틀렸다고 판단되면 기술 근거로 반박합니다.

명시적으로 요청받지 않는 한 commit, push, PR 생성은 실행하지 않습니다.
