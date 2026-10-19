# Documentation audit

Read for the `docs` focus or a `next` documentation-baseline opportunity. Run the full
comparison only for `docs`, within the selected repository/package/branch scope;
other audits retain their existing coverage. This reference grants no write authority.
Propose instruction/rule-file text for the user to apply; never create, modify or move
`AGENTS.md`, `CLAUDE.md` or rule files.

## Compare behavior claims

- Inventory tracked prose that asserts current behavior: guides, READMEs, instruction
  files, skill/prompt bodies, test/eval expectations and fixtures, exported API
  docstrings, and user-facing help or generated templates. Dated historical reports
  are not current contracts. Untracked drafts are evidence, not owned documentation.
- First compare every in-scope skill/prompt body with its own frontmatter, tests and
  evals, including assertions and fixtures. Then compare guides with the code/config/CLI
  they describe and instruction files with actual layout and commands. Include internal
  contradictions, examples, referenced contracts and relevant decision records;
  prioritize counterparts changed since the document. List uncompared documents and
  unavailable counterparts instead of claiming complete coverage. Inline implementation
  comments are related surfaces only when they repeat a confirmed wrong claim.
- Record checked-out and available upstream refs. If the local branch is behind,
  disclose it and check claims against the upstream ref with read-only `git show`;
  label findings with the ref where they hold. Do not checkout, pull or repair the
  audited tree. If fresh upstream evidence is unavailable, label that limitation.
  Pin each upstream finding to its immutable comparison SHA while retaining the local
  audited HEAD as session identity. Reproduce evidence at that SHA and recheck the ref
  before saving; ref movement blocks the ledger until re-audited. Carry both commits
  into handoff and revalidate against the executor's actual target before any fix.
- Require an exact `file:line` and a contradiction with current implementation,
  configuration or another owned statement, plus concrete impact. An omission needs
  evidence that the list claims completeness; a table or numbered example alone does
  not establish that. Exclude illustrative lists and historical claims.

## Prevent recurrence

For confirmed stale claims, attach the smallest justified sync mechanism to the fix
sketch, or explain why recurrence does not warrant one. Describe shared mechanisms once
and cross-reference them; do not turn every finding into an infrastructure project.

- **Change-to-document mapping** (default): seed rows from a confirmed contradiction
  or observed source/document co-changes: changed source → owned statement to recheck.
  Keep unverified candidate rows separate. Use an existing docs map or propose a row in
  an instruction file. Prefer a pointer when the same fact is duplicated across files.
- **Review criterion**: add only when a repository-wide checklist or automated review
  actually runs, evidenced by a workflow or recent reviews. Configuration alone is
  `unverified`; a single skill's completion step is not repository-wide enforcement.
- **Path check**: use for moved/renamed/deleted paths, never as semantic-drift coverage.
  Reuse an existing checker. Otherwise outline, without implementing, a check of tracked
  document links/path literals with root-relative and document-relative resolution,
  fenced-code/example exclusions and an explicit ignore escape. Require an actual
  tracked-path candidate before flagging it. Suggest all-PR CI when CI already exists,
  otherwise the existing verification command; never invent CI for a no-CI repository.

A general prose reminder is not a verified sync mechanism. Keep audit findings and
mechanism proposals separate from implementation or publication authority.

## `next` documentation baseline

Use current paths, missing parts, change history and observed co-changes as why-now
evidence. Propose only missing, justified parts; missing infrastructure alone creates no
finding. For a dormant repository, lower priority and limit the immediate proposal to
instruction-file setup. Determine activity from available upstream history, or disclose
that only local history is available.

- An automatically loaded instruction entry with setup/verification commands from
  existing scripts, and pointers to decisions, pitfalls and affected documents. Run
  proposed commands only when read-only and safe; report failures and unrun commands.
  Check the current tool's actual loading/import rules before proposing migration;
  keep tool-specific entries when needed. Put bootstrap/import guidance somewhere
  already read, such as README setup, not solely inside a file that is not loaded.
- Reuse existing decision/pitfall locations; propose minimal locations only when needed
  for real records, check `git check-ignore`, and avoid backfilled history or empty trees.
- Seed a mapping with evidence-qualified rows; do not invent documents for undocumented
  code. Add path checks only where path drift warrants them under the rules above.
- Preserve existing Diátaxis organization. Otherwise suggest a map labeling existing
  tutorial/how-to/reference/explanation guides only when navigation difficulty warrants
  it; no arbitrary document-count threshold or empty taxonomy directories.
