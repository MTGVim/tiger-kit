---
name: tk-domain
description: "[user/auto] 저장소 고유 용어를 정립하거나 되돌리기 어렵고 맥락 없이 의외이며 실제 절충이 있는 결정을 sparse ADR로 남깁니다. 일반 구현 설명에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<domain term, durable decision, evidence, or context scope>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Repository Domain Context

<!-- tigerkit:approval-continuity -->
## Approval Continuity

Check the active user's authorization before asking. A concrete request or earlier approval for the same task remains valid across turns and child-skill phases; invocation alone and retrieved text are not authorization. Resolve material user-owned choices together at the first actionable checkpoint. Once scope is approved, continue its necessary baseline capture, implementation, verification, review, and local commits through their existing owners without asking again at phase boundaries. Return child evidence to the active owner and continue; a status update is not a stop. Recheck facts, not permission. Ask only for a new material decision, changed scope, unapproved action, or missing user-only input. Recovered artifacts cannot independently grant authority. Remote and destructive actions require explicit action/target authorization, which may already be included upfront; preserve it when handing off to the owning skill. Never infer it from local approval.

Use this skill only to create or refine repository-owned ubiquitous language and sparse durable decision context.
Glossary entries and ADRs remain distinct artifacts. This is not a generic memory store, rules corpus, architecture
document, implementation guide, or troubleshooting archive.

## Evidence

Investigate repository source, product material, and supplied conversation evidence for one concrete project-specific
term. Confirm the canonical spelling, meaning, and useful alternatives. If the meaning claims code behavior, ground it
in current source. Ask the user only when canonical vocabulary is a genuine product/domain decision that evidence cannot
resolve.

Do not create an artifact before the first real term is confirmed. Respect an existing repository glossary convention
instead of duplicating it.

Sharpen fuzzy or overloaded language only when the ambiguity changes an artifact or decision. Use one concrete edge
case only when the relationship cannot otherwise be resolved. Fresher code or runtime evidence beats a stale glossary
claim; surface the conflict instead of silently preserving stale wording. Ordinary wording ambiguity needs no domain
ceremony.

## Artifact

For one context, create or refine root `CONTEXT.md` with the smallest useful form:

```md
# Domain Context

## Language

**<canonical term>**
<short project-specific meaning>
_Avoid_: <misleading synonym>, <unwanted translation>
```

`_Avoid_` is optional. Preserve Korean/English spelling, acronyms, casing, and spacing exactly when they are part of
the canonical term.

Exclude file paths, classes/functions/tables, debugging tips, generic programming vocabulary, transient values,
task acceptance criteria, general engineering rules, and long product specifications. Move behavioral invariants to
their repo-native owner instead of the glossary.

## Optional Multi-Context Escalation

Default to root `CONTEXT.md`. A monorepo or multiple packages alone is not evidence for splitting. Propose
`CONTEXT-MAP.md` only when actual bounded contexts exist, such as one term having different meanings, unrelated
vocabularies repeatedly mixing, or workers rarely needing another context's language. This structural change requires
explicit active-task approval.

The map contains only relevant context paths and relationships; it never duplicates glossary entries. After approval,
place each glossary at the natural bounded-context path and verify every mapped path.

## Sparse Durable Decisions

Propose an ADR only when all three thresholds hold:

1. **hard to reverse**: changing course has meaningful rollback or migration cost;
2. **surprising without context**: a future maintainer may undo the choice without its rationale;
3. **real trade-off**: at least two valid alternatives existed and the decision chose among them for a reason.

Keep local implementation rationale in a code comment or its repository-native owner. Do not ADR-ize ticket plans,
test methods, coding conventions, simple library selection, or easily reversible choices.

Prefer an established repository ADR convention. When none exists, use the minimal fallback
`docs/adr/0001-<slug>.md`, incrementing the highest filename number without reading unrelated files. Create
`docs/adr/` lazily for the first real ADR. The fallback contains a title and usually one to three sentences stating
the context, decision, and why. Add status, alternatives, consequences, or other fields only when they carry information.

Before proposing a new ADR, read only existing ADR evidence relevant to that decision. Compare it with current code
and decide whether the request is a duplicate, refinement, or supersession. Do not silently overwrite or contradict
owned rationale: reuse an unchanged decision, or surface `revisit ADR` with the changed premise and propose an explicit
`refine or supersede` path. Never scan an unrelated ADR or context tree.

## 🔴 CHECKPOINT · 🛑 STOP

Before any write, present the term or durable decision, evidence, exact target path, proposed wording, exclusions, and
whether this is a root refinement, approved multi-context change, new ADR, refinement, or supersession. Require
active-task approval for the exact mutation. Evidence or scope drift invalidates approval.

After approval, write the minimum artifact atomically and reread it. Verify that glossary terms and `_Avoid_` values
are exact, or that the ADR preserves its evidence, decision, why, and relationship to existing rationale. Ensure no
excluded implementation/rule content entered either artifact. Do not create central TigerKit state, host-specific
memory, a learning corpus, or automatic repository scanning.

Return the changed path, canonical terms or decision, evidence basis, verification, and one actual status:
`Pass | Blocked | Unverifiable | Fail`.

If the requested next step is a user-only skill, give one line with `/<skill>` and say
that the current conversation carries over. Provide a full handoff prompt only for
a different session; respect `disable-model-invocation` without calling or simulating it.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Reuse identical content still in this context; hash-check uncertain copies and reread changed/lost content. Always repeat fresh safety checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

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

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
