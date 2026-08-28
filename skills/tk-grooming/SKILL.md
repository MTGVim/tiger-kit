---
name: tk-grooming
description: "[user/auto] 기존 repository 또는 user skill의 중복, 범위, trigger, reference, no-op 위험을 감사합니다. 일반 코드 정리나 신규 skill 작성에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill Grooming Audit

Apply only upon an explicit invocation concerning existing repository or user skills, or a clear
audit request. Do not apply automatically to general cleanup or implementation requests.
Implicit mode is report-only.
When ownership evidence or apply approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, ask the same decision in plain chat and do not write beyond the approved scope.

## Workflow

1. `scope`: Confirm the requested scope, literal `--apply`, target paths, and
   permitted mutations. Preserve exclusions specified in the active conversation
   or a durable governing source without reconfirming them.
2. `discovery`: Read only existing native paths and create a candidate list for
   the requested area.
3. `evidence`: Record area-specific observations, paths, verification status,
   and ownership evidence for every candidate.
4. `description shortcut audit`: Before any frontmatter description rewrite, identify
   the exact process-summary phrase that could substitute for loading the body, preserve
   the smallest routing discriminator, and compare prior/candidate routing and body behavior.
5. `instruction economy audit`: For the selected existing skills only, inspect conditional
   reference pointers, duplicated environment facts, behavioral no-ops, stale sediment,
   and branch-specific prose that unnecessarily stays on the main execution path.
6. `classification/proposal`: Apply the
   [placement criteria table](references/repository-placement.md) to skill candidates
   and classify them as `keep | keep (vendor) | tighten | merge | split | move
   | deprecate | delete | fix`.
7. `🔴 CHECKPOINT · 🛑 STOP`: Summarize the exact scope, evidence, proposal, target paths, and permitted apply actions.
   A literal initial `--apply` pre-approves only that verified mechanical scope; otherwise stop until explicit current-turn
   approval. Scope, evidence, or target drift invalidates approval.
8. `apply/report`: In report-only mode, output the proposal/receipt. If authority
   exists, reread the sources, search references before delete/move, preserve
   managed/generated markings, and modify only the approved receipt scope.
9. `revalidate`: Recheck links, duplication, frontmatter, and any behavior comparison
   that justified instruction pruning, then report the results, unverified scope, and unresolved items.

Investigate only the repository or user skill areas explicitly stated or implied
by the request. Use the actual host-native skill paths from
[discovery](references/discovery.md). Do not create missing files or investigate,
migrate, or create repository/user rule state or legacy/global TigerKit state.
Do not expand this audit into generic `AGENTS.md`, `CLAUDE.md`, ticket, spec, or repository-doc cleanup.

Evaluate repository/user skills as independently normative instruction/workflow
units, not as whole files. Use `move` only when an exact native skill target exists,
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

For an instruction-economy audit:

- Treat a description or conditional reference link as a context pointer. A useful
  pointer names the material and the distinct branch/condition that needs it; body or
  workflow summaries do not make the pointer stronger.
- Treat a current package/config value, directory inventory, or host/tool capability as
  an environment-cache candidate only when a cheap fresh lookup is the real source of
  truth. Commands, paths, literals, or state that the skill intentionally owns as a
  contract are not stale merely because they are concrete.
- Call something a behavioral no-op only when removing it preserves the same observable
  behavior against a no-skill/prior baseline. Do not infer no-op from prose style.
- Move branch-specific reference out of the main path only when a precise pointer still
  causes the branch that needs it to read and apply it. Always-needed safety/authority
  guards stay inline.
- Treat long-but-live instruction as `keep`; `sprawl` or `sediment` needs evidence that
  the material is irrelevant, duplicated, stale, or on the wrong branch.

Before proposing `tighten`, compare the prior and candidate against the relevant existing
behavior cases. For a description change, include train/validation trigger cases and body
behavior. For a pointer, cache, or no-op change, include the branch that needs the rule and
a branch that does not. The candidate must preserve valid behavior and safety while
removing only proven load. Trigger success, source-text presence, line count, or token
reduction alone does not prove compliance. If semantic behavior would change, report an
exact pending proposal for `tk-learn` instead of applying it here.

Determine ownership from confirmed paths and link targets, package-manager
installation locations, updater/version artifacts, and verifiable author history.
Names and conventions are not evidence. Always treat candidates confirmed as
vendor-managed as `keep (vendor)`; report only quality findings and do not create
proposals or edits. If ownership is uncertain, stop before proposing edits and ask
whether it is user-managed or externally installed.

Classification alone does not grant modification authority. Even after approval,
directly own only meaning-preserving `tighten`, mechanical `move` with an exact
target, unreferenced `delete`, and frontmatter/link `fix`. Leave semantic `merge`,
`deprecate`, workflow `split`, and semantic skill rewrites only as exact `pending`
proposals. These proposals may be handed off to `tk-learn`, but this skill does not
invoke it. Keep vendor-managed candidates report-only in every apply mode.

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
