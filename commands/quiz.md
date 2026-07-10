---
description: 머지 전 이해도 게이트를 엽니다.
argument-hint: '"[focus]" [--path <area>] [--print-report]'
flow: [route, next, handoff]
---

이 문서는 TigerKit `/tk:quiz` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:quiz`는 merge 전 인간 이해도 게이트입니다. 현재 diff와 decision ledger를 바탕으로 3~5개의 객관식 질문을 만들고, 오답이면 관련 섹션을 다시 보게 한 뒤 다른 선지로 재출제합니다.

related wrapper skill:

```text
skills/quiz/SKILL.md
```

```text
quiz = current diff + ledger -> comprehension gate before merge
```

## Core boundary

- 공통 command boundary는 `.tigerkit/docs/usage.md`의 `Shared command boundaries`를 따릅니다.
- source of truth는 merge-base 대비 current diff와 same worktree `ledger/current.md` 입니다.
- clean diff이면 실행을 거부하고 receipt만 남깁니다.
- publish, remote write, merge 자체를 실행하지 않습니다.
- 이 command의 목적은 이해도 확인이지 테스트 대체가 아닙니다.

## Default paths

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/ledger/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/quiz/current.md
```

helper 예시:

```bash
python3 scripts/tigerkit_state.py draft-paths --repo-root "$PWD" --kind ledger
python3 scripts/tigerkit_state.py draft-paths --repo-root "$PWD" --kind quiz
```

## Question policy

우선순위:
1. 비지시 판단의 이유
2. "X가 바뀌면 뭐가 깨지나"
3. 안 한 것과 그 이유

규칙:
- 질문 수는 3~5개
- `AskUserQuestion` 스타일 객관식으로 낼 수 있어야 함
- 오답이면 관련 리포트 섹션을 안내하고, 같은 주제를 다른 선지로 재출제할 수 있음
- receipt에는 pass/fail을 남김

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Quiz 준비 완료 | Quiz 진행중 | Quiz 완료 | Quiz 중단
🧭 Diff state:
- dirty | clean-diff-rejected
[📁 Ledger path:
- <path>]
[📁 Report path:
- <path>]
📝 Focus:
- <what the quiz is probing>
[🧪 Questions:
- <3~5 question topics>]
[✅ Result:
- pass | fail]
▶️ Next step:
- <answer questions | revisit ledger/report | continue to merge review>
```

## Verification

- clean diff fixture에서는 `clean-diff-rejected` receipt가 나와야 합니다.
- report artifact는 `quiz/current.md`에 current-first로 저장되어야 합니다.
- decision ledger가 있으면 그 판단을 최우선 질문 소재로 사용해야 합니다.
