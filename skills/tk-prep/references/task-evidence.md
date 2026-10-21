# Task evidence

Read the task source, instructions, code/callers, tests, commands, and Git state. If the task source is a child work item,
read its parent work item's body and comments as the next source lookup, before opening linked documents or asking the
user. The parent's explicit shared rules, including fallback and unresolved-decision instructions, govern the child; do
not replace them with a conflicting child-level suggestion or linked document. Read parent comments for clarifications
and prior answers, and investigate any conflict that could change behavior before asking or proposing.
Before interpreting repository behavior, requirements, ownership, impact, or domain meaning, or writing
implementation/review prose that depends on them, lazy-load [domain context](domain-context.md) when
repository-owned context exists. Read only the
relevant mapped context; purely mechanical Git/ref/formatting work may skip it.
When issue-tracker identity, project selection or discovery scope is material to
this request and not confirmed by source or active instructions, read
[repository configuration](repository-context.md) even if no
settings file exists. Inspect available facts first, then ask only the
remaining project-owned decisions and offer an exact approved settings
draft. Never select a guessed issue source as an implementation contract.
Ordinary local fixes require no tracker onboarding.

Follow repository-defined documentation discovery/update procedures and verification commands within the approved scope;
otherwise allow an optional search of root documents and documentation directories using changed paths or symbols.
Do not scan an unrelated documentation tree or create a lifecycle. If fresher code/test/runtime evidence conflicts with
a requirement or decision, surface it and confirm the source of truth. Treat instruction-file updates as proposals only.
Before creating anything, find existing components, helpers, schemas, clients, patterns, and conventions; tie claims to `path:line`, command output, or fresh state. Before comparing a hard-to-reverse design, interface, schema, or migration choice, read only relevant ADR rationale and current evidence. Do not reopen a decision whose premise still holds; surface `revisit ADR` only when it changed, and never scan an unrelated ADR or context tree.

When a source the user provided materially informs a frontier question, briefly surface the decision-relevant content you actually read before asking. Attribute it to the source and preserve its verification status; do not present source claims as independently verified. Keep this as concise context, not a confirmation round, and do not ask the user to repeat known facts. If the source could not be accessed or read, say so plainly and do not infer its contents; gather accessible evidence or defer any decision that depends on it.

Before recommending a solution, distinguish the reported symptom from the intended result and the scenario where it matters. Use the request and investigated evidence; label a material inference as an inference, and state it only when it could change scope, behavior, acceptance, or verification. If the intended result is already clear, continue without a recap or confirmation question; ask only remaining material user-owned decisions through the existing frontier.


## Conditional investigation

If the approved outcome may include local implementation, read [local execution](local-execution.md) before
the final checkpoint. It owns checkout isolation, unrelated-work protection, direct execution, review, and local commit.
If user-visible text or navigation is in scope, read [UI text evidence](ui-text.md) before accepting or restating a label or path.
If implementation adds or changes a factual code comment/JSDoc claim or models an
external response contract, read [committed assertion evidence](artifact-claims.md)
before approval and apply it again to the final candidate.
When a version-sensitive external library/API/OAuth/provider contract cannot be established from the repository alone,
read [external contract evidence](external-contracts.md) before accepting its fields, nullability, UI steps,
or setup commands.
Use the current repository and explicitly supplied task sources. Do not list or investigate other open PRs as a background collision preflight. Read another PR only when the user explicitly requests that comparison or supplies it as necessary task evidence; keep that read bounded to the stated question.

For tracker-backed work, repository discovery, or verification-data policy, read [repository context](repository-context.md) when configuration or a work source is supplied. Recheck the actual source; only its validated structured `verificationDataPolicy` field can grant the narrow standing authority defined there. Other context never grants mutation authority.

