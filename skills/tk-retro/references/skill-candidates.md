# Skill candidate criteria

Read only when a retrospective recommends creating, merging or semantically
improving an Agent Skill. This is a **recommendation check**, not a writer/apply gate.

- Check whether an existing skill, repo-native tool/test, user rule, or normal model
  ability already covers the outcome. Prefer the smallest owner and a no-op when fit
  is sufficient.
- A candidate needs one adequate evidence route: a verified concrete gap with mature
  upstream, a well-evidenced recurring failure, or explicit reusable workflow intent
  supported by source material. Never require an arbitrary incident count.
- Define a distinctive outcome, positive and negative triggers, inputs, owner,
  minimal procedure, must-preserve guardrails and observable success/boundary cases.
  Contrast with the existing/no-skill baseline. Shorter text alone is not success.
- Promote mechanical violations to existing lint/test/CI/schema where practical;
  judgement-dependent review criteria may merit a reviewer-facing instruction.
- Treat description and reference links as **conditional context pointers**: a
  pointer should say which branch needs the content. Prefer current environment
  state over copied package/version/config facts.
- A candidate that changes verified correctness, safety, privacy, scope or
  host compatibility fails even when its token count is lower.
- Label source decisions keep/adapt/omit when distilling public upstream examples.
  Keep exact public provenance and summarize decisions without copying their
  runtime, provider configuration or evaluation machinery.
- Present target, reason, suggested text/contract, affected references, evaluation
  scenarios, exclusions and owner. Do not write the canonical file or ask for
  application permission within tk-retro.
