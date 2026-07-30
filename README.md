# TigerKit

<p align="center">
  <img src="assets/tigerkit-cover.png" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit 21.0.7는 Claude Code, Codex, Hermes Agent용 소규모 엔지니어링 Agent Skills
모음입니다. 중앙 workflow runtime 없이 15개 self-contained skill을
`npx skills`로 배포합니다. 하나의 명시적 `tk-drive <source>`가 내부
direct procedure graph에서 `tk-grill-me`, Ready spec, 조건부 ticket,
implementation·aggregate verification·reflection을 순서대로 선택합니다.
최신 immutable release는 `v21.0.7`이며,
현재 `main`에는 다음 release를 위한 skill 변경이 포함될 수 있습니다.

현재 `main`의 `tk-drive`는 phase receipt나 mutable prep lifecycle로
제어를 되돌리지 않습니다. 각 procedure의 native 결과를 다음 applicable
node에 직접 넘기며, `.tigerkit/prep.md`는 task·repository·graph·verification
profile·조건부 browser hint·spec/ticket reference만 담는 compact preflight
snapshot입니다. Resume은 저장된 status/cursor가 아니라 현재 artifact, Git,
test, browser evidence에서 다음 node를 다시 선택합니다.

Agent Skill의 same-turn continuation은 prompt-directed이며 확률적입니다.
TigerKit은 durable scheduler, event replay, hard cross-turn continuation을
보장하는 workflow engine이 아닙니다. 그런 보장이 필요한 작업에는 별도
runtime product가 필요합니다.

`tk-adhd`를 명시적으로 선택하면 그 응답 하나에만 action-first, bounded
steps, current-state restatement를 적용합니다. 다음 응답에는 승계되지
않으며 같은 출력을 원하면 다시 명시적으로 호출해야 합니다. 다른 skill,
ADHD 언급, formatting 요청은 이 utility를 암묵적으로 호출하지 않습니다.

`tk-adhd` 이외의 canonical skill은 최신 명시 언어 지시를 우선하는
response-language hard gate와 terminal-summary boundary를 자체 포함합니다.
최종 사용자 영역은 해당 skill의 canonical 첫 heading 또는 result sentence로
바로 시작하며 standalone separator, 반복 `Outcome:`, 하단 receipt metadata를
렌더링하지 않습니다. Active drive의 성공 procedure 사이에는 terminal
response를 만들지 않습니다. 검증된 성공은 `tk-drive finalization`, terminal
non-success는 `tk-drive non-success finalization`만 최종 사용자 응답을
소유합니다.

`tk-drive` Preparing은 product mutation 전에 material implementation 및
verification strategy를 점검합니다. Browser evidence는
`required | optional | N/A`로 분류하며, 필요할 때만 target environment,
계정 역할·tenant, opaque profile hint, 인증 기대값과 safe interaction을
명확화합니다. 정확한 식별정보는 저장하지 않고 cold-start 재요청 marker만
Ready spec에 남깁니다.

## 설치

모든 지원 host에 전체 skill을 전역 설치합니다.

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

선택한 skill만 설치합니다.

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill tk-implement \
  --skill tk-browser-verify
```

변경되지 않는 `v21.0.7` snapshot:

```bash
npx skills add "MTGVim/tiger-kit#v21.0.7" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code와 Hermes Agent에서는 `/tk-implement` 같은 slash command로 표시됩니다. Codex에서는 `$tk-implement` 또는 skill picker를 사용합니다.

## Skill 목록

- **`[user]` user-invoked 3개**: 사용자가 명시적으로 선택하며 implicit invocation이 차단됩니다.
- **`[user/auto]` hybrid 12개**: 사용자 선택과 description의 좁은 positive trigger를 모두 지원합니다.
- model-only skill은 없습니다.

