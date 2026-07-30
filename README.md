# TigerKit 20.3.1

<p align="center">
  <img src="assets/tigerkit-cover.png" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 소규모 엔지니어링 Agent Skills
모음입니다. 중앙 workflow runtime 없이 14개 self-contained skill을
`npx skills`로 배포합니다. Decision closure, spec, ticket, implementation은
각각 하나의 canonical phase skill이 소유하고 `tk-drive`가 그 결과를
단방향으로 오케스트레이션합니다. 최신 immutable release는 `v20.3.1`이며,
현재 `main`에는 다음 release를 위한 skill 변경이 포함될 수 있습니다.

`v20.3.1` release는 모든 terminal user summary를 정확히 한 번의 Markdown
`---` 뒤에서 시작하고, 맨 아래 Receipt block과 반복 `Outcome:` label을
제거합니다. 진행 commentary와 active-drive phase handoff는 이 경계를 만들지
않습니다. Phase receipt는 내부 control envelope로 유지되고, 장기 provenance는
각 skill이 이미 소유한 spec·tickets·implementation·handoff·browser ledger에만
남습니다. 공용 receipt ledger나 read-only skill의 새 write surface는 없습니다.
`tk-drive`는 terminal boundary 직전에 transition debt를 검사하므로 성공한
child receipt의 `Outstanding transition`이 실행되기 전에는 최종 응답으로
종료할 수 없습니다.

14개 canonical skill 모두 최신 명시 언어 지시를 우선하는 response-language
hard gate를 포함합니다. 별도 지시가 없으면 현재 사용자 메시지의 언어를
따르며, 자유 서술은 그 언어로 통일합니다. Canonical heading, status, ID,
command, path, code, exact source literal은 원문 그대로 유지합니다.

같은 14개 skill은 canonical output schema를 보존하는 actionable-output hard
gate도 자체 포함합니다. 필수 heading·table·status semantics는 유지하면서 첫
자유 서술 위치에서 답·결과·행동을 먼저 제시하고, 진행 상태와 근거 있는 복구
행동을 짧게 드러냅니다. 완료 뒤에는 불필요한 다음 행동이나 맺음말을 만들지
않습니다. 별도 mode skill이나 shared runtime reference는 없습니다.

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

변경되지 않는 `v20.3.1` snapshot:

```bash
npx skills add "MTGVim/tiger-kit#v20.3.1" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code와 Hermes Agent에서는 `/tk-implement` 같은 slash command로 표시됩니다. Codex에서는 `$tk-implement` 또는 skill picker를 사용합니다.

## Skill 목록

- **`[user]` user-invoked 2개**: 사용자가 명시적으로 선택하며 implicit invocation이 차단됩니다.
- **`[user/auto]` hybrid 12개**: 사용자 선택과 description의 좁은 positive trigger를 모두 지원합니다.
- model-only skill은 없습니다.

| Skill | 호출 | 목적 |
| --- | --- | --- |
| `tk-ask-repo` | user | 외부에서 들어온 repository 질문을 분류하고 원점·소비처·영향·책임을 `path:line` 근거로 조사합니다. |
| `tk-drive` | user | 명시적으로 시작한 source를 조건부 decision closure, canonical phase owner, ticket별 commit과 최종 aggregate verification까지 진행합니다. |
| `tk-grill-me` | hybrid | 명시 선택 또는 drive decision handoff에서 사실을 조사하고 중요한 결정을 한 번에 한 질문씩 닫습니다. |
| `tk-to-spec` | hybrid | 독립 요청 또는 drive handoff에서 Ready spec을 작성·검증합니다. |
| `tk-to-tickets` | hybrid | 독립 요청 또는 drive handoff에서 source를 수직 ticket으로 나눕니다. |
| `tk-implement` | hybrid | 명시 선택 또는 drive의 implementation handoff에서 unit 하나를 테스트·review하고 commit 하나로 만듭니다. |
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

전체 흐름은 현재 host에서 user-invoked `tk-drive`를 명시적으로 선택해
시작합니다. Claude Code·Hermes Agent의 `/tk-drive`, Codex의 `$tk-drive`,
host skill picker의 직접 선택이 같은 explicit start입니다. Unresolved
user-owned decision이 있으면 drive가 `tk-grill-me`에 decision closure를
위임하고, `confirmed` receipt 뒤 spec gate부터 자동으로 이어갑니다. 이미
명확한 source에는 grill을 호출하지 않습니다.

```text
<host-native explicit tk-drive> <source>
→ 필요할 때만 tk-grill-me: confirmed Decisions receipt
→ tk-to-spec: Ready spec
→ 필요할 때만 tk-to-tickets: vertical ticket ledger
→ ticket마다 tk-implement: test + review + verified commit 하나
→ tk-drive: aggregate traceability + broad verification 한 번
```

Preflight는 source와 repository evidence에서 material risk signal이 확인될
때만 compact verification profile을 고정합니다. Profile은 기존 owner에
regression, compatibility, browser, recovery, bounded independent-review
의무를 전달할 뿐 새 score·stage·artifact를 만들지 않습니다. 근거가 없는
low-risk 경로는 추가 출력이나 검증 없이 기존 흐름을 유지합니다.

Spec 또는 tickets 단계가 새 사용자 결정을 요구하면 해당 phase는
`User decision: required`와 근거를 native non-success receipt로 drive에
반환합니다. Drive는 grill로 결정을 닫고 Ready spec을 다시 검증한 뒤
downstream tickets를 재도출합니다. 같은 blocker가 재발하면 다시 순환하지
않고 `Blocked`로 멈춥니다. Phase owner끼리는 서로 호출하지 않습니다.

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

`.tigerkit/`은 현재 spec, ticket, handoff, prototype, skill draft, browser evidence를 보관하는 선택적 repo/worktree-local scratch입니다. 영구 project 문서나 전역 TigerKit 상태가 아닙니다. TigerKit은 consumer repository의 `.gitignore`를 수정하지 않고, scratch가 무시되지 않으면 경고합니다. `docs/tigerkit/`를 만들지 않습니다.

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
