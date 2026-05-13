---
description: WatchMe mode를 끝내고 retrospective와 Reflect promotion 후보를 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: active WatchMe mode를 종료하고, 무엇이 배움이었는지 retrospective를 남기며, reusable lesson을 `Promote to Reflect` 후보로 정리합니다.

## 종료 동작

1. active WatchMe state를 해제합니다.
2. indicator 출력을 멈춥니다.
3. retrospective를 `.tigerkit/{work_id}/watchme-retrospective.md` 또는 work_id가 없으면 `.tigerkit/watchme-retrospective.md`에 작성합니다.
4. `Promote to Reflect` 섹션을 포함합니다.
5. 채팅에는 retrospective 전문이 아니라 receipt와 artifact path만 짧게 보고합니다.

## retrospective 규약

단순 요약이 아니라 agent가 다음부터 어떻게 더 잘할지를 뽑아야 합니다.

필수 구조:

```md
# WatchMe 회고

## 사용자가 보여준 판단 흐름
- ...

## agent가 원래 다르게 행동했을 지점
- ...

## 더 나은 판단을 놓친 이유
- ...

## 더 일찍 했어야 할 context scan
- ...

## 다음부터 안전하게 따라도 되는 규칙
- ...

## 다음부터 반드시 물어야 하는 규칙
- ...

## implementation context 개선점
- ...

## Promote to Reflect

### User-level Learning Candidates
- User behavior patterns:
- User decision heuristics:
- User review/correction style:
- User ask-vs-act preferences:
- User evidence expectations:

### Agent Guardrail Candidates
- ...

### Project Convention Candidates
- repo-specific일 때만

### Command / Prompt Improvement Candidates
- tool-specific일 때만
```

## Reflect promotion 원칙

WatchMe lesson은 기본적으로 user-level learning 후보입니다. 아래 우선순위를 씁니다.

1. user-level learning
2. agent guardrail
3. project convention, repo-specific일 때만
4. command/doc improvement, tool-specific일 때만
5. one-off context는 폐기

중요:

- durable knowledge는 사용자 승인 없이 갱신하지 않습니다.
- 이 command는 reflect patch proposal 또는 promotion candidate를 제시할 수는 있지만, silent mutation은 하지 않습니다.
- current TigerKit plugin은 `/reflect` direct command를 보장하지 않습니다. 필요하면 외부 reflect flow나 별도 승인 단계로 넘깁니다.

## 출력

receipt-first로 짧게 보고합니다.

```text
watchme 종료했습니다.
- state: cleared
- retrospective: `.tigerkit/{work_id}/watchme-retrospective.md`
- promote to reflect: proposed only
- durable write: not performed

다음: reflect 후보를 검토하거나 일반 실행으로 돌아가기
```

## 금지

- indicator를 active로 남기기
- retrospective 없이 종료
- user-level lesson을 project file에 그대로 dump
- 승인 없는 reflect write
- `.git` 내부 state 사용