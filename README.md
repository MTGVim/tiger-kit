# TigerKit

`Claude Code`, `Codex`, `Hermes Agent`에서 골라 쓰는 작고 조합 가능한 에이전트 스킬 모음입니다.

각 스킬은 필요한 작업에 맞게 선택하여 조합할 수 있습니다.

## 설치

```bash
npx --yes skills@1.7.4 add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill '*' --copy
```

전체 설치의 갱신에도 위 명령을 사용하고, 기존 내용과 덮어쓰기 대상을 먼저 확인합니다. 지원 버전의 `skills update`는 복사 모드를 보존하지 않습니다. 선택 설치의 갱신은 기존 선택·호스트·범위를 유지하며 `tk-setup-skills`로 필요한 업무 스킬과 공통 의존성을 함께 준비합니다. 설치기는 의존성을 자동 해결하지 않습니다.

`Claude Code`·`Hermes`는 `/tk-setup-skills`, `Codex`는 `$tk-setup-skills`로 호출합니다. **인자 없이 실행해도** 설치 환경을 읽기 전용으로 점검하고 스킬 설치·업데이트, 공통 지침, 사용법 가운데 필요한 기능을 안내합니다. 하고 싶은 일을 설명하면 관련 스킬 ID와 의존성·설치 위치를 조사해 제안하므로, 기술 식별자를 미리 입력할 필요가 없습니다. 설치는 출처·revision·대상·범위를 제시한 뒤 별도로 승인받아 실행합니다. 소스·설치본 검사와 gallery·legacy report CLI의 소유자 검사에는 `Python 3.9+`·`PyYAML`이 필요하며, 파서가 없으면 자동 설치하지 않고 중단합니다. 빈 대상의 카탈로그 계획은 표준 라이브러리만 사용합니다.

모든 TigerKit 저작(질문 초안·영상 대본/자막·HTML·Markdown·스킬 본문·설명·협업 메시지)은 생성 전과 인계 전에 `tk-writing`의 [공통 저작 품질 관문](skills/tk-writing/references/authoring-gate.md)을 적용합니다. 기존 스킬이 범위·권한·출력 계약을 유지하며, 정확한 리터럴과 기계 출력은 보호하고 추가 에이전트·승인 라운드를 강제하지 않습니다.

공통 기준·HTML 자원과 도우미는 `tk-writing` 등 참조 전용 소유 스킬에, 검증 registry·설정 도우미는 `tk-verification-guidance`에 한 번 둡니다. 선택한 스킬의 `dependencies.json` 전체 closure를 같은 설치 컬렉션에 준비해야 하며, 업무 패키지 하나만 복사하면 충분하다고 가정하지 않습니다. 소유자가 없으면 해당 단계를 중단하고 setup을 안내하며, 출력·임시 파일은 호출한 업무가 설치 패키지 밖에서 관리합니다.

`tk-explain`의 이미지 제작 분기에는 `tk-illustrate`가 필요합니다. 기존 선택 설치도 setup으로 이 의존성을 함께 갱신합니다. `tk-illustrate`와 `tk-comic`은 각각 직접 호출할 수 있습니다.

## 시작하기

일반 작업은 목적에 맞는 스킬 하나로 시작합니다. 이후 필요한 리뷰, 검증 및 다른 스킬은 기존 작업 절차에 따라 조합합니다. 모든 호출 순서를 외울 필요는 없습니다.

| 하고 싶은 일 | 권장 시작 스킬 |
| --- | --- |
| 기능 개발, 수정 또는 리팩터링 | [tk-prep](skills/tk-prep/SKILL.md) |
| 일감 등록·진행 상태 확인·다음 작업 시작 | [tk-tasks](skills/tk-tasks/SKILL.md) |
| 오류 원인 조사와 수정 | [tk-prep](skills/tk-prep/SKILL.md) |
| 아이디어와 결정 구체화 | [tk-grill](skills/tk-grill/SKILL.md) |
| 사용성 개선 및 신규 기능 발굴 | [tk-experience-review](skills/tk-experience-review/SKILL.md) |
| 장기 목표·마일스톤과 /goal용 실행 장부 작성·점검 | [tk-ralplan](skills/tk-ralplan/SKILL.md) |
| 현재 작업을 다른 세션으로 인계 | [tk-handoff](skills/tk-handoff/SKILL.md) |
| AI의 설명·판단이 이상할 때 교정안 제안받기 | [tk-sowhat](skills/tk-sowhat/SKILL.md) |

스킬 호출에서 명령과 옵션은 `foo` 형태의 키워드를 사용합니다. 실제 CLI 명령의 플래그는 변경하지 않습니다.

### 대표 사용 예시

