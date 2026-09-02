---
name: tk-grooming
description: "[user/auto] 기존 skill·지속 rule·auto memory의 중복, 충돌, 낡은 지침을 감사합니다. rule이나 memory를 따른 동작이 사용자 피드백 또는 최신 skill과 충돌한 경우에도 사용하며, 일반 코드 오류나 신규 skill 작성에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill Grooming Audit

Apply only upon an explicit invocation concerning existing repository or user skills,
persistent rules, or auto memory; a clear audit request; or user correction of behavior
that plausibly followed persistent context. Do not apply automatically to general cleanup,
implementation requests, or failures without persistent-context evidence.
Implicit mode is report-only.
When ownership evidence or apply approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, ask the same decision in plain chat and do not write beyond the approved scope.

## Workflow

1. `scope`: Confirm the requested scope, literal `--apply`, target paths, and
   permitted mutations. Preserve exclusions specified in the active conversation
   or a durable governing source without reconfirming them.
2. `discovery`: Read only existing native skill, rule, and auto-memory paths and create
   a candidate list for the requested area. Read
   [persistent context](references/persistent-context.md) only when rules, memory, or a
   user-corrected behavior is in scope.
3. `evidence`: Record area-specific observations, paths, verification status,
   and ownership evidence for every candidate.
4. `incident attribution`: When user feedback says prior behavior was wrong, compare
   the behavior's cited or observed instruction with the active skill and persistent
   context. Classify a proven obsolete instruction that conflicts with the current owner
   as `stale override`; do not infer precedence or causation from file presence alone.
5. `description shortcut audit`: Before any frontmatter description rewrite, identify
   the exact process-summary phrase that could substitute for loading the body, preserve
   the smallest routing discriminator, and compare prior/candidate routing and body behavior.
6. `instruction economy audit`: When existing skill or persistent-instruction load is in
   scope, read [instruction economy](references/instruction-economy.md) and apply its
   branch-aware behavior comparison. Do not load it for a persistent-memory-only incident
   whose question is solely freshness, conflict, or attribution.
7. `classification/proposal`: Apply the
   [placement criteria table](references/repository-placement.md) to skill candidates.
   Classify skill actions as `keep | keep (vendor) | tighten | merge | split | move |
   deprecate | delete | fix`; persistent context may also use `duplicate | conflict |
   stale override` as a finding before proposing an action.
8. `🔴 CHECKPOINT · 🛑 STOP`: Summarize the exact scope, evidence, proposal, target paths, and permitted apply actions.
   A literal initial `--apply` pre-approves only that verified mechanical scope; otherwise stop until explicit current-turn
   approval. Scope, evidence, or target drift invalidates approval.
9. `apply/report`: In report-only mode, output the proposal/receipt. If authority
   exists, reread the sources, search references before delete/move, preserve
   managed/generated markings, and modify only the approved receipt scope.
10. `revalidate`: Recheck links, duplication, frontmatter, persistent-context conflicts,
    and any behavior comparison that justified instruction pruning, then report the
    results, unverified scope, and unresolved items.

Investigate only the repository or user skill, rule, and auto-memory areas explicitly
stated or implicated by the request. Use the actual host-native paths from
[discovery](references/discovery.md). Do not create missing files, invent a memory backend,
or migrate legacy/global TigerKit state. Rule and memory inspection is for persistent
instruction health, not generic ticket, spec, or repository-document cleanup.

Evaluate repository/user skills, rules, and auto-memory entries as independently normative
instruction/workflow units, not as whole files. Use `move` only when an exact native target exists,
and use `split` when independent outcomes are mixed in one artifact. Use `tighten`
only when removing duplication/ambiguity without changing ownership, kind, scope,
or meaning. Otherwise, use `keep`. If path or ownership evidence is missing or
conflicting, treat only that area as `Partial/Blocked | Unverifiable`.

