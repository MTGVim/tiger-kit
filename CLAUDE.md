# CLAUDE.md

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 TigerKit 작업 산출물(`.claude/rules/**/*.md`, `.claude/handoffs/current.md`, `.tigerkit/docs/*.md`)은 반드시 한글로 작성한다.
- 사용자에게 진행 상황, 계획, 검증 결과를 보고할 때도 한글을 기본으로 사용한다.
- 사용자 대화에 보이는 안내, 추천, 요약, next action은 변수명, path, identifier, contract field name 같은 계약용어를 제외하고 한글로 작성한다.
- 기존 공개 문서나 manifest가 영어 문구를 쓰는 경우에는 주변 문맥과 일관성을 우선한다.

## 검증 및 참조 규칙

- 이 저장소에는 package manager 기반 build/test/lint 설정이 없다.
- 기능 변경 후에는 `claude plugin validate .claude-plugin/plugin.json`, `claude plugin validate .`, `python3 -m json.tool evals/evals.json >/dev/null`, `python3 scripts/check-plugin-version.py`, `git diff --check`를 우선 실행한다.
- `evals/evals.json`은 자동 실행 테스트가 아니라 기대 동작 fixture다. eval 검증은 JSON 문법 검증과 수동 기대 동작 검토를 뜻한다.
- plugin version을 올릴 때는 로컬 파일만 기준으로 계산하지 말고 먼저 `origin/main`의 현재 version을 확인한다. 변경은 `python3 scripts/bump-plugin-version.py <version>` 또는 `--part patch|minor|major`를 사용한다. 이 스크립트는 기본적으로 `origin/main:.claude-plugin/plugin.json`을 기준으로 계산하며, eval에는 특정 version literal을 하드코딩하지 않는다.
- 사용자 관점 사용법, 산출물 구조, 응답 receipt 세부 규칙은 `.tigerkit/docs/usage.md`, `.tigerkit/docs/artifact-layout.md`, `.tigerkit/docs/output-contract.md`를 기준으로 본다.

## 핵심 정책

