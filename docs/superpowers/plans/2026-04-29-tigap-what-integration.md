# tigap mwhat Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `/tigap:mwhat` to the existing `tigap-skills` plugin so confusing LLM answers can be turned into a short, friendly Korean action explanation.

**Architecture:** Follow the existing `prep`/`gap` plugin pattern: a short slash command entrypoint in `commands/mwhat.md`, detailed behavior in `skills/mwhat/SKILL.md`, and plugin registration in `.claude-plugin/plugin.json`. Documentation and evals are updated in the same repo so `mwhat → prep → gap` becomes the visible workflow.

**Tech Stack:** Claude Code plugin manifest JSON, Markdown command files, Markdown skill instructions, Bash/PowerShell standalone install scripts, JSON eval metadata.

---

## File Structure

- Create `commands/mwhat.md`: short slash command entrypoint for `/tigap:mwhat`.
- Create `skills/mwhat/SKILL.md`: full natural-language trigger and output behavior for the `mwhat` skill.
- Modify `.claude-plugin/plugin.json`: bump version from `1.1.1` to `1.2.0`, register the new command and skill.
- Modify `scripts/install-standalone.sh`: copy `skills/mwhat` in standalone mode and print `/mwhat` in the command list.
- Modify `scripts/install-standalone.ps1`: copy `skills\mwhat` in standalone mode and print `/mwhat` in the command list.
- Modify `README.md`: add `/tigap:mwhat` to the command overview and recommended workflow.
- Modify `docs/usage.md`: add a new first section explaining `/tigap:mwhat` and update recommended command phrases.
- Create `docs/kickoff.md`: capture the kickoff decisions from this conversation because no existing kickoff file was found during exploration.
- Modify `evals/evals.json`: add eval cases for `what` behavior.

---

### Task 1: Add `what` command and skill

**Goal:** Create the user-facing `/tigap:mwhat` entrypoint and the reusable skill instructions that define the approved Korean output format.

**Files:**
- Create: `commands/mwhat.md`
- Create: `skills/mwhat/SKILL.md`

**Acceptance Criteria:**
- [ ] `/tigap:mwhat` command file exists and delegates to the `mwhat` skill.
- [ ] `skills/mwhat/SKILL.md` triggers on Korean and English “what does this mean” prompts.
- [ ] The default output uses only `🤔 뭣? 쉽게 말하면` and `💡 추천`.
- [ ] The skill forbids vague hedging such as `~에 가까워요`.
- [ ] The skill says not to invent action when the source has no actionable content.

**Verify:** `test -f commands/mwhat.md && test -f skills/mwhat/SKILL.md && grep -q "뭣? 쉽게 말하면" skills/mwhat/SKILL.md`

**Steps:**

- [ ] **Step 1: Create the command directory and skill directory**

Run:

```bash
mkdir -p commands skills/mwhat
```

Expected: command exits with status 0.

- [ ] **Step 2: Write `commands/mwhat.md`**

Write this exact file:

```markdown
---
description: 긴 LLM 답변이나 애매한 설명이 결국 무슨 말인지 짧고 실행 가능하게 풀어줍니다.
---

이 플러그인의 `what` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자가 붙여넣은 긴 LLM 답변, 애매한 설명, 회의록식 덤프를 다시 길게 요약하지 말고 “이 말이 무슨 뜻인지”, “무엇을 하려던 건지”, “왜 막히는지”, “어떻게 답하면 되는지”로 짧게 정리합니다.

기본 출력은 `🤔 뭣? 쉽게 말하면`, `💡 추천` 두 블록을 사용합니다.

명시적으로 요청받지 않는 한 이 명령에서는 코드를 구현하거나 파일을 수정하지 않습니다.
```

- [ ] **Step 3: Write `skills/mwhat/SKILL.md`**

Write this exact file:

