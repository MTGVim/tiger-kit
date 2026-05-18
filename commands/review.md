---
description: TigerKit command, docs, evals, artifacts, implementation change를 adversarial하게 검토해 source-loss, reuse exploration, baseline, Decision Gate, handoff/reflect contract 위반을 찾는 artifact-free review입니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `/tk:review`는 TigerKit 준수룰 전체를 적대적으로 검토합니다. 재사용 탐사 누락은 high-priority finding으로 다루지만, review 범위는 source preservation, branch-local artifact, reproducible baseline, gap contract, Decision Gate, reflection, handoff, docs/evals/manifest sync까지 포함합니다.

```text
review = TigerKit compliance check, not implementation
```

## 기본 산출물

- 없음

`/tk:review`는 chat review만 출력합니다. `.tigerkit/branches/{escaped-branch}/` artifact, `CLAUDE.md`, `DESIGN.md`, `reuse-map.md`, docs, source code를 수정하지 않습니다.

## 검토 입력

가능한 범위에서 아래를 확인합니다.

1. 현재 사용자 요청과 명시적 결정
2. current diff 또는 review 대상 file set
3. `.claude-plugin/plugin.json`
4. `commands/*.md`
5. `README.md`, `docs/usage.md`, `docs/output-contract.md`, `docs/artifact-layout.md`
6. `evals/evals.json`
7. branch-local TigerKit artifacts, if present and relevant
8. `CLAUDE.md`, `DESIGN.md`, `reuse-map.md`, if mentioned or modified

## severity

- `Critical`: source loss, inaccessible SOT 추측, protected branch/root artifact write, implementation side effect 같은 core contract 위반
- `High`: reuse exploration 누락, common module impact analysis 누락, user approval 없는 risky decision, command surface drift
- `Medium`: receipt/output contract 불일치, ambiguity/resolvability 분류 누락, handoff freshness 확인 부족
- `Low`: 혼동을 부르는 wording, minor eval coverage gap, non-blocking documentation inconsistency

## 검토 기준

### Source preservation

- 외부 source를 local requirement로 복사, 요약, 정규화, 재작성하지 않았는지 확인합니다.
- 직접 사용자 인터뷰 raw text와 derived interpretation을 분리했는지 확인합니다.
- source가 결론을 지지하지 않는데 fact나 decision처럼 저장하지 않았는지 확인합니다.

### Branch-local artifact and baseline

- write command가 detached HEAD, `main`, `master`, `develop`에서 branch-local artifact를 쓰지 않는지 확인합니다.
- `/tk:gap`이 clean HEAD + commit hash만 baseline으로 쓰는지 확인합니다.
- staged, unstaged, untracked diff를 baseline evidence처럼 다루지 않는지 확인합니다.
- root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`를 active target으로 쓰지 않는지 확인합니다.

### Gap contract

- gap이 SOT reference vs code baseline comparison record인지 확인합니다.
- gap을 실행 queue, task plan, implementation checklist로 바꾸지 않았는지 확인합니다.
- evidence, finding, interpretation, decision, suggestion을 분리했는지 확인합니다.
- severity와 resolvability를 분리했는지 확인합니다.
- external dependency를 locally fixable처럼 표현하지 않았는지 확인합니다.

### Decision Gate

- high-impact ambiguity, inaccessible SOT, SOT conflict, user decision, external dependency, broad/risky refactor가 `/tk:checkpoint` 대상으로 분리됐는지 확인합니다.
- inaccessible SOT 내용을 추측하거나 dependent item을 evidence 없이 `Match`로 표시하지 않았는지 확인합니다.
- SOT 접근성 검증 없이 URL/image/Figma/local path를 inspected source처럼 다루지 않았는지 확인합니다.
- pending SOT entry와 accessible fallback 요청이 빠지지 않았는지 확인합니다.
- binding visual SOT에 stable local asset reference(`./docs/assets/sot/...`)를 선호하는지 확인합니다.
- 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `docs/IMPLEMENTATION_POLICY.md`, `docs/COMPONENT_REUSE_MAP.md`를 단일 `SOT.md`로 합치지 않았는지 확인합니다.
- checkpoint final status가 정의된 값 중 하나인지 확인합니다.
- low-risk trivial detail마다 불필요하게 pause를 만들지 않았는지 확인합니다.
- `/tk:gap`이 `SOT Access Coverage`를 누락했는지 확인합니다.
- inaccessible binding SOT가 있는데 audit partial statement가 누락됐는지 확인합니다.
- pending fallback이 필요한데 자연어 fallback 요청이 빠졌는지 확인합니다.

### Reuse and common module discipline

재사용 탐사 누락은 high-priority finding입니다.

- `reuse-map.md` miss를 reusable module 없음의 evidence로 사용하지 않았는지 확인합니다.
- 새 component, hook, util, mapper, API client, layout primitive, UI pattern 생성 전 repo-wide exploration이 있었는지 확인합니다.
- repo-wide exploration에 file inventory, source root/package/domain structure, keyword search, import/export search, naming search, candidate file inspection, callsite inspection이 포함됐는지 확인합니다.
- explored scope, excluded scope, exclusion reason, shared package/design system/common module 포함 여부가 기록됐는지 확인합니다.
- existing candidate 배제 근거와 새 모듈 대신 가능한 대안이 기록됐는지 확인합니다.
- common module 수정 전 repo-wide callsite impact analysis와 explicit user approval이 있었는지 확인합니다.

### Reflection and durable artifacts

- `/tk:reflect`가 현재 대화 context를 primary source로 썼는지 확인합니다.
- `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` 수정이 user approval 전 적용되지 않았는지 확인합니다.
- `DESIGN.md`가 없을 때 TigerKit이 새로 만들지 않았는지 확인합니다.
- inspect하지 않은 reusable capability, prop, API field, behavior를 기록하지 않았는지 확인합니다.
- `/tk:reflect`를 default next command로 추천하지 않았는지 확인합니다.

### Handoff contract

- `/tk:handoff-write`가 continuation contract이지 task queue가 아닌지 확인합니다.
- branch/HEAD, artifact map, gap context, ambiguity, not-confirmed item, next safe action, do-not-do가 분리됐는지 확인합니다.
- `/tk:handoff-read`가 current branch/HEAD/artifact freshness를 확인한 뒤 stale/missing/conflict/needs-confirmation을 분리하는지 확인합니다.

### Command surface sync

- `.claude-plugin/plugin.json`, README, docs/usage, docs/output-contract, eval fixture가 같은 command surface를 말하는지 확인합니다.
- command 추가/변경 시 plugin version patch bump가 되었는지 확인합니다.
- `evals/evals.json`에 새 behavior fixture가 있고 JSON 문법상 유효한지 확인합니다.

## 출력

finding이 있으면 아래 형식을 사용합니다.

```md
FINDINGS

1. [Severity] 짧은 제목
- 위치: `path:line` 또는 artifact path
- 규칙: 위반한 TigerKit rule
- evidence: 직접 확인한 근거
- 영향: source loss, reuse drift, baseline unreproducibility 등 실제 위험
- 필요한 수정: 완료 기준
```

finding이 없으면 아래 한 줄만 출력합니다.

```text
NO_FINDINGS
```

## 금지

- implementation, commit, push, PR 생성, merge, deploy
- artifact 작성 또는 수정
- source 내용을 추측해 gap/requirements처럼 기록
- inaccessible SOT-dependent item을 evidence 없이 `Match`로 표시
- preference 수준 wording을 blocking finding으로 격상
- unrelated cleanup 요구
