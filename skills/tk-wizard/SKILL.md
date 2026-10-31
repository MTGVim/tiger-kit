---
name: tk-wizard
description: "[user/auto] 사용자가 직접 수행해야 하는 provisioning, 인증, 권한, device pairing, migration 절차를 근거 기반의 대화로 안전하게 안내합니다."
disable-model-invocation: false
argument-hint: "<사용자가 직접 해야 하는 설정·인증·이관 작업>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# User-Run Wizard

<!-- tigerkit:ui-evidence -->
## UI Evidence

Quote existing UI labels verbatim, including language, case, punctuation and spacing. Navigation instructions need evidence for every menu/breadcrumb label and connection; a title, route, identifier, enum, schema, glossary or ticket wording alone does not prove the entry path. Keep proposed copy separate. Bind claims to target/environment/locale/role and actual rendering evidence; preserve conflicting or missing provenance rather than guessing.

Before collecting or verifying UI labels/paths within this skill's investigation authority, read [UI evidence collection](references/ui-evidence.md). Skip collection guidance for non-UI work and propagation-only tasks. A handoff or publication-only phase carries supplied evidence and pending requests without starting a new investigation.

In reports and publication preparation, preserve exact verified literals and explicitly list required unverified labels/connections, available evidence, the concrete limitation and smallest missing input. User-supplied text is user-provided, not independently observed; it resolves only the supported claim. Never turn an unverified path into navigation instructions or hide uncertainty in PR/QA/handoff output.

Guide `host-session` procedures that users must perform themselves. Internally, strictly track steps, value
sources/destinations, secrecy, and safety boundaries, but do not dump them to the user
like an approval document.

**Keep the conversation natural and the state strict.**

Open with a brief overview of the full journey, then naturally guide the user through
one action they must take now. Do not repeatedly confirm already completed steps.

## Scope

Applicable examples:

- `provisioning` and `dashboard` setup
- Issuing and placing `credential`/`secret` values
- `login`, MFA, OTP, CAPTCHA, `passkey`
- `permission`/`keychain`/`device` `pairing`
- Human-only steps during `migration`/`cutover`
- Exact consumer handoffs for host configuration, authentication, permission, or restart
  actions that the invoking skill cannot perform safely

Routine code/CLI tasks the `agent` can safely execute, product decisions, and `acceptance` `verification`
are outside this skill's scope.

When another skill supplies an exact setup handoff, read
[consumer handoffs](references/consumer-handoffs.md). The invoking skill keeps ownership of
its operation and verdict; this wizard owns only the current human action and its completion
signal.

## Research and Planning

Read [upstream distillation](references/upstream-distillation.md) only when deciding `upstream provenance` or `adaptation`;
do not read it during an ordinary `wizard` run.

First read the `repository` and current `host` `evidence` to build this internal state:

- Full journey and sequence
- Each value's `source`/`destination`
- `secret`/`public` classification
- Already completed steps
- Steps the user must perform
- Irreversible steps
- Verifiable `completion` `signal`

For a consumer handoff, also preserve the consumer, exact pending criterion, detected host
and capability state, required versus recommended properties, and resume action. Do not ask
the user to restate values already present in the handoff.

Do not invent unknown UI, buttons, URLs, or commands. Where evidence is unavailable, describe only that point
as `Unverifiable`.

When the journey depends on a version-sensitive external API, OAuth/SSO provider, or provider dashboard that repository
evidence cannot establish, read [external contract evidence](references/external-contracts.md). Installed/local contract
evidence stays authoritative over generic latest documentation.

Apply UI Evidence to every user instruction, including provider-dashboard navigation.

For example, tell the user:

```text
대략 키 발급 → 로컬 저장 → 연결 확인 세 단계면 끝납니다.
키 값은 대화에 남기지 않을게요. 먼저 발급 화면까지 들어가 주세요.
```

Guide the next step only after observing the previous step's `completion`.

## Secrets and Authentication

Never `echo` a `secret` or store it in `chat`, Markdown, `log`, or `eval`.
Use hidden input for one-time secrets. For explicitly authorized development/QA application
credentials, including passwords, read [worktree-local authentication](references/authentication.md)
before reuse or cleanup and use only the scoped protected file; retention does not authorize
new login or automated secret entry.

Do not prompt users to paste OTP, `password`, `token`, `session` `value`, or `recovery` `code`
into the conversation. Do not retain even non-secret `identifier` values unless needed for the task.

