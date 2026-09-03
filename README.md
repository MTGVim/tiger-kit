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
| `tk-audit` | `user` | 읽기 전용 저장소 감사와 `AUD-*` 발견 사항 |
| `tk-ask-repo` | `user` | 저장소 동작·값·영향·귀속을 근거와 함께 설명 |
| `tk-review` | `user` | 정확한 커밋 범위/`PR`/`current worktree`의 읽기 전용 `Spec/AC` + `Quality/Standards` 검토 |
| `tk-pr-open` | `hybrid` | 검증된 `commit`의 `single | stacked` 발행 계획 + 제한된 `push`/PR 생성·갱신 |
| `tk-pr-respond` | `hybrid` | 한 PR의 리뷰/지원 CI 분석·수정·검증·`reply`/`resolve` |
| `tk-pr-rebase` | `hybrid` | 정확한 PR의 최신 `base` `rebase`와 제한된 `force-with-lease` |
| `tk-pr-sweep` | `user` | 여러 PR의 결정론적 분류와 승인된 유지보수 묶음 |
| `tk-github-image-upload-to-pr` | `user` | 기존 PR에 로컬 근거 이미지 올리기 |
| `tk-prototype` | `hybrid` | 폐기 가능한 UI/로직 비교물 |
| `tk-eli5` | `hybrid` | 큰 그림과 적은 글의 초보자용 `self-contained HTML` 설명 자료 |
| `tk-browser-verify` | `hybrid` | 화면에 보이는 AC의 `headless` 실행 검증 |
| `tk-skill-diagnose` | `hybrid` | `Agent Skill` 사고 재현·격리와 `learn-ready` 인계 |
| `tk-learn` | `hybrid` | 재사용 가능한 스킬의 생성/개선/병합 작성자 |
| `tk-domain` | `hybrid` | 저장소 고유 용어의 `canonical vocabulary`와 `sparse durable decision/ADR context` 작성·정제 |
| `tk-grooming` | `hybrid` | 기존 스킬·지속 `rule`·`auto memory`의 중복·충돌·낡은 지침 감사 |
| `tk-handoff` | `hybrid` | 진행 중 작업의 재개용 상태 사진 |
| `tk-merge-conflict` | `hybrid` | 활성 Git 충돌 의도 복원 |
| `tk-wizard` | `hybrid` | 사람이 직접 해야 하는 설정·인증·이관 절차 안내 |

`user`는 명시 호출 전용이고, `hybrid`는 해당 작업 의도가 명확할 때 자동 진입할 수 있습니다.

`tk-audit`은 저장소·실행 근거로 동일한 인과 원인, 수정 경계, 실패 유형이 확인된 여러 증상을 하나의
원인 `finding`으로 묶고 영향을 받은 표면을 연결합니다. 원인이나 되돌리기·위험·검증 경계가 독립적이면
별도 `finding`으로 유지합니다.

## `tk-prep`, 직접 실행, `Seed`, SDD

`tk-prep`은 고정 양식 위저드가 아닙니다.
내부적으로는 명확도와 엔지니어링 준비도를 엄격하게 평가하지만,
사용자에게는 현재 이해, 추천, 이유를 자연스러운 대화로 설명합니다.

사용자에게 직접 묻는 것은 제품/범위 같은 사용자 소유 결정, 위험하거나 비가역적인 결정,
충분히 개선한 뒤에도 남는 엔지니어링 예외 승인뿐입니다.

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
목표/배경, 현재 상태, 범위, 사용자 결정, 구현 안내, AC, 검증, 브라우저 계획, 엔지니어링 예외를 구현자가 원 대화 없이 이해할 수 있게 담습니다.

`worker`/`wave` 진행 상태, 제공자 모델 선택자, 추론 강도, 영수증, 비밀 값은 `Seed`에 저장하지 않습니다.

코드 변경 직접/SDD 경로는 행동 우선 `RED → GREEN → REFACTOR`를 기본으로 하며 현실적인 변이를 잡는
테스트를 남깁니다. SDD는 `tk-prep`과 `tk-pr-respond`가 공유하는 패키지 로컬 절차로 정확한 `Unit` 범위 검토와
5회 수정 차단기를 사용합니다. 브라우저 증거는 자동 회귀 보호를 대체하지 않습니다.

직접 실행에서 여러 `commit`이 필요하면 파일 종류나 계층이 아니라 독립적으로 이해·검증·되돌릴 수 있는
작업 단위로 나눕니다. 동작과 이를 입증하는 테스트 및 반드시 바뀌어야 하는 사실 문서는 가능한 한 같은
`commit`에 둡니다.

## 브라우저 검증

`browser-visible` AC가 있으면 `tk-prep`에서 대상, `headless`, 인증, `viewport`, 개발 서버, `criterion`별 `runtime` 근거와 통과 조건을 정합니다. `Visual/visible-state` 근거는 검증 대상이 실제 담긴 `screenshot`을 사용합니다.
비밀번호, `token`, OTP, `cookie`, `session` 비밀 값은 `Seed`에 저장하지 않고 실행 시 일시 입력으로만 다룹니다.

개발 서버가 필요하면 시작·준비 확인·정리는 `tk-browser-verify`가 소유합니다.

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
→ reply-only | code-changing Ready Seed + direct-TDD/SDD-TDD
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
제한하지 않습니다. 실제로 무시되지 않으면 `.gitignore`를 자동으로 수정하거나 접근하기 어려운 외부 임시
경로로 전환하지 않습니다. 격리 `checkout`, `release`/`eval` 출력처럼 사용자가 직접 접근하지 않는 도구 내부
파일은 운영체제 임시 경로를 사용할 수 있습니다.

비밀 입력 파일은 빈 상태로 생성하고 상대·절대 경로와 안전한 입력 명령만 안내합니다. 편집기나 파일 열기
명령은 자동으로 실행하지 않으므로, 사용자는 원하는 시점과 도구를 직접 선택할 수 있습니다. 에이전트는 파일
내용을 노출하지 않는 제한적 감시를 시작하고, 값이 입력되면 별도 확인 메시지를 요구하지 않고 작업을 이어갑니다.

`tk-pr-sweep`의 장기 저장소 범위는 다음 사용자 설정을 사용할 수 있습니다.

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

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
skills/<skill>/evals/triggers.json
skills/<skill>/evals/evals.json
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
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```

모든 검증은 로컬 전용입니다.

변경 이력은 `commit` 기록으로 확인하며 별도 `CHANGELOG.md`, 신규 `tag`, 별도 `release`를 유지하지 않습니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 참고하세요.
