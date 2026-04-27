# tigap-skills

`tigap-skills` is a small Claude Code / agent workflow pack for turning vague work into a controlled implementation loop.

It provides three skills:

- `/tigap:gap` — collect source material and produce a gap report
- `/tigap:gaplan` — convert the gap report into an implementation plan and task list
- `/tigap:go` — execute the task list in small, verifiable steps

The workflow is intentionally generic. It can consume issue tracker tickets, knowledge-base pages, PRDs, design docs, user-written briefs, screenshots, code references, or plain notes.

## Recommended flow

```text
/tigap:gap
/tigap:gaplan
/tigap:go
```

## Artifact layout

By default, generated work artifacts should live under the current project:

```text
.gap/{branch_name}/
  sources/
  normalized/source-packet.md
  analysis/gap-report.md
  plan/implementation-plan.md
  tasks.md
  execution-log.md
  review-checklist.md
```

The skill files are reusable workflow instructions. Runtime artifacts are project-local working notes.

## Plugin mode

Use this repo as a Claude Code plugin directory:

```bash
claude --plugin-dir ./tigap-skills
```

Expected commands:

```text
/tigap:gap
/tigap:gaplan
/tigap:go
```

## Standalone mode

Copy skills into a project-local `.claude/skills` directory:

```bash
./scripts/install-standalone.sh /path/to/project
```

PowerShell:

```powershell
./scripts/install-standalone.ps1 -TargetProject C:\path\to\project
```

This installs:

```text
/path/to/project/.claude/skills/gap
/path/to/project/.claude/skills/gaplan
/path/to/project/.claude/skills/go
```

Standalone invocation may be available as:

```text
/gap
/gaplan
/go
```

## Design notes

- Keep source intake generic.
- Normalize all inputs into a source packet before analysis.
- Save analysis and plans as project-local artifacts.
- Prefer small tasks with explicit validation.
- Avoid broad implementation before `/tigap:gaplan` has produced a task plan.
