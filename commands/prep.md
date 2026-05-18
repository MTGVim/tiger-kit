---
description: source-of-truth reference와 사용자 인터뷰 원문을 branch-local .tigerkit/branches/{escaped-branch}/requirements.md에 인덱싱합니다. pseudo-requirement를 만들지 않습니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:prep`은 TigerKit의 source-loss prevention 진입점입니다. 요구사항을 새로 쓰는 명령이 아니라 source-of-truth 위치를 인덱싱하고, 현재 세션에서 사용자가 직접 말한 내용만 원문에 가깝게 보존합니다.

```text
prep = index sources, preserve interview, avoid source loss
```

## 기본 산출물

- `.tigerkit/branches/{escaped-branch}/requirements.md`

`{escaped-branch}`는 현재 git branch name을 collision-safe하게 path-safe 변환한 값입니다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode합니다. 예: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

Root-level `.tigerkit/requirements.md`는 deprecated artifact입니다. 발견하면 현재 branch-local 위치로 migration할지 제안하되, 사용자 승인 없이 이동하지 않습니다.

## branch safety rule

prep 기록 전에 현재 branch를 확인합니다.

- detached HEAD이면 기록하지 않고 branch switch/create를 요청합니다.
- `main`, `master`, `develop`이면 기록하지 않고 feature branch switch/create를 요청합니다.
- working tree가 어떤 상태인지 receipt에 표시합니다.

TigerKit artifact는 branch-local working material입니다. Protected branch나 detached HEAD에 기록하지 않습니다.

## 핵심 원칙

`requirements.md`는 source of truth가 아닙니다. source of truth를 가리키는 branch-local index입니다.

외부 source는 reference만 저장합니다.

- URL
- file path
- ticket link
- Figma link
- PRD link
- issue link
- API docs link
- source code path
- commit hash

외부 source 내용을 local requirement text로 복사, 요약, 정규화, 재작성하지 않습니다. 중요한 wording이 있으면 section pointer만 남기고, 원문 위치를 우선합니다.

현재 세션의 직접 사용자 인터뷰 내용만 local text로 저장할 수 있습니다. 가능한 한 사용자 wording을 보존하고, `원문`과 `파생 해석`을 분리합니다.

## 일반 대화 SOT 후보 유도

일반 대화에서 사용자가 아래 같은 source를 주면 구현, gap 분석, API 검증, design 비교 전에 SOT 후보로 분류합니다.

- Jira
- Figma
- Confluence
- ClickUp
- GitHub issue/PR
- API docs
- MCP resource
- backend repo
- source path

이런 source가 보이면 branch-local `requirements.md`에 reference를 남기기 위해 `/tk:prep`를 강하게 권장합니다. 사용자가 slash command를 직접 치지 않아도 동의하면 `/tk:prep` 계약으로 진행할 수 있습니다.

artifact를 쓰기 전에 `requirements.md`에 reference를 기록한다고 먼저 밝힙니다.

외부 source 내용은 local requirement text로 복사, 요약, 정규화, 재작성하지 않습니다. URL, resource id, path, ticket id, title, source owner, lookup time 같은 pointer metadata만 기록합니다.

### SOT 접근성 검증 gate

외부 SOT reference는 durable SOT처럼 기록하기 전에 현재 agent/runtime에서 접근 가능한지 검증합니다.

```text
Having a URL is not the same as seeing the image, reading the document, or inspecting the design.
```

검증 대상:

- document URL
- image URL
- Figma/design URL
- screenshot URL
- local file path
- pasted reference
- file attachment
- 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `docs/IMPLEMENTATION_POLICY.md`, `docs/COMPONENT_REUSE_MAP.md`

Do not rename everything to a single `SOT.md` file. 기존 구조는 `SOT.md` 같은 단일 파일로 합치지 않습니다. 위 파일들이 있으면 source category별 active SOT candidate로 intake하고, branch-local `requirements.md`의 SOT 접근성 manifest에 연결합니다.

권장 access status:

```text
accessible
mirrored_local
provided_inline
local_missing
inaccessible
auth_required
expired_or_unavailable
unsupported_format
pending_user_input
decorative_non_binding
not_verifiable
```

접근 실패 시:

1. verified requirement로 materialize하지 않습니다.
2. branch-local `requirements.md`에 pending SOT entry를 남깁니다.
3. 사용자에게 accessible file, local path, screenshot/export, pasted content를 요청합니다.
4. binding visual SOT는 가능한 경우 stable local asset reference를 선호합니다.

권장 fallback path:

```text
./docs/assets/sot/requirements/1.1.1.png
./docs/assets/sot/design/bulk-confirm-modal.png
./docs/assets/sot/policy/example.pdf
```

원본 URL은 traceability를 위해 보존하되, credential/token query는 저장하지 않거나 redacted로 표시합니다. private asset을 외부 서비스에 업로드하지 않습니다.

### API 검증 source

API 검증은 가능하면 backend state reference set을 우선합니다.

- backend repo name
- branch policy: 조회 시점의 최신 `develop`
- lookup HEAD commit
- open PR list 또는 관련 PR
- endpoint, schema, source path
- 관련 API docs, ticket, issue reference

backend repo나 PR 본문 내용은 local requirements text로 복사하지 않습니다.

## 권장 구조

```md
# TigerKit 요구사항 인덱스

## SOT 접근성 manifest

A source is not binding-auditable until TigerKit can access and inspect it, or explicitly marks it as pending/not-verifiable. `accessible`, `mirrored_local`, or `provided_inline` still require inspected evidence before requirement materialization.

