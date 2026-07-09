# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 sibling command surface 전체에서 일관되게 씁니다.
- 같은 역할의 label naming은 괜히 갈라지지 않게 맞춥니다. 현재 canonical next-action label은 `▶️ Next step:`입니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path 또는 ledger path를 출력합니다.
- Active command surface는 `/tk:gap`, `/tk:route`, `/tk:reflect`, `/tk:learn`, `/tk:grill`, `/tk:grooming`, `/tk:prototype`, `/tk:arch-review`, `/tk:merge-conflict`, `/tk:handoff`, `/tk:to-prd`, `/tk:to-issues`, `/tk:browser-verify`입니다.
- 기본 projection은 compact합니다. empty section, default empty list, `NONE` line은 의미 보존에 필요할 때만 출력합니다.
- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- compact를 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.

## `/tk:gap` Output Contract

`/tk:gap`은 SoT와 Current Implementation의 one-shot gap analysis입니다.

```md
## 📊 Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## 🔎 Findings

### 1. <finding title>
- SoT:
- Current:
- 🔎 Evidence:
- 🧪 Evidence type:
- 📉 Impact:
- 🚦 Priority:
- 🛠️ Suggested fix:
- 🧭 Route: direct | brainstorm | decision
- 🔎 Route evidence:

## ❓ Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## 🧹 Not accepted summary

- <optional low-priority or rejected note>

## ▶️ Recommended Next Steps

1. <next step>
```

Artifact path가 필요하면 repo 밖 `~/.tigerkit/.../gap/` 아래에 둡니다.

같은 gap run의 machine-readable handoff가 필요하면 `current.packet.json`을 함께 둘 수 있습니다. schema는 `tigerkit.gap-packet/v1`이며, `source_refs`, `precedence`, `findings`, `unresolved_questions`를 담아 `/tk:route`가 same repo/scope `gap packet`을 재사용할 수 있게 합니다.

## `/tk:route` Output Contract

`/tk:route`는 inline-only decision / brainstorming surface입니다.

```text
🧭 Route: <direct|subagent-driven|goal-driven|decision|need-sot>
📶 Confidence: high | medium | low
📝 Why:
- <reason>

⚖️ Tradeoffs:
- <route>: <pros / cons>

🧩 Needs first:
- <missing info>

▶️ First step:
- <one concrete next step>
[👥 Delegation plan:
- 🧱 Architect: <goal / constraints / files / acceptance criteria / risks>
- 🛠️ Implementor context: <narrow implementation brief only; no redesign or scope expansion>
- 🧪 Reviewer context: <diff + acceptance criteria only; assume the patch is wrong>
- ✅ Verification: <smallest relevant checks>]
[🚀 Goal command:
- </goal <recommended goal>>]
```

missing info가 없으면 `Needs first` section은 생략합니다. `subagent-driven`이 역할/문맥 분리 때문에 선택된 경우에는 `Delegation plan` section을 추가할 수 있습니다. 이 section은 추천된 역할 분리를 설명하는 것이지, command 자체를 workflow executor로 바꾸지는 않습니다. `goal-driven`이 선택되고 host가 `/goal` surface를 지원할 때만 `Goal command` section을 추가할 수 있습니다. 이 section은 ready-to-run recommendation이며, 특정 host command 존재 자체를 증명하지는 않습니다.

same repo/scope `gap packet`이 있으면 `/tk:route`는 그 packet의 source set, precedence, ambiguity, evidence type을 먼저 읽고 route 판단 근거로 재사용할 수 있습니다. packet이 없거나 stale하면 기존 read-only route 판단으로 fallback 합니다.

기본적으로 persisted artifact를 만들지 않습니다.

## `/tk:learn` Output Contract

`/tk:learn`은 direct source 또는 reflect candidate에서 reusable skill을 직접 만듭니다.

```text
Learn 완료 | Learn 미리보기 | Learn 중단
🧾 Input:
- <source or candidate_id>
🧭 Source mode:
- direct | reflect-candidate
🛠️ Apply:
- preview | explicit
🏷️ Suggested name:
- <slug>
[✅ Confirmed name:
- <slug>]
🎯 Target:
- user skill surface only
[📁 Created path:
- <path>]
[✍️ Write result:
- preview only | name confirmation needed]
▶️ Next step:
- <review skill | confirm name | apply explicitly | patch source>
```

Notes:
- 기본은 preview-only 입니다.
- `--apply=true`일 때만 user skill surface write를 허용합니다.
- `--from-reflect <candidate_id>`는 same-session + same-ledger candidate만 읽습니다.
- reflect candidate를 읽을 때는 ledger를 source of truth로 삼습니다.
- helper surface가 있으면 `read-reflect-candidate`로 current ledger candidate를 읽을 수 있지만, same-session + same-ledger boundary는 계속 유지됩니다.
- `/tk:learn`은 `repo-local`, `user-global`, `hook`, `command`, `agent` direct write를 하지 않습니다.

## `/tk:reflect` Output Contract

`/tk:reflect`는 reusable learning을 canonical target으로 분류하고, repo-local/user-global guidance는 기본 apply(opt-out)로 반영할 수 있습니다.

