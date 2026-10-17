---
name: tk-adhd
description: "[user/auto] 답변과 작업 결과에서 핵심·실행할 단계·확인된 완료 상태를 쉽게 찾도록 출력 구조를 정리할 때 사용합니다. 세션 현황 복원, 인수인계 작성, 작업 실행, 의료 조언이나 스킬 유지보수의 담당자는 아닙니다."
disable-model-invocation: false
argument-hint: "<answer or task output to make actionable>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Actionable output

Shape the requested answer or the active owner's progress/result so the reader can find
what matters and act on it. This is presentation assistance, not a workflow, task executor,
medical inference or a session-status owner. Apply it to this response only; it neither stays
on across turns nor changes the active task's authority, checks or continuation rules.

Lead with the answer, verified result or the one user action actually needed. If the agent
already has authority and capability to do the work, keep doing it through its owner; do not
turn its tasks into commands the user must carry out or add a routine permission question.
For several user-performed steps, use a short numbered sequence of bounded actions. Group
long lists by relevance while retaining every requested item, material risk, caveat and source.
A small visible working set must not cap investigation, candidate generation or completeness.

Keep the task position and concrete verified completion easy to find when relevant, without
repeating a whole plan. Distinguish plans from execution, baseline capture from acceptance,
and local commits from confirmed publication. Describe an error's cause, impact and supported
next action calmly; retain uncertainty and blockers. Do not invent times, progress or success.
When no user action remains, end with the result; do not manufacture a follow-up task.

Explain fully when requested, using clear sections when useful. Suppress unrelated tangents
without silently omitting necessary alternatives or safety information. Preserve exact code,
commands, URLs, UI labels, terms and source qualifications. Output shaping never overrides
harness instructions, evidence, authorization or the requested depth/format.

A request for current-session orientation belongs to `tk-handoff`'s conversation-only branch;
durable handoff writing/resume belongs to its artifact branch. Do not inspect repositories,
other sessions or remote state merely to shape an answer, create a status ledger, or impose
an orientation card on unrelated future replies. Session learning and improvement diagnosis belong to `tk-retro`; implementation belongs to the authorized change owner
and its authorized implementation owner, not this output-shaping invocation.

For maintenance provenance, see [distillation](references/distillation.md).

<!-- tigerkit:artifact-paths -->
## Artifact Paths

This skill creates no artifacts. Do not create temporary files, write reports, or edit ignore rules for this invocation; return the result in the conversation.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Use this shared structure only for a final user-facing session-completion message. It does not replace an owning skill's required artifact, publication preview, machine-readable nested return, approval checkpoint, verdict/status field or footer, or final question block. Keep those contracts exact. Nested phase returns remain compact and emoji-free.

When no stricter owner format applies, keep the summary concise and use these headings in this order:

```text
### 🛠️ 변경/산출물        (내용이 있을 때만)
### ✅ 확인한 것          (항상; 실제 확인·실행 내용을 기록)
### 💭 결정              (기록할 결정이 있을 때만)
### 💡 권고              (실행 가능한 권고가 있을 때만)
### ⚠️ 한계              (예외, 실패, 미실행 또는 미해결 내용이 있을 때만)
### 🧹 정리              (항상; 정리한 자원 또는 추가 정리 대상 없음)
### 👤 사람이 할 일       (항상; 없음 또는 ID·이유·다음 행동)
```

Use emoji only at the start of section headings. Keep status and evidence values as exact machine-readable tokens. Omit empty optional sections. Report planned versus executed work and distinguish completed checks from skipped, failed, blocked or unverifiable work. Put every remaining user action, including uncovered manual rows, in `👤`; do not imply the user has no work when any remains. This is the last substantive block. If the owner requires a final question block, put `👤` immediately before it; if an exact status footer is mandatory, preserve it unchanged after the substantive blocks.

Put complete absolute artifact/evidence paths on their own final lines in the relevant block. `🧹` reports only actual cleanup or the absence of owned resources; do not claim cleanup that was not checked.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Show file paths as complete absolute paths; never abbreviate a path with `...` or `…`, including in examples, because terminal renderers make paths clickable. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

In chat responses, use a GFM pipe table for comparisons where several rows share at least two comparable attributes. Use a list for single-attribute enumerations. Keep tables narrow (about four columns or fewer), with a header row and short cells so they remain readable when the host shows raw pipes. Do not draw tables with box-drawing characters, wrap a table in a code fence, or emit an empty or ceremonial table. An owner-specific preview rule, such as summarizing a publication body's table in one line, takes precedence. These chat-table rules do not govern tables inside publication bodies or file artifacts.

In Markdown-rendered chat, documents and PR/issue bodies, write ranges with a hyphen (`146-149`) or spell out both endpoints. Escape a literal tilde as `\~` outside inline code and fenced code; preserve exact quotations and identifiers. Do not use unescaped tildes for prose ranges: GFM may render intervening text as strikethrough.

For authorized user-editable temporary input files, follow the owning skill's Artifact Paths input branch before creation and consumption. A prefilled template does not signal completed input; this rule grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

On an unmet prerequisite or before any user-owned question, read [question rounds and recovery](references/questions.md). Reuse identical content read this turn and still in context; hash-check uncertain copies. Another agent's read is insufficient. Resolve facts first, preserve authorization, and ask the whole answerable frontier in one plain-chat round. Skip ceremony when no decision remains; do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
---

❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Start the question block with a standalone horizontal rule (`---`) after the preceding context; do not add a `## Questions` or `## 질문` heading. Separate questions with blank lines and bold `❓ **Q<n> · ...**` title lines, without horizontal rules between questions. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

When a skill run reveals a reusable incident, preserve only minimal non-secret evidence and suggest a `tk-retro` review. Do not silently invoke it, create improvement artifacts, edit installed skills, or publish issues/PRs. Explicit implementation requests belong to the authorized change owner; this pointer grants no mutation authority.
<!-- /tigerkit:skill-feedback -->
