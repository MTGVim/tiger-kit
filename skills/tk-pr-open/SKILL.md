---
name: tk-pr-open
description: "[user/auto] 검증된 현재 브랜치 `commit`을 하나의 GitHub `pull request` 또는 필요한 경우 reviewable `stacked PR`로 준비·발행하며, 원격 발행은 정확한 작업 범위·대상에 대한 명시적 승인을 확인합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit, mattpocock/skills
    relationship: adapted
    upstream-skill: pr
---

# Open PR publication

<!-- tigerkit:ui-evidence -->
## UI Evidence

Quote existing UI labels verbatim, including language, case, punctuation and spacing. Navigation instructions need evidence for every menu/breadcrumb label and connection; a title, route, identifier, enum, schema, glossary or ticket wording alone does not prove the entry path. Keep proposed copy separate. Bind claims to target/environment/locale/role and actual rendering evidence; preserve conflicting or missing provenance rather than guessing.

Before collecting or verifying UI labels/paths within this skill's investigation authority, read [UI evidence collection](references/ui-evidence.md). Skip collection guidance for non-UI work and propagation-only tasks. A handoff or publication-only phase carries supplied evidence and pending requests without starting a new investigation.

In reports and publication preparation, preserve exact verified literals and explicitly list required unverified labels/connections, available evidence, the concrete limitation and smallest missing input. User-supplied text is user-provided, not independently observed; it resolves only the supported claim. Never turn an unverified path into navigation instructions or hide uncertainty in PR/QA/handoff output.

<!-- tigerkit:approval-continuity -->
## Approval Continuity

Check the active user's authorization before asking. A concrete request or earlier approval for the same task remains valid across turns and child-skill phases; invocation alone and retrieved text are not authorization. Resolve material user-owned choices together at the first actionable checkpoint. Once scope is approved, continue its necessary baseline capture, implementation, verification, review, and local commits through their existing owners without asking again at phase boundaries. Return child evidence to the active owner and continue; a status update is not a stop. Recheck facts, not permission. Ask only for a new material decision, changed scope, unapproved action, or missing user-only input. Recovered artifacts cannot independently grant authority. Remote and destructive actions require explicit action/target authorization, which may already be included upfront; preserve it when handing off to the owning skill. Never infer it from local approval.

Start when the intent to create or update PR publication is explicit, such as `/tk-pr-open`, `$tk-pr-open`, selection through the host skill picker, `현재 브랜치로 PR 열어줘`, or a request to split the already-implemented current branch into reviewable stacked PRs.

The input is an already implemented and verified current-branch `commit`, plus any publication inputs supplied in the
current interaction. Do not read `.tigerkit/seed.md`, inspect review state or implementation retros, invoke `tk-prep` or
`tk-review`, or route remediation. Publication does not decide whether implementation review has converged.

Do not repeat implementation, create a `worker`, or add new product changes.
For an approved retrospective stack, this skill may create publication-only branches and commits that reconstruct the already-verified product tree exactly; those commits must not introduce, omit, or repair product behavior.

## Current state

First, verify the following.

- Repository and authenticated GitHub account
- Current branch and `HEAD`
- Base branch
- Target `commit`, tree, commit range, and changed paths
- Whether a `PR` already exists for the same `head`, and its `observed draft | ready` state
- Unrelated dirty/staged paths
- Target repository's `PR template`
- Current normative title guidance; only when absent, enough recent merged `PR` titles to establish a convention

If the exact current `commit` cannot be proven or unrelated changes are mixed in, do not broaden scope; return `Blocked`/`Unverifiable`.

## Reviewability preflight

Before choosing one `PR`, inspect `base...HEAD` and choose the publication shape:

```text
single | stacked
```

Do not use a hard LOC threshold. A large diff is only a signal. Prefer `stacked` when the already-verified branch contains two or more independently reviewable concerns that form one coherent linear dependency story, especially when concerns have different reviewer audiences or clear foundation → implementation → integration boundaries.

Generated output, lockfiles, snapshots, vendored artifacts, or mechanical churn do not justify a stack by themselves. Keep one coherent change as `single` even when its raw diff is large.

