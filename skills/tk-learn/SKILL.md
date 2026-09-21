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

Apply this to an explicit `invocation` or clear intent to author a reusable `skill`.
Convert conversations, notes, paths, URLs, repeated workflows, or skill-evolution
candidates into `repo skill | user skill` candidates. Rules, one-off tips, and general
implementation are out of scope, and never invoke another user-invoked `skill`.

This is the sole TigerKit author for `skill` `create | improve | merge`, including new
`skill`s and semantic updates. Candidates or targets from other `skill`s must also pass
evidence, deduplication, evaluation, compatibility, and apply gates.

For every `create | improve | merge`, check mature upstream practice first when available.
Use [Skill quality](references/skill-quality.md) to verify provenance, distill behavior and
failure modes, and record each applicable disposition with the literal `keep | adapt | omit`
label; never copy an upstream framework wholesale.

A verified `learn-ready` from `tk-skill-diagnose` may enter candidate processing when the active user request
already includes a semantic fix for the same target and scope. A bare request to write to a skill path without
a reusable objective does not establish learning intent. Reuse that authorization at its actual extent;
do not require a new invocation merely because diagnosis finished. A diagnosis-only handoff, generic skill
discussion, one-off tip, or ordinary implementation does not activate this route. Recheck material target,
scope, and evidence drift and every apply gate before canonical writes; the handoff itself is not authority.

Draft and apply are separate.

- `draft gate`: Distinguish verified evidence from unverified user claims and design a
  `pending` candidate. Even when evidence remains `unverified`, keep a clear design
  request in the active candidate packet without treating it as apply evidence.
- `apply gate`: Every checklist row must pass before writing to a `skill` path.

## Need-based draft checkpoint
When candidate or apply approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, present the same approval packet in plain chat; do not write a canonical skill path before approval.

Keep a straightforward same-turn candidate in the current interaction when the host can faithfully retain and reread it.
Use the singleton repository-root `.tigerkit/learn.md` only for explicit `save`, multi-turn handoff/recovery, a complex
candidate whose evidence/checklist cannot fit safely in the approval packet, or when the host cannot retain exact state.
Do not create the artifact for a clear `no-op` merely to report that nothing should change. This file is neither a
canonical `skill` path nor `.tigerkit/skill-drafts/<skill-name>/`.

The active candidate packet, and `learn.md` when used, owns each of these fields exactly once: work `Status` (`Pending | Blocked`),
`Disposition` (`reported | applied | pending`),
`Decision` (`proposed | merge | no-op | continue | pending`), `Candidate`,
`Evidence` (ID/source/`verified | unverified` for every claim), `Checklist` (each apply
check's `passed | pending | failed` state and evidence), `Target path` (the exact planned
path and `not created`), `Not created` (both canonical write boundaries),
`Next step` (one executable action), and `Updated` (write time or run ID).

Use `Disposition: reported | pending` for a candidate, including a successfully written and reread draft ledger. Reserve `Disposition: applied` for an authorized canonical skill mutation whose write and verification succeeded. Recording a proposal is not applying it.

When an artifact is required, create a temporary file in the same directory, atomically rename it, and reread
immediately. If required fields are absent, the ledger is stale or missing, or the reread differs from the written
content, stop as `Blocked` and do not write canonical paths. Do not overwrite a different active candidate; stale
completed content may be invalidated and replaced, never archived into per-run files.

## Workflow

1. **Evidence:** Accept any sufficient route: mature upstream plus a concrete TigerKit gap; one strongly verified,
   reusable incident; explicit reusable workflow intent plus sufficient source or repository evidence; or genuinely
   recurring verified cases. Weak anecdotes, raw logs, unsourced claims, and one-off mistakes without reusable
   correction evidence do not promote. Once one route is verified, advance to a pending candidate and the remaining
   gates instead of requesting recurrence. Unverified claims cannot pass apply.
2. **Promotion and deduplication:** Apply [Skill quality](references/skill-quality.md),
   then compare against existing repository/user `skill`s, default model capability,
   and a short rule. Choose one of `merge | no-op | continue | pending`. If the
   catalog cannot be read, remain `pending` and record that status and rationale in the candidate packet.
   Before skill/rule promotion, use the mechanical-enforceability gate in Skill quality.
   If a repository-native check is the better owner, stop skill promotion with `no-op`
   and propose its smallest useful extension. This does not authorize repository edits:
   change lint/CI/hooks/code only when the active request explicitly includes that change
   and existing authority permits it. Do not create a handoff artifact just for this decision.
3. **Candidate proposal:** Present the target, action name, invocation kind, and
   positive/negative triggers. Draft a trigger-first description that answers when to
   load and preserves only the routing discriminators; keep procedure in the body.
   Use the user's domain/workflow language to choose a lowercase, hyphenated,
   verb-form name of at most 64 characters; check for collisions, then mark it
   `proposed`. Leave unsupported values as `TBD`.
4. **Minimal draft:** Record the minimal SKILL.md inputs, workflow, failure branches,
   approval boundaries, completion criteria, output contract, and prohibitions
   directly in the candidate packet. Also add train/validation triggers, success/boundary
   assertions, behavior evidence designed for the candidate's skill type, a no-skill
   or prior-skill baseline, and the
   portable-core/host-extension determination.
5. **Approval checkpoint:** After rereading the active packet and any required `learn.md`, follow the checkpoint and
   output contract below. Ask only if exact apply authority is missing; otherwise continue to writing in the same turn.
