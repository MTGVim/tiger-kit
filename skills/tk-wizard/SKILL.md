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

Routine code/CLI tasks the `agent` can safely execute, product decisions, and `acceptance` `verification`
are outside this skill's scope.

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

Do not invent unknown UI, buttons, URLs, or commands. Where evidence is unavailable, describe only that point
as `Unverifiable`.

Verified UI controls are literals, not prose to translate. Keep the exact language, case, punctuation, and spacing
of a button, tab, menu, field, or modal title in every user instruction. An `enum`, code identifier, i18n key, route,
or domain term is not a label unless the current render path proves that it is displayed as-is. If the rendered text
is not verified, keep the code literal separate and mark the UI wording `Unverifiable`.

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

For file-mediated input in a repository task, first prove that a repository-tracked `ignore`
rule covers `.tigerkit/`. Create an empty
`.tigerkit/secret-input/tk-wizard-<run-id>/<credential-type>` with directory mode `0700`
and file mode `0600`, then show both its repository-relative and absolute paths plus a
clipboard-to-file command that does not expose the value in command arguments or shell
history. Do not launch an editor, file opener, GUI, terminal UI, or focus-changing
application to collect the value. Open the file only after showing the path and receiving
an explicit user request. If the path cannot be proven safe and accessible, use an
available host-native hidden input or return `Blocked | Unverifiable`; do not fall back to
an external scratch path.

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
