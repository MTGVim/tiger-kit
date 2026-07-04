# TigerKit gap→route evidence packets

이 문서는 `/tk:gap`이 남길 수 있는 machine-readable handoff packet과 `/tk:route`가 그것을 재사용하는 규칙을 정의합니다.

## Goal

- `gap`이 이미 확인한 source set, precedence, ambiguity, evidence type을 prose로 다시 풀지 않고 넘깁니다.
- `route`는 같은 repo/branch scope의 `gap packet`이 있으면 그 정보를 먼저 읽고 route 판단에 활용합니다.
- packet이 없으면 기존 read-only route 판단으로 fallback 합니다.

## Schema

```text
schemaVersion: tigerkit.gap-packet/v1
```

필수 top-level field:

- `schemaVersion`
- `invocation_id`
- `gap_id`
- `repo_root`
- `repo_key`
- `scope_key`
- `target`
- `source_refs`
- `precedence`
- `findings`
- `unresolved_questions`
- `report_path`
- `created_at`

## Minimal packet shape

```json
{
  "schemaVersion": "tigerkit.gap-packet/v1",
  "invocation_id": "gap-20260704-220500",
  "gap_id": "GAP-20260704-220500-ABCD",
  "repo_root": "/path/to/repo",
  "repo_key": "tiger-kit--abcd1234",
  "scope_key": "main",
  "target": "commands/route.md",
  "source_refs": [
    {
      "ref_id": "S1",
      "role": "SoT",
      "label": "README.md",
      "access_status": "readable"
    },
    {
      "ref_id": "C1",
      "role": "Current",
      "label": "commands/route.md",
      "access_status": "readable"
    }
  ],
  "precedence": {
    "status": "unresolved",
    "resolved_order": [],
    "conflicts": ["S1", "S2"],
    "note": "owner-confirmed precedence 없음"
  },
  "findings": [
    {
      "finding_id": "F1",
      "gap_type": "ambiguous",
      "title": "stale plan vs live surface conflict",
      "sot_refs": ["S1", "S2"],
      "current_evidence": [
        {
          "evidence_id": "C1",
          "type": "file-read",
          "strength": "direct"
        }
      ],
      "route": "decision"
    }
  ],
  "unresolved_questions": [
    "Which source has precedence?"
  ],
  "report_path": "~/.tigerkit/repos/.../gap/current.md",
  "created_at": "2026-07-04T22:05:00Z"
}
```

## Field intent

### `source_refs`

`source_refs`는 packet이 어떤 ref를 비교했는지 남깁니다.

- `role`: `SoT | Current | Unknown`
- `access_status`: `readable | inaccessible | missing | unknown`
- `label`: human-readable source identifier

### `precedence`

`precedence`는 source priority를 억지로 확정하지 않게 하는 핵심 필드입니다.

- `status`: `resolved | unresolved`
- `resolved_order`: precedence가 확인된 경우만 사용
- `conflicts`: unresolved conflict에 참여한 ref id 목록
- `note`: why unresolved / how it was resolved

### `findings`

각 finding은 최소한 아래를 담아야 합니다.

- `finding_id`
- `gap_type`: `missing | mismatch | overbuilt | ambiguous`
- `title`
- `sot_refs`
- `current_evidence`
- `route`

`current_evidence[]`는 evidence type과 strength를 숨기지 않아야 합니다.

예:
- `type`: `file-read | command-output | rendered-output | diff | generated-artifact | implementation-plan`
- `strength`: `direct | derived | weak`

## Storage

runtime generated state는 project repository 밖 `~/.tigerkit/`에 둡니다.

권장 path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/GAP-YYYYMMDD-HHmmss-RAND.packet.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.packet.json
```

markdown gap report와 packet은 나란히 보관하되, packet은 route handoff용 machine-readable state입니다.

same repo/scope 현재 packet을 읽으려면 helper의 `read-gap-packet` surface를 사용합니다.

```bash
python3 "$TIGERKIT_STATE_SCRIPT" read-gap-packet --repo-root "$PWD"
```

응답은 최소한 아래 의미를 포함합니다.

- `found: true | false`
- `currentPacketPath`
- `packet` (found=true일 때)

## Route consumption rule

- `/tk:route`는 same repo/scope `gap packet`이 있으면 먼저 읽습니다.
- packet이 있어도 source 수정, build/test/network 실행은 하지 않습니다.
- packet이 없거나 stale하면 기존 conversation + repo evidence로 fallback 합니다.
- packet은 route label을 강제하지 않습니다. route는 packet을 근거로 삼되 direct / subagent-driven / goal-driven / decision / need-sot 중에서 다시 판단합니다.

## Non-goals

- packet 자체가 route 결론을 고정하지 않습니다.
- packet만으로 implementation proof를 대신하지 않습니다.
- repo 안 `.claude/tigerkit/`에 runtime generated packet을 쓰지 않습니다.