### Apply semantics

- option 생략: 기본 apply
- `--apply=false`: preview-only
- `--apply=true`: 명시적 apply 표기용
- 기본 apply 대상: `repo-local`, `user-global`
- explicit materialize 대상: `skill`
- `user-global` direct write는 writable host-native surface를 exact resolve할 수 있을 때만 허용합니다.

### stdout projection

```text
Reflect 완료
🧾 Requested target:
- <raw requested target or default>
🎯 Effective targets:
- <canonical target list>
[🧭 Target modes:
- repo-local, user-global: direct-apply candidate
- skill: explicit materialize only
- repo-shared, hook, command, agent: suggest-only]
📝 Summary:
- <what changed or what was proposed>
🗂️ Ledger:
- <absolute ledger path>
[✅ Applied candidates:
- <candidate ids or NONE>]
[🧩 Reason code:
- <reason_code or NONE>]
[📁 Changed paths:
- <path>]
[↩️ Rollback:
- <succeeded | failed | not_needed>]
[▶️ Next step:
- <next step>]
```

Notes:
- receipt는 target boundary를 compact하게 드러내야 합니다.
- reject/failure는 silent skip이 아니라 `reason_code` 또는 동등한 reject 이유를 노출해야 합니다.
- verification failure와 rollback failure는 서로 다른 상태로 보여야 합니다.

### Ledger contract

reflect는 machine-readable ledger + compact human summary를 남깁니다.

권장 path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

ledger는 최소한 아래를 포함합니다.

```yaml
schemaVersion: tigerkit.reflect-ledger/v1
invocation_id: <id>
requested_target: <raw target>
effective_targets: [repo-local, user-global, skill]
summary:
  - <compact bullet>
ledger_path: <absolute path>
candidates:
  - candidate_id: R1
    status: candidate | confirmed | deprecated
    duplicate_status: confirmed | unknown
    action: apply | preview_only | suggest_only | discard
    target: repo-local | repo-shared | user-global | skill | hook | command | agent | discard
    path: <path or NONE>
    evidence: <direct observed evidence>
    reason: <routing reason>
apply_plan: <optional exact plan object>
```

exact `apply_plan`은 stdout이 아니라 ledger에 둡니다. `repo-local`과 `user-global` direct write 모두 `target_path`, `base_state`, `base_sha256`, `result_sha256`, `planned_result_bytes_sha256`, `unified_diff`를 포함해야 합니다.

### skill materialize mode

`/tk:reflect --target skill --apply=true`는 reflect가 제안한 candidate를 `/tk:learn` authoring pipeline으로 넘겨 실제 artifact를 생성합니다. 1차 범위는 `skill only`입니다.

```text
Reflect 완료 | Reflect 미리보기 | Reflect 중단
🧾 Requested target:
- skill
🛠️ Apply:
- explicit
🧾 Input:
- <candidate_id or --desc>
🏷️ Suggested name:
- <slug>
[✅ Confirmed name:
- <slug>]
🗂️ Ledger:
- <reflect ledger path>
[📁 Created path:
- <path>]
[✍️ Write result:
- preview only | name confirmation needed]
[▶️ Next step:
- <rename/remove/follow-up>]
```

Rules:
- `candidate_id`는 same-session + same-ledger만 유효합니다.
- skill source 생성은 explicit apply일 때만 허용합니다.
- reflect candidate는 `/tk:learn`이 ledger를 source of truth로 읽어 마무리합니다.
- helper surface가 있으면 `/tk:learn`은 `read-reflect-candidate`로 current ledger candidate를 읽을 수 있습니다.
- 생성 target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- 이름 확정 전 write 금지
- `--dry-run`은 preview only입니다.
- 상세 preview/diff는 별도 ledger 또는 generated preview file로 둘 수 있습니다.

## `/tk:grill` Output Contract

`/tk:grill`은 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증하고, 사용자가 답을 모른다고 직접 말할 때만 후보를 최대 3개까지 제안할 수 있습니다.

```text
Grill 진행중 | Grill 중단 | Grill 요약
❓ Question:
- <one sharp question>
[💡 Candidate suggestions:
- <up to 3 candidate answers when the user says they do not know>]
📝 Why:
- <why this matters>
📌 Confirmed facts:
- <confirmed facts>
🧠 Decision summary:
- <decisions>
📎 Assumptions:
- <assumptions>
⚠️ Risks:
- <remaining risks>
▶️ Next step:
- <continue questioning | proceed with assumptions | stop>
```

## `/tk:grooming` Output Contract

`/tk:grooming`은 guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 direct apply하며 나머지는 suggestion-only로 남깁니다.

```text
Grooming 리포트 | Grooming 적용 완료 | Grooming 중단
📍 Scope:
- user | repo | all
🧭 Mode:
- report-only | preview-only mixed-scope | user-global direct-apply | suggestion-only
🔎 Findings:
- <confirmed drift summary>
[🎯 Direct apply target:
- <user-global path>]
[✅ Applied changes:
- <what changed>]
[💡 Suggested changes:
- <repo/user suggestions kept as suggestion-only>]
[🛡️ Protected exclusions:
- <reported-only exclusions>]
✅ Verification:
- <readback / re-grep / preview reason>
▶️ Next step:
- <approve apply | review suggestions | rerun with narrower scope>
```

