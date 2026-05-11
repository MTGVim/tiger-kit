# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. 인용한 원문, 코드, 명령어, 경로, 식별자는 원문 그대로 유지할 수 있습니다.

## 브랜치와 작업 ID

변경 가능한 작업 산출물을 쓰기 전에 작업과 연결되는 브랜치 또는 작업 ID를 우선 사용합니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면 작업 브랜치를 만들거나 전환할지, 또는 `.tigerkit/{work_id}/` 아래에서 사용할 작업 ID를 정할지 물어봅니다.

브랜치 생성과 전환은 사용자 승인 없이 조용히 수행하지 않습니다.

## 권장 흐름

권장 loop:

```text
/tk:prep
/tk:gap
/tk:plan
/tk:breakdown
/tk:do 또는 /tk:do-all
/tk:gap
... 반복
/tk:close
```

자주 쓰는 유틸:

```text
/tk:state
/tk:next
/tk:auto
```

세부 command:

```text
/tk:plan
/tk:breakdown
```

core workflow command와 상태 조회 command는 채팅 응답 마지막에 `다음 추천: ...` 한 줄을 붙여 다음 단계를 안내합니다. 반대로 `reflect`, `improve` 같은 maintenance 보고서에는 기본으로 붙이지 않습니다.

## Agent orchestration

TigerKit은 command-first workflow를 유지합니다. agent는 command를 대체하지 않고 단계 내부 보조로만 사용합니다.

아래 `tk-*` 이름은 짧은 표기입니다. plugin runtime에서 `tk:tk-*`로 표시되면 namespaced 이름을 사용합니다. agent별 기본 model은 비용 폭주를 막기 위해 frontmatter에 고정합니다. cleanup 계열은 `haiku`, 나머지 판단/구현/시각/API 계열은 `sonnet`을 기본으로 쓰며 `opus`는 기본값으로 쓰지 않습니다.

| Agent | 기본 model | 용도 | 주로 쓰는 command |
| --- | --- | --- | --- |
| `tk-sif-muna` | `sonnet` | 지식의 신. 실제 API, 공식 contract, `mock_api_contract`, `TK-API-*` 확인 | `/tk:gap`, `/tk:plan`, `/tk:do`, `/tk:review-fix` |
| `tk-ru` | `sonnet` | 트레이드오프의 신. review, YAGNI, architecture risk, correctness 판단 | `/tk:plan`, `/tk:review`, `/tk:review-fix`, `/tk:improve` |
| `tk-trog` | `sonnet` | 단순무식 힘의 신. scope가 명확한 bounded implementation | `/tk:do`, `/tk:do-all` |
| `tk-nemelex-xobeh` | `sonnet` | 트릭스터. UI/UX, prototype variant, visual polish | `/tk:prototype`, UI task의 `/tk:do` |
| `tk-ashenzari` | `sonnet` | 예지와 감지의 신. screenshot, PDF, diagram 등 visual artifact 관찰 | `/tk:prep`, `/tk:gap`, `/tk:prototype`, `/tk:review` |
| `tk-elyvilon` | `haiku` | 청결과 치유의 신. cleanup, docs hygiene, review-fix 정리 | `/tk:do`, `/tk:do-all`, `/tk:improve`, `/tk:review-fix` |

최종 산출물 작성, task 상태 갱신, 검증, local commit은 command를 실행하는 main agent가 책임집니다.

## 1. 도움말

권장 workflow와 command 선택 기준을 빠르게 확인할 때 실행합니다.

```text
/tk:help
```

`/tk:help`는 core workflow, 보조 기능, 현재 상황별 다음 추천 1개를 짧게 표시합니다. 파일을 수정하지 않습니다.

## 2. 답변 해독

긴 LLM 답변, 애매한 설명, 회의록식 덤프가 결국 무슨 말인지 모르겠을 때 실행합니다.

```text
/tk:mwhat <긴 답변, 설명, 또는 정리 요청>
```

`/tk:mwhat`은 `mwhat` skill의 명시 호출 alias입니다. 자연어 자동 trigger는 `뭣?` 하나로만 제한합니다. `뭐라고?`, `무슨 말이야?` 같은 넓은 confusion 표현으로는 자동 실행하지 않습니다.

기본 출력은 두 블록입니다.

```text
뭣? 쉽게 말하면
추천
```