```text
using tk-prep, 검색 화면에 필터 기능을 추가해 주세요.
using tk-tasks, 이 개선 작업은 일감으로 남겨두고 기존 진행 중인 작업을 확인해 주세요.
using tk-prep, 결제 버튼을 누르면 오류가 발생하는 원인만 조사해 주세요.
using tk-grill, 새 기능의 요구사항을 함께 구체화해 주세요.
using tk-ralplan, 다음 분기의 개선 목표와 마일스톤을 /goal 계획으로 정리해 주세요.
using tk-sowhat, 방금 답변에서 무엇이 확실하고 무엇을 해야 하는지 다시 판단해 주세요. 실행은 승인 후에요.
```

### 사용자 공통 한국어 지침 설치

`tk-setup-skills`에는 Claude Code의 `~/.claude/CLAUDE.md`, Codex의 `~/.codex/AGENTS.md`, Hermes의 기존 `~/.hermes/SOUL.md`에 적용할 한국어 대화 지침이 포함되어 있습니다. 개인 저장소 없이도 설치할 수 있습니다.

```text
using tk-setup-skills, user-guidance를 세 에이전트에 적용할 변경을 먼저 점검해 주세요.
```

사용자가 설치를 승인하면 해당 스킬의 `--apply` 절차로 백업 후 반영합니다. 예전 `fluent-korean` 관리 블록만 정리하고 사용자 작성 지침은 유지합니다. 자세한 내용은 [설치 절차](skills/tk-setup-skills/SKILL.md#user-guidance-install)를 참고합니다.

### 업무 Task 관리

`tk-tasks`는 구현·진단·조사·리뷰 등 독립 업무가 대화에서 사라지지 않도록 호스트의 작업 목록에 등록하고 추적합니다. 미완료 선행 업무에 의존하면 `planned` 의미로 보류하고, 즉시 수행 가능한 업무는 `in_progress` 의미로 착수합니다. Orca Bot에서는 Items를 우선 사용하며 독립 Task당 주 Worker·프로젝트 Worktree 하나를 Bot 아래에 연결합니다. 내부 Todo에 Worker를 추가 생성하지 않고, 검증과 PR 등 최종 납품을 마친 뒤 Worktree 정리를 사용자에게 한 번 묻습니다. Orca 외 환경에서는 기본 Todo 도구만 사용하며 자체 Task 파일·CLI·실행기를 추가하지 않습니다. 기존 업무 스킬이 구현과 검증을 계속 담당합니다.

### Ralph 반복 작업용 계획 준비

`tk-ralplan`은 인터뷰와 저장소 조사를 통해 목표·전체 성공 기준·Task·현재 상태·결정·검증 근거를 한 Markdown 장부로 준비하고 점검합니다. `### Task N:`와 체크박스는 Ralphex 호환 표기를 유지하지만 외부 Ralphex CLI, 모델 옵션, 원샷 스크립트는 사용하지 않습니다. 실행은 사용자가 지원을 확인한 Claude Code·Codex·Hermes의 `/goal`에 장부를 전달해 수행합니다.

```text
using tk-ralplan, 현재 작업의 목표와 검증 기준을 /goal용 장부로 준비해 주세요.
using tk-ralplan check docs/plans/feature.md
```

계획 장부는 기본적으로 `.tigerkit/ralph/<slug>.md`에 작성합니다. 준비된 장부를 호스트에서 `/goal <plan-path>`로 전달하며 인수 지원은 호스트에서 확인합니다. `tk-ralplan`은 외부 실행기·시작 스크립트를 만들거나 목표 실행을 직접 담당하지 않습니다. 과거 `tk-goal` 제거 및 새 방향은 [ADR 0007](docs/adr/0007-retire-tk-goal-use-ralphex-plan.md)을 따릅니다.

### 위임 모드

`tk-route-mode`는 인자 없이 상태를 확인합니다. `tk-route-mode standard`와 `tk-route-mode economy`는 승인된 프로필과 위임 규칙을 함께 적용·검증하며, `tk-route-mode update`는 최신 벤치마크와 공식 모델 지원 수명주기를 비교한 뒤 승인받아 갱신합니다. 신규 기본값의 OpenAI top은 GPT-6.2 Sol medium이며 기존 사용자 설정은 자동 변경하지 않습니다. Hermes는 [프로필별 advanced-delegation 설정·검증 안내](skills/tk-route-mode/references/hermes-setup.md)를 사용합니다. Terra 6.1의 Effort 고정 시범 재채용 경위는 [ADR 0009](docs/adr/0009-route-mode-terra-retrial.md)에 기록했습니다.

## 스킬 구성

`user`는 명시적인 스킬 호출로만 시작하며, `hybrid`는 명시적 호출 외에 자연어 요청에서 자동 선택될 수도 있습니다. 자동 선택은 구현·설치·원격 발행 등 별도 행동에 대한 승인이 아닙니다. 상세한 권한과 진입 조건은 각 스킬 문서에 있습니다.

### 개발·기획

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-prep](skills/tk-prep/SKILL.md) | `hybrid` | 읽기 전용 오류 진단과 자연어 SWE 착수·구현을 담당하고 승인된 로컬 구현·검증을 진행합니다. |
| [tk-tasks](skills/tk-tasks/SKILL.md) | `hybrid` | 자연어 일감을 호스트 Task에 등록·재개·추적합니다. Orca 우선, 다른 호스트는 기본 Todo만 활용합니다. |
| [tk-ralplan](skills/tk-ralplan/SKILL.md) | `user` | /goal용 목표·작업·현재 상태·검증 장부를 작성합니다. Task 형식은 Ralphex 호환입니다. |
| [tk-audit](skills/tk-audit/SKILL.md) | `hybrid` | 저장소의 기술 일감을 읽기 전용으로 감사합니다. |
| [tk-prototype](skills/tk-prototype/SKILL.md) | `hybrid` | UI·로직 대안을 비교하는 시제품을 만듭니다. |
| [tk-experience-review](skills/tk-experience-review/SKILL.md) | `hybrid` | 사용자 경험과 외부 레퍼런스에서 개선·신규 기능 일감을 발굴합니다. |
| [tk-domain](skills/tk-domain/SKILL.md) | `hybrid` | 저장소 용어와 지속할 결정을 정리합니다. |
| [tk-merge-conflict](skills/tk-merge-conflict/SKILL.md) | `hybrid` | 활성 Git 충돌의 의도를 복원하고 해결합니다. |

