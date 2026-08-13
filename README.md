# TigerKit

TigerKit은 Claude `Code`, Codex, Hermes `Agent`용 엔지니어링 `Agent` `Skills` 모음입니다.
중앙 `workflow` `runtime`이나 `plugin` 없이 독립형 `skill`을 `npx skills`로 배포합니다.

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

## 기본 사용

제품 작업의 기본 흐름은 단순합니다.

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

`tk-prep`은 자연스러운 대화로 작업을 명확하게 만들고,
새 세션이나 더 낮은 수준의 구현 모델이 원 대화 없이 읽을 수 있는
`.tigerkit/seed.md`를 만듭니다.

Ready `Seed` 뒤의 `split`, `subagent` `fan-out`, `sequential` `execution`, 구현 모델 선택은
TigerKit `runtime` `protocol`이 아니라 현재 `agent`/`host`의 실행 판단입니다.

같은 세션에서는 `Seed` 승인 뒤 “진행해”라고 하면 되고, 새 세션에서는
“`.tigerkit/seed.md` 읽고 진행해” 정도면 충분해야 합니다.

## 스킬 구성

| `Skill` | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | hybrid | `repository` `evidence`와 대화형 `interview`로 `executor-ready` `seed.md` 작성 |
| `tk-audit` | `user` | `repository` `read-only` `audit`와 `AUD-*` `finding` |
| `tk-ask-repo` | `user` | `repository` 동작·값·영향·귀속을 근거와 함께 자연스럽게 설명 |
| `tk-pr-open` | hybrid | 검증된 `commit`의 `bounded` `push` + PR `create`/`update` |
| `tk-pr-respond` | hybrid | 한 PR의 `review`/지원 CI 분석·수정·검증·`reply`/`resolve` |
| `tk-pr-rebase` | hybrid | `exact` PR의 최신 `base` `rebase`와 `bounded` `force-with-lease` |
| `tk-pr-sweep` | `user` | 여러 PR의 `deterministic` `triage`와 승인된 `maintenance` `batch` |
| `tk-github-image-upload-to-pr` | `user` | `existing` PR에 `local` `evidence` `image` `upload` |
| `tk-prototype` | hybrid | 폐기 가능한 UI/`logic` 비교물 |
| `tk-browser-verify` | hybrid | 승인된 `browser-visible` AC의 `headless` `runtime` `verification` |
| `tk-skill-diagnose` | hybrid | `Agent` `Skill` `incident` 재현·격리와 `learn-ready` `handoff` |
| `tk-learn` | hybrid | `reusable` `skill`의 `create | improve | merge` `writer` |
| `tk-grooming` | hybrid | `repository`/`user` `skill` `catalog` `audit` |
| `tk-handoff` | hybrid | 진행 중 작업의 `resume` `snapshot` |
| `tk-merge-conflict` | hybrid | `active` Git `conflict` 의도 복원 |
| `tk-mwhat` | `user` | 직전 설명을 더 쉽게 다시 설명 |
| `tk-wizard` | hybrid | 사람이 직접 해야 하는 설정·인증·이관 절차 안내 |

작은 수정과 일반 후속 `feedback`은 `skill` 없이 현재 대화에서 처리합니다.
별도 `context` `preparation`, `remote` `authority`, `runtime` `evidence`, `human-only` `safety` `boundary`가 있을 때
해당 `skill`을 사용합니다.

## `tk-prep`

`tk-prep`은 `form` `wizard`가 아닙니다.

내부적으로는 명확도와 `engineering` `readiness`를 엄격하게 평가하지만,
사용자에게는 현재 이해, 추천, 이유를 자연스러운 대화로 설명합니다.
사용자만 결정할 수 있는 내용, 위험한 결정, `engineering` 예외 승인만 직접 묻습니다.

### `Understanding` `Gate`

내부 점수는 `0 | 0.25 | 0.5 | 0.75 | 1`만 사용합니다.

```text
Goal          20%
Context       20%
Scope         15%
Decisions     15%
Acceptance    15%
Verification  15%
```

`Interview`는 `weighted` `ambiguity`가 `0.20` 이하이고 모든 축이 `0.75` 이상이며
`material` `blocker`/`conflict`가 없을 때만 종료할 수 있습니다.

### `Engineering` `Readiness`

각 축은 독립적으로 확인합니다.

```text
Reuse
Simplicity
Tests
Security
Experience
```

사용자-`facing` 상태는 다음만 사용합니다.

```text
준비됨
보완 필요
개선 한계
예외 승인
해당 없음
```

`개선 한계` 전에는 추가 조사와 `approach` 개선을 먼저 시도합니다.
예외 승인은 남은 `gap`, 이유, 대체 검증을 설명한 뒤에만 가능합니다.

### `Browser-visible` 작업

`Seed`에는 필요 시 다음 `browser` `verification` 계획이 포함됩니다.

