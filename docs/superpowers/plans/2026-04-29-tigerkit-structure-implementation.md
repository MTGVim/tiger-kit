# TigerKit Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the current `tigap-skills` plugin into TigerKit with `/tk:mwhat`, `/tk:prep`, `/tk:gap`, `.tigerkit/{work_id}/requirements.md`, and `.tigerkit/{work_id}/gap.md` as the primary workflow.

**Architecture:** Keep the existing command/skill/documentation-only plugin architecture, but rename the product surface from `tigap` to `tk` and replace `prep/source-packet` with `prep/requirements.md`. Preserve the existing `mwhat` behavior as answer clarification, and make `gap` a requirements coverage checker rather than an implementation planner.

**Tech Stack:** Claude Code plugin manifest JSON, Markdown command files, Markdown skill instructions, Bash/PowerShell standalone installers, JSON eval fixtures, `claude plugin validate`, `git diff --check`, GitHub CLI `gh`.

---

## File Structure

Create/replace these files:

- Create: `commands/prep.md` — `/tk:prep` slash command entrypoint.
- Modify: `commands/mwhat.md` — update wording from tigap to TigerKit/tk while keeping behavior.
- Modify: `commands/gap.md` — update required input/output paths and verdict wording.
- Create: `skills/prep/SKILL.md` — requirements normalization workflow replacing `skills/prep`.
- Modify: `skills/mwhat/SKILL.md` — keep answer clarification behavior, update product naming.
- Modify: `skills/gap/SKILL.md` — read `.tigerkit/{work_id}/requirements.md`, write `.tigerkit/{work_id}/gap.md`.
- Delete: `commands/prep.md` — no legacy `/tigap:prep` alias in first TigerKit implementation.
- Delete: `skills/prep/SKILL.md` and `skills/prep/` — replaced by `skills/prep/`.
- Modify: `.claude-plugin/plugin.json` — plugin name `tk`, command/skill list for req/gap/mwhat.
- Modify: `.claude-plugin/marketplace.json` — package/repository-facing name and description for TigerKit.
- Modify: `scripts/install-standalone.sh` — install `prep`, `gap`, `what`; print `/prep`, `/gap`, `/mwhat`.
- Modify: `scripts/install-standalone.ps1` — same for PowerShell.
- Modify: `README.md` — product name, install command, command overview, artifact path.
- Modify: `docs/usage.md` — usage for `/tk:mwhat`, `/tk:prep`, `/tk:gap`.
- Modify: `docs/artifact-layout.md` — `.tigerkit/{work_id}/` structure.
- Modify: `docs/kickoff.md` — add TigerKit restructuring decision without preserving old primary flow.
- Modify: `CLAUDE.md` — repository guidance for TigerKit and `.tigerkit/` artifacts.
- Modify: `evals/evals.json` — workflow-level evals for req/gap/mwhat.
- Modify: `skills/gap/evals/evals.json` — gap-specific evals for requirements path/verdict behavior.
- Modify: `skills/prep/evals/evals.json` by moving content to `skills/prep/evals/evals.json` — prep-specific evals.

Do not edit or stage pre-existing untracked evaluation workspace directories such as `skills/prep-gap-eval-workspace/`.

---

### Task 1: Add TigerKit eval contracts first

**Goal:** Establish failing-but-clear evaluation contracts for the new TigerKit surface before changing implementation docs.

**Files:**
- Modify: `evals/evals.json`
- Create: `skills/prep/evals/evals.json`
- Modify: `skills/gap/evals/evals.json`
- Delete after migration: `skills/prep/evals/evals.json`

**Acceptance Criteria:**
- [ ] Workflow evals use `/tk:prep`, `/tk:gap`, `/tk:mwhat` instead of `/tigap:*`.
- [ ] Prep evals expect `.tigerkit/{work_id}/requirements.md` and `requirements.meta.json`.
- [ ] Gap evals expect `.tigerkit/{work_id}/requirements.md`, `.tigerkit/{work_id}/gap.md`, verdict behavior, and no implementation planning.
- [ ] What evals keep the existing four-block answer clarification behavior.
- [ ] JSON files are valid.

**Verify:** `python -m json.tool evals/evals.json >/dev/null && python -m json.tool skills/prep/evals/evals.json >/dev/null && python -m json.tool skills/gap/evals/evals.json >/dev/null && grep -R "/tigap\|source-packet\|gap-report\|\.gap/" -n evals skills/prep/evals skills/gap/evals` → JSON commands succeed; final grep returns no matches.

**Steps:**

- [ ] **Step 1: Create the req eval directory**

Run:

```bash
mkdir -p skills/prep/evals
```

Expected: command exits with status 0.

- [ ] **Step 2: Replace `evals/evals.json` with TigerKit workflow evals**

Write this exact JSON shape, preserving valid JSON string escaping:

