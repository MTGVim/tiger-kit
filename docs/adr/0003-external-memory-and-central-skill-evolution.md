# ADR 0003: External memory and central skill evolution

- Status: Accepted
- Date: 2026-07-31
- Source: MTGVim/tiger-kit issue #224
- Release procedure: maintainer patch release `v21.0.9`
- Supersedes: ADR 0001 and ADR 0002

## Context

TigerKit's earlier drive protocol included a post-verification reflection tail
and mixed reusable-candidate, rule, and skill lifecycle concerns across several
skills. That made the final product verification head ambiguous and left
repository/user instruction lifecycle inside an Agent Skills distribution
that does not own persistent memory.

Browser verification also allowed some Guard paths to stop after interaction or
DOM evidence without a uniform, user-navigable image artifact.

## Decision

1. `tk-drive` ends after aggregate product verification and direct
   `tk-drive` finalization. It does not invoke a post-session reflection or
   persistent-memory writer.
2. `tk-learn` is the sole TigerKit writer for skill `create | improve | merge`.
   It retains its evidence, dedupe, eval, compatibility, and approval gates.
3. `tk-skill-diagnose` is read-only and emits one verified `learn-ready`
   handoff for a later explicit `tk-learn` run. It does not own a patch or
   invoke the writer.
4. `tk-grooming` audits repository/user skills only. Rule lifecycle and
   persistent-memory lifecycle are outside its scope.
5. `tk-browser-verify` requires every started Guard or Verdict run to leave at
   least one non-empty screenshot and actual image inspection. Its evidence
   result records an absolute `Evidence directory: /...` when resolvable;
   unresolved evidence is `Unverifiable` and says
   `Evidence directory: unavailable`.
6. The retired skill's historical eval contract may disappear only through an
   explicit `retired_skill_contracts` release-manifest declaration. Historical
   migration records remain provenance, not active routing.

## Consequences

- The canonical catalog contains 14 skills and has no active reflection route.
- Existing repository/user rules and memory remain external to TigerKit; this
  repository does not create, migrate, or synchronize them.
- The direct aggregate-to-finalization graph makes the product verification
  HEAD the final product evidence anchor.
- Browser users can open the absolute evidence directory directly when the
  runtime resolves it, and incomplete capture cannot be reported as Pass.
- Historical CHANGELOG and MIGRATION entries may mention superseded behavior;
  current README, contracts, and active skill bodies must use the new owners.

## Verification

The release gate, skill validators, full script test suite, catalog audit,
package listing smoke checks, and Darwin quality assessment are required before
the maintainer patch release is applied.
