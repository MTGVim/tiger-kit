---
description: 다음 command 1개를 고릅니다.
argument-hint: '"[task or resume request]" [--print-reasoning]'
flow: [gap, route, to-prd, to-issues, quiz, handoff]
---

이 문서는 TigerKit `/tk:next` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:next`는 현재 작업 설명이나 current artifact 상태를 바탕으로 **다음 command 정확히 1개만** 지목하는 conductor surface입니다. 자동 연쇄 실행 없이, 추천 command와 멈춰야 할 gate를 분명히 남깁니다.

related wrapper skill:

```text
skills/next/SKILL.md
```

```text
next = current task or current artifacts -> choose exactly one next TigerKit command
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- `docs/help-map.json`과 frontmatter `flow`를 읽어 command 후보를 고릅니다.
- task text가 있으면 entrypoint 분류를 먼저 하고, 없으면 `usage-summary` helper로 현재 worktree artifact 상태를 읽습니다.
- SoT 부재, 최근 user-authored commit 부재, 신규 경계 초월 같은 객관 신호가 있으면 `gap` blindspot 경로를 우선 검토할 수 있습니다.
- 어느 경우에도 command 2개 이상을 연쇄 호출하지 않습니다.
- superpowers 구간은 추천이나 delegation context 제안까지만 하고, conductor가 구현 workflow를 직접 실행하지 않습니다.

## Heuristic signals

- SoT가 없다 → `gap` blindspot 우선 검토
- 현재 repo/대상경로에 최근 user-authored commit이 없다 → discovery 성격 강화
- draft `prd/current.md`만 있고 `issues/current.md`가 없다 → `to-issues`
- route가 이미 정리됐고 ledger/quiz gate가 남았다 → `quiz`
- 작업 종료 직전 요약/재개성이 더 중요하다 → `handoff`

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Next 추천 완료 | Next 중단
🧭 Next command:
- </tk:* command>
📝 Why:
- <why this one is next>
[🧪 Signals:
- <heuristic signals or current artifact clues>]
[📁 Usage summary:
- <helper-derived current artifact state>]
⚠️ Stop gate:
- call exactly one command, then stop at that receipt or approval gate
▶️ Next step:
- <run the recommended command>
```

## Verification

- helper source는 `python3 scripts/tigerkit_state.py usage-summary --repo-root "$PWD"` 입니다.
- fixture 성격으로는 최소한 다음을 구분해야 합니다.
  - SoT 없음 + unfamiliar area → `gap`
  - explicit PRD만 있음 → `to-issues`
  - route/ledger chain 마무리 → `quiz`