```json
{
  "skill_name": "tigerkit-workflow",
  "evals": [
    {
      "id": 0,
      "name": "prep-cache-hit",
      "prompt": "You are evaluating the TigerKit prep skill instructions. A project already has .tigerkit/checkout-retry/requirements.md and .tigerkit/checkout-retry/requirements.meta.json. The meta fields input_source_hash, prep_prompt_version, scope_hash, and input_identities all match the current request. The user runs: /tk:prep checkout retry 요구사항 다시 정리해줘. Describe exactly what Claude should do and what the user-facing response should include. Do not write files.",
      "expected_output": "Should reuse the existing requirements.md, state cache hit reason briefly, include the requirements.md path, keep the response short, and avoid dumping the whole requirements document.",
      "files": [],
      "expectations": [
        "Says the existing requirements.md should be reused because cache keys match",
        "Names the requirements.md path in the user-facing response",
        "Says the user-facing response should be short and include source/requirement/ambiguity counts when known",
        "Does not instruct regenerating requirements.md or metadata on cache hit"
      ]
    },
    {
      "id": 1,
      "name": "prep-force-miss",
      "prompt": "You are evaluating the TigerKit prep skill instructions. A previous requirements.md exists for .tigerkit/search-filter/requirements.md, but the user runs: /tk:prep --force docs/search-filter.md 기준으로 다시 정리해줘. Describe exactly what Claude should do and what the user-facing response should include. Do not write files.",
      "expected_output": "Should ignore the cache because --force was requested, regenerate requirements.md and metadata, briefly explain the force/cache miss reason, show the path, and keep the chat response short.",
      "files": [],
      "expectations": [
        "Says --force makes Claude ignore or bypass the existing cache",
        "Says requirements.md should be regenerated from docs/search-filter.md",
        "Says requirements metadata should be updated or regenerated",
        "Says the user-facing response should include the path and stay short"
      ]
    },
    {
      "id": 2,
      "name": "gap-requirement-coverage",
      "prompt": "You are evaluating the TigerKit gap skill instructions. A requirements document exists at .tigerkit/onboarding-copy/requirements.md, the repository has relevant docs and code paths, and the user runs: /tk:gap 방금 정리한 요구사항 대비 현재 구현 갭 분석해줘. Describe the expected report structure and the final user-facing response. Do not write files.",
      "expected_output": "Should describe cache check based on git commit, requirements hash, gap prompt version, and scope; write/reuse gap.md with metadata; include Verdict, Requirement Coverage, Remaining Gaps, Unable to Verify, and Notes; final chat response should not dump the full report and should include verdict, path, core gaps, and one next action.",
      "files": [],
      "expectations": [
        "Describes gap cache checking with git commit, requirements hash, prompt version, and scope",
        "Mentions gap.md metadata",
        "Requires Verdict with GAPS_FOUND, NO_GAPS_FOUND, or UNVERIFIABLE",
        "Says Unable to Verify prevents a NO_GAPS_FOUND verdict",
        "Says the chat response should not dump the full report and should include verdict, path, core gaps, and one next action"
      ]
    },
    {
      "id": 3,
      "name": "mwhat-confusing-answer",
      "prompt": "You are evaluating the TigerKit mwhat skill instructions. The user runs /tk:mwhat with this source answer: '이 기능은 확장성을 고려해서 모듈화하고, 상태 관리는 나중에 요구사항이 명확해지면 정하는 게 좋겠습니다. 우선 데이터 흐름을 정리하고 컴포넌트 경계를 잡는 방향으로 접근하면 될 것 같습니다.' Describe the expected user-facing response. Do not write files.",
      "expected_output": "Should use the two approved Korean blocks, explain that the answer means structure first rather than immediate implementation, identify missing component boundary and state-management decision criteria, and provide a practical reply draft.",
      "files": [],
      "expectations": [
        "Includes the block label '🤔 뭣? 쉽게 말하면'",
        "Includes the block label '🎯 하던 것'",
        "Includes the block label '😵 문제 상황'",
        "Includes the block label '💡 추천'",
        "Explains the source answer directly instead of producing a generic summary",
        "Mentions that component boundaries or state-management decision criteria are missing",
        "Provides a message the user can send or adapt"
      ]
    }
  ]
}
```

- [ ] **Step 3: Write `skills/prep/evals/evals.json`**

Use this JSON:

```json
{
  "skill_name": "prep",
  "evals": [
    {
      "id": 1,
      "prompt": "아직 티켓은 없는데 결제 실패 알림 UX를 개선하고 싶어. 바로 구현하지 말고 요구사항부터 잡아줘.",
      "expected_output": "한국어로 앞선 대화 기준으로 정리할지 별도 자료를 받을지 확인하고, 작업 ID를 제안하며, 요구사항·acceptance signal·scope boundary·unknowns를 requirements.md 기준으로 정리한다.",
      "files": [],
      "assertions": [
        "한국어로 응답한다.",
        "구현이나 파일 수정을 시작하지 않는다.",
        "앞선 대화로 정리할지 별도 자료를 제공할지 확인한다.",
        "스펙명 또는 작업 ID를 제안하거나 확인한다.",
        "requirements.md를 기준 산출물로 언급한다.",
        "구현 계획이나 task breakdown을 만들지 않는다.",
        "다음 단계로 /tk:gap 또는 별도 구현 계획 workflow를 짧게 안내한다."
      ]
    },
    {
      "id": 2,
      "prompt": "우리 앱 온보딩이 너무 길다는 피드백이 있어. source 문서는 없고, 먼저 범위랑 완료조건을 정리해줘.",
      "expected_output": "별도 자료가 없으면 앞선 대화 맥락을 기준으로 정리할 수 있음을 확인하고, 완료 조건과 acceptance signal을 분리하되 구현 작업 목록은 확정하지 않는다.",
      "files": [],
      "assertions": [
        "별도 자료가 없음을 전제로 대화 맥락 기반 정리를 제안한다.",
        "Normalized Requirements와 Acceptance Signal 관점으로 정리한다.",
        "In Scope와 Out of Scope를 구분한다.",
        "Unknowns 또는 Conflicts / Ambiguities를 분리한다.",
        "코드 구현을 시작하지 않는다."
      ]
    }
  ]
}
```

- [ ] **Step 4: Replace `skills/gap/evals/evals.json`**

Use this JSON:

```json
{
  "skill_name": "gap",
  "evals": [
    {
      "id": 1,
      "prompt": "이 저장소에서 부족한 점을 gap 분석해줘.",
      "expected_output": "requirements.md 또는 명시된 작업 기준이 없음을 설명하고 저장소를 임의 분석하지 않으며, 먼저 /tk:prep로 요구사항 기준을 정리하라고 안내한다.",
      "files": [],
      "assertions": [
        "작업 기준이 없다고 보고한다.",
        "저장소를 임의로 기준 자료 삼아 분석하지 않는다.",
        ".tigerkit/ 산출물을 만들지 않는다.",
        "먼저 /tk:prep를 안내한다.",
        "구현을 시작하지 않는다."
      ]
    },
    {
      "id": 2,
      "prompt": ".tigerkit/login-failure-ux/requirements.md 기준으로 gap 분석해줘.",
      "expected_output": "준비된 requirements.md를 기준으로 현재 상태를 확인하려 하고, 로그인 실패 UX의 requirement coverage, remaining gaps, unable to verify를 분리한 뒤 verdict를 제시한다.",
      "files": [],
      "assertions": [
        "requirements.md를 작업 기준으로 삼는다.",
        "Verdict를 GAPS_FOUND, NO_GAPS_FOUND, UNVERIFIABLE 중 하나로 제시한다.",
        "Requirement Coverage를 포함한다.",
        "Unable to Verify가 있으면 NO_GAPS_FOUND로 판정하지 않는다.",
        "코드를 구현하지 않는다.",
        "구현 계획 대신 짧은 다음 행동 후보만 제시한다."
      ]
    }
  ]
}
```