## `/tk:prototype` Output Contract

`/tk:prototype`은 UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증합니다.

```text
Prototype 준비 | Prototype 완료 | Prototype 중단
🧭 Mode: ui | logic
🎯 Goal:
- <what is being tested>
[📁 Created files:
- <prototype files>]
✅ Confirmed:
- <what the prototype proved>
🎭 Still fake:
- <what is mocked or assumed>
▶️ Next production step:
- <what to port, delete, or refine>
```

## `/tk:arch-review` Output Contract

`/tk:arch-review`는 boundary, ownership, coupling, repeated pain을 evidence-first로 검토하는 report-only 구조 리뷰입니다.

```text
Arch Review 완료 | Arch Review 중단
📍 Scope:
- <target area>
💪 Strengths:
- <what is already clean>
🔥 Hotspots:
- <confirmed architectural hotspots>
⚠️ Boundary risks:
- <where ownership/coupling leaks>
🔎 Evidence:
- <file / behavior / repeated pain evidence>
🧭 Suggested direction:
- <smallest safe architectural direction>
▶️ First step:
- <one concrete next step>
```

## `/tk:merge-conflict` Output Contract

`/tk:merge-conflict`는 merge/rebase conflict를 상태 확인 → intent 추적 → 검증 순서로 해결합니다.

```text
Merge conflict 분석 | Merge conflict 해결 | Merge conflict 중단
📍 State:
- <merge|rebase|no-active-merge-state>
📄 Conflict files:
- <file list>
🧩 Hunks:
- <summary>
🛠️ Resolution:
- <how each intent was reconciled>
✅ Verification:
- <commands run and result>
▶️ Next step:
- <continue merge/rebase | manual follow-up>
```

## `/tk:handoff` Output Contract

`/tk:handoff`는 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 worktree-scoped current-first handoff를 repo-scoped `~/.tigerkit` root 아래에 만듭니다.

```text
Handoff 완료 | Handoff 미리보기 | Handoff 중단
🎯 Goal:
- <one-line goal>
📤 Output mode:
- draft file | inline preview
[📁 Output path:
- <path>]
📦 Includes:
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context
✅ Verification:
- <verified / partially verified / unverified>
▶️ Next step:
- <what the next agent should do first>
```

## `/tk:to-prd` Output Contract

`/tk:to-prd`는 현재 대화나 요구사항을 draft-only PRD로 정리합니다.

```text
To-PRD 완료 | To-PRD 미리보기 | To-PRD 중단
🎯 Goal:
- <what the PRD covers>
📤 Output mode:
- draft file | inline preview
[📁 Output path:
- <path>]
📦 Includes:
- problem / goal / user value / non-goals / requirements / acceptance criteria / risks / open questions
📣 Publish:
- disabled by default
▶️ Next step:
- <review draft | convert to issues | revise scope>
```

## `/tk:to-issues` Output Contract

`/tk:to-issues`는 plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다.

```text
To-Issues 완료 | To-Issues 미리보기 | To-Issues 중단
📌 Source:
- <plan|prd|scope>
📤 Output mode:
- draft file | inline preview
[📁 Output path:
- <path>]
🔢 Issue count:
- <N>
📏 Rules applied:
- vertical slice only
- no layer slicing
- draft-only by default
⛓️ Dependencies:
- <blocked-by summary>
📣 Publish:
- disabled by default
▶️ Next step:
- <review drafts | revise slicing | publish explicitly>
```

## `/tk:browser-verify` Output Contract

`/tk:browser-verify`는 provisioning command가 아니라 direct QA / behavior verification surface입니다.

```text
Browser Verify 준비 완료 | Browser Verify 프로필 생성 완료 | Browser Verify 프로필 템플릿 출력 | Browser Verify migration guide
🧭 Mode: env-diff | figma-diff | behavior-verify
[📁 Profile path:
- <path>]
[🗃️ Legacy profile path:
- <path>]
[📁 Created files:
- <path>]
[✍️ Write result:
- existing profile reused | profile files created | template only | blocked by legacy profile]
[🧭 Migration guide:
- <move legacy ui-diff profile to browser-verify path and rerun>]
🧠 Engine skill:
- skills/browser-verify/SKILL.md
▶️ Next step:
- <run verify / fill env-login-screen values / migrate profile and rerun>
```

Rules:
- current repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile만 읽습니다.
- 신 profile이 없고 legacy `~/.tigerkit/repos/<repo-key>/ui-diff/`가 있으면 migration guide를 출력하고 멈춥니다.
- 둘 다 없을 때만 같은 repo-scoped 경로에 missing 파일을 생성합니다.
- bundled template source는 `skills/browser-verify/templates/`입니다.
- `--print-profile-template`가 있으면 템플릿 내용을 preview만 하고 write는 하지 않습니다.
- `login.local.md`는 tracked repo 밖 `~/.tigerkit` 아래에 두는 local override입니다.
- engine install/update나 user-global provisioning mode는 없습니다.
