# Autoresearch Persistence

Read this reference before establishing a research home, initializing persistence, changing persistence
settings, recording a terminal outcome, or committing research-owned knowledge.

## Minimal configuration

The canonical persistence preference file is `.tigerkit/autoresearch/config.json` inside the research home.
Keep the schema small:

```json
{
  "version": 1,
  "mode": "hybrid",
  "trackedRoot": "docs/autoresearch/<slug>",
  "commitOnCheckpoint": true
}
```

Do not add per-document tracking switches. The mode owns the document set:

- `local`: canonical config/state and durable research knowledge stay ignored under
  `.tigerkit/autoresearch/`; no tracked research documents and no research-knowledge commit.
- `hybrid` (default): canonical config/state/scratch stay ignored; tracked research knowledge is
  `README.md`, `findings.md`, `journal.md`, and `experiments/EXP-<NNN>.md`.
- `tracked`: the same tracked research knowledge as `hybrid`, plus sanitized inspectable snapshots of
  `config.json` and `state.md`. Canonical ignored config/state remain the execution source of truth.

`trackedRoot` and `commitOnCheckpoint` apply only to `hybrid` and `tracked`. When
`commitOnCheckpoint=false`, update tracked research documents but do not stage or commit them automatically.

Users may change the config in plain language or by editing JSON. Re-read it before every terminal outcome.
Validate exact keys and types. Reject unknown modes, unknown keys and unsafe paths without rewriting the
user's file.

## Research identity and home

Assign one stable `researchId` after the repository and research goal are clear. Compute it from stable
repository identity plus the normalized initial research goal, persist it, and do not change it for ordinary
wording refinements. Never derive it from secrets or user identifiers.

For the default `hybrid` mode and for `tracked`, establish one dedicated linked research worktree before
creating canonical config/state, tracked research documents, or research source changes. Reuse an existing
worktree only when its canonical state has the same `researchId`. Otherwise create/reuse a safe
`research/<slug>` branch/worktree and make it the research home.

For `local`, the current worktree may be the research home while it is safe and no source mutation requires
isolation. If source mutation becomes useful in a dirty/default/product worktree, move the research program
to a safe linked research worktree before mutation and migrate only this run-owned autoresearch config,
state, local knowledge and experiment artifacts.

Canonical config/state, tracked research documents, experiment code and checkpoint commits for one research
program should live in the same research home. Do not leave canonical state in one worktree while research
knowledge and commits advance in another.

Derive `<slug>` deterministically from the research goal using a short filesystem-safe lowercase slug.
`trackedRoot` must be repository-relative, nonsymlinked, inside the research home repository, and outside
`.git/` and `.tigerkit/`.

The tracked root must advertise its owner in its `README.md` with the stable `researchId`. If an existing
tracked root has a different owner, do not overwrite it. Choose a non-colliding sibling path derived from the
same slug and researchId, then persist that path in canonical config/state.

## Durable knowledge

For `hybrid` and `tracked`:

```text
<trackedRoot>/
├── README.md
├── findings.md
├── journal.md
└── experiments/
    └── EXP-<NNN>.md
```

For `tracked`, also mirror sanitized snapshots:

```text
<trackedRoot>/config.json
<trackedRoot>/state.md
```

Roles:

- `README.md`: current synthesis, direction portfolio, researchId, limitations, current frontier and
  terminal handoff when concluded.
- `findings.md`: supported, rejected, inconclusive and blocked findings. Supersede with reason/provenance;
  never silently delete negative results.
- `journal.md`: append-only research lineage, one `CHK-<NNN>` per material completed batch.
- `experiments/EXP-<NNN>.md`: question/hypothesis, baseline, procedure, evidence, verdict, invalidated
  assumptions, implementation evidence and next implication.
- tracked config/state: sanitized snapshots only and never an authority source.

For `local`, keep equivalent knowledge under `.tigerkit/autoresearch/knowledge/`.

## Tracked-knowledge safety