- [ ] **Step 5: Remove old prep eval fixture**

Run:

```bash
rm -f skills/prep/evals/evals.json
rmdir skills/prep/evals 2>/dev/null || true
```

Expected: old eval file is gone; `rmdir` may do nothing if the directory is not empty.

- [ ] **Step 6: Verify and commit eval contracts**

Run:

```bash
python -m json.tool evals/evals.json >/dev/null
python -m json.tool skills/prep/evals/evals.json >/dev/null
python -m json.tool skills/gap/evals/evals.json >/dev/null
! grep -R "/tigap\|source-packet\|gap-report\|\.gap/" -n evals skills/prep/evals skills/gap/evals
```

Expected: JSON commands exit 0; grep command exits 0 because `! grep` found no matches.

Commit:

```bash
git add evals/evals.json skills/prep/evals/evals.json skills/gap/evals/evals.json
git add -u skills/prep/evals
git commit -m "test: define TigerKit workflow evals"
```

---

### Task 2: Rename plugin surface to `tk` and create `prep` command/skill shell

**Goal:** Make the plugin expose only `/tk:prep`, `/tk:mwhat`, and `/tk:gap`, with no legacy `/tigap:*` or `prep` command registration.

**Files:**
- Create: `commands/prep.md`
- Modify: `commands/mwhat.md`
- Modify: `commands/gap.md`
- Create: `skills/prep/SKILL.md`
- Modify: `skills/mwhat/SKILL.md`
- Modify: `skills/gap/SKILL.md`
- Delete: `commands/prep.md`
- Delete: `skills/prep/SKILL.md`
- Modify: `.claude-plugin/plugin.json`

**Acceptance Criteria:**
- [ ] `.claude-plugin/plugin.json` has name `tk` and command list `prep`, `what`, `gap`.
- [ ] `commands/prep.md` is removed.
- [ ] `skills/prep/SKILL.md` is removed after `skills/prep/SKILL.md` exists.
- [ ] Command entrypoints mention TigerKit and `tk` names.
- [ ] Plugin validation for `.claude-plugin/plugin.json` succeeds.

**Verify:** `claude plugin validate .claude-plugin/plugin.json && ! grep -R "commands/prep\|skills/prep\|/tigap" -n .claude-plugin commands skills/prep/SKILL.md skills/gap/SKILL.md skills/mwhat/SKILL.md` → validation succeeds; grep finds no matches.

**Steps:**

- [ ] **Step 1: Create `commands/prep.md`**

Write:

```markdown
---
description: 외부 요구사항 소스를 정제해 이후 계획과 갭 확인의 기준이 되는 requirements.md로 정리합니다.
---

TigerKit의 `prep` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: Jira 티켓, Confluence 문서, PRD, 사용자 메모, 회의 요약, 기존 요구사항 문서 같은 source of truth 후보를 중복 제거, 충돌/모호점 표시, acceptance signal, scope boundary 중심으로 정규화해 `.tigerkit/{work_id}/requirements.md`에 저장합니다.

먼저 앞선 대화에서 추론한 스펙명 또는 작업 ID를 제안하고, 그 이름으로 `.tigerkit/{work_id}/`에 정리해도 되는지 확인합니다.

명시적으로 요청받지 않는 한 이 명령에서는 구현 계획을 확정하거나 코드를 수정하지 않습니다.
```

- [ ] **Step 2: Update `commands/mwhat.md` wording**

Replace the line `이 플러그인의 \`what\` 스킬을 사용합니다.` with:

```markdown
TigerKit의 `mwhat` 스킬을 사용합니다.
```

Keep the four-block output description and the “do not implement or edit files” rule unchanged.

- [ ] **Step 3: Update `commands/gap.md` wording and paths**

Replace the body after frontmatter with:

```markdown
TigerKit의 `gap` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md`에 정리된 요구사항 기준을 읽고, 필요한 범위에서 현재 구현이나 문서를 확인한 뒤 `.tigerkit/{work_id}/gap.md`를 작성합니다.

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 말고 `/tk:prep`로 요구사항 기준을 먼저 정리하라고 안내합니다.

명시적으로 요청받지 않는 한 이 명령에서는 코드를 구현하거나 구현 계획을 새로 만들지 않습니다.
```

- [ ] **Step 4: Copy current prep skill to req as a starting point**

Run:

```bash
mkdir -p skills/prep
cp skills/prep/SKILL.md skills/prep/SKILL.md
```

Expected: `skills/prep/SKILL.md` exists. Task 3 rewrites it fully.

- [ ] **Step 5: Update plugin manifest**

Replace `.claude-plugin/plugin.json` with:

```json
{
  "name": "tk",
  "description": "요구사항 정제, 답변 해독, 요구사항 대비 갭 확인을 돕는 TigerKit Claude Code 스킬 모음입니다.",
  "version": "2.0.0",
  "author": {
    "name": "MTGVim"
  },
  "commands": [
    "./commands/prep.md",
    "./commands/mwhat.md",
    "./commands/gap.md"
  ],
  "skills": [
    "./skills/prep",
    "./skills/mwhat",
    "./skills/gap"
  ]
}
```

- [ ] **Step 6: Remove old prep command and skill file**

Run:

```bash
rm -f commands/prep.md
rm -f skills/prep/SKILL.md
rmdir skills/prep 2>/dev/null || true
```

Expected: command exits 0. `skills/prep/` may remain if hidden or untracked files exist; do not delete unrelated workspaces.

- [ ] **Step 7: Verify and commit plugin surface**

Run:

```bash
claude plugin validate .claude-plugin/plugin.json
! grep -R "commands/prep\|skills/prep\|/tigap" -n .claude-plugin commands skills/prep/SKILL.md skills/gap/SKILL.md skills/mwhat/SKILL.md
```

Expected: validation succeeds; grep command exits 0 because there are no matches.

Commit:

```bash
git add .claude-plugin/plugin.json commands/prep.md commands/mwhat.md commands/gap.md skills/prep/SKILL.md skills/mwhat/SKILL.md skills/gap/SKILL.md
git add -u commands/prep.md skills/prep
git commit -m "feat: rename plugin surface to TigerKit tk"
```

---

### Task 3: Rewrite `prep` skill around `requirements.md`

**Goal:** Replace prep/source-packet behavior with a requirements normalization workflow that does not create implementation plans.

**Files:**
- Modify: `skills/prep/SKILL.md`

**Acceptance Criteria:**
- [ ] Frontmatter name is `prep`.
- [ ] Required output is `.tigerkit/{work_id}/requirements.md`.
- [ ] Optional source storage is `.tigerkit/{work_id}/inputs/`.
- [ ] Metadata path is `.tigerkit/{work_id}/requirements.meta.json`.
- [ ] Document format includes Source Inputs, Normalized Requirements, Scope Boundary, Conflicts / Ambiguities, Assumptions, Unknowns, Gap Check Basis.
- [ ] Skill explicitly forbids implementation planning, task breakdown, file-level patch instructions, and code edits.
- [ ] User handoff is short and points to `requirements.md` plus `/tk:gap` or a separate implementation planning workflow.

**Verify:** `grep -n "source-packet\|source_packet\|\.gap/\|/tigap\|prep" skills/prep/SKILL.md` → no output.

**Steps:**

- [ ] **Step 1: Replace `skills/prep/SKILL.md` with req instructions**

Write this file structure exactly, filling prose in Korean as shown:

```markdown
---
name: prep
description: 외부 요구사항 소스와 대화 맥락을 이후 계획과 갭 확인의 기준이 되는 requirements.md로 정리합니다. 사용자가 요구사항을 정리하거나, source of truth 후보를 합치거나, gap 분석 전에 기준 문서를 만들려 할 때 반드시 사용합니다.
---