```markdown
---
name: mwhat
description: 긴 LLM 답변, 애매한 설명, 회의록식 덤프가 결국 무슨 말인지 모르겠을 때 반드시 사용합니다. 사용자가 “뭐라는거야”, “그래서 뭐 하라는 거야”, “이거 실행 가능하게 정리해줘”, “이 답변을 mwhat으로 정리해줘”, “what does this mean”, “turn this into an actionable spec”처럼 말하면 이 스킬로 짧은 한국어 실행 해설을 만듭니다.
---

# what

## 목적

긴 LLM 답변이나 애매한 설명을 다시 장황하게 요약하지 않고, 사용자가 바로 판단하거나 답할 수 있는 짧은 한국어 해설로 바꿉니다.

핵심 질문은 이것입니다.

```text
그래서 이 말이 무슨 뜻이고, 나는 지금 어떻게 답하면 되지?
```

## 동작 방식

사용자에게 보이는 응답은 기본적으로 한글로 작성합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

이 스킬은 구현, 파일 수정, 계획 수립을 하지 않습니다. 사용자가 제공한 답변이나 설명을 해석해서 실행 가능한 다음 말로 줄이는 데 집중합니다.

## 기본 출력 형식

기본 출력은 두 블록만 사용합니다.

```md
🤔 뭣? 쉽게 말하면
음, 이 말은 A를 하자는 뜻이에요. 그런데 지금 바로 시작하면 안 되고, 먼저 B 기준부터 정해야 해요.

🎯 하던 것
- A 방향으로 문제를 풀려고 했어요.
- B를 기준으로 작업 범위를 잡으려고 했어요.

😵 문제 상황
- B 기준이 아직 없어요.
- 누가 어디까지 할지도 정해지지 않았어요.

💡 추천
“방향은 이해했습니다. 진행하려면 B 기준과 담당 범위를 먼저 정해야 할 것 같습니다.”
```

### 블록별 역할

- `🤔 뭣? 쉽게 말하면`: 원문이 실제로 말하는 핵심을 1~3문장으로 바로 해석합니다.
- `🎯 하던 것`: 원문 작성자나 LLM이 하려던 목표, 방향, 의도를 정리합니다.
- `😵 문제 상황`: 원문만 보고 바로 움직이기 어려운 이유를 정리합니다.
- `💡 추천`: 사용자가 상대나 LLM에게 보낼 수 있는 문장을 제공합니다.

## 말투

친절하고 부드럽지만 단정적으로 말합니다. 딱딱한 보고서체보다 편한 해설자 톤을 사용하되, 결과는 업무 대화에 붙여도 어색하지 않아야 합니다.

선호 표현:

- `이 말은 ...라는 뜻이에요.`
- `핵심은 ...예요.`
- `지금 바로 할 수 없는 이유는 ...예요.`
- `이렇게 답하면 됩니다.`

피할 표현:

- `~에 가까워요`
- `아마도`를 남발하는 문장
- `일 수도 있어요`를 남발하는 문장
- 과한 역할극, 플러팅, 밈만 있는 문장
- 원문보다 길어지는 재요약

## 판단 규칙

1. 원문보다 훨씬 짧게 씁니다.
2. 원문에 없는 일을 만들어내지 않습니다.
3. 확실한 내용과 추정한 내용을 섞지 않습니다.
4. 원문이 이미 실행 가능하면 `😵 문제 상황`에는 “크게 막히는 지점은 없어요”라고 짧게 씁니다.
5. 원문에 실질 액션이 없으면 `🎯 하던 것`과 `😵 문제 상황`에서 그 사실을 분명히 말합니다.
6. `💡 추천`은 사용자가 복사해서 보낼 수 있는 문장으로 씁니다.

## 선택 블록

기본 두 블록으로 충분하면 선택 블록을 쓰지 않습니다. 원문에 빠진 조건이나 결정사항이 뚜렷할 때만 아래 블록을 추가할 수 있습니다.

```md
🧩 빠진 정보
- ...

