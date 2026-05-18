---
name: tigerkit-review
description: TigerKit command, docs, evals, artifacts, or implementation changes를 adversarial하게 검토해 source-loss, reuse-rule, baseline, Decision Gate, handoff/reflect contract 위반을 잡습니다. TigerKit 변경 리뷰, /tk:* command contract 검토, gap/prep/checkpoint/reflect/handoff 산출물 검토, 재사용 탐사 누락, compliance review, adversarial reviewer 요청이 나오면 반드시 사용합니다.
---

# TigerKit Adversarial Review

TigerKit review는 구현자가 놓친 contract drift를 잡는 적대적 검토입니다. 특히 새 component/hook/util/mapper/API client/layout primitive/UI pattern을 만들거나 공통 모듈을 수정한 작업에서 reuse exploration 누락을 high-priority finding으로 봅니다.

## 원칙

- 리뷰만 합니다. 수정, commit, push, PR 생성은 하지 않습니다.
- evidence 없는 확신을 쓰지 않습니다. file path, excerpt, observed diff, artifact path, user confirmation 중 하나로 근거를 댑니다.
- finding은 actionable해야 합니다. 위치, 위반한 규칙, evidence, 필요한 수정 기준을 함께 씁니다.
- 문제가 없으면 정확히 `NO_FINDINGS`를 출력합니다.
- 사소한 취향, 문체 선호, unrelated cleanup은 finding으로 만들지 않습니다.

## 검토 입력

가능한 범위에서 아래를 확인합니다.

1. 현재 사용자 요청과 명시적 결정
2. relevant diff 또는 changed files
3. `.claude-plugin/plugin.json`
4. `commands/*.md`
5. `README.md`, `docs/usage.md`, `docs/output-contract.md`, `docs/artifact-layout.md`
6. `evals/evals.json`
7. branch-local TigerKit artifacts if task is artifact review
8. `CLAUDE.md`, `DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `COMPONENT_REUSE_MAP.md` if mentioned or modified
9. `reuse-map.md` only as legacy alias/migration candidate if mentioned or modified

## Finding severity

- `Critical`: source loss, inaccessible SOT 추측, protected branch/root artifact write, implementation/commit/push side effect 같은 core contract 위반
- `High`: reuse exploration 누락, common module impact analysis 누락, user approval 없는 risky decision, docs/manifest/evals command drift
- `Medium`: receipt/output contract 불일치, ambiguity/resolvability 분류 누락, handoff freshness 확인 부족
- `Low`: 혼동을 부르는 wording, minor eval coverage gap, non-blocking documentation inconsistency

## Review checklist

### 1. Source preservation

- 외부 source를 local requirement로 복사, 요약, 정규화, 재작성했는지 확인합니다.
- branch-local `requirements.md`가 SOT 본문이 아니라 reference index로 남았는지 확인합니다.
- direct user interview raw text와 derived interpretation이 분리됐는지 확인합니다.
- source가 결론을 지지하지 않는데 fact나 decision처럼 저장했는지 확인합니다.

### 2. Branch-local artifact and baseline

- write command가 detached HEAD, `main`, `master`, `develop`에서 branch-local artifact를 쓰지 않는지 확인합니다.
- `/tk:gap`이 clean HEAD + commit hash만 baseline으로 쓰는지 확인합니다.
- staged, unstaged, untracked diff를 baseline evidence처럼 다루지 않는지 확인합니다.
- root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`를 active target으로 쓰지 않는지 확인합니다.

### 3. Gap contract

- gap이 SOT reference vs code baseline comparison record인지 확인합니다.
- gap을 실행 queue, task plan, implementation checklist로 바꾸지 않았는지 확인합니다.
- evidence, finding, interpretation, decision, suggestion이 분리됐는지 확인합니다.
- severity와 resolvability가 섞이지 않았는지 확인합니다.
- external dependency를 locally fixable처럼 표현하지 않았는지 확인합니다.

### 4. Decision Gate

