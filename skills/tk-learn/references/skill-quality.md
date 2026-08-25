# Skill quality

Require a clear name, narrow description, inputs, core behavior, boundaries, completion
criteria, and minimal output shape. Keep the directory self-contained. Prefer concise
instructions; add detail only for recurring omissions, costly ordering mistakes, change
safety, objective completion proof, specialist procedures, or bounded delegation/review.

## Upstream distillation

For every `create | improve | merge`, check mature upstream practice before inventing a
TigerKit procedure. When upstream evidence exists:

1. Pin the repository or URL, revision, and relevant paths or locations as provenance.
2. Read the current implementation, its rationale, and behavior or failure-mode eval evidence.
   Mark anything unavailable as `unverified`; a reputation or summary is not a substitute.
3. Compare each transferable contract with TigerKit's existing owner and boundary. In
   `learn.md`, give every applicable element a literal `keep`, `adapt`, or `omit` label plus
   its reason; do not replace the disposition with a synonym.
4. Distill behavior and failure modes. Do not copy provider routing, runtime state, workspace
   machinery, helper frameworks, or other infrastructure outside TigerKit's Agent Skills boundary.
5. Prefer the existing simpler TigerKit contract when the comparison reveals no concrete gap.

## Promotion gate

- One verified route is sufficient: mature upstream plus a concrete TigerKit gap; a strongly verified reusable incident;
  explicit reusable workflow intent plus sufficient source material or repository evidence; or genuinely recurring
  verified cases. Do not impose a universal incident count.
- A strongly verified incident has attributable source evidence, an exact reproduction, a root cause, a correction that
  generalizes beyond the event, and independent or holdout verification. A weak anecdote, raw log, or one-off mistake
  without reusable correction evidence remains `no-op | pending`.
- Check whether an existing skill, default model capability, or a short rule is enough.
  Prefer `merge | no-op` over a duplicate directory.
- Provide distinguishable positive and negative triggers. Separate description training
  from regression validation. Stop creation when triggers remain ambiguous.
- Include at least one success evaluation and one boundary/failure evaluation with
  observable assertions. Do not store raw secrets, credentials, logs, or screenshots.
- Define comparison against a prior skill, no-skill behavior, or another named baseline.
  Prose scores alone are insufficient.
- Separate portable-core Agent Skills fields from target-host extensions and do not copy
  the body per host. Leave unknown target-host `invocation` as `pending`.
- Before approval, candidate state is `reported | pending` and no files are applied.
  Only post-approval success receives `applied`.

## Draft artifact checkpoint

Before approval, record the draft only in `.tigerkit/learn.md` at the repository root as
a `pending` scratch ledger. Record the candidate, evidence, checklist, target path,
paths not created, next step, and decision/status; rename it atomically and read it back.
If it is missing, stale, or mismatched on re-read, return `Blocked` and stop both the
approval question and canonical write. Chat shows only the absolute path, status, short
summary, and one approval question; do not copy the full ledger or exact file body.
Before approval, the canonical skill path and `.tigerkit/skill-drafts/<skill-name>/`
must remain `not created`.

User-facing progress and receipt prose follow the user's language.
