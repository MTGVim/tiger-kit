---
description: reflect가 제안한 candidate를 실제 artifact로 생성합니다. 1차 범위는 skill only 입니다.
argument-hint: '"<candidate_id>" | --desc "<freeform description>" [--target skill] [--dry-run]'
---

이 문서는 TigerKit `/tk:forge` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:forge`는 `/tk:reflect`가 제안한 durable candidate를 실제 artifact로 materialize합니다. 1차 범위는 `skill only`입니다. `reflect`는 source를 직접 만들지 않고, `forge`가 그 후단 생성 surface를 맡습니다.

```text
forge = reflect candidate or freeform description -> confirm name -> create durable skill source
```

## Core boundary

- 1차 구현 범위는 `skill only`입니다.
- `hook|command|agent`는 reflect target으로는 남길 수 있지만, forge가 실제 source를 생성하지 않습니다.
- 생성 전 이름 확정이 필요합니다.
- `candidate_id`는 same-session + same-ledger에서만 유효합니다.
- repo tracked file, plugin manifest, source code는 자동 수정하지 않습니다.

## Inputs

다음 입력 형태를 지원합니다.

- `tk:forge <candidate_id>`
- `tk:forge --desc "<freeform description>"`
- `--target skill`
- `--dry-run`

`--target`은 1차에서 `skill`만 허용합니다. 다른 target을 명시하면 preview rejection 또는 not-supported 안내를 출력합니다.

## Candidate lookup

`candidate_id` 입력은 아래 규칙을 따릅니다.

1. 직전 same-session `reflect` ledger를 source of truth로 읽습니다.
2. same-ledger 안에서만 `candidate_id`를 찾습니다.
3. cross-invocation durable handle은 1차에서 지원하지 않습니다.
4. ledger가 없거나 candidate를 찾을 수 없으면 source를 생성하지 않고 이유를 출력합니다.

## Name confirmation

forge는 evidence에서 이름을 제안할 수 있습니다.

- 기본 형태: `<domain>:<skill>` 또는 `<skill>`
- 예: `ui-diff`, `ui:pixel-diff`

하지만 실제 생성 전에는 아래가 필요합니다.

1. suggested name
2. user-confirmed name
3. target path preview

auto-write default는 유지하되, 그 default는 **이름이 확정된 뒤**에만 적용됩니다.

## Write target

1차 write target은 아래 경로입니다.

```text
~/.claude/skills/<name>/SKILL.md
```

필요하면 같은 skill directory 아래에 supporting file을 둘 수 있지만, command의 필수 deliverable은 `SKILL.md`입니다.

## Dry-run

`--dry-run`에서는 아래만 수행합니다.

- candidate/description 해석
- suggested name 계산
- target path preview
- 생성될 `SKILL.md` outline 또는 content preview

실제 파일 write는 하지 않습니다.

## Post-create follow-up

생성 후 사용자는 아래 후속 조치를 요청할 수 있습니다.

- remove
- rename
- patch

forge가 생성했다는 사실만으로 tracked repo 변경이나 plugin surface 활성화를 의미하지는 않습니다.

## Output contract

```text
Forge 완료 | Forge 미리보기 | Forge 중단
Input: <candidate_id or --desc>
Target: skill
Name:
- suggested: <slug>
- confirmed: <slug or NONE>
Ledger: <reflect ledger path or NONE>
Created:
- <path or NONE>
다음 행동:
- <rename/remove/follow-up>
```

Rules:

- same-session ledger를 찾지 못하면 `Ledger: NONE`과 중단 사유를 출력합니다.
- `--dry-run`이면 `Created: NONE`입니다.
- 이름이 아직 확정되지 않았으면 실제 write를 하지 않습니다.
- stdout은 compact summary만 유지하고, detailed preview는 별도 ledger/preview text에 둘 수 있습니다.

## Examples

```text
/tk:forge R3
/tk:forge R3 --dry-run
/tk:forge --desc "이 CDP QA/LOCAL 비교 루틴을 skill로 굳혀줘"
```

## Non-goals

- hook source generation
- command source generation
- agent source generation
- plugin manifest wiring
- source code modification
- tracked repo file write
