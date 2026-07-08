---
description: guidance 파일을 평가하고, 승인된 user-global 변경만 직접 반영하며 나머지는 suggestion-only로 남깁니다.
argument-hint: '"[scope]" [--scope <user|repo|all>] [--apply=true]'
---

이 문서는 TigerKit `/tk:grooming` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:grooming`은 guidance 파일을 바로 정리했다고 주장하지 않고, 먼저 report-only로 평가한 뒤 승인된 범위의 user-global guidance만 직접 apply하고 나머지는 suggestion-only로 남기는 정비 surface입니다.

canonical skill:

```text
skills/grooming/SKILL.md
```

## Core boundary

- default report-only
- no-publish 기본
- 승인 전 write 금지
- direct apply 대상은 `user-global` guidance만 허용
- repo shared / repo local guidance는 suggestion-only
- user-global direct apply와 repo suggestion-only가 한 변경 안에 섞이면 전체를 preview-only로 남김
- 원본 파일을 직접 읽고, 세션 주입 사본을 source of truth로 쓰지 않음

## Scope contract

지원 scope:

```text
user | repo | all
```

기본값은 `user`입니다.

해석 규칙:
- `user`: `~/.claude/CLAUDE.md`, `~/.claude/rules/<rule-name>/CLAUDE.md`
- `repo`: 현재 repo의 `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/**`
- `all`: user + 현재 repo에서 실행 중이면 repo까지 포함

## Problem classes

최소한 아래 클래스를 탐지합니다.

1. 위치 오염
2. 자기모순
3. 죽은 참조
4. 실효성 없는 룰
5. 사실 부정확
6. 방어적 반복
7. 추가 제안 후보

## Apply semantics

- option 생략: report-only
- `--apply=true`: 승인된 범위의 direct apply를 시도
- direct apply는 user-global exact target이 분명할 때만 가능
- repo 파일 변경은 항상 suggestion-only
- user-global direct apply와 repo suggestion-only가 한 묶음에 섞이면 `preview-only mixed-scope`로 보고하고 쓰지 않음

## Protected exclusions

기본 보호 대상:
- 역사 기록물: branch snapshot, `*.original.md`, transcript/history
- 서드파티 관리 블록: marker block (`CODEGRAPH_START`, `vowline:start` 등)
- TigerKit 관리 섹션: 최소 수정만 허용
- import(`@...`) / plugin 주입 블록: 명시 요청 없으면 범위 밖

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Grooming 리포트 | Grooming 적용 완료 | Grooming 중단
Scope:
- user | repo | all
Mode:
- report-only | preview-only mixed-scope | user-global direct-apply | suggestion-only
Findings:
- <confirmed drift summary>
[Direct apply target:
- <user-global path>]
[Applied changes:
- <what changed>]
[Suggested changes:
- <repo/user suggestions kept as suggestion-only>]
[Protected exclusions:
- <reported-only exclusions>]
Verification:
- <readback / re-grep / preview reason>
Next step:
- <approve apply | review suggestions | rerun with narrower scope>
```

## Non-goals

- repo source code 수정
- repo guidance direct apply
- 신규 guidance를 임의 추가하는 것
- reflect/learn 역할 대체
- 승인 없는 광범위 rewrite