Tracked research knowledge is repository history. Before writing or committing it, sanitize every tracked
artifact.

Never write secrets, credentials, tokens, private keys, raw protected/operational data, direct personal/user
identifiers, raw request/response dumps, or full sensitive logs into tracked research knowledge, even when
access to the source data was authorized. Do not copy secret values into ignored research state either.

Tracked documents should contain the minimum decision-relevant abstraction: aggregates, generalized examples,
redacted identifiers, source path/revision, experiment ID, evidence hash or an ignored local evidence pointer.
Raw authorized evidence that must temporarily survive stays in a safe ignored run-owned evidence location and
must not be included in checkpoint commits.

If a meaningful conclusion cannot be explained without exposing protected material, keep the detailed
evidence local/ephemeral, write only a safe limitation/provenance statement to tracked knowledge, and mark
the corresponding verification boundary.

## Concurrent-run guard

At the start of a resumed/new batch, capture the canonical state fingerprint and research-home Git HEAD.
During the batch use provisional labels for new experiments when necessary. Before allocating new final
`CHK-<NNN>`/`EXP-<NNN>` IDs or writing a terminal outcome, reread canonical state and current HEAD.

If either changed outside this run, do not append using stale IDs and do not overwrite newer state. Reload the
latest state and reconcile the run's findings when that is mechanically safe; otherwise preserve run-owned
evidence under ignored scratch and return `BLOCKED` with the exact drift. Never silently fork the same
researchId into competing checkpoint sequences.

## Durable outcome transaction

A material run outcome is durable only after the current research delta is recorded. Apply the same
transaction before `CHECKPOINT`, `CONCLUDE`, or a `BLOCKED` outcome that produced material evidence.

1. pass the concurrent-run guard and allocate fresh monotonic checkpoint/experiment IDs;
2. finalize every attempted experiment, including `REJECT`, `INCONCLUSIVE` and evidence-producing
   `BLOCKED` attempts;
3. update durable findings;
4. append exactly one checkpoint journal entry describing question, actions, evidence, verdicts, retired
   directions, new directions and next implication;
5. refresh the current synthesis/direction portfolio;
6. update canonical state atomically and reread it;
7. sanitize and write configured tracked artifacts;
8. when `commitOnCheckpoint=true` and mode is `hybrid` or `tracked`, stage only run-owned research
   documents plus coherent run-owned experiment code from this batch and create one local commit named
   `research(CHK-<NNN>): <short outcome>`;
9. record the resulting local commit in canonical ignored state.

For `CONCLUDE`, the final synthesis must also record the research-home branch, exact research HEAD,
trackedRoot, accepted finding/experiment IDs, rejected alternatives, remaining risks/unknowns and the
recommended next owner such as `tk-prep` or `tk-roadmap`. Experimental code remains research evidence;
handoff does not declare it production-ready.

For `BLOCKED` with no material research delta, do not invent a checkpoint. Record only the minimum canonical
blocking state needed for resume.

Never stage, commit, reset, stash, clean or absorb unrelated user changes. If tracked knowledge cannot be
written or committed safely, preserve the run's knowledge in ignored canonical/local research state, restore
run-owned partial tracked writes when safe, and return `BLOCKED` rather than claiming a durable checkpoint.

Rejected experiment code does not need permanent source retention. Record its experiment result and research
knowledge before reverting/discarding run-owned failed code. Preserve the implementation in a local experiment
commit only when the implementation itself has future research value.

## No-delta rule

Do not create a checkpoint merely because an invocation ran.

- no action and no new decision-relevant evidence -> `NO-ACTION` or `NO-DELTA`;
- an attempted approach that yields new negative evidence -> material delta; persist it before a terminal
  material outcome;
- a source refresh that repeats the existing conclusion without new decision value -> no new finding.

The journal is research lineage, not a heartbeat log. Resume should read canonical state, current synthesis and
relevant findings first; consult journal/experiment history by ID only when needed instead of replaying the
entire history every run.
