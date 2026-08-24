# Skill quality

Require a clear name, narrow description, inputs, core behavior, boundaries, completion
criteria, and minimal output shape. Keep the directory self-contained. Prefer concise
instructions; add detail only for recurring omissions, costly ordering mistakes, change
safety, objective completion proof, specialist procedures, or bounded delegation/review.

## Promotion gate

- Require either two independent recurrences or an artifact-backed reusable workflow.
  Unsourced claims and one-off cases do not satisfy promotion.
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
