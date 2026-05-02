---
name: reflect
description: 현재 세션에서 드러난 재사용 가능한 convention, 용어, agent 교정사항을 추출하고 CLAUDE.md, AGENTS.md, rules, skill docs, README/docs 등 적절한 target에 대한 patch 후보를 제안합니다. hook, queue, history scan, 자동 적용 없이 수동 회고가 필요할 때 사용합니다.
---

# reflect

## 목적

현재 세션 대화에서 드러난 재사용 가능한 convention, 용어, agent 교정사항을 추출하고 durable target에 반영할 patch 후보를 제안합니다.

이 스킬은 `claude-reflect`의 session reflection 개념에서 영감을 받았지만 TigerKit에서는 더 작게 유지합니다.

- hook 없음
- queue 없음
- history scan 없음
- automatic memory capture 없음
- automatic broad rewrite 없음
- automatic apply 없음
- 기본 범위는 현재 세션뿐

## 정의

```text
reflect
= 현재 세션에서 드러난 재사용 가능한 convention, 용어, agent 교정사항을 추출하고,
  CLAUDE.md, AGENTS.md, .claude/rules, skill docs, README/docs 중 적절한 target에 대한 patch 후보를 제안하는 수동 회고 skill.
```

이 스킬은 현재 세션의 reusable learning을 durable guidance 후보로 정리하는 데 집중합니다. 기존 repository knowledge layer 전체를 넓게 감사하거나 구조 개선을 찾는 일은 `improve`의 책임입니다.

## 입력 범위

기본 입력은 현재 세션 conversation입니다.

다음 파일은 후보 확인이나 target 분류에 필요할 때만 읽습니다. 모든 파일이 존재해야 하는 것은 아닙니다.

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/rules/*.md`
- `commands/*.md` (TigerKit repo command entrypoint)
- `.claude/commands/**/*.md` (standalone 또는 target repo가 Claude command 디렉터리를 실제로 사용할 때)
- `skills/*/SKILL.md`
- `README.md`
- `docs/**/*.md`
- `.tigerkit/{work_id}/requirements.md`
- `.tigerkit/{work_id}/gap.md`

사용자가 명시적으로 파일이나 저장소 검토를 요청하지 않았다면 현재 세션 밖의 과거 대화나 history를 스캔하지 않습니다.

## Target 분류

| Target | Use For |
|---|---|
| `CLAUDE.md` | repo-wide Claude Code instructions, workflow rules, verification commands, prohibited behaviors |
| `AGENTS.md` | instructions useful across multiple coding agents |
| `.claude/rules/*.md` | path-scoped or topic-scoped rules |
| `commands/*.md` | TigerKit plugin command behavior corrections |
| `.claude/commands/**/*.md` | standalone or target repo command behavior corrections, only when that repo uses Claude command directories |
| `skills/*/SKILL.md` | skill boundary, output contract, or behavior corrections |
| `README.md` | user-facing usage, public workflow, project overview |
| `docs/**/*.md` | human-readable domain terminology, conventions, migration context |
| `.tigerkit/{work_id}/reflection.md` | session-local reflection output when promotion target is unclear |

## 후보로 남길 것

다음 조건 중 하나 이상을 만족하고 operational effect가 있을 때만 후보로 남깁니다.

- 사용자가 agent의 이해나 접근을 교정함
- 같은 오류가 future session에서 재발할 수 있음
- repo-local convention이 명확해짐
- canonical term 또는 domain meaning이 명확해짐
- deprecated/current/to-be behavior가 명확해짐
- command, validation flow, forbidden path, workflow rule이 명확해짐
- skill boundary 또는 responsibility가 교정됨
- 기존 docs나 skills에 해당 guidance가 없을 가능성이 높음

## 버릴 것

다음은 durable knowledge 후보로 승격하지 않습니다.

- one-off ticket requirements
- temporary task instructions
- repo와 무관한 개인 취향
- speculative or unverified assumptions
- actionable content가 없는 vague feedback
- target에 이미 같은 guidance가 있는 내용
- secrets or sensitive information
- operational effect가 없는 broad philosophy

## 진행 절차

### 1. 범위 확인

기본적으로 현재 세션만 검토합니다. 사용자가 특정 파일, repository target, work_id를 제공하면 해당 범위만 추가로 확인합니다.

사용자가 “적용해”, “REF-001 적용”, “이 patch 반영”처럼 명시적으로 승인한 경우에만 선택된 patch를 적용할 수 있습니다. 승인 대상이 모호하면 적용 전에 어떤 후보를 적용할지 묻습니다.

### 2. 후보 추출

각 후보는 atomic하게 작성합니다. 한 후보에는 하나의 learning만 담습니다.

각 후보에는 다음을 분류합니다.

- Learning
- Type
- Suggested Target
- Confidence
- Reason

권장 Type:

- `workflow-rule`
- `skill-boundary`
- `terminology`
- `validation-rule`
- `forbidden-behavior`
- `docs-drift`
- `reflection-note`

### 3. 기존 guidance 확인

patch를 제안하기 전에 suggested target에 equivalent guidance가 이미 있는지 확인합니다.

이미 있으면 새 patch를 만들지 말고 “existing guidance found”로 non-action에 남깁니다.

### 4. 보고서 작성

기본 출력은 report이며 direct edit가 아닙니다.

```md
# Session Reflection

## Summary

이번 세션에서 durable knowledge 후보 N개를 발견했습니다.

## Candidates

| ID | Learning | Type | Suggested Target | Confidence | Reason |
|---|---|---|---|---|---|
| REF-001 | ... | skill-boundary | `skills/example/SKILL.md` | high | ... |

## Proposed Patches

### REF-001 -> skills/example/SKILL.md

```diff
+ ...
```

## Non-Actions

| Item | Reason |
|---|---|
| ... | ... |

## Actions

- Apply: 승인한 후보 ID만 적용합니다.
- Edit: 후보 문구를 조정한 뒤 적용합니다.
- Skip: durable target에 반영하지 않습니다.
```

후보가 없으면 “현재 세션에서 durable knowledge로 승격할 후보가 없습니다”라고 짧게 보고합니다.

### 5. 승인 후 적용

명시적으로 승인된 후보만 적용합니다.

- 후보 ID 또는 target이 분명하면 해당 patch만 적용합니다.
- “좋아”, “ㅇㅇ”처럼 적용 범위가 애매한 승인은 적용 전 다시 확인합니다.
- 새 파일 생성보다 기존 guidance 업데이트를 우선합니다.
- target이 불분명하면 `.tigerkit/{work_id}/reflection.md` 후보로 남기고 durable target에는 쓰지 않습니다.
- broad rewrite나 다수 target 동시 수정은 사용자가 분명히 승인하지 않았다면 하지 않습니다.
- secrets나 sensitive information은 어떤 경우에도 승격하지 않습니다.

## 완료 기준

이 스킬은 다음 조건을 만족하면 완료됩니다.

- 현재 세션 기준으로 reusable learning 후보를 검토함
- 후보마다 target, confidence, reason을 분류함
- equivalent guidance가 있는지 확인함
- 기본 결과를 patch proposal 중심 보고서로 제시함
- 승인 없이 durable target을 수정하지 않음
- `improve`의 repository-wide audit 책임과 섞이지 않음