⚖️ 결정할 것
- ...
```

선택 블록을 추가하더라도 전체 응답은 짧게 유지합니다.

## 예시

입력:

```text
이 기능은 확장성을 고려해서 모듈화하고, 상태 관리는 나중에 요구사항이 명확해지면 정하는 게 좋겠습니다. 우선 데이터 흐름을 정리하고 컴포넌트 경계를 잡는 방향으로 접근하면 될 것 같습니다.
```

출력:

```md
🤔 뭣? 쉽게 말하면
음, 이 말은 “지금 바로 구현하지 말고 구조부터 정하자”는 뜻이에요. 상태 관리 방식은 아직 정하지 말고, 데이터 흐름과 컴포넌트 경계부터 잡자는 말이에요.

🎯 하던 것
- 기능을 바로 만들기 전에 구조를 먼저 나누려고 했어요.
- 상태 관리 선택을 뒤로 미루려고 했어요.
- 데이터 흐름과 컴포넌트 책임을 먼저 정하려고 했어요.

😵 문제 상황
- 어떤 컴포넌트를 어디까지 나눌지 기준이 없어요.
- “나중에” 정할 상태 관리의 조건이 없어요.
- 그래서 이 답변만으로는 바로 구현 범위를 잡기 어려워요.

💡 추천
“좋습니다. 그러면 이번 단계에서는 구현보다 데이터 흐름과 컴포넌트 경계를 먼저 정리하겠습니다. 상태 관리는 어떤 조건이 정해졌을 때 결정하면 될지도 같이 적어두겠습니다.”
```

## 중단 조건

사용자가 실제 구현, 파일 수정, 테스트 실행을 요청하면 이 스킬만으로 진행하지 말고, 먼저 이 해석이 맞는지 짧게 확인합니다. `what`은 실행 전에 말을 이해시키는 스킬입니다.
```

- [ ] **Step 4: Verify the files exist and contain the approved headings**

Run:

```bash
test -f commands/mwhat.md && test -f skills/mwhat/SKILL.md && grep -q "🤔 뭣? 쉽게 말하면" skills/mwhat/SKILL.md && grep -q "💡 추천" skills/mwhat/SKILL.md
```

Expected: command exits with status 0.

- [ ] **Step 5: Commit this task**

Run:

```bash
git add commands/mwhat.md skills/mwhat/SKILL.md
git commit -m "feat: add what skill and command"
```

Expected: a new commit is created.

---

### Task 2: Register `what` in plugin metadata and standalone installers

**Goal:** Make `/tigap:mwhat` available through the plugin manifest and make standalone installs include the new skill.

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `scripts/install-standalone.sh`
- Modify: `scripts/install-standalone.ps1`

**Acceptance Criteria:**
- [ ] Plugin version is `1.2.0`.
- [ ] Manifest commands include `./commands/mwhat.md`.
- [ ] Manifest skills include `./skills/mwhat`.
- [ ] Bash standalone installer copies `skills/mwhat`.
- [ ] PowerShell standalone installer copies `skills\mwhat`.
- [ ] Standalone install output mentions `/prep, /gap, /mwhat`.

**Verify:** `python -m json.tool .claude-plugin/plugin.json >/dev/null && grep -q './commands/mwhat.md' .claude-plugin/plugin.json && grep -q 'skills/mwhat' scripts/install-standalone.sh scripts/install-standalone.ps1`

**Steps:**

- [ ] **Step 1: Replace `.claude-plugin/plugin.json` with registered `what` metadata**

Write this exact JSON:

```json
{
  "name": "tigap",
  "description": "모호한 요청과 흩어진 자료를 작업 기준으로 정리하고 현재 상태와의 갭을 분석하는 Claude Code 스킬 모음입니다.",
  "version": "1.2.0",
  "author": {
    "name": "MTGVim"
  },
  "commands": [
    "./commands/prep.md",
    "./commands/gap.md",
    "./commands/mwhat.md"
  ],
  "skills": [
    "./skills/prep",
    "./skills/gap",
    "./skills/mwhat"
  ]
}
```

