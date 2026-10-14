---
name: tk-pr-image
description: "[user/auto] 기존 GitHub PR body 또는 지정된 comment에 local evidence image를 업로드합니다. 명시적 이미지 요청이나 정확한 evidence handoff에만 사용합니다."
disable-model-invocation: false
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR Image Upload

Handle explicit local-image evidence requests for an existing GitHub PR or an exact
`tk-pr-open` generic manifest handoff with `evidence_required: true`. Only the parent handoff is an
automatic trigger.

## Scope

Handle one bounded upload: validate and stage local images, upload
repository-scoped GitHub attachments, minimally update the PR body or selected
comment, and verify the source Markdown and uploaded image objects. The default target is the PR body.

For `tk-pr-open`, validate the producer-neutral evidence fields and never branch on, whitelist, or require a producing
skill name. If required evidence is missing or invalid, mark the evidence handoff `Blocked`; do not revert an
already-created `tk-pr-open` PR.

Use [references/gh-attach.md](references/gh-attach.md) to classify and run the
extension route. Read [references/cdp-fallback.md](references/cdp-fallback.md)
only after CDP is selected or the extension route cannot use target write
capability. Invoke `tk-wizard` only for an exact human-only host setup,
authentication, permission, or restart step; preserve this skill's upload target and route
across the handoff. Use `tk-browser-verify` for browser-controlled runtime verification.

## 🔴 CHECKPOINT · 🛑 STOP · Upload mutation boundary

Before any upload or PR body/comment update, reverify the explicitly selected target, valid local evidence or producer handoff, authenticated route, and requested write scope; stop as `Blocked` or `Unverifiable` when those preconditions cannot be established.

## Workflow

1. Confirm `origin`, the current PR, and the executing repository from regular
   local image file(s) or a valid producer evidence handoff. Read the existing PR
   body.
2. Reuse the existing `## 스크린샷` heading. If absent, insert it before the AI
   footer or append it at the end. Preserve unrelated body content. For manifest artifacts, use the supplied criterion,
   role, exact `display_route`, state/region, viewport, and comparison in the caption; never derive them from a filename,
   OCR, raw URL, or producer identity. Keep `visual-preservation` baseline and after visibly labeled as one pair.
3. Select and execute an eligible route using
   [gh-attach](references/gh-attach.md), or read
   [CDP fallback](references/cdp-fallback.md) only after CDP is selected.
   Repository visibility is not a routing signal, and a route that may have created
   remote state cannot silently fall back to the other route.
4. When the selected route needs a human-only host action, pass a bounded handoff to
   `tk-wizard` and perform no upload until its completion signal. Agent-approved reviewed
   extension installation remains here. Resume the exact repository, target, image set, and
   route after the wizard completes.
5. Update only the requested body or comment through the GitHub API or equivalent.
   Before `Pass`, verify byte-for-byte Markdown preservation, decodable `image/*` bytes from an authenticated fetch for
   every asset, and reachability of every linked upload object from the upload ref. Browser-session rendering is
   optional; report whether it was checked in the receipt without making it a `Pass` prerequisite.
6. Remove only owned staging files on every exit path.

## Execution Receipt · Single Evidence Record

