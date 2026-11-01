<a id="dependency-planner-cli"></a>
# 의존성 planner CLI

Python 3.9+가 필요합니다. 출처나 설치된 `SKILL.md`를 읽으려면 추가로 PyYAML이 필요합니다(6.0.3으로 검증했습니다). 파서 지원 누락은 확정적인 중단 조건이며, 성공한 패키지 확인이 아닙니다. 빈 목적지에 포함된 카탈로그로 계획할 때는 표준 라이브러리만 필요합니다. 승인된 설치 전에는 설치 후 확인을 수행할 Python 환경에서 파서 이용 가능 여부를 검증합니다. 환경·패키지 준비에는 해당하는 별도 승인이 필요합니다. 이 도우미는 파서를 설치하거나 regex 기반 YAML 검증으로 대체하지 않습니다.
설치된 패키지의 `scripts/skill_dependencies.py`를 실행합니다. 저장소 유지보수자는 저장소 루트의 공개 shim `scripts/skill_dependencies.py`를 사용할 수 있습니다. 예시는 그 저장소 shim을 사용합니다. 모든 예시 값을 검증된 사용자 선택으로 바꿉니다.

<a id="read-only-commands"></a>
## 읽기 전용 명령

```sh
python3 scripts/skill_dependencies.py validate --root /absolute/trusted/checkout
python3 scripts/skill_dependencies.py validate --root /absolute/trusted/checkout --catalog skills/tk-setup-skills/references/install-catalog.json
python3 scripts/skill_dependencies.py plan --skill tk-review tk-prep --source owner/repository --target /absolute/project --agent codex --scope project
python3 scripts/skill_dependencies.py plan --root /absolute/trusted/checkout --skill tk-review --source /absolute/trusted/checkout --target /absolute/project --agent claude-code --scope project
python3 scripts/skill_dependencies.py check --installed-root /absolute/project/.agents/skills --skill tk-review
```

`plan`의 기본값은 구현 옆에 포함된 카탈로그입니다. `--root`를 사용하면 대신 현재 저장소 선언을 검증합니다. `--catalog <path>`는 다른 신뢰할 수 있는 메타데이터 카탈로그를 명시적으로 선택합니다. `--skill`은 glob이나 경로가 아니라 하나 이상의 정확한 ID를 받습니다. 출력은 결정론적 JSON입니다.
`validate`는 출처 선언이 유효하지 않으면 `errors`와 함께 종료 코드 1을 반환합니다. 선택적인 카탈로그 비교는 오래된 메타데이터를 거부합니다. `check`는 선택한 설치 의존성 폐쇄만 순회하고 의존성이 누락되면 중단합니다. CLI 사용 오류는 2를 반환합니다. 검증·계획 실패는 traceback 없이 1을 반환합니다. 어떤 명령도 설치, 출처 가져오기나 설정 복구로 대체하지 않습니다. 인수 없이 호출하면 변경 없이 사용법을 출력합니다.

저장소 API `validate_dependencies(root: Path) -> list[str]`는 생성된 카탈로그 없이 출처 선언을 검증합니다. 누락·잘못된 선언은 예외를 발생시키는 대신 실행 가능한 오류로 반환합니다. 각 패키지는 정확히 `{"version":1,"requires":["tk-..."]}`를 담은 `dependencies.json`을 소유합니다. 디렉터리 basename과 `SKILL.md` frontmatter의 단일 일반·인용 `name:` 값은 정확히 일치해야 합니다. JSON 중복 키, 중복 edge, 알 수 없는 ID, 잘못된 schema, traversal과 symlink는 거부합니다. 순환과 공유 의존성은 유효합니다. 폐쇄에는 각 패키지가 정렬된 순서로 한 번씩 포함됩니다.

신뢰할 수 있는 설치 구현은 `read_package(base: Path, name: str) -> list[str]`도 내보냅니다. 이는 정확한 패키지 하나의 메타데이터, 선언과 symlink 경계를 검증하여 직접 요구 사항을 반환합니다. 설치된 전체 의존성 폐쇄를 검증하거나 설치를 승인하지 않습니다. gallery와 기존 report 도우미는 `tk-writing`을 사용하기 전에 `runpy.run_path`로 같은 컬렉션의 이 명시적인 파일을 로드합니다(설치된 bytecode를 쓰지 않습니다). 이들은 setup 패키지를 직접 의존성으로 선언하며 실행하는 Python 환경에 PyYAML이 필요합니다. 파서 로드는 여전히 지연됩니다. 빈 대상 카탈로그 계획에는 여전히 표준 라이브러리만 필요합니다. 이 API는 코드 진위 증명이 아닙니다.

