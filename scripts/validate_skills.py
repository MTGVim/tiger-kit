#!/usr/bin/env python3
"""Validate TigerKit Agent Skills using only the Python standard library."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
KINDS = {"user-invoked", "hybrid"}
INVOCATION_LABELS = {
    "user-invoked": "[user]",
    "hybrid": "[user/auto]",
}
RELATIONSHIPS = {"copied", "adapted", "inspired-by", "forked", "native"}
CORE_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
HOST_EXTENSION_FIELDS = {"argument-hint", "disable-model-invocation"}
MECHANICAL_ASSERTION_TYPES = {
    "event_absent",
    "event_count",
    "event_order",
    "terminal_status",
    "path_exists",
    "path_absent",
    "git_head_changed",
    "git_head_unchanged",
    "output_contains",
    "output_absent",
    "path_text_contains",
    "path_text_absent",
    "path_text_equals",
    "git_commit_count_delta",
    "changed_paths_equal",
    "git_diff_contains",
    "git_diff_absent",
}
EVENT_TYPES = {"phase_invocation", "final_output"}
TERMINAL_STATUSES = {
    "Pass",
    "Fail",
    "Blocked",
    "Unverifiable",
    "Pending",
    "NotApplicable",
}
SUPPORTED_EVAL_HOSTS = {"claude-code", "codex", "hermes-agent"}
USER_DECISION_CONTRACT_TOKENS = (
    "## User decision questions",
    "`Question`",
    "`Recommendation`",
    "decision-relevant evidence",
    "two or three",
    "mutually exclusive options",
    "exactly one label",
    "`(Recommended)` or `(추천)`",
    "native structured input",
    "Plain text is allowed only",
    "failed or rejected call is not absence",
    "`AskUserQuestion`",
    "`request_user_input`",
    "Hermes Agent",
    "`clarify`",
)
RESULT_BUDGET_TOKENS = {
    "tk-ask-repo": ("one to three short paragraphs", "two to seven results", "top five to seven"),
    "tk-browser-verify": ("two to seven verified scenarios", "top five to seven"),
    "tk-drive": ("two to seven behavior-level bullets", "one to four aggregate-result bullets", "top five to seven"),
    "tk-adhd": ("## Rules", "## When to break the rules"),
    "tk-grill-me": ("two to seven readable", "top five to seven"),
    "tk-grooming": ("two to seven findings", "top five to seven"),
    "tk-handoff": ("two to five short bullets", "top five to seven"),
    "tk-implement": ("2–5 short", "1–4 verification-result bullets", "underlying results exceed"),
    "tk-learn": ("two to seven candidate", "top five to seven"),
    "tk-merge-conflict": ("two to five short rows or bullets", "top five to seven"),
    "tk-prototype": ("two to five bullets or", "top five to seven"),
    "tk-reflect": ("at most five", "never substitutes for the Disposition table"),
    "tk-skill-diagnose": ("two to seven reproduced", "top five to seven"),
    "tk-to-spec": ("two to five short bullets", "top five to seven"),
    "tk-to-tickets": ("two to seven tickets", "top five to seven"),
}
TERMINAL_SUMMARY_GATE = (
    "### 🔴 HARD GATE · terminal user summary\n\n"
    "Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. "
    "Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. "
    "Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. "
    "Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.\n\n"
    "Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. "
    "When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. "
    "Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. "
    "Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.\n\n"
    "Persist provenance only in an artifact or ledger the skill already owns. "
    "A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. "
    "Never require a shared runtime reference outside this skill."
)
DRIVE_TERMINAL_SUMMARY_GATE = (
    "### 🔴 HARD GATE · terminal user summary\n\n"
    "Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. "
    "Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. "
    "Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. "
    "Do not emit a terminal user-summary opening between successful consecutive active-drive procedure invocations.\n\n"
    "Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. "
    "When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. "
    "Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.\n\n"
    "Persist provenance only in an artifact or ledger already owned by the workflow. "
    "Never require a shared runtime reference outside this skill."
)
DIRECT_TERMINAL_SUMMARY_GATE = (
    "### 🔴 HARD GATE · terminal user summary\n\n"
    "Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. "
    "Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. "
    "Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. "
    "Do not emit a terminal user-summary opening between successful consecutive active-drive procedure invocations.\n\n"
    "Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. "
    "When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. "
    "Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.\n\n"
    "Persist provenance only in an artifact or ledger already owned by the workflow. "
    "A read-only skill remains read-only. Never require a shared runtime reference outside this skill."
)
DIRECT_GRAPH_SKILLS = {
    "tk-browser-verify",
    "tk-drive",
    "tk-grill-me",
    "tk-implement",
    "tk-merge-conflict",
    "tk-prototype",
    "tk-reflect",
    "tk-to-spec",
    "tk-to-tickets",
}
DRIVE_GRAPH_NODES = {
    "tk-drive:preflight",
    "tk-grill-me",
    "tk-prototype",
    "tk-to-spec",
    "tk-to-tickets",
    "tk-implement",
    "tk-merge-conflict",
    "aggregate-verification",
    "tk-browser-verify",
    "tk-reflect",
    "tk-drive:finalization",
    "tk-drive:non-success-finalization",
}
DRIVE_GRAPH_EDGES = (
    ("tk-drive:preflight", "tk-grill-me", "material decisions remain", "confirmed", "stop", "tk-to-spec"),
    ("tk-drive:preflight", "tk-to-spec", "no material decisions remain", "Ready", "stop", "tk-to-tickets|tk-implement"),
    ("tk-grill-me", "tk-prototype", "bounded comparison reduces uncertainty", "evidence", "stop", "tk-grill-me"),
    ("tk-prototype", "tk-grill-me", "comparison completed", "confirmed", "stop", "tk-to-spec"),
    ("tk-grill-me", "tk-to-spec", "decisions confirmed", "Ready", "stop", "tk-to-tickets|tk-implement"),
    ("tk-to-spec", "tk-to-tickets", "multiple units", "verified tickets", "stop", "tk-implement"),
    ("tk-to-spec", "tk-implement", "single unit", "verified commit", "stop", "tk-implement|aggregate-verification"),
    ("tk-to-tickets", "tk-implement", "verified tickets", "verified commit", "stop", "tk-implement|aggregate-verification"),
    ("tk-implement", "tk-merge-conflict", "active conflict", "resolved", "stop", "tk-implement"),
    ("tk-merge-conflict", "tk-implement", "conflict resolved", "verified commit", "stop", "tk-implement|aggregate-verification"),
    ("tk-implement", "tk-implement", "more selected units", "verified commit", "stop", "tk-implement|aggregate-verification"),
    ("tk-implement", "aggregate-verification", "all units committed", "verified", "correct-or-stop", "tk-browser-verify|tk-implement|tk-reflect|tk-drive:finalization"),
    ("aggregate-verification", "tk-browser-verify", "browser evidence required", "verified", "stop", "aggregate-verification"),
    ("tk-browser-verify", "aggregate-verification", "browser check completed", "verified", "stop", "tk-implement|tk-reflect|tk-drive:finalization"),
    ("aggregate-verification", "tk-implement", "isolated failure under correction limit", "verified commit", "stop", "aggregate-verification"),
    ("aggregate-verification", "tk-reflect", "valid reflection handoff", "complete-or-no-op", "restore-or-stop", "tk-drive:finalization"),
    ("aggregate-verification", "tk-drive:finalization", "verified and reflection N/A", "terminal evidence reread", "stop", "terminal"),
    ("tk-reflect", "tk-drive:finalization", "reflection completed", "terminal evidence reread", "stop", "terminal"),
    ("tk-drive:preflight", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-grill-me", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-prototype", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-to-spec", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-to-tickets", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-implement", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-merge-conflict", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("aggregate-verification", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-browser-verify", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
    ("tk-reflect", "tk-drive:non-success-finalization", "terminal non-success with no alternate edge", "scope accounted", "preserve native status", "terminal"),
)
DRIVE_ALLOWED_LOOP_EDGES = {
    ("tk-grill-me", "tk-prototype"),
    ("tk-prototype", "tk-grill-me"),
    ("tk-implement", "tk-merge-conflict"),
    ("tk-merge-conflict", "tk-implement"),
    ("tk-implement", "tk-implement"),
    ("tk-implement", "aggregate-verification"),
    ("aggregate-verification", "tk-implement"),
    ("aggregate-verification", "tk-browser-verify"),
    ("tk-browser-verify", "aggregate-verification"),
}
DRIVE_STAGE_TOKENS = (
    "Preparing",
    "Executing",
    "same active",
    "`tk-grill-me`",
    "`tk-to-spec`",
    "`tk-to-tickets`",
    "`tk-prototype`",
    "`tk-implement`",
    "`tk-reflect`",
    "one amendment",
)
DRIVE_CORRECTIVE_BOUND_TOKENS = (
    "zero corrective cycles",
    "at most three",
    "fourth cycle",
)
BROWSER_PREFLIGHT_TOKENS = (
    "required | optional | N/A",
    "material user-owned",
    "opaque profile",
    "intentionally omitted",
    "re-request",
    "not a Preparing amendment",
)
CONTINUATION_BOUNDARY_TOKENS = {
    "README.md": (
        "prompt-directed",
        "확률적",
        "durable scheduler",
        "workflow engine",
    ),
    "skills/tk-drive/SKILL.md": (
        "prompt-directed instruction",
        "not a durable scheduler",
        "guaranteed cross-turn execution",
        "rereading current artifacts and repository evidence",
    ),
    "skills/tk-drive/references/phases.md": (
        "prompt-directed and probabilistic",
        "durable scheduling",
        "event replay",
        "guaranteed cross-turn execution",
    ),
}
ADHD_CONTRACT_TOKENS = (
    "disable-model-invocation: true",
    "/tk-adhd",
    "$tk-adhd",
    "origin: ayghri/i-have-adhd",
    "relationship: adapted",
    "upstream-skill: skills/i-have-adhd/SKILL.md",
    "## Scope",
    "only to the current response",
    "Do not carry them into the next response",
    "Every later response requires a new explicit",
    "No activation, stop command, confirmation, file, preference, or session state",
    "does not invoke this utility",
    "## Rules",
    "## When to break the rules",
    "## Pre-send check",
)
ADHD_FORBIDDEN_TOKENS = (
    "## Persistence",
    "ADHD mode: on",
    "ADHD mode: off",
    "latest explicit activation or stop event wins",
)
LEARNING_LOOP_TOKENS = {
    "skills/tk-grill-me/SKILL.md": ("active drive",),
    "skills/tk-reflect/SKILL.md": (
        "Preferred prevention owner",
        "Host dependency",
    ),
    "skills/tk-drive/SKILL.md": (
        "at most seven",
        "applicable rules, ADRs, tests, types, lint, CI, repository skills, and code invariants",
        "raw sessions, prior implementation or reflection scratch, pending drafts, arbitrary global state",
        "inaccessible host-only rules",
    ),
    "skills/tk-to-spec/SKILL.md": (
        "pass the Ready artifact path",
        "`adopted | already-satisfied | not-applicable | conflict`",
        "R/AC mapping",
        "A `conflict` disposition prevents `Ready`",
        "no relevant prior art exists, omit `## Prior art`",
    ),
    "skills/tk-to-tickets/SKILL.md": (
        "directly to the next applicable graph",
    ),
}
RESPONSE_LANGUAGE_GATE = (
    "### 🔴 HARD GATE · response language\n\n"
    "Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. "
    "Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. "
    "Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. "
    "Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language."
)
CATALOG_ROUTING_BOUNDARIES = {
    "tk-ask-repo vs ordinary repository Q&A",
    "tk-ask-repo vs tk-implement",
    "tk-ask-repo vs tk-grill-me",
    "tk-ask-repo vs runtime reproduction",
    "tk-ask-repo vs general technical knowledge",
    "tk-ask-repo vs effort estimation",
    "tk-to-spec vs tk-to-tickets",
    "tk-reflect vs tk-grooming",
    "tk-learn vs tk-reflect/tk-grooming",
    "tk-implement vs tk-drive",
    "tk-prototype vs tk-browser-verify",
    "tk-handoff vs generic summary/continue",
    "tk-drive vs tk-handoff/generic continue",
    "tk-drive vs tk-grill-me",
    "tk-drive explicit source vs generic request",
    "tk-adhd explicit invocation vs tk-reflect and implicit formatting",
    "tk-merge-conflict vs ordinary conflict-marker edit",
    "tk-skill-diagnose vs ordinary application/code debugging",
    "tk-skill-diagnose vs tk-grooming",
    "tk-skill-diagnose vs tk-learn",
    "tk-skill-diagnose vs tk-reflect",
    "tk-skill-diagnose vs Darwin/general optimization",
    "tk-reflect conditional handoff vs generic reflection",
}
HYBRID_TRIGGER_FACETS = {"formal", "casual", "typo", "ko-en", "short", "compound"}
HANGUL_SYLLABLE = re.compile(r"[가-힣]")
# This is the current catalog snapshot, not a product target count. Update it,
# its kind sets, and their tests whenever an independently justified catalog
# change lands.
EXPECTED_SKILLS = {
    "tk-ask-repo",
    "tk-browser-verify",
    "tk-drive",
    "tk-grill-me",
    "tk-grooming",
    "tk-handoff",
    "tk-implement",
    "tk-learn",
    "tk-merge-conflict",
    "tk-adhd",
    "tk-prototype",
    "tk-reflect",
    "tk-skill-diagnose",
    "tk-to-spec",
    "tk-to-tickets",
}
USER_INVOKED_SKILLS = {
    "tk-ask-repo",
    "tk-drive",
    "tk-adhd",
}
HYBRID_SKILLS = EXPECTED_SKILLS - USER_INVOKED_SKILLS
KEBAB = re.compile(r"^tk-[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
REQUIRED_BEHAVIOR_CASES = {
    "ask-repo-value-finds-assignment-origin",
    "ask-repo-impact-sweeps-consumers",
    "ask-repo-existence-distinguishes-states",
    "ask-repo-attribution-uses-transport",
    "ask-repo-blocks-two-candidate-ambiguity",
    "ask-repo-refuses-implementation-diff",
    "ask-repo-refuses-effort-estimate",
    "ask-repo-search-failure-is-unverifiable",
    "ask-repo-blocks-contradicted-premise",
    "ask-repo-bounds-result-cardinality",
    "drive-writes-compact-preflight",
    "drive-bounds-task-anchored-prior-art",
    "drive-excludes-forbidden-prior-art",
    "drive-preserves-preflight-on-write-failure",
    "drive-rejects-preflight-secrets",
    "drive-resumes-from-current-evidence",
    "drive-enforces-exact-procedure-graph",
    "drive-continues-without-receipt-boundary",
    "drive-continues-multi-unit-through-reflection",
    "drive-owns-single-terminal-response",
    "drive-finalizes-partial-blocked-scope",
    "drive-finalizes-aggregate-fail",
    "drive-finalizes-browser-unverifiable",
    "drive-blocks-unrestored-reflection-state",
    "drive-keeps-grill-pending-open",
    "drive-normalizes-grill-aborted",
    "drive-normalizes-terminal-spec-draft",
    "drive-normalizes-unresolved-split",
    "adhd-explicit-one-shot",
    "adhd-does-not-carry-over",
    "adhd-safety-exception",
    "implement-auto-decides-unspecified-strategy",
    "implement-respects-explicit-strategy",
    "implement-routes-visible-ui-through-browser-verify",
    "implement-browser-tool-requires-browser-verify",
    "implement-runs-design-preflight-before-ui-edit",
    "implement-non-agent-tools-are-not-delegation",
    "implement-delegation-is-single-level",
    "implement-tdd-follows-user-decision",
    "implement-commits-after-verification",
    "implement-does-not-commit-failing-change",
    "implement-does-not-push",
    "implement-preserves-source-ui-writing-verbatim",
    "implement-blocks-source-current-ui-mismatch",
    "browser-owned-session-cleans-up",
    "browser-attached-session-is-preserved",
    "browser-first-tool-call-owns-lazy-session",
    "browser-refuses-real-payment",
    "browser-guard-mode-is-lightweight",
    "browser-guard-visual-claim-needs-screenshot",
    "browser-verdict-mode-preserves-contract",
    "browser-explicit-invocation-uses-verdict",
    "browser-auto-open-fallback-closes-owned-tabs",
    "browser-chrome-headless-new-first-launch",
    "browser-interactive-auth-only-headed-exception",
    "browser-captures-move-to-tigerkit-ledger",
    "browser-bounds-result-cardinality",
    "grill-me-unifies-caller-modes",
    "grill-me-uses-native-question-tool",
    "grill-me-active-drive-routes-directly",
    "grill-me-blocks-active-drive-autostart",
    "grill-me-does-not-mutate-or-invoke-phases",
    "implement-tdd-requires-observed-red",
    "implement-tdd-uses-public-behavior",
    "implement-non-tdd-still-verifies",
    "implement-reviews-every-standalone-run",
    "implement-review-pins-fixed-point",
    "implement-review-rejects-drift",
    "implement-audits-postcommit-hook-drift",
    "implement-blocks-semantic-hook-drift",
    "implement-allows-bounded-hook-bypass",
    "implement-review-separates-standards-and-spec",
    "implement-review-bounds-independent-reviewer",
    "implement-review-bounds-large-diff-context",
    "implement-diagnoses-unknown-cause-failure",
    "implement-diagnosis-requires-red-capable-loop",
    "implement-diagnosis-does-not-patch-without-reproduction",
    "implement-diagnosis-reruns-original-reproduction",
    "implement-diagnosis-cleans-instrumentation",
    "implement-diagnosis-blocks-missing-seam",
    "implement-active-drive-unit-state",
    "implement-active-drive-non-success-handoff",
    "implement-ordinary-request-does-not-trigger",
    "implement-blocks-standalone-multi-ticket",
    "implement-production-behavior-requires-durable-test",
    "implement-runs-existing-coverage-gate",
    "implement-blocks-testless-production-without-exception",
    "implement-one-ticket-one-commit",
    "implement-reports-bounded-behavior-summary",
    "standalone-diagnose-only-is-read-only",
    "standalone-review-only-is-read-only",
    "implement-review-15-files-800-lines-is-small",
    "implement-review-size-unknown-is-bounded",
    "merge-conflict-requires-active-operation",
    "merge-conflict-finishes-operation",
    "merge-conflict-does-not-abort",
    "merge-conflict-does-not-force-push",
    "reflect-is-report-only",
    "reflect-checks-persistent-memory-prior-art",
    "reflect-separates-adjacent-memory-scope",
    "reflect-bounds-summary-cell-length",
    "reflect-bounds-result-cardinality",
    "reflect-classifies-prevention-owner-and-host-dependency",
    "reflect-drive-applies-exact-existing-ignored-rule",
    "reflect-drive-never-creates-local-rule-target",
    "reflect-drive-rejects-ineligible-target-matrix",
    "reflect-drive-skill-candidate-is-promotion-packet-only",
    "reflect-drive-blocks-target-drift",
    "reflect-classifies-repo-placement",
    "reflect-numbered-summary-target-table",
    "to-spec-does-not-create-tickets",
    "to-spec-structures-bug-evidence",
    "to-spec-preserves-source-ui-writing-verbatim",
    "to-spec-blocks-source-current-ui-mismatch",
    "to-spec-active-drive-preparing-handoff",
    "to-spec-returns-decision-blocker-to-prep",
    "to-spec-records-vertical-slicing-candidate-areas",
    "to-spec-bounds-result-cardinality",
    "to-spec-disposes-prior-art-semantically",
    "to-spec-omits-empty-prior-art",
    "to-spec-blocks-prior-art-conflict",
    "to-tickets-does-not-create-spec",
    "to-tickets-initial-status-is-pending",
    "to-tickets-keeps-one-vertical-bug-slice",
    "to-tickets-preserves-source-ui-writing-verbatim",
    "to-tickets-blocks-source-current-ui-mismatch",
    "to-tickets-active-drive-preparing-handoff",
    "to-tickets-returns-decision-blocker-to-prep",
    "to-tickets-preserves-failed-active-drive-attempt",
    "to-tickets-derives-from-candidate-areas",
    "to-tickets-bounds-result-cardinality",
    "prototype-is-not-production",
    "prototype-web-uses-disposable-variants",
    "prototype-web-toggle-preserves-legibility",
    "prototype-bounds-result-cardinality",
    "grooming-defaults-report-only",
    "grooming-vendor-artifact-remains-report-only",
    "grooming-unknown-ownership-asks-before-proposal",
    "grooming-honors-declared-exclusions",
    "grooming-classifies-repo-placement",
    "grooming-numbered-summary-target-table",
    "grooming-bounds-result-cardinality",
    "legacy-global-state-is-not-scanned",
    "handoff-resume-no-drift-continues",
    "handoff-resume-material-drift-blocks",
    "handoff-bounds-result-cardinality",
    "traceability-preserves-requirement-ids",
    "implement-review-high-risk-is-conditional",
    "browser-accessibility-is-conditional",
    "learn-requires-eval-and-compatibility",
    "learn-implicit-write-awaits-approval",
    "learn-bounds-result-cardinality",
    "handoff-ignores-generic-continue",
    "drive-requires-explicit-start",
    "drive-resumes-preparing-decision-answer",
    "drive-bounds-result-cardinality",
    "drive-response-language-explicit-korean",
    "drive-response-language-explicit-english",
    "drive-risk-profile-low-risk-silent",
    "drive-risk-profile-browser-ui",
    "drive-risk-profile-auth-data",
    "drive-risk-profile-inaccessible-evidence",
    "drive-reflects-once-then-finalizes",
    "drive-skips-unneeded-tickets",
    "drive-keeps-ticket-ledger",
    "drive-preserves-source-ui-writing-verbatim",
    "drive-invalidates-source-current-ui-mismatch",
    "drive-invalidates-unapproved-secondary-axis",
    "drive-reads-complete-remote-source",
    "drive-blocks-unreadable-ui-literal",
    "drive-invalidates-conflicting-ui-literals",
    "drive-commit-command-failure-is-fail",
    "drive-precommit-drift-is-blocked",
    "drive-carries-authorized-ui-writing-change",
    "browser-redacts-sensitive-captures",
    "browser-bounds-instrumented-evidence",
    "browser-instrumentation-residue-failure-is-unverifiable",
    "browser-labels-user-observed-evidence",
    "browser-proves-current-serving-source",
    "browser-classifies-failure-origin",
    "browser-causal-fix-requires-negative-control",
    "handoff-uses-single-snapshot",
    "reflect-placement-regression-matrix",
    "grooming-placement-regression-matrix",
    "reflect-skill-candidate-stays-pending",
    "grooming-semantic-convert-is-proposal-only",
    "learn-is-sole-semantic-skill-writer",
    "drive-bounds-nested-skills",
    "drive-invokes-direct-graph-owners",
    "drive-continues-after-preflight",
    "drive-enforces-exact-procedure-graph",
    "drive-continues-without-receipt-boundary",
    "drive-continues-multi-unit-through-reflection",
    "drive-owns-single-terminal-response",
    "drive-prepares-trivial-task",
    "drive-amends-on-first-new-decision",
    "drive-skips-grill-for-ready-source",
    "drive-blocks-second-amendment",
    "drive-writes-compact-preflight",
    "drive-preserves-preflight-on-write-failure",
    "drive-rejects-preflight-secrets",
    "drive-resumes-from-current-evidence",
    "drive-blocks-repeated-decision-return",
    "drive-commits-per-ticket",
    "drive-runs-final-aggregate-verification",
    "drive-propagates-phase-failure",
    "drive-bounds-corrective-cycle",
    "drive-stops-on-procedure-failure",
    "drive-preserves-valid-diff-on-partial-failure",
    "drive-aggregate-review-boundary",
    "to-spec-routes-ready-state-directly",
    "to-tickets-routes-ledger-state-directly",
    "implement-routes-unit-state-directly",
    "skill-diagnose-reproduces-overtrigger-selection",
    "skill-diagnose-isolates-approval-bypass",
    "skill-diagnose-separates-grader-false-negative",
    "skill-diagnose-classifies-host-loading-difference",
    "skill-diagnose-verifies-efficiency-regression",
    "skill-diagnose-requires-resource-anchor",
    "skill-diagnose-rejects-cheaper-incorrect-candidate",
    "skill-diagnose-does-not-patch-unreproduced-incident",
    "skill-diagnose-bounds-one-theme-and-holdout",
    "skill-diagnose-never-mutates-canonical-path",
    "skill-diagnose-drafts-anonymized-upstream-issue",
    "skill-diagnose-keeps-consumer-drift-local",
    "skill-diagnose-withholds-draft-without-exact-ref",
    "skill-diagnose-withholds-draft-without-two-upstream-runs",
    "skill-diagnose-withholds-draft-without-control-holdout",
    "skill-diagnose-withholds-draft-for-matching-open-issue",
    "skill-diagnose-withholds-draft-for-unverified-closed-regression",
    "skill-diagnose-withholds-draft-when-issue-search-unavailable",
    "skill-diagnose-redacts-private-upstream-evidence",
    "skill-diagnose-bounds-result-cardinality",
    "reflect-hands-off-qualified-skill-incident-once",
    "reflect-skips-diagnosis-without-four-gate",
    "reflect-blocks-repeated-diagnosis-handoff",
    "reflect-response-language-preserves-machine-tokens",
    "merge-conflict-bounds-result-cardinality",
}


def scalar(value: str) -> object:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    return value


def frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML frontmatter; add a leading --- block")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc

    data: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, data)]
    for number, raw in enumerate(lines[1:end], 2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        match = re.match(r"\s*([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if not match:
            raise ValueError(f"line {number}: unsupported frontmatter syntax")
        key, raw_value = match.groups()
        while stack[-1][0] >= indent:
            stack.pop()
        target = stack[-1][1]
        if raw_value in {None, ""}:
            child: dict[str, object] = {}
            target[key] = child
            stack.append((indent, child))
        else:
            target[key] = scalar(raw_value)
    return data, text


def nested(data: dict[str, object], *keys: str) -> object | None:
    value: object = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def parse_latest_changelog_version(text: str) -> str | None:
    match = re.search(r"(?m)^## (\d+\.\d+\.\d+)(?:\s|$)", text)
    return match.group(1) if match else None


def validate_release_version_contract(root: Path) -> list[str]:
    changelog = root / "CHANGELOG.md"
    readme = root / "README.md"
    if not changelog.is_file() or not readme.is_file():
        return []
    version = parse_latest_changelog_version(changelog.read_text(encoding="utf-8"))
    if version is None:
        return ["CHANGELOG.md: add a leading semantic version release heading"]
    if f"`v{version}`" not in readme.read_text(encoding="utf-8"):
        return [f"README.md: immutable snapshot must reference latest changelog release v{version}"]
    return []


def validate_release_alignment(
    main_sha: str,
    peeled_tag_sha: str,
    release_sha: str,
) -> list[str]:
    if len({main_sha, peeled_tag_sha, release_sha}) != 1:
        return ["release provenance: origin/main, peeled tag, and GitHub Release must match"]
    return []


def validate_local_only_workflows(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (
        ".github/workflows/validate.yml",
        ".github/workflows/skills-canary.yml",
        ".github/workflows/skill-evals.yml",
    ):
        if (root / relative).exists():
            errors.append(f"{relative}: remove CI validation; run verification locally")
    return errors


def validate_user_decision_contract(root: Path) -> list[str]:
    errors: list[str] = []
    for skill in sorted(EXPECTED_SKILLS):
        if skill == "tk-adhd":
            continue
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill}: SKILL.md: add the native user-decision question contract")
            continue
        text = path.read_text(encoding="utf-8")
        missing = [token for token in USER_DECISION_CONTRACT_TOKENS if token not in text]
        if missing:
            errors.append(
                f"{skill}: SKILL.md: native user-decision question contract missing "
                + ", ".join(repr(token) for token in missing)
            )
    return errors


def validate_response_language_contract(root: Path) -> list[str]:
    errors: list[str] = []
    for skill in sorted(EXPECTED_SKILLS):
        if skill == "tk-adhd":
            continue
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill}: SKILL.md: add the response-language hard gate")
            continue
        text = path.read_text(encoding="utf-8")
        if text.count(RESPONSE_LANGUAGE_GATE) != 1:
            errors.append(
                f"{skill}: SKILL.md: preserve exactly one complete response-language hard gate"
            )
    return errors


def validate_terminal_summary_contract(root: Path) -> list[str]:
    errors: list[str] = []
    terminal_heading = TERMINAL_SUMMARY_GATE.splitlines()[0]
    language_heading = RESPONSE_LANGUAGE_GATE.splitlines()[0]
    forbidden = ("`Outcome: <one user-facing sentence>`", "## Receipt")
    for skill in sorted(EXPECTED_SKILLS):
        if skill == "tk-adhd":
            continue
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill}: SKILL.md: add the terminal-summary hard gate")
            continue
        text = path.read_text(encoding="utf-8")
        gate = (
            DRIVE_TERMINAL_SUMMARY_GATE
            if skill == "tk-drive"
            else DIRECT_TERMINAL_SUMMARY_GATE
            if skill in DIRECT_GRAPH_SKILLS
            else TERMINAL_SUMMARY_GATE
        )
        complete = text.count(gate) == 1 and text.count(terminal_heading) == 1
        ordered = (
            complete
            and text.count(language_heading) == 1
            and text.index(terminal_heading) < text.index(language_heading)
        )
        if not complete or not ordered or any(token in text for token in forbidden):
            errors.append(
                f"{skill}: SKILL.md: preserve one ordered terminal-summary hard gate "
                "and remove terminal receipt rendering"
            )
    return errors


def validate_drive_graph_contract(
    root: Path,
    edges: tuple[tuple[str, str, str, str, str, str], ...] = DRIVE_GRAPH_EDGES,
) -> list[str]:
    errors: list[str] = []
    for index, edge in enumerate(edges, 1):
        if len(edge) != 6:
            errors.append(f"drive graph edge {index}: expected six fields")
            continue
        source, target, entry, success, failure, next_edge = edge
        for node in (source, target):
            if node not in DRIVE_GRAPH_NODES:
                errors.append(f"drive graph edge {index}: unknown node {node!r}")
        if not all(value.strip() for value in (entry, success, failure, next_edge)):
            errors.append(f"drive graph edge {index}: missing terminal condition")
        if source in {
            "tk-drive:finalization",
            "tk-drive:non-success-finalization",
        } or target == "tk-drive:preflight":
            errors.append(f"drive graph edge {index}: forbidden cycle")
        for next_node in next_edge.split("|"):
            if next_node != "terminal" and next_node not in DRIVE_GRAPH_NODES:
                errors.append(
                    f"drive graph edge {index}: unknown next node {next_node!r}"
                )

    pair_list = [(edge[0], edge[1]) for edge in edges if len(edge) == 6]
    actual_pairs = set(pair_list)
    expected_pairs = {(edge[0], edge[1]) for edge in DRIVE_GRAPH_EDGES}
    if len(pair_list) != len(actual_pairs):
        errors.append("drive graph: duplicate edge is ambiguous")
    if actual_pairs != expected_pairs:
        errors.append("drive graph: edge set differs from the canonical direct graph")

    adjacency: dict[str, set[str]] = {node: set() for node in DRIVE_GRAPH_NODES}
    for source, target in actual_pairs:
        if source in adjacency and target in adjacency:
            adjacency[source].add(target)

    active: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        visited.add(node)
        active.append(node)
        for target in adjacency[node]:
            if target not in visited:
                visit(target)
                continue
            if target not in active:
                continue
            start = active.index(target)
            cycle_nodes = active[start:] + [target]
            cycle_edges = set(zip(cycle_nodes, cycle_nodes[1:]))
            if not cycle_edges.issubset(DRIVE_ALLOWED_LOOP_EDGES):
                errors.append(
                    "drive graph: forbidden cycle "
                    + " -> ".join(cycle_nodes)
                )
        active.pop()

    for node in sorted(DRIVE_GRAPH_NODES):
        if node not in visited:
            visit(node)

    drive = root / "skills/tk-drive/SKILL.md"
    phases = root / "skills/tk-drive/references/phases.md"
    for path, label in ((drive, str(drive.relative_to(root))), (phases, str(phases.relative_to(root)))):
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        required = (
            "tk-drive preflight",
            "tk-grill-me",
            "tk-to-spec",
            "tk-to-tickets",
            "tk-implement",
            "aggregate verification",
            "tk-reflect",
            "tk-drive finalization",
            "tk-drive non-success finalization",
            "entry",
            "success",
            "failure",
            "next",
        )
        missing = [token for token in required if token not in text.casefold()]
        if missing:
            errors.append(f"{label}: incomplete direct graph contract ({', '.join(missing)})")
    return errors


def validate_prepared_drive_contract(root: Path) -> list[str]:
    errors: list[str] = []
    drive = root / "skills/tk-drive/SKILL.md"
    phases = root / "skills/tk-drive/references/phases.md"
    for path, label in (
        (drive, "skills/tk-drive/SKILL.md"),
        (phases, "skills/tk-drive/references/phases.md"),
    ):
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing_stage = [token for token in DRIVE_STAGE_TOKENS if token not in text]
        if missing_stage:
            errors.append(
                f"{label}: preserve Preparing-to-Executing stage ownership "
                f"({', '.join(missing_stage)})"
            )
        normalized = " ".join(text.casefold().split())
        missing_correction = [
            token
            for token in DRIVE_CORRECTIVE_BOUND_TOKENS
            if token not in normalized
        ]
        if missing_correction:
            errors.append(
                f"{label}: preserve the three-cycle corrective boundary "
                f"({', '.join(missing_correction)})"
            )
    return errors


def validate_reflect_ignored_target_contract(root: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "skills/tk-reflect/SKILL.md": (
            "exact pre-existing ignored `repo rule`",
            "skill-local script",
        ),
        "skills/tk-reflect/references/drive-optimistic.md": (
            "drive-start implementation ledger",
            "untracked, and ignored",
            "Tracked, unignored, new, symlinked, external, changed-since-baseline",
            "`scripts/ignored_rule_apply.py`",
            "mode-0600",
            "atomically replaces",
            "restores the exact before-image",
        ),
        "skills/tk-reflect/scripts/ignored_rule_apply.py": (
            "git\", \"ls-files",
            "git\", \"check-ignore",
            "os.replace",
            "reflect-backup",
            "exact rollback verified",
        ),
        "skills/tk-reflect/scripts/test_ignored_rule_apply.py": (
            "test_applies_existing_ignored_target_with_secure_backup",
            "test_rejects_tracked_target_before_write",
            "test_rejects_new_external_symlink_and_ambiguous_targets",
            "test_rejects_target_changed_since_baseline",
            "test_failed_validation_restores_exact_before_image",
        ),
    }
    for relative, tokens in required.items():
        path = root / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [token for token in tokens if token not in text]
        if missing:
            errors.append(
                f"{relative}: preserve exact ignored-target reflection safety "
                f"({', '.join(missing)})"
            )
    reference = root / "skills/tk-reflect/references/drive-optimistic.md"
    text = reference.read_text(encoding="utf-8") if reference.is_file() else ""
    for forbidden in ("## Tracked target", "Create one separate commit"):
        if forbidden in text:
            errors.append(
                "skills/tk-reflect/references/drive-optimistic.md: "
                f"remove tracked-target auto-apply contract {forbidden!r}"
            )
    return errors


def validate_continuation_boundary(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, tokens in CONTINUATION_BOUNDARY_TOKENS.items():
        path = root / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [token for token in tokens if token not in text]
        if missing:
            errors.append(
                f"{relative}: distinguish prompt-directed continuation from a "
                f"runtime workflow engine ({', '.join(missing)})"
            )
    return errors


def validate_browser_preflight_contract(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (
        "skills/tk-drive/SKILL.md",
        "skills/tk-drive/references/phases.md",
    ):
        path = root / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [token for token in BROWSER_PREFLIGHT_TOKENS if token not in text]
        if missing:
            errors.append(
                f"{relative}: preserve conditional browser strategy preflight "
                f"({', '.join(missing)})"
            )
    return errors


def validate_single_drive_adhd_contract(root: Path) -> list[str]:
    errors: list[str] = []
    if (root / "skills" / "tk-prep").exists():
        errors.append("skills/tk-prep: remove the public preparation skill surface")

    adhd_path = root / "skills" / "tk-adhd" / "SKILL.md"
    adhd = adhd_path.read_text(encoding="utf-8") if adhd_path.is_file() else ""
    missing = [token for token in ADHD_CONTRACT_TOKENS if token not in adhd]
    if missing:
        errors.append(
            "skills/tk-adhd/SKILL.md: preserve explicit adapted one-shot ADHD utility contract "
            + ", ".join(repr(token) for token in missing)
        )
    forbidden = [token for token in ADHD_FORBIDDEN_TOKENS if token in adhd]
    if forbidden:
        errors.append(
            "skills/tk-adhd/SKILL.md: remove persistent ADHD-mode state "
            + ", ".join(repr(token) for token in forbidden)
        )

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    if "tk-prep" in readme_text:
        errors.append("README.md: remove the public tk-prep invocation surface")

    shared_heading = "### 🔴 HARD GATE · actionable user output"
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        if shared_heading in path.read_text(encoding="utf-8"):
            errors.append(
                f"{path.relative_to(root)}: remove the shared ADHD-oriented output gate"
            )
    return errors


def validate_unified_grill_contract(root: Path) -> list[str]:
    errors: list[str] = []
    split = root / "skills" / "tk-grilling"
    if split.exists():
        errors.append(
            "skills/tk-grilling: merge the boundary-less duplicate procedure into tk-grill-me"
        )

    grill_path = root / "skills" / "tk-grill-me" / "SKILL.md"
    grill = grill_path.read_text(encoding="utf-8") if grill_path.is_file() else ""
    required = (
        "one evidence-first decision procedure",
        "`standalone`",
        "`active drive`",
        "continues directly to the next applicable procedure",
        "Do not split the same decision procedure into another skill",
    )
    missing = [token for token in required if token not in grill]
    if missing:
        errors.append(
            "skills/tk-grill-me/SKILL.md: preserve unified standalone/active-drive "
            "decision ownership (" + ", ".join(missing) + ")"
        )

    drive_path = root / "skills" / "tk-drive" / "SKILL.md"
    drive = drive_path.read_text(encoding="utf-8") if drive_path.is_file() else ""
    if "`tk-grill-me`" not in drive:
        errors.append(
            "skills/tk-drive/SKILL.md: name tk-grill-me as the exact decision edge"
        )
    return errors


def validate_compact_preflight_contract(root: Path) -> list[str]:
    errors: list[str] = []
    obsolete = (
        "skills/tk-drive/references/manifest.md",
        "skills/tk-drive/scripts/prep_manifest.py",
        "skills/tk-drive/scripts/prep_state.py",
        "skills/tk-drive/scripts/record_eval_event.py",
        "skills/tk-drive/scripts/test_prep_manifest.py",
        "skills/tk-drive/scripts/test_prep_state.py",
        "skills/tk-drive/scripts/test_record_eval_event.py",
    )
    for relative in obsolete:
        if (root / relative).exists():
            errors.append(f"{relative}: remove obsolete drive lifecycle machinery")

    required = {
        "skills/tk-drive/scripts/preflight.py": (
            "TOP_KEYS",
            "FORBIDDEN_KEYS",
            "os.replace",
            "is_symlink",
            "parse_preflight(reread)",
            "choose_resume_action",
            "browser_identity_action",
        ),
        "skills/tk-drive/references/preflight.md": (
            "Allowed fields",
            "secret-free",
            "Evidence-derived resume",
            "stored cursor",
        ),
    }
    for relative, tokens in required.items():
        path = root / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [token for token in tokens if token not in text]
        if missing:
            errors.append(
                f"{relative}: incomplete compact preflight contract "
                f"({', '.join(missing)})"
            )

    for skill in sorted(DIRECT_GRAPH_SKILLS - {"tk-drive"}):
        path = root / "skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for token in (
            "`Return to: tk-drive`",
            "`Outstanding transition`",
            "Keep phase receipts as internal handoff envelopes",
        ):
            if token in text:
                errors.append(f"{path.relative_to(root)}: remove active return-envelope contract")
                break
    return errors


def validate_learning_loop_contract(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, tokens in LEARNING_LOOP_TOKENS.items():
        path = root / relative
        text = " ".join(path.read_text(encoding="utf-8").split()) if path.is_file() else ""
        missing = [token for token in tokens if token not in text]
        if missing:
            errors.append(
                f"{relative}: preserve bounded learning-loop ownership "
                f"({', '.join(missing)})"
            )
    return errors


def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = path.parent
    label = skill_dir.name
    try:
        data, text = frontmatter(path)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"{label}: {path.relative_to(ROOT)}: {exc}"], []

    name = data.get("name")
    description = data.get("description")
    kind = nested(data, "metadata", "tigerkit", "kind")
    origin = nested(data, "metadata", "tigerkit", "origin")
    relationship = nested(data, "metadata", "tigerkit", "relationship")

    unknown_fields = sorted(set(data) - CORE_FRONTMATTER_FIELDS - HOST_EXTENSION_FIELDS)
    if unknown_fields:
        errors.append(f"{label}: SKILL.md frontmatter: unknown top-level fields: {', '.join(unknown_fields)}")

    if not isinstance(name, str) or not name:
        errors.append(f"{label}: SKILL.md field name: add a non-empty name")
    elif name != label:
        errors.append(f"{label}: SKILL.md field name: use directory name {label!r}")
    if isinstance(name, str) and (not name.startswith("tk-") or not KEBAB.fullmatch(name)):
        errors.append(f"{label}: SKILL.md field name: use tk- prefixed kebab-case")
    if isinstance(name, str) and len(name) > 64:
        errors.append(f"{label}: SKILL.md field name: keep within 64 characters")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: SKILL.md field description: add a non-empty description")
    elif len(description) > 1024:
        errors.append(f"{label}: SKILL.md field description: keep within 1024 characters")
    if not isinstance(kind, str) or kind not in KINDS:
        errors.append(f"{label}: metadata.tigerkit.kind: use one of {sorted(KINDS)}")
    elif isinstance(description, str) and not description.startswith(f"{INVOCATION_LABELS[kind]} "):
        errors.append(
            f"{label}: SKILL.md field description: prefix with {INVOCATION_LABELS[kind]!r}"
        )
    if label in USER_INVOKED_SKILLS and kind != "user-invoked":
        errors.append(f"{label}: metadata.tigerkit.kind: expected user-invoked")
    if label in HYBRID_SKILLS and kind != "hybrid":
        errors.append(f"{label}: metadata.tigerkit.kind: expected hybrid")
    if relationship not in RELATIONSHIPS:
        errors.append(f"{label}: metadata.tigerkit.relationship: use one of {sorted(RELATIONSHIPS)}")
    if origin != "tigerkit" and not nested(data, "metadata", "tigerkit", "upstream-skill"):
        errors.append(f"{label}: metadata.tigerkit.upstream-skill: required for external origins")

    openai = skill_dir / "agents" / "openai.yaml"
    openai_text = openai.read_text(encoding="utf-8") if openai.is_file() else ""
    disabled = data.get("disable-model-invocation") is True
    implicit_blocked = "allow_implicit_invocation: false" in openai_text
    if kind == "user-invoked":
        argument_hint = data.get("argument-hint")
        if not isinstance(argument_hint, str) or not argument_hint.strip():
            errors.append(f"{label}: argument-hint: add the explicit invocation input shape")
        if not disabled:
            errors.append(f"{label}: disable-model-invocation: set true for user-invoked skills")
        if not openai.is_file():
            errors.append(f"{label}: agents/openai.yaml: add Codex interface policy")
        else:
            for needle in (
                "interface:",
                "display_name:",
                "short_description:",
                "policy:",
                "allow_implicit_invocation: false",
            ):
                if needle not in openai_text:
                    errors.append(f"{label}: agents/openai.yaml: add {needle}")
            if 'short_description: "[user] ' not in openai_text:
                errors.append(f"{label}: agents/openai.yaml: prefix short_description with '[user]'")
    elif kind == "hybrid":
        if disabled:
            errors.append(f"{label}: disable-model-invocation: remove implicit-invocation block")
        if implicit_blocked:
            errors.append(f"{label}: agents/openai.yaml: remove allow_implicit_invocation: false")

    forbidden = {
        "commands/": "remove command-runtime references",
        "~/.tigerkit": "use repo-local .tigerkit scratch only",
        "/tk:": "use tk-* Agent Skill invocation names",
        "repo-root/scripts/": "move runtime code into this skill directory",
        "scripts/tigerkit_state.py": "remove legacy state helper dependency",
    }
    for token, fix in forbidden.items():
        if token in text:
            errors.append(f"{label}: SKILL.md: forbidden {token!r}; {fix}")

    normalized_text = " ".join(text.split())
    missing_budget = [
        token
        for token in RESULT_BUDGET_TOKENS.get(label, ())
        if token not in normalized_text
    ]
    if missing_budget:
        errors.append(
            f"{label}: SKILL.md: bounded result contract missing "
            + ", ".join(repr(token) for token in missing_budget)
        )

    for target in LINK.findall(text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target) or target.startswith("#"):
            continue
        resolved = (skill_dir / target).resolve()
        if resolved != skill_dir.resolve() and skill_dir.resolve() not in resolved.parents:
            errors.append(f"{label}: SKILL.md link {target!r}: keep references inside the skill directory")
        elif not resolved.exists():
            errors.append(f"{label}: SKILL.md link {target!r}: create the referenced file or remove the link")

    non_empty = sum(bool(line.strip()) for line in text.splitlines())
    limit = 250 if kind == "hybrid" else 120
    if non_empty > limit:
        warnings.append(
            f"{label}: SKILL.md: {non_empty} non-empty lines; move detail into references/ "
            f"(warning limit {limit})"
        )
    return errors, warnings


def validate_runtime_scratch(root: Path) -> list[str]:
    scratch = root / ".tigerkit"
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "--", ".tigerkit"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        tracked = None

    if tracked is not None and tracked.returncode == 0:
        if tracked.stdout.strip():
            return [".tigerkit: remove tracked TigerKit runtime scratch"]
        return []
    if scratch.exists():
        return [".tigerkit: remove TigerKit runtime scratch from packaged repository"]
    return []


def validate_repository_contract() -> list[str]:
    errors: list[str] = []
    required_files = (
        "README.md",
        "MIGRATION.md",
        "CHANGELOG.md",
        "NOTICE.md",
        "LICENSE",
        ".gitignore",
        "scripts/validate_skills.py",
        "scripts/run_skill_evals.py",
        "scripts/sync_eval_compat.py",
        "evals/trigger-cases.yaml",
        "evals/behavior-cases.yaml",
        "evals/catalog-routing.json",
        "evals/prompts/skill-diagnostic.md",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"{relative}: required TigerKit 21.0.5 repository file is missing")
    errors.extend(validate_local_only_workflows(ROOT))
    errors.extend(validate_skill_language(ROOT))
    errors.extend(validate_user_decision_contract(ROOT))
    errors.extend(validate_terminal_summary_contract(ROOT))
    errors.extend(validate_drive_graph_contract(ROOT))
    errors.extend(validate_prepared_drive_contract(ROOT))
    errors.extend(validate_browser_preflight_contract(ROOT))
    errors.extend(validate_single_drive_adhd_contract(ROOT))
    errors.extend(validate_unified_grill_contract(ROOT))
    errors.extend(validate_compact_preflight_contract(ROOT))
    errors.extend(validate_reflect_ignored_target_contract(ROOT))
    errors.extend(validate_continuation_boundary(ROOT))
    errors.extend(validate_learning_loop_contract(ROOT))
    errors.extend(validate_response_language_contract(ROOT))
    for relative in (".claude-plugin", "commands", "hooks", "docs/tigerkit", "package.json"):
        if (ROOT / relative).exists():
            errors.append(f"{relative}: remove legacy/runtime surface from TigerKit 21.0.5")
    errors.extend(validate_runtime_scratch(ROOT))
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    if ".tigerkit/" not in ignored.splitlines():
        errors.append(".gitignore: document TigerKit repo-local scratch with .tigerkit/")
    required_text = {
        "README.md": (
            "TigerKit 21.0.5",
            "15",
            "Claude Code",
            "Codex",
            "Hermes Agent",
            "npx skills add",
            "사용 시나리오",
        ),
        "MIGRATION.md": (
            "TigerKit 21.0.0",
            "Removed Skills",
            "model-only",
            "hybrid",
            "CONTEXT.md",
            "Phase ownership",
            "one ticket",
        ),
        "CHANGELOG.md": ("13", "hybrid", "v18.0.4"),
        "NOTICE.md": (
            "mattpocock/skills",
            "mizchi/skills",
            "empirical-prompt-tuning",
            "relationship: adapted",
            "Behavior merged from removed adapted skills",
            "MIT License",
        ),
        "skills/tk-browser-verify/SKILL.md": (
            "## 🔴 HARD GATE · Chrome `--headless=new`",
            "contain the exact token `--headless=new`",
            "do not open a headed browser",
            "headless launch failure",
            "user must directly complete",
            "restart the same binary and `user-data-dir`",
            "`Sensitivity: normal | sensitive`",
            "`Redaction: N/A | verified | failed | unverifiable`",
            "`Residue check: verified | unverifiable`",
        ),
        "skills/tk-browser-verify/references/environment.md": (
            "process arguments prove exact `--headless=new`",
            "Before a CDP provider",
            "do not fall back headed",
            "Visible requests, headless failure",
            "prove lock release",
        ),
        "skills/tk-reflect/SKILL.md": (
            "Assign `RF-01`, `RF-02`, ... once in discovery order",
            "In chat, emit only",
            "| ID | Candidate | Action | Target | Why |",
            "Only on an explicit report-artifact request",
            "no raw logs, transcripts, diff excerpts",
            "Only `tk-learn` creates a new skill or semantically updates/merges one",
            "### Conditional Agent Skill diagnosis",
        ),
        "skills/tk-skill-diagnose/SKILL.md": (
            "## Intake gate",
            "Reproduced | Not reproduced |",
            "## Efficiency gate",
            "Never semantically mutate the canonical source skill",
            "upstream-draft-ready",
            "### 🔴 HARD GATE · response language",
        ),
        "scripts/run_skill_evals.py": (
            '"--diagnose"',
            '"--diagnostic-scenario-limit"',
            '"--diagnostic-max-iterations"',
            '"normal-records.json"',
            '"diagnostic-records.json"',
            '"diagnostic-ledger.json"',
        ),
        "evals/prompts/skill-diagnostic.md": (
            "TIGERKIT_DIAGNOSTIC_START",
            "TIGERKIT_DIAGNOSTIC_END",
            "Do not guess an expected answer",
        ),
        "skills/tk-grooming/SKILL.md": (
            "Assign `GR-01`, `GR-02`, ... once in first-identification order",
            "Lead with one `## Disposition`",
            "| ID | Item | Action | Target | Basis |",
            "Add `## Exceptions` only",
            "`report-only | applied`",
            "rule-to-skill `convert`, workflow `split`, and semantic",
        ),
        "skills/tk-learn/SKILL.md": (
            "sole TigerKit writer",
            "current-host native repo/user skill paths",
            "fan out/sync across hosts",
        ),
        "skills/tk-drive/SKILL.md": (
            "selects `/tk-drive`, `$tk-drive`, or the host skill",
            "### 🔴 HARD GATE · source UI writing",
            "`authorized change`",
        ),
        "skills/tk-handoff/SKILL.md": (
            "only resume snapshot",
            "Never create `.tigerkit/work-map.md`",
            "Treat an existing work-map as legacy scratch",
        ),
        "skills/tk-reflect/references/repository-placement.md": (
            "closed safety token set",
            "default sibling threshold is `15`",
            "current-host native paths",
        ),
        "skills/tk-grooming/references/repository-placement.md": (
            "closed safety token set",
            "default sibling threshold is `15`",
            "current-host native paths",
        ),
    }
    for relative, needles in required_text.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{relative}: document required release contract {needle!r}")
    placement_refs = (
        ROOT / "skills/tk-reflect/references/repository-placement.md",
        ROOT / "skills/tk-grooming/references/repository-placement.md",
    )
    if all(path.is_file() for path in placement_refs) and (
        placement_refs[0].read_text(encoding="utf-8")
        != placement_refs[1].read_text(encoding="utf-8")
    ):
        errors.append(
            "repository placement rubric: keep tk-reflect and tk-grooming references identical"
        )
    for directory in SKILLS.glob("*/**"):
        if directory.is_dir() and directory.name in {"references", "scripts", "agents"} and not any(directory.iterdir()):
            errors.append(f"{directory.relative_to(ROOT)}: remove empty optional directory")
    errors.extend(validate_release_version_contract(ROOT))
    return errors


def validate_skill_language(root: Path) -> list[str]:
    errors: list[str] = []
    for skill in sorted(EXPECTED_SKILLS):
        skill_dir = root / "skills" / skill
        skill_path = skill_dir / "SKILL.md"
        paths = [skill_path, *sorted((skill_dir / "references").glob("*.md"))]
        for path in paths:
            if not path.is_file():
                continue
            in_fence = False
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                prose = "" if in_fence else re.sub(r"`[^`]*`", "", line)
                if HANGUL_SYLLABLE.search(prose):
                    relative = path.relative_to(root)
                    errors.append(
                        f"{relative}:{number}: canonical skill operational prose must be English"
                    )
    return errors


def validate_repo_links() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if (
            ".git" in path.parts
            or ".tigerkit" in path.parts
            or relative.parts[0] in {".agents", ".codex"}
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^(?:[a-z]+:)?//", target) or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken relative link {target!r}")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if (
            ".git" not in path.parts
            and ".tigerkit" not in path.parts
            and relative.parts[0] not in {".agents", ".codex"}
            and path.is_symlink()
            and not path.exists()
        ):
            errors.append(f"{path.relative_to(ROOT)}: broken symlink")
    return errors


def parse_trigger_cases(path: Path) -> tuple[dict[str, dict[str, int]], list[str]]:
    entries: dict[str, dict[str, int]] = {}
    duplicates: list[str] = []
    current: str | None = None
    mode: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- skill: "):
            current = line.removeprefix("- skill: ").strip()
            if current in entries:
                duplicates.append(current)
            entries[current] = {"examples": 0, "nearby": 0, "positive": 0, "negative": 0}
            mode = None
        elif line.strip() in {"examples:", "nearby:", "positive:", "negative:"}:
            mode = line.strip()[:-1]
        elif line.startswith("    - ") and current and mode:
            entries[current][mode] += 1
    return entries, duplicates


def parse_behavior_cases(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    duplicates: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- case: "):
            if current is not None:
                entries.append(current)
            current = {"case": line.removeprefix("- case: ").strip()}
            case = current["case"]
            if case in seen:
                duplicates.append(case)
            seen.add(case)
        elif current is not None and line.startswith("  skill: "):
            current["skill"] = line.removeprefix("  skill: ").strip()
        elif current is not None and line.startswith("  expect: "):
            current["expect"] = line.removeprefix("  expect: ").strip()
    if current is not None:
        entries.append(current)
    return entries, duplicates


def load_json_object(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be an object")
        return None
    return value


def darwin_test_prompt_projection(behavior_data: dict[str, object]) -> list[dict[str, object]]:
    evals = behavior_data.get("evals", [])
    if not isinstance(evals, list):
        return []
    selected = [case for case in evals if isinstance(case, dict) and case.get("darwin") is True]
    return [
        {
            "id": index,
            "prompt": case.get("prompt"),
            "expected": case.get("expected_output"),
        }
        for index, case in enumerate(selected, 1)
    ]


def validate_skill_eval_files(skill_dir: Path, kind: str) -> list[str]:
    errors: list[str] = []
    label = skill_dir.name
    trigger_path = skill_dir / "evals" / "triggers.json"
    behavior_path = skill_dir / "evals" / "evals.json"
    for path in (trigger_path, behavior_path):
        if not path.is_file():
            errors.append(f"{label}: {path.relative_to(skill_dir)}: add executable eval contract")
    if errors:
        return errors

    trigger_data = load_json_object(trigger_path, errors)
    if trigger_data is not None:
        if trigger_data.get("skill") != label:
            errors.append(f"{label}: evals/triggers.json: skill must match directory name")
        if trigger_data.get("kind") != kind:
            errors.append(f"{label}: evals/triggers.json: kind must be {kind}")
        queries = trigger_data.get("queries")
        if not isinstance(queries, list) or not queries:
            errors.append(f"{label}: evals/triggers.json: queries must be a non-empty list")
        else:
            ids: list[str] = []
            splits: set[str] = set()
            split_queries: dict[str, set[str]] = {"train": set(), "validation": set()}
            validation_positive = 0
            validation_negative = 0
            validation_facets: set[str] = set()
            any_positive = False
            any_negative = False
            for index, query in enumerate(queries, 1):
                if not isinstance(query, dict):
                    errors.append(f"{label}: evals/triggers.json: query {index} must be an object")
                    continue
                query_id = query.get("id")
                split = query.get("split")
                text = query.get("query")
                should_trigger = query.get("should_trigger")
                facets = query.get("facets", [])
                if not isinstance(query_id, str) or not query_id:
                    errors.append(f"{label}: evals/triggers.json: query {index} needs id")
                else:
                    ids.append(query_id)
                if split not in {"train", "validation"}:
                    errors.append(f"{label}: evals/triggers.json: query {index} split must be train or validation")
                else:
                    splits.add(split)
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{label}: evals/triggers.json: query {index} needs query text")
                elif split in split_queries:
                    split_queries[split].add(" ".join(text.casefold().split()))
                if not isinstance(should_trigger, bool):
                    errors.append(f"{label}: evals/triggers.json: query {index} should_trigger must be boolean")
                elif should_trigger:
                    any_positive = True
                    if split == "validation":
                        validation_positive += 1
                else:
                    any_negative = True
                    if split == "validation":
                        validation_negative += 1
                if not isinstance(facets, list) or not all(
                    isinstance(facet, str) and facet in HYBRID_TRIGGER_FACETS for facet in facets
                ):
                    errors.append(
                        f"{label}: evals/triggers.json: query {index} facets must use "
                        f"{sorted(HYBRID_TRIGGER_FACETS)}"
                    )
                elif split == "validation":
                    validation_facets.update(facets)
            duplicates = sorted({value for value in ids if ids.count(value) > 1})
            if duplicates:
                errors.append(f"{label}: evals/triggers.json: duplicate query ids: {', '.join(duplicates)}")
            if splits != {"train", "validation"}:
                errors.append(f"{label}: evals/triggers.json: include both train and validation splits")
            overlap = sorted(split_queries["train"] & split_queries["validation"])
            if overlap:
                errors.append(f"{label}: evals/triggers.json: train/validation query overlap")
            if not any_positive or not any_negative:
                errors.append(f"{label}: evals/triggers.json: include trigger and non-trigger queries")
            if kind == "hybrid" and (validation_positive < 8 or validation_negative < 8):
                errors.append(
                    f"{label}: evals/triggers.json: hybrid validation needs at least 8 positive and 8 negative queries"
                )
            if kind == "hybrid" and validation_facets != HYBRID_TRIGGER_FACETS:
                missing_facets = ", ".join(sorted(HYBRID_TRIGGER_FACETS - validation_facets))
                errors.append(
                    f"{label}: evals/triggers.json: hybrid validation is missing query facets: "
                    f"{missing_facets or 'none'}"
                )

    behavior_data = load_json_object(behavior_path, errors)
    if behavior_data is not None:
        if behavior_data.get("skill_name") != label:
            errors.append(f"{label}: evals/evals.json: skill_name must match directory name")
        evals = behavior_data.get("evals")
        if not isinstance(evals, list) or not evals:
            errors.append(f"{label}: evals/evals.json: evals must be a non-empty list")
        else:
            ids: list[str] = []
            paths: set[str] = set()
            for index, case in enumerate(evals, 1):
                if not isinstance(case, dict):
                    errors.append(f"{label}: evals/evals.json: case {index} must be an object")
                    continue
                case_id = case.get("id")
                path_type = case.get("path")
                if not isinstance(case_id, str) or not case_id:
                    errors.append(f"{label}: evals/evals.json: case {index} needs id")
                else:
                    ids.append(case_id)
                if path_type not in {"success", "boundary"}:
                    errors.append(f"{label}: evals/evals.json: case {index} path must be success or boundary")
                else:
                    paths.add(path_type)
                for field in ("prompt", "expected_output"):
                    if not isinstance(case.get(field), str) or not str(case.get(field)).strip():
                        errors.append(f"{label}: evals/evals.json: case {index} needs {field}")
                hosts = case.get("hosts")
                if hosts is not None and (
                    not isinstance(hosts, list)
                    or not hosts
                    or not all(
                        isinstance(host, str) and host in SUPPORTED_EVAL_HOSTS
                        for host in hosts
                    )
                    or len(set(hosts)) != len(hosts)
                ):
                    errors.append(
                        f"{label}: evals/evals.json: case {index} hosts must be "
                        "unique supported hosts"
                    )
                assertions = case.get("assertions")
                if not isinstance(assertions, list) or not assertions:
                    errors.append(f"{label}: evals/evals.json: case {index} needs non-empty assertions")
                else:
                    has_mechanical = False
                    for assertion_index, assertion in enumerate(assertions, 1):
                        if not isinstance(assertion, dict):
                            errors.append(
                                f"{label}: evals/evals.json: case {index} assertion "
                                f"{assertion_index} must be an object"
                            )
                            continue
                        assertion_type = assertion.get("type")
                        if assertion_type == "judge":
                            if not isinstance(assertion.get("criterion"), str) or not str(
                                assertion.get("criterion")
                            ).strip():
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} judge assertion "
                                    f"{assertion_index} needs criterion"
                                )
                            continue
                        if assertion_type not in MECHANICAL_ASSERTION_TYPES:
                            errors.append(
                                f"{label}: evals/evals.json: case {index} assertion "
                                f"{assertion_index} has unknown type {assertion_type!r}"
                            )
                            continue
                        has_mechanical = True
                        if assertion_type == "terminal_status":
                            allowed = assertion.get("allowed")
                            expected = assertion.get("expected")
                            forbidden = assertion.get("forbidden", [])
                            if (allowed is None) == (expected is None):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} terminal_status "
                                    "assertion needs exactly one of expected or allowed"
                                )
                            values = [expected] if expected is not None else allowed
                            if not isinstance(values, list) or not values or not all(
                                isinstance(value, str) and value in TERMINAL_STATUSES
                                for value in values
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} terminal_status "
                                    "values must use the terminal enum"
                                )
                            if not isinstance(forbidden, list) or not all(
                                isinstance(value, str) and value in TERMINAL_STATUSES
                                for value in forbidden
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} terminal_status "
                                    "forbidden values must use the terminal enum"
                                )
                            elif isinstance(values, list) and set(values) & set(forbidden):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} terminal_status "
                                    "expected/allowed and forbidden values must not overlap"
                                )
                        elif assertion_type == "event_order":
                            hosts = assertion.get("hosts")
                            if hosts is not None and (
                                not isinstance(hosts, list)
                                or not hosts
                                or not all(
                                    isinstance(host, str)
                                    and host in SUPPORTED_EVAL_HOSTS
                                    for host in hosts
                                )
                                or len(set(hosts)) != len(hosts)
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_order hosts must be unique supported hosts"
                                )
                            required_match_fields = {
                                "phase_invocation": ("phase",),
                            }
                            for field in ("before", "after"):
                                matcher = assertion.get(field)
                                event_type = (
                                    matcher.get("type")
                                    if isinstance(matcher, dict)
                                    else None
                                )
                                required = (
                                    required_match_fields.get(event_type)
                                    if isinstance(event_type, str)
                                    else None
                                )
                                valid = (
                                    isinstance(matcher, dict)
                                    and event_type in EVENT_TYPES
                                    and required is not None
                                    and all(
                                        isinstance(matcher.get(key), str)
                                        and str(matcher.get(key)).strip()
                                        for key in required
                                    )
                                )
                                if not valid:
                                    errors.append(
                                        f"{label}: evals/evals.json: case {index} "
                                        f"event_order {field} needs a complete phase event matcher"
                                    )
                            forbidden = assertion.get("forbidden_between", [])
                            if not isinstance(forbidden, list) or not forbidden or not all(
                                isinstance(matcher, dict)
                                and isinstance(matcher.get("type"), str)
                                and matcher.get("type") in EVENT_TYPES
                                for matcher in forbidden
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_order forbidden_between needs event matchers"
                                )
                        elif assertion_type == "event_absent":
                            hosts = assertion.get("hosts")
                            if hosts is not None and (
                                not isinstance(hosts, list)
                                or not hosts
                                or not all(
                                    isinstance(host, str)
                                    and host in SUPPORTED_EVAL_HOSTS
                                    for host in hosts
                                )
                                or len(set(hosts)) != len(hosts)
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_absent hosts must be unique supported hosts"
                                )
                            matcher = assertion.get("event")
                            event_type = (
                                matcher.get("type")
                                if isinstance(matcher, dict)
                                else None
                            )
                            required_match_fields = {
                                "phase_invocation": ("phase",),
                                "final_output": ("terminal_status",),
                            }
                            required = (
                                required_match_fields.get(event_type)
                                if isinstance(event_type, str)
                                else None
                            )
                            valid = (
                                isinstance(matcher, dict)
                                and event_type in EVENT_TYPES
                                and required is not None
                                and all(
                                    isinstance(matcher.get(key), str)
                                    and str(matcher.get(key)).strip()
                                    for key in required
                                )
                                and (
                                    event_type != "final_output"
                                    or matcher.get("terminal_status")
                                    in TERMINAL_STATUSES
                                )
                            )
                            if not valid:
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_absent event needs a valid event matcher"
                                )
                        elif assertion_type == "event_count":
                            hosts = assertion.get("hosts")
                            if hosts is not None and (
                                not isinstance(hosts, list)
                                or not hosts
                                or not all(
                                    isinstance(host, str)
                                    and host in SUPPORTED_EVAL_HOSTS
                                    for host in hosts
                                )
                                or len(set(hosts)) != len(hosts)
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_count hosts must be unique supported hosts"
                                )
                            matcher = assertion.get("event")
                            valid_matcher = (
                                isinstance(matcher, dict)
                                and matcher.get("type") == "phase_invocation"
                                and isinstance(matcher.get("phase"), str)
                                and str(matcher.get("phase")).strip()
                            )
                            minimum = assertion.get("min")
                            maximum = assertion.get("max")
                            valid_minimum = (
                                minimum is None
                                or (
                                    isinstance(minimum, int)
                                    and not isinstance(minimum, bool)
                                    and minimum >= 0
                                )
                            )
                            valid_maximum = (
                                maximum is None
                                or (
                                    isinstance(maximum, int)
                                    and not isinstance(maximum, bool)
                                    and maximum >= 0
                                )
                            )
                            if (
                                not valid_matcher
                                or not valid_minimum
                                or not valid_maximum
                                or (minimum is None and maximum is None)
                                or (
                                    isinstance(minimum, int)
                                    and isinstance(maximum, int)
                                    and minimum > maximum
                                )
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "event_count needs a phase matcher and valid min/max"
                                )
                        elif assertion_type in {
                            "path_exists",
                            "path_absent",
                            "path_text_contains",
                            "path_text_absent",
                        }:
                            relative = assertion.get("path")
                            if (
                                not isinstance(relative, str)
                                or not relative
                                or Path(relative).is_absolute()
                                or ".." in Path(relative).parts
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} path assertion "
                                    "needs a safe relative path"
                                )
                            if assertion_type.startswith("path_text_") and not (
                                isinstance(assertion.get("text"), str)
                                and str(assertion.get("text")).strip()
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} path text "
                                    "assertion needs text"
                                )
                        elif assertion_type in {
                            "output_contains",
                            "output_absent",
                            "git_diff_contains",
                            "git_diff_absent",
                        }:
                            if not isinstance(assertion.get("text"), str) or not str(
                                assertion.get("text")
                            ).strip():
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    f"{assertion_type} assertion needs text"
                                )
                        elif assertion_type == "changed_paths_equal":
                            paths_value = assertion.get("paths")
                            if not isinstance(paths_value, list) or not all(
                                isinstance(relative, str)
                                and relative
                                and not Path(relative).is_absolute()
                                and ".." not in Path(relative).parts
                                for relative in paths_value
                            ):
                                errors.append(
                                    f"{label}: evals/evals.json: case {index} "
                                    "changed_paths_equal needs safe relative paths"
                                )
                    if not has_mechanical:
                        errors.append(
                            f"{label}: evals/evals.json: case {index} needs at least one "
                            "mechanical assertion; judge-only prose is not release evidence"
                        )
                if "safety" in case and not isinstance(case.get("safety"), bool):
                    errors.append(f"{label}: evals/evals.json: case {index} safety must be boolean")
                if "darwin" in case and not isinstance(case.get("darwin"), bool):
                    errors.append(f"{label}: evals/evals.json: case {index} darwin must be boolean")
                files = case.get("files", [])
                if not isinstance(files, list):
                    errors.append(f"{label}: evals/evals.json: case {index} files must be a list")
                else:
                    for relative in files:
                        if not isinstance(relative, str) or not (skill_dir / relative).is_file():
                            errors.append(f"{label}: evals/evals.json: case {index} missing input file {relative!r}")
            duplicates = sorted({value for value in ids if ids.count(value) > 1})
            if duplicates:
                errors.append(f"{label}: evals/evals.json: duplicate case ids: {', '.join(duplicates)}")
            if paths != {"success", "boundary"}:
                errors.append(f"{label}: evals/evals.json: include success and boundary paths")
        projection = darwin_test_prompt_projection(behavior_data)
        compatibility_path = skill_dir / "test-prompts.json"
        if label in EXPECTED_SKILLS and len(projection) != 2:
            errors.append(f"{label}: evals/evals.json: select exactly 2 Darwin compatibility prompts")
        if compatibility_path.is_file():
            try:
                compatibility = json.loads(compatibility_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"{label}: test-prompts.json: invalid JSON: {exc}")
            else:
                if compatibility != projection:
                    errors.append(f"{label}: test-prompts.json: regenerate from evals/evals.json Darwin cases")
        elif label in EXPECTED_SKILLS:
            errors.append(f"{label}: test-prompts.json: add Darwin compatibility projection")
    return errors


def validate_catalog_routing(root: Path) -> list[str]:
    path = root / "evals" / "catalog-routing.json"
    errors: list[str] = []
    data = load_json_object(path, errors) if path.is_file() else None
    if data is None:
        if not path.is_file():
            errors.append("evals/catalog-routing.json: add catalog-level routing cases")
        return errors
    if data.get("version") != 1:
        errors.append("evals/catalog-routing.json: version must be 1")
    hosts = data.get("critical_hosts")
    if (
        not isinstance(hosts, list)
        or not all(isinstance(host, str) for host in hosts)
        or set(hosts) != SUPPORTED_EVAL_HOSTS
    ):
        errors.append(
            "evals/catalog-routing.json: critical_hosts must cover claude-code, codex, and hermes-agent"
        )
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("evals/catalog-routing.json: cases must be a non-empty list")
        return errors
    ids: list[str] = []
    boundaries: set[str] = set()
    critical_boundaries: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"evals/catalog-routing.json: case {index} must be an object")
            continue
        case_id = case.get("id")
        boundary = case.get("boundary")
        prompt = case.get("prompt")
        focus_skill = case.get("focus_skill")
        selected_skill = case.get("expected_selected_skill")
        critical = case.get("critical")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"evals/catalog-routing.json: case {index} needs id")
        else:
            ids.append(case_id)
        if boundary not in CATALOG_ROUTING_BOUNDARIES:
            errors.append(
                f"evals/catalog-routing.json: case {case_id or index} has unknown boundary"
            )
        else:
            boundaries.add(str(boundary))
            if critical is True:
                critical_boundaries.add(str(boundary))
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"evals/catalog-routing.json: case {case_id or index} needs prompt")
        if focus_skill not in EXPECTED_SKILLS:
            errors.append(
                f"evals/catalog-routing.json: case {case_id or index} has unknown focus_skill"
            )
        if selected_skill is not None and selected_skill not in EXPECTED_SKILLS:
            errors.append(
                f"evals/catalog-routing.json: case {case_id or index} has unknown expected_selected_skill"
            )
        if not isinstance(critical, bool):
            errors.append(
                f"evals/catalog-routing.json: case {case_id or index} critical must be boolean"
            )
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        errors.append(
            "evals/catalog-routing.json: duplicate case ids: " + ", ".join(duplicates)
        )
    if boundaries != CATALOG_ROUTING_BOUNDARIES:
        errors.append(
            "evals/catalog-routing.json: cover all required routing boundaries"
        )
    if critical_boundaries != CATALOG_ROUTING_BOUNDARIES:
        errors.append(
            "evals/catalog-routing.json: critical subset must cover all required routing boundaries"
        )
    return errors


def validate_eval_fixtures() -> list[str]:
    errors: list[str] = []
    trigger_path = ROOT / "evals" / "trigger-cases.yaml"
    behavior_path = ROOT / "evals" / "behavior-cases.yaml"
    if not trigger_path.is_file():
        errors.append("evals/trigger-cases.yaml: add trigger fixtures")
    else:
        trigger_text = trigger_path.read_text(encoding="utf-8")
        if "Static contract fixtures." not in trigger_text or "do not execute models" not in trigger_text:
            errors.append("evals/trigger-cases.yaml: describe static non-model fixtures")
        entries, duplicates = parse_trigger_cases(trigger_path)
        if duplicates:
            errors.append(f"evals/trigger-cases.yaml: duplicate skills: {', '.join(sorted(set(duplicates)))}")
        if set(entries) != EXPECTED_SKILLS:
            errors.append(
                "evals/trigger-cases.yaml: cover exactly "
                f"the {len(EXPECTED_SKILLS)} canonical skills"
            )
        for skill, values in sorted(entries.items()):
            if skill in USER_INVOKED_SKILLS:
                if values["examples"] < 2:
                    errors.append(f"evals/trigger-cases.yaml: {skill} needs at least 2 examples")
                if values["positive"] or values["negative"]:
                    errors.append(f"evals/trigger-cases.yaml: {skill} user-invoked entry must not use positive/negative")
            elif skill in HYBRID_SKILLS:
                if values["positive"] < 3 or values["negative"] < 3:
                    errors.append(f"evals/trigger-cases.yaml: {skill} needs positive and negative counts of at least 3")
                if values["examples"] or values["nearby"]:
                    errors.append(f"evals/trigger-cases.yaml: {skill} hybrid entry must use positive/negative")
    if not behavior_path.is_file():
        errors.append("evals/behavior-cases.yaml: add behavior-boundary fixtures")
    else:
        behavior_text = behavior_path.read_text(encoding="utf-8")
        if "Static contract fixtures." not in behavior_text or "do not execute models" not in behavior_text:
            errors.append("evals/behavior-cases.yaml: describe static non-model fixtures")
        entries, duplicates = parse_behavior_cases(behavior_path)
        if duplicates:
            errors.append(f"evals/behavior-cases.yaml: duplicate cases: {', '.join(sorted(set(duplicates)))}")
        cases = {entry.get("case", "") for entry in entries}
        missing = sorted(REQUIRED_BEHAVIOR_CASES - cases)
        if missing:
            errors.append(f"evals/behavior-cases.yaml: missing required cases: {', '.join(missing)}")
        for index, entry in enumerate(entries, 1):
            missing_fields = [field for field in ("case", "skill", "expect") if not entry.get(field)]
            if missing_fields:
                errors.append(
                    f"evals/behavior-cases.yaml: entry {index} missing fields: {', '.join(missing_fields)}"
                )
            skill = entry.get("skill")
            if skill and skill not in EXPECTED_SKILLS:
                errors.append(f"evals/behavior-cases.yaml: {entry.get('case', index)} references unknown skill {skill}")
    for skill in sorted(EXPECTED_SKILLS):
        kind = "user-invoked" if skill in USER_INVOKED_SKILLS else "hybrid"
        errors.extend(validate_skill_eval_files(SKILLS / skill, kind))
    errors.extend(validate_catalog_routing(ROOT))
    return errors


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--links-only":
        link_errors = validate_repo_links()
        if link_errors:
            for error in link_errors:
                print(f"ERROR: {error}")
            return 1
        print("Validated Markdown relative links with 0 errors.")
        return 0
    paths = sorted(SKILLS.glob("*/SKILL.md"))
    errors: list[str] = []
    warnings: list[str] = []
    actual_skills = {path.parent.name for path in paths}
    missing = sorted(EXPECTED_SKILLS - actual_skills)
    extra = sorted(actual_skills - EXPECTED_SKILLS)
    if missing:
        errors.append(f"skills: missing canonical skills: {', '.join(missing)}")
    if extra:
        errors.append(f"skills: remove non-canonical skill directories: {', '.join(extra)}")
    if not paths:
        errors.append("skills: no skills/*/SKILL.md files found")
    errors.extend(validate_repository_contract())
    errors.extend(validate_repo_links())
    errors.extend(validate_eval_fixtures())
    for path in paths:
        skill_errors, skill_warnings = validate_skill(path)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(errors)} errors.")
        return 1
    print(f"Validated Agent Skills portable core fields for {len(paths)} skills.")
    print(
        f"Validated TigerKit host extension profiles: "
        f"{len(USER_INVOKED_SKILLS)} user-invoked, {len(HYBRID_SKILLS)} hybrid."
    )
    print(f"Validated {len(paths)} skills with 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
