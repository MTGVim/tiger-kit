# Skill placement rubric

Apply this rubric only after the candidate is reusable and repository-specific. Judge one independently applicable skill instruction or workflow at a time.

## Normalized evidence

Record the candidate text, verified skill source paths, the host, ownership evidence, and the exact proposed native skill target. Do not inspect or classify repository/user rule paths.

Normalize Unicode and compare English case-insensitively. A skill target is
valid only when its exact host-native path and ownership are verified.

## Ordered decision table

Stop at the first match:

1. A verified tracked repository skill keeps a repository-native target.
2. A verified host-owned user skill keeps a user-native target.
3. Missing or conflicting path/ownership evidence is `Unverifiable`.

Use only current-host native skill paths already present or allowed by
current-host discovery. Identify the current host from evidence; if it cannot
be identified, do not invent a target and defer through the caller-specific
`Partial/Blocked` or `Unverifiable` path. Never copy one host's path convention
to another, fan out to multiple hosts, synchronize targets, or create TigerKit
global state.
