---
name: learn
description: source나 reflect candidate에서 reusable skill을 직접 만듭니다.
---

# Learn

path, URL, notes, 현재 대화, 또는 reflect candidate를 읽고 reusable skill source를 직접 만드는 skill입니다. 분류 라우터가 아니라 source-to-skill surface이며, write boundary는 skill only입니다. repo-local guidance나 user-global guidance는 이 skill의 대상이 아닙니다.

## Goal

- source를 읽어 reusable procedure를 skill source로 굳힙니다.
- reflect가 고른 skill candidate를 실제 skill source로 마무리할 수 있게 합니다.
- preview/apply/name confirmation을 분리해 무리한 write를 막습니다.

## Source modes

- `direct`: path / directory / URL / current conversation / notes
- `reflect-candidate`: same-session + same-ledger `candidate_id`

## Process

1. source와 requirement를 먼저 읽습니다.
2. direct source인지 reflect candidate인지 구분합니다.
3. skill only boundary 안에서 draft를 만듭니다.
4. 이름을 제안하고, 확정 전에는 write하지 않습니다.
5. explicit apply일 때만 user skill surface에 생성합니다.

## Boundaries

- `skill only`
- repo-local / user-global / hook / command / agent direct write 금지
- 이름 확정 전 write 금지
- reflect candidate는 ledger를 source of truth로 읽음
- source code 수정 금지