# prep

## 목적

Jira 티켓, Confluence 문서, PRD, 사용자 메모, 회의 요약, 기존 요구사항 문서, 앞선 대화 맥락을 갭 확인 가능한 요구사항 기준으로 정리합니다.

이 스킬은 구현 계획을 만들거나 코드를 수정하는 단계가 아닙니다. 무엇을 기준으로 계획하거나 갭을 볼지 먼저 고정합니다.

## 동작 방식

사용자에게 보이는 응답과 작업 산출물은 항상 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

긴 질문지를 던지지 않습니다. 현재 대화에서 추론할 수 있는 내용을 먼저 짧게 요약하고, 부족한 결정만 좁혀서 묻습니다.

## 하지 않는 일

- 요구사항 임의 창작
- 구현 계획 확정
- 파일별 수정 지시
- 코드 패치 작성
- CE plan이나 Superpowers plan을 대체하는 task breakdown 생성

## 시작 프롬프트

작업 기준이 아직 고정되지 않았다면 먼저 다음 두 가지를 확인합니다.

```text
현재 대화 기준으로는 “{추론한 스펙명}” 요구사항으로 정리할 수 있어 보입니다.

1. 별도 자료가 있나요?
   - 파일 경로, 기획서 URL, 티켓, 메모, 스크린샷 등
   - 없으면 앞선 대화 맥락만 기준으로 정리합니다.

2. 스펙명/작업 ID는 “{추론한 스펙명}”으로 잡아도 될까요?
```

사용자가 바로 자료를 제공했거나 스펙명을 명시했다면 불필요하게 다시 묻지 말고 확인된 정보로 진행합니다.

## 입력 자료

다음 자료를 요구사항 기준으로 사용할 수 있습니다.

- 앞선 대화 맥락
- 이슈 트래커 티켓
- 지식베이스 문서
- PRD 또는 디자인 문서
- 사용자가 작성한 브리프나 메모
- 스크린샷
- 코드 경로
- 풀 리퀘스트
- 기존 구현 참고 자료

외부 시스템이나 특정 도구 사용을 강제하지 않습니다. 사용자가 제공하거나 가져오라고 지시한 자료만 다룹니다.

## 산출물 디렉터리

가능하면 작업명이나 명시된 작업 ID에서 안전한 slug를 만듭니다.

산출물은 다음 경로 아래에 저장합니다.

```text
.tigerkit/{work_id}/
```

현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면, 산출물 작성 전에 작업 브랜치나 명시적 작업 ID를 권유합니다. 브랜치 생성이나 전환은 사용자 승인 없이 수행하지 않습니다.

## 출력 파일

다음 파일을 생성하거나 갱신합니다.

```text
.tigerkit/{work_id}/requirements.md
```

필요하면 다음 디렉터리도 사용합니다.

```text
.tigerkit/{work_id}/inputs/
```

`requirements.md`는 영구적인 원천소스가 아니라 이번 작업에서 계획과 갭 확인 기준으로 사용할 요구사항 스냅샷입니다.

Git 저장소에서 실행 중이라면 `.tigerkit/`이 ignore 또는 의도적으로 track되는지 확인합니다. 둘 다 아니라면 산출물 생성 전에 `.tigerkit/`을 `.gitignore`에 추가하라고 제안합니다. 사용자 저장소의 ignore 정책은 강제하지 않습니다.

## 캐시 메타데이터

`requirements.md`를 생성하거나 재사용할 때 다음 메타데이터를 함께 관리합니다.

```text
.tigerkit/{work_id}/requirements.meta.json
```

메타데이터에는 최소한 다음을 기록합니다.

- `artifact`: `requirements.md`
- `artifact_hash`: 생성 또는 재사용된 `requirements.md`의 해시
- `input_source_hash`: requirements 생성에 실제 사용한 입력 자료의 해시
- `prep_prompt_version`: prep 스킬 또는 지시문 버전
- `scope_hash`: 작업 ID, 스펙명, 포함 범위, 제외 범위를 정규화한 해시
- `input_identities`: 사람이 확인할 수 있는 입력 자료 목록
- `created_at`: 메타데이터 작성 시각

전체 대화가 아니라 requirements 생성에 실제 사용한 입력만 해시합니다.

## requirements.md 구조

```md
# Requirements

## Source Inputs
| Source | Type | Role | Status | Notes |
|---|---|---|---|---|

## Normalized Requirements
| ID | Requirement | Priority | Source | Acceptance Signal |
|---|---|---|---|---|

## Scope Boundary
### In Scope
-

### Out of Scope
-

## Conflicts / Ambiguities
| ID | Issue | Sources | Impact | Suggested Resolution |
|---|---|---|---|---|

## Assumptions
| ID | Assumption | Reason | Risk |
|---|---|---|---|

## Unknowns
| ID | Question | Impact | Suggested Next Step |
|---|---|---|---|

## Gap Check Basis
- `tk:gap`은 이 문서의 Normalized Requirements와 Acceptance Signal을 기준으로 현재 상태의 차이를 확인한다.
```

