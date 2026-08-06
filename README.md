# TigerKit

<p align="center">
  <img src="assets/tigerkit-cover.webp" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 엔지니어링 Agent Skills 모음입니다.
중앙 workflow runtime이나 plugin 없이 self-contained skill을 `npx skills`로
배포합니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

설치된 skill을 갱신하려면 전역 update를 실행합니다.

```bash
npx skills update --global --yes
# 짧은 표기: npx skills update -g -y
```

`npx skills add .` 또는 로컬 경로 설치는 저장소 검증·개발용입니다. 같은 checkout에
전역 설치와 로컬 설치를 함께 두면 Codex가 두 skill root를 모두 발견해 picker에
중복 표시할 수 있으므로 실제 사용자 설치에는 `MTGVim/tiger-kit`를 사용하세요.

Claude Code와 Hermes Agent에서는 `/tk-implement`, Codex에서는
`$tk-implement` 또는 skill picker를 사용합니다.
PR lifecycle은 `/tk-pr-open`, `/tk-pr-triage`, `/tk-pr-respond`,
`/tk-pr-rebase`, `/tk-pr-sweep`를 직접 선택하며, `tk-pr-open`은 명확한
단일 PR 자연어 요청으로도 시작할 수 있습니다.

## Skill 표면

| Skill | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-drive` | user | 명시 source를 결정·Ready spec·조건부 tickets·unit commits·aggregate verification·finalization까지 진행 |
| `tk-ask-repo` | user | repository 질문을 `path:line` 근거로 조사하는 read-only desk |
| `tk-grill-me` | hybrid | material user decision을 evidence-first 질문 하나씩 닫음 |
| `tk-to-spec` | hybrid | 독립 구현 가능한 Ready R/AC spec 작성 |
| `tk-to-tickets` | hybrid | Ready spec을 독립 검증 가능한 vertical units로 분해 |
| `tk-implement` | hybrid | unit 하나를 구현·테스트·review하고 verified commit 하나 생성 |
| `tk-pr-open` | hybrid | 명확한 단일 PR 요청으로 초안·publish plan을 작성하고 승인 후 create/update |
| `tk-pr-triage` | hybrid | 명시 호출 또는 sweep handoff에서 repository의 PR·review·check·reply 상태를 read-only 분류 |
| `tk-pr-respond` | hybrid | 명시 호출 또는 sweep handoff에서 feedback·GitHub Actions를 resolution unit으로 처리하고 bounded publish |
| `tk-pr-rebase` | hybrid | 명시 호출 또는 sweep handoff에서 열린 PR을 최신 base에 rebase하고 bounded force-with-lease·review follow-up publish |
| `tk-pr-sweep` | user | configured repositories의 지원 가능한 PR maintenance를 fresh triage·bounded child routes로 일괄 처리 |
| `tk-github-image-upload-to-pr` | user | 로컬 evidence image를 인증된 browser session으로 기존 PR 본문이나 요청된 comment에 upload |
| `tk-prototype` | hybrid | 폐기 가능한 UI/logic 비교물을 실행 |
| `tk-browser-verify` | hybrid | 실제 browser UI·network·최종 상태 검증 |
| `tk-skill-diagnose` | hybrid | 관찰된 Agent Skill incident를 재현·격리하고 verified `learn-ready` objective를 handoff |
| `tk-learn` | hybrid | `create | improve | merge`를 유일하게 소유하는 repository/user skill 작성자; 승인 전에는 쓰지 않음 |
| `tk-grooming` | hybrid | 기존 repository/user skill의 중복·범위·배치를 감사 |
| `tk-handoff` | hybrid | 현재 evidence 기반 resume snapshot 작성·재개 |
| `tk-merge-conflict` | hybrid | 진행 중인 Git conflict의 의도를 복원하고 operation 완료 |

작은 수정과 일반 후속 피드백은 skill 없이 현재 대화에서 처리합니다. 별도 artifact,
commit, 검증 또는 안전 경계가 있을 때만 해당 skill을 선택합니다.

## PR lifecycle

```text
/tk-pr-open
→ repository·branch·HEAD·기존 PR 확인
→ exact draft와 publish plan
→ current-turn publish approval
→ bounded push + PR create/update

/tk-pr-triage
→ executing repository resolve
→ paginated read-only PR·review·check·reply collection
→ actionable category와 next action

/tk-pr-respond
→ review thread와 comment를 resolution unit으로 grouping
→ user selection
→ unit마다 tk-implement + verified commit
→ aggregate verification과 exact publish plan
→ current-turn approval 뒤 push·reply·verified resolve
→ 모든 actionable finding 해결 시 필요한 human reviewer에게 re-review request

/tk-pr-rebase
→ exact PR head와 최신 base SHA 고정
→ local rebase; active conflict만 tk-merge-conflict로 해결
→ verification과 exact force-with-lease·review follow-up plan
→ current-turn approval 뒤 publish
→ post-push review state에 따라 human re-review request