`뭣? 쉽게 말하면`은 최대 3줄, `추천`은 최대 2줄로 유지합니다. 추천은 `이렇게 말하세요: ...` 또는 `이렇게 하세요: ...` 형식으로 적습니다.

이 명령은 코드를 구현하거나 파일을 수정하지 않습니다. 먼저 말뜻과 문제 상황을 짧게 풀고, 사용자가 말하거나 할 수 있는 추천을 제시합니다.

## 3. 요구사항 기준 정리

아이디어, 앞선 대화, 파일 경로, 기획서 URL, 티켓, 메모를 갭 분석 기준으로 정리할 때 실행합니다.

```text
/tk:prep <아이디어, 자료, 또는 정리 요청>
```

이 명령은 먼저 다음을 확인합니다.

1. 앞선 대화 내용을 바탕으로 바로 정리할지
2. 별도 자료를 추가로 제공할지: 파일 경로, 기획서 URL, 티켓, 메모, 스크린샷 등
3. 추론한 스펙명 또는 작업 ID를 그대로 사용할지

아이디어가 흐릿하면 긴 질문지 대신 문제, 목표, 제외 범위, 검증 방법만 짧게 좁힙니다.

주요 산출물:

```text
.tigerkit/{work_id}/requirements.md
.tigerkit/{work_id}/requirements.meta.json
```

동일한 입력 자료, prep 지시문 버전, 범위, input identity로 다시 실행하면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`를 붙이면 다시 생성합니다.

실행 후 채팅 응답은 생성/재사용 여부, 파일 경로, 3줄 이내 요약만 짧게 표시합니다.

## 4. 갭 분석

준비된 요구사항 기준과 현재 구현, 문서, 테스트, 관찰 가능한 동작 사이의 차이를 분석할 때 실행합니다.

```text
/tk:gap
```

`gap`은 다음 파일을 기준으로 분석합니다.

```text
.tigerkit/{work_id}/requirements.md
```

요구사항 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 않고 `/tk:prep`로 기준 자료를 먼저 정리하라고 안내합니다.

주요 산출물:

```text
.tigerkit/{work_id}/gap.md
.tigerkit/{work_id}/gap.meta.json
```

동일한 git commit, requirements 해시, gap 지시문 버전, 범위로 다시 실행하고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`를 붙이면 다시 분석합니다.

실행 후 채팅 응답은 전체 보고서를 길게 출력하지 않고, 보고서 경로, Verdict, 핵심 gap, next move 1개만 표시합니다.

보고서는 다음을 분리해서 정리합니다.

- Verdict
- Requirement Coverage
- Remaining Gaps
- API Contract Drift
- Unable to Verify
- Notes

`Requirement Coverage`, `Remaining Gaps`, `API Contract Drift`, `Unable to Verify`는 항상 Markdown 표로 작성합니다. 해당 항목이 없더라도 표 섹션과 헤더를 생략하지 않고 `없음` 행을 남깁니다.

각 finding은 요구사항 ID, 상태, 근거, 갭, 다음 행동을 포함합니다. `API Contract Drift`는 항상 표로 포함하고, 확인된 drift가 없더라도 헤더와 `없음` 행을 남깁니다. API 부재나 `TK-API-* blocked`가 남아 있고 사용자가 이번 범위 밖이라고 명시하지 않았다면 채팅 응답 끝에서 실제 API나 공식 contract가 준비됐는지 확인을 요청합니다.

분석 후에는 특정 계획/실행 명령으로 자동 연결하지 않습니다. 보고서 끝의 `Next Move` 하나를 참고해 사용자가 구현, 보류, 추가 확인 같은 다음 행동을 고릅니다.

## 5. 실행계획

`requirements.md` 또는 `gap.md` 기준으로 구현 전에 실행 순서와 검증 방식을 정리할 때 실행합니다.

```text
/tk:plan
```

주요 산출물:

```text
.tigerkit/{work_id}/plan.md
```

계획에는 Revision Notes, Context, Recommended Approach, API Readiness, Task Breakdown, Dependencies, Verification을 포함합니다. `plan.md`는 항상 canonical 최신 계획이며, 재실행 시 `plan.v2.md`를 만들지 않고 기존 계획에서 유지/폐기/새로 배운 것/API readiness 변경만 `Revision Notes`에 남깁니다.

`API Readiness`는 feature slice 단위 표입니다. 값은 `ready`, `mock_api_contract`, `blocked`를 사용합니다. API나 공식 contract를 확인할 수 없고 사용자가 이번 범위 밖이라고 명시하지 않았다면 기본값은 `mock_api_contract`입니다. 이 상태는 assumed contract와 mock API로 개발을 계속한다는 뜻이며 완료나 merge-ready를 뜻하지 않습니다.

