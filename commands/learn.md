---
description: 경로, 문서, 대화, reflect candidate에서 reusable skill을 직접 만듭니다.
argument-hint: '"<source or request>" [--name <slug>] [--apply=false|true] [--from-reflect <candidate_id>] [--dry-run]'
---

이 문서는 TigerKit `/tk:learn` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:learn`은 path, directory, URL, 현재 대화, pasted notes, 또는 `/tk:reflect`가 남긴 `candidate_id`를 source로 받아 reusable skill을 직접 만드는 source-to-skill surface입니다. write boundary는 `skill only`이며, repo-local guidance, user-global guidance, hook, command, agent source를 라우팅하지 않습니다.

canonical skill:

```text
skills/learn/SKILL.md
```

```text
learn = explicit source or reflect candidate -> gather evidence -> draft skill -> confirm name -> explicit apply to user skill surface
```

## Core boundary

- `/tk:learn`은 `skill only` surface입니다.
- `repo-local`, `repo-shared`, `user-global`, `hook`, `command`, `agent` direct write를 하지 않습니다.
- source code, plugin manifest, command source를 수정하지 않습니다.
- 이름 확정 전 skill source write 금지입니다.
- `--apply=false` 또는 `--dry-run`은 preview-only 입니다.
- `--from-reflect <candidate_id>`를 쓰면 same-session + same-ledger candidate만 읽습니다.
- reflect candidate를 읽을 때는 chat prose가 아니라 reflect ledger를 source of truth로 삼습니다.
- helper surface가 있으면 `read-reflect-candidate --candidate-id <id>`로 current ledger candidate를 읽을 수 있습니다. helper가 없더라도 source of truth는 계속 reflect ledger입니다.

## When to use

- path나 directory에서 reusable skill을 만들고 싶을 때
- URL 문서나 pasted notes를 skill로 굳히고 싶을 때
- "what we just did" 같은 현재 대화 기반 routine을 skill로 만들고 싶을 때
- `/tk:reflect`가 "이건 skill 후보"라고 분류한 뒤 실제 skill source를 만들고 싶을 때
- repo-local guidance가 아니라 user skill surface가 목적일 때

## Source modes

- `direct`: path, directory, URL, 현재 대화, notes 같은 source를 직접 읽습니다.
- `reflect-candidate`: `/tk:reflect` ledger의 `candidate_id`를 source로 읽고, 필요하면 추가 source를 gather합니다.

reflect candidate helper 예시:

```bash
python3 "$TIGERKIT_STATE_SCRIPT" read-reflect-candidate --repo-root "$PWD" --candidate-id R1
```

## Default target

```text
~/.claude/skills/<name>/SKILL.md
```

host가 다른 user skill surface를 지원하면 equivalent host-native user skill target을 쓸 수 있지만, 이 command의 write boundary는 계속 `skill only`입니다.

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Learn 완료 | Learn 미리보기 | Learn 중단
Input:
- <source or candidate_id>
Source mode:
- direct | reflect-candidate
Apply:
- preview | explicit
Suggested name:
- <slug>
[Confirmed name:
- <slug>]
Target:
- user skill surface only
[Created path:
- <path>]
[Write result:
- preview only | name confirmation needed]
Next step:
- <review skill | confirm name | apply explicitly | patch source>
```

## Apply semantics

- option 생략: preview-only 기본
- `--apply=false`: preview-only
- `--apply=true`: explicit apply
- `--dry-run`: preview-only
- `--name <slug>`: suggested/confirmed 이름 입력
- 이름이 확정되지 않았거나 preview-only면 `Confirmed name`/`Created path` section을 생략하고 `Write result`에 짧게 이유만 남깁니다.

## Non-goals

- repo-local guidance 반영
- user-global guidance 반영
- hook/command/agent 생성
- source code 수정
- publish/merge/release
