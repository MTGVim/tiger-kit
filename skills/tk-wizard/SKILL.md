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

Quote existing UI labels verbatim, preserving language, case, punctuation, and spacing. Navigation instructions require evidence for every menu/breadcrumb label and each connection in the path; a verified destination title or route does not prove its entry path. Identifiers, enums, i18n keys, domain terms, and ticket wording are not current UI evidence unless the current render path proves them. Keep proposed copy separate from existing labels. Report conflicting provenance instead of silently selecting a label or combining incompatible paths.

For each claim, use target/environment/locale/role-matched runtime evidence, source connected to the render path, or a supplied capture with provenance. API text needs the actual response and its rendering/transformation binding; a schema proves only shape. If another repository, host shell, API, configuration, or permission controls a missing segment, state the known boundary and what remains unverified. Do not present a plausible path as guidance, even with an inference disclaimer.

Within investigation authority, obtain missing evidence from accessible sources or attempt read-only browser inspection through the browser owner when the target and safe access are available. Do not stop at a repository miss or merely suggest browsing when an authorized inspection can proceed. If access or evidence is unavailable, mark the affected claim `Unverifiable`, explain the concrete limitation, and request the smallest missing input: a redacted menu API response with relevant label/hierarchy/route fields, owning source, or a screenshot showing the navigation. Never request credentials or an unredacted payload in chat. Preserve verified partial results and pending evidence in summaries, QA, and handoffs; propagation-only owners carry the request without opening a new investigation.

Guide `host-session` procedures that users must perform themselves. Internally, strictly track steps, value
sources/destinations, secrecy, and safety boundaries, but do not dump them to the user
like an approval document.

**Keep the conversation natural and the state strict.**

Initially describe the full journey in only 1–3 sentences, then naturally guide the user through
one action they must take now. Do not repeatedly confirm already completed steps.
When the user must choose an action or irreversible confirmation, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, give the same guidance in plain chat; never collect the secret itself as tool input.

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
When necessary, use only `hidden`/`ephemeral` `input` at execution time.

Do not prompt users to paste OTP, `password`, `token`, `session` `value`, or `recovery` `code`
into the conversation. Do not retain even non-secret `identifier` values unless needed for the task.

For file-mediated input in a repository task, first prove that `git ls-files -- .tigerkit/`
returns no tracked paths and `git check-ignore -q -- .tigerkit/` succeeds. Accept Git's
effective per-directory, local-exclude, or user-level-exclude decision. Create an empty
`.tigerkit/secret-input/tk-wizard-<run-id>/<credential-type>` with directory mode `0700`
and file mode `0600`, then show both its repository-relative and absolute paths plus a
clipboard-to-file command that does not expose the value in command arguments or shell
history. Do not launch an editor, file opener, GUI, terminal UI, or focus-changing
application to collect the value. Open the file only after showing the path and receiving
an explicit user request. If the path cannot be proven safe and accessible, use an
available host-native hidden input or return `Blocked | Unverifiable`; do not fall back to
an external scratch path.

After showing the path, start a bounded non-content watcher or poll for non-empty state.
Do not ask the user to report completion. When input appears, recheck ownership and mode
`0600`, continue the exact pending step, and remove the secret input immediately after use.
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

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, and lessons in `study/<topic>/`. Preserve existing owner-specific paths and explicit user-selected final destinations. Create artifacts only when the active task calls for them. Before writing, verify the repository root, no tracked `.tigerkit` paths, and safe nonsymlink destinations. From the repository root, run `git ls-files -- .tigerkit .tigerkit/` to check tracking, then `git check-ignore -q -- .tigerkit/` to check effective exclusion. Exit 0 means leave ignore files unchanged, including when exclusion comes from `core.excludesFile` (such as configured `~/.gitignore`), the default global ignore file, or `.git/info/exclude`; a missing repository `.gitignore` or missing literal entry is not evidence of missing coverage. Only exit 1 permits creating the root `.gitignore` or appending `/.tigerkit/`, preserving existing bytes and line endings, then rerunning the same check before writing. Any other exit status or command failure blocks the file branch without an ignore edit. Use `git check-ignore -v -- .tigerkit/` only to diagnose the source; a printed negated pattern is not proof of exclusion. This narrow ignore setup is part of an authorized artifact write even for a read-only task; it grants no other source/config/index/commit/publication authority. Existing effective ignore rules need no edit. Do not untrack files or follow a symlinked/nonregular `.gitignore`; if unsafe, unwritable, still unignored, or no repository is identified, stop only the file branch as `Blocked | Unverifiable`, without an OS-temp fallback. Briefly report an ignore edit; never stage or commit it solely for setup. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.