`plan`은 승인 전 `tasks.md`를 만들지 않습니다. 사용자가 구현을 요청하지 않았다면 코드를 수정하지 않습니다.

## 6. task 분해

`gap.md` 또는 `plan.md`를 작은 실행 task로 내릴 때 실행합니다.

```text
/tk:breakdown
```

주요 산출물:

```text
.tigerkit/{work_id}/tasks.md
```

각 task는 ID, 상태, 목적, 포함 작업 또는 묶인 gap 요약, 체크리스트, 완료 기준, blocker를 짧게 포함합니다. 포함 작업 요약은 task ID만 보고도 무엇을 해야 하는지 알 수 있게 한 줄로 적습니다. 상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용합니다.

`spec_unclear`나 모호한 요구사항은 task를 `blocked`로 만들지 않고 `Clarification Actions`에 `TK-CLARIFY-*`로 올립니다. `Clarification Actions`는 `ID`, `상태`, `모호점`, `추천 경로`, `영향 task`, `완료 조건`을 포함하고 상태는 `unresolved` 또는 `resolved`입니다. 다음 행동은 `/tk:grill-me`, targeted question, brainstorming, assumption 선택 중 하나로 적습니다. 외부에서만 풀 수 있는 `api_contract_missing`, `permission_required`, `external_dependency_unavailable`, `human_decision_required`는 `Shared Blockers`에 모읍니다. `Shared Blockers`는 `ID`, `유형`, `상태`, `영향 task`, `해소 조건`, `현재 근거`를 포함합니다.

`mock_api_contract` slice는 일반 task를 API 부재 때문에 전부 `blocked`로 만들지 않습니다. `API Follow-up Tasks` 섹션에 공유 API capability별 `TK-API-*` 항목 하나를 만들고, mock boundary에는 `FIXME(TK-API-<n>)` marker를 남깁니다. 저장소 규칙상 `FIXME`가 금지되면 `TODO(TK-API-<n>)`를 씁니다.

## 7. 상태 보기

`.tigerkit/{work_id}` 전체 상태를 볼 때 실행합니다.

```text
/tk:state
```

출력은 work_id, 현재 단계, 산출물 존재 여부, task 요약, clarification action, 외부 blocker, 다음 추천 1개만 짧게 표시합니다. task를 표나 목록으로 보여줄 때는 task ID만 적지 말고 `포함 작업` 같은 칼럼이나 문구로 묶인 gap/작업을 한 줄 요약합니다.

## 8. 다음 것 추천

현재 `.tigerkit/{work_id}/` 상태를 보고 지금 해야 할 다음 command 또는 다음 task 하나만 추천할 때 실행합니다.

```text
/tk:next
```

상태별 추천:

- `requirements.md`가 없으면 `/tk:prep`
- `requirements.md`는 있고 `gap.md`가 없으면 `/tk:gap`
- `gap.md`는 있고 `plan.md`가 없으면 `/tk:plan`
- `plan.md` 또는 `gap.md`는 있고 `tasks.md`가 없으면 `/tk:breakdown`
- unresolved `Clarification Actions`가 있으면 모호함을 `blocked`로 보지 않고 `/tk:grill-me`, targeted question, brainstorming, assumption 선택 중 하나를 추천
- `tasks.md`에 `in_progress` 또는 `todo`가 있으면 다음 task 1개와 `/tk:do`
- 이때 task ID만 던지지 말고 묶인 gap/포함 작업을 한 줄 요약해 함께 보여줍니다.
- 실행 가능 일반 task가 있고 `TK-API-* blocked`가 남아 있으면 일반 task를 추천하고 API/contract 확인 필요를 주의로 표시합니다.
- 실행 가능 일반 task가 없고 `TK-API-* todo`가 있으면 API replacement task와 `/tk:do`를 추천합니다.
- 실행 가능 일반 task가 없고 `TK-API-* blocked`만 있으면 기다림이 아니라 API/contract 확인 요청을 추천합니다.
- 실행 가능 task가 없고 외부 `blocked` 또는 `Shared Blockers`의 `상태=blocked` 항목만 있으면 blocker 해결에 필요한 결정이나 접근 확보
- task를 다 끝냈고 재평가 전이면 `/tk:gap`
- 재평가까지 끝났고 새 gap, unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목이 없으면 `/tk:close`

