---
description: steer 세션을 끝내고 correction/decision/reflect candidate를 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: active steer state를 끝내고, 무엇을 교정했고 무엇이 reflect candidate인지 compact하게 정리합니다. heavy retrospective를 강제하지 않습니다.

## 종료 동작

1. active steer state를 해제합니다.
2. indicator 출력을 멈춥니다.
3. `decisions.md`에 마지막 correction/heuristic를 flush합니다.
4. reflect candidate가 있으면 pending count를 유지합니다.
5. 채팅에는 receipt만 짧게 보고합니다.

## 정리 원칙

분리할 것:
- session-only decisions
- work-level conventions
- durable reflect candidates
- 폐기할 one-off noise

하지 않는 것:
- 긴 retrospective 본문 dump
- 승인 없는 durable write
- 자동 reflect promotion

## 출력

```text
steer 종료했습니다.
- state: cleared
- decisions: `.tigerkit/search/decisions.md`
- reflect pending: 2

다음 추천: /tk:task status
```

## 금지

- indicator를 active로 남기기
- correction flush 없이 종료
- reflect candidate를 자동 승격하기