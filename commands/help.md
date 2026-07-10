---
description: entrypoint navigation을 정리합니다.
argument-hint: '"[question or situation]" [--print-map]'
flow: [gap, route, grill, to-prd, to-issues, handoff, browser-verify, next]
---

이 문서는 TigerKit `/tk:help` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:help`는 TigerKit entrypoint를 찾아주는 navigation surface입니다. 전략을 깊게 결정하는 `/tk:route`와 달리, 지금 어떤 command를 먼저 열어야 하는지와 다음 연결 후보를 빠르게 보여줍니다.

related wrapper skill:

```text
skills/help/SKILL.md
```

```text
help = generated command map + current question -> pick the right entrypoint
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- mapping source of truth는 수동 목록이 아니라 `docs/help-map.json`입니다.
- `docs/help-map.json`은 `scripts/generate-help-map.py`가 `commands/*.md` frontmatter와 summary를 읽어 생성합니다.
- `/tk:help`는 navigation만 담당합니다. route 비교, 구현 승인, multi-step orchestration 실행은 `/tk:route`나 `/tk:next`가 맡습니다.
- superpowers 연결점 설명은 `docs/workflow-matrix.md` 한 곳만 참조합니다.

## Modes

- static map: command list와 언제 쓰는지 간단히 보여줍니다.
- situational question: "버그 고치는 중인데 뭐부터?" 같은 질문을 entrypoint + next candidates로 돌려줍니다.
- `--print-map`: `docs/help-map.json` 기준의 compact map만 출력합니다.

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Help 안내 | Help 맵 출력 | Help 중단
🧭 Mode:
- static-map | situational-question | print-map
📝 Entry point:
- </tk:* command>
📝 Why:
- <why this surface fits>
[🧭 Next candidates:
- </tk:* command>
- </tk:* command>]
[📁 Map source:
- docs/help-map.json]
▶️ Next step:
- <run the recommended command | ask /tk:route for strategy>
```

## Verification

- `docs/help-map.json`은 `python3 scripts/generate-help-map.py && git diff --exit-code docs/help-map.json`으로 drift 없이 재생성되어야 합니다.
- 새 command가 추가되면 수동 목록이 아니라 frontmatter source에서 map에 반영되어야 합니다.