Record every upload attempt in the single receipt below. It is not a separate lifecycle
output; it is the sole evidence record used for the `## GitHub image upload` result and
approval/verification decisions. Use `none` or `unavailable` for absent values; never guess.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: Markdown byte match: <Pass | Fail | unavailable>; image bytes/type: <Pass | Fail | unavailable>; upload ref reachability: <Pass | Fail | unavailable>; rendering: <checked | not performed | unavailable>
Changed: <body/comment changed | unchanged | unknown>
Cleanup: <owned staging path removed | failed | not applicable>
Status: Pass | Fail | Pending | Blocked | Unverifiable
```

## Evidence Manifest Handoff

When `evidence_required: true`, require all of the following:

- `verification_status: Pass`, a non-empty criterion, evidence kind, comparison result, and limitations.
- Every artifact has a role, non-empty image, absolute path, run-owned evidence directory, state/region, and viewport.
- Every image is marked `inspected: true` and has an exact origin-free `display_route` or an explicit safe omission
  limitation. Never reconstruct or mask a missing route.
- `visual-preservation` contains both a baseline and after artifact from its verified pair.

Reject arbitrary screenshots, missing paths, non-`Pass` results, uninspected artifacts, incomplete preservation pairs,
and artifacts not tied to the current run. If required evidence is missing or invalid, return `Blocked` before upload.

## Prohibitions

- Do not create or merge a PR, change reviewers, publish a release, or insert a
  comment unless the user explicitly selected that comment target.
- Do not bypass `tk-browser-verify` or use Orca or screen control as an automatic
  browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or
  any other submit button.
- Do not choose a route based on public/private visibility or claim success from
  only a placeholder, Markdown presence, fixed delay, or unrendered API response.
- Do not log or return a signed URL, JWT, or raw secret-bearing query string. This does not prohibit a verified-safe,
  origin-free `display_route`; preserve its pathname, query, and fragment exactly as supplied by the manifest.
- Redact only secret-bearing values (signed parameters, JWTs, tokens) in displayed output; preserve rendering parameters
  such as `raw=true`. Keep the extension's generated Markdown privately for the authorized body/comment mutation and
  insert it verbatim, with captions outside that block; never rebuild links from redacted or summarized output. Do not
  copy secret-bearing originals into logs, receipts, or evidence artifacts.

## Failure Handling

Return `Pending` while waiting for an absent-extension or unreviewed-upstream choice or a
human-only `tk-wizard` completion signal. Return `Blocked` for `unknown` provenance, a draft, or a rejected
installation without a selected CDP route. Return `Unverifiable` if authentication,
image-byte validation, or upload-ref reachability cannot be verified; rendered-page
evidence is optional. Return `Fail` for upload, remote ref
verification, or cleanup errors. State whether the selected body/comment changed
and whether an upload ref may remain.

For `tk-pr-open`, preserve the separate PR operation result and return the
evidence state as `uploaded` or `blocked`. While required evidence remains
blocked, the parent cannot claim full completion.

## Result

Start the terminal response with `## GitHub image upload`. Include `## Uploaded`,
`## Verification`, and `## Cleanup` when applicable. End the result-owning section with exactly
one `Status: Pass|Fail|Pending|Blocked|Unverifiable` line. Expose asset URLs only when …13580 tokens truncated…e, and any required re-review request within the approved scope.

**Keep the conversation natural and the state strict.**

Do not expose worker placement or GitHub state as a raw report.
The user needs to know what the review means, how it will be addressed, why that approach is appropriate, and what will be verified.

## Fresh state

At the start, fresh-read exactly one open PR.

- repository and authenticated identity
- PR author, base/head ref, and SHA
- checks and evidence from failed GitHub Actions
- reviews, inline threads, and conversation comments
- unresolved threads
- requested reviewers
- exact push target

Complete all required pagination. Do not treat cached lists or previous Markdown ledgers as current truth.
If identity, the exact PR/head, or remote authority is ambiguous, stop as `Blocked` before mutation.

When re-entering after any attempted publication, including an uncertain POST/push result, read
[publication recovery](references/publication-recovery.md) before planning mutations. Reconcile already
successful actions against fresh remote state and continue only the approved missing actions.

## Understand feedback

Assign every current finding exactly one response disposition and preserve it through the plan, reply, and current-head summary.

- `fixed`: change only the code or tests needed to correct a defect owned by this PR.
- `covered`: verified current code or behavior-level tests already satisfy the requested outcome.
- `rejected`: repository evidence disproves the finding's premise.
- `accepted-risk`: leave a verified risk unchanged only with explicit current user approval.
- `follow-up`: leave a pre-existing or otherwise out-of-scope concern unchanged and state whether a separate issue was approved.

Use the disposition to make the outcome auditable, but explain its evidence and practical meaning in natural language.

If the review text already specifies the required outcome, do not ask the same question again.
Investigate repository evidence independently, then explain the recommendation and rationale for decisions about reuse, simplification, testing, security, and user experience.

