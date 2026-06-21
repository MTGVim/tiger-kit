---
description: 명시적 task를 worktree-scoped LoopSpec recommendation으로 컴파일합니다.
argument-hint: '"<task>" [--explain] [--type bugfix|refactor|flaky-test] [--motif <motif>] [--name <name>] [--no-write] | validate <spec-id-or-path>'
---

이 문서는 TigerKit `/tk:loop-spec` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:loop-spec`은 사용자가 명시적으로 입력한 개발 task와 현재 worktree의 read-only capability를 분석해, 실행하지 않는 loop recommendation인 `LoopSpec`을 생성하거나 기존 spec을 검증합니다.

```text
loop-spec = explicit task + read-only worktree scan -> recommendation + LoopSpec
```

## Core boundary

- `/tk:loop-spec`은 `/tk:gap`의 확장이 아닙니다.
- `/tk:gap`은 `/tk:loop-spec`을 자동 호출하거나 자동 제안하지 않습니다.
- 이 command는 source tree, `.claude/tigerkit/`, Git branch/index/stash/commit을 변경하지 않습니다.
- package-manager script, build, test, lint, typecheck, network request를 실행하지 않습니다.
- 실행기, runner, approval, autopilot, orchestration은 이 command의 범위가 아닙니다.

## MVP surface

```bash
/tk:loop-spec "<task>"
/tk:loop-spec validate <spec-id-or-path>
```

Generate options:

```bash
/tk:loop-spec "<task>" --explain
/tk:loop-spec "<task>" --type bugfix
/tk:loop-spec "<task>" --type refactor
/tk:loop-spec "<task>" --type flaky-test
/tk:loop-spec "<task>" --motif reproduce-diagnose-patch-verify
/tk:loop-spec "<task>" --name fix-payment-modal-scroll
/tk:loop-spec "<task>" --no-write
```

MVP 범위 밖: `list`, `show`, `export`, `--from`, `--issue`, public JSON output, standalone CLI alias, `--probe`, LLM-assisted task analysis.

## Execution instruction

When this command is invoked, run the helper from the repository root:

```bash
python3 scripts/tigerkit_state.py loop-spec $ARGUMENTS
```

If the helper is unavailable, report the blocker instead of inventing a LoopSpec.

## Output contract

기본 출력은 아래 정보를 포함해야 합니다.

```text
Loop strategy: <motif or not-recommended>
Applicability: recommended | conditional | not-recommended
Readiness: complete | incomplete | manual
Fit score: <0..100>/100
Confidence: high | medium | low
Worktree: <branch or workspace>

Why
  - <reason and provenance>

Blockers
  - <blocker or NONE>

Guards
  - <guard>

Saved
  <~/.tigerkit/.../loop-specs/<spec-id>/spec.yaml or NONE>

Write receipt
  changed: <path or NONE>
  source tree changed: no
```

## Storage

기본 artifact는 project repository 밖 active generated state에 저장합니다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml
```

`--no-write`는 artifact를 쓰지 않고 recommendation만 출력합니다.

## Safety invariants

- Raw diff content와 secret content는 spec 또는 scanner artifact에 저장하지 않습니다.
- Fingerprint에는 normalized metadata와 safe content hash만 기록합니다.
- runnable, approval, agent/run lifecycle field는 schema에 포함하지 않습니다.
- Command-level `execution` probe metadata는 discovery와 실제 command success를 구분하기 위해서만 사용합니다.