| SOT ID | Type | Original Reference | Access Status | Local Path | Represents | Binding | Checked At | Notes |
|---|---|---|---|---|---|---|---|---|
| SOT-REQ-001 | markdown | ./docs/REQUIREMENTS.md | accessible | ./docs/REQUIREMENTS.md | functional requirements | binding | 2026-05-18 | local file |
| SOT-IMG-001 | image | https://example.com/private/spec.png | pending_user_input | pending | 1.1.1 기획서 이미지 | binding | 2026-05-18 | ask user for fallback |

## 외부 소스 참조

- PRD: https://...
- Figma: https://...
- GitHub Issue: https://...
- Source Code: src/...
- Commit: abc1234

## Pending SOT entries

### SOT-IMG-001

- Original Reference: https://example.com/private/spec.png
- Access Status: `pending_user_input`
- Represents: 1.1.1 기획서 이미지
- Binding: binding
- Needed fallback: file upload, local path, screenshot/export, or pasted content
- Recommended path: `./docs/assets/sot/requirements/1.1.1.png`
- Materialization: image-derived visual/copy requirements not recorded yet

## 사용자 인터뷰 요구사항

### 원문

> 사용자 원문에 가까운 내용

### 파생 해석

- 명시적으로 파생 해석임을 표시

## 모호성

- 확인되지 않은 점과 확인이 필요한 source
```

## 절차

1. 현재 branch를 확인합니다.
2. detached HEAD 또는 protected branch이면 branch switch/create를 요청하고 멈춥니다.
3. 사용자가 제공한 source를 external reference와 direct interview text로 분리합니다.
4. 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `docs/IMPLEMENTATION_POLICY.md`, `docs/COMPONENT_REUSE_MAP.md`, `docs/assets/sot/`가 있으면 active SOT candidate로 intake합니다.
5. 각 SOT candidate의 type과 access status를 검증합니다.
6. 외부 source는 pointer와 access metadata만 기록합니다.
7. inaccessible source는 pending SOT entry로 기록하고 fallback을 요청합니다.
8. 사용자 인터뷰 내용은 raw quote에 가깝게 기록합니다.
9. 파생 해석은 `파생 해석` 아래에 표시합니다.
10. source가 conclusion을 지지하지 않으면 추측하지 말고 ambiguity로 남깁니다.
11. `.tigerkit/branches/{escaped-branch}/requirements.md` 외의 산출물을 만들지 않습니다.
12. root-level `.tigerkit/requirements.md`가 있으면 migration 후보로만 표시합니다.
13. target repo의 active `CLAUDE.md`를 확인하고, missing 사항은 update proposal로 분리합니다.

## ambiguity rule

source가 결론을 지지하지 않으면 silent choice를 하지 않습니다.

```text
source does not specify X
→ ambiguity 기록
→ 필요하면 사용자에게 확인
```

## target repo CLAUDE.md guidance

이 플러그인 repo의 `CLAUDE.md`가 아니라 현재 작업 대상 repo의 active `CLAUDE.md`를 확인합니다.

확인 항목:

- active `CLAUDE.md` 자체가 없는지
- TigerKit managed section이 없는지
- 아래 현재 plugin 권장 규칙이 빠져 있거나 기존 managed section 내용이 오래되어 불일치하는지
  - SOT 후보 유도 규칙
  - API reference set 규칙
  - `reuse-map.md`를 cache-0 discovery aid로만 다루는 규칙
  - 새 모듈 생성 전 repo-wide exploration 규칙
  - 공통 모듈 수정 전 callsite impact analysis와 사용자 승인 규칙
  - `/tk:gap` clean HEAD baseline 규칙

위 항목 중 하나라도 비어 있거나 stale이면 `requirements.md` 기록과 분리해서 `CLAUDE.md` update proposal을 강하게 권장하고, 적용 여부를 사용자에게 묻습니다.

Marker:

```md
<!-- TIGERKIT:START -->
<!-- TIGERKIT:END -->
```

`/tk:prep`은 `CLAUDE.md`를 직접 수정하지 않습니다. `requirements.md` 기록과 `CLAUDE.md` update proposal을 분리하고, 실제 수정은 사용자 승인 후에만 진행합니다.

## 금지

- 실행 대기열이나 진행 상태 파일 생성
- external source를 local requirement처럼 요약/재작성
- inaccessible URL, image, Figma, screenshot, local path를 inspected SOT처럼 기록
- unverified asset-derived requirement를 confirmed requirement처럼 materialize
- 여러 source를 하나의 synthetic requirement로 병합
- `CLAUDE.md`, `DESIGN.md`, `reuse-map.md` 직접 업데이트
- root-level `.tigerkit/requirements.md` 새로 쓰기
- implementation, commit, push, PR 생성, merge, deploy

## 출력

receipt-first로 짧게 보고합니다.

```text
source index 기록 준비했습니다.
- branch: `feature__example`
- 기록: `.tigerkit/branches/feature__example/requirements.md`
- external sources: reference와 access status만 저장
- pending SOT: 접근 불가 source는 fallback 요청
- local asset: binding visual SOT는 `./docs/assets/sot/...` 경로 권장
- interview: raw와 interpretation 분리
- root artifact: migration 후보가 있으면 표시
- CLAUDE.md: managed section이 없으면 이후 반영을 강하게 추천할 고우선 후보로 표시

다음: 접근 불가 SOT가 있으면 파일 업로드, 로컬 경로, screenshot/export, pasted content를 제공해 주세요.
```