### 검토·검증

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-review](skills/tk-review/SKILL.md) | `hybrid` | 지정한 변경을 명세와 품질 기준으로 검토합니다. |
| [tk-browser-verify](skills/tk-browser-verify/SKILL.md) | `hybrid` | Playwright CLI 기본 화면·동작 검증, 명시적 접근성 결함 탐색과 데모 캡처를 담당합니다. |
| [tk-app-verify](skills/tk-app-verify/SKILL.md) | `hybrid` | 데스크톱 앱의 동작·화면·접근성을 검증합니다. |
| [tk-blind-comparison](skills/tk-blind-comparison/SKILL.md) | `hybrid` | 정체를 가린 후보의 점수와 메모를 로컬 갤러리에서 비교합니다. |
| [tk-qa-sheet](skills/tk-qa-sheet/SKILL.md) | `user` | 수동 점검을 기록하는 HTML 시트를 만듭니다. |

### PR 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-pr-open](skills/tk-pr-open/SKILL.md) | `hybrid` | 검증된 변경의 PR 발행을 준비하고 승인된 작업을 수행합니다. |
| [tk-pr-respond](skills/tk-pr-respond/SKILL.md) | `hybrid` | 한 PR의 리뷰와 지원 CI에 대응합니다. |
| [tk-pr-rebase](skills/tk-pr-rebase/SKILL.md) | `hybrid` | 지정 PR의 기준 브랜치 갱신과 `tk-pr-sweep`·`tk-pr-respond`의 승인된 작업 넘김을 처리합니다. |
| [tk-pr-sweep](skills/tk-pr-sweep/SKILL.md) | `user` | 여러 PR을 분류하고 승인된 유지보수를 처리합니다. |
| [tk-pr-media](skills/tk-pr-media/SKILL.md) | `hybrid` | PR에 로컬 이미지·GIF·영상을 올립니다. |

### 이해·연구·학습

개념·상황·코드 변경 설명과 실제 답변에 맞춘 후속 수업은 `tk-explain`을 사용합니다. 두 스킬은 일반 질문에 필요한 배경·근거·한계까지 대화로 설명합니다. `tk-explain`은 파일을 요청하거나 표현 선택을 위임하면 자료를 제작하고, `tk-research`는 별도 산출물을 요청한 경우에 제작합니다.

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-ask-repo](skills/tk-ask-repo/SKILL.md) | `hybrid` | 저장소의 동작과 근거를 설명합니다. |
| [tk-explain](skills/tk-explain/SKILL.md) | `hybrid` | 개념·코드 변경을 설명하고 후속 수업과 기존 설명 페이지의 피드백 반영을 지원합니다. |
| [tk-illustrate](skills/tk-illustrate/SKILL.md) | `hybrid` | 단일 그림·문서 삽화·인포그래픽을 제작하며, 이미지 도구가 없으면 MOSS 로컬 폴백·분리 식질 또는 콘티·프롬프트 전달을 선택합니다. |
| [tk-comic](skills/tk-comic/SKILL.md) | `hybrid` | 교육용 만화를 제작하고 부분 제작·페이지 복구를 지원하며, 도구가 없으면 MOSS 로컬 폴백·분리 식질 또는 외부 인계를 선택합니다. |
| [tk-video](skills/tk-video/SKILL.md) | `hybrid` | 소프트웨어와 개념을 설명하는 MP4·GIF 영상을 만듭니다. |
| [tk-research](skills/tk-research/SKILL.md) | `hybrid` | 근거를 조사하고 접근법을 비교합니다. |
| [tk-tts](skills/tk-tts/SKILL.md) | `hybrid` | 한국어 원고에서 검수 가능한 로컬 음원을 생성합니다. |

