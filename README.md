# TigerKit

TigerKit은 Claude Code, Codex, Hermes Agent용 독립 `Agent Skills` 모음입니다.
중앙 `workflow runtime`, `plugin`, `scheduler`, `shared state framework`가 아닙니다.
각 스킬은 `npx skills`로 배포합니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

갱신:

```bash
npx skills update --global --yes
```

Claude Code/Hermes에서는 `/tk-prep`, Codex에서는 `$tk-prep` 또는 스킬 선택기를 사용합니다.

## 기본 흐름

```text
요청 / issue / bug / review
          ↓
       tk-prep
          ↓
 final local-mutation approval
          ↓
 direct/no-Seed | Ready Seed | SDD | handoff
          ↓
 review / verification
          ↓
       commit
          ↓
 optional tk-review
          ↓
     tk-pr-open
```

`tk-prep`은 저장소 근거와 자연스러운 대화로 작업을 명확하게 만들고, 최종 승인 뒤 작업 크기에 맞는
로컬 실행을 수행합니다. 작고 명확한 같은 세션 작업은 `Seed` 없이 직접 진행할 수 있고, 인계/압축/
낮은 역량 실행/SDD에는 표시된 Ready `.tigerkit/seed.md`를 만듭니다. 원격 발행은 별도 담당자가 처리합니다.

작은 수정과 평범한 후속 의견은 스킬 없이 현재 대화에서 바로 처리합니다.

모든 스킬은 새로 작성하는 제목·목록·선택지에 `(1) 항목`, `1. 항목`처럼 번호 뒤에 공백을 둡니다.
터미널에서 글자와 겹칠 수 있는 원문자 숫자·단일 문자 괄호 숫자·숫자 이모지를 항목 번호로 사용하지 않습니다.
코드·인용문·실제 UI 라벨 등 정확히 보존해야 하는 문자열은 유지합니다.

사용자에게 결정이나 승인을 물어야 할 때는 근거로 확인할 사실을 먼저 조사합니다. 그다음 다른 미해결
답변에 의존하지 않고 지금 답할 수 있는 질문 전체를 한 번의 일반 채팅에 묶어 제시합니다.
`tk-grill`과 같은 `❓ Q1` 형식과 추천 이유를 사용하고, 선행 답변이 필요한 질문은 다음 라운드로 미룹니다.
분석, 설명, 주의사항과 실행 계획을 먼저 마친 뒤 질문 묶음을 메시지의 마지막에 둡니다.
질문 뒤에는 새로운 본문을 덧붙이지 않으며, 짧은 응답 형식 안내는 질문 묶음 안에 포함합니다.
일반 질문에는 `AskUserQuestion`, `request_user_input`, `clarify`를 사용하지 않습니다. 일반 채팅으로
동일한 의미와 권한을 표현할 수 없는 호스트의 필수 구조화 입력만 예외로 인정합니다.

## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | 적응형 준비 + 승인된 직접/Ready `Seed`/SDD/인계 로컬 실행 |
| `tk-grill` | `user` | 아이디어·계획·결정의 빠짐없는 점검과 확인된 `shared understanding` |
| `tk-autoresearch` | `user` | 열린 연구 목표의 방향·질문·가설·실험을 근거에 따라 갱신하고 충분히 수렴하면 종료 |
| `tk-roadmap` | `user` | 목표와 기술·비기술 제약을 고려하는 단계별 기획 인터뷰와 성과 중심 마일스톤 |
| `tk-audit` | `user` | 읽기 전용 저장소 감사와 `AUD-*` 발견 사항, `policy`로 비즈니스 정책 구조 검토 |
| `tk-research` | `hybrid` | 외부 사례·접근법을 깊이 비교하고 최소 충분한 해결 방식 제안 |
| `tk-ask-repo` | `user` | 저장소 동작·값·영향·귀속을 근거와 함께 설명 |
| `tk-review` | `user` | 정확한 커밋 범위/`PR`/`current worktree`의 읽기 전용 `Spec/AC` + `Quality/Standards` 검토 |
| `tk-pr-open` | `hybrid` | 검증된 `commit`의 `single` 또는 `stacked` 발행 계획 + 제한된 `push`/PR 생성·갱신 |
| `tk-pr-respond` | `hybrid` | 한 PR의 리뷰/지원 CI 분석·수정·검증·`reply`/`resolve` |
| `tk-pr-rebase` | `hybrid` | 정확한 PR의 최신 `base` `rebase`와 제한된 `force-with-lease` |
| `tk-pr-sweep` | `user` | 여러 PR의 결정론적 분류와 승인된 유지보수 묶음 |
| `tk-pr-image` | `hybrid` | 기존 PR에 로컬 근거 이미지 올리기 |
| `tk-prototype` | `hybrid` | 폐기 가능한 UI/로직 비교물 |
| `tk-explain` | `hybrid` | 배경지식과 실제 구조·동작을 시각화하는 자체 완결형 HTML 설명 자료 |
| `tk-explain-diff` | `hybrid` | 특정 코드 변경을 기존 구조와 실행 흐름부터 설명하는 자료 |
| `tk-study` | `hybrid` | 선수지식과 목표에 맞춰 조사하고 여러 챕터로 구성하는 HTML 학습 과정 |
| `tk-browser-verify` | `hybrid` | 화면에 보이는 AC의 `headless` 실행 검증과 읽기 전용 라벨·진입 경로 조사 |
| `tk-app-verify` | `hybrid` | 데스크톱 앱의 창, 상호작용, 시각적 변경과 접근성을 선택한 `provider`로 읽기 전용 검증 |
| `tk-skill-diagnose` | `hybrid` | `Agent Skill` 사고 재현·격리와 `learn-ready` 인계, 승인된 수정은 `tk-learn`으로 연속 진행 |
| `tk-learn` | `hybrid` | 재사용 가능한 스킬의 익명 이슈·PRD 초안을 임시 공간에 먼저 저장하고, 승인한 대상만 생성/개선/병합. 기존 검사 도구로 막을 수 있는 문제는 해당 도구의 최소 확장을 우선 제안 |
| `tk-domain` | `hybrid` | 저장소 고유 용어의 `canonical vocabulary`와 `sparse durable decision/ADR context` 작성·정제 |
| `tk-grooming` | `hybrid` | 기존 스킬·지속 `rule`·`auto memory`의 중복·충돌·낡은 지침 감사 |
| `tk-handoff` | `hybrid` | 진행 중 작업의 재개용 상태 사진 |
| `tk-adhd` | `hybrid` | 세션 전환 후 목표·진행·다음 행동을 짧게 안내 |
| `tk-rewrite` | `hybrid` | 기존 글의 맥락·구조 재구성과 표현 정제 |
| `tk-merge-conflict` | `hybrid` | 활성 Git 충돌 의도 복원 |
| `tk-wizard` | `hybrid` | 사람이 직접 해야 하는 설정·인증·이관 절차 안내 |

