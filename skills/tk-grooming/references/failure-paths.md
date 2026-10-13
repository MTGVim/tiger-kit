# Grooming failure paths

Read only when a grooming checkpoint fails.

- Missing/unreadable path: Mark only that area `Unverifiable`, keep other areas
  read-only, and report the required access.
- Unknown ownership: Do not create edit proposals or changes; return
  `Partial/Blocked` with one ownership question.
- Vendor ownership confirmed after classification: Convert every edit action to
  `keep (vendor)`, preserve the artifact, and report the evidence.
- Conflicting scope/apply authority: Make no changes and return `Partial/Blocked`
  with the one required decision.
- Referenced deletion/move target: Make no changes, change the proposal to
  `keep | tighten`, and cite the reference.
- Unproven no-op/cache/pointer claim: Keep the existing behavior and report the exact
  missing behavioral evidence; do not make a speculative tightening edit.
- Target drift after checkpoint: Make no changes, return `Partial/Blocked` with
  current evidence, and require a new proposal.
- Broken symlink, unknown shared target, or failed tracking probe: Mark the affected
  tier `Unverifiable`; do not equate a Git error with an untracked file or approve
  later tiers using stale evidence.
- Missing durable T1/T2 backup or failed byte-equality check: Make no changes to that
  target. Report the backup/access deficit; session-temp or auto-loaded storage is
  not a recovery backup. Keep other approved independent targets within their scope.
- Verification failure after apply: Never claim `Complete`. Restore/reverify only
  when this run's delta is exactly reversible, then return `Fail` with evidence.
  If preservation or restoration is uncertain, halt the mutation as `Unverifiable`
  and report the checks, paths, and observed state.
  Recheck the current real target and this run's delta before restoring; preserve
  concurrent edits. Retain the durable backup and report its path and restoration
  result. Do not continue dependent tiers after failed verification.
