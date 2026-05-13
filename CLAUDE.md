# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 작업 산출물(`.tigerkit/{work_id}/requirements.md`, `.tigerkit/{work_id}/leverage.md`, `.tigerkit/{work_id}/tasks.md`, `.tigerkit/{work_id}/tasks.index.json`, `.tigerkit/{work_id}/handoff.md`, `.tigerkit/{work_id}/archive/tasks.done.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선한다.

## 자주 쓰는 명령

- 플러그인 manifest 검증:

  ```bash
  claude plugin validate .claude-plugin/plugin.json
  ```

- 저장소 플러그인 패키지 검증:

  ```bash
  claude plugin validate .
  ```

- 변경 파일 whitespace 검증:

  ```bash
  git diff --check
  ```

- Eval fixture JSON 문법 검증:

  ```bash
  python3 -m json.tool evals/evals.json >/dev/null
  ```

이 저장소에는 package manager 기반 build/test/lint 설정이 없다. 기능 변경 후에는 위 plugin validation, eval fixture JSON 문법 검증, `git diff --check`를 우선 실행한다. `evals/evals.json`은 자동 실행 테스트가 아니라 기대 동작 fixture다. 현재 저장소에는 이 fixture를 LLM에 넣어 pass/fail 판정하는 runner나 harness가 없으므로, “eval 검증”은 JSON 문법 검증과 수동 기대 동작 검토만 의미한다. plugin version을 올릴 때는 로컬 파일만 기준으로 계산하지 말고 먼저 `origin/main`의 현재 version을 확인한 뒤 minor/patch를 결정한다.

## 저장소 구조

이 저장소는 Claude Code용 `tk` 플러그인만 제공한다.

- `.claude-plugin/plugin.json`: 플러그인의 command/skill manifest.
- `.claude-plugin/marketplace.json`: marketplace 등록용 manifest.
- `commands/prep.md`: requirements source를 `.tigerkit` task ledger로 변환한다.
- `commands/next.md`: `tasks.index.json` 기준 다음 task 하나를 추천한다.
- `commands/do.md`: task 하나를 구현하고 lazy API follow-up을 갱신한다.
- `commands/gap.md`: requirements/task/API/blocker/readiness를 report-only로 점검한다.
- `commands/close.md`: handoff와 merge-ready 판단을 정리한다.
- `skills/issue/SKILL.md`: command가 명시적으로 요청할 때 issue/task-ledger 변경 draft를 만드는 지침. 자연어 auto-trigger는 없다.
- `docs/usage.md`: 사용자 관점의 명령 사용법.
- `docs/artifact-layout.md`: `.tigerkit/{work_id}/` task ledger 구조.
- `docs/output-contract.md`: command 응답 receipt 규칙.

## 명령 개요

- `/tk:prep`: 요구사항 source를 `.tigerkit` task ledger로 정리하고 `tasks.md`, `tasks.index.json`을 만든다.
- `/tk:next`: `tasks.index.json`을 읽고 다음 task 또는 action 하나만 추천한다.
- `/tk:do`: task 하나를 구현하고 lazy API follow-up을 생성/재사용한다.
- `/tk:gap`: requirements 대비 누락, task 상태, API follow-up, shared blocker, close/merge readiness를 점검한다.
- `/tk:close`: 완료/잔여 task, unresolved API follow-up, blocker, handoff, merge-ready 여부를 정리한다.

## 핵심 정책

- TigerKit은 Backlog.md에 의존하지 않는다. `.tigerkit/{work_id}/` artifact가 source of truth다.
- gap/plan 중심이 아니라 task ledger와 lazy API follow-up 중심으로 동작한다.
- API 부재는 항상 development blocker가 아니다.
- mock contract로 안전하게 진행 가능하면 task를 계속 진행하고 `TK-API-*` follow-up을 만든다.
- unresolved `TK-API-*`는 task execution blocker가 아니라 close/merge blocker다.
- mock이 false confidence를 만들거나 유효하지 않은 구현을 강제하면 task를 `blocked`로 둔다.
- 강한 API Capability Key나 taxonomy를 만들지 않는다. `TK-API-*` follow-up ID만 사용한다.
- `tasks.index.json`은 compact state index다. 긴 plan, evidence log, 복잡한 dependency graph를 넣지 않는다.
- TigerKit은 초안과 draft를 만든다. 최종 wording, `done` 전환, 디자인/UX/API 승인 여부는 사람이 결정한다.
- 사람 검수가 필요하면 `done` 대신 `review_required` 상태를 사용한다.

## 작업 시 주의사항

- command/skill 변경 후에는 `.claude-plugin/plugin.json`의 command/skill 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작하게 될 때는 전용 작업 브랜치나 작업 ID 구성을 권유해야 하며, 사용자 승인 없이 브랜치 생성이나 전환을 수행하지 않는다.
- commit, push, PR 생성, merge, deploy는 사용자 승인 없이 수행하지 않는다.