기존 `tk-github-image-upload-to-pr`의 이름은 `tk-pr-image`로 변경했습니다.

`user`는 명시 호출 전용이고, `hybrid`는 해당 작업 의도가 명확할 때 자동 진입할 수 있습니다.

UI 라벨과 진입 경로를 설명하는 스킬은 실제 표시 문자열과 경로의 각 연결을 근거로 확인합니다.
`tk-ask-repo`는 저장소만으로 확인할 수 없으면 외부 결정 위치와 미확인 항목을 밝히고, 접근 가능한
브라우저 근거를 조사하거나 메뉴명·계층·경로가 담긴 비밀정보를 제거한 API 응답 또는 화면을 요청합니다.
확인하지 못한 경로는 요약·QA·인계에서도 실행 가능한 안내로 바꾸지 않습니다.
브라우저 조사에서는 진입 후 현재 렌더링된 텍스트를 한 번 수집하고, `breadcrumb`·헤더의 라벨과 실제 클릭 경로를 구분합니다.
`tk-pr-open`은 발행 전에 미확인 라벨·경로별 근거, 한계, 필요한 입력을 보고합니다. 사용자가 항목별로
제공한 정확한 문구·화면은 출처를 표시해 반영하고, 필수 QA·발행 근거가 미확인 상태이면 발행을 중단합니다.

`tk-audit`은 저장소·실행 근거로 동일한 인과 원인, 수정 경계, 실패 유형이 확인된 여러 증상을 하나의
원인 `finding`으로 묶고 영향을 받은 표면을 연결합니다. 원인이나 되돌리기·위험·검증 경계가 독립적이면
별도 `finding`으로 유지합니다.

## `tk-prep`, 직접 실행, `Seed`, SDD

`tk-prep`은 고정 양식 위저드가 아닙니다.
내부적으로는 명확도와 엔지니어링 준비도를 엄격하게 평가하지만,
사용자에게는 현재 이해, 추천, 이유를 자연스러운 대화로 설명합니다.

사용자에게 직접 묻는 것은 제품/범위 같은 사용자 소유 결정, 위험하거나 비가역적인 결정,
충분히 개선한 뒤에도 남는 엔지니어링 예외 승인뿐입니다.
범위 질문에 답을 받으면 남은 조사를 계속하고, 검토 가능한 실행안을 제시한 뒤 최종 승인을 기다립니다.
실제 차단 사유나 사용자 중단 지시가 없다면 확인 답변만으로 준비를 끝내지 않습니다.
실행안은 대화로 제시할 수 있으며, 승인 전 파일 생성은 의무가 아닙니다.

승인 전에는 목표와 범위가 실행 가능하게 명확하고, 중요한 제품 결정이 해결됐으며,
AC와 검증 방법이 실행 가능하고, 중대한 근거 충돌이나 차단 요인이 없어야 합니다.
사용자 승인으로 근거 충돌이나 준비 차단 요인을 우회할 수 없습니다.

엔지니어링 준비도는 `Reuse`, `Simplicity`, `Testing`, `Security`, `User experience`를 독립적으로 확인하되,
준비됐거나 무관한 축을 의례적인 상태표로 출력하지 않습니다. 계획을 바꾸는 공백·예외·결정만 드러냅니다.

```text
Reuse
Simplicity
Testing
Security
User experience
```

드러난 축에는 `보완 필요 | 개선 한계 | 예외 승인`을 사용합니다. 먼저 추가 조사와 접근 개선을 시도하고,
더 끌어올릴 수 없을 때만 이유·남은 위험·완화책과 함께 실제로 필요한 예외 승인을 받습니다.

Ready `.tigerkit/seed.md`는 필요할 때만 만드는 현재 작업의 자체 완결 실행 맥락입니다. 인터뷰 중
`Status: Pending` 파일은 만들지 않고, 새 `Seed`는 TigerKit 소유 표시와 현재 작업 식별자를 가집니다.
`direct/no-Seed`는 기존 `Seed`를 그대로 보존하고 현재 작업에 사용하지 않습니다. 기존 파일의 식별자가
모호하다는 이유만으로 중단하지 않으며, 실제로 읽어 실행하거나 교체해야 할 때만 식별·소유권을 확인합니다.
목표/배경, 현재 상태, 범위, 사용자 결정, 구현 안내, AC, 검증, 브라우저 계획, 엔지니어링 예외를 구현자가 원 대화 없이 이해할 수 있게 담습니다.

`Seed`와 SDD `Unit`에는 인터페이스, 불변 조건, 검증 기준처럼 구현자가 저장소만 보고 복원할 수 없는 결정을 남깁니다. 일반 구현 코드는 복제하지 않으며, 알고리즘이나 순서 자체가 승인된 결정이면 필요한 최소 구조를 보존합니다.

`worker`/`wave` 진행 상태, 제공자 모델 선택자, 추론 강도, 영수증, 비밀 값은 `Seed`에 저장하지 않습니다.

