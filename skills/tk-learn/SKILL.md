---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료에서 재사용 가능한 repository 또는 user skill을 설계합니다. 명확한 skill-authoring intent가 있으면 draft와 approval checkpoint까지만 진행하며, approval 전에는 쓰지 않습니다."
disable-model-invocation: false
argument-hint: "<conversation, note, path, URL, workflow, or skill-evolution candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill learning

Apply this to an explicit `invocation` or clear intent to author a reusable `skill`.
Convert conversations, notes, paths, URLs, repeated workflows, or skill-evolution
candidates into `repo skill | user skill` candidates. Rules, one-off tips, and general
implementation are out of scope, and never invoke another user-invoked `skill`.

This is the sole TigerKit author for `skill` `create | improve | merge`, including new
`skill`s and semantic updates. Candidates or targets from other `skill`s must also pass
evidence, deduplication, evaluation, compatibility, and apply gates.

Draft and apply are separate.

- `draft gate`: Distinguish verified evidence from unverified user claims and design a
  `pending` candidate. Even when evidence remains `unverified`, record a clear design
  request in `learn.md` without printing the full text in chat.
- `apply gate`: Every checklist row must pass before writing to a `skill` path.

## Artifact-first draft checkpoint
When candidate or apply approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, present the same approval packet in plain chat; do not write a canonical skill path before approval.

For a new draft, do not print the full minimal draft in chat before approval. First atomically
write a `pending` scratch ledger at repository-root `.tigerkit/learn.md`, then reread that same
path for verification. This file is neither a canonical `skill` path nor
`.tigerkit/skill-drafts/<skill-name>/`.

`learn.md` owns each of these fields exactly once: work `Status` (`Pending | Blocked`),
`Disposition` (`reported | applied | pending`),
`Decision` (`proposed | merge | no-op | continue | pending`), `Candidate`,
`Evidence` (ID/source/`verified | unverified` for every claim), `Checklist` (each apply
check's `passed | pending | failed` state and evidence), `Target path` (the exact planned
path and `not created`), `Not created` (both canonical write boundaries),
`Next step` (one executable action), and `Updated` (write time or run ID).

Use `Disposition: applied` when the atomic write and reread match the current candidate/run,
but preserve work `Status: Pending` before apply approval. `Disposition` describes the ledger
write/reread result and is not synonymous with `Status`.

Create a temporary file in the same directory, atomically rename it, and reread immediately.
If required fields are absent, the ledger is stale or missing, or the reread differs from the
written content, stop as `Blocked` and do not write canonical paths. If an existing ledger points
to another candidate/run, do not overwrite it; report `Blocked`.

## Workflow

1. **Evidence ledger:** Assign each case/workflow an ID, claim, source, and
   `verified | unverified`. Keep two user-claimed cases with inaccessible artifacts
   as separate `unverified` rows and record `pending` status in `learn.md`. Promotion
   requires two independently verified repetitions or a reusable workflow supported
   by artifacts. `Unverified` rows cannot pass apply. End one-off mistakes, raw logs,
   and single unsourced claims as `no-op`.
2. **Promotion and deduplication:** Apply [Skill quality](references/skill-quality.md),
   then compare against existing repository/user `skill`s, default model capability,
   and a short rule. Choose one of `merge | no-op | continue | pending`. If the
   catalog cannot be read, remain `pending` and record that status and rationale in
   `learn.md`.
3. **Candidate proposal:** Present the target, action name, invocation kind, and
   positive/negative triggers. Use the user's domain/workflow language to choose a
   lowercase, hyphenated, verb-form name of at most 64 characters; check for
   collisions, then mark it `proposed`. Leave unsupported values as `TBD`.
4. **Minimal draft:** Record the minimal SKILL.md inputs, workflow, failure branches,
   approval boundaries, completion criteria, output contract, and prohibitions
   directly in `learn.md`. Also add train/validation triggers, success/boundary
   assertions, a no-skill or prior-skill baseline, and the
   portable-core/host-extension determination.
