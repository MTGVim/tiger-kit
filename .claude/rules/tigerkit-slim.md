# TigerKit Repo Rules

## 언어 및 산출물 규칙

- 이 저장소에서 만드는 TigerKit 작업 산출물(`.claude/rules/**/*.md`, `.tigerkit/docs/*.md`)은 반드시 한글로 작성한다.
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
- TigerKit active command surface는 `/tk:gap`, `/tk:reflect`, `/tk:loop-spec`, `/tk:execute`다.
- 공개 command surface 변경은 plugin manifest, README, docs, evals 동기화를 함께 검토한다.
- Claude Code plugin command는 namespace를 사용하므로 slash invocation은 `/tk:*` 형태다. 자연어 요청은 같은 프로토콜을 따른다.
- `/tk:gap`은 SoT와 Current Implementation을 한 번 비교해 missing, mismatch, overbuilt, ambiguous를 분류하고 evidence, impact, priority, suggested fix를 보고한다. workflow를 생성하거나 freeze하지 않는다.
- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려한다.
- SoT가 없으면 먼저 SoT 제공을 제안한다.
- 사용자가 직접 진행을 원하면 `/tk:gap` 없이 진행할 수 있다. 이 경우 가정과 불확실성을 명시한다.
- `/tk:reflect`는 세션 내용, 실제 변경 결과, 사용자 피드백에서 재사용 가능한 learning을 추출한다. repo auto-write는 `CLAUDE.local.md`로 제한하고 repo shared `CLAUDE.md`는 suggest-only로 다룬다.
- repo convention은 `.claude/rules/**/*.md`를 우선 확인한다.
- UI copy는 basis 또는 confirmed contract와 exact match여야 한다. 의미상 유사함은 충분하지 않다.
- 외부 근거는 URL, path, ticket, PRD, issue, API docs, source code path, commit hash 같은 reference와 access status로 관리한다.
- 외부 근거 내용을 repo-wide durable 요구사항 텍스트로 복사, 요약, 정규화, 재작성하지 않는다.
- 접근 불가 URL, image, Figma/design link, screenshot URL, local path는 pending reference로 기록하고 file, local path, screenshot/export, pasted content를 요청한다.
- raw source text와 derived interpretation을 분리한다.
- gap 분석 시 source contracts, target, 현재 관측 가능한 baseline을 먼저 식별한다.
- working tree가 dirty하거나 target state가 재현 불가해도 관측 가능한 비교는 진행할 수 있다. 다만 재현 불가 항목은 `unverifiable`, source conflict, 또는 근거 부족으로 명시한다.
- ambiguity를 조용히 해결하지 않는다. 근거가 결론을 지지하지 않으면 source conflict 또는 rejected candidate로 기록하고 필요하면 사용자에게 묻는다.
- 대화 context에 남아 있지 않은 내용은 추측하지 않고 `확인 불가`로 둔다.

## Evidence Rule

중요 claim은 아래 중 하나에 근거해야 한다.

- external basis reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- TigerKit generated artifact clearly marked as generated working memory
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
- TigerKit active generated state는 repo 밖 `~/.tigerkit/`에 둔다. `.claude/tigerkit/`는 legacy/migration context로만 남기며 git ignore 대상이다. `.claude/` 전체를 ignore하지 않는다.
