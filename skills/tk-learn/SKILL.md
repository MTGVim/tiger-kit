---
name: tk-learn
description: "[user/auto] Design a reusable repository or user skill from supplied experience or material. On a clear skill-authoring intent, proceed only through draft and approval checkpoint; do not write before approval."
argument-hint: "<conversation, note, path, URL, workflow, or reflect candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Learn

Apply on explicit invocation or clear intent to author a reusable skill. Turn a
conversation, note, path, URL, repeated workflow, or reflect candidate into a
`repo skill | user skill` candidate. Rules, one-off tips, and ordinary
implementation are out of scope; do not invoke another user-invoked skill.

This is the sole TigerKit writer for new skills and semantic update/merge of
existing skills. A candidate/target from another skill must still pass this
skill's evidence, dedupe, eval, compatibility, and apply gates.

Draft and apply are separate:

- `draft gate`: distinguish verified evidence from unchecked user statements
  and design a `pending` candidate. A clear design request still receives a
  draft when evidence remains `unverified`.
- `apply gate`: every checklist row must pass before any skill-path write.

## Workflow

1. **Evidence ledger:** assign each case/workflow an ID, claim, source, and
   `verified | unverified`. Two user-stated cases whose artifacts are
   inaccessible stay separate unverified rows and still support a draft.
   Promotion requires two independently verified repetitions or an
   artifact-backed reusable workflow. Unverified rows never pass apply.
   One-off mistakes, raw logs, or unsourced single claims end `no-op`.
2. **Promotion and dedupe:** apply
   [skill quality](references/skill-quality.md), then compare existing
   repo/user skills, default model capability, and a short rule. Choose
   `merge | no-op | continue | pending`. If catalogs are unreadable, stay
   `pending` but continue drafting.
3. **Candidate proposal:** give target, working name, invocation kind, and
   positive/negative triggers. Use user domain/workflow language for a
   lowercase hyphen-case verb-led name under 64 characters; check collisions
   and mark `proposed`. Unsupported values stay `TBD`.
4. **Minimum draft:** show minimal SKILL.md input, workflow, failure branches,
   approval boundary, completion criteria, output contract, and DO NOT list.
   Add train/validation triggers, success/boundary assertions, no-skill or
   prior-skill baseline, and portable-core/host-extension decision.
5. **Approval summary:** summarize each apply check and planned path once, then
   stop in the checklist-defined state.
6. **Write, verify, report:** only after Apply authority passes, preserve
   before-write content, write through a same-directory temporary target and
   atomic rename, then reread and verify frontmatter, links, evals, and
   target-host invocation before reporting `applied`.

### Apply gate checklist

| Check | Pass evidence | Not passed |
|---|---|---|
| Promotion threshold | independent cases/common workflow meet promotion criteria | `no-op | pending` |
| Dedupe | difference from existing skill/default capability/short rule and `merge | continue` basis | `no-op | pending` |
| Candidate identity | native target, name, kind, positive/negative triggers confirmed | `pending | Unverifiable` |
| Behavior validation | train/validation triggers and success/boundary assertions pass | `pending | Blocked` |
| Baseline/compatibility | no-skill/prior baseline and portable-core/host-extension decision verified | `pending | Unverifiable` |
| Apply authority | current-turn approval names exact candidate and target path | `pending`; no write |

Use only current-host native repo/user skill paths proven by actual path or
host discovery. Unknown host is `Unverifiable`; never invent a location, force
one host's path on another, fan out/sync across hosts, or use `.tigerkit/` as a
permanent skill registry/global state.

## Failure paths

| Trigger | Immediate action | Still unresolved |
|---|---|---|
| two cases/workflow claimed but artifacts unreadable | record each `unverified` and show requested `pending` draft | request exact artifacts/checks; do not write |
| one one-off case or raw log only | record threshold/privacy and `no-op` | create no candidate/path |
| duplicate of skill/default capability | report `merge | no-op` and basis | create no new directory |
| target/name/trigger partly unknown | draft supported values as `proposed`, others `TBD` | keep Candidate identity `pending`; do not write |
| evidence/target/approval conflict | present conflict and one decision | stop `Blocked` |
| write/post-write check fails | preserve existing target and clean run temp; remove a partial new target only when proven run-owned | restore only when exact/reverifiable; ownership or preservation uncertainty is `Blocked | Unverifiable`, otherwise report actual path and `Fail` |

## 🔴 CHECKPOINT · 🛑 STOP

Before explicit current-turn apply approval, write neither canonical paths nor
`.tigerkit/skill-drafts/<skill-name>/`. Past approval, implicit invocation, and
generic continuation are insufficient. Before approval the candidate is
`pending`; Target path reports the exact planned path plus `not created`.

Even after approval, never report `applied` while any checklist row is unpassed.

## Output contract

Lead with the promotion or no-op decision. Use only non-empty `Evidence`,
`Dedupe`, `Candidate`, `Target path`, `Verification`, and
`Remaining concerns`. For a threshold-failed or duplicate no-op, omit
`Candidate` and `Verification` unless they add decision-relevant evidence.
When more than one candidate is evaluated, render `Candidate` as a compact
`Candidate | Disposition | Target` table. Use a sentence when only one
user-relevant row exists. Summarize two to seven candidate, target, and
remaining-gate results as bounded rows or bullets. For eight or more, show the
top five to seven and cite the draft or planned target path that owns the
remainder. These are budgets, not quotas. Record
`reported | pending | applied` in the owning candidate or concern section
without appending metadata or substituting for candidate results.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not promote one-off cases, credentials, raw logs, or screenshots into
  reusable evidence or copy them into a draft.
- Do not omit a requested pending draft merely because evidence is unverified.
- Do not create a duplicate skill, verbose default-capability wrapper, or
  indistinguishable trigger pair.
- Do not write before approval or treat implicit invocation as authority.
- Do not duplicate name/kind/path/verification/concerns in Receipt.
- Do not archive automatically, edit `.gitignore`, invoke another user skill,
  push, or publish.
