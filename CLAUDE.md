# CLAUDE.md

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 TigerKit 작업 산출물(`.tigerkit/branches/{escaped-branch}/requirements.md`, `gap.md`, `reflect.md`, `handoff.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선한다.

## 검증 및 참조 규칙

- 이 저장소에는 package manager 기반 build/test/lint 설정이 없다.
- 기능 변경 후에는 `claude plugin validate .claude-plugin/plugin.json`, `claude plugin validate .`, `python3 -m json.tool evals/evals.json >/dev/null`, `git diff --check`를 우선 실행한다.
- `evals/evals.json`은 자동 실행 테스트가 아니라 기대 동작 fixture다. eval 검증은 JSON 문법 검증과 수동 기대 동작 검토를 뜻한다.
- plugin version을 올릴 때는 로컬 파일만 기준으로 계산하지 말고 먼저 `origin/main`의 현재 version을 확인한다.
- 사용자 관점 사용법, 산출물 구조, 응답 receipt 세부 규칙은 `.tigerkit/docs/usage.md`, `.tigerkit/docs/artifact-layout.md`, `.tigerkit/docs/output-contract.md`를 기준으로 본다.

## 핵심 정책

- TigerKit의 목적은 AI-induced source loss를 줄이는 것이다.
- 기본 command set은 `/tk:prep`, `/tk:gap`, `/tk:checkpoint`, `/tk:review`, `/tk:reflect`, `/tk:handoff-write`, `/tk:handoff-read`다.
- TigerKit working material은 branch-local `.tigerkit/branches/{escaped-branch}/` 아래에 기록한다.
- root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`는 deprecated artifact이며 migration 후보로만 다룬다.
- `{escaped-branch}`는 collision-safe path encoding이다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode한다.
- branch-local `requirements.md`는 source of truth가 아니라 SOT reference index와 access manifest다.
- 외부 source는 URL, path, ticket, Figma, PRD, issue, API docs, source code path, commit hash 같은 reference와 access status만 저장한다.
- 외부 source 내용을 local requirement text로 복사, 요약, 정규화, 재작성하지 않는다.
- SOT reference는 접근 가능하고 inspect되기 전까지 binding-auditable로 다루지 않는다.
- inaccessible URL, image, Figma/design link, screenshot URL, local path는 pending SOT entry로 기록하고 file, local path, screenshot/export, pasted content를 요청한다.
- binding visual SOT는 `./docs/assets/sot/requirements/` 또는 `./docs/assets/sot/design/` 아래 stable local asset reference를 선호한다.
- 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `docs/assets/sot/`는 SOT category candidate로 intake하고 단일 `SOT.md`로 합치지 않는다. `COMPONENT_REUSE_MAP.md`는 target repo가 명시적으로 SOT로 정의한 경우가 아니면 derived reuse map으로 다룬다.
- 현재 session에서 사용자가 직접 말한 인터뷰 내용만 local text로 저장할 수 있다.
- raw interview text와 derived interpretation을 분리한다.
- branch-local `gap.md`가 TigerKit의 중심이다. gap은 SOT reference vs code baseline comparison record다.
- gap 분석 전 feature branch + clean working tree + HEAD commit hash가 반드시 필요하다.
- working tree가 clean하지 않으면 gap 기록을 시작하지 않고, 먼저 commit하거나 변경 정리를 요청한다.
- ambiguity를 조용히 해결하지 않는다. source가 결론을 지지하지 않으면 gap으로 기록하고 필요하면 사용자에게 묻는다.
- branch-local `reflect.md`는 현재 대화 context를 primary source로 사용하고, artifact와 git evidence는 보조 근거로만 사용한다.
- `/tk:reflect`는 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `COMPONENT_REUSE_MAP.md` escalation 후보를 제안하고, 사용자 승인 전에는 durable artifact를 수정하지 않는다.
- `/tk:handoff-write`는 current goal, branch/HEAD, artifact map, gap context, ambiguity/not-confirmed 분류, next safe action을 handoff에 남긴다.
- `/tk:handoff-read`는 handoff를 맹신하지 않고 현재 branch/HEAD, artifact map, `CLAUDE.md`, `DESIGN.md`, `COMPONENT_REUSE_MAP.md`, legacy `reuse-map.md`를 확인한 뒤 stale/missing/conflict/needs-confirmation을 분리한다.
- `/tk:gap`은 SOT access coverage를 기록하고 inaccessible binding SOT가 있으면 audit이 partial임을 명시한다.
- 대화 context에 남아 있지 않은 내용은 추측하지 않고 `확인 불가`로 둔다.
- `DESIGN.md`와 `COMPONENT_REUSE_MAP.md`는 derived repo-level knowledge이며 외부 SOT를 대체하지 않는다. `reuse-map.md`는 legacy alias/migration candidate로만 다룬다.
- `DESIGN.md`와 `COMPONENT_REUSE_MAP.md` 업데이트는 prep/gap 중 직접 하지 말고 reflection escalation gate를 통해 제안하고 사용자 승인 후에만 적용한다. `reuse-map.md`는 legacy migration 후보로만 제안한다.
- `DESIGN.md`가 없으면 TigerKit이 새로 생성하지 않는다. 넣을 derived design knowledge가 있으면 사용자에게 초기화 필요를 알린다.
- inspect하지 않은 component prop, API field, behavior, reusable capability를 기록하지 않는다.

## Evidence Rule

중요 claim은 아래 중 하나에 근거해야 한다.

- external SOT reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- derived artifact clearly marked as derived

항상 구분한다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or SOT
Suggestion = proposed, not confirmed
```

## 작업 시 주의사항

- command 변경 후에는 `.claude-plugin/plugin.json`의 command 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작하게 될 때는 전용 브랜치 사용을 권유해야 하며, 사용자 승인 없이 브랜치 생성이나 전환을 수행하지 않는다.
- commit, push, PR 생성, merge, deploy는 사용자 승인 없이 수행하지 않는다.
