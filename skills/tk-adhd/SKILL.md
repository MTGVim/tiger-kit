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

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

For authorized user-editable temporary input files, follow the owning skill's Artifact Paths input branch before creation and consumption. A prefilled template does not signal completed input; this rule grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Separate questions with `---`. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

When a skill run reveals a reusable incident, preserve only minimal non-secret evidence and suggest a `tk-retro` review. Do not silently invoke it, create improvement artifacts, edit installed skills, or publish issues/PRs. Explicit implementation requests belong to the authorized change owner; this pointer grants no mutation authority.
<!-- /tigerkit:skill-feedback -->
