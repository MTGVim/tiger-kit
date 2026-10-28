# Evidence binding

For change mode, resolve the repository and requested target before drafting. Pin full
base/head SHAs and comparison semantics: PR/branch normally uses merge base; an explicit
range uses its endpoints. A worktree uses HEAD plus separate staged/unstaged diffs and
hashes of relevant untracked files. Never replace an inaccessible PR with the checkout.
Read surrounding callers, models, tests and configuration at both snapshots. Cite deleted
code at base lines and new code at head lines. For uncommitted files use the recorded content
hash and snapshot line numbers, never pretend archify `@code` can read them from HEAD.
Trace behavior, preserved invariants and material boundary cases, not just changed lines.
Read referenced issue/RFC/ADR intent separately from code-verified behavior. A broken or
unverified invariant remains a disclosed explanation limit; `tk-review` owns defect verdicts.
Group meaningful behavior and de-emphasize verified mechanical changes without hiding
security, schema, compatibility, migration or generated-API changes.

For concept mode, pin repository examples to a commit. Verify current, specialist or
uncertain claims in primary sources. Record web URLs, access date, relevant version and
supporting passage; search snippets are discovery, not inspected evidence. Check a community
term's definition/glossary and primary use before discussing origin. Say origin is unverified
only after naming what was checked; absence in one search does not prove no origin exists.
Preserve uncertainty, conflicts, essential conditions and supplied question/figure inputs.
Label measured, simulated and illustrative values; do not imply benchmark or runtime evidence.

Use this compact evidence format; omit inapplicable fields:

```text
mode / reader goal / run ID:
repository / base / head / comparison meaning:
worktree snapshot: staged, unstaged, untracked hashes
claim | version-qualified path:line or URL | access date | supporting passage | observed/inferred/example
preserved invariants / verification limits:
supplied finite set: used / partial / unavailable / omitted-with-reason
```

Recheck line ranges and moving refs before delivery. Either retain and disclose the pinned
snapshot or refresh the whole affected explanation; never mix versions. Give reviewers this
same file and actual sources. Keep private code out of web queries and public artifacts.
