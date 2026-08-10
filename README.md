# TigerKit

<p align="center">
  <img src="assets/tigerkit-cover.webp" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 엔지니어링 Agent Skills 모음입니다.
중앙 workflow runtime이나 plugin 없이 self-contained skill을 `npx skills` 로
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
중복 표시할 수 있으므로 실제 사용자 설치에는 `MTGVim/tiger-kit` 를 사용하세요.

Claude Code와 Hermes Agent에서는 `/tk-drive`, Codex에서는
`$tk-drive` 또는 skill picker를 사용합니다.
PR lifecycle은 `/tk-pr-open`, `/tk-pr-respond`, `/tk-pr-rebase`,
`/tk-pr-sweep` 를 직접 선택하며 read-only inventory는 `/tk-pr-sweep --report` 를 사용합니다.

## Skill 표면

| Skill | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-drive` | user | 명시 source를 한 번 준비·승인하고 fresh worker unit·R/AC gap closure·verified commits·finalization까지 진행 |
| `tk-audit` | user | repository를 read-only audit하고 `.tigerkit/audit.md` 에 evidence-backed `AUD-*` finding을 기록 |
| `tk-ask-repo` | user | repository 질문을 `path:line` 근거로 조사하는 read-only desk |
| `tk-grill-me` | hybrid | material user decision을 evidence-first 질문 하나씩 닫음 |
| `tk-pr-open` | hybrid | 명확한 단일 PR 요청으로 초안·publish plan을 작성하고 승인 후 create/update |
| `tk-pr-respond` | hybrid | 단일 PR을 한 번 준비·승인하고 fresh-worker resolution unit·acceptance gap closure·bounded publish까지 처리 |
| `tk-pr-rebase` | hybrid | 명시 호출 또는 sweep handoff에서 열린 PR을 최신 base에 rebase하고 bounded force-with-lease·review follow-up publish |
| `tk-pr-sweep` | user | deterministic `--report` 또는 한 번 승인한 multi-PR maintenance batch와 bounded child routes를 소유 |
| `tk-github-image-upload-to-pr` | user | 로컬 evidence image를 인증된 browser session으로 기존 PR 본문이나 요청된 comment에 upload |
| `tk-prototype` | hybrid | 폐기 가능한 UI/logic 비교물을 실행 |
| `tk-browser-verify` | hybrid | 승인된 browser-visible AC를 headless-only로 검증하고 compact evidence를 상위 owner에 반환 |
| `tk-skill-diagnose` | hybrid | 관찰된 Agent Skill incident를 재현·격리하고 verified `learn-ready` objective를 handoff |
| `tk-learn` | hybrid | `create | improve | merge` 를 유일하게 소유하는 repository/user skill 작성자; 승인 전에는 쓰지 않음 |
| `tk-grooming` | hybrid | 기존 repository/user skill의 중복·범위·배치를 감사 |
| `tk-handoff` | hybrid | 현재 evidence 기반 resume snapshot 작성·재개 |
| `tk-merge-conflict` | hybrid | 진행 중인 Git conflict의 의도를 복원하고 operation 완료 |

작은 수정과 일반 후속 피드백은 skill 없이 현재 대화에서 처리합니다. 별도 artifact,
commit, 검증 또는 안전 경계가 있을 때만 해당 skill을 선택합니다.

## 출력 표시

일반적인 standalone skill은 진행 표기를 생략하고, 사용자 응답·외부 대기 또는
긴 작업 경계에서만 선택적으로 표시합니다. 이모지 뒤에는 항상 공백을 둡니다.

| 표기 | 의미 |
| --- | --- |
| `🤹 진행` | 의미 있는 긴 작업 경계 또는 부모 오케스트레이션 (`🤹 drive > child`) |
| `🙋 응답 필요` | 사용자 질문·승인·조치 필요 |
| `⏳ 대기` | 다음 행동이 CI·원격 작업·재리뷰 대기 |

정상 no-op 행은 생략하고, 표에는 한 번만 범례를 둡니다. PR·review thread 링크는
클릭 가능한 Markdown 링크로 표시하며 GitHub의 `<br>`/`<br/>` 는 TUI용 실제 개행으로
정규화합니다. terminal response에는 progress marker를 넣지 않으며, 최종 결과는
`Status: <token>` 한 줄만 결과 토큰으로 사용합니다.

## PR lifecycle

```text
/tk-pr-open
→ repository·branch·HEAD·기존 PR 확인
→ exact draft와 publish plan
→ current-turn publish approval
→ bounded push + PR create/update

/tk-pr-respond
→ fresh exact-PR evidence와 apply | reply | defer resolution units/waves 준비
→ assumptions·verification·bounded publication을 포함한 한 번의 plan approval
→ unit마다 fresh worker candidate → verifier → R/AC gap closure → verified commit
→ fresh PR validation 뒤 이미 승인된 push·reply·resolve·re-review·summary

/tk-pr-rebase
→ exact PR head와 최신 base SHA 고정
→ local rebase; active conflict만 tk-merge-conflict로 해결
→ verification과 exact force-with-lease·review follow-up plan
→ current-turn approval 뒤 publish
→ post-push review state에 따라 human re-review request