<a id="exact-destination-and-installer-guidance"></a>
## 정확한 목적지와 설치기 안내

지원되는 고정 `skills@1.7.4` 에이전트 ID는 `codex`, `claude-code`, `hermes-agent`입니다. 프로젝트 대상은 임의의 스킬 폴더가 아니라 기존 절대 프로젝트 디렉터리(설치기 `cwd`)를 뜻합니다. 각각의 프로젝트 형제 루트는 `.agents/skills`, `.claude/skills`, `.hermes/skills`입니다. 명시적인 `global` 범위에서는 대상이 현재의 절대 HOME이어야 합니다. 같은 상대 루트가 적용됩니다. 전역 환경 override(`CODEX_HOME`, `CLAUDE_CONFIG_DIR`, `HERMES_HOME`)는 재작성하지 않고 거부하여 호스트별 수동 안내를 받게 합니다. 운영체제 디렉터리 별칭을 먼저 해석합니다. symlink인 루트, 패키지 파일과 목적지 경계는 지원하지 않으며 dangling symlink도 포함됩니다. 다른 에이전트나 임의 목적지에는 추측한 옵션이 아니라 최신 설치기 근거와 수동 안내가 필요합니다.

`plan`은 정확한 목적지에서 선택한 의존성 폐쇄만 확인합니다. 호환되는 기존 패키지는 `present`에 나타나고, `missing`만 설치기 `--skill` 인수에 나타납니다. 호환되지 않는 선언이나 안전하지 않은 경로는 계획을 중단합니다. 누락 항목이 없으면 `argv`는 비어 있습니다. 기존 선언은 내용의 최신성, 출처 revision이나 진위를 증명하지 않습니다. 담당 워크플로를 계속하기 전에 이를 별도로 검증합니다.

설치기 argv는 배열이며, `cwd`와 `installed_root`는 별도로 출력됩니다. 고정된 `npx --yes skills@1.7.4 add SOURCE --skill ID... --agent AGENT --copy`를 사용하며, 명시적인 경우에만 `--global`을 사용합니다. 앞쪽 npx의 `--yes`는 패키지 해석만 허용합니다. 덮어쓰기 질문을 억제하지 않도록 설치기 `--yes`는 의도적으로 빠져 있습니다. `--copy`는 symlink를 배포 계약으로 사용하지 않게 합니다. 설치기 도움말과 에이전트 경로는 로컬에 캐시된 1.7.4 소스·도움말과 대조하여 확인했습니다. 임의 버전이 동작한다고 주장하지 않습니다.
나중에 사람이 실행하면 npx가 코드를 가져오고 설치기가 출처 가져오기, lock 메타데이터 생성과 파일 설치를 수행할 수 있습니다. 계획 자체는 이를 하지 않습니다. 이어 붙인 문자열을 shell에 넘기지 않습니다. 출처의 shell 메타문자는 하나의 리터럴 argv 항목으로 남습니다. 옵션처럼 보이거나 제어 텍스트인 출처는 거부합니다. 승인된 설치 직전에 출처 신뢰, 정확한 목적지, 관련 기존 내용과 고정 설치기의 현재 동작을 다시 확인합니다. 오래된 계획을 실행하거나 덮어쓰기 질문을 무시하지 않습니다.

<a id="maintainer-only-catalog-generation"></a>
## 유지보수자 전용 카탈로그 생성

```sh
python3 scripts/skill_dependencies.py build-catalog --root /absolute/trusted/checkout
python3 scripts/skill_dependencies.py build-catalog --root /absolute/trusted/checkout --output skills/tk-setup-skills/references/install-catalog.json
```

`--output`이 없으면 생성은 메타데이터만 출력합니다. 명시적인 출력은 파일을 쓰는 유일한 명령입니다. 부모 디렉터리가 있어야 하며 symlink 경계를 넘어서는 안 됩니다. 승인된 소스 checkout에서만 다시 생성하고, 자동 런타임 복구로 사용하지 않습니다. 생성된 카탈로그를 같은 출처 선언과 대조하여 검증합니다. 카탈로그에는 정확한 ID와 의존성 edge가 들어가며 스킬·참조 콘텐츠 사본, 네트워크 URL이나 추론한 출처 권한은 들어가지 않습니다. 포함된 카탈로그와 호환되는 신뢰할 수 있는 출처·revision을 명시적으로 선택합니다.