## 진행 절차

### 1. 기준 선택

앞선 대화 맥락만으로 정리할지, 별도 자료를 추가할지 확인합니다.

아이디어가 흐릿하면 다음 범위만 짧게 좁힙니다.

- 해결하려는 문제
- 원하는 완료 상태
- 반드시 지켜야 할 제약
- 이번에 제외할 범위
- 검증 방법 또는 acceptance signal

### 2. 캐시 확인

`--force`가 명시되지 않았고 기존 `requirements.md`와 `requirements.meta.json`이 있으면 캐시를 확인합니다.

다음 값이 모두 같으면 기존 `requirements.md`를 재사용합니다.

- `input_source_hash`
- `prep_prompt_version`
- `scope_hash`
- `input_identities`

하나라도 다르면 `requirements.md`를 다시 생성합니다.

사용자에게 cache hit/miss 여부와 이유를 한 문장으로 알려줍니다. `--force`가 명시되면 기존 캐시를 무시하고 다시 생성합니다.

### 3. 요구사항 정리

캐시 hit이면 이 단계를 건너뛰고 기존 `requirements.md`를 재사용합니다.

캐시 miss이거나 `--force`이면 모든 자료를 하나의 요구사항 기준으로 정규화합니다.

다음을 분리해서 기록합니다.

- Source Inputs
- Normalized Requirements
- Scope Boundary
- Conflicts / Ambiguities
- Assumptions
- Unknowns
- Gap Check Basis

확인된 사실과 추정을 섞지 않습니다. 두 자료가 충돌하면 조용히 합치지 말고 충돌을 명시합니다.

### 4. 저장과 인계

`requirements.md`를 작성하거나 재사용한 뒤, 다음에 `/tk:gap`으로 요구사항 대비 갭을 확인하거나 별도 구현 계획 workflow에서 이 문서를 기준으로 계획을 세울 수 있다고 안내합니다.

사용자 응답에는 다음만 포함합니다.

- 생성 또는 재사용 여부와 cache hit/miss 이유
- `requirements.md` 파일 경로
- 외부 요구사항 소스 수
- 정규화된 요구사항 수
- 모호점 또는 충돌 수
- 다음 단계 한 문장

전체 `requirements.md` 내용을 채팅에 길게 출력하지 않습니다.

## 완료 기준

이 스킬은 다음 조건을 만족하면 완료됩니다.

- 작업 기준 이름이 정해짐
- cache hit이면 기존 `requirements.md`를 재사용하고 이유를 알림
- cache miss 또는 `--force`이면 요구사항 기준이 `requirements.md`에 정리되고 메타데이터가 갱신됨
- 확인된 사실, 충돌/모호점, 추정, unknowns가 분리됨
- 다음 단계가 `/tk:gap` 또는 별도 구현 계획 workflow로 명확함
- 사용자 응답이 파일 경로와 짧은 요약 중심으로 정리됨
```

- [ ] **Step 2: Verify no old prep/source language remains**

Run:

```bash
! grep -n "source-packet\|source_packet\|\.gap/\|/tigap\|prep" skills/prep/SKILL.md
```

Expected: command exits 0 because grep finds no matches.

- [ ] **Step 3: Commit req skill rewrite**

Run:

```bash
git add skills/prep/SKILL.md
git commit -m "feat: define req requirements workflow"
```

---

### Task 4: Rewrite `gap` skill around requirements coverage

**Goal:** Make `gap` compare `.tigerkit/{work_id}/requirements.md` against current implementation/docs/tests and report verdict-based coverage.

**Files:**
- Modify: `skills/gap/SKILL.md`
- Modify: `commands/gap.md` if Task 2 left any stale language

**Acceptance Criteria:**
- [ ] Required input is `.tigerkit/{work_id}/requirements.md`.
- [ ] Output is `.tigerkit/{work_id}/gap.md`.
- [ ] Metadata is `.tigerkit/{work_id}/gap.meta.json`.
- [ ] Metadata uses `requirements_hash` rather than source packet terms.
- [ ] Report includes Verdict, Requirement Coverage, Remaining Gaps, Unable to Verify, Notes.
- [ ] `NO_GAPS_FOUND` is forbidden when any requirement is unverified.
- [ ] Skill forbids implementation planning and code changes unless explicitly requested outside this skill.

**Verify:** `grep -n "source-packet\|source_packet\|gap-report\|\.gap/\|/tigap\|prep" skills/gap/SKILL.md commands/gap.md` → no output.

**Steps:**

- [ ] **Step 1: Replace `skills/gap/SKILL.md` with requirements coverage instructions**

Use this structure:

```markdown
---
name: gap
description: requirements.md와 현재 구현, 문서, 테스트, 관찰 가능한 동작 사이의 차이를 분석합니다. .tigerkit/{work_id}/requirements.md가 준비된 뒤 요구사항 coverage, remaining gaps, 확인 불가 항목, ship blocker를 확인할 때 반드시 사용합니다.
---

# gap

## 목적

`prep` 단계에서 정리한 `requirements.md`를 바탕으로 현재 상태와의 갭을 분석합니다.

중간 점검과 최종 검산을 별도 skill로 나누지 않습니다. 남은 gap이 있으면 아직 작업 중이고, 확인 가능한 기준에서 gap이 없고 확인 불가 항목도 없으면 출고 가능 후보입니다.

## 동작 방식

사용자에게 보이는 응답과 작업 산출물은 항상 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

사용자가 명시적으로 워크플로우를 건너뛰라고 하지 않는 한 이 스킬에서는 코드를 구현하지 않습니다.

이 스킬은 자료 수집이나 requirements 작성을 담당하지 않습니다. 다음에 집중합니다.

1. 요구사항 기준 확인
2. 캐시 확인
3. 현재 상태 확인
4. coverage/gap 분석
5. 짧은 다음 행동 정리

## 필수 입력

다음 파일이 있어야 합니다.

```text
.tigerkit/{work_id}/requirements.md
```

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 않고 `/tk:prep`로 요구사항 기준을 먼저 정리하라고 안내합니다.

저장소를 임의로 기준 자료로 삼아 분석하지 않습니다.

