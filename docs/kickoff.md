# Kickoff Notes

이 문서는 restructuring 시점의 kickoff snapshot이다. 최신 운영 계약은 `README.md`, `docs/usage.md`, `commands/*.md`를 우선한다.

## 2026-04-29: TigerKit restructuring

TigerKit은 장문 답변 해독, 요구사항 기준 정리, 현재 상태와의 갭 확인, 실행 task 분해, 세션 종료 정리, 그리고 가벼운 knowledge layer 유지보수를 제공한다. 핵심 흐름은 `prep → gap → plan → breakdown → tasks/next → close`이고, utility command는 core lifecycle 밖에서 보조 역할을 한다.

현재 제품명: TigerKit

현재 플러그인 이름: `tk`

현재 명령 묶음:

```text
Core gap workflow: /tk:prep → /tk:gap → /tk:plan → /tk:breakdown → /tk:tasks 또는 /tk:next → /tk:close
Utility: /tk:mwhat, /tk:grill-me, /tk:caveman, /tk:prototype
Maintenance: /tk:reflect, /tk:improve
```

TigerKit은 command-first 구조를 기본으로 한다. 단, 자연어 트리거가 핵심인 `caveman`과 `write-a-skill`은 skill로도 등록한다.

## 명령별 결정

### `/tk:mwhat`

“뭐라고?”, “뭐라는거야?”, “무슨말이죠?”, “뭣” 싶은 긴 LLM 답변이나 애매한 설명을 짧고 실행 가능하게 풀어준다. 파일을 만들거나 코드를 수정하지 않는다.

Approved default output:

```md
뭣? 쉽게 말하면
...

추천
...
```

Behavior decisions:

- Do not create another long summary.
- Explain what the source answer meant.
- Explain what the source answer was trying to do.
- Explain why the user cannot act on it yet when that is relevant.
- Provide a message the user can send or adapt.
- Do not invent work when the source answer has no real action.

### `/tk:prep`

외부 요구사항 소스와 대화 맥락을 `.tigerkit/{work_id}/requirements.md` 기준 문서로 정리한다.

주요 결정:

- 입력 자료 원문, 메모, 캡처, 참고 코드는 필요할 때 `.tigerkit/{work_id}/inputs/` 아래에 둔다.
- 캐시 메타데이터는 `.tigerkit/{work_id}/requirements.meta.json`에 둔다.
- 요구사항, acceptance signal, scope boundary, conflicts, assumptions, unknowns를 분리한다.
- 구현 계획, task breakdown, 코드 수정 지시는 만들지 않는다.

### `/tk:gap`

`.tigerkit/{work_id}/requirements.md`를 기준으로 현재 구현, 문서, 테스트, 관찰 가능한 동작과의 차이를 확인하고 `.tigerkit/{work_id}/gap.md`를 작성한다.

주요 결정:

- 캐시 메타데이터는 `.tigerkit/{work_id}/gap.meta.json`에 둔다.
- 보고서는 Verdict, Requirement Coverage, Remaining Gaps, Unable to Verify, Notes를 포함한다.
- 확인 불가능한 요구사항이 있으면 `NO_GAPS_FOUND`로 판정하지 않는다.
- 명시적으로 요청받지 않는 한 구현 계획이나 코드 변경을 수행하지 않는다.

### `/tk:plan`

`requirements.md` 또는 `gap.md` 기준으로 구현 묶음, 선행관계, 검증 순서를 정리한다.

주요 결정:

- 승인 가능한 실행계획을 만들되 구현을 시작하지 않는다.
- 승인 전에는 `tasks.md`를 만들지 않는다.
- 계획에는 Context, Recommended Approach, Task Breakdown, Dependencies, Verification을 포함한다.

### `/tk:breakdown`, `/tk:tasks`, `/tk:next`

`gap.md` 또는 `plan.md`를 작은 실행 task로 내리고, `.tigerkit/{work_id}/tasks.md`의 상태를 관리한다.

주요 결정:

- 상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용한다.
- `/tk:next`는 다음 task 하나만 고른다.
- blocked, done, dropped task는 실행 후보에서 제외한다.

### `/tk:close`

세션 종료 전 남은 gap, task, 검증, cleanup 후보, 다음 재진입 포인트를 정리한다.

주요 결정:

- branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않는다.
- `/tk:reflect`는 maintenance alias로 유지하되 종료 루틴은 `/tk:close`를 우선한다.
