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

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Resolve researchable facts and reuse matching authorization before asking.
For an unmet prerequisite or material user-owned decision, read [question rounds and recovery](references/questions.md)
(reuse it if still in context). Ask only answerable decisions in its plain-chat format,
with approval separate. Otherwise continue without confirmation.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence and suggest `tk-retro`.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