## 출력 파일

다음 파일을 생성하거나 갱신합니다.

```text
.tigerkit/{work_id}/gap.md
```

## 캐시 메타데이터

`gap.md`를 생성하거나 재사용할 때 다음 메타데이터를 함께 관리합니다.

```text
.tigerkit/{work_id}/gap.meta.json
```

메타데이터에는 최소한 다음을 기록합니다.

- `artifact`: `gap.md`
- `artifact_hash`: 생성 또는 재사용된 `gap.md`의 해시
- `git_commit_sha`: 분석 기준 git commit SHA
- `working_tree_dirty`: 작업 트리에 커밋되지 않은 변경이 있었는지 여부
- `requirements_hash`: `requirements.md`의 해시
- `gap_prompt_version`: gap 스킬 또는 지시문 버전
- `scope_hash`: 분석 범위를 정규화한 해시
- `checked_paths`: 실제로 확인한 주요 파일 경로
- `created_at`: 메타데이터 작성 시각

## 진행 절차

### 1. 요구사항 기준 확인

`requirements.md`에서 다음을 확인합니다.

- Source Inputs
- Normalized Requirements
- Acceptance Signal
- Scope Boundary
- Conflicts / Ambiguities
- Assumptions
- Unknowns
- Gap Check Basis

Unknowns, assumptions, conflicts가 coverage 판단에 영향을 주면 보고서에 명시합니다.

### 2. 캐시 확인

`--force`가 명시되지 않았고 기존 `gap.md`와 `gap.meta.json`이 있으면 캐시를 확인합니다.

다음 값이 모두 같고 작업 트리에 커밋되지 않은 변경이 없으면 기존 `gap.md`를 재사용합니다.

- `git_commit_sha`
- `requirements_hash`
- `gap_prompt_version`
- `scope_hash`

하나라도 다르거나 작업 트리가 dirty이면 gap 분석을 다시 실행합니다.

사용자에게 cache hit/miss 여부와 이유를 한 문장으로 알려줍니다. `--force`가 명시되면 기존 캐시를 무시하고 다시 분석합니다.

### 3. 현재 상태 확인

캐시 hit이면 이 단계를 건너뛰고 기존 `gap.md`를 재사용합니다.

캐시 miss이거나 `--force`이면 requirements에 코드 경로, 현재 구현, 비교 대상, 문서 경로가 포함된 경우에만 관련 파일을 확인합니다.

요구사항에 비교 대상이 충분히 없으면 저장소 전체를 임의로 훑지 말고 `Unable to Verify` 또는 확인 질문으로 남깁니다.

### 4. gap.md 작성

보고서는 다음 구조를 기본으로 합니다.

```md
# Gap Report

## Verdict
GAPS_FOUND / NO_GAPS_FOUND / UNVERIFIABLE

## Requirement Coverage
| Requirement ID | Status | Evidence | Gap |
|---|---|---|---|

## Remaining Gaps
| Gap ID | Requirement ID | Severity | Description | Suggested Next Move |
|---|---|---|---|---|

## Unable to Verify
| Requirement ID | Reason | Needed Evidence |
|---|---|---|

## Notes
-
```

Verdict 규칙:

- 남은 gap이 있으면 `GAPS_FOUND`입니다.
- 확인 불가능한 requirement가 있으면 `NO_GAPS_FOUND`를 쓰지 않습니다.
- 확인 불가능한 항목이 주요 coverage 판단을 막으면 `UNVERIFIABLE`을 사용합니다.
- 확인 가능한 기준에서 충족되고 확인 불가 항목이 없을 때만 `NO_GAPS_FOUND`를 사용합니다.
- `NO_GAPS_FOUND`는 “현재 확인 가능한 기준에서는 남은 gap 없음”이라고 표현합니다.

### 5. 사용자 인계

전체 보고서를 채팅에 길게 출력하지 않습니다.

사용자 응답에는 다음만 포함합니다.

- 생성 또는 재사용 여부와 cache hit/miss 이유
- Verdict
- `gap.md` 파일 경로
- 핵심 gap 1~3개
- 다음 행동 1개
```

- [ ] **Step 2: Verify old terminology is gone**

Run:

```bash
! grep -n "source-packet\|source_packet\|gap-report\|\.gap/\|/tigap\|prep" skills/gap/SKILL.md commands/gap.md
```

Expected: command exits 0 because grep finds no matches.

- [ ] **Step 3: Commit gap rewrite**

Run:

```bash
git add skills/gap/SKILL.md commands/gap.md
git commit -m "feat: align gap with requirements coverage"
```

---

### Task 5: Update docs, installers, marketplace metadata, and repository guidance

**Goal:** Make every user-facing document and installer describe TigerKit, `tk:*`, `.tigerkit/`, `requirements.md`, and `gap.md` consistently.

**Files:**
- Modify: `README.md`
- Modify: `docs/usage.md`
- Modify: `docs/artifact-layout.md`
- Modify: `docs/kickoff.md`
- Modify: `CLAUDE.md`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `scripts/install-standalone.sh`
- Modify: `scripts/install-standalone.ps1`

**Acceptance Criteria:**
- [ ] README opens with TigerKit and lists `/tk:mwhat`, `/tk:prep`, `/tk:gap`.
- [ ] Installation docs use `MTGVim/tiger-kit` and `tk@tiger-kit` as the target GitHub slug/package examples.
- [ ] Artifact docs use `.tigerkit/{work_id}/inputs/`, `requirements.md`, `requirements.meta.json`, `gap.md`, `gap.meta.json`.
- [ ] CLAUDE.md Korean instructions use `.tigerkit/` artifact rules and `tk:*` command overview.
- [ ] Install scripts copy `skills/prep`, `skills/gap`, `skills/mwhat`.
- [ ] Marketplace metadata says TigerKit, not tigap.

**Verify:** `! grep -R "/tigap\|source-packet\|gap-report\|\.gap/\|tigap-skills" -n CLAUDE.md README.md docs commands skills .claude-plugin scripts` → no output, except historical text in `docs/kickoff.md` may remain only if clearly marked as history.

**Steps:**

- [ ] **Step 1: Rewrite `docs/artifact-layout.md` around `.tigerkit/`**

Use this content:

```markdown
# 산출물 구조

권장 프로젝트 로컬 산출물 구조:

