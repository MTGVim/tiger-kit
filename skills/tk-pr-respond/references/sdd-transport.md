# SDD Artifact Transport

Read only when exact content cannot be transported directly and a child needs file-backed material.


Prefer direct host payloads and child return values for Unit summaries, reports, and
exact diffs. Do not materialize an artifact merely to pass information that the active
host can transport faithfully.

Use a flat `.tigerkit/sdd-tmp/` only when a child requires a file path, an exact bundle
cannot be transported reliably through the host surface, or bounded context size makes
file transport necessary. Before the first write, read [artifact paths](artifact-paths.md) and prove with `git check-ignore -q -- .tigerkit/` that
Git's effective ignore rules cover `.tigerkit/` and verify that `git ls-files -- .tigerkit/`
returns no tracked paths. Per-directory `.gitignore`, `.git/info/exclude`, and configured
user-level exclude sources are all valid. Apply the owning SKILL.md Artifact Paths setup
when ignore coverage is missing, then recheck. If required file transport remains
unignored, unwritable, or invisible to the child, use no operating-system temporary
fallback; return `Blocked | Unverifiable` before dispatch.

Do not create per-run or per-plan hierarchies. Use unique filenames containing the
Seed identifier, `Unit`, and scope. Clean up only run-owned files and never delete
unrelated files. Do not put secrets in artifacts.