### 대화·글쓰기

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-grill](skills/tk-grill/SKILL.md) | `hybrid` | 아이디어와 결정을 질문으로 구체화합니다. |
| [tk-inquiry](skills/tk-inquiry/SKILL.md) | `hybrid` | 다른 담당자에게 보낼 질문 초안을 작성합니다. |
| [tk-sowhat](skills/tk-sowhat/SKILL.md) | `user` | 잘못된 판단과 설명을 읽기 전용으로 교정하고 실행 제안·승인 질문만 제공합니다. |
| [tk-rewrite](skills/tk-rewrite/SKILL.md) | `hybrid` | 기존 글의 어조·뉘앙스·독자 맥락을 요청에 맞춰 다듬습니다. |

### 세션·환경 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-retro](skills/tk-retro/SKILL.md) | `hybrid` | 세션을 회고하고 개선안을 제안합니다. |
| [tk-compound](skills/tk-compound/SKILL.md) | `user` | 완료 PR에서 반복 문제와 예방책을 찾습니다. |
| [tk-grooming](skills/tk-grooming/SKILL.md) | `hybrid` | 스킬·지속 규칙을 감사하고 최근 7일의 관련 런타임 기록을 진단합니다. |
| [tk-skill-vet](skills/tk-skill-vet/SKILL.md) | `hybrid` | 외부 스킬의 설치 전 보안 위험과 업데이트 동작을 정적으로 검토합니다. |
| [tk-handoff](skills/tk-handoff/SKILL.md) | `hybrid` | 세션 현황을 확인하고 일반 또는 장기 작업 인계를 작성하고 복원합니다. |
| [tk-route-mode](skills/tk-route-mode/SKILL.md) | `user` | 위임 티어별 기본/절약 모드를 설정하고 승인된 호스트 설정을 적용, 검증 및 복원합니다. |
| [tk-setup-skills](skills/tk-setup-skills/SKILL.md) | `user` | 필요한 스킬과 공통 의존성의 설치·설정을 지원합니다. |
| [tk-wizard](skills/tk-wizard/SKILL.md) | `hybrid` | 설정·인증·이관을 대화나 일회성 Bash Wizard로 안내합니다. |

### 공통 참조

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-questioning](skills/tk-questioning/SKILL.md) | `hybrid` | 질문·승인 라운드와 시각적 질문 기준을 제공합니다. |
| [tk-artifacts](skills/tk-artifacts/SKILL.md) | `hybrid` | 파일 경로·비밀 입력·인증 보존 기준을 제공합니다. |
| [tk-ui-evidence](skills/tk-ui-evidence/SKILL.md) | `hybrid` | UI 문구와 진입 경로의 근거 기준을 제공합니다. |
| [tk-writing](skills/tk-writing/SKILL.md) | `hybrid` | 글쓰기·설명·HTML 기준과 공통 자원·도우미를 제공합니다. |
| [tk-engineering](skills/tk-engineering/SKILL.md) | `hybrid` | 테스트·진단·리뷰·SDD 기준을 제공합니다. |
| [tk-repository-guidance](skills/tk-repository-guidance/SKILL.md) | `hybrid` | 저장소 맥락·도메인 문서·외부 계약 기준을 제공합니다. |
| [tk-pr-guidance](skills/tk-pr-guidance/SKILL.md) | `hybrid` | PR 본문 GFM·전달·시각 자료·리베이스 준비 기준을 제공합니다. |
| [tk-verification-guidance](skills/tk-verification-guidance/SKILL.md) | `hybrid` | 검증 제공자 선택·근거 기준과 registry·설정 도우미를 제공합니다. |

## 참고

- [설치 마이그레이션](MIGRATION.md)
- [릴리즈 체크리스트](RELEASE_CHECKLIST.md)
- [출처와 저작권 고지](NOTICE.md)