- high-impact ambiguity, inaccessible SOT, SOT conflict, user decision, external dependency, broad/risky refactor가 `/tk:checkpoint` 대상인지 확인합니다.
- inaccessible SOT 내용을 추측하거나 dependent item을 evidence 없이 `Match`로 표시했는지 확인합니다.
- SOT accessibility validation 없이 URL/image/Figma/local path를 inspected source처럼 다뤘는지 확인합니다.
- pending SOT entry와 accessible fallback request가 누락됐는지 확인합니다.
- binding visual SOT에 stable local asset reference(`./docs/assets/sot/...`)를 선호하는지 확인합니다.
- 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `docs/assets/sot/`를 단일 `SOT.md`로 합쳤는지 확인합니다.
- `IMPLEMENTATION_POLICY.md`가 있으면 binding project policy SOT candidate로 다뤘는지 확인합니다.
- `COMPONENT_REUSE_MAP.md`를 target repo가 명시적으로 SOT로 정의하지 않았는데 external SOT처럼 다뤘는지 확인합니다.
- checkpoint final status가 `CLEAR`, `PROCEED_WITH_ASSUMPTIONS`, `PAUSE_FOR_USER_DECISION`, `BLOCKED_BY_ACCESS`, `NEED_VERIFICATION` 중 하나인지 확인합니다.
- low-risk trivial detail마다 불필요하게 pause를 만들었는지 확인합니다.
- `/tk:gap`이 `SOT Access Coverage`를 누락했는지 확인합니다.
- inaccessible binding SOT가 있는데 audit partial statement가 누락됐는지 확인합니다.
- pending fallback이 필요한데 자연어 fallback 요청이 빠졌는지 확인합니다.

### 5. Reuse and common module discipline

Reuse omission은 TigerKit review의 high-priority target입니다.

- `COMPONENT_REUSE_MAP.md` hit을 review candidate로만 다뤘는지 확인합니다.
- `COMPONENT_REUSE_MAP.md` miss를 reusable module 없음의 evidence로 사용했는지 확인합니다.
- `reuse-map.md`를 legacy alias/migration candidate 외 용도로 사용했는지 확인합니다.
- 새 component/hook/util/mapper/API client/layout primitive/UI pattern 생성 전 repo-wide exploration이 있었는지 확인합니다.
- exploration에 file inventory, source root/package/domain structure, keyword search, import/export search, naming search, candidate file inspection, callsite inspection이 포함됐는지 확인합니다.
- explored scope, excluded scope, exclusion reason, shared package/design system/common module 포함 여부가 기록됐는지 확인합니다.
- existing candidate를 배제한 근거와 새 모듈 대신 가능한 대안이 기록됐는지 확인합니다.
- common module 수정 전 repo-wide callsite impact analysis와 explicit user approval이 있었는지 확인합니다.

### 6. Reflection and durable artifacts

- `/tk:reflect`가 현재 대화 context를 primary source로 썼는지 확인합니다.
- `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `COMPONENT_REUSE_MAP.md` 수정이 user approval 전 적용됐는지 확인합니다.
- `DESIGN.md`가 없을 때 TigerKit이 새로 만들었는지 확인합니다.
- inspect하지 않은 reusable capability, prop, API field, behavior를 기록했는지 확인합니다.
- `/tk:reflect`를 default next command로 추천했는지 확인합니다.

### 7. Handoff contract

- `/tk:handoff-write`가 continuation contract이지 task queue가 아닌지 확인합니다.
- branch/HEAD, artifact map, open/resolved gap, ambiguity, not-confirmed item, next safe action, do-not-do가 분리됐는지 확인합니다.
- `/tk:handoff-read`가 handoff를 맹신하지 않고 current branch/HEAD/artifact freshness를 확인하는지 확인합니다.

### 8. Command surface sync

- `.claude-plugin/plugin.json` command list, README command table, docs/usage command table, output contract, eval fixture가 같은 command surface를 말하는지 확인합니다.
- command 추가/변경 시 plugin version patch bump가 되었는지 확인합니다.
- `evals/evals.json`이 JSON 문법상 유효하고 새 behavior를 대표하는 fixture를 포함하는지 확인합니다.

### 9. Output contract

- chat output이 artifact dump가 아니라 receipt인지 확인합니다.
- receipt가 outcome, evidence/risk/ambiguity, artifact paths, next action/required confirmation에 집중하는지 확인합니다.
- `recorded only`, `applied`, `pending escalation`, `skipped`가 섞이지 않았는지 확인합니다.

## 출력 형식

Finding이 있으면 아래 형식을 씁니다.

```md
FINDINGS

1. [Severity] 짧은 제목
- 위치: `path:line` 또는 artifact path
- 규칙: 위반한 TigerKit rule
- evidence: 직접 확인한 근거
- 영향: source loss, reuse drift, baseline unreproducibility 등 실제 위험
- 필요한 수정: 완료 기준
```

Finding이 없으면 아래 한 줄만 씁니다.

```text
NO_FINDINGS
```
