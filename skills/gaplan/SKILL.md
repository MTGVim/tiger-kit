---
name: gaplan
description: Convert a gap report into an implementation plan, task breakdown, validation strategy, and ordered task list. Use after gap analysis and before coding.
---

# gaplan

## Purpose

Turn `.gap/{branch_name}/analysis/gap-report.md` into an executable plan.

Use this skill when the user wants planning, task decomposition, sequencing, validation design, or plan-mode style implementation preparation.

## Operating mode

Prefer planning over implementation.

Do not modify production code in this skill unless the user explicitly asks for implementation in the same step.

## Required inputs

Read:

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

If these files do not exist, ask the user to run:

```text
/tigap:gap
```

or perform a minimal source intake first.

## Required output files

Create or update:

```text
.gap/{branch_name}/plan/implementation-plan.md
.gap/{branch_name}/tasks.md
```

Optionally create:

```text
.gap/{branch_name}/review-checklist.md
```

## Planning principles

1. Keep tasks small.
2. Prefer inspect-before-edit.
3. Identify files likely to change before implementation.
4. Define validation per task.
5. Separate assumptions from confirmed requirements.
6. Mark blockers instead of guessing.
7. Preserve existing project patterns unless there is a clear reason not to.

## Process

### 1. Read gap artifacts

Load the source packet and gap report.

Extract:

- goal
- scope
- non-goals
- assumptions
- risks
- required clarifications
- implementation gaps
- validation needs

### 2. Inspect code shape

If a repository is available, inspect relevant directories and nearby patterns.

Look for:

- architecture boundaries
- component ownership
- data fetching flow
- state management
- validation layers
- test conventions
- naming conventions
- feature flag patterns

### 3. Build implementation plan

Use `templates/implementation-plan.md`.

For each task, include:

- objective
- files to inspect
- files likely to change
- implementation notes
- validation
- risk

### 4. Build task list

Use `templates/tasks.md`.

Tasks must be executable one at a time.

A good task is small enough that `/tigap:go` can complete it without losing scope.

### 5. Review readiness

Before finishing, check:

- Does every requirement map to a task or explicit non-goal?
- Does every high-risk area have validation?
- Are blockers clearly marked?
- Is the first task safe and small?

## Completion criteria

This skill is complete when:

- implementation plan exists
- task list exists
- tasks are ordered
- validation is attached to each meaningful task
- `/tigap:go` can begin without broad replanning

## Handoff

End by recommending:

```text
/tigap:go
```

when the plan is ready.
