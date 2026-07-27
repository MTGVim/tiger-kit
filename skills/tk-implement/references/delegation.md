# Delegation

## Definitions

`direct` means the current agent owns implementation. Non-agent tools such as
context-mode, MCP, search, static analysis, browser tooling inside the required
browser contract, sandboxes, subprocesses, test runners, formatters, linters,
and type checkers are compatible with direct work and are not delegation.

`delegated` means transferring implementation ownership to one autonomous
implementor agent. A tool or subprocess does not make work delegated.

## Decision

Prefer direct when the change is small or mechanical, concentrated in one or a
few files, touches shared or tightly coupled code, fits current context,
requires tight implementation-verification loops, or costs more to isolate
than to implement.

Consider delegated only when scope and completion criteria transfer
independently, relevant files and decisions are clear, shared-file conflicts
are unlikely, context preservation or isolation has material value, and the
main task is implementation rather than design. Size alone is not sufficient.

## Implementor contract

Give one implementor:

- goal, included scope, and excluded scope;
- relevant files or entry points;
- confirmed decisions and TDD mode;
- verification commands or expectations;
- prohibited actions;
- required diff, verification results, and remaining-risk return.

The implementor does not create another agent, re-delegate, invoke a
user-invoked TigerKit skill, expand scope, mix unrelated refactors, commit,
push, create a PR, merge, tag, release, or publish.

The current agent inspects the actual diff, request compliance, and
verification evidence. It may give one concrete fix request and run regression
verification. Never accept delegated output without review. Final verification
and commit remain with the current agent.
