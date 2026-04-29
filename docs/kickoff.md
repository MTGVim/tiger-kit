# Kickoff Notes

## 2026-04-29: `what` command and skill

`what` started from the user’s frustration with long LLM answers that sound detailed but do not make the next action clear. The desired interaction is: when the user thinks “뭐라는거야?”, Claude should stop elaborating and translate the answer into a short, usable explanation.

Approved name: `what`.

Approved integration: add it to the existing `tigap-skills` plugin instead of keeping a separate repository. The product flow becomes:

```text
what → prep → gap
해독 → 기준화 → 차이분석
```

Approved default output:

```md
🐯 제가 요약해드리죠
...

🎯 하려던 것
...

😵 막히는 지점
...

💡 이렇게 답하면 됨
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