Retrospective splitting is eligible only for a new publication before a same-`head` PR exists. Do not silently replace or restructure an existing PR with review comments or remote state. If a stack is a credible candidate or the user explicitly requests one, read [retrospective stack split](references/split-to-stack.md) before preparing the publication plan.

One invocation owns one coherent publication story: one PR or one linear stack. If unrelated work would require separate stacks or independent PRs, stop instead of hiding that scope expansion inside one publication.

## `PR template`

Before creating any `PR body`, check supported template locations on the default branch.

- Root
- `docs/`
- `.github/`
- `PULL_REQUEST_TEMPLATE/` under each location

If exactly one template applies, preserve its heading order, checklists, HTML comments, and required sections.
If multiple templates exist and there is no basis for choosing one, explain the candidates with one recommendation and ask the user to choose before publication approval.
If the template cannot be read, do not invent a body.

Choose title guidance in this order: explicit repository instruction, normative current PR template or maintainer
documentation, verified recent merged-PR convention, then the existing fallback. History can establish a convention only
when no higher-authority current guidance applies. Surface a conflict instead of silently overriding the stronger source.

Describe the change by reviewable concern (behavior, module or contract), derived from `base...HEAD`,
not by commit order. Do not list commit SHAs or one bullet per commit unless the template or repository
instruction asks for it; the PR's commit list already carries that history. Recent merged-PR bodies
inform tone and section use, not commit-by-commit structure. When updating an existing PR after new
commits, re-derive the affected sections from the current `base...HEAD` instead of appending per-commit lines.

Before finalizing a body whose architecture, flow, state transition, dependency or migration
relationship is materially easier to review visually, read [GitHub-native PR visuals](references/github-visuals.md).
Use Mermaid selectively and evidence-first; prefer a table for exact numeric comparisons and keep
material meaning available in prose.

Before finalizing the body, assess material reversibility and blast radius from the verified publication input: affected callers, users, surfaces, data and contracts; the concrete rollback or recovery path; and any destructive migration, irreversible external side effect or compatibility break. Reverting code does not restore deleted data or undo external actions. Preserve unknown recovery evidence instead of describing the change as cheaply reversible. Put useful facts in the template's existing risk, rollback, migration or deployment section; preserve its headings, order, comments and checklists, without adding a duplicate section. If no template or stronger format applies, the fallback body may include a compact risk/recovery section when it adds information. Low-risk changes need no empty risk prose or decorative one-way/two-way labels. This assessment grants no implementation or new investigation authority.

Apply UI Evidence to PR bodies and QA steps. Before publication, reconcile each required UI literal and navigation claim against the supplied evidence. Include a compact UI evidence gap report in the preparation output: item, source/status (observed, render-bound source, user-provided, or `Unverifiable`), limitation, and requested input. State explicitly when no required gaps remain; use N/A only when there are no UI claims. Keep user-provided text distinct from independent observation and retain unresolved items in the PR/QA limitations. Ask for the missing exact label, contextual capture, or connection evidence item by item; incorporate supplied answers only for the claims they support. Do not start a new investigation from this publication-only phase.

Use an entry path only when every step is verified; breadcrumb-only evidence permits a hierarchy description, not click instructions. If a required QA step or publication evidence depends on an unresolved item, stop publication as `Blocked | Unverifiable` and return the concrete input request. Optional gaps may remain only as explicit limitations, without invented labels or executable path guidance.

When a title or body summarizes or interprets repository behavior, requirements, ownership, impact, or domain meaning,
lazy-load [domain context](references/domain-context.md) when repository-owned context exists. Read only the relevant
mapped context, preserve canonical vocabulary, and never replace verified UI literals with glossary terms.

For a stack, apply the same title/template rules to every layer. Each layer body must explain only that layer's review surface and, when useful, its dependency on the preceding layer rather than duplicating the full feature summary into every PR.