- [ ] **Step 2: Replace `scripts/install-standalone.sh` with `what` support**

Write this exact file:

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_PROJECT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_SKILLS="$TARGET_PROJECT/.claude/skills"

mkdir -p "$TARGET_SKILLS"
cp -R "$REPO_ROOT/skills/prep" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/gap" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/mwhat" "$TARGET_SKILLS/"

echo "Installed tigap skills into: $TARGET_SKILLS"
echo "Standalone commands may be available as: /prep, /gap, /mwhat"
```

- [ ] **Step 3: Replace `scripts/install-standalone.ps1` with `what` support**

Write this exact file:

```powershell
param(
  [string]$TargetProject = "."
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$TargetSkills = Join-Path $TargetProject ".claude\skills"

New-Item -ItemType Directory -Force -Path $TargetSkills | Out-Null
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\prep") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\gap") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\mwhat") $TargetSkills

Write-Host "Installed tigap skills into: $TargetSkills"
Write-Host "Standalone commands may be available as: /prep, /gap, /mwhat"
```

- [ ] **Step 4: Verify manifest JSON and installer references**

Run:

```bash
python -m json.tool .claude-plugin/plugin.json >/dev/null
grep -q './commands/mwhat.md' .claude-plugin/plugin.json
grep -q './skills/mwhat' .claude-plugin/plugin.json
grep -q 'skills/mwhat' scripts/install-standalone.sh
grep -q 'skills\\what' scripts/install-standalone.ps1
```

Expected: every command exits with status 0.

- [ ] **Step 5: Commit this task**

Run:

```bash
git add .claude-plugin/plugin.json scripts/install-standalone.sh scripts/install-standalone.ps1
git commit -m "chore: register what in tigap plugin"
```

Expected: a new commit is created.

---

### Task 3: Document the `mwhat → prep → gap` workflow and kickoff decisions

**Goal:** Make the new command discoverable and preserve the design decisions from the kickoff conversation.

**Files:**
- Modify: `README.md`
- Modify: `docs/usage.md`
- Create: `docs/kickoff.md`

**Acceptance Criteria:**
- [ ] README lists `/tigap:mwhat`, `/tigap:prep`, and `/tigap:gap`.
- [ ] README recommended flow is `mwhat → prep → gap`.
- [ ] Usage docs explain when to use `/tigap:mwhat`.
- [ ] Usage docs include `/tigap:mwhat` in recommended command phrases.
- [ ] `docs/kickoff.md` summarizes the approved `what` design and integration decision.

**Verify:** `grep -q '/tigap:mwhat' README.md docs/usage.md docs/kickoff.md && grep -q 'mwhat → prep → gap' README.md docs/kickoff.md`

**Steps:**

- [ ] **Step 1: Update the README command list and flow**

Change the opening command list so it states:

```markdown
제공하는 명령/스킬 흐름은 세 단계입니다.

- `/tigap:mwhat` — 긴 LLM 답변이나 애매한 설명이 결국 무슨 말인지 짧고 실행 가능하게 풀어줍니다.
- `/tigap:prep` — 아이디어, 대화 맥락, 별도 자료를 이번 작업의 기준 자료로 정리합니다.
- `/tigap:gap` — 캡처된 작업 기준과 현재 구현, 문서, 동작 사이의 갭을 분석합니다.
```

Change the recommended flow block to:

```markdown
```text
/tigap:mwhat  # 장문/애매한 답변 해독
/tigap:prep  # 작업 기준 정리
/tigap:gap   # 기준 대비 갭 분석
```
```

Change the standalone sentence to:

```markdown
Standalone 모드에서는 같은 흐름을 `/mwhat`, `/prep`, `/gap`으로 호출합니다.
```

Add this sentence after the workflow explanation:

```markdown
흐름으로 보면 `mwhat → prep → gap`입니다. 먼저 말뜻과 막히는 지점을 풀고, 그다음 작업 기준으로 고정한 뒤, 마지막으로 현재 상태와의 차이를 봅니다.
```

- [ ] **Step 2: Add `/tigap:mwhat` to `docs/usage.md` as the first command section**

Insert this section before the current `## 1. 작업 기준 정리` section:

