# Skill placement rubric

Apply this rubric only when a candidate is reusable and repository-specific. Evaluate
one independently applicable skill instruction or workflow at a time.

## Normalized evidence

Record the candidate text, verified skill source path, host, ownership evidence, and
exact proposed native skill target. Do not inspect or classify repository/user rule
paths.

Normalize Unicode and compare English case-insensitively. Treat a skill target as valid
only when the exact host-native path and ownership are verified.

## Ordered decision table

Stop at the first match.

1. A verified tracked repository skill keeps its repository-native target.
2. A verified host-owned user skill keeps its user-native target.
3. Missing or conflicting path/ownership evidence is `Unverifiable`.

Use only an existing current-host native skill path or one allowed by current-host
discovery. Identify the current host from evidence. If it cannot be identified, do not
invent a target; route to a caller-specific `Partial/Blocked` or `Unverifiable` path.
Do not copy one host's path convention to another, fan out across hosts, synchronize
targets, or create TigerKit global state.
