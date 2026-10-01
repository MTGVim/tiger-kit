# Autoresearch Persistence

Read this reference before initializing persistence, changing persistence settings, writing a checkpoint,
or committing research-owned knowledge.

## Configuration

The canonical execution preference file is `.tigerkit/autoresearch/config.json`. It is local, ignored
runtime state even when selected research knowledge is tracked. Create it automatically after the research
identity is clear if it does not exist. Do not make initial configuration a user interview.

Default:

```json
{
  "version": 1,
  "mode": "hybrid",
  "trackedRoot": "docs/autoresearch/<slug>",
  "track": {
    "config": true,
    "summary": true,
    "findings": true,
    "journal": true,
    "experiments": true,
    "state": false
  },
  "commitOnCheckpoint": true
}
```

Derive `<slug>` deterministically from the research goal using a short filesystem-safe lowercase slug.
Never include secrets, user identifiers, issue prose or mutable timestamps in the slug.

Users may change these settings in plain language or by editing the JSON. Re-read the current config before
each checkpoint. Validate exact keys/types and reject unknown modes, unsafe paths or malformed values without
rewriting the user's file.

Modes:

- `local`: keep state and research knowledge under `.tigerkit/autoresearch/`; create no tracked research
  documents and no checkpoint knowledge commit.
- `hybrid` (default): keep execution state/config/scratch under `.tigerkit/autoresearch/`, while durable
  research knowledge selected by `track` is written under `trackedRoot`.
- `tracked`: same durable knowledge surface as `hybrid`, and also mirror selected config/state snapshots
  under `trackedRoot` when their `track` flags are true. Local config/state remain the execution source
  of truth and tracked copies are inspectable snapshots, not authority.

`trackedRoot` must be repository-relative, inside the current repository, nonsymlinked and outside
`.git/` and `.tigerkit/`. Apply the same safe-path/ownership discipline as Artifact Paths before writes.
Do not delete old tracked research history merely because mode or tracked root changes.

## Durable knowledge

For `hybrid` and `tracked`, use this compact tracked surface by default:

```text
<trackedRoot>/
├── README.md
├── findings.md
├── journal.md
└── experiments/
    └── EXP-<NNN>.md
```

When enabled by `track`, also mirror:

```text
<trackedRoot>/config.json
<trackedRoot>/state.md
```

Roles:

- `README.md`: current synthesis, direction portfolio, important limitations and next research frontier.
- `findings.md`: durable supported, rejected, inconclusive and blocked findings. Never silently remove a
  negative result; supersede it with reason and provenance.
- `journal.md`: append-only checkpoint history. One `CHK-<NNN>` entry per meaningful completed batch.
- `experiments/EXP-<NNN>.md`: question/hypothesis, baseline, procedure, evidence, verdict, invalidated
  assumptions, implementation evidence when applicable, and next implication.
- tracked `config.json`/`state.md`: sanitized snapshots only. Never let them grant runtime authority.

For `local`, keep equivalent knowledge under `.tigerkit/autoresearch/knowledge/` so failed directions and
checkpoint history still survive locally even though Git does not track them.

## Checkpoint transaction

A `CHECKPOINT` is successful only after the current research delta is durably recorded.

Before returning `CHECKPOINT`:

1. finalize every experiment attempted in the batch, including `REJECT`, `INCONCLUSIVE` and `BLOCKED`;
2. update `findings.md` or its local equivalent with new/superseded findings;
3. append exactly one `CHK-<NNN>` entry to `journal.md` or its local equivalent;
4. refresh the current synthesis and next frontier;
5. atomically update and reread canonical state;
6. mirror configured tracked artifacts;
7. when `commitOnCheckpoint` is true and mode is `hybrid` or `tracked`, stage only run-owned research
   documents plus coherent run-owned experiment code that belongs to this batch, then create one local commit
   named `research(CHK-<NNN>): <short outcome>`;
8. record the resulting local commit in canonical ignored state after the commit succeeds.

Never stage, commit, reset, stash, clean or absorb unrelated user changes. If tracked checkpoint output cannot
be committed safely, preserve canonical/local research state, report the checkpoint as `Blocked` rather than
claiming a committed checkpoint, and keep independent read-only research available for a later run.

Rejected experiment code does not need permanent source retention. Before reverting/discarding run-owned
failed code, write the experiment record and checkpoint knowledge first. If the implementation itself has
future research value, preserve it in a local experiment commit and reference the experiment/checkpoint ID.
The durable reason/evidence for failure is mandatory even when the failed code is removed.

## No-delta rule

Do not append a journal checkpoint merely because an invocation ran.

- no action and no new evidence -> `NO-ACTION` or `NO-DELTA`, with no synthetic checkpoint;
- an attempted approach that produced decision-relevant negative evidence -> this is a material delta and
  must be recorded as a finding/experiment before `CHECKPOINT`, `CONCLUDE` or `BLOCKED`;
- a changed source that merely repeats an existing conclusion without new decision value is not a new finding.

The journal is research lineage, not a heartbeat log.