```text
.tigerkit/{work_id}/
  inputs/
  requirements.md
  requirements.meta.json
  gap.md
  gap.meta.json
```

`/tk:prep`는 입력 자료와 대화 맥락을 `requirements.md`로 정리합니다. `/tk:gap`은 현재 repo 상태와 `requirements.md`의 차이를 `gap.md`에 기록합니다.

## 브랜치 이름과 작업 ID

현재 git 브랜치가 진행 중인 작업을 나타낸다면 그 브랜치 이름을 사용할 수 있습니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치 같은 기반 브랜치라면 변경 가능한 산출물을 쓰기 전에 다음 중 하나를 우선합니다.

- 사용자 승인 후 작업 브랜치를 만들거나 전환
- 사용자에게 짧은 작업 ID를 묻고 `.tigerkit/{work_id}/` 아래에 사용

브랜치를 자동으로 만들거나 전환하지 않습니다. git 브랜치를 확인할 수 없다면 사용자가 제공한 짧은 작업 ID를 사용합니다.

## 파일 책임

| 파일 | 역할 |
|---|---|
| `inputs/` | `requirements.md`를 만들 때 참고한 원문 자료, 메모, 캡처, 참고 코드 보관 위치 |
| `requirements.md` | 이번 작업의 정규화된 요구사항 기준 문서 |
| `requirements.meta.json` | `requirements.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `gap.md` | 현재 상태와 `requirements.md` 사이의 coverage/gap 분석 |
| `gap.meta.json` | `gap.md` 재사용 여부를 판단하는 캐시 메타데이터 |

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
|---|---|---|
| `req-needed` | `requirements.md` 없음 | `/tk:prep` 실행 |
| `gap-needed` | `requirements.md`는 있고 `gap.md` 없음 | `/tk:gap` 실행 |
| `gap-complete` | `gap.md` 있음 | Verdict와 Remaining Gaps를 보고 구현, 보류, 추가 확인 중 선택 |

## 캐시 정책

`/tk:prep`는 입력 자료 해시, prep 지시문 버전, 범위 해시, input identity가 같으면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`가 있으면 다시 생성합니다.

`/tk:gap`은 현재 git commit SHA, `requirements.md` 해시, gap 지시문 버전, 범위 해시가 같고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`가 있으면 다시 분석합니다.

각 명령은 cache hit/miss 이유를 사용자에게 짧게 표시합니다.
```

- [ ] **Step 2: Update installers**

In `scripts/install-standalone.sh`, replace `skills/prep` with `skills/prep` and final echo with:

```bash
echo "Installed TigerKit skills into: $TARGET_SKILLS"
echo "Standalone commands may be available as: /prep, /gap, /mwhat"
```

In `scripts/install-standalone.ps1`, replace `skills\prep` with `skills\prep` and final output with:

```powershell
Write-Host "Installed TigerKit skills into: $TargetSkills"
Write-Host "Standalone commands may be available as: /prep, /gap, /mwhat"
```

- [ ] **Step 3: Update `.claude-plugin/marketplace.json`**

Replace with:

```json
{
  "name": "tiger-kit",
  "owner": {
    "name": "MTGVim"
  },
  "metadata": {
    "description": "요구사항 정제, 답변 해독, 요구사항 대비 갭 확인을 돕는 TigerKit Claude Code 스킬 모음입니다."
  },
  "plugins": [
    {
      "name": "tk",
      "source": "./",
      "description": "요구사항 정제, 답변 해독, 요구사항 대비 갭 확인을 돕는 TigerKit Claude Code 스킬 모음입니다."
    }
  ]
}
```

- [ ] **Step 4: Update README and usage docs**

Make README command overview exactly use:

```markdown
제공하는 명령/스킬 흐름은 세 단계입니다.

- `/tk:mwhat` — 긴 LLM 답변이나 애매한 설명이 결국 무슨 말인지 짧고 실행 가능하게 풀어줍니다.
- `/tk:prep` — 외부 요구사항 소스와 대화 맥락을 `requirements.md` 기준 문서로 정리합니다.
- `/tk:gap` — `requirements.md` 대비 현재 구현, 문서, 테스트의 남은 차이를 확인합니다.
```

Make recommended flow:

```text
/tk:mwhat  # 장문/애매한 답변 해독
/tk:prep   # 요구사항 기준 정리
/tk:gap   # 기준 대비 갭 분석
```

Update installation examples to:

```text
/plugin marketplace add MTGVim/tiger-kit
/plugin install tk@tiger-kit
/reload-plugins
```

In `docs/usage.md`, rename sections to:

```markdown
## 1. 답변 해독
## 2. 요구사항 기준 정리
## 3. 갭 분석
```

and use `/tk:mwhat`, `/tk:prep`, `/tk:gap` in all examples.

- [ ] **Step 5: Update `CLAUDE.md`**

Change the language/output rules to mention:

```markdown
- 이 저장소에서 만드는 작업 산출물(`.tigerkit/{work_id}/requirements.md`, `.tigerkit/{work_id}/gap.md`)은 반드시 한글로 작성한다.
```

Change command overview to:

```markdown
- `/tk:mwhat`: 긴 LLM 답변이나 애매한 설명을 짧고 실행 가능하게 해독한다.
- `/tk:prep`: 외부 요구사항 소스와 대화 맥락을 `requirements.md` 기준 문서로 정리한다.
- `/tk:gap`: `requirements.md` 대비 현재 구현, 문서, 테스트의 남은 차이를 확인하고 `gap.md`를 작성한다.
```

Change repository structure bullets to use `commands/prep.md`, `skills/prep/SKILL.md`, and `.tigerkit/`.

- [ ] **Step 6: Verify docs and commit**

Run:

```bash
! grep -R "/tigap\|source-packet\|gap-report\|\.gap/\|tigap-skills" -n CLAUDE.md README.md docs commands skills .claude-plugin scripts
```

If the only matches are intentionally historical lines in `docs/kickoff.md`, either remove those lines or rewrite them as TigerKit current decisions.

Commit:

```bash
git add CLAUDE.md README.md docs/usage.md docs/artifact-layout.md docs/kickoff.md .claude-plugin/marketplace.json scripts/install-standalone.sh scripts/install-standalone.ps1
git commit -m "docs: document TigerKit tk workflow"
```

---

### Task 6: Validate plugin, clean old tracked paths, and commit plan artifacts