Attribute each finding before proposing a code change. Compare its anchor (`path`, side, current/original line, and outdated state when available) with the fresh PR diff. An unchanged-line anchor is strong evidence for a `follow-up`, not a conclusive rule: the anchor may describe behavior caused elsewhere, and a changed-line anchor may still point to an unrelated concern.

Keep the finding in the current PR when the PR introduced, exposed, or worsened the behavior, when the acceptance criteria require it, or when the evidence may involve runtime breakage, security, payment, data loss, permissions/account access, or public API compatibility. Do not automatically defer these cases because the comment anchor is unchanged. Ask for a user decision when causal ownership remains ambiguous or the consequence is high risk.

When review text explicitly requires a code change, `fixed` is the default. Reclassifying it as `covered`, `rejected`, `accepted-risk`, or `follow-up` needs explicit user reapproval in the current turn or a verifiable prior approval record (conversation log or memory); approval wording in the agent's own earlier reply is not evidence. Independently verified evidence may support the proposed override but does not authorize it.

A `follow-up` changes no code for that finding. Create a separate issue only when the approved current plan explicitly includes the exact repository and issue intent; otherwise record it as not ticketed. Never infer issue-creation approval from approval to reply or resolve.

Apply UI Evidence to review replies as well as implementation claims; never repeat unsupported feedback wording as current UI text.

Before interpreting feedback through repository behavior, requirements, ownership, impact, or domain meaning, lazy-load
[domain context](references/domain-context.md) when repository-owned context exists. Read only the relevant mapped
context, preserve canonical vocabulary, and never override verified user-visible UI literals.

When feedback directly concerns architecture, compatibility, or a boundary decision, combine the current diff with
only relevant ADR rationale. Do not make ADR review a generic checklist and never scan an unrelated ADR or context tree.

When feedback requests a test, do not close it with file-existence or source-text assertions. Reproduce the reported
regression and add protection that fails when the real behavior or side effect breaks again.

Ask the user directly only about:

- user-owned decisions that materially change product behavior or scope
- risky or hard-to-reverse decisions involving security, permissions, data, or compatibility
- exceptional approval when the work has been sufficiently improved but verification readiness cannot be raised further

## 🔴 CHECKPOINT · 🛑 STOP · Plan and mutation boundary

Before mutation, require fresh state plus one current approval for standalone work, or the exact parent `tk-pr-sweep` approval for a handed-off PR; invalidate it on material drift and stop before mutation.

## Resolution plan and approval

Before mutation, explain the resolution plan for the current feedback in natural language.

At minimum, cover:

- each finding's disposition, causal evidence, and whether it changes code
- implementation approach and existing code to reuse
- how unnecessary complexity will be avoided
- regression and new-test plan
- any approved follow-up issue creation; otherwise state that follow-ups will not be ticketed
- any special security or user-experience concerns
- the `tk-browser-verify` plan for browser-visible changes
- bounded publication scope for push/reply/resolve/re-review
- practical execution shape: reply-only, direct, or SDD

For every code-changing route, keep the semantic Review Plan from the code-change reference in the approved current
interaction even when no Seed is needed. Do not expose reviewer/model/worker routing as part of the user plan.

For a code-changing plan, inspect the actual repository test surface and use [behavior-first testing](references/testing.md)
to resolve RED feasibility or pre-edit GREEN for behavior-preserving refactoring, the focused command, required suite,
realistic mutation, and any `N/A` or engineering exception.
Explain the practical route among reply-only, direct+TDD, and SDD+TDD without exposing an internal classification form.
Once a code-changing route is selected, read [code-change execution](references/code-change.md) before requesting approval;
use its workspace and Seed sections for the plan, but perform no mutation until approval.

Send feedback/CI failures with an obvious cause and exact regression seam directly through the existing testing path.
Lazy-load [shared diagnosis](references/diagnosis.md) only for unknown-cause, intermittent/flaky, performance, or
difficult-to-reproduce hard CI/regression cases, and establish a red-capable feedback loop before a fix hypothesis.
Do not lock the first guess into a change without evidence that such a loop cannot be established.

TigerKit decides only `reply-only | direct | SDD`; host/user model selection remains outside durable artifacts.
Do not mark the task `Blocked` merely because model-control capability is unavailable.

