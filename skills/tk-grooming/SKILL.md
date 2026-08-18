---
name: tk-grooming
description: "[user/auto] 기존 repository 또는 user skill의 중복·범위·배치·trigger를 감사합니다. 기본값은 report-only이며 literal --apply 또는 current-turn approval 전에는 절대 변경하지 않습니다."
disable-model-invocation: false
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill Grooming Audit

Apply only upon an explicit invocation concerning existing rules or skills, or a clear
audit request. Do not apply automatically to general cleanup or implementation requests.
Implicit mode is report-only.
ownership evidence나 apply approval을 물을 때 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 결정을 plain chat으로 fallback하고 승인 범위를 넘겨 쓰지 않습니다.

## Workflow

1. `scope`: Confirm the requested scope, literal `--apply`, target paths, and
   permitted mutations. Preserve exclusions specified in the active conversation
   or a durable governing source without reconfirming them.
2. `discovery`: Read only existing native paths and create a candidate list for
   the requested area.
3. `evidence`: Record area-specific observations, paths, verification status,
   and ownership evidence for every candidate.
4. `classification/proposal`: Apply the
   [placement criteria table](references/repository-placement.md) to skill candidates
   and classify them as `keep | keep (vendor) | tighten | merge | split | move
   | deprecate | delete | fix`.
5. `🔴 CHECKPOINT · 🛑 STOP`: Summarize the scope, evidence, proposal, and permitted
   apply actions in the receipt. A literal initial `--apply` pre-approves only the
   exact receipt scope that passed; otherwise, stop until explicit approval in the
   current turn.

Include every field below in the receipt. This is not a separate lifecycle output,
but the single evidence record used for `.tigerkit/audit.md` and approval decisions.

```text
Scope: <exact repository/user skill scope>
Target paths: <exact paths | none>
Evidence refs: <path:line or unavailable>
Proposal IDs: <GR-## list | none>
Apply authority: report-only | literal --apply | current-turn approval
Audited: <covered paths/categories>
Unaudited: <excluded or incomplete paths/categories>
Verification: <check results or unavailable>
Drift rule: <scope/evidence/target change => Partial/Blocked>
```

6. `apply/report`: In report-only mode, output the proposal/receipt. If authority
   exists, reread the sources, search references before delete/move, preserve
   managed/generated markings, and modify only the approved receipt scope.
7. `revalidate`: Recheck links, duplication, and frontmatter, then report the
   results, unverified scope, and unresolved items.

Investigate only the repository or user skill areas explicitly stated or implied
by the request. Use the actual host-native skill paths from
[discovery](references/discovery.md). Do not create missing files or investigate,
migrate, or create repository/user rule state or legacy/global TigerKit state.

Evaluate repository/user skills as independently normative instruction/workflow
units, not as whole files. Use `move` only when an exact native skill target exists,
and use `split` when independent outcomes are mixed in one artifact. Use `tighten`
only when removing duplication/ambiguity without changing ownership, kind, scope,
or meaning. Otherwise, use `keep`. If path or ownership evidence is missing or
conflicting, treat only that area as `Partial/Blocked | Unverifiable`.

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
