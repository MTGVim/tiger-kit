# Kickoff Notes

## 2026-04-29: TigerKit restructuring

TigerKit은 사용자가 장문 답변을 이해하고, 요구사항 기준을 고정하고, 현재 상태와의 차이를 확인하는 세 단계 흐름으로 정리한다.

현재 제품명: TigerKit

현재 플러그인 이름: `tk`

현재 명령 흐름:

```text
/tk:mwhat → /tk:prep → /tk:gap
해독 → 요구사항 기준 정리 → 요구사항 대비 갭 분석
```

## 명령별 결정

### `/tk:mwhat`

“뭐라고?”, “뭐라는거야?”, “무슨말이죠?”, “뭣” 싶은 긴 LLM 답변이나 애매한 설명을 짧고 실행 가능하게 풀어준다. 파일을 만들거나 코드를 수정하지 않는다.

Approved default output:

```md
🤔 뭣? 쉽게 말하면
...

🎯 하던 것
...

😵 문제 상황
...

💡 추천
...
```

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
