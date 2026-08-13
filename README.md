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
 .tigerkit/seed.md
          ↓
 ordinary agent work
          ↓
 review / verification
          ↓
       commit
          ↓
     tk-pr-open
```

`tk-prep`은 저장소 근거와 자연스러운 대화로 작업을 명확하게 만들고,
새 세션이나 더 낮은 수준의 구현 모델이 원 대화 없이 읽을 수 있는 `.tigerkit/seed.md`를 만듭니다.

Ready `Seed` 뒤의 `split`, 하위 에이전트 `fan-out`, 순차 실행, 실제 모델 선택은
TigerKit 실행 규약이 아니라 현재 `agent`/`host`의 실행 판단입니다.
같은 세션에서는 `Seed` 승인 뒤 “진행해”, 새 세션에서는 “`.tigerkit/seed.md` 읽고 진행해” 정도면 충분해야 합니다.

작은 수정과 평범한 후속 의견은 스킬 없이 현재 대화에서 바로 처리합니다.

## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | 저장소 근거와 대화형 인터뷰로 실행 준비된 `Seed` 작성 |
| `tk-audit` | `user` | 읽기 전용 저장소 감사와 `AUD-*` 발견 사항 |
| `tk-ask-repo` | `user` | 저장소 동작·값·영향·귀속을 근거와 함께 설명 |
| `tk-pr-open` | `hybrid` | 검증된 `commit`의 제한된 `push` + PR 생성/갱신 |
| `tk-pr-respond` | `hybrid` | 한 PR의 리뷰/지원 CI 분석·수정·검증·`reply`/`resolve` |
| `tk-pr-rebase` | `hybrid` | 정확한 PR의 최신 `base` `rebase`와 제한된 `force-with-lease` |
| `tk-pr-sweep` | `user` | 여러 PR의 결정론적 분류와 승인된 유지보수 묶음 |
| `tk-github-image-upload-to-pr` | `user` | 기존 PR에 로컬 근거 이미지 올리기 |
| `tk-prototype` | `hybrid` | 폐기 가능한 UI/로직 비교물 |
| `tk-browser-verify` | `hybrid` | 화면에 보이는 AC의 `headless` 실행 검증 |
| `tk-skill-diagnose` | `hybrid` | `Agent Skill` 사고 재현·격리와 `learn-ready` 인계 |
| `tk-learn` | `hybrid` | 재사용 가능한 스킬의 생성/개선/병합 작성자 |
| `tk-grooming` | `hybrid` | 저장소/사용자 스킬 목록 감사 |
| `tk-handoff` | `hybrid` | 진행 중 작업의 재개용 상태 사진 |
| `tk-merge-conflict` | `hybrid` | 활성 Git 충돌 의도 복원 |
| `tk-mwhat` | `user` | 직전 설명을 더 쉽게 다시 설명 |
| `tk-wizard` | `hybrid` | 사람이 직접 해야 하는 설정·인증·이관 절차 안내 |

`user`는 명시 호출 전용이고, `hybrid`는 해당 작업 의도가 명확할 때 자동 진입할 수 있습니다.

## `tk-prep`과 `Seed`

`tk-prep`은 고정 양식 위저드가 아닙니다.
내부적으로는 명확도와 엔지니어링 준비도를 엄격하게 평가하지만,
사용자에게는 현재 이해, 추천, 이유를 자연스러운 대화로 설명합니다.

사용자에게 직접 묻는 것은 제품/범위 같은 사용자 소유 결정, 위험하거나 비가역적인 결정,
충분히 개선한 뒤에도 남는 엔지니어링 예외 승인뿐입니다.

이해 준비도는 다음 축을 봅니다.

```text
Goal          20%
Context       20%
Scope         15%
Decisions     15%
Acceptance    15%
Verification  15%
```

점수는 `0 | 0.25 | 0.5 | 0.75 | 1`만 사용하며,
가중 모호성이 `0.20` 이하이고 모든 축이 `0.75` 이상이어야 인터뷰를 끝낼 수 있습니다.
이 기준은 사용자 승인으로 우회할 수 없습니다.

엔지니어링 준비도는 각 축을 독립적으로 확인합니다.

```text
Reuse
Simplicity
Tests
Security
Experience
```

사용자 표시 상태는 `준비됨 | 보완 필요 | 개선 한계 | 예외 승인 | 해당 없음`입니다.
미달 축은 먼저 추가 조사와 접근 개선을 시도하고, 더 끌어올릴 수 없을 때만 이유·남은 위험·완화책과 함께 예외 승인을 받습니다.

Ready `.tigerkit/seed.md`는 현재 작업의 자체 완결 실행 맥락입니다.
목표/배경, 현재 상태, 범위, 사용자 결정, 구현 안내, AC, 검증, 브라우저 계획, 엔지니어링 예외를 구현자가 원 대화 없이 이해할 수 있게 담습니다.

`worker`/`wave` 진행 상태, 제공자 모델 선택자, 추론 강도, 영수증, 비밀 값은 `Seed`에 저장하지 않습니다.

## 브라우저 검증

`browser-visible` AC가 있으면 `tk-prep`에서 대상, `headless`, 인증, `viewport`, 개발 서버, `screenshot` 근거, 통과 조건을 정합니다.
비밀번호, `token`, OTP, `cookie`, `session` 비밀 값은 `Seed`에 저장하지 않고 실행 시 일시 입력으로만 다룹니다.

개발 서버가 필요하면 시작·준비 확인·정리는 `tk-browser-verify`가 소유합니다.

## 대화형 사용 경험

공통 원칙은 **대화는 자연스럽게, 상태는 엄격하게**입니다.

- `tk-prep`: 함께 작업 맥락을 정리해 `Seed`를 만듭니다.
- `tk-wizard`: 사람이 직접 해야 하는 일을 한 단계씩 자연스럽게 안내합니다.
- `tk-ask-repo`: 질문에 먼저 답하고 코드 흐름을 설명한 뒤 `3~10`줄 공유용 요약을 제공합니다.
- `tk-pr-respond`: 리뷰 의도를 해석하고 해결 방향과 이유를 합의합니다.
- `tk-pr-sweep`: 여러 PR 중 지금 할 일과 기다릴 일을 최신 분류로 브리핑합니다.

내부 분류, 실행 기반, 경로 상태, 영수증을 기본 사용자 화면에 덤프하지 않습니다.

## PR 흐름

```text
tk-pr-open
→ verified branch/HEAD/template/evidence preview
→ current-turn publication approval
→ bounded push + PR create/update

tk-pr-respond
→ fresh exact PR read
→ review/CI 의미 설명 + 필요한 결정만 질문
→ one approval
→ code-changing task는 seed.md
→ implement/review/verify
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

PR 원격 권한은 서로 자동 확장되지 않습니다. `merge`, `tag`, `release`에는 별도 권한이 필요합니다.

## 상태와 설정

`.tigerkit/`은 저장소/작업 트리 로컬 임시 공간이며 전역 프로젝트 기억이 아닙니다.
제품 작업의 기본 영구 맥락은 `.tigerkit/seed.md` 하나입니다.

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
  --baseline "$(git describe --tags --abbrev=0)" \
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```

모든 검증은 로컬 전용입니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 참고하세요.