/tk-pr-sweep --report
→ package-local deterministic triage를 read-only 실행

/tk-pr-sweep
→ configured repositories deterministic triage와 actionable/held/report-only batch 준비
→ assumptions·waves·bounded child/publication actions를 포함한 한 번의 plan approval
→ conflict는 tk-pr-rebase --ci, Actions·feedback은 tk-pr-respond --ci
→ nested routes는 competing Markdown ledger 없이 pr-sweep evidence로 반환
→ final deterministic triage와 aggregate R/AC gap result
```

네 skill은 포괄 권한을 공유하지 않습니다. `tk-pr-sweep --report` 는 read-only이고,
`tk-pr-open`, standalone `tk-pr-respond`, standalone `tk-pr-rebase` 는 각자의 exact
plan 승인이 있기 전에는 remote write를 하지 않습니다. 명시적 interactive
`tk-pr-sweep` plan만 fresh exact evidence 안에서 child의 bounded `--ci` route를
한 번 승인합니다.

## `tk-drive`

```text
explicit tk-drive <source>
→ Prepare: Ready R/AC, assumptions, units/waves, verification obligations
→ material blocking decision이 있을 때만 tk-grill-me
→ 한 번의 final plan approval
→ Execute: unit마다 fresh worker candidate
→ required verifier 후 R/AC Close gaps
→ unit마다 verified commit
→ aggregate verification → Finalize
```

`tk-learn`만 `create | improve | merge` skill 변경을 작성합니다.
`tk-skill-diagnose` 는 검증된 목표를 `learn-ready` 로 handoff하고,
`tk-grooming` 은 repository/user skill만 감사하며 rule lifecycle을 소유하지
않습니다. `tk-browser-verify` 는 visible login이나 product source mutation 없이
승인된 AC만 검증합니다. 인증이 필요하면 repository/application 근거가 있는
transient token/session injection을 사용하고, 불가능하면 product mutation 전에
`Unverifiable` 을 반환합니다. Nested verifier는 Markdown ledger를 만들지 않고
상위 owner에 compact facts와 inspected binary evidence path만 반환합니다.

Continuation은 prompt-directed이며 durable scheduler나 cross-turn replay를
보장하지 않습니다. Process 또는 host 경계를 넘으면 `.tigerkit/` artifact,
Git, tests, browser evidence를 다시 읽어 다음 node를 선택합니다.

TigerKit은 이 한계를 문구로 숨기지 않습니다. `scripts/run_drive_experiment.py` 는
동일한 source를 `tk-drive` arm과 ordinary host control arm으로 실행하여 terminal
상태, phase continuation, commit, verification, token/time을 비교합니다. 측정된
명확한 열세가 없으면 catalog에서 `tk-drive` 를 자동 삭제하지 않습니다.

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
동기화 단계는 없습니다. `scripts/validate_skills.py` 는 `skills/tk-*` 를 자동
발견하고 canonical JSON schema, mechanical assertions, host metadata, links,
release-critical references를 직접 검증합니다.

## 로컬 검증

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
node --check skills/tk-pr-sweep/scripts/triage.mjs
node --test skills/tk-pr-sweep/scripts/triage.test.mjs
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

`.tigerkit/` 은 repo/worktree-local scratch이며 영구 project 문서나 전역 상태가
아닙니다. TigerKit은 consumer `.gitignore` 를 수정하지 않습니다.

`tk-learn` 은 reusable skill의 `create | improve | merge` 를 유일하게 소유합니다.
Evidence, dedupe, trigger/eval, baseline/compatibility gate를 먼저 검증하고,
현재 turn의 명시적 apply 승인이 있기 전에는 canonical skill path를 쓰지 않습니다.
`tk-skill-diagnose` 와 `tk-grooming` 은 `tk-learn`용 proposal만 만들며 자동 invoke하지
않습니다.

`tk-drive` 의 명시 호출은 승인된 unit의 문서화된 current-branch commit까지만
허용합니다. Controller는 product change를 직접 작성하지 않고 fresh worker
candidate를 verifier와 R/AC gap closure 뒤 commit합니다. Push, PR, merge, tag,
release, publish는 별도 명시 권한 없이는 수행하지 않습니다.

`tk-pr-sweep --report` 는 repository와 GitHub를 변경하지 않습니다. `tk-pr-open` 은 PR create/update를,
standalone `tk-pr-respond` 는 한 번 승인한 exact plan 안에서 push·reply·verified resolve를,
`tk-pr-rebase` 는 exact lease를 고정한 force-with-lease와 review follow-up만 수행합니다.
interactive `tk-pr-sweep` 는 승인된 batch 안에서 두 one-PR owner의 bounded `--ci` route만
orchestration합니다. 네 mutation skill 모두 merge·tag·release 권한을 갖지 않습니다.

이전 구조에서 갱신한다면 [MIGRATION.md](MIGRATION.md)를 읽으세요.
Attribution은 [NOTICE.md](NOTICE.md)에 보존됩니다.
