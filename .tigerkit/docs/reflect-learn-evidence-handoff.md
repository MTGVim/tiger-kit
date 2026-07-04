# TigerKit reflect→learn evidence handoff

이 문서는 `/tk:reflect`가 남긴 candidate/ledger evidence를 `/tk:learn`가 어떻게 안전하게 이어받는지 정의합니다.

## Goal

- `reflect`가 이미 분류한 reusable candidate를 `learn`가 chat prose로 다시 재구성하지 않게 합니다.
- `learn`는 same-session + same-ledger `candidate_id`만 읽고, reflect ledger를 source of truth로 사용합니다.
- write boundary는 계속 `skill only`로 유지합니다.

## Source contract

```text
schemaVersion: tigerkit.reflect-learn-source/v1
```

필수 top-level field:

- `schemaVersion`
- `source_mode`
- `ledger_path`
- `candidate_id`
- `same_session_required`
- `same_ledger_required`
- `source_of_truth`
- `candidate`
- `created_at`

기본값:

- `source_mode`: `reflect-candidate`
- `source_of_truth`: `reflect-ledger`
- `same_session_required`: `true`
- `same_ledger_required`: `true`

## Minimal shape

```json
{
  "schemaVersion": "tigerkit.reflect-learn-source/v1",
  "source_mode": "reflect-candidate",
  "ledger_path": "~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml",
  "candidate_id": "R1",
  "same_session_required": true,
  "same_ledger_required": true,
  "source_of_truth": "reflect-ledger",
  "candidate": {
    "candidate_id": "R1",
    "target": "skill",
    "action": "suggest_only",
    "reason": "repeatable CDP verification routine",
    "evidence": "Observed across this session's successful validation loop"
  },
  "created_at": "2026-07-04T22:40:00Z"
}
```

## Why ledger wins

reflect candidate는 chat prose보다 ledger가 더 신뢰할 수 있습니다.

- chat prose는 생략, 요약, 말투 변화가 생길 수 있습니다.
- ledger는 `candidate_id`, target, action, evidence를 machine-readable하게 남깁니다.
- 그래서 `learn`는 reflect candidate를 읽을 때 ledger를 source of truth로 삼아야 합니다.

## Helper surface

same repo/scope 현재 reflect ledger에서 candidate를 읽으려면 helper의 `read-reflect-candidate` surface를 사용합니다.

```bash
python3 "$TIGERKIT_STATE_SCRIPT" read-reflect-candidate --repo-root "$PWD" --candidate-id R1
```

응답은 최소한 아래 의미를 포함합니다.

- `found: true | false`
- `ledgerPath`
- `candidateId`
- `same_session_required`
- `same_ledger_required`
- `source_of_truth`
- `candidate` (found=true일 때)

## Learn consumption rule

- `/tk:learn --from-reflect <candidate_id>`는 same-session + same-ledger candidate만 읽습니다.
- helper surface가 있으면 `read-reflect-candidate`로 current ledger candidate를 읽고, 없으면 packet/helper 없이도 reflect ledger를 source of truth로 해석하는 contract를 유지합니다.
- candidate를 읽었다고 해서 곧바로 write하면 안 됩니다.
- 이름 확정 전 write 금지, explicit apply 전 write 금지 규칙은 그대로 유지됩니다.

## Non-goals

- reflect candidate를 repo-local / user-global / hook / command / agent write로 바로 확장하지 않습니다.
- helper surface가 same-session enforcement 자체를 완전히 대신하진 않습니다.
- reflect candidate를 source code proof나 implementation completion proof로 바꾸지 않습니다.
