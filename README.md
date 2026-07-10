# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/route/reflect cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, route를 고르고, 끝나면 reflect로 남기고, 필요하면 그 자리에서 skill로 굳힌다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현의 차이를 먼저 확인합니다. entrypoint가 헷갈리면 `/tk:help`, 다음 command 하나만 고르고 싶으면 `/tk:next`, 구현 route가 애매하면 `/tk:route`로 direct, subagent-driven, goal-driven 중 어떤 방식이 맞는지 얇게 정리합니다. 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 분류하고 repo-local/user-global guidance에 반영할 수 있습니다. path, URL, 현재 대화, notes, 또는 reflect candidate에서 skill을 바로 만들고 싶으면 `/tk:learn`을 씁니다. 또 구현 전 압박 검증은 `/tk:grill`(사용자가 답을 모른다고 **직접 말할 때만** 후보 최대 3개 제안 가능), guidance 감사/정비는 `/tk:grooming`, throwaway 검증은 `/tk:prototype`, 긴 작업 지도는 `/tk:wayfinder`, 구조 리뷰는 `/tk:arch-review`, 충돌 해결은 `/tk:merge-conflict`, 세션 인계는 `/tk:handoff`, 저장된 handoff 재호출은 `/tk:handon`, draft 요구 문서화는 `/tk:to-prd`, draft issue 분해는 `/tk:to-issues`, merge 전 이해도 게이트는 `/tk:quiz`로 다룹니다. browser-verify 엔진은 번들 skill로 유지하고, `/tk:browser-verify`는 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile을 읽는 direct QA / behavior verification surface입니다.

```text
Check the gap. Pick the route. Keep the learning. Materialize durable skills from reflect when needed.
```

## Start here

처음에는 아래 4개만 알면 됩니다.

1. `/tk:help` — 지금 어떤 command부터 열어야 할지 찾습니다.
2. `/tk:gap` — SoT와 현재 구현의 차이를 먼저 봅니다.
3. `/tk:route` — direct / subagent-driven / goal-driven 중 어떤 구현 경로가 맞는지 고릅니다.
4. `/tk:reflect` — 끝난 뒤 재사용 가능한 learning을 남깁니다.

이후에는 필요할 때만 나머지 surface를 꺼내 쓰면 됩니다.

- Practical: `/tk:grill`, `/tk:grooming`, `/tk:prototype`, `/tk:browser-verify`, `/tk:arch-review`, `/tk:merge-conflict`, `/tk:quiz`, `/tk:wayfinder`
- Output / navigation: `/tk:handoff`, `/tk:handon`, `/tk:to-prd`, `/tk:to-issues`, `/tk:next`

## Installation

Claude Code에서 TigerKit marketplace를 등록한 뒤 `tk` plugin을 설치합니다.

```bash
claude plugin marketplace add MTGVim/tiger-kit
claude plugin install tk@tiger-kit --scope user
```

설치 여부와 사용 가능한 명령을 확인합니다.

```bash
claude plugin list --available --json
claude plugin details tk
```

설치 후 Claude Code를 다시 시작하고 `/tk:help`, `/tk:gap`, `/tk:route`, `/tk:next`, `/tk:quiz`, `/tk:reflect`, `/tk:learn`, `/tk:browser-verify`, `/tk:grill`, `/tk:grooming`, `/tk:prototype`, `/tk:wayfinder`, `/tk:arch-review`, `/tk:merge-conflict`, `/tk:handoff`, `/tk:handon`, `/tk:to-prd`, `/tk:to-issues` 명령을 사용합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없다고 바로 중단하지는 않습니다. blindspot pass가 더 맞는 경우에는 unknown unknowns를 질문 목록으로 바꿔 discovery를 돕습니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 direct, subagent-driven, goal-driven 같은 구현 경로를 비교합니다.
- `/tk:reflect`는 교훈을 canonical target으로 분류합니다. `repo-local`과 `user-global`은 기본 apply(opt-out)로 반영할 수 있고, 명시적 skill materialize는 `/tk:learn` authoring pipeline으로 위임합니다. 실패 유형을 먼저 `discipline_failure | wrong_shaped_output | missing_evidence | source_ambiguity`로 분류하고, stdout Reason은 2~3줄 compact evidence pointer만 남깁니다.
- `/tk:learn`은 path, URL, 현재 대화, notes, 또는 reflect candidate를 source로 받아 reusable skill을 직접 만들고, `skill only` 경계로 user skill surface에만 씁니다. skill 완료 판정은 `RED → GREEN → REFACTOR` evidence와 `pos3 / neg2 / owner` eval coverage를 함께 요구합니다.
- `/tk:grill`은 계획/설계/RFC를 수렴형 질문으로 압박 검증하고, 사용자가 답을 모른다고 **직접 말할 때만** 후보를 최대 3개까지 제안할 수 있습니다.
- `/tk:grooming`은 guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 직접 반영하며 나머지는 suggestion-only로 남깁니다. `guidanceBudgetBytes`와 raw byte footprint를 같이 보고, archive/demotion은 승인 전까지 suggestion-only 입니다.
- `/tk:prototype`은 UI 또는 logic/state 가설을 throwaway prototype으로 빨리 검증합니다.
- `/tk:wayfinder`는 긴 작업의 shared map과 재개 힌트를 worktree-scoped file-only state로 남깁니다. compaction 직전 자동 handoff가 필요하면 `scripts/install-precompact-hook.sh`로 opt-in hook을 설치합니다.
- `/tk:arch-review`는 반복 마찰, 경계 붕괴, ownership 혼선 같은 구조 문제를 report-only로 검토합니다.
- `/tk:merge-conflict`는 merge/rebase conflict를 ours/theirs intent 기준으로 해결합니다.
- `/tk:handoff`는 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다.
- `/tk:handon`은 현재 repo/worktree의 저장된 handoff를 다시 읽습니다.
- `/tk:to-prd`는 현재 대화나 요구사항을 draft-only PRD로 정리합니다.
- `/tk:to-issues`는 plan/PRD를 vertical-slice issue draft로 분해합니다.
- `/tk:browser-verify`는 번들된 browser-verify 엔진 skill을 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile과 함께 사용하는 direct QA / behavior verification surface입니다.