`/tk:next`는 파일을 수정하지 않습니다.

## 9. task 구현

현재 task 1건을 구현하고 검증할 때 실행합니다. 코드 수정이 포함된 task는 검증 통과 후 local commit으로 남깁니다.

```text
/tk:do
```

동작:

- task ID가 있으면 그 task를 구현합니다.
- task ID가 없으면 `in_progress`를 우선, 없으면 첫 번째 `todo`를 구현합니다.
- task 성격에 따라 TDD 적용 여부를 판단합니다.
- 새 behavior, bug fix, business logic, regression risk가 있으면 TDD를 추천합니다.
- docs, prompt, manifest, config, copy 변경은 TDD를 생략할 수 있습니다.
- 작은 task는 inline, 큰 독립 task는 sub-agent 방식을 스스로 판단합니다.
- sub-agent를 쓰면 task 성격에 따라 `tk-trog`, `tk-sif-muna`, `tk-elyvilon`, `tk-nemelex-xobeh`, `tk-ashenzari`, `tk-ru`를 고릅니다.
- 구현 중 모호함이 드러나면 task를 `blocked`로 만들지 않고 `Clarification Actions`와 다음 clarification 경로를 남깁니다.
- 외부에서만 풀 수 있는 blocker는 `Shared Blockers`에 유형, 상태, 영향 task, 해소 조건, 현재 근거를 모읍니다.
- 코드 수정이 포함됐고 검증이 통과했으면 관련 변경 파일만 stage해 새 commit을 만듭니다.

TDD 적용 시 한 test → 최소 구현 → green → 다음 test 순서로 진행합니다. 모든 test를 먼저 쓰는 horizontal slice는 금지합니다.

선택한 task가 `TK-API-*` follow-up이면 실제 API나 공식 contract 기준으로 assumed contract와 mock 경계를 교체하고, 관련 `FIXME(TK-API-<n>)` 또는 `TODO(TK-API-<n>)` marker를 해결하거나 남은 차단 사유를 갱신합니다.

## 10. 전체 task 구현

실행 가능한 task를 끝날 때까지 하나씩 구현할 때 실행합니다.

```text
/tk:do-all
```

각 task는 `/tk:do`와 같은 규칙으로 처리하며, task별 agent routing을 다시 판단합니다. 코드 수정이 포함된 task는 task별 검증 통과 후 local commit으로 남깁니다. 외부 blocker, 검증 실패, clarification action 필요, 기반 브랜치 변경 위험이 있으면 중단하고 보고합니다. 모호함은 `blocked`로 만들지 않고 `/tk:grill-me`, targeted question, brainstorming, assumption 선택을 다음 행동으로 둡니다. 단 `TK-API-* blocked`만 있으면 일반 task 구현은 계속하고 merge blocker로 보고합니다.

실행 가능한 일반 task를 모두 처리했고 unresolved `Clarification Actions`, 외부 blocked task, `Shared Blockers`의 `상태=blocked` 항목이 없으면 tail gap check를 한 번만 수행합니다. 새 gap이 있으면 `gap.md`를 갱신하고 `/tk:plan`을 추천합니다. 새 gap이 없고 unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목이 없으면 `/tk:close`를 추천합니다. unresolved `Clarification Actions`가 있으면 clarification next action, unresolved `TK-API-*`가 있으면 API/contract 확인을 다음 action으로 둡니다. 새 gap을 발견해도 바로 다시 구현 loop를 돌지 않습니다.

## 11. 1사이클 자율주행

`prep` 이후 `gap -> plan -> breakdown -> do-all -> gap` 1사이클을 자율주행할 때 실행합니다.

```text
/tk:auto
```

조건:
- work_id가 명확해야 합니다.
- `requirements.md`가 있어야 합니다.

API나 공식 contract를 확인할 수 없고 사용자가 범위 밖이라고 명시하지 않았다면 `/tk:auto`는 `mock_api_contract`로 계속 진행합니다. 코드 수정이 포함된 task는 `/tk:do-all` 규칙에 따라 task별 검증 통과 후 local commit으로 남깁니다. 모호함이 발견되면 `Clarification Actions`로 올리고 clarification next action을 보고합니다. 새 gap이 생기면 1사이클에서 멈추고 `/tk:plan`을 추천합니다. 새 gap이 없고 unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목이 모두 없으면 `/tk:close`를 추천합니다. unresolved `Clarification Actions`가 있으면 clarification next action, unresolved `TK-API-*`가 있으면 API/contract 확인, blocked `Shared Blockers`가 있으면 해소 조건을 다음 action으로 둡니다. 자동으로 2사이클째를 시작하지 않습니다.

