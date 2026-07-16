# TigerKit 19

<p align="center">
  <img src="assets/tigerkit-cover.png" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 소규모 엔지니어링 Agent Skills 모음입니다. 중앙 workflow runtime 없이 13개 self-contained skill을 `npx skills`로 배포합니다.

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

변경되지 않는 `v19.0.5` snapshot:

```bash
npx skills add "MTGVim/tiger-kit#v19.0.5" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code와 Hermes Agent에서는 `/tk-implement` 같은 slash command로 표시됩니다. Codex에서는 `$tk-implement` 또는 skill picker를 사용합니다.

## Skill 목록

- **`[user]` user-invoked 9개**: 사용자가 명시적으로 선택하며 implicit invocation이 차단됩니다.
- **`[user/auto]` hybrid 4개**: 사용자 선택과 명확한 상황의 자동 적용을 모두 지원합니다.
- model-only skill은 없습니다.

| Skill | 호출 | 목적 |
| --- | --- | --- |
| `tk-grill-me` | user | 사실을 조사한 뒤 중요한 결정을 한 번에 한 질문씩 검증합니다. |
| `tk-to-spec` | user | 확인된 사실과 결정을 구현 명세로 작성합니다. |
| `tk-to-tickets` | user | 명세를 독립 검증 가능한 수직 ticket으로 나눕니다. |
| `tk-implement` | user | 전략 승인 후 구현, 검증, current-branch commit을 수행합니다. |
| `tk-prototype` | user | 폐기 가능한 UI 또는 logic 검증물을 만듭니다. |
| `tk-reflect` | user | 재사용 가능한 repository/user rule 또는 skill 후보를 보고합니다. |
| `tk-learn` | user | 확인된 근거를 reusable repository/user skill로 작성합니다. |
| `tk-grooming` | user | 기존 rule과 skill을 점검하고 명시 승인 시 수정합니다. |
| `tk-handoff` | user | 검증된 작업 상태를 기록하거나 재개합니다. |
| `tk-browser-verify` | hybrid | 실제 browser에서 UI, network, final state를 검증합니다. |
| `tk-diagnosing-bugs` | hybrid | red-capable feedback loop로 원인 불명 결함을 진단하고 검증합니다. |
| `tk-code-review` | hybrid | fixed point 이후 diff를 Standards와 Spec 축으로 수정 없이 검토합니다. |
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

원인과 수정이 명확하면 현재 대화 또는 `tk-implement`로 처리합니다. 재현, 최소화, 가설 검증이 필요하면 `tk-diagnosing-bugs`를 사용합니다.

```text
tk-implement
→ 결함 발견
   ├─ 원인과 수정이 명확함: 현재 대화 또는 tk-implement
   └─ 원인이 불명확함: tk-diagnosing-bugs
```

### 독립 Review

현재 branch나 fixed point 이후 변경을 수정 없이 검토하려면 `tk-code-review`를 사용하세요.

```text
tk-implement
→ 필요하면 tk-code-review
```

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
| diff 구조 review | `tk-code-review` Standards 축 |
| regression seam 문제 | `tk-diagnosing-bugs` |
| 장기 학습 | `tk-reflect`, 필요하면 `tk-learn` |

`CONTEXT.md`, glossary, domain 문서, ADR은 feature branch 작업 중 자동 mutation하지 않습니다.

## `.tigerkit/`

`.tigerkit/`은 현재 spec, ticket, handoff, prototype, skill draft, browser evidence를 보관하는 선택적 repo/worktree-local scratch입니다. 영구 project 문서나 전역 TigerKit 상태가 아닙니다. TigerKit은 consumer repository의 `.gitignore`를 수정하지 않고, scratch가 무시되지 않으면 경고합니다. `docs/tigerkit/`를 만들지 않습니다.

## 버전 관리

`main`은 지속 갱신되는 최신 source입니다. Git tag는 immutable snapshot입니다. Skill 이름 삭제, invocation kind 변경, 호환되지 않는 scratch 또는 배포 변경은 major release입니다.

## 출처 표기

현재 배포 skill과 제거·병합된 upstream-derived behavior attribution은 `NOTICE.md`에 구분해 보존합니다. TigerKit은 adapted skill에 `tk-` prefix와 `relationship: adapted` metadata를 사용합니다.

TigerKit 16.x 또는 18.x에서 이전한다면 `MIGRATION.md`를 읽으세요.