/tk-pr-sweep
→ configured repositories fresh triage
→ supported Act now PR을 exact head로 순차 revalidate
→ conflict는 tk-pr-rebase --ci, Actions·feedback은 tk-pr-respond --ci
→ PR-local failure를 격리하고 bounded route·worktree lifecycle 적용
→ final fresh triage와 aggregate report
```

다섯 skill은 포괄 권한을 공유하지 않습니다. `tk-pr-triage`는 항상 read-only이며,
`tk-pr-open`, 일반 `tk-pr-respond`, 일반 `tk-pr-rebase`는 exact publish plan의 현재
turn 승인이 있기 전에는 remote write를 하지 않습니다. 명시적 `tk-pr-sweep`만 fresh
exact evidence 안에서 child의 bounded `--ci` route를 승인합니다.

## `tk-drive`

```text
explicit tk-drive <source>
→ material decision이 있을 때만 tk-grill-me
→ tk-to-spec
→ 여러 독립 unit일 때만 tk-to-tickets
→ unit마다 tk-implement + verified commit
→ aggregate verification
→ 필요할 때 tk-browser-verify
→ tk-drive finalization
```

`tk-learn`만 `create | improve | merge` skill 변경을 작성합니다.
`tk-skill-diagnose`는 검증된 목표를 `learn-ready`로 handoff하고,
`tk-grooming`은 repository/user skill만 감사하며 rule lifecycle을 소유하지
않습니다. `tk-browser-verify`는 Guard와 Verdict 모두 실제 이미지 검사를 거친
스크린샷과 가능한 경우 `Evidence directory: /absolute/path/...`를 남깁니다.

Continuation은 prompt-directed이며 durable scheduler나 cross-turn replay를
보장하지 않습니다. Process 또는 host 경계를 넘으면 `.tigerkit/` artifact,
Git, tests, browser evidence를 다시 읽어 다음 node를 선택합니다.

TigerKit은 이 한계를 문구로 숨기지 않습니다. `scripts/run_drive_experiment.py`는
동일한 source를 `tk-drive` arm과 명시 phase composition arm으로 실행하여 terminal
상태, phase continuation, commit, verification, token/time을 비교합니다. 측정된
명확한 열세가 없으면 catalog에서 `tk-drive`를 자동 삭제하지 않습니다.

## Eval single source of truth

각 package가 자신의 executable 계약을 소유합니다.

```text
skills/<skill>/evals/triggers.json  trigger SSOT
skills/<skill>/evals/evals.json     behavior SSOT
evals/catalog-routing.json          cross-skill routing SSOT
evals/release-critical.json         release quality subset
evals/drive-ab.json                  drive A/B scenarios
```

생성된 `test-prompts.json`, root trigger/behavior 복제 fixture, Darwin projection
동기화 단계는 없습니다. `scripts/validate_skills.py`는 `skills/tk-*`를 자동
발견하고 canonical JSON schema, mechanical assertions, host metadata, links,
release-critical references를 직접 검증합니다.

## 로컬 검증

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
node --check skills/tk-pr-triage/scripts/triage.mjs
node --test skills/tk-pr-triage/scripts/triage.test.mjs
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

Release gate:

```bash
python3 scripts/run_release_gate.py \
  --baseline "$(git describe --tags --abbrev=0)" \
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```

Release gate는 contract 비교, validator, test, package, diff를 로컬에서만 실행합니다.
실제 host 품질 실험은 release 차단 조건이 아니며 별도의 목적별 실험으로 수행합니다.

Drive 비교 실험:

```bash
python3 scripts/run_drive_experiment.py \
  --candidate HEAD \
  --output /tmp/tigerkit-drive-ab
```

## State와 권한

`.tigerkit/`은 repo/worktree-local scratch이며 영구 project 문서나 전역 상태가
아닙니다. TigerKit은 consumer `.gitignore`를 수정하지 않습니다.

`tk-learn`은 reusable skill의 `create | improve | merge`를 유일하게 소유합니다.
Evidence, dedupe, trigger/eval, baseline/compatibility gate를 먼저 검증하고,
현재 turn의 명시적 apply 승인이 있기 전에는 canonical skill path를 쓰지 않습니다.
`tk-skill-diagnose`와 `tk-grooming`은 `tk-learn`용 proposal만 만들며 자동 invoke하지
않습니다.

`tk-implement`와 `tk-drive`의 명시 호출은 문서화된 current-branch commit까지만
허용합니다. Push, PR, merge, tag, release, publish는 별도 명시 권한 없이는
수행하지 않습니다.

`tk-pr-triage`는 remote와 local을 변경하지 않습니다. `tk-pr-open`은 PR create/update를,
`tk-pr-respond`는 push·reply·verified thread resolve를 exact current-turn publish
approval 뒤에만 수행합니다. `tk-pr-rebase`는 exact lease를 고정한 force-with-lease,
rebase-satisfied reply·resolve, 조건부 human re-review만 같은 승인 뒤에 수행합니다.
`tk-pr-sweep`는 이 두 one-PR owner의 bounded `--ci` route만 orchestration합니다.
네 mutation skill 모두 merge·tag·release 권한을 갖지 않습니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 읽으세요.
Attribution은 [NOTICE.md](NOTICE.md)에 보존됩니다.