6. **Write, verify, report:** After every checklist row and apply authority pass,
   preserve the pre-write contents, write with an atomic rename, then reread and
   verify frontmatter, links, evals, and target-host invocation.

### Apply gate checklist

| Check | Passing evidence | If not passed |
|---|---|---|
| Promotion threshold | One sufficient evidence route in Skill quality is verified | `no-op \| pending` |
| Deduplication | Differences from existing skill/default capability/short rule and rationale for `merge \| continue` exist | `no-op \| pending` |
| Candidate identity | Native target, name, kind, trigger-first description, and positive/negative routing discriminators are confirmed | `pending \| Unverifiable` |
| Behavior validation | Observable train/validation routing and skill-type success/boundary behavior pass; source-text presence alone is insufficient | `pending \| Blocked` |
| Baseline/compatibility | A practical no-skill baseline for creation or prior-skill baseline for semantic edits and the portable-core/host-extension determination are verified | `pending \| Unverifiable` |
| Apply authority | Active-task approval names the exact candidate and target path | `pending`; do not write |

Use only the current host's native repo/user `skill` paths proven through actual path
or host discovery. An unknown host is `Unverifiable`. Do not invent locations, force
one host's paths onto another host, perform cross-host fan-out/sync, or use
`.tigerkit/` as a permanent `skill` registry/global state.

## Failure paths

| Trigger | Immediate action | What remains unresolved |
|---|---|---|
| Cases/workflows are claimed but artifacts cannot be read | Record each as `unverified` and leave the candidate `Blocked` | Request exact artifacts/checks; do not write |
| Only a weak one-off anecdote or raw log exists | Report the threshold/privacy basis with `Decision: no-op`, `Status: Pending` | Create no artifact, candidate, or path unless explicit `save` is requested |
| Duplicate of a skill/default capability | Report `merge \| no-op` and rationale | Create no new directory |
| Some target/name/trigger is unknown | Record supported values as `proposed` and the rest as `TBD` in the candidate packet | Keep candidate identity `pending`; do not write |
| Evidence, target, or approval conflicts | Present the conflict and one decision | Stop as `Blocked` |
| Write/post-write verification fails | Preserve the existing target and run temporary file; remove a partially created new target only when run ownership is proven | Recover only when exactly reproducible/verifiable; report `Blocked \| Unverifiable` when ownership/preservation is unclear, otherwise report the actual path and `Fail` |

## 🔴 CHECKPOINT · 🛑 STOP (Approval and stop point)

Do not write to the canonical path or
`.tigerkit/skill-drafts/<skill-name>/` before explicit active-task apply approval.
An earlier explicit approval of this candidate and target remains sufficient while scope matches. Implicit `invocation`, a recovered artifact alone, and a generic request to continue without that authorization are insufficient. Before approval, the candidate remains `pending`, and Target
path records the exact planned path and `not created`.

The approval checkpoint occurs only after rereading the complete active packet and any required `.tigerkit/learn.md`.
When the artifact branch is required, a write or reread failure is `Blocked` and cannot request approval. A simple
same-turn packet may proceed without the artifact; the one-off `no-op` branch creates neither.

## Output contract

Report `Decision`/`Status`/`Disposition` and, when created, the exact `learn.md` path, then summarize the key result in
only `1–3` lines. End with one approval question only when apply is eligible and authorization is missing. When authorized, apply and verify without that question. A `no-op` ends without an invented
approval question. Do not copy the packet's full `Evidence`, `Dedupe`, `Candidate`,
`Target path`, `Verification`, or `Remaining concerns` into chat. A no-op caused by a threshold
failure or duplicate remains concise and need not materialize an artifact.

## Prohibitions / antipatterns

- Do not promote weak one-off anecdotes, credentials, raw logs, or screenshots as
  reusable evidence or copy them into a draft.
- Do not omit a requested `pending` draft because evidence is `unverified`.
- Do not create duplicate `skill`s, verbose wrappers around default capability, or
  indistinguishable trigger pairs.
- Do not duplicate the name/kind/path/verification/concerns in the Receipt.
- Do not auto-archive, invoke another user `skill`, push, or publish. Limit ignore edits
  to the authorized artifact setup described in Artifact Paths.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, and lessons in `study/<topic>/`. Preserve existing owner-specific paths and explicit user-selected final destinations. Create artifacts only when the active task calls for them. Before writing, verify the repository root, no tracked `.tigerkit` paths, and safe nonsymlink destinations. From the repository root, run `git ls-files -- .tigerkit .tigerkit/` to check tracking, then `git check-ignore -q -- .tigerkit/` to check effective exclusion. Exit 0 means leave ignore files unchanged, including when exclusion comes from `core.excludesFile` (such as configured `~/.gitignore`), the default global ignore file, or `.git/info/exclude`; a missing repository `.gitignore` or missing literal entry is not evidence of missing coverage. Only exit 1 permits creating the root `.gitignore` or appending `/.tigerkit/`, preserving existing bytes and line endings, then rerunning the same check before writing. Any other exit status or command failure blocks the file branch without an ignore edit. Use `git check-ignore -v -- .tigerkit/` only to diagnose the source; a printed negated pattern is not proof of exclusion. This narrow ignore setup is part of an authorized artifact write even for a read-only task; it grants no other source/config/index/commit/publication authority. Existing effective ignore rules need no edit. Do not untrack files or follow a symlinked/nonregular `.gitignore`; if unsafe, unwritable, still unignored, or no repository is identified, stop only the file branch as `Blocked | Unverifiable`, without an OS-temp fallback. Briefly report an ignore edit; never stage or commit it solely for setup. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.
