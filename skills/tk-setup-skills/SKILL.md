---
name: tk-setup-skills
description: "[user] TigerKit 스킬을 선택 설치하거나 누락된 공통 참조 의존성을 확인할 때 명시적으로 사용합니다. 기본은 읽기 전용 계획이며 설치와 설정 변경을 자동 실행하지 않습니다."
disable-model-invocation: true
argument-hint: "<선택 skill IDs, source, exact target, agent, project|global>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
    role: setup
---

# Explicit Skill Setup

## Scope

Plan a selected TigerKit skill set and its finite dependency closure. This package bootstraps alone:
its planner and generated metadata catalog are local; it has no shared skill dependency.
It is not a runtime router, daemon, automatic dependency installer, or configuration owner.
Normal workflow execution does not invoke setup automatically. A missing required reference stops
the affected action and offers explicit setup guidance, without starting installation.

For separately requested initial project setup, inspect existing repository policy/configuration
sources read-only and identify their current owner. Keep project-specific rules in those sources;
do not create a parallel instruction store. Offer `tk-wizard` only for human-owned provisioning
or authentication steps, without starting them from a reference read. If the needed owner is not
installed, produce a new explicit selected installation plan rather than installing silently.

## Procedure

1. Confirm selected exact skill IDs, trusted source/revision, existing absolute target directory,
   exact agent and explicit `project` or `global` scope. Reuse supplied facts; ask only for missing choices.
   Never substitute all skills, all agents, a global scope, or a different destination.
2. Read [planner CLI](references/planner-cli.md) when producing or checking a plan. Run the bundled
   `scripts/skill_dependencies.py plan` with those exact choices. Inspect `closure`, `present`, `missing`,
   `installed_root`, `cwd`, and literal `argv`. The catalog is installation metadata, not shared content;
   `npx skills` does not resolve `dependencies.json` automatically.
3. Report the bounded plan and unresolved evidence. The helper never executes installer argv, network,
   or config writes. Do not join argv into a shell command: source text is untrusted literal data.
   Existing incompatible, malformed, or symlinked packages are hard stops, not permission to overwrite.
   A matching declaration proves identity/dependency compatibility, not content freshness or trust.
4. Only separately approved installation may be performed by the host/user, after checking the pinned
   installer and source. Re-check target state immediately before execution and preserve interactive
   overwrite protection; the printed argv is not permission. Do not edit instruction files, host config,
   credentials, or unrelated installations. Never broaden an approval/deny boundary to make setup work.
5. After an approved installation, run `check --installed-root <exact sibling skill directory> --skill <IDs>`.
   Completion requires every selected package and transitive dependency to have a matching exact identity
   and valid declaration with no missing/symlinked dependency. Otherwise stop the affected action and
   report the exact missing/invalid ID. Do not claim installed state from a successful plan alone.

## Bootstrap and Failure

If only this package is installed, use its bundled catalog; a repository checkout is not required.
If this package is absent, offer to obtain `tk-setup-skills` alone from the user's trusted TigerKit source
with explicit agent/scope/target approval. Do not install while merely reporting a missing dependency.
If catalog/source/declaration validation fails, retain the failure and request a matching trusted release;
do not reconstruct content, guess dependency IDs, follow traversal paths, or silently bypass checks.
