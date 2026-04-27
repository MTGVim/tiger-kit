---
name: gap
description: Analyze the gap between source-of-truth material, current implementation, and desired behavior. Use when the user wants requirements intake, source normalization, missing-condition discovery, or pre-planning analysis.
---

# gap

## Purpose

Turn scattered source material into a concrete gap report.

Use this skill when the user wants to understand what is missing, ambiguous, conflicting, risky, or not yet implemented before planning or coding.

## Operating mode

Do not implement code in this skill unless the user explicitly overrides the workflow.

Focus on:

1. source intake
2. source normalization
3. deduplication
4. current-state inspection
5. gap analysis
6. clear next-step recommendations

## Input sources

Ask the user for source-of-truth material if it is not already available.

Accepted source types include:

- issue tracker ticket
- knowledge-base page
- PRD
- design document
- user-written brief
- screenshot
- code path
- pull request
- existing implementation reference
- plain text notes

Do not require a specific tool. Treat all external systems as generic source providers.

## Artifact directory

Use the current git branch name when possible.

Save artifacts under:

```text
.gap/{branch_name}/
```

If the branch name is unavailable, ask for a short work id or infer a safe slug from the task title.

## Required output files

Create or update:

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

Optionally create:

```text
.gap/{branch_name}/sources/
```

Use source snapshots or summaries only when helpful for traceability.

## Process

### 1. Collect source references

If no source material exists, ask for one or more of the following:

```text
- issue tracker ticket
- knowledge-base page
- PRD
- design document
- user-written brief
- relevant code path
```

### 2. Normalize into Source Packet

Transform all source material into the source packet template.

Capture:

- goal
- problem
- confirmed requirements
- acceptance criteria
- constraints
- non-goals
- decisions
- comments or discussion points
- open questions
- related sources

### 3. Deduplicate

When two sources repeat the same content, keep one canonical statement and record that it was duplicated.

When two sources conflict, do not silently merge them. Mark the conflict explicitly.

### 4. Inspect current implementation

If code access is available, inspect relevant files before producing implementation gaps.

Look for:

- existing behavior
- related components
- existing data flow
- validation rules
- tests
- feature flags
- error handling
- naming patterns

### 5. Produce gap report

Use `templates/gap-report.md`.

Classify findings as:

- confirmed requirement
- missing requirement
- ambiguous requirement
- conflicting information
- implementation gap
- UX/UI gap
- API/data gap
- edge case
- risk
- required clarification

## Completion criteria

This skill is complete when:

- source material has been normalized
- duplicate and conflicting information has been handled
- current implementation has been inspected where possible
- a gap report exists
- next steps are clear enough for `/tigap:gaplan`

## Handoff

End by recommending:

```text
/tigap:gaplan
```

only after the gap report is ready.