For file-mediated input in a repository task, first prove that `git ls-files -- .tigerkit/`
returns no tracked paths and `git check-ignore -q -- .tigerkit/` succeeds. Accept Git's
effective per-directory, local-exclude, or user-level-exclude decision. Read the user-editable
input branch in [artifact paths](references/artifact-paths.md) before creation or consumption.
If a parent already created and showed an input file, reuse that exact path under its
established owner, lifecycle and target binding; do not create a second wizard file.
If that boundary is missing, conflicts or belongs to a different task/worktree, application,
verified origin, environment or account/role, hold reuse, overwrite and deletion until the
parent resolves it. For a new wizard-owned input, create
`.tigerkit/secret-input/tk-wizard-<run-id>/input.json` with directory mode `0700`
and file mode `0600`, seeded with a plain JSON object such as `{"token": ""}` or the exact
required credential fields. Before waiting for input, verify the exact file still exists
at the reported path, then visibly show both the repository-relative and absolute paths
as well as the secret-free template and fields to fill
and save. A clipboard command must JSON-serialize into the named field, preserve other
fields and expose no value in arguments or shell history.
Do not launch an editor, file opener, GUI, terminal UI, or focus-changing
application to collect the value. Open the file only after showing the path and receiving
an explicit user request. If the path cannot be proven safe and accessible, use an
available host-native hidden input or return `Blocked | Unverifiable`; do not fall back to
an external scratch path.

After showing the path, use bounded metadata-change polling; the non-empty initial template
is still `Pending`. On change, a trusted local reader validates JSON and all required fields
without returning content or parser excerpts. Blank, missing or partly saved values stay
`Pending` without rewriting the file. Before use, recheck safe path, ownership and mode
`0600`, validate and consume the same snapshot, then continue the exact pending step without
a completion message. Apply the established lifecycle: immediately remove consumed one-time
secret input and its run directory on success, failure or exception only within the owner's
cleanup authority, and verify no residue. For authorized scoped application authentication,
including development/QA passwords, preserve the protected file under
[worktree-local authentication](references/authentication.md); phase completion, failure,
interruption and access expiry are not deletion triggers. Actual production credentials,
OTPs, recovery codes and passwords outside that approved scope remain one-time input.
Never return a user-input `Pending` state unless both actual paths have appeared in the
user-visible answer; absence of an actual created file is `Blocked | Unverifiable`,
not an instruction to guess a path.
Renew an expired wait window while the task remains active. Only when the runtime can no
longer wait, preserve the run-owned input path and explain how to resume monitoring.

If a `helper` is needed, create it as a one-time `user-run` `helper` and preserve these semantics:

- Separate normal input from `secret` `input`
- Do not `persist` `secret` values by default
- Clearly show the `destination`
- Do not silently overwrite existing values
- Statically validate with `bash -n` and, when possible, `shellcheck`
- Explain how to delete or retain it afterward

## 🔴 CHECKPOINT · 🛑 STOP · Safety Confirmation

Treat irreversible, production-affecting, or unverifiable steps below as hard stops; ordinary reversible steps remain frictionless.

Do not ask for approval at every ordinary `reversible` step.
Require explicit confirmation only for actions that change the user's decision, are difficult to reverse,
or affect `production`.

Example:

```text
여기서 기존 production key를 폐기하면 현재 서비스에 영향이 생길 수 있어요.
새 key 연결이 정상인지 먼저 확인한 뒤 폐기하는 걸 권장합니다.
새 key 확인 후 기존 key를 폐기할까요?
```

If no safe verification path exists, do not rush execution; explain the state as `Blocked` or `Unverifiable`.

## Completion

At the end, briefly explain what the user completed and how it was verified.
Do not expose a `stage` `table`, `secret` `inventory`, internal state machine, or long `receipt` by default.

Use exactly one actual state from `Status: Pass | Pending | Blocked | Unverifiable | Fail` as the `terminal` `token`.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit or the eligible durable-root branch applies. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Investigate facts; reuse authorization. For user-owned decisions read
[question rounds](references/questions.md); otherwise proceed.
Plain chat, even one approval: standalone `---`, then
`❓ **Q<n> · <title>**: <question>` and `➡️ <recommendation>` per item.
Ask only settled-prerequisite questions; separate approval.
Questions come last; put status, risks and plans before them.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
