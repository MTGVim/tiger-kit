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

# 직전 설명 다시 설명하기

사용자가 `/tk-mwhat` 또는 “뭐라고?”, “뭐라는 거야?”, “무슨 말이죠?”처럼 **명시적으로** 요청할 때만 사용한다. 입력은 대화의 **즉시 앞선 explanation/source 하나**뿐이다. 없거나 무엇을 가리키는지 모호하면 정확히 `Unverifiable`만 출력하고 중단한다.

## 출력

두 블록만 출력한다.

```md
🤔 쉽게 말하면
[뜻과 현재 문제를 최대 3개의 짧은 줄로 재설명]

💡 추천
[추천 또는 그대로 보낼 다음 문장 최대 2개의 짧은 줄]
```

원문보다 짧게 쓰되 의미를 바꾸지 않는다. path, command, URL, literal, status/ID, source attribution은 정확히 보존한다. 추천을 만들 근거가 없으면 `추천: 없음` 으로 둔다.

재설명 뒤에는 **hard stop**한다. 파일을 변경하거나 구현·계획·요약을 만들거나 명령/도구를 실행하지 않는다. 새 작업·변경 요청·일반 summary 요청은 이 skill의 대상이 아니므로 `NotApplicable` 로 중단한다.

## Provenance

Historical prior-art: TigerKit `mwhat` (commit `c6963e8`, `skills/mwhat/SKILL.md`)의 two-block short Korean explanation, exact source/literal preservation, and no implementation contract. Matt Pocock `wait-what` source는 이 checkout/history에서 확인되지 않아 동작을 추정하지 않았다.
