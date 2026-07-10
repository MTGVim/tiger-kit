---
description: current-first handoff를 다시 읽습니다.
argument-hint: '["<focus or question>"] [--path-only]'
flow: [next, route]
---

이 문서는 TigerKit `/tk:handon` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:handon`은 `/tk:handoff`가 남긴 current-first handoff artifact를 현재 repo/worktree 기준으로 다시 여는 read-only surface입니다. 저장된 handoff 파일을 source of truth로 읽고, 필요하면 focus에 맞춰 짧게 요약하거나 경로만 확인해줍니다.

related wrapper skill:

```text
skills/handon/SKILL.md
```

```text
handon = current repo/worktree handoff current.md -> read saved artifact -> resume work
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- read-only 입니다.
- 기본은 현재 repo/worktree의 `handoffs/current.md`만 읽습니다.
- source of truth는 저장된 handoff artifact이며, chat memory나 추측으로 빈칸을 메우지 않습니다.
- handoff가 없으면 missing path를 숨기지 않고 그대로 보여줍니다.
- 기존 handoff를 regenerate, overwrite, append 하지 않습니다.

## Default source path

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py draft-paths --kind handoffs` helper가 계산합니다.

helper 예시:

enabled `tk@tiger-kit` install이 오래되어 `draft-paths`가 `invalid choice`로 실패하면 먼저 marketplace/plugin을 업데이트하거나, matching checkout/install root를 `CLAUDE_PLUGIN_ROOT`로 지정합니다.

```bash
claude plugin marketplace update tiger-kit
claude plugin install tk@tiger-kit --scope user
```

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" draft-paths --repo-root "$PWD" --kind handoffs
```

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Handon 읽기 완료 | Handon 경로 확인 | Handon 없음
📁 Handoff path:
- <path>
[📝 Focus:
- <focus or question>]
📝 Source:
- current repo/worktree handoff artifact
[📝 Summary:
- <compact summary from saved handoff>]
[⚠️ Missing:
- no current handoff draft found]
▶️ Next step:
- <resume from remaining tasks | create a new handoff with /tk:handoff>
```

## Examples

```text
/tk:handon
/tk:handon "남은 작업만 짧게"
/tk:handon --path-only
```
