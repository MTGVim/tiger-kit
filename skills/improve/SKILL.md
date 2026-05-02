---
name: improve
description: CLAUDE.md, AGENTS.md, .claude/rules, commands, skills, README/docs 같은 repo knowledge layer를 읽고 중복, 모순, 낡은 지침, 누락된 경계, skill hygiene 문제를 찾아 작은 patch 후보를 제안합니다. 자동 broad rewrite 없이 수동 audit이 필요할 때 사용합니다.
---

# improve

## 목적

타깃 repo의 existing agent knowledge layer를 audit하고, 중복·모순·비대함·낡은 지침·누락된 경계를 작은 patch 후보로 제안합니다.

이 스킬은 OACP `self-improve`의 knowledge-layer audit 개념에서 영감을 받았지만 TigerKit에서는 더 작게 유지합니다.

- hook 없음
- queue 없음
- history scan 없음
- automatic memory capture 없음
- automatic broad rewrite 없음
- automatic apply 없음
- self-modifying workflow 없음
- mandatory external installation 없음
- project memory system 강제 없음

## 정의

```text
improve
= 타깃 리포의 CLAUDE.md / AGENTS.md / .claude/rules / skills / docs를 읽고,
  중복·모순·비대함·낡은 지침·누락된 경계를 찾아
  작고 안전한 개선 patch를 제안한다.
```

이 스킬은 이미 존재하는 repository knowledge layer를 점검하는 데 집중합니다. 현재 세션에서 새로 드러난 reusable learning을 회고하고 durable target 후보로 승격하는 일은 `reflect`의 책임입니다.

## 입력 범위

존재하는 파일만 확인합니다. 없는 파일을 만들거나 있다고 가정하지 않습니다.

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/rules/*.md`
- `commands/*.md` (TigerKit repo command entrypoint)
- `.claude/commands/**/*.md` (standalone 또는 target repo가 Claude command 디렉터리를 실제로 사용할 때)
- `.claude/settings.json`
- `skills/*/SKILL.md`
- `README.md`
- `docs/**/*.md`
- plugin manifest와 installer docs, if present

## Target별 audit 기준

| Target | Audit For |
|---|---|
| `CLAUDE.md` | duplicate, stale, contradictory, overly broad, or one-off instructions |
| `AGENTS.md` | cross-agent consistency and overlap with `CLAUDE.md` |
| `.claude/rules/*.md` | incorrect scope, repeated rules, overly broad rules |
| `commands/*.md` | TigerKit command drift or unclear command contracts |
| `.claude/commands/**/*.md` | target repo or standalone Claude command drift, only when present |
| `skills/*/SKILL.md` | bloat, multi-responsibility, unclear output contract |
| `README.md` | mismatch with current skill behavior |
| `docs/**/*.md` | stale conventions, duplicated guidance, deprecated guidance mixed with to-be behavior |

## 찾을 문제

### Bloat

- 목적에 비해 파일이 지나치게 김
- 하나의 skill이 unrelated modes를 여러 개 가짐
- 반복되는 예외 때문에 guidance를 따라가기 어려움
- 긴 internal decision tree가 contract를 가림

### Contradiction

- `CLAUDE.md`와 `README.md`가 다르게 말함
- `AGENTS.md`와 `CLAUDE.md`가 충돌함
- skill description과 output contract가 다름
- deprecated rule과 to-be rule이 label 없이 섞임

### Staleness

- 존재하지 않는 command, path, package를 current guidance로 다룸
- 삭제된 migration instruction을 현재 규칙처럼 둠
- temporary로 표시된 항목이 permanent guidance처럼 남음

### Missing Boundary

- skill이 하지 않는 일을 밝히지 않음
- output location이 불명확함
- scope가 불명확함
- user approval boundary가 불명확함

### Skill Hygiene

- skill이 100줄 미만이면 obvious problem이 없을 때 구조 비판을 강제하지 않습니다.
- skill이 100줄을 넘으면 multiple responsibility인지 확인합니다.
- 새로운 mode 추가보다 input/output contract 명확화를 우선합니다.
- execution, memory promotion, architecture review, requirements snapshotting을 한 skill에 섞지 않습니다.

## 진행 절차

### 1. 대상 파일 수집

존재하는 knowledge-layer 파일만 확인합니다. repository 전체를 무차별적으로 훑지 말고 위 입력 범위에 맞는 파일을 우선합니다.

### 2. Finding 작성

각 finding은 atomic하고 actionable해야 합니다.

각 finding에는 다음을 포함합니다.

- ID
- Target
- Type
- Severity
- Finding
- Suggested Fix

권장 Type:

- `bloat`
- `contradiction`
- `staleness`
- `missing-boundary`
- `skill-hygiene`
- `docs-drift`

Severity는 확실성과 영향에 따라 `high`, `medium`, `low` 중 하나를 씁니다. 불확실하면 severity를 낮추고 과장하지 않습니다.

### 3. Patch 후보 제안

작고 안전한 patch를 제안합니다.

- broad rewrite를 기본으로 제안하지 않습니다.
- 새 파일 생성보다 기존 guidance 수정을 우선합니다.
- 하나의 patch는 하나의 finding을 해결합니다.
- style과 naming은 repository 기존 방식을 따릅니다.

### 4. 보고서 작성

기본 출력은 audit report이며 direct edit가 아닙니다.

```md
# Improve Report

## Summary

타깃 리포의 agent knowledge layer에서 개선 후보 N개를 발견했습니다.

## Findings

| ID | Target | Type | Severity | Finding | Suggested Fix |
|---|---|---|---|---|---|
| IMP-001 | `README.md` | docs-drift | medium | ... | ... |

## Proposed Patches

### IMP-001 -> README.md

```diff
- ...
+ ...
```

## Non-Actions

| Item | Reason |
|---|---|
| ... | ... |
```

Finding이 없으면 “현재 확인한 knowledge layer에서 작은 patch로 개선할 뚜렷한 후보가 없습니다”라고 짧게 보고합니다.

### 5. 승인 후 적용

명시적으로 승인된 finding 또는 patch만 적용합니다.

- 후보 ID 또는 target이 분명하면 해당 patch만 적용합니다.
- “좋아”, “ㅇㅇ”처럼 적용 범위가 애매한 승인은 적용 전 다시 확인합니다.
- automatic broad rewrite를 하지 않습니다.
- 여러 finding을 한 번에 적용하라는 뜻이 불분명하면 어떤 후보를 적용할지 다시 묻습니다.
- 새 skill 생성, ADR 생성, CONTEXT.md 생성은 사용자가 명시적으로 요청하지 않는 한 하지 않습니다.

## 하지 않는 일

- hook-based reflection
- queue files
- history scanning
- automatic memory capture
- automatic file edits
- skill auto-generation
- ADR generation
- CONTEXT.md generation
- architecture review
- `grill`, `arch`, `close`, `promote` 추가

## 완료 기준

이 스킬은 다음 조건을 만족하면 완료됩니다.

- 존재하는 knowledge-layer target을 확인함
- bloat, contradiction, staleness, missing boundary, skill hygiene 관점으로 finding을 분류함
- small patch proposal 중심으로 보고함
- 승인 없이 파일을 수정하지 않음
- `reflect`와 responsibility가 섞이지 않음
