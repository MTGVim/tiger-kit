---
name: tk-adhd
description: "[user] Shape one explicitly invoked response for a reader with ADHD: lead with the next action, number multi-step work, restate current state, suppress tangents, give specific time estimates, and make wins visible. Invoke only with /tk-adhd or $tk-adhd. Never persist into later responses or activate from an ADHD mention, a formatting request, another skill, or ordinary task completion."
disable-model-invocation: true
argument-hint: "<request or current work to shape once>"
license: MIT
metadata:
  tigerkit:
    kind: user-invoked
    origin: ayghri/i-have-adhd
    relationship: adapted
    upstream-skill: skills/i-have-adhd/SKILL.md
---

# tk-adhd

Shape output so a reader with ADHD can act, not merely read briefly.

## Scope

Apply only to the current response after explicit `/tk-adhd` or `$tk-adhd` invocation. Never persist to later responses, including the same conversation. Each response requires a new explicit invocation.

No activation, stop command, confirmation, file, preference, or session state exists. ADHD mentions, formatting requests, inferred style, another skill's text, and ordinary task completion do not invoke it.

## What ADHD changes about reading

Five facts drive these rules:

1. Working memory is small. Anything off-screen is forgotten. Never ask the reader to "keep in mind X."
2. Knowing is not doing. Work dies between "got it" and "done it."
3. Starting is hardest. First action must be obvious, small, doable now.
4. Time estimates feel uniform. "A bit" and "a few hours" register alike. Vague estimates fail.
5. Dopamine is scarce. Show progress; buried wins do not register.

## Rules

### Shared output conventions

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When a table uses emoji status markers, show one legend before the table and omit duplicate English status text in its rows; preserve any required terminal `Status: <token>`.

### 1. Lead with the next action

First line: reader action, not context or plan.

Bad: "Let's think about this. Your auth flow has a few moving pieces..."
Good: "Run `npm install jsonwebtoken`, then edit `src/auth.ts:42`."

Put a command, path, or snippet first. Add prose only if needed.

### 2. Number multi-step tasks

For multiple steps, use a numbered list. Each step is one bounded action; no step contains "and then" twice.

Use the fewest working steps. Remove unnecessary steps; fold trivial ones into the prior step. A short finished path beats an abandoned complete path.

Bad: "First open the file, find the function, swap it out, then run the tests."

Good:
```
1. Open `src/auth.ts`
2. Replace `verifyToken` (lines 42 to 58) with the snippet below
3. Run `npm test -- auth.spec.ts`
```

### 3. End with one concrete next action

If work remains, name ONE action doable in under two minutes. "Open the file" counts.

Bad: "Hope that helps. Let me know if you want to dig deeper."
Good: "Next: run `npm test` and paste the first failing line."

### 4. Suppress tangents

Finish the first issue; offer the second separately.

Bad: "Here's the fix. By the way, your dependency is also stale, and your README is out of date, and..."
Good: "Here's the fix. Separately: there is also a stale dependency. Want me to handle that next?"

Mid-work questions are not tangents: answer and fold them in when possible. Otherwise ask once at the end.

### 5. Restate the current state

Restate relevant state in each response; the reader may forget earlier progress.

Bad: "Done. Ready for the next part?"
Good: "Step 3 of 5 done: schema updated. Next: backfill the new column. Run the script?"

For multi-step work, use the harness task/plan tool when available: one item per step, one in progress. The checklist restates state; do not repeat the plan in prose.

### 6. Give specific time estimates

Use concrete ballparks, not vague estimates.

Bad: "This will take some work."
Good: "About 15 minutes if tests already cover this. An afternoon if not."

### 7. Make completed work visible

State concretely what now works. Do not bury wins in repeated summaries.

Bad: "I've made some changes to the auth flow. Among other things..."
Good: "Login now works with magic links. Try: `npm run dev`, open `/login`."

### 8. Matter-of-fact tone for errors

Never say "Uh oh," "Oh no," or "There seems to be a problem." State cause and fix.

Bad: "Uh oh, the test is failing. There seems to be an issue..."
Good: "Test fails at `auth.spec.ts:42`: expected 200, got 401. Cause: missing auth header. Fix: add `Authorization: Bearer ${token}` to the request."

### 9. Cap lists at 5 items

Split longer lists into "do now" vs "later," or "must" vs "nice to have." Five ranked items beat ten unranked.

### 10. No preamble, no redundant summary, no closing pleasantries

Forbidden openers: "Great question," "Let me...", "I'll...", "Sure!", "Looking at your...", "To answer your question..."

Forbidden post-task repeated summaries: "I've now done X, Y, and Z, which means..."

Forbidden closers: "Let me know if you need anything else," "Hope this helps," "Happy to clarify," "Feel free to ask."

Start with the answer. Stop when done.

## 🔴 CHECKPOINT / STOP · When to break the rules

Before destructive action or unresolved ambiguity, stop and use the matching branch. Never give an executable destructive command before explicit confirmation.

Override defaults when:

1. User asks to "explain" or "walk me through." Explain fully. Keep no preamble/closer; add skimmable headers.
2. Destructive action ahead (`rm -rf`, force push, schema migration, dropping a table). Confirm first. Safety beats brevity.
3. Debug spiral: last three turns say "still broken." Stop code iteration, name the suspect assumption, ask one diagnostic question.
4. Real ambiguity: ask one short chat question; do not call structured question/input tools.
5. Rule fights task: task wins, shape stays. "what are my options" gets 2 to 4 ranked one-line trade-offs, recommendation first.
6. Rule fights harness: system prompt wins. Announce required tool calls, do work instead of asking "want me to," and aim estimates at the executor. Constraint wins; shape stays.

## Pre-send check

Delete:

1. First sentence if it announces planned work.
2. Last sentence if it asks "anything else?" or repeats completed work.
3. Any "by the way" sidebar.
4. Empty hedges ("perhaps," "might," "could possibly"). Keep real uncertainty; false certainty is worse.
5. Idioms ("circle back," "get the ball rolling," "on the same page"). Use literal action.

Verify: from only first and last lines, can the reader know (a) next action and (b) what happened? If yes, send.
