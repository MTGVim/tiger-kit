# Kickoff Notes

이 문서는 restructuring 시점의 kickoff snapshot이다. 최신 운영 계약은 `README.md`, `docs/usage.md`, 각 `skills/*/SKILL.md`를 우선한다.

## 2026-04-29: TigerKit restructuring

TigerKit은 장문 답변 해독, 요구사항 기준 정리, 현재 상태와의 갭 확인, 그리고 가벼운 knowledge layer 유지보수를 제공한다. 핵심 흐름은 `prep → gap`이고, `mwhat`은 독립 유틸리티이며, 유지보수 명령은 별도 묶음으로 다룬다.

현재 제품명: TigerKit

현재 플러그인 이름: `tk`

현재 명령 묶음:

```text
Core gap workflow: /tk:prep → /tk:gap
Utility: /tk:mwhat
Maintenance: /tk:reflect, /tk:improve
```

## 명령별 결정

아래 상세 결정은 core 3개 명령(`/tk:mwhat`, `/tk:prep`, `/tk:gap`) 중심으로 기록한다.
maintenance 명령(`/tk:reflect`, `/tk:improve`)의 최신 계약은 각 `SKILL.md`와 README/docs를 우선한다.

### `/tk:mwhat`

“뭐라고?”, “뭐라는거야?”, “무슨말이죠?”, “뭣” 싶은 긴 LLM 답변이나 애매한 설명을 짧고 실행 가능하게 풀어준다. 파일을 만들거나 코드를 수정하지 않는다.

Approved default output:

```md
🤔 뭣? 쉽게 말하면
...

💡 추천
...
```

`하던 것`과 `문제 상황`은 필요하면 `🤔 뭣? 쉽게 말하면` 안에서 함께 풀고, 별도 출력 블록으로 분리하지 않는다.

Tone decisions:

- Use Korean by default.
- Make the voice friendly, warm, and direct.
- Avoid stiff default LLM wording.
- Avoid vague hedging such as `~에 가까워요`.
- Keep the final `이렇게 답하면 됨` block practical enough to paste into work chat.
- Do not turn the skill into heavy roleplay or meme-only output.

Behavior decisions:

- Do not create another long summary.
- Explain what the source answer meant.
- Explain what the source answer was trying to do.
- Explain why the user cannot act on it yet.
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
