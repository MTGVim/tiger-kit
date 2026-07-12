# TigerKit 18

TigerKit is a collection of small engineering Agent Skills for Claude Code, Codex, and Hermes Agent. Version 18.0.0 uses the Agent Skills format and no longer ships a Claude Code plugin runtime.

## Install

Install every skill globally for all initially supported hosts:

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

Install selected skills:

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill tk-implement \
  --skill tk-browser-verify
```

Install the immutable 18.0.0 snapshot:

```bash
npx skills add "MTGVim/tiger-kit#v18.0.0" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code and Hermes Agent expose installed skills as slash commands such as `/tk-implement`. Codex uses `$tk-implement` or its skill picker.

## Skill catalog

### Shape

| Skill | Purpose |
| --- | --- |
| `tk-grill-me` | Pressure-test consequential decisions one question at a time. |
| `tk-grill-with-docs` | Grill decisions while recording settled terms and qualifying ADRs. |
| `tk-grilling` | Model discipline for one-question-at-a-time decision convergence. |
| `tk-domain-modeling` | Sharpen domain language and concept boundaries. |
| `tk-prototype` | Build a throwaway UI or logic proof. |
| `tk-codebase-design` | Propose the smallest evidence-backed structural improvement. |

### Document

| Skill | Purpose |
| --- | --- |
| `tk-to-spec` | Synthesize evidence and decisions into a spec. |
| `tk-to-tickets` | Create independently verifiable vertical tickets. |

### Build

| Skill | Purpose |
| --- | --- |
| `tk-implement` | Implement and verify a requested change. |
| `tk-browser-verify` | Verify real browser UI, behavior, environments, and design fidelity. |

### Learn

| Skill | Purpose |
| --- | --- |
| `tk-reflect` | Propose reusable repo/user rule or skill candidates. |
| `tk-learn` | Turn evidence into a reusable repo or user skill. |
| `tk-grooming` | Audit and optionally repair existing rules and skills. |

### Continue

| Skill | Purpose |
| --- | --- |
| `tk-handoff` | Write or resume verified work state. |

### Disciplines

| Skill | Purpose |
| --- | --- |
| `tk-tdd` | Apply red-green-refactor at a valuable behavior seam. |
| `tk-diagnosing-bugs` | Reproduce, minimize, diagnose, fix, and regress difficult bugs. |
| `tk-code-review` | Review a fixed diff without editing it. |
| `tk-merge-conflict` | Resolve active conflicts while preserving both intents. |

## How skills compose

TigerKit is not a mandatory pipeline. A small change can be only:

```text
tk-implement
```

A complex design may use:

```text
tk-grill-me
→ optionally tk-to-spec
→ optionally tk-to-tickets
→ tk-implement
```

User-invoked skills suggest follow-ups but do not automatically invoke one another. Model-invoked disciplines may guide relevant work. Delegation and review stay bounded.

## `.tigerkit/`

`.tigerkit/` is optional worktree-local scratch for current specs, tickets, handoffs, prototypes, skill drafts, and browser evidence. It is gitignored by this repository, is not durable project documentation, has no archive/current-pointer database, and is never stored in a global TigerKit state directory. TigerKit does not modify another repository's `.gitignore`; if `.tigerkit/` is not ignored, the skill reports that fact. TigerKit does not create `docs/tigerkit/`.

## Versioning

`main` is the rolling latest source. Git tags are stable immutable snapshots. The repository follows SemVer as one product: skill rename/removal, invocation-kind changes, incompatible `.tigerkit/` changes, and distribution changes are major releases.

## Attribution

The following adapted skills retain names and behavioral influence from [`mattpocock/skills`](https://github.com/mattpocock/skills): `grilling`, `domain-modeling`, `grill-me`, `grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `diagnosing-bugs`, `code-review`, and `implement`. TigerKit adds the `tk-` prefix and records `relationship: adapted` in each skill. See `NOTICE.md` for license attribution.

Migrating from TigerKit 16.x? Read `MIGRATION.md`.
