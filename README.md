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

## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | 적응형 준비 + 승인된 직접/Ready `Seed`/SDD/인계 로컬 실행 |
| `tk-grill` | `user` | 아이디어·계획·결정의 빠짐없는 점검과 확인된 `shared understanding` |
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
| `tk-study` | `hybrid` | 낯선 주제를 조사하고 배경·동작·응용 문제 순서로 가르치는 학습 자료 |
| `tk-browser-verify` | `hybrid` | 화면에 보이는 AC의 `headless` 실행 검증과 읽기 전용 라벨·진입 경로 조사 |
| `tk-skill-diagnose` | `hybrid` | `Agent Skill` 사고 재현·격리와 `learn-ready` 인계, 승인된 수정은 `tk-learn`으로 연속 진행 |
| `tk-learn` | `hybrid` | 재사용 가능한 스킬의 생성/개선/병합 작성자. 기존 검사 도구로 막을 수 있는 문제는 해당 도구의 최소 확장을 우선 제안 |
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

`worker`/`wave` 진행 상태, 제공자 모델 선택자, 추론 강도, 영수증, 비밀 값은 `Seed`에 저장하지 않습니다.

코드 변경 직접/SDD 경로는 행동 우선 `RED → GREEN → REFACTOR`를 기본으로 하며 현실적인 변이를 잡는
테스트를 남깁니다. 순수 동작 보존 리팩터링은 수정 전 `GREEN`을 확보하고 구조를 변경한 뒤 같은 동작이
유지되는지 확인합니다. 실패를 만들기 위해 정상 코드를 깨뜨리지 않습니다. SDD는 `tk-prep`과 `tk-pr-respond`가 공유하는 패키지 로컬 절차로 정확한 `Unit` 범위 검토와
5회 수정 차단기를 사용합니다. 브라우저 증거는 자동 회귀 보호를 대체하지 않습니다.

열린 PR은 자동으로 탐색하지 않습니다. 사용자가 비교를 요청하거나 작업 근거로 지정한 PR만 필요한 범위에서 읽습니다.

최초 요청이나 앞선 대화에서 승인한 범위는 하위 스킬에도 이어집니다. 기준 화면 캡처, 구현, 검증, 리뷰, 로컬 커밋 사이에
다시 진행 여부를 묻지 않습니다. 원격 발행까지 명시적으로 승인했다면 해당 담당자가 이어서 수행하고, 새 범위나 실제 사용자 결정이 필요할 때만 질문합니다.

직접 실행의 최종 리뷰는 실제 변경과 검증 근거로 저위험임을 확인한 경우 독립 리뷰어 한 명이 수행합니다.
보안·권한, 저장 데이터, 공개 계약 호환성, 여러 경계에 걸친 상태·생명주기, 복잡하거나 불확실한 변경은
두 명이 수행합니다. SDD 전체 변경과 명시적인 `tk-review`는 두 명을 유지하며, 모든 리뷰어는 두 판정 축과
두 검토 절차를 모두 수행합니다.

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
TigerKit 설치 과정에서는 브라우저 제공자를 함께 설치하지 않습니다. 호환 제공자가 없으면
`tk-browser-verify`가 `tk-wizard`로 현재 호스트에 맞는 설정과 재시작 절차를 안내합니다. 새
`Chrome DevTools MCP` 설정에서는 `--headless --isolated`를 권장하며, 외부 `Chrome`에 연결하는
`--browserUrl`과 `9222`는
일반적인 기본값으로 사용하지 않습니다.

## 대화형 사용 경험

공통 원칙은 **대화는 자연스럽게, 상태는 엄격하게**입니다.

- `tk-prep`: 함께 준비하고 승인된 로컬 직접/`Seed`/SDD/인계 경로를 수행합니다.
- `tk-wizard`: 사람이 직접 해야 하는 일을 한 단계씩 자연스럽게 안내합니다.
- `tk-ask-repo`: 질문에 먼저 답하고 코드 흐름을 설명한 뒤 보통 `3~10`줄의 공유용 요약을 제공합니다. 검증된 중요한 경계는 줄 수 때문에 생략하지 않습니다.
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