Obtain one user approval for the current plan. That approval covers the exact listed dispositions, code changes, replies,
resolutions, and issue creations; it does not authorize adjacent cleanup or unlisted tickets. Do not split publication for
the same plan into a separate second question.
However, if the PR head/thread/check/identity changes materially after approval, invalidate the approval and explain only what changed.
A verified normal fast-forward during publication recovery may retain approval only under the recovery reference's
ancestry, unchanged response validity, and exact action-scope checks; it does not authorize new fixes or feedback.

Reply-only execution uses no Seed, product mutation, push, workspace solely for isolation, or ceremonial test. For any
code-changing route, follow the already loaded code-change reference after approval. It owns isolation, conditional Seed
use, direct/SDD execution, review, and browser handoff.

## Comment authorship

Comment authorship is a per-comment property, not an account property. Classify each feedback comment in this order:

1. If its body carries a prefix from `toolAuthoredCommentMarkers` in the repository-scope
   `$XDG_CONFIG_HOME/tigerkit/pr-triage.json`, classify it as `tool-authored` regardless of account type.
2. Otherwise, if `user.type == "Bot"` or the login ends with `[bot]`, classify it as `tool-authored`.
3. Otherwise classify it as `human-authored`.

With no configured marker, apply only steps 2 and 3. Record that the human classification used no marker evidence;
never invent a tool marker or infer tool authorship from writing style. A marker is comment-local: the same `User`
account may have both tool-authored and human-authored comments.

Use this classification only for the user-confirmation boundary before publishing a reply. A tool-authored finding needs
no extra human-communication confirmation after the exact resolution/publication plan is approved. A human-authored
finding requires current approval of the reply's exact substance, but the existing one-plan approval satisfies that
requirement when it already covered that substance; never ask twice for the same decision.

Authorship never changes whether a finding must be investigated or addressed. It also never controls re-review targets:
`CHANGES_REQUESTED`, approval, and review-request capability belong to accounts, so those paths use account identity only.

## Publication

Immediately before any remote write, recheck the exact repository, authenticated identity, open PR, fresh remote head,
local ancestry, thread/check state, and approved scope.

Before replying to or resolving anything, freeze the account-based human reviewer set attached to approved findings that produced a
verified code change. Keep each finding-to-reviewer mapping through publication; do not try to reconstruct it from only
the remaining unresolved threads. Exclude the PR author, authenticated user, account bots (`user.type == "Bot"` or a
`[bot]` login), and still-valid approvers. Do not use comment-authorship markers for this set. Fresh-check
whether each remaining reviewer can be requested on the repository. A human who is not request-eligible is mention-only;
report that downgrade instead of failing the whole publication.

Then perform only the approved actions in this order.

