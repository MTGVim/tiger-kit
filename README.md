# TigerKit 20

<p align="center">
  <img src="assets/tigerkit-cover.png" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 소규모 엔지니어링 Agent Skills 모음입니다. 중앙 workflow runtime 없이 12개 self-contained skill을 `npx skills`로 배포합니다. 현재 `main`은 최신 release source이며, 아래 immutable tag로 동일한 released snapshot을 설치할 수 있습니다.

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

변경되지 않는 `v20.1.2` snapshot:

```bash
npx skills add "MTGVim/tiger-kit#v20.1.2" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code와 Hermes Agent에서는 `/tk-implement` 같은 slash command로 표시됩니다. Codex에서는 `$tk-implement` 또는 skill picker를 사용합니다.

## Skill 목록

- **`[user]` user-invoked 2개**: 사용자가 명시적으로 선택하며 implicit invocation이 차단됩니다.
- **`[user/auto]` hybrid 10개**: 사용자 선택과 description의 좁은 positive trigger를 모두 지원합니다.
- model-only skill은 없습니다.

| Skill | 호출 | 목적 |
| --- | --- | --- |
| `tk-grill-me` | user | 사실을 조사한 뒤 중요한 결정을 한 번에 한 질문씩 검증합니다. |
| `tk-to-spec` | hybrid | 명확한 artifact 요청에서 확인된 사실과 결정을 구현 명세로 작성합니다. |
| `tk-to-tickets` | hybrid | 명확한 decomposition 요청에서 source를 수직 ticket으로 나눕니다. |
| `tk-implement` | user | 전략 결정 후 구현, 검증, built-in review와 current-branch commit을 수행합니다. |
| `tk-drive` | hybrid | 명시적으로 시작한 source를 planning부터 verified commit 하나까지 진행하고 pending 답변에서 재개합니다. |
| `tk-prototype` | hybrid | 폐기 가능한 UI 또는 logic 비교 검증물을 실제 실행합니다. |
| `tk-reflect` | hybrid | 명확한 회고 요청에서 재사용 가능한 rule/skill 후보를 report-only로 분류합니다. |
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

결정이 끝났거나 변경이 작다면 바로 `tk-implement`를 사용할 수 있습니다.

반복해서 같은 전체 흐름을 쓴다면 현재 host에서 `tk-drive`를 명시적으로 선택해 시작할 수 있습니다. Claude Code·Hermes Agent의 `/tk-drive`, Codex의 `$tk-drive`, host skill picker의 직접 선택이 같은 explicit start입니다. Blocking ambiguity가 있을 때만 질문 하나를 남기고, 같은 대화의 답변 뒤 자동으로 이어갑니다. 작은 single-slice에는 ticket을 만들지 않고, 여러 vertical slice 또는 장기 재개 가치가 있을 때만 상태 ledger를 둡니다.

```text
<host-native explicit tk-drive> <source>
→ Ready spec
→ 필요할 때만 tickets 또는 disposable prototype
→ implementation + built-in review
→ verified commit 하나
```

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

모든 `tk-implement`와 `tk-drive` 구현 phase는 commit 전에 current-agent Standards/Spec review를 실행합니다. Large 또는 high-risk 변경만 독립 reviewer 한 명을 사용할 수 있습니다. 일반 review-only 요청은 source를 수정하지 않는 일반 agent 작업으로 처리합니다.

### 재사용 가능한 학습

```text
작업 완료
→ tk-reflect
→ 필요하면 tk-learn
```

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
| 장기 학습 | `tk-reflect`, 필요하면 `tk-learn` |

`CONTEXT.md`, glossary, domain 문서, ADR은 feature branch 작업 중 자동 mutation하지 않습니다.

## `.tigerkit/`

`.tigerkit/`은 현재 spec, ticket, handoff, prototype, skill draft, browser evidence를 보관하는 선택적 repo/worktree-local scratch입니다. 영구 project 문서나 전역 TigerKit 상태가 아닙니다. TigerKit은 consumer repository의 `.gitignore`를 수정하지 않고, scratch가 무시되지 않으면 경고합니다. `docs/tigerkit/`를 만들지 않습니다.

## 버전 관리

`main`은 지속 갱신되는 최신 source이며 stable release tag와 GitHub Release는 검증된 `origin/main` commit에서만 생성합니다. Git tag는 immutable snapshot입니다. Skill 이름 삭제, invocation kind 변경, 호환되지 않는 scratch 또는 배포 변경은 major release입니다.

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

Packaging 변경은 임시 home에서 Claude Code·Codex·Hermes Agent를 smoke-install합니다. Root `evals/*.yaml`은 빠른 정적 계약이며 각 skill의 `evals/`는 trigger train/validation과 success/boundary behavior assertion을 소유합니다. 실제 모델 평가는 candidate를 이전 stable baseline과 clean context에서 로컬 비교하고 결과를 repository 밖의 임시 경로에 보관합니다. User-invoked skill의 `argument-hint`, `disable-model-invocation`과 Codex `agents/openai.yaml`은 portable Agent Skills core 위의 명시적인 host extension입니다.

Live eval adapter는 격리된 실행마다 `skill_loaded`, `output`, `terminal_status`, `total_tokens`, `duration_ms`를 JSON으로 반환합니다. Python harness가 terminal/file/Git assertion을 직접 검증하고 의미 품질만 별도 grader에 전달하며, token/time이 없거나 credential이 없으면 `Pass` 대신 `Unverifiable`로 남깁니다.

## 출처 표기

현재 배포 skill과 제거·병합된 upstream-derived behavior attribution은 `NOTICE.md`에 구분해 보존합니다. TigerKit은 adapted skill에 `tk-` prefix와 `relationship: adapted` metadata를 사용합니다.

TigerKit 16.x 또는 18.x에서 이전한다면 `MIGRATION.md`를 읽으세요.