```markdown
## 1. 답변 해독

긴 LLM 답변, 애매한 설명, 회의록식 덤프가 결국 무슨 말인지 모르겠을 때 실행합니다.

```text
/tigap:mwhat <긴 답변, 설명, 또는 정리 요청>
```

예시:

```text
/tigap:mwhat 이 답변 뭐라는거야?
/tigap:mwhat 아래 LLM 답변을 실행 가능하게 정리해줘.
/tigap:mwhat 그래서 내가 뭐라고 답하면 되는지 알려줘.
```

기본 출력은 두 블록입니다.

```text
🤔 뭣? 쉽게 말하면
🎯 하던 것
😵 문제 상황
💡 추천
```

이 명령은 코드를 구현하거나 파일을 수정하지 않습니다. 먼저 말뜻, 의도, 막히는 지점, 사용자가 보낼 수 있는 답장을 짧게 정리합니다.
```

Then renumber the existing headings:

```markdown
## 2. 작업 기준 정리
## 3. 갭 분석
```

Update the recommended command block to:

```markdown
```text
/tigap:mwhat 이 긴 답변 뭐라는 건지 정리해줘.
/tigap:prep 앞선 대화 기준으로 작업 기준 정리해줘.
/tigap:gap 방금 정리한 기준 대비 현재 구현 갭 분석해줘.
```
```

- [ ] **Step 3: Create `docs/kickoff.md`**

Write this exact file:

```markdown
# Kickoff Notes

## 2026-04-29: `what` command and skill

`what` started from the user’s frustration with long LLM answers that sound detailed but do not make the next action clear. The desired interaction is: when the user thinks “뭐라는거야?”, Claude should stop elaborating and translate the answer into a short, usable explanation.

Approved name: `what`.

Approved integration: add it to the existing `tigap-skills` plugin instead of keeping a separate repository. The product flow becomes:

```text
mwhat → prep → gap
해독 → 기준화 → 차이분석
```

Approved default output:

```md
🤔 뭣? 쉽게 말하면
...

🎯 하던 것
...

😵 문제 상황
...

💡 추천
...
```

Tone decisions:

- Use Korean by default.
- Make the voice friendly, warm, and direct.
- Avoid stiff default LLM wording.
- Avoid vague hedging such as `~에 가까워요`.
- Keep the final `이렇게 답하면 됨` block practical enough to paste into work chat.
- Do not turn the skill into heavy roleplay or meme-only output.

Behavior decisions:

- Do not create another long summary.
- Explain what the source answer meant.
- Explain what the source answer was trying to do.
- Explain why the user cannot act on it yet.
- Provide a message the user can send or adapt.
- Do not invent work when the source answer has no real action.
```

- [ ] **Step 4: Verify docs mention the new flow**

Run:

```bash
grep -q '/tigap:mwhat' README.md
grep -q '/tigap:mwhat' docs/usage.md
grep -q 'mwhat → prep → gap' README.md
grep -q 'mwhat → prep → gap' docs/kickoff.md
grep -q '뭣? 쉽게 말하면' docs/kickoff.md
```

Expected: every command exits with status 0.

- [ ] **Step 5: Commit this task**

Run:

```bash
git add README.md docs/usage.md docs/kickoff.md
git commit -m "docs: document what workflow kickoff"
```

Expected: a new commit is created.

---

### Task 4: Add eval coverage for `what`

**Goal:** Add objective eval prompts so future changes can check that `mwhat` preserves the approved format and behavior.

**Files:**
- Modify: `evals/evals.json`

**Acceptance Criteria:**
- [ ] Evals include a confusing LLM answer case.
- [ ] Evals include an already-actionable answer case.
- [ ] Evals include a no-action answer case.
- [ ] Each `mwhat` eval checks the approved four block labels.
- [ ] JSON remains valid.

