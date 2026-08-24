---
name: tk-mwhat
description: "[user] 직전 설명이 이해되지 않아 사용자가 명시적으로 다시 설명을 요청할 때만, 바로 앞 explanation/source를 짧고 정확하게 재설명한다. 자동 호출하지 않으며 파일 변경·구현·실행을 하지 않는다."
disable-model-invocation: true
argument-hint: "<직전 설명>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: adapted
---

# Re-explain the Previous Explanation

Use only when the user **explicitly** requests it with `/tk-mwhat` or phrases such as `뭐라고?`, `뭐라는 거야?`, or `무슨 말이죠?`. The input is only the **immediately preceding explanation/source** in the conversation. If none exists or the reference is ambiguous, output exactly `Unverifiable` and stop.

## Output

Output only these two blocks.

```md
🤔 쉽게 말하면
[뜻과 현재 문제를 최대 3개의 짧은 줄로 재설명]

💡 추천
[추천 또는 그대로 보낼 다음 문장 최대 2개의 짧은 줄]
```

Write more briefly than the source without changing its meaning. Preserve paths, commands, URLs, literals,
verified UI strings, `Status`/IDs, and original authorship attribution exactly. Keep a verified UI string's language,
case, punctuation, and spacing; do not translate, paraphrase, or normalize it. Do not turn an `enum`, code identifier,
or i18n key into a UI label. If there is no basis for a recommendation, use
`추천: 없음`.

After the re-explanation, **`hard stop`**. Do not modify files, implement anything, create plans or summaries, or run commands or tools. New tasks, change requests, and general summary requests are outside this skill; stop with `NotApplicable`.

## Source

Prior precedent is TigerKit `mwhat` (commit `c6963e8`, `skills/mwhat/SKILL.md`):
two short Korean explanation blocks, exact source/literal preservation, and no implementation contract.
Matt Pocock's original `wait-what` was not available in this checkout or its records, so no behavior was inferred.
