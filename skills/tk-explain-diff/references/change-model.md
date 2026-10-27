# Source-bound change model v1

Build `change.json` and `sources.json` in authorized run scratch after the existing snapshot
and inventory checks. Invoke `python3 <package>/scripts/change_model.py --model <change.json>
--sources <sources.json>`. Resolve diagnostics by field path; do not coerce or silently drop
invalid data. The validator reads only these JSON files; it does not run inputs, access Git,
network, settings or browsers. A successful result establishes structural consistency and
agreement with the supplied bundle only, not true Git identity, complete inventory, correct
interpretation, runtime behavior or artifact quality. Keep missing source and inventory limits
visible and obtain the existing independent content review.

All objects have exactly the fields below; optional `graph` may be omitted. Required nullable
fields are explicitly `null`. IDs are collection-local ASCII slugs. Arrays have no fixed quota.
`schema_version` is integer 1; `inventory_complete` is boolean. Nonempty strings are required
unless a field is explicitly nullable.

- Root: `schema_version`, `title`, `summary`, `snapshot`, `inventory_complete`,
  `inventory_limit` (string/null), `units`, `evidence`, `groups`, optional `graph`.
- Snapshot: `repository`, `comparison` (`merge-base|range|workspace|synthetic`), `from`, `to`,
  `versions` mapping version keys to `{kind,id}`. Endpoints must be distinct existing keys.
  Kinds are `commit|index|worktree|untracked|synthetic`. Commit IDs are full 40/64 hex;
  workspace state IDs are SHA256 fingerprints. Label synthetic examples as synthetic.
- Evidence: `id`, `kind` (`text|metadata`), `version`, repository-relative `path`, `start`,
  `end`, `availability` (`available|unavailable`), `sha256`, `reason`. Available entries bind
  to a matching supplied source via UTF-8 SHA256 and 1-based inclusive `splitlines()` range.
  Empty sources use null bounds; unavailable entries require null digest and a reason.
- Unit: `id`, `kind` (`text|rename|binary|mode|submodule`), `before`, `after` evidence-ID
  arrays, `disposition` (`primary|secondary|unavailable`) and nullable `reason`. Evidence on
  each side belongs to its endpoint. Non-primary dispositions require a reason.
- Claim: `text`, `basis` (`source|inference|unverified`), `evidence` IDs and nullable
  `limitation`. Source needs available evidence; inference and unverified need a limitation.
  Before/after source claims reference the respective endpoint.
- Group: `id`, `title`, `summary`, `unit_ids`, `evidence_ids`, `depends_on`, `before`, `after`,
  `invariants` (claims), `checkpoints` and `limitations` (strings). Every primary unit is
  covered; dependencies precede their dependent group. Evidence shown by a group may also come
  from its claims and units; no redundant evidence identity list is needed.
- Sources: `{schema_version:1,files:[{kind,version,path,text}]}`; each tuple is unique. Paths
  are identifiers, never opened as host paths. Preserve source text and whitespace exactly.
- Optional graph: `{nodes,edges,flows}`. Nodes contain `id,label,delta,versions,evidence_ids`.
  Edges contain `id,from,to,label,delta,versions,basis,evidence_ids,limitation`. Delta is
  `added|modified|removed|unchanged`, presence follows the endpoints, and endpoints exist in
  every edge version. Inferred or unverified edges need limitations; source edges need available
  evidence. Flows contain `id,title,group_id,version,steps`; each step has unique `id,edge_id,
  explanation`. The referenced edge exists in the flow version. This graph records sourced
  relations, not a claim that a runtime flow was observed.

The synthetic `assets/change-example.json` and paired `.sources.json` illustrate a two-file
TTL group, a separate boundary change in the same file, and unchanged context. They are not
actual PR evidence. The user-facing artifact must preserve the real snapshot and source labels.
