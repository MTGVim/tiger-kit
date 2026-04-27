# tigap-skills

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

`tigap-skills`는 모호한 요청을 정리된 구현 루프로 바꾸기 위한 Claude Code / 에이전트 워크플로우 스킬 모음입니다.

제공하는 명령/스킬 흐름은 다섯 단계입니다.

- `/tigap:plan` — 원천 자료가 없을 때 인터뷰와 계획 모드로 아이디어를 구체화합니다.
- `/tigap:gap` — 자료를 수집하고 갭 분석 보고서를 만듭니다.
- `/tigap:gaplan` — 갭 분석 결과를 구현 계획 초안으로 바꾸고, 검토 후 작업 목록을 만듭니다.
- `/tigap:go` — 작업 목록을 작고 검증 가능한 단위로 실행합니다.
- `/tigap:next` — 현재 TIGAP 단계와 다음 행동을 확인합니다.

이 워크플로우는 일부러 범용적으로 설계되어 있습니다. 이슈 트래커 티켓, 지식베이스 문서, PRD, 디자인 문서, 사용자가 작성한 브리프, 스크린샷, 코드 참조, 간단한 메모를 모두 입력 자료로 사용할 수 있습니다.

## 권장 흐름

```text
/tigap:plan   # 원천 자료가 없을 때만 필요
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

Standalone 모드에서는 같은 흐름을 `/plan`, `/gap`, `/gaplan`, `/go`, `/next`로 호출합니다.

## 산출물 구조

작업 산출물은 기본적으로 현재 프로젝트의 `.gap/{branch_name}/` 아래에 저장합니다. 완료된 산출물은 `.gap/{branch_name}/archive/` 아래에 보관할 수 있습니다. 자세한 파일 구조는 `docs/artifact-layout.md`를 참고하세요.

`main`, `master`, `develop` 같은 기반 브랜치에서 작업을 시작했다면, 실제 변경 전에 원천 자료에 맞는 작업 브랜치나 작업 ID를 정하는 것을 권장합니다.

스킬 파일은 재사용 가능한 워크플로우 지침입니다. 실행 중 만들어지는 산출물은 프로젝트 로컬 작업 노트로 취급합니다. commit, push, PR 생성은 제안할 수 있지만 사용자 승인 없이 실행하지 않습니다.

## 설계 원칙

- 입력 자료 수집은 특정 도구나 문서 형식에 묶이지 않게 유지합니다.
- 모든 입력은 분석 전에 source packet(원천 자료 묶음)으로 정규화합니다.
- 작업은 명확한 검증 방법이 있는 작은 단위로 나눕니다.
- `/tigap:gaplan`이 작업 계획을 만들기 전에는 큰 구현을 시작하지 않습니다.

## Contributors

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MTGVim"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="Taekwon Yoo"/><br /><sub><b>Taekwon Yoo</b></sub></a><br /><a href="https://github.com/MTGVim/tigap-skills/commits?author=MTGVim" title="Code">💻</a> <a href="https://github.com/MTGVim/tigap-skills/commits?author=MTGVim" title="Documentation">📖</a> <a href="#ideas-MTGVim" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome.
