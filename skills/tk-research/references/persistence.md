# Research persistence

Read before initializing durable research, migrating legacy state, recording a material outcome,
sharing tracked knowledge, or making research-owned local commits.

## One local canonical home

Default to ignored `.tigerkit/research/<slug>/state.md`, with a filesystem-safe goal slug and a
stable `researchId` derived from repository identity and the initial normalized goal, never secrets
or personal identifiers. A slug is a display/path hint, not project identity: verify `researchId`
and repository identity before reuse. A different owner requires a noncolliding sibling path.
No configuration file, tracked tree or worktree is required for read-only research. Create state
only when resume, frontier/history, negative results or next-batch evidence reuse needs it.

The state is the hot index; retain decision-relevant findings and material checkpoint/experiment
records under this same home only as needed. Do not create empty knowledge scaffolding. HTML is
a projection and never the resume source. Short research can retain its verified facts in the
current interaction without a state file. Apply Artifact Paths before every write.

Source-changing experiments require a safe isolated research workspace. Reuse a clean, explicitly
designated non-product home or create/reuse a dedicated linked research worktree under the active
local authority, honoring repository/user restrictions on branch/worktree creation. A default/product,
dirty, shared or differently owned checkout is unsafe for experimental mutation. If isolation is
unavailable, continue read-only items; stop the mutation branch rather than absorb unrelated work.
Move only run-owned local state/evidence into the experiment home with identity/readback checks;
leave one canonical home and record its location. Never split one project across competing states.

A small material delta can use one state update containing findings, the checkpoint entry and handoff. Split substantial reusable experiment evidence only when needed; reference it instead of repeating narratives in synthesis, journal and handoff files. Keep freshness fingerprints in transient run context or the state's prior transaction fields; no extra transaction/baseline/config receipt is required.

## Material outcome transaction

Capture state fingerprint and home HEAD at batch start; recheck both before final ID allocation or
write. External drift requires safe reconciliation against fresh state or `BLOCKED` with run-owned
evidence preserved; never overwrite newer state or reuse IDs.

Before `CHECKPOINT`, `CONCLUDE` or evidence-producing `BLOCKED`:

1. Allocate fresh monotonic `CHK-<NNN>` / `EXP-<NNN>` IDs after the drift check.
2. Finalize attempted experiments including negative, inconclusive and blocked evidence; retain
   sources, acceptance/evaluator identity, limits, next implications and relevant parent lessons.
3. Record the material delta in findings and one checkpoint entry, update synthesis/frontier and
   atomically write canonical state; reread it. Keep untested budget deferrals separate from rejection.
4. Generate the human projection using [report](report.md). A report failure leaves canonical facts
   intact and marks only the artifact branch `Unverifiable`; do not claim an unwritten report.
5. Make an optional local experiment commit only when coherent run-owned code has future value;
   stage exact owned paths, never unrelated work. Record its HEAD in local state. No default knowledge
   commit, tracked mirror or commit-on-checkpoint policy exists.

Record a minimal blocker without inventing a checkpoint when no evidence delta exists. Preserve
negative results before reverting/discarding run-owned failed code. `CONCLUDE` includes identity,
home HEAD, accepted findings/experiments, rejected alternatives, limits and a next-owner handoff;
research code is evidence, not production readiness or product integration authority.

## Explicit shareable knowledge

Only an explicit save/share request promotes a sanitized report or decision-relevant knowledge to
an agreed repository-relative destination outside `.git/` and `.tigerkit/`. Validate nonsymlink
paths and ownership; never overwrite another project's files. A save is not commit/publication
authority. HTML and tracked Markdown are shareable projections, never canonical execution mirrors.
Do not write secrets, raw operational/protected data, direct personal identifiers, request/response
dumps or full sensitive logs into shared files or ignored state. Use minimum abstractions, source
revision, experiment IDs/hashes and safe ignored evidence pointers; retain raw authorized evidence
only temporarily in a run-owned ignored location. If sanitization cannot preserve a claim, report
its limitation rather than expose the data. Failed exports preserve local facts without false success.

## Legacy migration

`tk-autoresearch` is removed; install/invoke `tk-research`. Discover an actual matching legacy
`.tigerkit/autoresearch/state.md` only on explicit resume or migration, within this repository's
current/linked homes. Preserve `researchId`, repository/home identity, stable IDs, findings (including
negative results), experiments, source/evaluator provenance, premises, pending questions, frontier,
reopen conditions and handoffs. Validate any legacy config's exact keys/types: `version: 1`,
`mode: local | hybrid | tracked`, `trackedRoot` string and `commitOnCheckpoint` boolean when supplied;
reject unknown keys/version/mode and unsafe paths without rewriting the legacy input.

Legacy modes are historical preferences, not the new default. Copy verified run-owned facts to one
safe local canonical home atomically, reread and compare essential fields before retiring the old
canonical pointer. Keep legacy originals until verification succeeds, then label/archive them as
historical so resume finds one owner. Existing tracked knowledge/mirrors remain historical and are
not automatically updated or removed; continue sharing only under an explicit current request.
Do not infer authority from legacy config or migrate other projects. Multiple possible owners,
missing/mismatched state, unsafe paths or failed readback block migration without destroying originals.

## No-delta rule

No action or no new decision-relevant evidence means `NO-ACTION | NO-DELTA`, not a checkpoint,
knowledge commit, journal heartbeat or HTML regeneration. New negative evidence is a material delta.
Resume reads state/current findings first and history only by relevant IDs, never the full journal
every invocation. A new no-candidate regeneration can update its proof in state without a checkpoint.