| Skill | 호출 | 목적 |
| --- | --- | --- |
| `tk-ask-repo` | user | 외부에서 들어온 repository 질문을 분류하고 원점·소비처·영향·책임을 `path:line` 근거로 조사합니다. |
| `tk-drive` | user | 명시 source를 내부 Preparing에서 Ready로 만들고 같은 run의 Executing에서 unit별 commit, aggregate verification, reflection까지 진행합니다. |
| `tk-adhd` | user | 명시 호출한 응답 하나를 action-first 형태로 만드는 단발 출력 utility입니다. |
| `tk-grill-me` | hybrid | 명시 선택 또는 active-drive decision edge에서 사실을 조사하고 중요한 결정을 한 번에 한 질문씩 닫습니다. |
| `tk-to-spec` | hybrid | 독립 요청 또는 active-drive graph에서 Ready spec을 작성·검증합니다. |
| `tk-to-tickets` | hybrid | 독립 요청 또는 active-drive graph에서 source를 수직 ticket으로 나눕니다. |
| `tk-implement` | hybrid | 명시 선택 또는 drive graph에서 unit 하나를 테스트·review하고 commit 하나로 만듭니다. |
| `tk-prototype` | hybrid | 폐기 가능한 UI 또는 logic 비교 검증물을 실제 실행합니다. |
| `tk-reflect` | hybrid | 명확한 회고 요청에서 재사용 가능한 rule/skill 후보를 report-only로 분류합니다. |
| `tk-skill-diagnose` | hybrid | 관찰되거나 측정된 Agent Skill 이상을 fresh execution으로 재현하고 failure plane·효율 원인을 격리합니다. |
| `tk-learn` | hybrid | 명확한 skill 작성 요청을 draft/checkpoint까지 진행하고 승인 후에만 씁니다. |
| `tk-grooming` | hybrid | 기존 rule/skill을 기본 report-only로 감사합니다. |
| `tk-handoff` | hybrid | 명확한 handoff artifact 작성 또는 resume 요청을 처리합니다. |
| `tk-browser-verify` | hybrid | 실제 browser에서 UI, network, final state를 검증합니다. |
| `tk-merge-conflict` | hybrid | 진행 중인 Git conflict를 의도 기반으로 해결하고 operation을 완료합니다. |

## 사용 시나리오

TigerKit은 반드시 따라야 하는 pipeline이 아닙니다. 일반 후속 질문이나 작은 피드백은 현재 대화에서 계속 처리하세요. 명확한 절차, artifact, 독립 검증 또는 commit 경계가 필요할 때 skill을 선택하세요.

### 아이디어를 검토하고 구현하기

```text
tk-grill-me
→ 필요하면 tk-to-spec
→ 필요하면 tk-to-tickets
→ tk-implement
```

Standalone decision discovery에는 `tk-grill-me`를 명시적으로 선택할 수
있습니다. 결정이 끝났거나 변경이 작다면 `tk-implement`를 명시적으로 선택해
바로 사용할 수 있습니다. 일반 구현 요청은 이 hybrid skill을 자동 호출하지
않습니다.

전체 흐름은 `tk-drive` 하나를 source와 함께 명시 선택합니다. Claude
Code·Hermes Agent에서는 `/tk-drive <source>`, Codex에서는
`$tk-drive <source>`를 사용합니다. Preparing은 unresolved user-owned
decision만 `tk-grill-me`에 위임하고 Ready spec과 필요한 vertical ticket
ledger를 검증한 뒤 compact preflight를 기록합니다. 같은 active turn에서
현재 evidence가 가리키는 첫 implementation unit으로 직접 진행합니다.

```text
<host-native explicit tk-drive> <source>
→ 필요할 때만 tk-grill-me: confirmed decision state
→ tk-to-spec: Ready spec
→ 필요할 때만 tk-to-tickets: vertical ticket ledger
→ .tigerkit/prep.md: compact secret-free preflight
→ ticket마다 tk-implement: test + review + verified commit 하나
→ tk-drive: aggregate traceability + broad verification 한 번
→ tk-reflect: 조건부 classification + exact ignored-rule safety gate
→ tk-drive finalization: 성공 terminal response 하나

terminal non-success + alternate edge 소진
→ product mutation freeze
→ tk-drive non-success finalization: scoped terminal response 하나
```

Preflight는 task scope, repository/worktree/branch/baseline/dirty evidence,
procedure graph, compact verification profile, browser decision과 안전한
runtime hint, spec/ticket reference만 기록합니다. Credential, cookie, token,
OTP, exact identity, lifecycle status, claim, cursor는 저장하지 않습니다.
Writer는 repo-local·symlink-safe·mode-0600 atomic replacement를 사용하며,
resume은 artifact와 repository evidence를 다시 읽습니다.

Spec 또는 tickets 단계가 새 사용자 결정을 요구하면 해당 procedure는
`User decision: required`와 근거를 active graph에 직접 넘깁니다. Drive는
`tk-grill-me`로 결정을 닫고 Ready spec을 다시 검증한 뒤 필요한 downstream
tickets를 재도출합니다. Executing 중 발견된 첫 late decision도 같은 graph의
한 번의 amendment만 허용하며, 같은 blocker 재발 또는 두 번째 결정은
`Blocked`로 멈춥니다. Phase owner끼리는 서로 호출하지 않습니다.