**Verify:** `python -m json.tool evals/evals.json >/dev/null && grep -q 'mwhat-confusing-answer' evals/evals.json && grep -q 'mwhat-no-action' evals/evals.json`

**Steps:**

- [ ] **Step 1: Replace `evals/evals.json` with expanded workflow evals**

Write this exact JSON:

```json
{
  "skill_name": "tigap-workflow",
  "evals": [
    {
      "id": 0,
      "name": "prep-cache-hit",
      "prompt": "You are evaluating the tigap prep skill instructions. A project already has .gap/checkout-retry/normalized/source-packet.md and .gap/checkout-retry/normalized/source-packet.meta.json. The meta fields input_source_hash, prep_prompt_version, scope_hash, and source_identities all match the current request. The user runs: /tigap:prep checkout retry 기준 자료 다시 정리해줘. Describe exactly what Claude should do and what the user-facing response should include. Do not write files.",
      "expected_output": "Should reuse the existing source-packet, state cache hit reason briefly, include the source-packet path, keep the response short with a three-line-or-less summary, and avoid dumping the whole source-packet.",
      "files": [],
      "expectations": [
        "Says the existing source-packet should be reused because cache keys match",
        "Names the source-packet path in the user-facing response",
        "Says the user-facing response should be short and include a three-line-or-less summary",
        "Does not instruct regenerating source-packet or metadata on cache hit"
      ]
    },
    {
      "id": 1,
      "name": "prep-force-miss",
      "prompt": "You are evaluating the tigap prep skill instructions. A previous source-packet exists for .gap/search-filter/normalized/source-packet.md, but the user runs: /tigap:prep --force docs/search-filter.md 기준으로 다시 정리해줘. Describe exactly what Claude should do and what the user-facing response should include. Do not write files.",
      "expected_output": "Should ignore the cache because --force was requested, regenerate source-packet and metadata, briefly explain the force/cache miss reason, show the path, and keep the chat response short.",
      "files": [],
      "expectations": [
        "Says --force makes Claude ignore or bypass the existing cache",
        "Says source-packet should be regenerated from docs/search-filter.md",
        "Says source-packet metadata should be updated or regenerated",
        "Says the user-facing response should include the path and stay short"
      ]
    },
    {
      "id": 2,
      "name": "gap-report-ux",
      "prompt": "You are evaluating the tigap gap skill instructions. A source-packet exists at .gap/onboarding-copy/normalized/source-packet.md, the repository has relevant docs and code paths, and the user runs: /tigap:gap 방금 정리한 기준 대비 현재 구현 갭 분석해줘. Describe the expected report structure and the final user-facing response. Do not write files.",
      "expected_output": "Should describe cache check based on git commit, source-packet hash, gap prompt version, and scope; write/reuse gap-report with metadata; keep findings minimally structured with category/content/evidence/next action; end report with one Next Move; final chat response should not dump the full report and should include path, summary table, key issues, and one next move.",
      "files": [],
      "expectations": [
        "Describes gap cache checking with git commit, source-packet hash, prompt version, and scope",
        "Mentions gap-report metadata",
        "Requires each finding to include category, content, evidence, and next action",
        "Ends the report with exactly one Next Move rather than a numbered list of choices",
        "Says the chat response should not dump the full report and should include path, summary table, key issues, and one next move"
      ]
    },
    {
      "id": 3,
      "name": "mwhat-confusing-answer",
      "prompt": "You are evaluating the tigap what skill instructions. The user runs /tigap:mwhat with this source answer: '이 기능은 확장성을 고려해서 모듈화하고, 상태 관리는 나중에 요구사항이 명확해지면 정하는 게 좋겠습니다. 우선 데이터 흐름을 정리하고 컴포넌트 경계를 잡는 방향으로 접근하면 될 것 같습니다.' Describe the expected user-facing response. Do not write files.",
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
    },
    {
      "id": 4,
      "name": "what-already-actionable",
      "prompt": "You are evaluating the tigap what skill instructions. The user runs /tigap:mwhat with this source answer: '먼저 src/auth/session.ts의 만료 시간 계산을 30분으로 바꾸고, tests/auth/session.test.ts에 만료 케이스를 추가한 뒤 npm test -- auth/session.test.ts를 실행하세요.' Describe the expected user-facing response. Do not write files.",
      "expected_output": "Should use the two approved Korean blocks, say the answer is already actionable, keep the blocked section short, and provide a concise confirmation reply.",
      "files": [],
      "expectations": [
        "Includes the two approved block labels",
        "Says the source answer is already actionable or has no major blocking point",
        "Does not invent additional tasks beyond editing src/auth/session.ts, adding tests, and running the named test command",
        "Provides a concise message the user can send or adapt"
      ]
    },
    {
      "id": 5,
      "name": "mwhat-no-action",
      "prompt": "You are evaluating the tigap what skill instructions. The user runs /tigap:mwhat with this source answer: '좋은 질문입니다. 이 주제는 여러 관점에서 볼 수 있으며, 상황과 맥락에 따라 접근이 달라질 수 있습니다. 충분히 고민해보는 것이 중요합니다.' Describe the expected user-facing response. Do not write files.",
      "expected_output": "Should use the two approved Korean blocks, clearly state that there is no actionable content, avoid inventing work, and provide a reply asking for concrete criteria or next steps.",
      "files": [],
      "expectations": [
        "Includes the two approved block labels",
        "States that the source answer has no real actionable content",
        "Does not invent implementation steps or decisions not present in the source",
        "Provides a reply asking for concrete criteria, options, or next steps"
      ]
    }
  ]
}
```