For a description audit, quote the exact phrase that summarizes workflow order,
internal routing, approval sequence, artifact lifecycle, or another procedure well
enough to become a shortcut around body loading. Preserve only the smallest trigger,
symptom, intended scope, and positive/negative routing discriminator needed to decide
whether the skill should load. Do not shorten mechanically. If a longer description is
necessary to avoid false-positive or false-negative invocation, return `keep`/no-op.

Determine ownership from confirmed paths and link targets, package-manager
installation locations, updater/version artifacts, and verifiable author history.
Names and conventions are not evidence. Always treat candidates confirmed as
vendor-managed as `keep (vendor)`; report only quality findings and do not create
proposals or edits. If ownership is uncertain, stop before proposing edits and ask
whether it is user-managed or externally installed.

Classification alone does not grant modification authority. Even after approval,
directly own only meaning-preserving `tighten`, mechanical `move` with an exact
target, unreferenced `delete`, and frontmatter/link `fix`. A rule or auto-memory deletion
or semantic rewrite always requires exact item-level current-turn approval. Leave semantic `merge`,
`deprecate`, workflow `split`, and semantic skill rewrites only as exact `pending`
proposals. These proposals may be handed off to `tk-learn`, but this skill does not
invoke it. Keep vendor-managed candidates report-only in every apply mode.

If no persistent instruction can be tied to the corrected behavior, preserve the candidate
and hand the behavioral incident to `tk-skill-diagnose`. If the active skill contract itself
needs semantic change, leave an exact `tk-learn` proposal. Do not invoke either skill
automatically.

Do not invent knowledge or substitute for skill learning.

Continue excluding exclusions declared in the active conversation from subsequent
grooming runs in that conversation. Continue excluding exclusions recorded in a
governing repository/user rule or another requested durable source across sessions.
Do not create hidden global state or store exclusions in `.tigerkit/`.

## Failure Paths

- Missing/unreadable path: Mark only that area `Unverifiable`, keep other areas
  read-only, and report the required access.
- Unknown ownership: Do not create edit proposals or changes; return
  `Partial/Blocked` with one ownership question.
- Vendor ownership confirmed after classification: Convert every edit action to
  `keep (vendor)`, preserve the artifact, and report the evidence.
- Conflicting scope/apply authority: Make no changes and return `Partial/Blocked`
  with the one required decision.
- Referenced deletion/move target: Make no changes, change the proposal to
  `keep | tighten`, and cite the reference.
- Unproven no-op/cache/pointer claim: Keep the existing behavior and report the exact
  missing behavioral evidence; do not make a speculative tightening edit.
- Target drift after checkpoint: Make no changes, return `Partial/Blocked` with
  current evidence, and require a new proposal.
- Verification failure after apply: Never claim `Complete`. Restore/reverify only
  when this run's delta is exactly reversible, then return `Fail` with evidence.
  If preservation or restoration is uncertain, halt the mutation as `Unverifiable`
  and report the checks, paths, and observed state.

## Contract

Evidence records the actual path/content for each area. If required evidence is
missing, treat that area as `Unverifiable`. If any area is blocked, overall
completion cannot be claimed; use `Complete | Fail | Partial/Blocked | Unverifiable`.

## Output Contract

Assign `GR-01`, `GR-02`, ... once, in initial identification order, to each
independently normative instruction/workflow. Output one `## Disposition` table
first.

| ID | Item | Action | Target | Basis |
| --- | --- | --- | --- | --- |
| GR-01 | `<short name>` | `<classification>` | `<target>` | `<evidence refs>` |

Reuse the same IDs for applied changes and verification. Add `## Exceptions` only
when there are evidence gaps, ownership conflicts, unresolved scope, or failed
verification. Add `## Applied` and `## Verification` only after mutation. Show
findings in two to seven rows. If there are eight or more, show the top five to
seven and group the rest by audited target path. Do not create artifact/lifecycle
actions solely for output. This is a budget, not a quota.

Record the overall `report-only | applied` disposition in `## Disposition`, but do
not repeat the table or append metadata. If there are no items, output one
`— | None | keep | — | no finding` row. Use `keep (vendor)` for vendor rows.