코드 변경 직접/SDD 경로는 행동 우선 `RED → GREEN → REFACTOR`를 기본으로 하며 현실적인 변이를 잡는
테스트를 남깁니다. 순수 동작 보존 리팩터링은 수정 전 `GREEN`을 확보하고 구조를 변경한 뒤 같은 동작이
유지되는지 확인합니다. 실패를 만들기 위해 정상 코드를 깨뜨리지 않습니다. SDD는 `tk-prep`과 `tk-pr-respond`가 공유하는 패키지 로컬 절차로 정확한 `Unit` 범위 검토와
5회 수정 차단기를 사용합니다. 브라우저 증거는 자동 회귀 보호를 대체하지 않습니다.
사용자 의도·범위·완료 기준의 결정과 호스트가 부모 전용으로 지정한 승인은 계속 부모가 처리합니다.
현재 호스트가 자식의 정확한 요청·응답 연결, 동일 승인 정책과 안전한 재개를 보장하면 승인된 작업 범위의 인증·양식 입력은
같은 자식에서 이어갑니다. 지원 근거가 불명확하면 부모에게 전달하며, 새로운 권한이나 별도 상호작용 장부는 만들지 않습니다.

구현자와 리뷰어를 포함한 하위 에이전트는 같은 대상 환경에서 부모와 같거나 더 좁은 도구 및 데이터 접근 권한만 사용합니다.
현재 호스트의 권한 상속 근거를 확인할 수 없으면 위임하지 않으며, 다른 환경의 승인이나 이전 승인을 더 넓은 접근에 재사용하지 않습니다.
안전한 부모 실행 경로가 있으면 사용하되, 독립 리뷰를 부모의 자체 검토로 대체하지 않습니다.

열린 PR은 자동으로 탐색하지 않습니다. 사용자가 비교를 요청하거나 작업 근거로 지정한 PR만 필요한 범위에서 읽습니다.

최초 요청이나 앞선 대화에서 승인한 범위는 하위 스킬에도 이어집니다. 기준 화면 캡처, 구현, 검증, 리뷰, 로컬 커밋 사이에
다시 진행 여부를 묻지 않습니다. 원격 발행까지 명시적으로 승인했다면 해당 담당자가 이어서 수행하고, 새 범위나 실제 사용자 결정이 필요할 때만 질문합니다.

직접 실행의 최종 리뷰는 실제 변경과 검증 근거로 저위험임을 확인한 경우 독립 리뷰어 한 명이 수행합니다.
보안·권한, 저장 데이터, 공개 계약 호환성, 여러 경계에 걸친 상태·생명주기, 복잡하거나 불확실한 변경은
두 명이 수행합니다. SDD 전체 변경과 명시적인 `tk-review`는 두 명을 유지하며, 모든 리뷰어는 두 판정 축과
두 검토 절차를 모두 수행합니다.

각 리뷰어에게는 같은 검토 대상에서 이미 확보한 테스트·빌드·실행 근거를 전달합니다. 독립 리뷰는 병렬로
진행하지만 전체 테스트·빌드·개발 서버는 리뷰어가 다시 실행하지 않습니다. 남은 의문을 확인하는 집중 검사는
담당자가 실행 순서를 조율하여 다른 검사와 겹치지 않게 하고, 장시간 대기 보고는 실제 프로세스 상태를 확인한 뒤 전달합니다.

직접 실행에서 여러 `commit`이 필요하면 파일 종류나 계층이 아니라 독립적으로 이해·검증·되돌릴 수 있는
작업 단위로 나눕니다. 동작과 이를 입증하는 테스트 및 반드시 바뀌어야 하는 사실 문서는 가능한 한 같은
`commit`에 둡니다.

## 브라우저 검증

`browser-visible` AC가 있으면 `tk-prep`에서 대상, `headless`, 인증, `viewport`, 개발 서버, `criterion`별 `runtime` 근거와 통과 조건을 정합니다. `Visual/visible-state` 근거는 검증 대상이 실제 담긴 `screenshot`을 사용합니다.
비밀번호, `token`, OTP, `cookie`, `session` 비밀 값은 `Seed`에 저장하지 않고 실행 시 일시 입력으로만 다룹니다.

구현까지 승인한 작업에서는 기준 화면 촬영이 끝나면 같은 활성 턴에서 구현과 변경 후 비교를 계속합니다.
같은 에이전트의 `Skill` 호출과 별도 자식 실행에 모두 적용하며, 기준 화면 성공 보고만으로 부모 턴을 끝내지 않습니다.
촬영만 요청한 독립 실행이나 사용자가 명시적으로 중단한 작업에는 구현 권한을 추가하지 않습니다.

기준 화면과 변경 후 화면을 비교하거나 렌더링에 영향을 주는 후보를 검증할 때는 `visual.md` 계약을
적용하고 `visual_contract: applied`를 반환해야 합니다. 의도한 변경 영역에는 의도별로 `outline`을 표시하며,
촬영 방식·실제 화면 크기·촬영 전용 변경 사항을 근거 색인과 결과에 공개합니다. 콘텐츠 높이에 맞춘 캡처는
페이지 전체 근거가 필요하고 높이 의존 레이아웃·가상 목록·스크롤 지연 로딩 등이 없음을 확인한 경우에만 허용합니다.

개발 서버가 필요하면 시작·준비 확인·정리는 `tk-browser-verify`가 소유합니다.

브라우저와 데스크톱 앱은 검증 절차와 실제 조작 `provider`를 분리합니다. 두 스킬은 UI 원문 근거,
변경 전후 대조, 의도별 윤곽선, 실제 이미지 확인과 미확인 항목 보고 규칙을 공유합니다.
`tk-app-verify`는 앱과 빌드, 프로세스 및 창을 식별하고 접근성 트리와 창 캡처를 사용합니다.
앱 검증 결과에는 입력 방식과 포커스 영향도 기록하며, 사용자 소유 창이나 프로세스는 종료하지 않습니다.

