# Plain-chat Question Rounds

Apply only when a question genuinely belongs to the user; this reference does not add an interview,
shared-understanding gate, or new authority to its caller.

1. Investigate safely answerable facts from current evidence instead of asking for them.
2. The current frontier is every unresolved user-owned decision answerable now without guessing
   another unresolved answer. Preserve earlier and parent-owned approvals; do not re-ask them.
3. Ask the whole frontier in one plain-chat round, grouping independent decisions. Defer dependent
   questions until their prerequisites settle; impose no fixed count or round size.
4. Include a recommendation and reason when supported. Wait for user answers, update the decisions
   and evidence, then recompute the frontier. An empty frontier needs no invented question ceremony.

Use the caller's language and this scannable format:

When handing control back for answers, finish analysis, context, recommendations, limitations and
plans before the frontier. The question frontier must be the final substantive block. Keep each
question's choices and recommendation inside that block, and put any short reply-format hint at
its end. Add no analysis, reference note, suggestion, execution plan, or redundant promise after
it. This also applies to a single clarification or approval question; preserve `Q1`, `Q2`, ...
and the prerequisite-aware batching above.

If the narrow structured-input exception below applies, complete explanatory text before the
required tool call and append no follow-up explanation afterward. A technically required fixed
host/system warning may follow only when its exact source mandates that placement; ordinary
writing convenience is not an exception.

```text
❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommended answer and reason, when supported>

---

❓ **Q2 · <short title>**: <independent frontier question>

➡️ <recommended answer and reason, when supported>
```

Do not call `AskUserQuestion`, `request_user_input`, or `clarify` for TigerKit clarification,
selection, approval, scope, publication, product or engineering decisions. They are neither
preferred tools nor fallbacks. The sole exception is an actual host/system contract technically
requiring structured input that plain chat cannot represent with the same meaning and authority.
Before using it, identify that exact requirement and document and verify its bounded scope.
Convenient controls, option display and ordinary approval confirmation do not qualify.

Distilled from TigerKit's `tk-grill` and `mattpocock/skills` grilling at
`d81f3a183412e71a5b1e84ca21bc1a35eea03a60`; the original MIT notice is in the calling package's `LICENSE.txt`.