## 12. 종료 정리

세션 종료 전 남은 gap, task, 검증, cleanup 후보를 정리할 때 실행합니다.

```text
/tk:close
```

기본 출력은 `Close Report`입니다. 필요하면 사용자의 승인 후 `.tigerkit/{work_id}/close.md`를 작성할 수 있습니다.

확인 항목:

- 남은 gap, unresolved `Clarification Actions`, 외부 blocked task 또는 `Shared Blockers`
- unresolved `Clarification Actions`가 있으면 blocked가 아니라 clarification next action으로 표시합니다.
- `Shared Blockers`의 `상태=blocked` 항목이 있으면 영향 task와 해소 조건을 표시합니다.
- unresolved `TK-API-*` follow-up. 남아 있으면 사용자가 mock 포함 merge를 명시적으로 허용하지 않는 한 merge blocker와 incomplete 상태로 표시합니다.
- 완료한 task와 아직 남은 task
- task를 표나 목록으로 보여줄 때는 task ID만 적지 말고 `포함 작업` 같은 칼럼이나 문구로 묶인 gap/작업을 한 줄 요약합니다.
- 실행한 검증과 실패한 검증
- tail gap check 필요 여부와 결과
- archive 또는 cleanup 후보
- 다음에 이어갈 명령 1개

branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.

## 13. 계획 압박 질문

구현 전에 계획, 설계, 결정의 허점을 파고들 때 실행합니다.

```text
/tk:grill-me
```

활성 세션 중에는 응답 한 턴에 질문 하나만 합니다. 질문 전에 현재 working assumption과 추천 기본값을 짧게 밝히고, 답이 모호하면 더 좁혀 묻습니다.

## 14. 초압축 응답 모드

응답을 더 짧게 만들고 싶을 때 실행합니다.

```text
/tk:caveman
```

`/tk:caveman`은 `caveman` skill alias입니다. 자연어로 `caveman mode`, `less tokens`, `be brief`처럼 요청해도 활성화될 수 있습니다.

기술 용어, 코드 블록, 오류 메시지는 유지하고 filler와 장황한 설명을 줄입니다. 보안 경고, 되돌리기 어려운 action 확인, 순서가 중요한 절차에서는 일시적으로 더 명확히 씁니다.

## 15. skill 작성

새 Claude Code skill을 만들거나 기존 skill을 가볍게 고칠 때는 `write-a-skill` skill을 사용합니다.

자연어 예시:

```text
새 skill 하나 만들어줘.
skill-creator 말고 짧은 SKILL.md로 정리해줘.
이 workflow를 skill로 바꿔줘.
```

기본은 `skills/{skill-name}/SKILL.md` 하나입니다. reference나 scripts는 필요할 때만 추가합니다.

## 16. review 요청

구현 직후나 merge 전에 review에 필요한 맥락을 정리하고 코드 리뷰를 요청할 때 실행합니다.

```text
/tk:review
```

출력은 `Review Brief`입니다. review scope, 변경 요약, 기대 동작, verify 방법, reviewer가 봐야 할 risk를 포함합니다. 사용 가능한 외부 review surface가 없고 TigerKit agent가 사용 가능하면 `tk-ru`를 reviewer로 사용할 수 있습니다. 외부 review를 요청하기 전에 코드베이스 내부 맥락 정리가 필요할 때도 `tk-ru`를 사용할 수 있습니다. 둘 다 없으면 `Review Brief`만 남기고 멈춥니다.

## 17. review 반영

받은 리뷰 피드백을 검증하고, 맞는 것만 순서대로 반영할 때 실행합니다.

```text
/tk:review-fix
```

모호한 항목은 먼저 clarification을 요청합니다. reviewer가 틀릴 수 있다고 가정하되, 기술적으로 검증한 뒤 처리합니다. cleanup이나 docs hygiene 성격이면 `tk-elyvilon`을 사용할 수 있습니다. 코드 수정이 포함되면 검증 통과 후 local commit으로 남깁니다.

## 18. FE prototype 범위 정리

프론트엔드 화면 결정을 production 코드로 확정하기 전에 브라우저에서 비교 가능한 throwaway UI prototype으로 검증할 때 실행합니다.

