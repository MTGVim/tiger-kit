# Adaptive execution shape

Choose only after repository investigation establishes a concrete implementation topology; tell the user the practical consequence, not a classification report.
Ticket length, raw file count, or the presence of both UI and API work never decides the shape.

- durable context `none`: same-session task is small/clear and conversation + repository state are sufficient;
- durable context `seed`: new-session handoff, compaction recovery, lower-capability execution, SDD, or complex
  verification benefits from a self-contained contract;
- execution `direct`: one coherent implementation/test/review judgment surface, including small same-shape changes that can be reviewed together, with or without a Seed;
- execution `sdd`: multiple material Units need independent implementation/test/review judgment loops; requires a Ready Seed;
- execution `handoff`: prepare a Ready Seed and stop for another session/executor.

Complexity may raise safeguards only: inline direct → Seed direct → SDD/re-prep. Never silently downgrade for convenience.
Direct/no-Seed never loads SDD guidance. Load [private SDD](sdd.md) only after SDD is selected.

When durable context is `seed`, execution is `sdd`, or the outcome is `handoff`, read the [Ready Seed contract](seed.md)
before approval. Preserve any existing Seed before approval; direct/no-Seed does not load the Seed contract merely to create ceremony.

