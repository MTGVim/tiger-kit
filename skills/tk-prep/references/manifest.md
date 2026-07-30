# Sealed preparation manifest

`.tigerkit/prep.md` begins at byte zero with one fenced JSON object using
schema `tigerkit.prep/v1`. The Markdown body follows the fence and contains
references only.

## Machine header

The top-level object has exactly these fields:

- `schema_version`: exact `tigerkit.prep/v1`
- `prep_id`: `prep-` plus sixteen lowercase hexadecimal characters derived
  from and revalidated against the canonical identity
- `task`: exact `id` and non-empty unique `anchors`
- `repository`: exact absolute `root`, absolute `worktree`, `branch`, and
  40-hex `base_head`
- `digests`: exact SHA-256 values for `source`, `dirty_inventory`,
  `instructions`, `spec`, `tickets`, and `verification_profile`
- `ticket_mode`: `tickets | no-ticket`
- `status`: `ready | active | completed | invalid | failed`
- `claim`: exact nullable `actor` and `id`
- `timestamps`: exact `created_at`, nullable `claimed_at`, and nullable
  `finished_at`, all UTC RFC3339 when present

Unknown, missing, duplicated, mistyped, malformed, or unsupported fields are
invalid. Repository and worktree paths are absolute, and worktree is inside
the repository root. Timestamps must be real, ordered UTC instants. `ready`
has no claim or finish data. `active` requires claim identity and `claimed_at`
but no `finished_at`. `completed` and `failed` require a claim; `invalid` may
come from Ready without one or Active with one. Every terminal state requires
`finished_at`.

The no-ticket digest is SHA-256 over the exact canonical bytes
`{"mode":"no-ticket"}`. Other JSON inventories use sorted keys and compact
separators, and unordered inventory arrays are sorted before hashing. Spec and
ticket digests use their exact file bytes.

## Markdown body

The body starts with `# TigerKit preparation` and references:

- task and source;
- `.tigerkit/spec.md`;
- `.tigerkit/tickets.md` or the no-ticket single slice;
- `digests.verification_profile`;
- the prior-art disposition owner or `none`.

Do not copy source, spec, ticket, verification, or prior-art prose into this
body.

## Writer

Run `scripts/prep_manifest.py create` from this skill with the complete
arguments shown by `--help`. The output must resolve to
`<worktree>/.tigerkit/prep.md`. The writer:

1. validates every input and Ready/Pass gate before touching the destination;
2. writes and fsyncs a mode-0600 temporary sibling;
3. atomically replaces the destination;
4. fsyncs the containing directory;
5. strictly rereads the installed document.

Use `scripts/prep_manifest.py validate <worktree>/.tigerkit/prep.md` after the
write. A non-zero result is terminal preparation failure and cannot authorize
drive.