1. For a code-changing response, push the verified commit to the exact branch only if fresh ancestry evidence shows it is still unpublished. If it is already the current head or its verified ancestor, adopt that successful push after checking current response validity. For reply-only work, do not push.
2. Create only explicitly approved follow-up issues after a fresh duplicate check. Record each created URL; do not create an issue for an unapproved follow-up.
3. Post an exact reply to each feedback item with its disposition and evidence only when no matching submitted reply is already visible under the recovery identity checks. A `follow-up` reply links its approved issue or states that no ticket was created.
4. Resolve only still-unresolved threads whose exact reply succeeded or was independently verified remotely and whose disposition was approved and verified. Keep unresolved ambiguity open.
5. Fresh-read reviews/threads/checks.
6. After an actionable reply or code change has been successfully published and all actionable threads are closed, fresh-read the exact current head and ensure exactly one current-head summary comment contains `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, with `<HEAD_SHA>` replaced by the exact observed head SHA. This summary is required even when no re-review request is needed. If the run published no reply or code change, skip the summary. The summary must be posted or updated after thread closure. If the marker already exists exactly once for the current head, verify its timing and re-review markers; update that same comment when it predates closure or is incomplete instead of creating a duplicate. For each request-eligible reviewer in the frozen code-change set, include one hidden `<!-- tigerkit:pr-rereview:<HEAD_SHA>:<LOGIN> -->` marker in that same comment. Do not add this marker for an account bot, author, authenticated user, still-valid approver, mention-only reviewer, or reply-only finding. A summary for an earlier head does not satisfy this requirement. Write the summary as a real message to the reviewer, not an internal processing record. Address every identifiable human reviewer with `@mention`, map each finding to its disposition, evidence, code response, and follow-up ticket status in natural prose or a matching table, and state when a reviewer is mention-only. Do not publish a third-person completion log that only lists checks or totals.
7. For every request-eligible reviewer in the frozen code-change set, and every human reviewer with a still-active `CHANGES_REQUESTED` review, request re-review for the exact current head unless that reviewer is already requested or has submitted a review after the current-head summary. A current request or a later review is completion evidence; the absence of a current request alone is not. Reply-only feedback with no code change does not require re-review.

Do not claim publication complete unless fresh evidence proves every required reviewer's current request or post-summary
review, zero actionable unresolved threads, and exactly one required current-head summary comment after a published reply or code change.
Missing evidence is `Unverifiable`, not complete.
Do not claim completion while any unresolved inline thread remains.
An approved and verified `follow-up` may be resolved after its exact reply succeeds or is remotely verified;
include the approved issue URL or explicitly state that no ticket was created. Keep unapproved,
unverifiable, or failed feedback open.

Every generated GitHub comment must end with `_🤖 본 코멘트는 AI가 작성했습니다._`.
Do not merge, close, tag, release, plain force push, or resolve unrelated threads.

## Execution under Sweep

For an exact PR handed off by an active `tk-pr-sweep`, do not ask again about material decisions already approved by the parent.
The child confirms the PR fresh state and parent-approved scope, then proceeds immediately when they match.

Reply-only handoffs need no workspace solely for isolation. An explicitly approved index-only handoff uses the exact
PR/head/row identity and run ownership under [code-change execution](references/code-change.md), without a workspace path.
Other code-changing handoffs must include a newly established
dedicated workspace path, exact PR head, and enough provenance to prove it belongs to that row. "Newly established" may
mean a host-native workspace or a safe manual Git fallback; it never requires a nested manual worktree inside an already
proven host-managed workspace. If the path/HEAD/provenance is missing or not fresh, return `Blocked` before mutation. Run
the code-changing child from that workspace; never switch the parent `main` or `develop` checkout to the PR branch.

If new feedback or head drift materially changes the approved scope, escalate only that PR back to the parent.
Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
For a code-changing PR that needs durable context, only `seed.md` in the proven dedicated workspace may be used as task context.

The Respond controller may select SDD for its own PR. Normal implementer/reviewer/re-reviewer children remain leaf and may
not recursively delegate. The parent Sweep decides cross-PR scheduling; this child never starts another PR controller.

## Completion response

Do not output a normal protocol receipt.

When authorship changed the reply-confirmation boundary, state its basis in one concise sentence: name the configured
marker match, account-bot evidence, or absence of marker configuration without dumping the triage record.
Only when an issue remains, explain the blocker and next action in detail.
Use exactly one final state matching the actual result: `Status: Pass | Pending | Blocked | Unverifiable | Fail`.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

In chat responses, use a GFM pipe table for comparisons where several rows share at least two comparable attributes. Use a list for single-attribute enumerations. Keep tables narrow (about four columns or fewer), with a header row and short cells so they remain readable when the host shows raw pipes. Do not draw tables with box-drawing characters, wrap a table in a code fence, or emit an empty or ceremonial table. An owner-specific preview rule, such as summarizing a publication body's table in one line, takes precedence. These chat-table rules do not govern tables inside publication bodies or file artifacts.

In Markdown-rendered chat, documents and PR/issue bodies, write ranges with a hyphen (`146-149`) or spell out both endpoints. Escape a literal tilde as `\~` outside inline code and fenced code; preserve exact quotations and identifiers. Do not use unescaped tildes for prose ranges: GFM may render intervening text as strikethrough.

For authorized user-editable temporary input files, follow the owning skill's Artifact Paths input branch before creation and consumption. A prefilled template does not signal completed input; this rule grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

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
