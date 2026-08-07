# TigerKit Repository Guidance

## Product boundary

TigerKit is an Agent Skills repository, not a workflow runtime, plugin, or shared
state framework.

- Keep each `skills/tk-*` package self-contained.
- `SKILL.md` owns runtime behavior; package-local `references/`, `scripts/`,
  `agents/`, and `evals/` own conditional detail and executable evidence.
- Do not restore `.claude-plugin/`, `commands/`, global TigerKit state, host-specific
  copies of skill bodies, or GitHub Actions validation.
- Prefer deletion and progressive disclosure over duplicated ceremony.
- Canonical operational prose is English; user-facing prose follows the user's
  language while exact statuses, IDs, commands, paths, and literals remain stable.

## Skill existence discipline

A skill needs an independent invocation or narrow automatic trigger, a procedure
materially different from ordinary model behavior, objective completion criteria,
and an owned artifact, mutation, approval, or safety boundary.

Before adding or retaining a skill, verify:

1. a user or a documented parent has a real reason to invoke it;
2. positive and negative trigger cases distinguish it from adjacent behavior;
3. success and boundary eval paths exist;
4. catalog routing or another documented consumer references it;
5. removing it would reduce measured task quality.

Weak candidates should be inlined, merged, converted to a conditional reference,
made explicitly user-invoked, or deleted. `scripts/audit_catalog.py` derives this
evidence from canonical contracts. It may mark `tk-drive` for removal review only
when `scripts/run_drive_experiment.py` reports a measured `RemoveCandidate` result.

## Core boundaries

- `tk-drive` is the explicit product-change orchestrator. `tk-pr-sweep` is the
  narrow second explicit orchestrator for multi-PR maintenance only. Other phase
  owners never invoke sibling phase owners. Continuation is prompt-directed, not
  durable scheduling.
- `tk-ask-repo` is read-only investigation and never implements.
- `tk-drive` and `tk-pr-respond` controllers never author product changes;
  fresh workers produce one bounded candidate at a time.
- Required verifiers and R/AC gap closure precede one verified commit per unit;
  the top-level owner may perform only the final mechanical Git bookkeeping.
- `tk-drive` owns aggregate traceability, ancestry, cross-unit verification, and
  finalization.
- Browser tools for user-visible behavior run inside `tk-browser-verify`.
- Push, PR, merge, tag, release, and publish need separate explicit authority;
  explicit `tk-pr-sweep` supplies only its documented bounded PR-maintenance
  authority.
- Small work and ordinary follow-up feedback stay in the current conversation.

## Eval single source of truth

Only these files own executable eval behavior:

```text
skills/<skill>/evals/triggers.json
skills/<skill>/evals/evals.json
evals/catalog-routing.json
evals/release-critical.json
evals/drive-ab.json
```

Do not add generated `test-prompts.json`, root trigger/behavior mirror fixtures,
Darwin projections, or Python lists duplicating canonical case IDs. The validator
auto-discovers `skills/tk-*`; adding or deleting a justified skill must not require a
catalog count edit in Python.

When changing an eval:

- address a case by exact `id`;
- preserve or explicitly migrate existing case IDs;
- keep at least one mechanical assertion per behavior case;
- preserve safety, host coverage, terminal strictness, and nonterminal assertions
  unless a documented migration replaces them;
- keep release-critical references resolvable to canonical cases.

## Host quality

`scripts/adapters/tigerkit_host_adapter.py` is the default live adapter. It tries
Codex, Claude Code, and Hermes Agent in that order under isolated homes. A missing
or unusable runtime is quality `Advisory`, not deterministic success or failure.
Custom adapters may override the command but must return the same JSON protocol.

The adapter's selected-skill and phase events are eval-envelope evidence produced
by the host run. Do not present them as lower-level runtime telemetry when the host
does not expose such telemetry directly.

## State and documentation

Runtime scratch is repo/worktree-local `.tigerkit/`; never create global archives,
current pointers, or automatic migration. Branch decisions belong in spec, tickets,
commits, PRs, code, and tests. Create an ADR only on an explicit request for a
long-lived repository constraint.

## Required checks

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

For packaging changes, smoke-install all supported hosts in disposable homes. For
release quality, run the deterministic local `scripts/run_release_gate.py`; for
drive retention evidence, run `scripts/run_drive_experiment.py`. Keep all
validation local-only.
