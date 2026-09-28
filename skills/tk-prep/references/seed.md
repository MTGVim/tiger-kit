# Ready Seed Contract

Read this reference only when durable context is `seed`, execution is `sdd`, or the approved outcome is `handoff`.

Write only `.tigerkit/seed.md`, only after approval, atomically, and reread it. Every new Seed starts with
`<!-- tigerkit:seed -->`, names a deterministic current-task identity, and is `Status: Ready`. It must be self-contained
for a fresh lower-capability executor and preserve:

- source, goal/background, exact checkout or PR head, and current evidence/entry points;
- scope, exclusions, do-not-change constraints, and approved material decisions with reasons;
- implementation direction and only material Reuse/Simplicity/Tests/Security/Experience gaps, exceptions, or decisions;
- AC with per-AC verification, browser plan, exceptions, traps, and exact UI literals;
- a semantic Review Plan: change intent, original incident or expected scenario, expected changed outcome,
  `must-not-change` behavior or visual regions, change-owned risk edges, required evidence, and known uncertainty;
- execution recommendation and, for SDD, the private protocol's exact `## Execution` grammar.

Do not add readiness rows merely to state that an axis is ready or irrelevant. Never store reviewer count, transcript,
provider/model ID, reasoning intensity, secrets, worker/wave routing, receipts, or progress in a Seed. Before approval, preserve an existing
Ready Seed byte-for-byte and create no `Status: Pending` file. Replace only a proven TigerKit-owned Seed.
Before consuming an existing Seed, establish its current-task identity; before replacing it, also establish ownership.
If that required evidence is missing or ambiguous, preserve the file and return `Blocked` for the Seed-dependent path.
The owning SKILL.md handles direct/no-Seed without loading this reference or consuming an existing Seed.

## Decision density

Persist decisions the executor cannot safely reconstruct: exact interfaces/signatures, schemas,
spec-fixed values, invariants, compatibility/migration constraints, test names and assertions,
observable acceptance, verification commands and passing results, review risks and Unit dependencies.
Point to current paths and symbols rather than copying ordinary function/component bodies, glue,
mechanical mappings or the same implementation sequence into multiple Units. Self-contained means
unambiguous constraints, not prewritten implementation. If an approved algorithm or ordering is
itself material to correctness, security or compatibility, retain its minimum pseudocode,
transitions or invariants without expanding unrelated boilerplate.

Before finalizing a Ready Seed or its Execution section, compare it with the source issue/spec:
unusual growth, dominant code blocks, repeated decisions or fresh-readable source details call for
compression into interfaces, invariants, assertions and verification. Preserve exact identity,
scope, acceptance and recovery obligations; impose no fixed line/token budget or ratio and add no
reviewer, skeleton or preview artifact. This check does not create a Seed for direct/no-Seed work.
At execution, reread current repository evidence instead of following stale copied implementation
prose. Implementation-detail drift alone needs no reapproval; material approved-contract drift
still follows the existing re-prep/reapproval boundary.
