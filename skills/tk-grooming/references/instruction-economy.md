# Instruction economy audit

Read this only when the approved grooming scope includes existing skill or persistent-instruction load, description shortcuts, conditional references, environment caches, no-op instructions, or stale sediment.

- Treat a description or conditional reference link as a context pointer. A useful pointer names the material and the distinct branch that needs it; a workflow summary is not stronger.
- Treat package/config values, directory inventory, and host/tool capability as cache candidates only when a cheap fresh lookup is the source of truth. Owned contract literals are not stale merely because they are concrete.
- Keep a deliberate copy of external tool/plugin/host behavior when a fresh lookup on each invocation is impractical. Compare its declared baseline version with the same component's installed identity/version, not the latest remote release.
- A version mismatch is a `stale override` candidate: record both versions and evidence paths in Basis, reread the relevant installed rule without executing it, and report its actual difference (or no difference). Mismatch alone does not prove a behavioral conflict or authorize rewriting the copy. A matching version remains `keep` with no extra version-only finding/row.
- A missing baseline version is a finding with a `tighten` proposal to add verified provenance; never invent the version or mechanically relabel an unverified copy as current. If installation identity/version or the relevant rule cannot be checked, mark that comparison `Unverifiable` and preserve the copy.
- Call an instruction a behavioral no-op only when removing it preserves observable behavior against a no-skill or prior-skill baseline. Prose style, source presence, line count, token reduction, and trigger success do not prove that.
- Move branch-specific material only when a precise pointer still causes the relevant branch to read and apply it. Keep always-needed authority, safety, freshness, and cross-scope guards inline.
- Treat long-but-live instructions as `keep`; `sprawl` or `sediment` requires evidence that material is irrelevant, duplicated, stale, or on the wrong branch.
- Treat a skill as the current behavior owner only when package and installation evidence establish it. Compare exact applicability before classifying persistent context as `stale override`; recency, specificity, or load order alone is insufficient.

Before proposing `tighten`, compare prior and candidate behavior. Description changes need train/validation routing and body behavior; pointer, cache, or no-op changes need both the branch that requires the rule and one that does not. Preserve valid behavior and pressure-tested guards. If behavior would change, leave an exact recommendation for the authorized implementation owner instead of applying it here. Use `tk-retro` when causal session evidence needs investigation.