**Goal:** Ensure the repository is internally consistent before changing remote repository metadata.

**Files:**
- Inspect: all modified files
- Create/commit: `docs/superpowers/specs/2026-04-29-tigerkit-structure-design.md`
- Create/commit: `docs/superpowers/plans/2026-04-29-tigerkit-structure-implementation.md`
- Create/commit: `docs/superpowers/plans/2026-04-29-tigerkit-structure-implementation.md.tasks.json`

**Acceptance Criteria:**
- [ ] `claude plugin validate .claude-plugin/plugin.json` succeeds.
- [ ] `claude plugin validate .` succeeds.
- [ ] `git diff --check` succeeds.
- [ ] `git status --short` shows no tracked old `prep` file changes left unstaged.
- [ ] Pre-existing untracked workspaces are not staged.
- [ ] Plan/spec artifacts are committed.

**Verify:** `claude plugin validate .claude-plugin/plugin.json && claude plugin validate . && git diff --check && git status --short` → validation succeeds; status contains only expected untracked files not part of this work.

**Steps:**

- [ ] **Step 1: Run plugin validations**

Run:

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
```

Expected: all exit 0.

- [ ] **Step 2: Check old terminology in tracked surface**

Run:

```bash
! grep -R "/tigap\|source-packet\|gap-report\|\.gap/\|tigap-skills" -n CLAUDE.md README.md docs commands skills evals .claude-plugin scripts
```

Expected: command exits 0. If `docs/superpowers/plans/` old plan files match, exclude old historical plans from this check or leave them unmodified.

- [ ] **Step 3: Check git status carefully**

Run:

```bash
git status --short
```

Expected: changes from TigerKit implementation are tracked in staged/unstaged files; pre-existing untracked directories such as `docs/superpowers.backup-what-merge-20260429/` and `skills/prep-gap-eval-workspace/` remain untracked and are not staged unless the user explicitly asks.

- [ ] **Step 4: Commit spec and plan artifacts**

Run:

```bash
git add docs/superpowers/specs/2026-04-29-tigerkit-structure-design.md docs/superpowers/plans/2026-04-29-tigerkit-structure-implementation.md docs/superpowers/plans/2026-04-29-tigerkit-structure-implementation.md.tasks.json
git commit -m "docs: add TigerKit structure plan"
```

Expected: a new commit is created if these files were not already committed.

---

### Task 7: Rename GitHub repository slug and update local remote

**Goal:** Rename the uploaded GitHub repository from `MTGVim/tigap-skills` to `MTGVim/tiger-kit`, then update local origin to the new slug and push the completed branch.

**Files:**
- No repository file changes expected.
- Remote repository metadata changes via GitHub CLI.

**Acceptance Criteria:**
- [ ] `gh repo view --json nameWithOwner,url` shows `MTGVim/tigap-skills` before rename.
- [ ] `gh repo rename tiger-kit --yes` succeeds.
- [ ] `git remote -v` uses `git@github.com:MTGVim/tiger-kit.git` after update.
- [ ] `git push` succeeds to the renamed repository.
- [ ] `gh repo view MTGVim/tiger-kit --json nameWithOwner,url` shows the new slug.

**Verify:** `git remote -v && gh repo view MTGVim/tiger-kit --json nameWithOwner,url` → remote and GitHub metadata use `tiger-kit`.

**Steps:**

- [ ] **Step 1: Verify current GitHub repository**

Run:

```bash
gh repo view --json nameWithOwner,url
```

Expected before rename:

```json
{"nameWithOwner":"MTGVim/tigap-skills","url":"https://github.com/MTGVim/tigap-skills"}
```

- [ ] **Step 2: Rename the GitHub repository slug**

Run:

```bash
gh repo rename tiger-kit --yes
```

Expected: command exits 0 and GitHub repository slug becomes `MTGVim/tiger-kit`.

- [ ] **Step 3: Update local origin remote**

Run:

```bash
git remote set-url origin git@github.com:MTGVim/tiger-kit.git
git remote -v
```

Expected:

```text
origin	git@github.com:MTGVim/tiger-kit.git (fetch)
origin	git@github.com:MTGVim/tiger-kit.git (push)
```

- [ ] **Step 4: Push completed commits**

Run:

```bash
git push
```

Expected: push succeeds to `MTGVim/tiger-kit`.

- [ ] **Step 5: Verify renamed repository**

Run:

```bash
gh repo view MTGVim/tiger-kit --json nameWithOwner,url
```

Expected:

```json
{"nameWithOwner":"MTGVim/tiger-kit","url":"https://github.com/MTGVim/tiger-kit"}
```

- [ ] **Step 6: Optional local directory rename outside this session**

Do not rename the active working directory from inside this Claude Code session unless the user explicitly asks after the GitHub rename succeeds. Renaming the active CWD can break tool path assumptions. If requested after completion, run from the parent directory in a new shell:

```bash
mv /home/tigeryoo/workspace/tigap-skills /home/tigeryoo/workspace/tiger-kit
```

Expected: local checkout path changes to `/home/tigeryoo/workspace/tiger-kit`.

---

## Dependencies

- Task 1 must complete before Tasks 2-5 so eval contracts describe the new surface.
- Task 2 must complete before Tasks 3-5 because `prep` paths and plugin naming need to exist.
- Tasks 3 and 4 can run independently after Task 2.
- Task 5 should run after Tasks 2-4 so docs match final skill behavior.
- Task 6 runs after Tasks 1-5.
- Task 7 runs only after Task 6 succeeds and commits are ready to push.

## Self-Review

- Spec coverage: The plan covers `tk:what`, `tk:prep`, `tk:gap`, `.tigerkit/{work_id}/requirements.md`, `.tigerkit/{work_id}/gap.md`, no `audit` skill, no `tk:what` state-realignment mode, short user notifications, docs/evals/installers/manifests, validation, and GitHub slug rename.
- Placeholder scan: No `TBD`, `TODO`, `implement later`, or vague “write tests” placeholders are present.
- Type/name consistency: The plan consistently uses `prep_prompt_version`, `input_identities`, `requirements_hash`, `.tigerkit/`, `requirements.md`, `gap.md`, `/tk:prep`, `/tk:mwhat`, and `/tk:gap`.
- Risk note: GitHub repository rename and push are explicitly requested by the user, but they are still isolated to Task 7 after local validation succeeds.
