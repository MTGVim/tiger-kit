# Skill quality

Require a clear name, narrow description, inputs, core behavior, boundaries, completion
criteria, and minimal output shape. Keep the directory self-contained. Prefer concise
instructions; add detail only for recurring omissions, costly ordering mistakes, change
safety, objective completion proof, specialist procedures, or bounded delegation/review.

## Trigger-first descriptions

A description answers only whether the skill should load now. Preserve the smallest
routing discriminators needed for positive and negative selection: concrete triggers,
symptoms, intended scope, and exclusions. Keep workflow order, internal routing,
approval sequence, artifact lifecycle, and procedure in the body. A process summary
that could substitute for reading the body fails this rule even if routing cases pass.

## Agent-facing instruction economy

Treat a skill description and every conditional reference link as a **context pointer**:
it should identify the material and the distinct branch/condition that makes reading it
necessary. Do not repeat body identity or workflow in the pointer. Put behavior needed by
every execution path in the body; move branch-specific reference behind a precise pointer
only when doing so keeps the main path clearer without hiding a load-bearing guard.

The environment is also a source of truth. Do not copy cheap, fresh facts such as current
package/config values, directory inventory, or host/tool capability into prose unless the
skill intentionally owns that value as a contract or the lookup is expensive/unreliable.
A duplicated environmental fact is a stale-cache risk, not useful context.

Prune behaviorally, not aesthetically. For every candidate removal or compression, compare
no-skill/prior behavior on a realistic task. A sentence that is long but prevents a known
pressure failure earns its load; a short sentence that changes no behavior is a no-op.
Prefer positive steering for ordinary behavior, while preserving explicit hard stops for
authority, destructive mutation, secrets, freshness, and cross-scope safety boundaries.

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

## Behavior-first evaluation

Source-text presence, a successful grep, or proof that a file was loaded does not by
itself prove skill behavior. Use observable outcomes and realistic judge criteria.

- For a new skill, observe a no-skill baseline when practical. For a semantic edit to
  an existing skill, compare the prior skill and candidate on the same scenarios.
  If the required baseline cannot run, mark it `unverified` instead of substituting a
  source-text check.
- For a discipline-enforcing skill, use combined pressure and rationalization scenarios
  that make violation tempting and require an observable choice.
- For a technique skill, test new applications, variations, missing information, and
  relevant edge cases rather than replaying only the source example.
- For a pattern or mental-model skill, test recognition and application plus a
  counter-example that establishes when not to apply it.
- For a reference skill, verify that the agent finds the needed information and applies
  it correctly to a realistic task; text retrieval alone is insufficient.
- When a description changes, compare prior and candidate positive/negative routing,
  including false-positive invocation, and verify that the candidate still follows the
  body behavior rather than treating the description as the procedure.
- For pointer/disclosure edits, verify both sides: the required reference is reached on
  the branch that needs it, and unrelated branches do not pay the load or inherit rules
  they never use.
- For instruction pruning, a source-text deletion or smaller token count is not success;
  the relevant task behavior and safety boundary must remain unchanged.

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