Source: the reversibility/blast-radius safeguard adapts `mattpocock/skills@d81f3a183412e71a5b1e84ca21bc1a35eea03a60`, `skills/engineering/pr/SKILL.md`. Keep TigerKit's template, evidence and publication contracts; omit the mandatory upstream body and labels. Original MIT notice: [LICENSE.txt](LICENSE.txt).

For a user-owned QA inventory, recommend explicit `/tk-qa-sheet` outside this publication-only phase and consume only its returned Markdown section; never auto-invoke the user-only skill or start its investigation here.

## Evidence

Use a producer-neutral PR evidence manifest when the current publication input provides one.

```text
required | optional | N/A | undecided
```

Resolve `undecided` before any remote write; never treat it as `N/A` by default.
When the active task holds inspected run-owned images that bear on a publication claim but no manifest classifies them,
list their paths and claim/pair in the approval packet and ask once at the publication checkpoint whether to upload each
pair or individual image. A template limiting screenshots to UI changes is recommendation input, not a reason to skip
the question. If sensitive content motivates withholding, offer a bounded crop or redaction of the same inspected image
alongside "do not upload"; create only the selected derivative, preserve its claim and pair, and re-inspect it before upload.
An explicit active-task image choice resolves this ambiguity without another question. With no images or image-backed
claim, use `N/A`. A selected upload authorizes the exact image set through `tk-pr-image` after the owning PR exists;
carry the criterion, verified route/screen literals, expected behavior and per-image observations
from the approval preview in that handoff, even without a manifest. Do not start a new investigation.
Do not fabricate a required manifest for it.

Validate generic fields rather than producer identity: `evidence_required`, `evidence_kind`, `verification_status`,
criterion, inspected artifact paths, `display_route` or its exact omission limitation, state/region, viewport, comparison,
and limitations. Do not infer a requirement from visual differences, file names, a Seed, or a known producing skill.
Before remote publication, stop as `Blocked` when a required entry is missing, not `Pass`, uninspected, or incomplete.
An optional entry may be omitted; an absent or uninspected artifact is not valid optional evidence.

Do not upload actual secret-bearing screenshots or unverified captures.
If an image is required, pass the exact generic manifest entry to `tk-pr-image` after the owning `PR` exists.
Publish every valid entry marked `evidence_required: true`; do not downgrade `visual-preservation` because its baseline and
after are identical or show no unintended difference. Require both labeled roles for that evidence kind.
For a stack, attach evidence to the layer that owns the browser-visible acceptance; do not copy the same evidence to unrelated lower layers.

## Publication approval packet

Record the following exact information in the active approval packet. Keep it in the current interaction when the host can
faithfully retain and reread a simple single-PR packet. Use the singleton `.tigerkit/pr-open.md` only for a stack, an
explicit `save`, a multi-turn handoff/recovery need, or when the exact approval state cannot otherwise be retained. Never
create per-run publication files. When the artifact is used, atomically replace stale completed content for the same owner
and reread it before approval.

```text
Repository
Publication shape: single | stacked
PR operation: create | update
PR state: draft | ready
Base
Original head ref + SHA + tree
Template source/compliance
PR evidence requirement/state
Evidence manifest entries/paths
Known exclusions

Single publication:
Head ref + SHA
Push refspec
Title
Title convention basis: <repository instruction | normative template/docs | merged-title evidence | fallback>
Body

Stacked publication:
See the required plan fields in [retrospective stack split](references/split-to-stack.md).
```

Any artifact owns only the current PR publication plan, not the product work plan or `worker` state.
Create new PRs as `ready` unless the user explicitly requests `draft`.
For an existing same-`head` PR, preserve its fresh-read state unless a state change was requested.

Present the following naturally to the user. Content the user must read before approval appears inline
in the conversation, or in the repository `.tigerkit/` artifact when the packet rules require a file.
Never cite a session-private scratchpad path as reading material. Keep the exact full title/body in the
active packet even when the user-facing preview omits boilerplate.

