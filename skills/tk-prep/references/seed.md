# Ready Seed Contract

Read this reference only when durable context is `seed`, execution is `sdd`, or the approved outcome is `handoff`.

Write only `.tigerkit/seed.md`, only after approval, atomically, and reread it. Every new Seed starts with
`<!-- tigerkit:seed -->`, names a deterministic current-task identity, and is `Status: Ready`. It must be self-contained
for a fresh lower-capability executor and preserve:

- source, goal/background, exact checkout or PR head, and current evidence/entry points;
- scope, exclusions, do-not-change constraints, and approved material decisions with reasons;
- implementation direction and only material Reuse/Simplicity/Tests/Security/Experience gaps, exceptions, or decisions;
- AC with per-AC verification, browser plan, exceptions, traps, and exact UI literals;
- execution recommendation and, for SDD, the private protocol's exact `## Execution` grammar.

Do not add readiness rows merely to state that an axis is ready or irrelevant. Never store transcript, provider/model ID,
reasoning intensity, secrets, worker/wave routing, receipts, or progress in a Seed. Before approval, preserve an existing
Ready Seed byte-for-byte and create no `Status: Pending` file. Replace only a proven TigerKit-owned Seed. For approved
direct/no-Seed, remove only a marked stale TigerKit Seed after proving it is not current. Preserve an unmarked, legacy, or
identity-ambiguous Seed and return `Blocked` before execution.
