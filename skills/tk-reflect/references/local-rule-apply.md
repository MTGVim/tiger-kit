# Local rule apply

Use this procedure for the only direct rule mutation owned by `tk-reflect`.
The candidate must already be `high` confidence with at least two independent
verified Evidence IDs, no counterexample, no earlier prevention owner, and one
exact existing user-managed target.

## Target-state preflight

Classify scope before deciding eligibility.

| Scope and observed state | Local apply |
| --- | --- |
| Existing user-level host-native regular file outside the current repository | eligible |
| Existing repository regular file, untracked and ignored | eligible |
| Existing repository regular file, untracked and visible | eligible |
| Tracked repository file | pending; never direct-apply |
| New, missing, vendor/generated, unknown ownership, symlinked, external, ambiguous, or drifted | blocked from mutation |
| Git state command failure or conflicting results | `Unverifiable` |

For a repository target, run deterministic Git checks from the exact worktree
root before classifying it:

```bash
git ls-files --error-unmatch -- <target>
git check-ignore -v --no-index -- <target>
git status --porcelain=v1 --ignored --untracked-files=all -- <target>
```

Interpret exit codes exactly:

- `git ls-files`: `0` means tracked and ineligible; `1` means untracked;
  any other exit is `Unverifiable`.
- `git check-ignore`: `0` means `untracked-ignored`; `1` means
  `untracked-visible`; any other exit is `Unverifiable`.
- `git status` must corroborate the result with `!!` or `??`. Missing or
  conflicting evidence is `Unverifiable`.

Record `git_state` and the verbose ignore source when present. Ignored state is
additional evidence, not an eligibility requirement.

For a user-level target, require an exact absolute current-host-native path
inside the user's home, outside the current repository, with verified
user-managed ownership. Never reclassify a repository-local path as user scope.

## Mutation

Use `scripts/safe_rule_apply.py` with:

- exact repository root;
- `--scope repo` plus one normalized repository-relative target, or
  `--scope user` plus one exact absolute target;
- the verified baseline SHA-256;
- `--user-managed` only after ownership evidence passes;
- a regular candidate file inside `.tigerkit/`;
- at least one shell-free JSON-array validation command.

The executor rechecks containment, regular-file and symlink state, Git state for
repository targets, baseline hash, and user-scope separation. It saves a
mode-0600 before-image and metadata under `.tigerkit/reflect-backup/`, atomically
replaces the target, reruns state checks and validators, and restores the exact
before-image on failure.

Do not bypass a rejection. The ownership flag is an evidence assertion from the
caller; the executor cannot infer ownership. Successful mutation creates no Git
commit. Record `applied locally`, scope, target, target state, hashes, validator
evidence, backup path, and exact restore guidance in `.tigerkit/reflect.md`.
