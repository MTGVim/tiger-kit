# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 작업 산출물(`.tigerkit/{work_id}/requirements.md`, `.tigerkit/{work_id}/gap.md`, `.tigerkit/{work_id}/plan.md`, `.tigerkit/{work_id}/tasks.md`, `.tigerkit/{work_id}/close.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선하되, `.tigerkit/` 산출물은 한글 규칙을 유지한다.

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

- `.claude-plugin/plugin.json`: 플러그인의 command/skill manifest. 새 command나 skill을 추가하면 여기 등록해야 한다.
- `.claude-plugin/marketplace.json`: marketplace 등록용 manifest.
- `commands/*.md`: TigerKit slash command entrypoint. command 파일이 직접 절차와 중단 조건을 안내한다.
- `skills/mwhat/SKILL.md`: `뭣?` trigger로만 자동 실행되는 답변 해독 지침.
- `skills/caveman/SKILL.md`: 자연어 트리거와 세션 지속성이 필요한 caveman 응답 모드 지침.
- `skills/write-a-skill/SKILL.md`: 장황한 skill creator 대체용 경량 skill 작성 지침.
- `skills/issue-to-task/SKILL.md`: 진행 중 제기된 문제를 task insertion, task revision, clarification, shared blocker 후보로 정리하는 지침.
- `docs/usage.md`: 사용자 관점의 명령 사용법.
- `docs/artifact-layout.md`: `.tigerkit/{work_id}/` 산출물 구조와 작업 단계 기준.

## 명령 개요

- `/tk:help`: 권장 loop와 command 선택 기준을 짧게 안내한다.
- `/tk:mwhat`: 긴 LLM 답변이나 애매한 설명을 짧고 실행 가능하게 해독한다.
- `/tk:prep`: 외부 요구사항 소스와 대화 맥락을 `requirements.md` 기준 문서로 정리한다.
- `/tk:gap`: `requirements.md` 대비 현재 구현, 문서, 테스트의 남은 차이를 확인하고 `gap.md`를 작성한다.
- `/tk:plan`: `gap.md` 기준으로 실행계획을 정리한다.
- `/tk:breakdown`: `gap.md` 또는 `plan.md`를 작은 실행 task로 분해한다.
- `/tk:state`: `.tigerkit/{work_id}` 전체 상태를 요약한다.
- `/tk:next`: 현재 상태를 기준으로 다음 command 또는 다음 task 하나를 추천한다.
- `/tk:do`: 현재 task 1건을 구현하고 검증한다.
- `/tk:do-all`: 실행 가능한 task를 끝날 때까지 하나씩 구현하고, 완료 후 tail gap check를 한 번 수행한다.
- `/tk:auto`: `gap -> plan -> breakdown -> do-all -> gap` 1사이클을 자율주행한다.
- `/tk:close`: 세션 종료 전 남은 gap, task, 검증, cleanup 후보를 정리한다.
- `/tk:grill-me`: `prep`이나 `plan`에서 허점을 질문 하나씩 파고든다.
- `/tk:caveman`: `caveman` skill alias로, 기술 정확도를 유지하며 응답을 초압축한다.
- `/tk:prototype`: FE 화면 결정을 브라우저에서 비교 가능한 throwaway UI variants로 검증한다.
- `/tk:review`: 구현 직후나 merge 전에 review 맥락을 정리하고 코드 리뷰를 요청한다.
- `/tk:review-fix`: 받은 리뷰 피드백을 검증하고 맞는 것만 순서대로 반영한다.
- `/tk:reflect`: 현재 세션의 재사용 가능한 learning 후보를 회고하고 knowledge patch 후보를 제안한다.
- `/tk:improve`: 저장소 knowledge layer를 audit하고 작은 patch 후보를 제안한다.

## 작업 시 주의사항

- `.tigerkit/`은 이 저장소에서 로컬 작업 노트로 취급되어 `.gitignore` 대상이다. 사용자가 명시하지 않는 한 커밋 대상으로 포함하지 않는다.
- command/skill 변경 후에는 `.claude-plugin/plugin.json`의 command/skill 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작하게 될 때는 전용 작업 브랜치나 작업 ID 구성을 권유해야 하며, 사용자 승인 없이 브랜치 생성이나 전환을 수행하지 않는다.
