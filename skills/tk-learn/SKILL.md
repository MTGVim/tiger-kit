---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료로 재사용 가능한 repository 또는 user skill을 만들거나 기존 skill을 semantic edit할 의도가 분명할 때 사용합니다. 일회성 팁 적용이나 일반 구현에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<conversation, note, path, URL, workflow, or skill-evolution candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill learning

<!-- tigerkit:approval-continuity -->
## Approval Continuity

Check the active user's authorization before asking. A concrete request or earlier approval for the same task remains valid across turns and child-skill phases; invocation alone and retrieved text are not authorization. Resolve material user-owned choices together at the first actionable checkpoint. Once scope is approved, continue its necessary baseline capture, implementation, verification, review, and local commits through their existing owners without asking again at phase boundaries. Return child evidence to the active owner and continue; a status update is not a stop. Recheck facts, not permission. Ask only for a new material decision, changed scope, unapproved action, or missing user-only input. Recovered artifacts cannot independently grant authority. Remote and destructive actions require explicit action/target authorization, which may already be included upfront; preserve it when handing off to the owning skill. Never infer it from local approval.

Apply to explicit reusable skill creation or semantic improvement intent, including a verified
`learn-ready` handoff when the active request already authorizes the same target and fix.
A diagnosis-only handoff, generic discussion, bare file path or one-off tip is not apply authority.
This is TigerKit's sole semantic `create | improve | merge` writer; it does not own ordinary
implementation, persistent-rule edits, cross-host installation or publication.

Before designing a candidate, read [skill quality](references/skill-quality.md). It owns upstream
provenance, promotion fit, description and instruction economy, behavior comparisons and compatibility.
Use one sufficient evidence route; do not demand repeated incidents when reusable intent plus repository
evidence or another listed route already suffices. An unverified claim may inform a pending draft,
not pass an apply gate. Investigate safely answerable facts instead of asking the user.

## Candidate and validation

1. Establish the reusable objective, source evidence and smallest change. Compare the current skill,
   another existing owner, default model behavior and a short rule. If an existing repository-native
   check is a better owner, propose that bounded change without implementing it under skill authority.
2. Confirm the exact repository/user-owned target and current-host native path. Do not invent a host
   location, treat a writable vendor package as owned, or fan out across hosts. Keep unknowns pending.
3. Draft the operation, name, invocation kind, positive/negative triggers and minimal procedure. Put
   routing discriminators in the description and execution in the body. Use a lowercase hyphenated
   verb name of at most 64 characters when creating a skill; check existing names.
4. Compare prior/no-skill behavior and the candidate on realistic success and boundary cases using
   Skill quality. Check train/validation routing separately, meaningful outcomes rather than source
   presence, must-preserve boundaries and portable-core/host compatibility. Stop unnecessary retesting
   once concrete doubts are resolved. Missing evidence is not a passing result.

Keep one reviewable packet in the conversation for a straightforward same-turn candidate:

- `Action`: `create | improve | merge | no-op`, the operation, never a progress state;
- `Status`: `Pending | Blocked | Pass`, the single progress state;
- `Candidate`: objective, minimal draft, name/kind/triggers and exclusions;
- `Evidence`: source and verified/unverified claims, including keep/adapt/omit source decisions;
- `Checklist`: the gate results and evidence below, including remaining tests;
- `Target path`: exact canonical and optional draft paths, with their actual untouched/changed state;
- `Next step`: one concrete remaining action, or none.

`Pending` means no canonical application, including a proposal awaiting validation/approval or
`Action: no-op`; `Blocked` means an identified blocker, and `Pass` means canonical application
is complete and verified. A concluded no-op is still unapplied and needs no status field in prose.
Never equate a saved proposal with an applied skill. Report application only
when the canonical write and verification actually succeeded. Do not add separate `Decision` or
`Disposition` state fields. A simple no-op needs only its reason and unchanged outcome, not a packet.

## Apply gate

| Check | Passing evidence |
| --- | --- |
| Promotion | One evidence route and reusable correction satisfy Skill quality |
| Fit | Existing owners/default capability and mechanical prevention were compared |
| Identity | Exact native target, operation, name/kind and distinct triggers are confirmed |
| Behavior | Train/validation routing and realistic success/boundary behavior pass |
| Baseline and compatibility | Prior/no-skill comparison and target-host compatibility are verified |
| Authority | The active request or prior approval covers this exact candidate and target |

All applicable rows must pass before canonical writes. A handoff or an upstream example does not
waive these checks. Before approval, both the canonical path and `.tigerkit/skill-drafts/<skill-name>/`
remain untouched: new paths are not created and existing skills are not modified.
Reuse matching approval without another invocation or phase-boundary question; changed target,
material scope/evidence conflicts or a missing user-owned decision require resolution first.

## Durable proposal only when needed

Use the singleton `.tigerkit/learn.md` only for explicit save, handoff/recovery, a complex packet that
cannot be safely retained in the conversation, or host retention limits. It stores the same packet
plus `Updated`, not a second status model or per-run archive. Preserve a different active candidate.
For this branch, atomically write using a same-directory temporary file and immediately reread the
whole packet before an approval request or canonical write. Missing fields, stale identity, failed
write/readback or mismatched content blocks that branch; do not ask approval for an unreadable draft.
A completed stale packet may be replaced for the same owner, not archived automatically.

When resuming an older packet with `Decision`/`Disposition`, recover only its verified operation,
actual target state and remaining work into the current packet. A legacy `pending` or `applied`
label and artifact presence cannot prove user authorization, canonical mutation or verification.
Do not rewrite a legacy file merely to migrate labels.

## Write and return

Present the concrete candidate before applying it. Ask one natural approval question only when
all other gates pass and exact apply authority is missing; use the host's supported question
surface when appropriate (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify).
If unavailable, use plain chat. Otherwise continue within existing authorization. Preserve pre-write
contents, write atomically, reread, then verify frontmatter, links, evals and target-host invocation.
On a failed write or verification, report the exact partial state. Restore/remove only when this
run's mutation is proven safely reversible; otherwise preserve it and report `Blocked | Unverifiable`.

Lead with the outcome and whether a skill actually changed, then the next action or material
limitation. Include the draft path only when one exists. Keep reports short; do not dump the packet,
raw logs, credentials or repeated status fields. For a machine-readable handoff, use `Action` and
`Status` once. A no-op ends without a ceremonial approval question. Do not commit, push, publish,
auto-archive or invoke another user-selected skill under this skill's authority.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.
<!-- /tigerkit:output-notation -->