처음 실행할 때는 호출 가능한 도구, 설치된 실행 파일, 버전, 권한과 지원 환경을 확인하고 가용 후보를
한 번의 질문 묶음으로 제시합니다. 선택은 기본적으로 `~/.config/tigerkit/verify.json`에 저장합니다.
`XDG_CONFIG_HOME`이 설정되어 있으면 그 아래 `tigerkit/verify.json`을 사용합니다.
이번 실행에만 적용하는 선택도 가능하며, 저장된 선택이 없거나 필요한 기능이 부족하면 사용자의
선택을 받습니다. 저장된 `fallbacks`는 대안 제시 순서이며 자동 실행 목록이 아닙니다.
브라우저의 기존 `headless` 및 실행 소유권 조건은 선택한 `provider`와 관계없이 유지합니다.

각 패키지에 포함된 [제공자 목록](skills/tk-browser-verify/references/providers.json)는
공식 사용 문서 URL, 탐지 정보, 가능한 기능과 입력·프로필 경계를 관리합니다.
[설정 계약](skills/tk-browser-verify/references/provider-selection.md)에 따라 불확실한 사용법은
공식 문서에서 다시 확인합니다. `docsOverrides`로 문서 URL을 지정할 수도 있습니다.
`Cua Driver`, `Orca`, `Codex` 및 `Claude` 내장 기능은 실제 호스트와 행동별 지원을 확인하며,
백그라운드 입력 실패를 전경 입력이나 전역 마우스·키보드 조작으로 자동 전환하지 않습니다.
로그인된 사용자 프로필 연결과 외부 상태 변경도 정확한 대상 및 행동에 대한 승인이 필요합니다.

패키지의 `scripts/verify_preferences.py`는 선택과 문서 URL, 검증된 문제 해결 메모만 원자적으로
저장하는 보조 도구입니다. 도구 자체는 `provider`를 실행하거나 조작하지 않습니다.
`select --scope app --provider cua-driver`처럼 명시적으로 선택하며, `--session-only`는 파일을
쓰지 않습니다. 잘못된 설정이나 저장 실패는 기존 파일을 보존한 채 보고합니다.
`providerNotes`에는 진단과 해결 뒤 재검증한 재현 가능한 사례만 환경·조건·증상·해결법과 함께
저장합니다. 같은 환경 및 조건의 메모는 교체하고, `provider`당 최대 20건으로 제한합니다.
비밀정보, 개인 화면 내용과 원시 로그는 저장하지 않습니다.
TigerKit 설치 과정에서는 브라우저 제공자를 함께 설치하지 않습니다. 호환 제공자가 없으면
`tk-browser-verify`가 `tk-wizard`로 현재 호스트에 맞는 설정과 재시작 절차를 안내합니다. 새
`Chrome DevTools MCP` 설정에서는 `--headless --isolated`를 권장하며, 외부 `Chrome`에 연결하는
`--browserUrl`과 `9222`는
일반적인 기본값으로 사용하지 않습니다.

## 대화형 사용 경험

공통 원칙은 **대화는 자연스럽게, 상태는 엄격하게**입니다.

- `tk-prep`: 함께 준비하고 승인된 로컬 직접/`Seed`/SDD/인계 경로를 수행합니다.
- `tk-wizard`: 사람이 직접 해야 하는 일을 한 단계씩 자연스럽게 안내합니다.
- `tk-ask-repo`: 질문에 먼저 답하고 필요한 코드 근거를 설명합니다. 공유 요청이나 복합적인 영향·소유권 조사에는 공유용 요약을 덧붙이고, 단순 사실 답변에는 중복 요약을 붙이지 않습니다.
- `tk-pr-respond`: 리뷰 의도를 해석하고 해결 방향과 이유를 합의합니다.
- `tk-pr-sweep`: 여러 PR 중 지금 할 일과 기다릴 일을 최신 분류로 브리핑합니다.

내부 분류, 실행 기반, 경로 상태, 영수증을 기본 사용자 화면에 덤프하지 않습니다.

## PR 흐름

`tk-review`는 구현 중 자동 절차가 아닙니다. 사용자가 명시적으로 호출했을 때 정확한 `BASE..HEAD`, GitHub PR,
또는 현재 `worktree` 하나를 읽기 전용으로 검토하고 `Spec/AC`와 `Quality/Standards`를 독립 판정합니다. `Worktree`는
`HEAD`와 `staged/unstaged/in-scope untracked content`를 메모리에서 고정하며 `drift` 시 판정하지 않습니다. 외부 리뷰
대응은 `tk-pr-respond`가 소유합니다.

```text
tk-pr-open
→ verified branch/HEAD/template/evidence + reviewability preflight
→ single | stacked publication preview
→ current-turn publication approval
→ single: bounded push + PR create/update
   stacked: preserve source branch + reconstruct review layers + lossless tree check + gh-stack submit
→ fresh remote verification

tk-pr-respond
→ fresh exact PR read
→ review/CI 의미 설명 + 필요한 결정만 질문
→ one approval
→ reply-only | code-changing direct-TDD (no Seed) | Ready Seed + direct-TDD/SDD-TDD when durable context is needed
→ exact-range review/verify
→ bounded push/reply/resolve/re-review

tk-pr-rebase
→ fresh exact PR/base/head
→ rebase + conflict handling + verification
→ bounded force-with-lease

tk-pr-sweep --report
→ deterministic fresh triage 읽기 전용 briefing

tk-pr-sweep
→ fresh multi-PR briefing + batch approval
→ exact PR별 Respond/Rebase
→ final fresh triage
```

실행 검증이 필요 없는 일반 주석·문서 수정은 승인된 임시 인덱스 경로로 대응할 수 있습니다.
이 경로는 부모 `checkout`과 실제 인덱스를 보존하고, 정확한 변경 범위 검토와 푸시 뒤 현재 커밋의 CI `build`/`test`
통과를 요구합니다. 동작 변경, 실행 지시문, 로컬 테스트, 여러 커밋 또는 `rebase`가 필요한 작업은 기존 `workspace`
경로를 사용합니다. `tk-pr-sweep`도 `tk-pr-respond` 담당자가 검증한 이 경로를 격리로 인정합니다.

