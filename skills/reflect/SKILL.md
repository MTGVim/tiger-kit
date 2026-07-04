---
name: reflect
description: 세션 결과와 피드백에서 재사용 가능한 learning을 뽑아 canonical target으로 분류합니다.
---

# Reflect

세션 결과와 피드백에서 재사용 가능한 learning을 꺼내고, 안전한 durable promotion surface로 분류하는 skill입니다.

## Goal

- repo-local guidance와 user-global guidance는 지원 host에서 기본 apply(opt-out) 대상으로 봅니다.
- reusable procedure는 skill/hook/command/agent 후보로 분류합니다.
- skill은 explicit apply일 때만 실제 source로 materialize하며, authoring은 `/tk:learn` pipeline으로 위임합니다.
- writable host-native surface를 확인할 수 없으면 suggest-only로 남깁니다.
- branch-local one-off와 저신뢰 정보는 버립니다.

## Canonical targets

- `repo-local`
- `repo-shared`
- `user-global`
- `skill`
- `hook`
- `command`
- `agent`
- `discard`

## Process

1. 세션 결과, 실제 변경, 성공/실패, 사용자 피드백을 읽습니다.
2. reusable candidate를 canonical target으로 분류합니다.
3. `repo-local`과 `user-global`은 지원 host에서 기본 apply 후보로 봅니다.
4. `skill`은 explicit apply일 때만 source 생성 후보로 보고, 같은 session/ledger candidate를 `/tk:learn` pipeline으로 넘깁니다.
5. exact apply plan은 ledger에 남기고 stdout은 compact하게 유지합니다.
6. `hook/command/agent`는 제안만 하고 source는 직접 만들지 않습니다.
7. branch-specific one-off, 민감 정보, 중복, 저신뢰 항목은 `discard`합니다.

## Repo-local apply

- 유일한 repo-local direct write target: `<git-root>/CLAUDE.local.md`
- 기본은 apply enabled
- `--apply=false`면 preview-only
- tracked file / not ignored / symlink / repo 밖 path는 reject

## User-global apply

- 지원 host에서는 user-global도 기본 apply 후보입니다.
- Claude Code 계열이면 `~/.claude/CLAUDE.md` 또는 `~/.claude/rules/<rule-name>/CLAUDE.md`를 target으로 잡을 수 있습니다.
- host가 `CLAUDE.md` 계열 파일을 직접 다루지 않으면 host-native user-global guidance surface를 사용합니다.
- writable host-native surface를 확인할 수 없으면 `suggest_only`로 남깁니다.

## Boundaries

- Claude Code auto memory write/mirror/backup 금지
- source code / hook settings / command source / agent source / plugin manifest 수정 금지
- `PROFILE.md`, `automation`, `hookify`를 target 이름으로 쓰지 않음

## Skill materialize

- `reflect`는 candidate를 제안합니다.
- `skill` target은 explicit apply일 때만 실제 skill source를 생성합니다.
- skill source 생성은 `/tk:learn` pipeline이 ledger를 source of truth로 읽어 마무리합니다.
- `candidate_id`는 same-session ledger 안에서만 유효합니다.
