# Skill quality

Require a clear name, narrow description, input, core behavior, boundaries,
completion criteria, and minimum output shape. Keep the directory
self-contained. Prefer concise instructions; add detail only for repeated
omissions, costly ordering errors, mutation safety, objective completion
proof, specialist procedure, or bounded delegation/review.

## Promotion gate

- Require two independent repetitions or a reusable workflow backed by an
  artifact. Unsourced claims and one-off cases miss threshold.
- Check existing skills, default model capability, and whether a short rule is
  sufficient. Prefer `merge | no-op` over a duplicate directory.
- Provide distinguishable positive/negative triggers; separate description
  training from regression validation. Unclear triggers stop creation.
- Include at least one success and one boundary/failure behavior eval with
  observable assertions. Never persist raw secrets, credentials, logs, or
  screenshots.
- Define comparison against a prior skill, no-skill, or named baseline; prose
  score alone is insufficient.
- Separate Agent Skills portable-core fields from target-host extensions and
  never copy the body per host. Unknown target-host invocation stays `pending`.
- Before approval, candidate status is `reported | pending` and no file is
  applied. Only post-approval success receives `applied`.

User-facing progress and receipt prose follows the user's language.