- [ ] **Step 2: Verify JSON validity and eval names**

Run:

```bash
python -m json.tool evals/evals.json >/dev/null
grep -q 'mwhat-confusing-answer' evals/evals.json
grep -q 'what-already-actionable' evals/evals.json
grep -q 'mwhat-no-action' evals/evals.json
```

Expected: every command exits with status 0.

- [ ] **Step 3: Commit this task**

Run:

```bash
git add evals/evals.json
git commit -m "test: add what skill eval coverage"
```

Expected: a new commit is created.

---

### Task 5: Validate, commit plan artifacts, and push

**Goal:** Validate the integrated plugin, commit the planning artifacts, and push the approved changes to the tracked remote branch.

**Files:**
- Create: `docs/superpowers/plans/2026-04-29-tigap-what-integration.md`
- Create: `docs/superpowers/plans/2026-04-29-tigap-what-integration.md.tasks.json`

**Acceptance Criteria:**
- [ ] Plugin manifest validation passes.
- [ ] Repository plugin validation passes.
- [ ] Whitespace check passes.
- [ ] Git status only contains the known untracked `skills/prep-gap-eval-workspace/` outside this work.
- [ ] Plan artifacts are committed.
- [ ] Branch is pushed to its tracked remote.

**Verify:** `claude plugin validate .claude-plugin/plugin.json && claude plugin validate . && git diff --check && git status --short --branch`

**Steps:**

- [ ] **Step 1: Validate plugin manifest and repository**

Run:

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
```

Expected: validation commands pass and `git diff --check` exits with status 0.

- [ ] **Step 2: Check working tree before final commit**

Run:

```bash
git status --short --branch
```

Expected: modified or untracked files from this work are limited to committed plan artifacts. The pre-existing untracked `skills/prep-gap-eval-workspace/` may still appear and must not be staged.

- [ ] **Step 3: Commit plan artifacts**

Run:

```bash
git add docs/superpowers/plans/2026-04-29-tigap-what-integration.md docs/superpowers/plans/2026-04-29-tigap-what-integration.md.tasks.json
git commit -m "docs: add what integration plan"
```

Expected: a new commit is created.

- [ ] **Step 4: Push the branch**

Run:

```bash
git push
```

Expected: push succeeds to the branch tracked by `main...origin/main`.
```