`tk-pr-open`의 `stacked` 경로는 `raw LOC` 임계값으로 자동 분할하지 않습니다. 이미 검증된 브랜치에 여러 독립적인 `review concern`이 있고 하나의 선형 의존 흐름으로 나눌 수 있을 때만 제안하며, 원본 브랜치는 `rewrite`하지 않고 최상단 `tree`가 원본 `tree`와 정확히 같은지 검증한 뒤 공식 `github/gh-stack`으로 발행합니다.

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
확인합니다. 작업 트리의 상위 `.gitignore`·저장소 로컬 `exclude`·사용자 전역 `exclude` 중 어느 규칙이 적용되었는지는
제한하지 않습니다. 실제로 무시되지 않으면 저장소 루트 `.gitignore`를 생성하거나 끝에 `/.tigerkit/`를
추가하고, Git의 무시 판정을 다시 확인한 뒤 저장을 계속합니다. 기존 내용과 줄바꿈은 보존하며, 이미 다른
규칙으로 무시된다면 수정하지 않습니다. 이 설정은 요청된 산출물 작성에 포함되므로 별도 확인을 요구하지
않습니다. 추적 중인 파일을 자동으로 추적 해제하거나 설정만을 위해 스테이징·커밋하지 않습니다. 수정 내용을
간단히 알리고, 경로가 안전하지 않거나 설정을 쓸 수 없으면 해당 파일 저장만 중단합니다. 설명 자료는 `.tigerkit/explanations/`, 학습 자료는 `.tigerkit/study/<topic>/`,
저장을 요청한 조사 자료는 `.tigerkit/research/`를 기본으로 사용합니다. 사용자가 지정한 최종 경로는 존중합니다.
격리 `checkout`·설치 검사·평가 실행도 `.tigerkit/tmp/`를 사용하고, `release`/`eval` 결과는
`.tigerkit/evidence/`에 남깁니다. 외부 도구 자체 캐시와 격리 단위 테스트용 데이터만 도구의 임시 공간을 유지합니다.
원자적 교체에 필요한 임시 파일은 대상과 같은 파일시스템의 실행이 소유하는 임시 파일을 사용할 수 있습니다.
공통 실행 정책은 `scripts/artifact_policy.py`가 소유하며, 각 설치 스킬에 동일한 계약을 포함합니다.

비밀 입력 파일은 빈 상태로 생성하고 상대·절대 경로와 안전한 입력 명령만 안내합니다. 편집기나 파일 열기
명령은 자동으로 실행하지 않으므로, 사용자는 원하는 시점과 도구를 직접 선택할 수 있습니다. 에이전트는 파일
내용을 노출하지 않는 제한적 감시를 시작하고, 값이 입력되면 별도 확인 메시지를 요구하지 않고 작업을 이어갑니다.

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
표현 정제에서는 수정 근거가 있는 부분만 바꾸며, 문제가 없으면 원문을 그대로 반환합니다. 독자의 이해에 필요한 구조 변경은 유지합니다.
“말투만” 또는 “구조만”이라고 요청하면 해당 범위만 처리하며, 검토만 요청하면 전체 글을 재작성하지 않습니다. 파일 수정은 대상을 지정해 요청했을 때 수행합니다.

개념을 배경지식부터 시각적으로 이해하려면 `/tk-explain`으로 HTML 설명 자료를 만듭니다.
해당 분야를 모르는 성인을 기본 독자로 보고, 필요한 선행 개념을 소개한 뒤 실제 구성 요소와 작동 방식을 그립니다.
비유와 장면·단어 수를 의무화하지 않으며, 일반 텍스트 질문에는 HTML을 만들지 않습니다.

코드 변경을 이해하려면 `/tk-explain-diff`, 낯선 주제를 조사해서 배우려면 `/tk-study`를 사용합니다.
두 신규 스킬은 기본적으로 Markdown 자료 하나를 만들며, HTML 등 명시한 형식과 최종 경로를 존중합니다.

글쓰기와 설명·학습 스킬은 같은 `references/clear-writing.md` 기준을 사용합니다. 정본은 `tk-rewrite`에 두고
`tk-explain`, `tk-explain-diff`, `tk-study`에 동일한 사본을 동기화하며, 각 패키지에 참조 문서와 원본 라이선스를 포함합니다.
의미와 필수 문장 성분을 보존하고, 일반 설명문의 엠대시와 절 기호은 빈도와 무관하게 교정합니다.
코드·인용 등은 보존하며, 자연스러운 단발 표현은 유지하고 반복·밀집된 표현만 선택적으로 정리합니다.
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
이미 답한 내용을 재질문하지 않고 다음 판단 주제로 넘어갑니다. 기술·데이터뿐 아니라 인력·예산·권한·협업·운영
제약을 함께 고려하고, 대안과 우선순위를 논의한 뒤 목표·범위·완료 근거·의존성을 갖춘 마일스톤을 정리합니다.
미정과 마감 없음도 유효한 답변이며, 조사 후 보류하거나 추진하지 않기로 결정하는 단계도 인정합니다.
확장 마일스톤과 상시 운영을 구분하고, 계획 정리 후 종료합니다. 구현이나 이슈 생성으로 자동 진입하지 않습니다.
저장을 요청하면 `.tigerkit/roadmap.md`를 사용하며 명시한 최종 경로를 존중합니다. 저장소가 없어도 대화는
진행할 수 있고, 파일 저장 조건을 충족하지 못하면 결과를 대화로 제공합니다.

기존 결정의 전면 점검은 `tk-grill`, 외부 접근법 조사는 `tk-research`, 선택한 구현 작업의 준비는 `tk-prep`이
담당합니다. `tk-roadmap`은 개발 작업의 필수 선행 단계가 아닙니다.
