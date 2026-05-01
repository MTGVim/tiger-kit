# TigerKit

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

TigerKit(`tk`)은 요구사항 소스를 정제하고, 긴 답변을 해독하며, 요구사항 대비 현재 상태의 갭을 확인하기 위한 Claude Code 스킬 모음입니다.

제공하는 명령/스킬 흐름은 세 단계입니다.

- `/tk:mwhat` — “뭐라고?”, “뭐라는거야?”, “무슨말이죠?”, “뭣” 싶은 긴 답변이나 애매한 설명을 짧고 실행 가능하게 풀어줍니다.
- `/tk:prep` — 외부 요구사항 소스와 대화 맥락을 `requirements.md` 기준 문서로 정리합니다.
- `/tk:gap` — `requirements.md` 대비 현재 구현, 문서, 테스트의 남은 차이를 확인합니다.

이 흐름은 이슈 트래커 티켓, 지식베이스 문서, PRD, 디자인 문서, 사용자가 작성한 브리프, 스크린샷, 코드 참조, 간단한 메모를 모두 입력 자료로 사용할 수 있게 설계되어 있습니다.

## 권장 흐름

```text
/tk:mwhat  # 장문/애매한 답변 해독
/tk:prep   # 요구사항 기준 정리
/tk:gap   # 기준 대비 갭 분석
```

흐름으로 보면 `mwhat → prep → gap`입니다. 먼저 말뜻과 막히는 지점을 풀고, 그다음 요구사항 기준으로 고정한 뒤, 마지막으로 현재 상태와의 차이를 봅니다.

`mwhat`은 긴 답변의 핵심과 막히는 지점을 짧게 풀어줍니다. `prep`은 앞선 대화 내용과 외부 요구사항 소스를 `requirements.md`로 정리합니다. `gap`은 준비된 요구사항 기준을 바탕으로 현재 구현, 문서, 테스트의 남은 차이를 분석합니다.

## 설치

### Marketplace로 설치

Claude Code 안에서 이 저장소를 marketplace로 추가한 뒤 `tk` 플러그인을 설치합니다.

```text
/plugin marketplace add MTGVim/tiger-kit
/plugin install tk@tiger-kit
/reload-plugins
```

> 이 저장소에는 marketplace 등록에 필요한 `.claude-plugin/marketplace.json`과 플러그인 매니페스트 `.claude-plugin/plugin.json`이 포함되어 있습니다.

### 로컬 플러그인 디렉터리로 사용

이 저장소를 Claude Code 플러그인 디렉터리로 직접 지정할 수 있습니다.

```bash
claude --plugin-dir ./tiger-kit
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

Standalone 모드에서는 같은 흐름을 `/mwhat`, `/prep`, `/gap`으로 호출합니다.

## 산출물 구조

작업 산출물은 기본적으로 현재 프로젝트의 `.tigerkit/{work_id}/` 아래에 저장합니다. 입력 자료는 `.tigerkit/{work_id}/inputs/`에 둘 수 있고, 주요 산출물은 `requirements.md`, `requirements.meta.json`, `gap.md`, `gap.meta.json`입니다. 자세한 파일 구조는 `docs/artifact-layout.md`를 참고하세요.

`main`, `master`, `develop` 같은 기반 브랜치에서 작업을 시작했다면, 실제 변경 전에 작업 브랜치나 작업 ID를 정하는 것을 권장합니다.

스킬 파일은 재사용 가능한 작업 흐름 지침입니다. 실행 중 만들어지는 산출물은 프로젝트 로컬 작업 노트로 취급합니다. commit, push, PR 생성은 제안할 수 있지만 사용자 승인 없이 실행하지 않습니다.

## 검증

이 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. TigerKit을 수정한 뒤에는 다음 검증을 우선 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool skills/prep/evals/evals.json >/dev/null
python3 -m json.tool skills/gap/evals/evals.json >/dev/null
```

`evals/evals.json`, `skills/prep/evals/evals.json`, `skills/gap/evals/evals.json`은 Claude가 따라야 할 동작을 설명하는 fixture입니다. 현재 저장소에는 이 fixture들을 자동으로 실행하는 별도 harness가 없으므로, JSON 문법 검증과 fixture 내용 수동 확인까지가 저장소 안에서 확인 가능한 범위입니다.

Standalone 설치 경로는 임시 프로젝트에 설치한 뒤 `.claude/skills/prep`, `.claude/skills/gap`, `.claude/skills/mwhat` 디렉터리와 각 `SKILL.md`가 복사됐는지 확인하는 방식으로 smoke 검증합니다. 자세한 절차는 `docs/usage.md`를 참고하세요.

## 설계 원칙

- 입력 자료 수집은 특정 도구나 문서 형식에 묶이지 않게 유지합니다.
- 모든 입력은 분석 전에 요구사항 기준 스냅샷으로 정리합니다.
- 갭 분석은 요구사항 기준과 현재 상태의 차이를 찾는 데 집중합니다.
- 분석 이후의 구현, 보류, 추가 확인은 사용자가 결과를 보고 선택합니다.

## Contributors

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MTGVim"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="Taekwon Yoo"/><br /><sub><b>Taekwon Yoo</b></sub></a><br /><a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Code">💻</a> <a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Documentation">📖</a> <a href="#ideas-MTGVim" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome.