`tk-pr-respond`는 발행 도중 중단된 뒤 재실행하면 GitHub의 최신 상태로 성공한 작업을 확인하고 남은
승인 작업만 수행합니다. 정확한 게시자, 원래 피드백 및 제출된 본문이 일치하는 답글과 이미 해결된
스레드는 중복 처리하지 않습니다. 기존 수정 커밋이 현재 커밋에 포함되고 응답이 여전히 유효한
정상적인 `fast-forward`는 기존 승인을 유지할 수 있지만, 커밋 재작성이나 식별 정보 변경은 중단합니다.
조회 실패와 모호한 근거는 성공 또는 미게시로 추정하지 않습니다.

`tk-pr-open`의 `stacked` 경로는 `raw LOC` 임계값으로 자동 분할하지 않습니다. 이미 검증된 브랜치에 여러 독립적인 `review concern`이 있고 하나의 선형 의존 흐름으로 나눌 수 있을 때만 제안하며, 원본 브랜치는 `rewrite`하지 않고 최상단 `tree`가 원본 `tree`와 정확히 같은지 검증한 뒤 공식 `github/gh-stack`으로 발행합니다.

`tk-pr-open`은 변경을 되돌리는 방법과 영향을 받는 사용자, 호출부, 데이터 및 계약을 검토하여
기존 PR 템플릿의 위험, 복구 또는 마이그레이션 절에 반영합니다. 템플릿이 없을 때에만 필요에 따라
짧은 복구 설명을 추가하며, 코드 되돌리기를 삭제된 데이터나 외부 작업의 복구로 간주하지 않습니다.

`tk-pr-open`은 `manifest` 없이 검수한 이미지가 PR의 주장을 뒷받침하면 발행 전에 업로드 여부를 확인합니다.
민감정보가 있으면 필요한 영역만 자르거나 가리는 선택지를 함께 제시하고, 사용자가 선택한 파생 이미지를
다시 검수합니다. 기존 이미지 선택이 명확하거나 유효한 필수 `manifest`가 있으면 같은 질문을 반복하지 않습니다.
`tk-pr-image`는 생성된 Markdown을 그대로 삽입하고, 표시할 때에는 서명값만 가려 렌더링 매개변수를 보존합니다.
원문 일치, 이미지 바이트와 실제 브라우저 렌더링을 확인하며, 렌더링을 확인할 수 없으면 `Pass`를 보류합니다.

PR 원격 권한은 서로 자동 확장되지 않습니다. `merge`나 다른 발행 권한에는 별도 승인이 필요합니다.
TigerKit은 새 `tag`나 별도 `release`를 발행하지 않으며 기존 태그는 과거 이력으로만 보존합니다.

## 상태와 설정

`.tigerkit/`은 저장소/작업 트리 로컬 임시 공간이며 전역 프로젝트 기억이 아닙니다.
제품 작업의 지속 가능한 맥락이 필요할 때는 `.tigerkit/seed.md` 하나를 사용합니다. 활성 SDD 복구는 현재 `Seed`
식별자와 해시가 일치하는 무시된 `.tigerkit/sdd.md` 하나만 추가로 사용할 수 있습니다.

`audit`, `PR publication/rebase`, `skill learning`의 `owner`별 `singleton Markdown`은 `explicit save`, `multi-turn handoff/recovery`,
복잡한 승인 상태처럼 `durable state`가 실제로 필요할 때만 만듭니다. 같은 턴에 완결되는 단순 작업과 명확한 `no-op`은
대화와 현재 `Git/GitHub` 상태를 사용하며, `run`별 `report` 파일을 쌓지 않습니다.

사용자가 직접 열거나 값을 입력하는 임시파일과 저장소별 실행 산출물도 무시된 `.tigerkit/` 아래에 둡니다.
일반 실행 파일은 `.tigerkit/tmp/<skill>/<run-id>/`, 비밀 입력은
`.tigerkit/secret-input/<skill>-<run-id>/`, 검증 근거는 `.tigerkit/evidence/<skill>/<run-id>/`를 사용합니다.
쓰기 전에는 추적 파일이 없고 `Git`이 `.tigerkit/`을 실제로 무시하는지 `git ls-files`와 `git check-ignore`로
확인합니다. 저장소 `.gitignore`의 파일 존재 여부나 문자열 검색만으로 판단하지 않습니다.
`git check-ignore -q -- .tigerkit/`가 `0`을 반환하면 수정하지 않고, `1`일 때만 아래 설정을 수행합니다.
명령 실행 오류는 규칙 누락으로 취급하지 않고 파일 작성을 중단합니다. 작업 트리의 상위 `.gitignore`·저장소 로컬 `exclude`·사용자 전역 `exclude` 중 어느 규칙이 적용되었는지는
제한하지 않습니다. 실제로 무시되지 않으면 저장소 루트 `.gitignore`를 생성하거나 끝에 `/.tigerkit/`를
추가하고, Git의 무시 판정을 다시 확인한 뒤 저장을 계속합니다. 기존 내용과 줄바꿈은 보존하며, 이미 다른
규칙으로 무시된다면 수정하지 않습니다. 이 설정은 요청된 산출물 작성에 포함되므로 별도 확인을 요구하지
않습니다. 추적 중인 파일을 자동으로 추적 해제하거나 설정만을 위해 스테이징·커밋하지 않습니다. 수정 내용을
간단히 알리고, 경로가 안전하지 않거나 설정을 쓸 수 없으면 해당 파일 저장만 중단합니다. 설명 자료는 `.tigerkit/explanations/`, 학습 자료는 `.tigerkit/study/<topic>/`,
저장을 요청한 조사 자료는 `.tigerkit/research/`를 기본으로 사용합니다. 사용자가 지정한 최종 경로는 존중합니다.
격리 `checkout`·설치 검사·평가 실행도 `.tigerkit/tmp/`를 사용하고, `release`/`eval` 결과는
`.tigerkit/evidence/`에 남깁니다. 외부 도구 자체 캐시와 격리 단위 테스트용 데이터만 도구의 임시 공간을 유지합니다.
원자적 교체에 필요한 임시 파일은 대상과 같은 파일시스템의 실행이 소유하는 임시 파일을 사용할 수 있습니다.
공통 실행 정책은 `scripts/artifact_policy.py`가 소유하며, 파일을 쓰지 않는 스킬에는 쓰기 금지 경계를, 파일을 쓰는 스킬에는 조건부 패키지 로컬 참조를 포함합니다. 설치 검증은 해당 본문과 참조의 누락·변경을 검사합니다.

