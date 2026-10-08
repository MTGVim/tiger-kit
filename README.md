# TigerKit

`Claude Code`, `Codex`, `Hermes Agent`에서 필요한 순간에 골라 쓰는 에이전트 스킬 모음입니다.
각 스킬은 독립된 역할과 완료 기준을 갖고, 조사·구현·검증·발행을 필요에 따라 조합합니다.
작고 명확한 일반 수정은 스킬 없이 처리해도 됩니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill '*'
npx skills update --global --yes
```

필요한 스킬만 선택할 수 있습니다. `Claude Code`와 `Hermes`에서는 `/tk-prep`,
`Codex`에서는 `$tk-prep` 또는 스킬 선택기를 사용합니다.
이름 변경과 제거는 [설치·마이그레이션](MIGRATION.md)을 참고하세요.

## 어디서 시작하나요?

- **만들기:** `tk-prep`에서 준비·승인·로컬 구현을 진행합니다. 작업 크기에 따라 직접 수정, `Ready Seed`, `SDD`, 인계를 선택하고 기본 브랜치에서는 작업 공간을 격리합니다.
- **이해하기:** `tk-ask-repo`에서 현재 코드의 근거를 찾고, `tk-explain`·`tk-explain-diff`에서 배경지식부터 읽을 수 있는 오프라인 HTML 설명을 만듭니다.
- **발굴·연구:** `tk-audit`에서 기술 일감을 감사하고, `tk-research`에서 접근법을 비교합니다.
- **검증·발행:** `tk-review`와 필요한 실행 검증을 거쳐 `tk-pr-open`으로 발행합니다. 로컬 실행 승인은 원격 푸시나 PR 발행 승인으로 확대되지 않습니다.

## 스킬 구성

`user`는 사용자가 명시적으로 호출합니다. `hybrid`는 사용자가 호출하거나 작업에 맞으면
에이전트가 선택할 수 있습니다. 행동과 권한은 링크된 `SKILL.md`가 정합니다.

### 개발·기획

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-prep](skills/tk-prep/SKILL.md) | `user` | 준비·승인부터 격리된 로컬 구현·검증·커밋까지 진행합니다. |
| [tk-roadmap](skills/tk-roadmap/SKILL.md) | `user` | 목표와 제약을 인터뷰해 성과 중심 마일스톤을 만듭니다. |
| [tk-audit](skills/tk-audit/SKILL.md) | `user` | 기술 일감·추적기 중복·정책 구조를 읽기 전용으로 감사합니다. |
| [tk-prototype](skills/tk-prototype/SKILL.md) | `hybrid` | 판단에 필요한 폐기 가능한 UI·로직 비교물을 만듭니다. |
| [tk-domain](skills/tk-domain/SKILL.md) | `hybrid` | 저장소 고유 용어와 지속할 결정 맥락을 작성·정제합니다. |
| [tk-merge-conflict](skills/tk-merge-conflict/SKILL.md) | `hybrid` | 활성 Git 충돌의 양쪽 의도를 복원합니다. |

### 검토·검증

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-review](skills/tk-review/SKILL.md) | `user` | 정확한 커밋 범위·PR·현재 작업 공간을 명세와 품질 관점에서 읽기 전용으로 검토합니다. |
| [tk-browser-verify](skills/tk-browser-verify/SKILL.md) | `hybrid` | 브라우저 화면의 실행 근거를 수집하고 `headless` 방식으로 검증합니다. |
| [tk-app-verify](skills/tk-app-verify/SKILL.md) | `hybrid` | 데스크톱 앱의 창·상호작용·시각적 변경·접근성을 검증합니다. |
| [tk-qa-sheet](skills/tk-qa-sheet/SKILL.md) | `user` | HTML QA 시트에서 자동 검증 근거와 사용자의 수동 체크를 구분합니다. |

### PR 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-pr-open](skills/tk-pr-open/SKILL.md) | `hybrid` | 검증된 커밋의 단일·연속 PR 발행을 준비하고 승인된 푸시·PR 생성을 수행합니다. |
| [tk-pr-respond](skills/tk-pr-respond/SKILL.md) | `hybrid` | 한 PR의 리뷰·지원 CI를 분석하고 승인된 수정·검증·답변을 진행합니다. |
| [tk-pr-rebase](skills/tk-pr-rebase/SKILL.md) | `hybrid` | 정확한 `PR`을 최신 기준 브랜치에 `rebase`하고 제한된 `force-with-lease`를 수행합니다. |
| [tk-pr-sweep](skills/tk-pr-sweep/SKILL.md) | `user` | 여러 PR을 결정론적으로 분류하고 승인된 유지보수 묶음을 처리합니다. |
| [tk-pr-image](skills/tk-pr-image/SKILL.md) | `hybrid` | 기존 PR에 로컬 검증 이미지를 올립니다. |

### 이해·연구·학습

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-ask-repo](skills/tk-ask-repo/SKILL.md) | `user` | 현재 저장소의 동작·값·영향·귀속을 근거와 함께 설명합니다. |
| [tk-explain](skills/tk-explain/SKILL.md) | `hybrid` | 배경지식과 실제 구조·동작을 자체 완결형 HTML로 설명합니다. |
| [tk-explain-diff](skills/tk-explain-diff/SKILL.md) | `hybrid` | 특정 코드 변경을 기존 구조와 실행 흐름부터 설명합니다. |
| [tk-research](skills/tk-research/SKILL.md) | `hybrid` | 외부 비교부터 지속 연구·실험·재개까지 필요한 단계만 수행하고 HTML 결과를 제공합니다. |
| [tk-teach](skills/tk-teach/SKILL.md) | `hybrid` | 실제 학습 기록으로 맞춤 수업·복습과 HTML 강의를 구성합니다. |

### 대화·글쓰기

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-grill](skills/tk-grill/SKILL.md) | `user` | 아이디어·계획·결정을 인터뷰해 공통 이해를 확인합니다. |
| [tk-to-questionnaire](skills/tk-to-questionnaire/SKILL.md) | `hybrid` | 다른 담당자에게 보낼 질문 초안을 말투·채널별 템플릿에 맞춰 작성합니다. |
| [tk-adhd](skills/tk-adhd/SKILL.md) | `hybrid` | 답변과 작업 결과에서 핵심·실행 단계를 찾기 쉽게 구성합니다. |
| [tk-rewrite](skills/tk-rewrite/SKILL.md) | `hybrid` | 기존 글의 맥락·구조와 표현을 정제합니다. |

### 세션·환경 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-retro](skills/tk-retro/SKILL.md) | `hybrid` | 세션 과정과 스킬 사고를 회고해 개선안을 제안합니다. |
| [tk-grooming](skills/tk-grooming/SKILL.md) | `hybrid` | 스킬·지속 규칙·자동 기억의 중복·충돌·낡은 지침을 감사합니다. |
| [tk-handoff](skills/tk-handoff/SKILL.md) | `hybrid` | 현재 대화의 현황을 확인하거나 재개용 인수인계를 작성·복원합니다. |
| [tk-wizard](skills/tk-wizard/SKILL.md) | `hybrid` | 사람이 직접 해야 하는 설정·인증·이관 절차를 안내합니다. |

## 프로젝트 설정

공유 정책은 선택적인 `tigerkit.config.json`, 개인 정책은 무시된 `.tigerkit/repository.json`에 둡니다.
스크립트가 소비하는 ID·경로는 정형 타입을 유지하고, 모델이 해석하는 정책과
`questionnaire.templates.slack` 같은 템플릿은 `key: string`으로 작성할 수 있습니다.
중요한 설정이 없으면 근거를 조사한 뒤 필요한 결정만 묻고, 확인한 설정을 저장해 작업을 이어갑니다.
설정과 외부 자료는 원격 변경·메시지 전송·스크립트 실행 권한을 부여하지 않습니다.

`Orca` 작업 공간과 콜백은 `orca.yaml`·`.worktreeinclude`를 따릅니다.
`tk-prep`의 격리 절차와 `tk-pr-sweep`의 사용자 단위 `pr-triage.json` 설정은 각 스킬이 유지합니다.

## 브라우저 검증의 인증 및 실행 자원

`tk-prep`에서 승인된 화면 변경은 기존 순서대로 구현 전 기준 화면을 먼저 촬영합니다.
`tk-browser-verify`는 해당 캡처가 끝나면 실행 소유 브라우저와 개발서버를 즉시
종료하고, 스크린샷과 재실행 조건만 유지합니다. 에이전트가 서버를 실행할 때에는
같은 저장소에서 공유하는 배타적 잠금을 확보합니다. 윈도우 운영체제에서는
`msvcrt.locking`과 작업 객체를 사용합니다. 맥 운영체제와 리눅스에서는
`flock`과 프로세스 그룹을 사용합니다. 여러 작업 트리는 서버 실행권을 번갈아 사용합니다.
사용자가 직접 실행한 서버는 종료하지 않으며, 잠금 대기는 제한된 시간 안에서만 수행합니다.
구현과 리뷰가 완료된 뒤
최종 변경본을 확인할 때 필요한 실행 자원만 다시 시작하고, 검증 후 종료합니다.

같은 Git 저장소에 연결된 작업 트리에서는 **명시적으로 허용한 개발용 인증정보**에 한해
`tk-browser-verify/scripts/shared_auth.py`를 통해 토큰을 재사용할 수 있습니다.
실제 인증 서버 주소, 환경, 역할, 비밀이 아닌 계정 프로필 식별자로 사용 범위를
구별하며, 한 실행만 토큰 입력을 요청하도록 만료된 요청을 잠금 처리합니다.
인증정보를 자동으로 갱신하는 API 요청은 제공하지 않습니다. 인증이 만료되면 사용자가 입력할
`.tigerkit/secret-input/.../input.json`의 실제 상대경로와 절대경로를 안내하고,
현재 활성화된 실행에서 파일 변경을 감시해 검증을 재개합니다. 종료된 대화를
자동으로 다시 시작하는 데몬은 없습니다.

공유 인증정보는 Git 공통 메타데이터 디렉터리에 별도로 저장되며, 유닉스 계열 환경에서
사용자 소유 디렉터리 `0700`, 파일 `0600`을 검사합니다. **암호화 저장소가 아니므로**
동일한 운영체제 계정의 프로세스와 백업에서는 내용을 읽을 수 있습니다. 보안 정책상
비암호화 보관이 허용되지 않거나 파일 접근권한을 검증할 수 없는 플랫폼에서는
공유를 사용하지 않고 기존 일회용 입력을 유지합니다. 운영용 인증정보는
공유 캐시에 저장하지 않습니다. 자세한 조건과 수동 폐기 방법은
[브라우저 인증 참조](skills/tk-browser-verify/references/environment.md)를 확인하세요.

## 유지보수

원격 CI 없이 로컬 릴리즈 게이트를 실행합니다.

```bash
python3 scripts/run_seed_release_gate.py --baseline origin/main --candidate HEAD
```

게이트는 README의 스킬 누락·삭제 잔재·중복, 호출 방식, 스킬 링크, 문서 표와
공개 계약 변경에 따른 README 갱신 여부를 검사합니다. 행동 설명은 실제 스킬과 독립 검수로 대조합니다.
공개 변화가 없는 변경은 [문서 최신화 절차](MIGRATION.md#문서-최신화-릴리즈-게이트)에 따라 사유를 남깁니다.

`Matt Pocock`의 [스킬 구성](https://github.com/mattpocock/skills)을 참고했습니다.
개별 증류 근거와 [저작권 고지](NOTICE.md)를 보존합니다.
