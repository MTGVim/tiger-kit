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

Invocation kind spends the same load budget. A model-invoked or hybrid skill pays an
always-loaded model-facing description so the model or another skill can discover it;
choose that reach only when autonomous discovery or composition is behaviorally useful.
When a workflow is intentionally human-selected, prefer user invocation and let the human
be the index. Do not change an existing invocation kind merely to reduce context: compare
positive/negative routing and body behavior first.

Prune behaviorally, not aesthetically. For every candidate removal or compression, compare
no-skill/prior behavior on a realistic task. A sentence that is long but prevents a known
pressure failure earns its load; a short sentence that changes no behavior is a no-op.
Prefer positive steering for ordinary behavior, while preserving explicit hard stops for
authority, destructive mutation, secrets, freshness, and cross-scope safety boundaries.

### Body-size review signals

For a new or simple skill, use roughly 180–450 body tokens as an initial target when practical.
Above about 700 tokens, review whether branch-specific procedures, examples, or schemas can be
lazy-loaded. At about 1000 tokens or more, perform an instruction-load review. These thresholds
are review signals, never correctness gates or hard limits.

Preserve behavior before optimizing size. Never remove or blur authority, destructive-mutation,
secrets/privacy, freshness/drift, cross-scope safety, or behaviorally proven pressure guards to
meet a budget. A smaller token count is not success: compare prior-skill/candidate behavior, and
do not move content to references merely to shrink the body. Priority is behavior preservation,
then safety/authority correctness, instruction economy, and raw token count.

## Upstream distillation

For every `create | improve | merge`, check mature upstream practice before inventing a
TigerKit procedure. When upstream evidence exists:

1. Pin the repository or URL, revision, and relevant paths or locations as provenance.
2. Read the current implementation, its rationale, and behavior or failure-mode eval evidence.
   Mark anything unavailable as `unverified`; a reputation or summary is not a substitute.
3. Compare each transferable contract with TigerKit's existing owner and boundary. In
   the active candidate packet, give every applicable element a literal `keep`, `adapt`, or `omit` label plus
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

## Draft state checkpoint

Before approval, retain one complete `pending` candidate packet with candidate, evidence, checklist, target path, paths
not created, next step, and decision/status. Use `.tigerkit/learn.md` only when explicit persistence, handoff/recovery,
candidate complexity, or host retention limits require it; rename it atomically and read it back. If that required
artifact is missing, stale, or mismatched, return `Blocked` and stop both approval and canonical write. A clear same-turn
candidate or `no-op` does not need a scratch file. Chat shows only status, a short summary, the path when one exists, and
one approval question when apply is eligible; do not copy the full packet or exact file body.
Before approval, the canonical skill path and `.tigerkit/skill-drafts/<skill-name>/`
must remain `not created`.

User-facing progress and receipt prose follow the user's language.