## Command Surface

### Core

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. | optional external generated report + gap packet |
| `/tk:route` | 지금 이 task를 direct, subagent-driven, goal-driven 중 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | 세션 결과와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류하고, repo-local/user-global guidance 기본 apply와 명시적 skill materialize를 처리합니다. | machine-readable reflect ledger + compact summary |
| `/tk:learn` | path, URL, 현재 대화, notes, 또는 reflect candidate에서 reusable skill을 직접 만듭니다. | skill draft / user skill source |

### Practical

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:grill` | 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증하고, 사용자가 답을 모른다고 **직접 말할 때만** 후보를 최대 3개까지 제안할 수 있습니다. | inline questioning + compact summary |
| `/tk:grooming` | guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 직접 반영하며 나머지는 suggestion-only로 남깁니다. | guidance audit + compact summary |
| `/tk:prototype` | UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증합니다. | prototype files + compact summary |
| `/tk:wayfinder` | 긴 작업의 shared map과 reopen hint를 current-first artifact로 정리합니다. | worktree-scoped wayfinder map under repo-scoped `~/.tigerkit` root |
| `/tk:arch-review` | 경계, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only 구조 리뷰입니다. | inline architecture review |
| `/tk:merge-conflict` | merge/rebase conflict를 상태 확인 → intent 추적 → 검증 순서로 해결합니다. | conflict resolution summary |
| `/tk:browser-verify` | 번들된 browser-verify 엔진 skill을 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile과 함께 사용하는 direct QA / behavior verification surface입니다. | direct QA summary |

### Output

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:handoff` | 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다. | worktree-scoped handoff artifact under repo-scoped `~/.tigerkit` root |
| `/tk:handon` | 현재 repo/worktree의 최신 handoff draft를 다시 읽습니다. | read-only current handoff reopen under repo-scoped `~/.tigerkit` root |
| `/tk:to-prd` | 현재 대화나 요구사항을 draft-only PRD로 정리합니다. | worktree-scoped PRD draft under repo-scoped `~/.tigerkit` root |
| `/tk:to-issues` | plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다. | worktree-scoped issue draft set under repo-scoped `~/.tigerkit` root |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:next "이제 뭐부터 해야 하는지 1개만 골라줘"
/tk:wayfinder "issue 164 긴 작업 지도 갱신해줘"
/tk:reflect --target repo-local
/tk:learn "우리가 방금 한 작업"
/tk:reflect --target repo-local --apply=false
/tk:reflect R3 --target skill --apply=true
/tk:grill "이 RFC 허점 짚어줘"
/tk:grooming --scope all
/tk:prototype "이 모달 상태 전이를 빠르게 검증해줘" --logic
/tk:quiz "머지 전 이해도 점검해줘"
/tk:arch-review "이 모듈 경계가 왜 자꾸 새는지 검토해줘"
/tk:merge-conflict
/tk:handoff "issue 138 skill-first rollout 상태 넘겨줘"
/tk:handon "남은 작업만 짧게"
/tk:to-prd "이 요구를 PRD draft로 정리해줘"
/tk:to-issues "이 PRD를 issue draft로 쪼개줘"
/tk:reflect --target skill --apply=true --desc "이 CDP 검증 루틴을 skill로 굳혀줘"
/tk:browser-verify
/tk:browser-verify "QA와 로컬 화면 비교"
```

## Reflect write boundary

`/tk:reflect`가 기본적으로 파일을 쓸 수 있는 직접 대상은 지원 host의 repo-local/user-global guidance surface입니다.

- repo-local: eligibility를 통과한 `<git-root>/CLAUDE.local.md`
- user-global (Claude Code 계열): `~/.claude/CLAUDE.md` 또는 `~/.claude/rules/<rule-name>/CLAUDE.md`
- user-global (non-CLAUDE.md agent): host-native user-global guidance surface

- repo shared `CLAUDE.md`: suggest-only
- user-global guidance: supported host에서는 기본 apply(opt-out)
- skill: suggest-only from reflect, explicit materialize는 `/tk:learn` pipeline으로 처리
- hook: suggest-only
- command: suggest-only
- agent: suggest-only
- discard: no write

`PROFILE.md`, `automation`, `hookify`는 promotion target 이름이 아닙니다. Claude Code auto memory는 TigerKit이 쓰거나, mirror하거나, backup하지 않습니다.

## Reflect skill-materialize scope

`/tk:reflect --target skill --apply=true`는 1차에서 `skill only`를 실제 생성하며, skill authoring은 `/tk:learn` pipeline으로 위임합니다.

- same-session + same-ledger `candidate_id`만 읽습니다.
- reflect candidate는 chat prose가 아니라 ledger를 source of truth로 읽습니다.
- 이름은 제안할 수 있지만 생성 전 사용자 확정이 필요합니다.
- 생성 target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- `hook|command|agent`는 아직 reflect 제안 target으로만 남고 source를 직접 생성하지 않습니다.

## Learn surface

`/tk:learn`은 source-to-skill surface입니다.

- direct source: path / directory / URL / 현재 대화 / notes
- reflect source: same-session + same-ledger `candidate_id`
- 기본은 preview-only 입니다.
- explicit apply일 때만 user skill surface에 write합니다.
- `repo-local`, `user-global`, `hook`, `command`, `agent`로 라우팅하지 않습니다.

## Browser Verify surface

`/tk:browser-verify`는 프로비저닝 command가 아니라 direct QA / behavior verification surface입니다.

- engine은 repo에 번들된 `skills/browser-verify/` 기준 지식을 사용합니다.
- profile은 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/`만 읽습니다.
- 신 profile이 없고 legacy `~/.tigerkit/repos/<repo-key>/ui-diff/`가 남아 있으면 자동 migration 대신 migration guide로 멈춥니다.
- 둘 다 없으면 bundled template 기준으로 `~/.tigerkit/repos/<repo-key>/browser-verify/` 신규 생성 절차로 들어가고 missing 파일만 만듭니다.
- `login.local.md`는 tracked repo 밖 `~/.tigerkit` 아래에 두는 local override입니다.
## Operational Docs