- TigerKit의 목적은 AI-induced source loss를 줄이는 것이다.
- v8.0 핵심 command flow는 `/tk:gap`, `/tk:launch`, `/tk:reflect`이며 utility/compatibility/secondary command는 `/tk:next`, `/tk:gap --review`, `/tk:handoff`, `/tk:meta-feedback`다.
- 공개 command surface 변경은 compatibility와 docs/evals 동기화를 함께 검토한다. v8 MVP에서 `/tk:spec`은 공개 command로 노출하지 않는다.
- Claude Code plugin command는 namespace를 사용하므로 slash invocation은 `/tk:*` 형태다. 자연어 요청은 같은 프로토콜을 따른다.
- 기본 `/tk:gap`은 사용자 지시, 브레인스토밍, 회의 메모, 결정사항, URL/ticket/docs, legacy branch-local Spec Patch를 source material로 intake하고, source grounding, ambiguity attack, sealed launch workflow 생성을 수행한 뒤 `GAP_READY` 또는 `GAP_BLOCKED`로 끝난다. v7 Contract-based Gap Review는 `/tk:gap --review` compatibility mode로 유지한다.
- `/tk:launch`는 `GAP_READY` sealed workflow만 `tk-runner` subagent로 실행하며, workflow 밖 scope 확장, missing requirement 임의 해석, verification 없는 success 선언, preflight 승인 없는 commit을 금지한다. git/GitHub 부재는 workflow가 commit/PR을 요구하지 않는 한 abort 사유가 아니며 명시 skip reason으로 기록한다. `tk-runner` runtime harness와 model binding은 receipt에 기록해야 하며, required harness unavailable 상태를 숨기지 않는다.
- `/tk:reflect`는 branch/workspace-local working memory에서 repo에 영구 보존할 insight만 추출한다. 기본 동작은 `apply=true`이며, source code는 수정하지 않고 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 직접 반영한다.
- `/tk:next`는 현재 TigerKit artifact와 workspace/repo 상태를 읽어 handoff/trace의 다음 안전 작업을 실제로 이어서 시도하는 steering replacement continuation command다. sealed workflow가 필요한 구현은 `/tk:gap → /tk:launch`를 우회하지 않으며, commit/push/PR/merge/release/deploy 같은 외부 side effect는 사용자 승인 또는 artifact상의 명시 approval 없이는 수행하지 않는다.
- `/tk:handoff`는 다음 세션이나 다음 작업자가 이어받을 continuation 문서를 작성한다.
- `/tk:meta-feedback`은 현재 세션 내역에서 TigerKit command/skill 개선안을 일반화해 추출한다.
- Git worktree context 처리는 Superpowers-style `SessionStart` read-only context check로 세션 시작 시 한 번 감지한다. base/source worktree에만 있는 root-level Markdown과 `.claude/` 후보를 `additionalContext`로 제안하되 자동 symlink/hydration은 금지한다. `/tk:gap`은 이 context를 source grounding에 반영하고, `/tk:launch`와 `/tk:next`는 command마다 재질문하지 말고 session context 또는 decline marker를 소비한다. 사용자가 같은 candidate signature를 거절하면 `.claude/tigerkit/local/session-start/worktree-context-declines.json`에 기록해 다시 묻지 않는다. tracked file symlink, regular file overwrite, `.claude/` 전체 symlink, `node_modules` symlink, source_worktree mutation은 금지한다.
- repo convention은 `.claude/rules/**/*.md`를 우선 확인한다.
- UI copy는 basis 또는 confirmed contract와 exact match여야 한다. 의미상 유사함은 충분하지 않다.
- 외부 근거는 URL, path, ticket, Figma, PRD, issue, API docs, source code path, commit hash 같은 reference와 access status로 관리한다.
- 외부 근거 내용을 repo-wide durable 요구사항 텍스트로 복사, 요약, 정규화, 재작성하지 않는다.
- legacy branch-local Spec Patch가 남아 있으면 `/tk:gap` source material 후보로만 다룬다. 이것은 repo-wide durable knowledge가 아니며 `/tk:reflect`를 거치기 전에는 durable insight가 아니다.
- 접근 불가 URL, image, Figma/design link, screenshot URL, local path는 pending reference로 기록하고 file, local path, screenshot/export, pasted content를 요청한다.
- 현재 session에서 사용자가 직접 말한 인터뷰 내용만 local text로 저장할 수 있다.
- raw source text와 derived interpretation을 분리한다.
- gap 분석 시 source contracts, target, 현재 관측 가능한 baseline을 먼저 식별한다.
- working tree가 dirty하거나 target state가 재현 불가해도 관측 가능한 비교는 진행할 수 있다. 다만 재현 불가 항목은 rejected `unverifiable`, source conflict, 또는 근거 부족으로 명시한다.
- ambiguity를 조용히 해결하지 않는다. 근거가 결론을 지지하지 않으면 source conflict 또는 rejected candidate로 기록하고 필요하면 사용자에게 묻는다.
- 대화 context에 남아 있지 않은 내용은 추측하지 않고 `확인 불가`로 둔다.
- `DESIGN.md`와 `COMPONENT_REUSE_MAP.md`는 derived repo-level knowledge다. basis나 사용자 확인을 대체하지 않는다. `reuse-map.md`는 legacy alias/migration candidate로만 다룬다.
- `DESIGN.md`가 없으면 TigerKit이 새로 생성하지 않는다. 넣을 derived design knowledge가 있으면 사용자에게 초기화 필요를 알린다.
- inspect하지 않은 component prop, API field, behavior, reusable capability를 기록하지 않는다.

## Evidence Rule

중요 claim은 아래 중 하나에 근거해야 한다.

- external basis reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- branch-local TigerKit artifact clearly marked as generated working memory
- derived artifact clearly marked as derived

항상 구분한다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or basis
Suggestion = proposed, not confirmed
```

## 작업 시 주의사항

- command 변경 후에는 `.claude-plugin/plugin.json`의 command 목록과 README/docs의 명령 목록이 서로 맞는지 확인한다.
- `.claude/tigerkit/`은 generated branch-local working memory이므로 git ignore 대상이다. `.claude/` 전체를 ignore하지 않는다.
- `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작하게 될 때는 전용 브랜치 사용을 권유해야 하며, 사용자 승인 없이 브랜치 생성이나 전환을 수행하지 않는다.
- commit, push, PR 생성, merge, deploy는 사용자 승인 없이 수행하지 않는다.
