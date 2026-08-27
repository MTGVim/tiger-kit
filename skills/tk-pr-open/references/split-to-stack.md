# Retrospective stack split

Read this only when `tk-pr-open` has already-implemented, verified work on one branch and a reviewability preflight selects or seriously considers `stacked` publication.

## Upstream boundary

The primary upstream is GitHub's official `github/gh-stack` skill and CLI contract.

Keep:

- linear bottom-to-top dependency layers;
- one concern per layer and one coherent story per stack;
- non-interactive `gh stack init <branch>...`, `gh stack submit --auto`, and `gh stack view --json` usage;
- `submit --auto --open` for ready PRs and `submit --auto` for draft PRs;
- exact command help as the runtime source of truth.

Adapt:

- upstream correctly recommends creating stacks before implementation;
- TigerKit supports a narrow retrospective path because `tk-pr-open` receives work that is already implemented and verified before publication;
- this path reconstructs new publication branches beside the preserved source branch instead of rewriting that source branch.

Omit:

- interactive `gh stack modify` or other TUI-only restructuring;
- automatic extension installation;
- ad-hoc ordinary PR chaining that pretends to be a GitHub Stack when official stacked PRs are unavailable.

## Eligibility

Use retrospective stacking only when all of these hold.

- The source worktree is clean and the exact source branch, `HEAD`, tree, base, and commit range are proven.
- No same-head PR already exists. Existing reviewed/published PRs are not silently migrated into a stack.
- The change contains at least two independently reviewable concerns that belong to one feature/project and can form a linear dependency chain.
- Each proposed layer can be described in one sentence and is expected to remain buildable/testable enough for its repository requirements.
- Branch names are collision-free locally and on the publication remote.

Do not stack solely because raw LOC is high. Generated files, lockfiles, snapshots, vendored artifacts, and mechanical churn follow their owning concern but do not create a layer by themselves.

If concerns are unrelated, stop instead of forcing them into one stack. If the dependency graph is not linear, use fewer layers or keep a single PR. If the same file contains inseparable changes for several concerns, assign it to one owning layer or coarsen the split; do not invent fragile hunk surgery merely to reach a target PR size.

## Tool provenance

Before approval, inspect `gh extension list` without executing the extension itself.

Eligible tooling is an unambiguous installed extension whose repository is exactly `github/gh-stack`. Treat missing, duplicated, ambiguous, or differently sourced `gh stack` installations as unavailable.

Do not install or replace an extension automatically. If the official extension is absent, keep the publication plan `Pending` and offer the user the official installation path or a single PR instead.

After approval and before mutation, use `gh stack <command> --help` as the fresh authority for flags. Avoid bare interactive forms. When several remotes exist, require `remote.pushDefault` or pass the exact approved `--remote <name>` wherever the command supports it.

## Preserve the source snapshot

The source branch is the recovery artifact. Never reset, rebase, rename, force-push, or delete it as part of retrospective splitting.

Record:

```text
SOURCE_BRANCH=<current branch>
ORIGINAL_HEAD=<exact approved HEAD>
ORIGINAL_TREE=<git rev-parse "$ORIGINAL_HEAD^{tree}">
BASE_REF=<approved base>
BASE_SHA=<fresh merge/base anchor used by the plan>
```

Reverify these values immediately before reconstruction. Any source `HEAD` or base drift invalidates the approval.

## Design the layers

Analyze the full `base...ORIGINAL_HEAD` diff and commit history for semantic ownership. Prefer boundaries such as:

```text
foundation/types/schema
→ domain/API/core implementation
→ UI/integration
→ end-to-end or cross-layer acceptance
```

These names are illustrative, not defaults. Repository branch/title conventions take precedence.

Prefer intact existing commits only when they already map cleanly to the approved layers in dependency order. Otherwise reconstruct from the approved source snapshot by path ownership. Do not preserve incidental commit boundaries at the cost of reviewability.

For every layer, record before approval:

- exact branch name and parent;
- one-sentence review concern;
- exact owned paths or intact source commits;
- exact PR title/body;
- template and evidence ownership;
- smallest relevant verification that proves the layer is not intentionally broken.

A file must have one deterministic state at each layer. If path-level reconstruction cannot express the intended intermediate state without authoring new product code, merge concerns until it can.

## Reconstruct beside the source branch

Only after exact approval, create new stack branches without mutating the source branch.

For path-owned layers, the safe shape is:

```text
approved base
  └─ <topic>/<layer-1>
       └─ <topic>/<layer-2>
            └─ <topic>/<layer-3>

preserved separately:
SOURCE_BRANCH -> ORIGINAL_HEAD
```

Create the first branch from the approved base, then each later branch from the preceding layer. Restore only the approved source paths or reuse only the approved intact commits. Before every reconstruction commit, inspect staged paths and stop on anything outside that layer.

A path-based restoration may use the source commit as the content authority, for example:

```bash
git restore --source "$ORIGINAL_HEAD" --staged --worktree -- <approved-paths...>
git diff --cached --name-status
git commit -m "<approved layer commit subject>"
```

The exact command may vary for repository state, renames, deletions, or intact-commit reuse. The invariant does not: reconstruction selects already-approved source content; it does not edit product content.

Do not use `git add -A` to compensate for an unclear layer. Do not rewrite the source branch to make the stack easier.

## Verify every layer

After each layer commit:

1. verify the branch parent and staged/committed path ownership;
2. run the smallest relevant repository check from the verified work/Seed/current repository contract that establishes the layer is not intentionally broken;
3. if the layer cannot stand on its own, merge it with an adjacent concern rather than publishing a knowingly broken intermediate PR.

Before any remote write, prove the lossless final invariant:

```bash
STACK_TIP=<top reconstructed branch>
test "$(git rev-parse "$STACK_TIP^{tree}")" = "$ORIGINAL_TREE"
git diff --exit-code "$ORIGINAL_HEAD" "$STACK_TIP" --
```

Both checks must pass. Tree equality is the primary invariant; the empty diff is a readable confirmation. If they fail, stop as `Blocked` and leave the source branch untouched.

## Adopt and submit with `gh-stack`

After local verification, adopt the already-created branch chain with the official extension. Existing branches are passed bottom to top.

```bash
git config rerere.enabled true
gh stack init <layer-1> <layer-2> <layer-3> [--base <non-default-base>]
```

Use the exact current `--help` syntax rather than copying optional flags blindly.

Submit only after `gh stack view --json` proves the expected local chain.

```text
ready -> gh stack submit --auto --open
 draft -> gh stack submit --auto
```

`submit` is not atomic. If it partially pushes branches or creates PRs before failing, do not delete, close, or silently retry through another publication route. Reread the remote stack/PR state and report the exact partial result.

If stacked PRs are unavailable for the repository, do not silently fall back to ordinary chained PRs. Preserve any actual remote state, report the blocker, and require a new user choice.

## Restore exact PR metadata

`gh stack submit --auto` may derive PR titles/bodies from branch or commit metadata. After submit, use `gh stack view --json` to map each approved layer to its actual PR, then edit only those PRs to the exact approved title/body and state.

Re-read every PR and verify:

- bottom-to-top base/head relation;
- exact title/body and template compliance;
- requested `draft | ready` state;
- evidence ownership/state;
- head SHA for the reconstructed layer.

Do not merge the stack. Do not delete or force-push the preserved source branch.

## Failure result

A failure after local reconstruction but before remote publication leaves only new local publication branches; the original source branch remains unchanged.

A failure after `submit` may leave remote branches/PRs because `submit` is non-atomic. Report those objects exactly and return `Blocked` or `Fail` as appropriate. Never claim rollback that was not verified.
