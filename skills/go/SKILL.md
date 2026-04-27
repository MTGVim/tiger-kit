---
name: go
description: Execute a prepared task list in small validated steps. Use after planning when the user wants implementation progress without losing scope.
---

# go

## Purpose

Execute `.gap/{branch_name}/tasks.md` one task at a time.

Use this skill when the user wants implementation to begin after gap analysis and planning.

## Operating mode

Small-step execution only.

Do not jump ahead. Do not rewrite the plan unless a blocker or contradiction is found.

## Required inputs

Read:

```text
.gap/{branch_name}/plan/implementation-plan.md
.gap/{branch_name}/tasks.md
```

If missing, ask the user to run:

```text
/tigap:gaplan
```

or produce a minimal plan first.

## Required output files

Update:

```text
.gap/{branch_name}/tasks.md
.gap/{branch_name}/execution-log.md
```

Optionally update:

```text
.gap/{branch_name}/review-checklist.md
```

## Process

### 1. Select next task

Choose the first unchecked task in `Ready` unless the user specifies another task.

Move it to `In Progress` or mark it clearly as active.

### 2. Inspect before editing

Before changing code, inspect:

- files listed in the plan
- adjacent implementations
- tests
- existing patterns
- relevant imports and exports

### 3. Implement narrowly

Make only the changes required for the active task.

Avoid opportunistic refactors unless they are required for correctness.

### 4. Validate

Run the task-specific validation if available.

Prefer existing project commands:

- typecheck
- lint
- unit tests
- integration tests
- build

If validation cannot be run, record why.

### 5. Update artifacts

Update `tasks.md`:

- move completed task to `Done`
- keep incomplete task in `In Progress` or `Blocked`
- add newly discovered tasks under `Ready` or `Blocked`

Append to `execution-log.md`:

- task name
- files changed
- validation run
- result
- risks or follow-ups

## Stop conditions

Stop and report if:

- requirements conflict with implementation reality
- required source material is missing
- validation fails and the fix is not obvious
- the task requires a scope increase
- the implementation would affect unrelated areas

## Completion criteria

This skill is complete when one task has been implemented and validated, or when a blocker has been clearly documented.