초기 구현 뒤 aggregate verification이 격리된 실패를 관찰한 경우에만
corrective `tk-implement`를 최대 세 번 호출합니다. 네 번째, 동일 실패 반복,
격리되지 않은 실패, scope 확장은 남은 실패 명령과 근거를 한 번 보고하고
mutation을 중단합니다. Reflection 자동 적용은 drive 시작 시 기록된 정확한
기존 ignored/untracked user-managed repo rule 하나에만 허용됩니다. Tracked,
new, unignored, symlinked, external, drifted, ambiguous target은 정상 approval
boundary에 남습니다.

Recoverable alternate edge가 없는 `Fail | Blocked | Unverifiable`에서는
product mutation과 downstream specialist invocation을 즉시 동결합니다.
`tk-drive non-success finalization`은 기존 artifact와 Git evidence만 다시
읽어 prior verified commits를 `Completed`, 직접 중단된 scope를 `Stopped`,
남은 unit을 `Dependency blocked | Not attempted | Unverified`로 구분하고,
originating native status와 recovery action 하나를 보고합니다. 새 partial
status, public skill, run ledger, 자동 cleanup, 독립 unit continuation은
추가하지 않습니다. Child-native `pending | Draft | Unresolved split report |
aborted`는 graph에서 먼저 정규화하며, terminal ticket attempt의 bounded
writer는 `tk-drive non-success finalization` 하나로 고정합니다.

### 브라우저 검증이 필요한 구현

`tk-implement`가 사용자에게 보이는 UI나 browser behavior를 변경하면 hybrid `tk-browser-verify`를 최종 검증 단계에 자동 적용합니다. Figma, screenshot 또는 디자인 명세가 기준이면 구현 전 intent preflight와 구현 후 runtime screenshot 검증을 모두 수행합니다.

```text
tk-implement
→ UI 또는 browser behavior 변경
→ tk-browser-verify 자동 적용
→ runtime screenshot 실제 검사
→ Pass일 때 commit
```

### 구현 후 추가 피드백

작은 UI 조정, 문구 수정, 명확한 누락이나 단순 피드백은 새 skill 없이 현재 대화에서 처리하세요. 별도 전략, 검증, commit이 필요한 추가 작업에는 `tk-implement`를 다시 사용하세요.

```text
구현 완료
→ 작은 후속 피드백: 현재 대화에서 계속
→ 별도 변경과 commit: tk-implement
```

### 구현 후 결함

원인과 수정이 명확하면 현재 대화 또는 `tk-implement`로 처리합니다. 원인이 불명확한 bug를 명시적으로 구현 요청하면 `tk-implement`가 red-capable feedback loop, 가설 격리, regression seam과 cleanup을 조건부로 적용합니다.

```text
tk-implement
→ 결함 발견
   ├─ 원인과 수정이 명확함: 최소 수정과 검증
   └─ 원인이 불명확함: 내장 investigation loop 후 수정
```

### 구현 Review

모든 `tk-implement` unit은 commit 전에 current-agent Standards/Spec review를
실행합니다. Large 또는 high-risk 변경만 독립 reviewer 한 명을 사용할 수
있습니다. `tk-drive`는 이 ticket-level review를 반복하지 않고 전체 R/AC,
commit ancestry, cross-ticket interaction을 aggregate review합니다. 일반
review-only 요청은 source를 수정하지 않는 일반 agent 작업으로 처리합니다.

### 테스트와 커버리지

TDD는 공개 동작 seam과 회귀 위험에 따라 선택하는 구현 전략입니다. 그러나 새
production behavior의 durable automated test는 완료 조건입니다. 버그·회귀에
의미 있는 public seam이 있으면 수정 전 red와 수정 후 green을 실제로
관찰합니다.

Repository에 coverage command나 threshold가 있으면 그대로 실행합니다. 도구가
없으면 dependency나 임의 percentage를 만들지 않고
`coverage: unavailable`로 보고합니다. Production behavior에 의미 있는 test
seam이 없으면 named exception과 deterministic alternative verification을
사용자가 명시적으로 승인하기 전에는 commit하지 않습니다.

### 재사용 가능한 학습

```text
작업 완료
→ tk-reflect
→ 필요하면 tk-learn
```

