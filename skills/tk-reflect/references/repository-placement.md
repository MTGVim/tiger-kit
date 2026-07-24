# Repository placement rubric

Apply this rubric only after the candidate is reusable and repository-specific. Judge one independently applicable normative instruction or workflow at a time.

## Normalized evidence

Record the candidate text, verified repository-relative source paths, each immediate parent, the count of other Git-tracked regular files directly in that parent, the threshold and its source, and the matched safety token or `none`. Do not count directories, globs, examples, missing paths, recursive descendants, or the candidate source paths themselves. Different immediate parents cannot share one nested placement.

Normalize Unicode and compare English case-insensitively. The closed safety token set is: `XSS`, `cross-site scripting`, `SQL injection`, `command injection`, `prompt injection`, `인젝션`, `개인정보`, `PII`, `유출`, `secret`, `credential`, `API key`, `data loss`, `irreversible loss`, `비가역 손실`, `복구 불가`. Generic words such as `must`, `never`, `금지`, or `절대` do not create a safety signal.

The default sibling threshold is `15`; `sibling_count <= threshold` is local. Override it only with a positive integer explicitly given in the current request or an existing exact repository key `tigerkit.repo_rule_sibling_threshold: <positive integer>`, in that precedence order. Conflicting values at the same precedence or non-positive/non-integer values stop classification. Never create configuration or TigerKit state for an override.

## Ordered decision table

Stop at the first match:

1. A safety token matches: root or always-loaded host-native `repo rule`.
2. No safety token, every verified path has one immediate parent, and `sibling_count <= threshold`: the nearest host-native nested `repo rule` for that parent.
3. No safety token and there is no concrete path, there are multiple parents, or `sibling_count > threshold`: `repo skill`.
4. Required path, count, Git, or threshold evidence is inaccessible or conflicting: defer classification through the caller's `low`, `Blocked`, or `Unverifiable` path.

Use only current-host native paths already present or allowed by current-host discovery. Identify the current host from evidence; if it cannot be identified, do not invent a target and defer through the caller-specific `low`, `Partial/Blocked`, or `Unverifiable` path. Never copy one host's path convention to another host, fan out to multiple hosts, synchronize targets, or create TigerKit global state. A shared repository rule is eligible only when the user names it or a tracked shared instruction file is discovered. A nested rule remains a placement of the `repo rule` target, not a fifth target kind.
