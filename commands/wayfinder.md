---
description: shared map을 정리합니다.
argument-hint: '"[goal or map update]" [--print-only]'
flow: [route, next, handoff]
---

이 문서는 TigerKit `/tk:wayfinder` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:wayfinder`는 긴 작업을 위한 shared map surface입니다. 현재 작업 목표, 진행 슬라이스, 막는 edge, 재개 힌트를 worktree-scoped file-only artifact로 남겨 다음 세션이나 다른 agent가 빠르게 상태를 파악할 수 있게 합니다.

related wrapper skill:

```text
skills/wayfinder/SKILL.md
```

```text
wayfinder = long-running work map -> persist current context, edges, and resume hints
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- tracker/Jira 연동 없이 file-only state로만 남깁니다.
- 기본은 current-first artifact 갱신입니다.
- publish나 remote write를 하지 않습니다.
- implementation proof를 대신하지 않고, 진행 지도와 resume context만 정리합니다.

## Default path

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/wayfinder/current.md
```

helper 예시:

```bash
python3 scripts/tigerkit_state.py draft-paths --repo-root "$PWD" --kind wayfinder
```

## Map fields

최소한 아래를 포함합니다.

- current goal
- current slice / status
- blocked-by / blocking edges
- recent decisions
- next concrete step
- reopen hints after compact/session switch

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Wayfinder 완료 | Wayfinder 미리보기 | Wayfinder 중단
🎯 Goal:
- <current long-running goal>
🧭 Output mode:
- draft file | inline preview
[📁 Output path:
- <path>]
📝 Includes:
- current goal / current slice / blocked-by / blocking edges / recent decisions / next concrete step / reopen hints
▶️ Next step:
- <resume from map | update map after the next milestone>
```

## Verification

- `draft-paths --kind wayfinder`가 유효 path를 반환해야 합니다.
- current-first artifact는 `wayfinder/current.md`에 저장되어야 합니다.