### Agent Skill 이상 진단

```text
특정 tk-* skill의 관찰된 호출·계약·host·eval·효율 이상
→ tk-skill-diagnose
→ fresh reproduction + failure-plane isolation
→ semantic candidate면 tk-learn handoff 제안
```

증상 없는 전체 catalog 최적화는 Darwin 같은 외부 optimizer가 담당하고,
기존 rule/skill의 정적 구조 감사는 `tk-grooming`이 담당합니다.

### 장기 저장소 결정

기능 branch의 일반 구현 결정은 spec, ticket, commit, PR, code, test에 남기세요. Branch마다 ADR이나 domain 문서를 자동 생성하지 않습니다.

Merge 이후에도 저장소 전체를 장기 제약하고, 되돌리기 비싸며, 코드만으로 선택 이유를 이해하기 어려운 결정만 명시적으로 ADR 작성을 요청하세요.

```text
branch 한정 결정 → spec / ticket / commit / PR
저장소 장기 제약 → 명시적 ADR 요청
```

## 제거 기능 대체

| 제거된 기능 | 대체 위치 |
| --- | --- |
| 질문형 설계 검증 | `tk-grill-me` |
| domain 용어 결정 | `tk-grill-me`에서 질문하고 필요하면 `tk-to-spec`에 기록 |
| TDD | `tk-implement`의 TDD option |
| diff 구조 review | `tk-implement`의 built-in Standards/Spec review |
| regression seam 문제 | `tk-to-spec` bug contract와 `tk-implement` investigation loop |
| Agent Skill incident 원인 | `tk-skill-diagnose` |
| 장기 학습 | `tk-reflect`, 필요하면 `tk-learn` |

`CONTEXT.md`, glossary, domain 문서, ADR은 feature branch 작업 중 자동 mutation하지 않습니다.

## `.tigerkit/`

`.tigerkit/`은 compact preflight, 현재 spec, ticket, implementation/reflection
ledger, handoff, prototype, skill draft, browser evidence를 보관하는 선택적
repo/worktree-local scratch입니다. 영구 project 문서나 전역 TigerKit 상태가
아닙니다. TigerKit은 consumer repository의 `.gitignore`를 수정하지 않고,
scratch가 무시되지 않으면 경고합니다. `docs/tigerkit/`를 만들지 않습니다.

## 버전 관리

`main`은 지속 갱신되는 최신 source이며 stable release tag와 GitHub Release는 검증된 `origin/main` commit에서만 생성합니다. Git tag는 immutable snapshot입니다. Skill 이름이나 기존 explicit invocation 경로 삭제, 호환되지 않는 scratch 또는 배포 변경은 major release입니다.

## 로컬 검증

TigerKit은 GitHub Actions에서 validator, eval, packaging smoke test, CLI canary를 실행하지 않습니다. 유지보수자는 변경과 release 전에 다음 검증을 로컬에서 실행합니다.

```sh
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
(cd scripts && python3 -m unittest)
python3 scripts/sync_eval_compat.py
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
```

Packaging 변경은 임시 home에서 Claude Code·Codex·Hermes Agent를
smoke-install합니다. Root `evals/*.yaml`은 빠른 정적 계약이며 각 skill의
`evals/`는 trigger train/validation과 success/boundary behavior assertion을
소유합니다. 실제 모델 평가는 candidate를 이전 stable baseline과 clean
context에서 로컬 비교하고 결과를 repository 밖의 임시 경로에 보관합니다.
User-invoked skill의 `argument-hint`, `disable-model-invocation`, hybrid skill의
좁은 trigger eval, Codex `agents/openai.yaml`은 portable Agent Skills core
위의 명시적인 host extension입니다.

Live eval adapter는 격리된 실행마다 `skill_loaded`, `output`, `terminal_status`, `total_tokens`, `duration_ms`를 JSON으로 반환합니다. Python harness가 terminal/file/Git assertion을 직접 검증하고 의미 품질만 별도 grader에 전달하며, token/time이 없거나 credential이 없으면 `Pass` 대신 `Unverifiable`로 남깁니다.

## 출처 표기

현재 배포 skill과 제거·병합된 upstream-derived behavior attribution은 `NOTICE.md`에 구분해 보존합니다. TigerKit은 adapted skill에 `tk-` prefix와 `relationship: adapted` metadata를 사용합니다.

TigerKit 20.1.2 또는 이전 버전에서 갱신한다면 `MIGRATION.md`를 읽으세요.
