# tigap-skills

`tigap-skills`는 모호한 요청을 정리된 구현 루프로 바꾸기 위한 Claude Code / 에이전트 워크플로우 스킬 모음입니다.

제공하는 스킬은 세 가지입니다.

- `/tigap:gap` — 자료를 수집하고 갭 분석 보고서를 만듭니다.
- `/tigap:gaplan` — 갭 분석 결과를 구현 계획과 작업 목록으로 바꿉니다.
- `/tigap:go` — 작업 목록을 작고 검증 가능한 단위로 실행합니다.
- `/tigap:next` — 현재 TIGAP 단계와 다음 행동을 확인합니다.

이 워크플로우는 일부러 범용적으로 설계되어 있습니다. 이슈 트래커 티켓, 지식베이스 문서, PRD, 디자인 문서, 사용자가 작성한 브리프, 스크린샷, 코드 참조, 간단한 메모를 모두 입력 자료로 사용할 수 있습니다.

## 권장 흐름

```text
/tigap:gap
/tigap:gaplan
/tigap:go
/tigap:next
```

## 설치

### Marketplace로 설치

Claude Code 안에서 이 저장소를 marketplace로 추가한 뒤 `tigap` 플러그인을 설치합니다.

```text
/plugin marketplace add MTGVim/tigap-skills
/plugin install tigap@tigap-skills
/reload-plugins
```

> 이 저장소에는 marketplace 등록에 필요한 `.claude-plugin/marketplace.json`과 플러그인 매니페스트 `.claude-plugin/plugin.json`이 포함되어 있습니다.

### 로컬 플러그인 디렉터리로 사용

이 저장소를 Claude Code 플러그인 디렉터리로 직접 지정할 수 있습니다.

```bash
claude --plugin-dir ./tigap-skills
```

### Standalone 모드로 설치

스킬을 특정 프로젝트의 `.claude/skills` 디렉터리로 복사합니다.

```bash
./scripts/install-standalone.sh /path/to/project
```

PowerShell에서는 다음 명령을 사용합니다.

```powershell
./scripts/install-standalone.ps1 -TargetProject C:\path\to\project
```

Standalone 모드에서는 같은 흐름을 `/gap`, `/gaplan`, `/go`로 호출합니다.

## 산출물 구조

작업 산출물은 기본적으로 현재 프로젝트의 `.gap/{branch_name}/` 아래에 저장합니다. 자세한 파일 구조는 `docs/artifact-layout.md`를 참고하세요.

`main`, `master`, `develop` 같은 기반 브랜치에서 작업을 시작했다면, 실제 변경 전에 source-of-truth에 맞는 작업 브랜치나 work id를 정하는 것을 권장합니다.

스킬 파일은 재사용 가능한 워크플로우 지침입니다. 실행 중 만들어지는 산출물은 프로젝트 로컬 작업 노트로 취급합니다.

## 설계 원칙

- 입력 자료 수집은 특정 도구나 문서 형식에 묶이지 않게 유지합니다.
- 모든 입력은 분석 전에 source packet으로 정규화합니다.
- 작업은 명확한 검증 방법이 있는 작은 단위로 나눕니다.
- `/tigap:gaplan`이 작업 계획을 만들기 전에는 큰 구현을 시작하지 않습니다.