사용자가 값을 채우는 새 임시 입력 파일은 `input.json`의 일반 JSON 객체로 통일합니다. 예를 들어 단일 토큰은
`{"token": ""}` 템플릿을 미리 만들고, 상대·절대 경로와 입력할 필드를 안내합니다. 비밀 입력에는 기존의
제한된 권한과 즉시 삭제 규칙을 유지합니다. 편집기나 파일 열기
명령은 자동으로 실행하지 않으므로, 사용자는 원하는 시점과 도구를 직접 선택할 수 있습니다. 에이전트는 파일
내용을 노출하지 않는 제한적 감시를 시작하고, 변경된 JSON과 필수 필드가 유효하면 별도 확인 메시지를 요구하지
않고 작업을 이어갑니다. 초기 템플릿이나 미완성 입력은 대기 상태로 유지하며 사용자 값을 덮어쓰지 않습니다.
공통 `Output Notation`과 패키지 로컬 산출물 참조를 동기화하고, 설치·릴리즈 검사에서 누락이나 변경을 검출합니다.

`tk-learn`은 기본적으로 익명 이슈·PRD 초안 하나를 호스트 `scratchpad`에 저장하고, 없으면 실행 소유
OS 임시 폴더를 사용합니다. 저장 후 전체 재읽기와 식별자 검사를 수행하며, 명시적으로 승인한 후보와
대상에만 정본 변경을 적용합니다. 원문 보존 요청에도 비밀값은 제외합니다. 지속 저장이나 인계는
명시한 목적지 또는 `.tigerkit/learn.md`를 사용하며, 일회성 팁과 일반 논의에는 초안을 만들지 않습니다.

평가 어댑터는 실제 호스트 메타데이터에서 확인한 `execution_identity`의 `model`과 관측 가능한 좁은
`config`만 반환합니다. 요청한 모델이나 에이전트 자기보고는 근거가 아닙니다. 평가기는 호스트·프롬프트·
사례·회차·실제 모델과 제공된 설정이 일치할 때만 상대 비교를 수행합니다. 실행 식별 정보가 없거나 다르면
개별 근거를 보존하고 비교는 `Unverifiable`로 둡니다. 설정이 양쪽 모두 누락됐다는 사실은 설정 동등성의
증거가 아니며, 모델을 관측하지 못하는 호스트는 같은 명령으로 실행해도 비교할 수 없습니다.
누락 수치는 `null`로 보존하고 잘못된 수치는 거부합니다. 후보 자체의 안전 위반은 비교 가능성과
별개로 실패 처리하며 TigerKit이 모델을 선택하거나 재실행해서 조건을 맞추지는 않습니다.

Codex 평가 어댑터는 원래 인증 디렉터리 경로를 보존하고 실제 CLI 버전과
`--ignore-user-config` 지원 여부를 확인합니다. 지원하지 않으면 평가를 실행하지 않습니다.
지원하는 CLI에는 해당 옵션을 적용하며 인증 파일을 복사하지 않고 프로젝트 스킬 사본을 유지합니다.
이 옵션과 설치된 파일만으로 전역 지침, 기억, 훅, 플러그인의 배제 및 프로젝트 스킬 로딩을
입증할 수는 없습니다. 현재 기본 어댑터는 이 한계를 `execution_provenance`에 기록하여
Codex 상대 비교를 `Unverifiable`로 처리합니다. 개별 실행 결과는 관찰 자료로 보존할 수 있으나
스킬 개선의 증거로 해석하지 않습니다. 비교하려면 독립적인 실행 근거로 설정 격리와 스킬 로딩을
입증하고 버전, 실제 모델 및 관측 설정을 맞춰야 합니다.

`tk-pr-sweep`의 장기 저장소 범위와 선택적인 댓글별 도구 작성 마커는 다음 사용자 설정을 사용할 수 있습니다.

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

`toolAuthoredCommentMarkers`에는 HTML 주석 접두어만 둡니다. 협업자 개인 계정으로 게시된 자동 리뷰도 해당
댓글만 도구 작성으로 판정해 답글 컨펌에 사용하며, 재리뷰 대상은 계속 계정 상태로 판정합니다.

모델 매핑, 선택자, 추론 강도, 작업자 경로, `fan-out` 선호, 함정 모음은 TigerKit 사용자 설정으로 만들지 않습니다.

## 학습과 반복 발견

별도 `tk-evolve`, `pitfalls.md`, `troubleshooting.md`를 만들지 않습니다.

```text
Seed 계약을 바꾸는 새 evidence
→ tk-prep revision + user reapproval

repository에서 반복될 사실
→ test/type/schema/policy/code invariant 같은 repo-native owner 개선 후보

TigerKit skill 자체 반복 실패
→ tk-skill-diagnose / tk-learn

개인 cross-repo memory
→ 외부 memory tool
```

## 평가 정본

```text
evals/skills/<skill>/triggers.json
evals/skills/<skill>/evals.json
evals/catalog-routing.json
evals/release-critical.json
```

검증기는 `skills/tk-*`를 자동 발견합니다.

## 로컬 검증

