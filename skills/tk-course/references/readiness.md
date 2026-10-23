# Optional prerequisite preparation

Use only when a goal depends on important knowledge this course will not teach. Compare the
actual curriculum, assessments and inspected sources before naming a gap. Content taught here
is not an untaught prerequisite. Keep the scope tied to the goals; terminology similarity alone
is not evidence. In curriculum.md retain the dependency, its source and whether it is confirmed
or inferred; state what evidence would resolve an inference. Ask only a material user-owned
unknown, reusing the learner scope and narration decisions already established.

Prioritize preparation by the affected goals, dependency reach and learner evidence. Authored
order expresses that priority; no graph, numerical weighting or fixed question count is needed.
Use a concrete code/error/output/reasoning situation with one defensible correct answer. Split
ambiguous multiple-answer questions. Explain the correct reasoning and each plausible wrong
mental model; a selected distractor suggests a review need, not a proven enduring misconception.

Use the optional course-level `readiness` list in course.json, rendered in the existing home.
Each entry has stable `id`, `title`, `basis` (inspected source/curriculum evidence), `confidence`
(`confirmed` or `inferred`), nonempty `objective_ids` for affected course goals, `prompt`,
`choices` as `[id, label]` pairs, `answer`, `explanation`, `choice_explanations` keyed by every
choice ID, and `preparation` containing enough inline review to proceed offline. For inferred
entries include the uncertainty and what would resolve it in `basis`; learners see that label.
Keep the source/curriculum evidence accurate; the builder checks structure, not pedagogical truth.

The native question/answer component provides optional feedback and retry. Preparation remains
readable without JavaScript. Never gate lesson entry or turn answers into proficiency, completion,
placement or certification. Answers are transient, never exported with progress, stored or sent.
No login, server, consumer runtime, API or network is required. Optional external reading cannot
replace the inline preparation. With no readiness list, add no diagnostic UI or interview.

On revision, preserve lesson IDs/manual progress and bump the course revision for readiness
changes; retain the ordinary source, incremental replacement and sharing contracts. Verify a
wrong, correct and unanswered choice, retry, keyboard/mobile/theme access and actual file://
operation. Check that preparation does not change completion or progress export. Do not claim
learning from a visit or a score. Pass only relevant evidence and its uncertainty to tk-teach
when an authorized learner handoff is requested, never automatic cross-course sharing.
