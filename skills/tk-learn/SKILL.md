---
name: tk-learn
description: "[user/auto] Design a reusable repository or user skill from supplied experience or material. On a clear skill-authoring intent, proceed only through draft and approval checkpoint; do not write before approval."
argument-hint: "<conversation, note, path, URL, workflow, or skill-evolution candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Learn

Apply on explicit invocation or clear intent to author reusable skill. Turn conversation, note, path, URL, repeated workflow, or skill-evolution candidate into `repo skill | user skill` candidate. Rules, one-off tips, and ordinary implementation are out of scope; never invoke another user-invoked skill.

Sole TigerKit writer for skill `create | improve | merge`, including new skills and semantic updates. Candidate/target from another skill must still pass evidence, dedupe, eval, compatibility, and apply gates.

Draft/apply are separate:

- `draft gate`: distinguish verified evidence from unchecked user statements; design `pending` candidate. Clear design request still gets draft when evidence remains `unverified`.
- `apply gate`: every checklist row must pass before skill-path write.

## Workflow

1. **Evidence ledger:** assign each case/workflow ID, claim, source, and `verified | unverified`. Two user-stated cases with inaccessible artifacts stay separate unverified rows and support draft. Promotion needs two independently verified repetitions or artifact-backed reusable workflow. Unverified rows never pass apply. One-off mistakes, raw logs, or unsourced single claims end `no-op`.
2. **Promotion and dedupe:** apply [skill quality](references/skill-quality.md), then compare existing repo/user skills, default model capability, and short rule. Choose `merge | no-op | continue | pending`. If catalogs unreadable, stay `pending` but continue drafting.
3. **Candidate proposal:** give target, working name, invocation kind, and positive/negative triggers. Use user domain/workflow language for lowercase hyphen-case verb-led name under 64 characters; check collisions and mark `proposed`. Unsupported values remain `TBD`.
4. **Minimum draft:** show minimal SKILL.md input, workflow, failure branches, approval boundary, completion criteria, output contract, and DO NOT list. Add train/validation triggers, success/boundary assertions, no-skill or prior-skill baseline, and portable-core/host-extension decision.
5. **Approval summary:** summarize each apply check and planned path once; stop in checklist-defined state.
6. **Write, verify, report:** only after Apply authority passes, preserve before-write content, write through same-directory temporary target and atomic rename, then reread/verify frontmatter, links, evals, and target-host invocation before `applied`.

### Apply gate checklist

| Check | Pass evidence | Not passed |
|---|---|---|
| Promotion threshold | independent cases/common workflow meet promotion criteria | `no-op | pending` |
| Dedupe | difference from existing skill/default capability/short rule and `merge | continue` basis | `no-op | pending` |
| Candidate identity | native target, name, kind, positive/negative triggers confirmed | `pending | Unverifiable` |
| Behavior validation | train/validation triggers and success/boundary assertions pass | `pending | Blocked` |
| Baseline/compatibility | no-skill/prior baseline and portable-core/host-extension decision verified | `pending | Unverifiable` |
| Apply authority | current-turn approval names exact candidate and target path | `pending`; no write |

Use only current-host native repo/user skill paths proven by actual path or host discovery. Unknown host is `Unverifiable`; never invent location, force one host's path on another, fan out/sync across hosts, or use `.tigerkit/` as permanent skill registry/global state.

## Failure paths

| Trigger | Immediate action | Still unresolved |
|---|---|---|
| two cases/workflow claimed but artifacts unreadable | record each `unverified`; show requested `pending` draft | request exact artifacts/checks; no write |
| one one-off case or raw log only | record threshold/privacy and `no-op` | create no candidate/path |
| duplicate of skill/default capability | report `merge | no-op` and basis | create no new directory |
| target/name/trigger partly unknown | draft supported values as `proposed`, others `TBD` | keep Candidate identity `pending`; no write |
| evidence/target/approval conflict | present conflict and one decision | stop `Blocked` |
| write/post-write check fails | preserve existing target and clean run temp; remove partial new target only when proven run-owned | restore only when exact/reverifiable; ownership/preservation uncertainty is `Blocked | Unverifiable`, else report actual path and `Fail` |

## 🔴 CHECKPOINT · 🛑 STOP

Before explicit current-turn apply approval, write neither canonical paths nor `.tigerkit/skill-drafts/<skill-name>/`. Past approval, implicit invocation, and generic continuation are insufficient. Before approval candidate is `pending`; Target path reports exact planned path plus `not created`.

Even after approval, never report `applied` while any checklist row remains unpassed.

## Output contract

Lead with promotion/no-op decision. Use only non-empty `Evidence`, `Dedupe`, `Candidate`, `Target path`, `Verification`, and `Remaining concerns`. For threshold-failed or duplicate no-op, omit `Candidate` and `Verification` unless decision-relevant. For multiple candidates, render `Candidate` as compact `Candidate | Disposition | Target` table; use sentence for one user-relevant row. Summarize 2–7 candidate, target, and remaining-gate results as bounded rows/bullets. For 8+, show top 5–7 and cite draft/planned target path owning remainder. Budgets, not quotas. Record `reported | pending | applied` in owning candidate/concern section; never append metadata or substitute for candidate results.

## DO NOT / ANTI-PATTERNS

- Never promote one-off cases, credentials, raw logs, or screenshots into reusable evidence or copy into draft.
- Never omit requested pending draft because evidence is unverified.
- Never create duplicate skill, verbose default-capability wrapper, or indistinguishable trigger pair.
- Never write before approval or treat implicit invocation as authority.
- Never duplicate name/kind/path/verification/concerns in Receipt.
- Never auto-archive, edit `.gitignore`, invoke another user skill, push, or publish.