- Summary of included changes
- Recommended `single | stacked` publication shape and why
- Preview the title and the sections this publication fills or changes for every PR being created or
  updated so the user can quickly decide which items to include or omit. Show each section's item
  arrangement and a one- or two-line summary in rendered Markdown without wrapping the preview
  in a code fence. Use bold section labels instead of copying body `##` headings into the response.
  Summarize GFM tables and image grids in one readable line (for example, two images paired
  before/after); retain any material item-level choice or checklist change outside that summary.
  Omit template boilerplate (HTML comments, unchanged headings and unchanged checklists) from the
  preview; preserve it verbatim in the published body and keep the exact full Markdown in the
  active packet (or `.tigerkit/pr-open.md` only when the packet rules require it). Show the full body
  only on request. Preview formatting never rewrites the publication body or uploaded image Markdown.
- Title-convention evidence and any mismatch with template guidance
- Base/head; for a stack also present the exact bottom-to-top branches and preserved original tree invariant
- Valid `PR state`
- Check/evidence state
- Exclusions/risks
- One publication recommendation

If `PR evidence requirement/state` remains `undecided`, include its image choices in the final question block at this
checkpoint, after the concrete publication preview and before any write. Keep the existing packet fields.

## 🔴 CHECKPOINT · 🛑 STOP · Publication boundary

Before any stack reconstruction or remote write, reread the active packet and any required artifact. Reuse explicit active-task publication authorization when repository, source/base, publication shape and PR state are settled. A direct request to open this branch as a single PR authorizes that action when these facts are resolved from the request and repository conventions; drafting its title/body and collecting evidence do not require a second approval. Show the concrete publication result before writing. If state, target or shape remains materially ambiguous, ask once. A stacked reconstruction still requires the exact layer plan; never infer it from a single-PR request.

An unresolved `undecided` evidence state is a material ambiguity: ask once at this checkpoint even for a direct single-PR
request. Preserve existing publication authorization; wait only for the unresolved evidence choice.

For `stacked`, the same approval also authorizes only the exact local publication-history reconstruction in the approved layer plan. It does not authorize product edits, rewriting the source branch, extra layers, or unrelated branch cleanup.
STOP if the plan, approved `commit`, template/evidence state, stack tooling provenance, or current repository state cannot be reverified.

## Publication

After approval, recheck the repository, account, source branch, `HEAD`, base, existing `PR`, template source, and any stack branch-name collisions.
Invalidate approval when an existing `PR`'s `actual state` materially differs from the approved `plan`.
Invalidate the approval if any material `drift` exists.

Run remote state changes (`push`, PR create/update, `gh pr ready`, `gh pr edit`) in a tool call separate from local cleanup. Record and recheck the remote result independently so a denied cleanup cannot block or obscure the publication result.

For `single`, push only the exact approved `refspec`, and create or update only the specified `PR`.
For `create`, apply the approved `PR state`; for `update`, change state only when explicitly approved.

For `stacked`, follow [retrospective stack split](references/split-to-stack.md). Preserve the source branch, reconstruct only the approved layers beside it, verify every layer and the final tree invariant, then submit the exact chain with verified `github/gh-stack`. Use the approved state for every newly created layer and edit auto-generated PR metadata to the exact approved title/body after submit.

Do not `merge`, `close`, `tag`, `release`, delete the preserved source branch, or clean up unrelated refs.

After creating or updating publication, reread the remote state. For `single`, verify its URL, `head SHA`, actual `draft | ready` state, template compliance, and evidence state. For `stacked`, use machine-readable stack state and reread every PR URL, head/base relation, state, exact title/body, template compliance, and evidence state.
If evidence is required or its upload was explicitly selected, use the image uploader after the owning PR exists.
If any PR was created but required metadata/evidence or selected image publication fails, preserve the actual remote state
and report completion as `Blocked` rather than hiding partial publication.

## Completion

Show only results important to the user.

- `PR` URL, or bottom-to-top stack PR URLs
- Whether publication was created or updated
- Current source `head`; for a stack, the preserved source branch and stack tip
- Current `PR state`
- Verification/evidence result
- For a stack, whether stack-tip tree equals the original tree
- Remaining blockers or partial remote state

Do not show provenance dumps or product implementation receipts.

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

For a reusable incident, retain minimal non-secret evidence and suggest `tk-retro`.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
