---
description: 구현 route를 direct, subagent-driven, goal-driven 중에서 정리합니다.
argument-hint: '"<task>" [--context <note>] [--target <path|area>] [--print-checklist]'
---

이 문서는 TigerKit `/tk:route` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:route`는 지금 작업을 어떤 방식으로 구현할지 얇게 정리하는 decision / brainstorming surface입니다. direct, subagent-driven, goal-driven 같은 route를 비교하고, 가장 무난한 1안과 바로 시작할 첫 스텝을 제안합니다.

canonical skill:

```text
skills/route/SKILL.md
```

```text
route = explicit task + current constraints -> compare implementation routes -> choose next move
```

## Core boundary

- 이 command는 source tree, `.claude/tigerkit/`, Git branch/index/stash/commit을 변경하지 않습니다.
- package-manager script, build, test, lint, typecheck, network request를 실행하지 않습니다.
- sealed workflow, spec artifact, approval receipt를 만들지 않습니다.
- 사용자가 이미 바로 구현하라고 했으면 route brainstorming을 강요하지 않습니다.
- SoT가 없어서 판단 근거가 약하면 route를 억지로 확정하지 않고 `need-sot` 또는 `decision`으로 남길 수 있습니다.

## When to use

- task는 있는데 지금 direct로 들어갈지 잠깐 헷갈릴 때
- subagent-driven으로 넘기는 편이 나은지 판단하고 싶을 때
- host가 `/goal` 같은 goal surface를 지원할 때 그쪽이 더 맞는지 비교하고 싶을 때
- 구현 전에 필요한 정보, 리스크, ownership을 짧게 정리하고 싶을 때

## Canonical routes

- `direct`: 현재 세션/에이전트가 바로 구현합니다.
- `subagent-driven`: 역할을 나눠 subagent나 외부 coding agent에 위임하는 편이 낫습니다.
- `goal-driven`: host가 지원하는 goal/task orchestration surface로 푸는 편이 낫습니다. 예: `/goal`.
- `decision`: owner 확인이나 제품 판단이 먼저라서 구현 route를 지금 고정하면 안 됩니다.
- `need-sot`: Source of Truth가 부족해서 route 판단보다 SoT 보강이 먼저입니다.

`goal-driven`은 host-neutral한 route 이름입니다. 특정 host가 `/goal`을 지원하면 그 표면을 예시로 들 수 있지만, command contract 자체는 특정 구현에 종속되지 않습니다.

## Output contract

기본 출력은 아래 정보를 포함해야 합니다.

```text
Route: <direct|subagent-driven|goal-driven|decision|need-sot>
Confidence: high | medium | low
Why
  - <reason>

Tradeoffs
  - <route>: <pros / cons>

Needs first
  - <missing info or NONE>

First step
  - <one concrete next step>
[Goal command]
  - </goal <recommended goal> or NONE>
```

`goal-driven`이 선택되고 host가 `/goal` surface를 지원할 때만 `Goal command` 줄을 추가할 수 있습니다. 이 줄은 ready-to-run recommendation이며, 특정 host command 존재 자체를 증명하지는 않습니다.

가능하면 `direct`, `subagent-driven`, `goal-driven` 세 route를 모두 짧게 비교하되, 억지 균형을 맞추지는 않습니다. 분명히 안 맞는 route는 한 줄로 빨리 제외해도 됩니다.

## Decision policy

1. task의 범위가 작고 file-local이며 명확하면 `direct`를 우선 검토합니다.
2. 병렬 탐색, 독립 검증, reviewer/implementer 분리가 유리하면 `subagent-driven`을 우선 검토합니다.
3. 한 번의 patch보다 goal decomposition, status tracking, multi-step orchestration이 더 중요하면 `goal-driven`을 우선 검토합니다.
4. Source of Truth가 없거나 owner decision이 없어서 route보다 전제 정리가 중요하면 `need-sot` 또는 `decision`을 선택합니다.
5. reject를 피하려고 command 밖 우회 문구를 시도하라고 유도하지 않습니다. 안 맞는 surface면 안 맞는다고 말하고 다른 route를 제안합니다.

## Examples

```text
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:route "이거 direct로 할지 subagent-driven으로 할지 정리해줘"
/tk:route "멀티파일 리팩터인데 /goal로 푸는 게 나은지 봐줘"
```

## Non-goals

- source 수정
- spec 생성
- runtime execute
- 승인 우회 조언
- command 밖에서만 통과할 수도 있다는 식의 편법 유도