```bash
python3 scripts/sync_execution_protocol.py --check
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
python3 scripts/check_docs.py
node --check skills/tk-pr-sweep/scripts/triage.mjs
node --test skills/tk-pr-sweep/scripts/triage.test.mjs
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

호환성이 깨지는 스킬/평가 계약을 포함한 릴리스 검증:

```bash
python3 scripts/run_seed_release_gate.py \
  --baseline "$(git rev-parse origin/main)" \
  --candidate HEAD
```

모든 검증은 로컬 전용입니다.

변경 이력은 `commit` 기록으로 확인하며 별도 `CHANGELOG.md`, 신규 `tag`, 별도 `release`를 유지하지 않습니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 참고하세요.

세션을 오가다 맥락을 놓치면 `/tk-adhd` 또는 “여기 어디까지 했어?”로 현재 작업을 확인할 수 있습니다.
목표·완료·진행·다음 행동·사용자가 할 일만 짧게 보여줍니다. 진행 중인 작업의 기존 승인이 있어도 안내 뒤 턴을 끝내고 재개 지시를 기다립니다.
다른 세션이나 열린 PR을 찾아보거나 현황 파일을 만들지 않습니다.

기존 글이 이해하기 어렵거나 표현이 어색하다면 `/tk-rewrite`로 재작성합니다.
기본적으로 맥락과 설명 구조를 정리한 뒤 표현을 다듬으며, 중간 결과 없이 최종 본문 하나만 반환합니다.
작성 대화를 모르는 독자에게 필요한 맥락을 본문에 담고, 주장에 영향을 주는 가능성이나 의무 및 권고의 강도를 보존합니다.
문체를 다듬을 때 명시된 순위, 비교 범위와 동시성을 보존하며, 실제 의미 관계가 없는 공허한 강조는 정리합니다.
표현 정제에서는 수정 근거가 있는 부분만 바꾸며, 문제가 없으면 원문을 그대로 반환합니다. 독자의 이해에 필요한 구조 변경은 유지합니다.
“말투만” 또는 “구조만”이라고 요청하면 해당 범위만 처리하며, 검토만 요청하면 전체 글을 재작성하지 않습니다. 파일 수정은 대상을 지정해 요청했을 때 수행합니다.

개념을 배경지식부터 시각적으로 이해하려면 `/tk-explain`으로 HTML 설명 자료를 만듭니다.
해당 분야를 모르는 성인을 기본 독자로 보고, 필요한 선행 개념을 소개한 뒤 실제 구성 요소와 작동 방식을 그립니다.
비유와 장면·단어 수를 의무화하지 않으며, 일반 텍스트 질문에는 HTML을 만들지 않습니다.

코드 변경을 이해하려면 `/tk-explain-diff`, 낯선 주제를 조사해서 배우려면 `/tk-study`를 사용합니다.
`tk-explain-diff`는 비교 근거와 변경 전후 흐름을 담은 HTML을 `.tigerkit/explanations/<target-slug>.html`에 만듭니다.
`tk-study`는 사전 조사, 필요한 선수지식 질문, 범위를 반영한 재조사와 커리큘럼 구성을 거쳐
`.tigerkit/study/<topic>/index.html`을 만듭니다. 질문으로 확인한 학습자 프로필과 커리큘럼·출처·챕터 원고도
같은 주제 폴더에 보관하며, 기존 지식이나 숙달 여부를 추측하지 않습니다.
지정된 유한 자료 목록이 있으면 `sources.md`에 각 자료의 반영, 부분 확인, 접근 실패 또는 생략 사유를 남기고, 미확인 범위를 최종 결과에 밝힙니다. 일반 주제 조사에는 검색 결과별 추적을 추가하지 않습니다.
두 스킬 모두 오프라인 HTML을 기본으로 하며, 명시한 Markdown 형식과 최종 경로를 존중합니다.
세 설명·학습 스킬은 `tk-explain`의 HTML 참조 문서를 각 패키지에 동기화하여 사용합니다.

글쓰기, 설명, 학습 스킬은 같은 `references/clear-writing.md` 기준을 사용합니다. 정본은 `tk-rewrite`에 두고
`tk-explain`, `tk-explain-diff`, `tk-study`에 동일한 사본을 동기화하며, 각 패키지에 참조 문서와 원본 라이선스를 포함합니다.
의미와 필수 문장 성분을 보존하고, 일반 설명문의 엠대시와 절 기호는 빈도와 무관하게 교정합니다.
평가의 강도와 확신의 강도를 각각 보존하며, 효과가 있다는 확신을 효과의 크기로 바꾸지 않습니다.
실제 양보나 대조 관계는 연결어만 보고 삭제하지 않고 두 절의 의미를 확인합니다.
한국어 산문의 가운뎃점 명사 나열과 근거 없는 중요도 및 규모 수식어도 한 번만 나와도 교정합니다.
원문에 있는 예시와 근거로 대상을 구체화하고, 부서나 직책이 확인되면 모호한 상위어 대신 명시합니다.
없는 정보는 추측하지 않으며, 근거가 있는 중요도 주장과 코드, 인용, 공식 명칭, 검증된 UI 라벨은 보존합니다.
그 밖의 자연스러운 단발 표현은 유지하고 반복되거나 밀집된 표현만 선택적으로 정리합니다.
외부 `fluent-korean` 설치 없이도 사용할 수 있으며, `tigeryoo-ai-setup`의 기존 공용 지침 설치는 별도로 유지됩니다.
세션 현황을 짧게 확인하고 멈추는 용도는 계속 `tk-adhd`가 담당합니다.
이전 이름으로 설치한 사용자는 [마이그레이션 안내](MIGRATION.md)에 따라 새 이름을 설치하고 남은 구버전을 제거하세요.

### 문서 정합성 검사 범위

릴리즈 게이트는 기존 Markdown 상대 링크, README 스킬 목록, 공유 참조 동기화에 더해
표의 열 수, README 호출 방식과 실제 스킬 메타데이터, 설치 스킬의 산출물 정책 일치를 검사합니다.
`python3 scripts/check_docs.py`로 따로 실행할 수 있습니다. 자연어 설명의 의미까지 자동으로 보장하지는
않으므로 공개 동작을 바꾸면 해당 문서를 함께 갱신하고 독립 검수에서 실제 계약과 대조합니다.

### 기획과 마일스톤 수립

`/tk-roadmap` 또는 `$tk-roadmap`을 인자 없이 호출하면 인터뷰를 시작합니다. 대화에 관련 맥락이 있으면
이미 답한 내용을 재질문하지 않고 현재 독립적으로 답할 수 있는 판단 주제를 함께 묻습니다. 기술·데이터뿐 아니라 인력·예산·권한·협업·운영
제약을 함께 고려하고, 대안과 우선순위를 논의한 뒤 목표·범위·완료 근거·의존성을 갖춘 마일스톤을 정리합니다.
미정과 마감 없음도 유효한 답변이며, 조사 후 보류하거나 추진하지 않기로 결정하는 단계도 인정합니다.
확장 마일스톤과 상시 운영을 구분하고, 계획 정리 후 종료합니다. 구현이나 이슈 생성으로 자동 진입하지 않습니다.
저장을 요청하면 `.tigerkit/roadmap.md`를 사용하며 명시한 최종 경로를 존중합니다. 저장소가 없어도 대화는
진행할 수 있고, 파일 저장 조건을 충족하지 못하면 결과를 대화로 제공합니다.

기존 결정의 전면 점검은 `tk-grill`, 외부 접근법 조사는 `tk-research`, 선택한 구현 작업의 준비는 `tk-prep`이
담당합니다. `tk-roadmap`은 개발 작업의 필수 선행 단계가 아닙니다.


### 연구와 탐색: 지속 연구

`/tk-autoresearch` 또는 `$tk-autoresearch`는 연구 목표는 있지만 필요한 질문·가설·접근 방향이 결과에 따라 계속 바뀌는 과제를 담당합니다. 사용자는 연구 목표만 짧게 입력하면 되고, 스킬이 필요한 사실을 먼저 조사한 뒤 실제 사용자 소유 결정만 질문 형식으로 묻습니다. 작업 공간 권한·저장 규칙·실험 반복 방식·종료 조건을 장문으로 미리 작성할 필요가 없습니다.

연구 진행률은 검색 횟수가 아니라 상태 변화로 판단합니다. 연구 결과를 닫거나 방향을 지지·반증·보류하고, 새 근거가 기존 전제를 깨면 `DEEPEN`·`BROADEN`·`PIVOT`·`CONCLUDE` 중 다음 방향을 다시 정합니다. 같은 자료를 반복해도 결론이 바뀔 가능성이 낮으면 `NO-ACTION` 또는 `NO-DELTA`로 끝낼 수 있습니다. 명시적인 `tk-autoresearch` 호출은 해당 저장소의 가역적인 로컬 연구 변경을 기본 허용하므로, 필요하면 별도 `research/<slug>` 작업 트리를 자동으로 만들고 개념 검증·파서·검증용 입력·벤치마크·재현 도구·테스트·로컬 커밋까지 중간 승인 없이 수행할 수 있습니다. 사용자 미커밋 변경은 건드리지 않으며, `push`·PR·병합·릴리스·배포, 운영/보호 데이터, 비밀정보, 유료·상태 변경 외부 서비스, 파괴적·비가역 작업은 별도 권한으로 남깁니다.

기본 저장 정책은 `hybrid`입니다. 연구 식별이 정해지면 하나의 전용 연구 작업 트리를 연구 홈으로 잡고, 그 홈의 `.tigerkit/autoresearch/`에 실행 상태와 간단한 `config.json`을 둡니다. 현재 요약·연구 결과·체크포인트 연구 일지·실험 기록은 `docs/autoresearch/<slug>/`에 추적하며 체크포인트마다 같은 연구 묶음만 로컬 커밋합니다. 설정은 `mode`, `trackedRoot`, `commitOnCheckpoint`만 유지합니다. `local`은 전부 무시되는 로컬 상태, `hybrid`는 연구 지식만 추적, `tracked`는 여기에 정제한 설정·상태 스냅샷을 더합니다.

질문이 정해진 일회성 외부 비교와 선행 사례 조사는 `tk-research`, 선택한 방향의 실행 마일스톤은 `tk-roadmap`, 제품 구현은 `tk-prep`이 담당합니다. 일반적인 자동연구는 연구 식별이 정해지면 `.tigerkit/autoresearch/state.md`를 재개 정본으로 유지합니다. 다음 세션이나 다음날에는 `$tk-autoresearch --resume`만으로 현재 작업 트리의 상태를 복원해 기존 현재 탐색 가능 항목부터 이어갑니다. 현재 작업 트리에 상태가 없으면 같은 저장소의 연결된 작업 트리를 확인하고, 유효한 연구 상태가 하나뿐이면 그 작업 트리에서 자동으로 재개합니다. 여러 상태가 있거나 상태가 전혀 없을 때만 필요한 선택을 한 번 묻습니다. 한 번의 호출은 무한 실행하지 않고 의미 있는 연구 묶음이 자연스럽게 닫히면 `CHECKPOINT`로 상태와 시행착오를 보존하고 종료합니다. 새 근거가 있는 `CONCLUDE`나 `BLOCKED`도 같은 기록 절차를 거칩니다. Git에 남는 연구 문서에는 비밀정보·직접 식별자·원시 운영 로그를 넣지 않고 결정에 필요한 정제된 근거만 남깁니다.

`tk-study`의 실행 가능한 코딩 연습문제는 이미 사용 가능한 안전한 실행 환경에서 기준 해답의 통과와
학습 목표에 관련된 그럴듯한 오답의 실패를 확인합니다. 오답도 통과하면 검사나 문제를 보완하고
두 결과를 다시 확인합니다. 개념형 질문에는 이 절차를 강제하지 않으며, 실행 환경이 없으면 자료를
계속 만들되 해당 연습문제를 실행 검증하지 못했다고 명시합니다.
