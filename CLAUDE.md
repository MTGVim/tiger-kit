# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 작업 산출물(`.gap/{work_id}/normalized/source-packet.md`, `.gap/{work_id}/analysis/gap-report.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선하되, `.gap/` 산출물은 한글 규칙을 유지한다.

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

- Standalone 설치 스크립트 실행:

  ```bash
  ./scripts/install-standalone.sh /path/to/project
  ```

- PowerShell standalone 설치:

  ```powershell
  ./scripts/install-standalone.ps1 -TargetProject C:\path\to\project
  ```

이 저장소에는 package manager 기반 build/test/lint 설정이 없다. 기능 변경 후에는 위 plugin validation과 `git diff --check`를 우선 실행한다.

## 저장소 구조

이 저장소는 Claude Code용 `tigap` 플러그인과 standalone skill 설치 스크립트를 제공한다.

- `.claude-plugin/plugin.json`: 플러그인의 command/skill manifest. 새 command나 skill을 추가하면 여기 등록해야 한다.
- `.claude-plugin/marketplace.json`: marketplace 등록용 manifest.
- `commands/*.md`: `/tigap:prep`, `/tigap:gap` slash command entrypoint. command 파일은 짧게 유지하고 자세한 절차는 skill 문서에 둔다.
- `skills/*/SKILL.md`: 재사용 가능한 작업 흐름 지침. 실제 동작 방식과 중단 조건은 주로 여기에 정의한다.
- `docs/usage.md`: 사용자 관점의 명령 사용법.
- `docs/artifact-layout.md`: `.gap/{work_id}/` 산출물 구조와 작업 단계 기준.
- `scripts/install-standalone.*`: `skills/prep`, `skills/gap`을 대상 프로젝트의 `.claude/skills`로 복사한다.

## 명령 개요

- `/tigap:prep`: 아이디어, 앞선 대화, 파일 경로, 기획서 URL, 티켓, 메모를 이번 작업의 기준 자료로 정리한다. 앞선 대화로 바로 정리할지, 별도 자료를 받을지, 스펙명/작업 ID를 어떻게 잡을지 먼저 확인한다.
- `/tigap:gap`: `.gap/{work_id}/normalized/source-packet.md`를 기준으로 현재 구현, 문서, 동작과의 갭을 분석하고 `.gap/{work_id}/analysis/gap-report.md`를 작성한다. 기준 자료가 없으면 `/tigap:prep`을 먼저 안내한다.

## 작업 시 주의사항

- `.gap/`은 이 저장소에서 로컬 작업 노트로 취급되어 `.gitignore` 대상이다. 사용자가 명시하지 않는 한 커밋 대상으로 포함하지 않는다.
- command/skill 변경 후에는 `.claude-plugin/plugin.json`의 command/skill 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작하게 될 때는 전용 작업 브랜치나 작업 ID 구성을 권유해야 하며, 사용자 승인 없이 브랜치 생성이나 전환을 수행하지 않는다.