- [Workflow matrix](docs/workflow-matrix.md)
- [Operator follow-ons](docs/operator-environment-followons.md)
- [Usage](.tigerkit/docs/usage.md)
- [Output Contract](.tigerkit/docs/output-contract.md)
- [Storage boundary](.tigerkit/docs/storage-boundary.md)
- [Browser Verify migration guide](.tigerkit/docs/browser-verify-migration.md)
- [FULL eval pilots](.tigerkit/docs/full-eval-pilots.md)
- [Gap→Route evidence packets](.tigerkit/docs/gap-route-evidence-packets.md)
- [Reflect→Learn evidence handoff](.tigerkit/docs/reflect-learn-evidence-handoff.md)
- [Promotion statuses](.tigerkit/docs/promotion-statuses.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [Reflect promotion helper guide](.tigerkit/docs/reflect-promotion-helpers.md)

## Generated State

Active generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다.

- `/tk:gap` report:
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/...`
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.packet.json`
- `/tk:reflect` ledger:
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml`
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml`
- `/tk:handoff` draft:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md`
- `/tk:handon` read target:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md`
- `/tk:to-prd` draft:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md`
- `/tk:to-issues` draft:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/issues/current.md`
- decision ledger draft:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/ledger/current.md`
- `/tk:quiz` draft:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/quiz/current.md`
- `/tk:wayfinder` map:
  - `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/wayfinder/current.md`
- `/tk:browser-verify` profile:
  - `~/.tigerkit/repos/<repo-key>/browser-verify/env.md`
  - `~/.tigerkit/repos/<repo-key>/browser-verify/login.md`
  - `~/.tigerkit/repos/<repo-key>/browser-verify/login.local.md`
  - `~/.tigerkit/repos/<repo-key>/browser-verify/screens/README.md`
- `/tk:route`는 기본적으로 persisted artifact를 만들지 않습니다.
- `/tk:browser-verify`는 repo-scoped profile을 `~/.tigerkit` 아래에서 읽고, legacy profile이 있으면 migration guide를 출력하며, 둘 다 없을 때만 missing 파일을 bootstrap할 수 있습니다.

`/tk:handoff`, `/tk:handon`, `/tk:to-prd`, `/tk:to-issues`는 repo 내부 `.claude/tigerkit/`가 아니라 `~/.tigerkit` 아래 worktree-scoped current-first draft 구조를 사용합니다. `/tk:handoff`는 그 경로에 기록하고, `/tk:handon`은 같은 current handoff를 다시 읽습니다. `.claude/` 전체를 ignore하지 않습니다.

## Contributors

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MTGVim"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="Taekwon Yoo"/><br /><sub><b>Taekwon Yoo</b></sub></a><br /><a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Code">💻</a> <a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Documentation">📖</a> <a href="#ideas-MTGVim" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org/) specification. Contributions of any kind are welcome.