```text
/tk:prototype
```

기본 방식은 기존 page에 붙이고, `?variant=` URL search param으로 3개 variant를 전환하는 것입니다. 관련 기존 page가 없을 때만 `prototype` 이름이 드러나는 throwaway route를 만듭니다. UI/UX 판단이나 variant 설계가 핵심이면 `tk-nemelex-xobeh`, screenshot 해석이 필요하면 `tk-ashenzari`를 사용할 수 있습니다.

variant는 색이나 copy 차이가 아니라 layout, information hierarchy, primary affordance가 구조적으로 달라야 합니다. 화면 하단에는 prototype 전용 floating switcher를 두고, production build에서는 숨깁니다.

완료 후에는 winner와 이유만 남기고 loser variant와 switcher를 삭제합니다. 명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.

## 19. 세션 회고

현재 세션에서 반복된 교정 포인트, 놓친 확인 절차, 다음부터 줄이고 싶은 실수를 짧게 회고할 때 실행합니다.

```text
/tk:reflect
```

`/tk:reflect`는 session learning과 knowledge patch 후보를 정리하는 maintenance command입니다. 작업 종료 상태 정리는 `/tk:close`가 맡습니다.

주요 출력은 `Session Reflection` 형식의 짧은 회고 보고서입니다. 이 명령은 사용자 사전 승인 없이 파일을 수정하지 않습니다. hook, queue, 히스토리 스캔, 자동 memory capture를 수행하지 않고, 현재 세션에서 드러난 내용만 바탕으로 patch proposal 또는 다음 확인 포인트를 정리합니다.

## 20. Knowledge layer 개선 audit

저장소의 CLAUDE.md, command 문서, 운영 메모처럼 knowledge layer에 해당하는 내용을 가볍게 점검하고 개선 후보를 찾고 싶을 때 실행합니다.

```text
/tk:improve
```

주요 출력은 `Improve Report` 형식의 audit finding과 patch proposal입니다. 보고서는 우선순위가 있는 개선 후보를 제안하지만, 범위가 큰 전면 재작성으로 바로 이어지지 않으며 변경을 자동 적용하지도 않습니다. cleanup patch나 docs hygiene 검토에는 `tk-elyvilon`을 사용할 수 있습니다. finding ID(`IMP-001` 같은 식별자)는 `Findings` 표와 `Proposed Patches` 요약/상세 섹션에서 같은 값으로 반복해 승인 대상을 쉽게 고를 수 있게 유지합니다.

이 명령은 저장소 전체를 광범위하게 다시 쓰지 않습니다. 필요한 경우에도 사용자가 승인한 선택적 patch만 반영 대상으로 삼습니다.

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
```

Eval fixture를 수정했다면 JSON 문법도 확인합니다.

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

현재 저장소 안에서 확인되는 eval 자산은 다음 하나입니다.

| 경로 | 역할 | 현재 가능한 검증 |
| --- | --- | --- |
| `evals/evals.json` | TigerKit command/skill 흐름의 기대 동작 fixture (`prompt`, `expected_output`, `expectations` 필드 사용) | `python3 -m json.tool`로 JSON 문법 확인, fixture prompt/expectation 수동 검토 |

`evals/evals.json`은 자동 실행 테스트가 아닙니다. 현재 저장소에는 이 fixture를 LLM에 넣어 pass/fail 판정하는 runner나 harness가 없습니다. 따라서 “eval을 돌렸다”는 말은 JSON 문법 검증만 의미하며, 동작 판정은 수동 검토입니다. 자동 판정이 필요하면 별도 eval runner를 먼저 추가해야 합니다.

## 추천 명령 문장

```text
/tk:mwhat 이 긴 답변 뭐라는 건지 정리해줘.
/tk:prep 앞선 대화 기준으로 요구사항 정리해줘.
/tk:gap 방금 정리한 요구사항 대비 현재 구현 갭 분석해줘.
/tk:plan 이 gap 기준으로 실행계획 세워줘.
/tk:breakdown gap을 실행 task로 쪼개줘.
/tk:next 현재 상태 기준으로 다음 단계 진행해줘.
/tk:do T-003 구현해줘.
/tk:do-all 남은 task 전부 진행해줘.
/tk:close 이번 세션 종료 정리해줘.
/tk:improve 이 저장소 knowledge layer 개선 후보를 audit해줘.
```
