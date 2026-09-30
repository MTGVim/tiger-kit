# Executable Exercise Verification

Apply only to executable coding exercises, such as a small function, parser or deterministic CLI,
when a safe runtime/sandbox is already available within current authority. Conceptual retrieval,
written explanations and open-ended design transfer keep the lightweight course checks.

Run the reference/expected solution against the actual checker; source inspection is not a pass.
Construct and run at least one valid-running, plausible wrong implementation tied to the outcome:
hardcoded output, off-by-one, omitted boundary/validation, wrong branch or input-contract misunderstanding.
A syntax error, missing dependency or unrelated execution failure is not discrimination evidence.

If that wrong implementation passes, the checker has not distinguished the intended understanding.
Improve the wording, assertion, inputs or expected behavior, then rerun both reference-pass and
plausible-wrong-fail. For misconception-specific feedback, verify that the linked misconception
actually fails the checker; avoid invented feedback categories.

Keep mutant/driver/temporary solutions in `.tigerkit/tmp/tk-study/<run-id>/`, using Artifact Paths.
Report the actual reference and wrong-variant results and material limits in existing course delivery,
without adding a durable validation report, ledger or mutation framework.
When safe execution is unavailable, continue useful course generation and explicitly mark that
exercise's runtime validation `unavailable / not run`. Never claim execution, install a new runtime
or dependency just for validation, or execute in production.
