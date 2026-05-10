---
name: mwhat
description: 긴 답변이나 애매한 설명을 사용자가 `뭣?`이라고 반응했을 때만 짧고 실행 가능하게 풀어줍니다. Use only when the user explicitly says `뭣?`, or when invoked via `/tk:mwhat`; do not trigger on broader phrases like "뭐라고?", "무슨 말이야?", or generic confusion.
---

# mwhat

긴 LLM 답변, 애매한 설명, 회의록식 덤프를 다시 길게 요약하지 않고, 사용자가 바로 판단하거나 답할 수 있는 짧은 한국어 해설로 바꿉니다.

## Trigger boundary

자연어 trigger는 `뭣?` 하나로 제한합니다.

Trigger:
- `뭣?`

Do not auto-trigger on:
- `뭐라고?`
- `뭐라는거야?`
- `무슨 말이야?`
- `이게 무슨 뜻이야?`
- 일반적인 confusion 표현

위 표현은 사용자가 명시적으로 `/tk:mwhat`을 호출하지 않았다면 일반 대화로 처리합니다.

## Output

두 블록만 사용합니다.

```md
뭣? 쉽게 말하면
...

추천
이렇게 말하세요: ...
```

## Rules

1. 원문보다 훨씬 짧게 씁니다.
2. 원문에 없는 일을 만들지 않습니다.
3. 확실한 내용과 추정한 내용을 섞지 않습니다.
4. `뭣? 쉽게 말하면`은 최대 3줄입니다.
5. `추천`은 최대 2줄입니다.
6. 실질 액션이 없으면 추가 질문이나 확인 문장을 제안합니다.

명시적으로 요청받지 않는 한 코드를 구현하거나 파일을 수정하지 않습니다.