5. **Approval checkpoint:** After rereading `learn.md`, follow the checkpoint and
   output contract below, then stop.
6. **Write, verify, report:** After every checklist row and apply authority pass,
   preserve the pre-write contents, write with an atomic rename, then reread and
   verify frontmatter, links, evals, and target-host invocation.

### Apply gate checklist

| Check | Passing evidence | If not passed |
|---|---|---|
| Promotion threshold | Independent cases/common workflow meet the promotion threshold | `no-op | pending` |
| Deduplication | Differences from existing skill/default capability/short rule and rationale for `merge | continue` exist | `no-op | pending` |
| Candidate identity | Native target, name, kind, and positive/negative triggers are confirmed | `pending | Unverifiable` |
| Behavior validation | Train/validation triggers and success/boundary assertions pass | `pending | Blocked` |
| Baseline/compatibility | No-skill/prior baseline and portable-core/host-extension determination are verified | `pending | Unverifiable` |
| Apply authority | Current-turn approval names the exact candidate and target path | `pending`; do not write |

Use only the current host's native repo/user `skill` paths proven through actual path
or host discovery. An unknown host is `Unverifiable`. Do not invent locations, force
one host's paths onto another host, perform cross-host fan-out/sync, or use
`.tigerkit/` as a permanent `skill` registry/global state.

## Failure paths

| Trigger | Immediate action | What remains unresolved |
|---|---|---|
| Two cases/workflows are claimed but artifacts cannot be read | Record each as `unverified` and leave `learn.md` `Blocked` | Request exact artifacts/checks; do not write |
| Only one one-off case or raw log exists | Record the threshold/privacy basis with `Decision: no-op`, `Status: Pending` | Create no candidate or path |
| Duplicate of a skill/default capability | Report `merge | no-op` and rationale | Create no new directory |
| Some target/name/trigger is unknown | Record supported values as `proposed` and the rest as `TBD` in `learn.md` | Keep candidate identity `pending`; do not write |
| Evidence, target, or approval conflicts | Present the conflict and one decision | Stop as `Blocked` |
| Write/post-write verification fails | Preserve the existing target and run temporary file; remove a partially created new target only when run ownership is proven | Recover only when exactly reproducible/verifiable; report `Blocked | Unverifiable` when ownership/preservation is unclear, otherwise report the actual path and `Fail` |

## 🔴 CHECKPOINT · 🛑 STOP (Approval and stop point)

Do not write to the canonical path or
`.tigerkit/skill-drafts/<skill-name>/` before explicit current-turn apply approval.
Past approval, implicit `invocation`, and a generic request to continue are
insufficient authority. Before approval, the candidate remains `pending`, and Target
path records the exact planned path and `not created`.

The approval checkpoint for a new draft occurs only after writing and rereading
`.tigerkit/learn.md`; a write or reread failure is `Blocked` and cannot request
approval. The failure table owns the one-off `no-op` status.

## Output contract

After writing the artifact, first report the exact `learn.md` path and
`Decision`/`Status`/`Disposition`, then summarize the key result in only `1–3` lines. End with
exactly one approval question. Do not copy the ledger's full `Evidence`, `Dedupe`, `Candidate`,
`Target path`, `Verification`, or `Remaining concerns` into chat. A no-op caused by a threshold
failure or duplicate follows the same artifact-first rule.

## Prohibitions / antipatterns

- Do not promote one-off cases, credentials, raw logs, or screenshots as reusable
  evidence or copy them into a draft.
- Do not omit a requested `pending` draft because evidence is `unverified`.
- Do not create duplicate `skill`s, verbose wrappers around default capability, or
  indistinguishable trigger pairs.
- Do not duplicate the name/kind/path/verification/concerns in the Receipt.
- Do not auto-archive, edit `.gitignore`, invoke another user `skill`, push, or
  publish.
