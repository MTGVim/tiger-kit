# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 TIGAP 산출물(`.gap/{branch_name}/normalized/source-packet.md`, `analysis/gap-report.md`, `plan/implementation-plan.md`, `tasks.md`, `execution-log.md`, `review-checklist.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선하되, TIGAP workflow 산출물은 한글 규칙을 유지한다.

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

- `.claude-plugin/plugin.json`: `tigap` 플러그인의 command/skill manifest. 새 command나 skill을 추가하면 여기 등록해야 한다.
- `.claude-plugin/marketplace.json`: marketplace 등록용 manifest.
- `commands/*.md`: `/tigap:gap`, `/tigap:gaplan`, `/tigap:go`, `/tigap:next` slash command entrypoint. command 파일은 짧게 유지하고 자세한 절차는 skill 문서에 둔다.
- `skills/*/SKILL.md`: 재사용 가능한 TIGAP workflow 지침. 실제 동작 방식과 중단 조건은 주로 여기에 정의한다.
- `docs/usage.md`: 사용자 관점의 명령 사용법.
- `docs/artifact-layout.md`: `.gap/{branch_name}/` 산출물 구조와 workflow stage 기준.
- `scripts/install-standalone.*`: `skills/gap`, `skills/gaplan`, `skills/go`를 대상 프로젝트의 `.claude/skills`로 복사한다.

## TIGAP workflow 개요

- `/tigap:gap`: source-of-truth를 수집/정규화하고 gap report를 만든다. source 자료나 추출 지시가 없으면 저장소를 임의 분석하지 말고 멈춰서 자료 제공, 자료 추출, 인터뷰 중 하나를 요청한다.
- `/tigap:gaplan`: gap report를 구현 계획과 작업 목록으로 바꾼다. 구현은 하지 않는다.
- `/tigap:go`: `.gap/{branch_name}/tasks.md`의 Ready 작업 하나만 좁게 실행하고 `tasks.md`와 `execution-log.md`를 갱신한다.
- `/tigap:next`: `.gap/{branch_name}/` artifacts를 읽어 현재 단계와 다음 행동을 알려준다. read-only여야 한다.

## 작업 시 주의사항

- `.gap/`은 이 저장소에서 로컬 workflow note로 취급되어 `.gitignore` 대상이다. 사용자가 명시하지 않는 한 커밋 대상으로 포함하지 않는다.
- command/skill 변경 후에는 `.claude-plugin/plugin.json`의 command/skill 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `commands/next.md`는 read-only command이므로 파일, branch, git 상태를 변경하는 지시를 넣지 않는다.
- TIGAP workflow에서 `main`, `master`, `develop` 같은 기반 브랜치에서 mutable work를 시작하게 될 때는 전용 작업 브랜치나 work id 구성을 권유해야 하며, 사용자 승인 없이 branch 생성이나 checkout을 수행하지 않는다.