- `target`/`environment`
- `headless`/`auth` `strategy`
- `viewport`/`state`
- `dev` `server` `command`/`cwd`/`readiness`
- `screenshot` `evidence`
- `sensitive` `evidence` 처리
- `tk-browser-verify` Pass 조건

`password`/`token`/OTP/`session` `secret` 값은 `Seed`에 저장하지 않습니다.

## `Seed`

`.tigerkit/seed.md`는 현재 작업의 `self-contained` `execution` `context`입니다.

목표는:

> 원 대화가 없는 `fresh` `lower-capability` `executor`가 `repository` + Ready `Seed`만 읽고
> `scope`, `decisions`, `approach`, AC, `verification`을 이해해 안전하게 작업을 시작할 수 있을 것.

`Seed`는 `transcript`나 실행 장부가 아닙니다.
`worker` ID, `wave` `progress`, `provider` `selector`, `reasoning` `effort`, `secret`을 저장하지 않습니다.

실행 중 새 `evidence`가 `Seed`의 `material` `decision`/`scope`/AC를 깨면 임의로 해석 변경하지 않고
`tk-prep`으로 돌아가 `Seed`를 수정·재승인합니다.

## 대화형 UX

다음 `skill`은 공통적으로 **대화는 자연스럽게, 상태는 엄격하게**를 따릅니다.

- `tk-prep`: 함께 작업 `context`를 정리
- `tk-wizard`: 사용자가 직접 해야 할 일을 한 단계씩 안내
- `tk-ask-repo`: `repository` 동작을 자연스럽게 설명하고 마지막에 공유용 요약 제공
- `tk-pr-respond`: 리뷰어 의도를 해석해 해결 방향을 합의
- `tk-pr-sweep`: 여러 PR의 지금 할 일과 기다릴 일을 브리핑

내부 `category`, `backend`, `routing` `state`, `receipt`를 기본 사용자 UI로 덤프하지 않습니다.

## PR `lifecycle`

```text
tk-pr-open
→ exact branch/HEAD/template/evidence preview
→ current-turn publish approval
→ bounded push + PR create/update

tk-pr-respond
→ fresh exact PR/read
→ review/CI 의미 설명 + 필요한 결정만 질문
→ 한 번 승인
→ code-changing task는 seed.md
→ implement/review/verify
→ bounded push/reply/resolve/re-review

tk-pr-rebase
→ exact PR/base/head
→ rebase + conflict owner
→ verification
→ bounded force-with-lease

tk-pr-sweep --report
→ deterministic fresh triage를 읽기 전용 briefing

tk-pr-sweep
→ fresh multi-PR briefing + batch approval
→ exact PR별 Respond/Rebase
→ final fresh triage
```

네 `skill`의 `remote` `authority`는 서로 자동 확장되지 않습니다.
`merge`/`tag`/`release`는 별도 권한이 필요합니다.

## 저장소 질문

`tk-ask-repo`는 질문에 먼저 답하고 코드 흐름을 사람이 이해하기 좋은 순서로 설명합니다.
중요한 주장은 `path:line` 근거에 연결합니다.

답변 마지막에는 본문에서 검증된 사실만 압축한 **공유용 요약 3~10줄**을 제공해
타팀/기획/백엔드/리뷰어에게 그대로 전달할 수 있게 합니다.

## 사람이 직접 해야 하는 설정

`tk-wizard`는 전체 `stage` 표를 먼저 결재받는 도구가 아닙니다.
전체 여정을 짧게 설명하고 사용자가 지금 해야 하는 행동 하나씩 안내합니다.
`secret`은 대화에 남기지 않고, 되돌리기 어렵거나 `production` 영향이 있는 단계에서만
명시 확인을 요구합니다.

## 상태와 설정

`.tigerkit/`은 `repo`/`worktree-local` `scratch`이며 전역 `project` `memory`가 아닙니다.

`Product` `task`의 `durable` `context`는 기본적으로:

```text
.tigerkit/seed.md
```

입니다.

`Sweep`의 장기 `repository` 범위는 다음 `user` `config`를 사용할 수 있습니다.

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

`model` `mapping`, `selector`, `effort`, `worker` `routing`, `fan-out` `preference`, `pitfall` `corpus`는
TigerKit `user-level` `config`로 만들지 않습니다.

## 학습과 반복 발견

별도 `tk-evolve`, `pitfalls.md`, `troubleshooting.md`를 만들지 않습니다.

새 `evidence`는 다음 순서로 처리합니다.

```text
현재 Seed 계약을 바꿈
→ Seed revision + user reapproval

repository에서 반복될 사실
→ test/type/schema/code/instruction 같은 repo-native owner 개선 후보

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

`validator`는 `skills/tk-*`를 자동 발견합니다.

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

`Breaking` `skill`/`eval` `contract`까지 포함한 `release` `gate`:

```bash
python3 scripts/run_seed_release_gate.py \
  --baseline "$(git describe --tags --abbrev=0)" \
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```

모든 `validation`은 `local-only`입니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 참고하세요.
