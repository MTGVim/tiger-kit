---
name: tk-wizard
description: "[user/auto] 사용자가 직접 해야 하는 `provisioning`, `credential`·`secret`, `login`/MFA/OTP/CAPTCHA/`passkey`, `dashboard`, `permission`, `device` `pairing`, `migration`/`cutover` 절차를 근거 기반의 자연스러운 대화로 안전하게 안내한다."
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
사용자가 action이나 비가역 confirmation을 선택해야 하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 안내를 plain chat으로 fallback하고 secret 자체를 tool input으로 수집하지 않습니다.

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

`upstream provenance` 또는 `adaptation` 판단이 필요할 때만 [upstream 증류](references/upstream-distillation.md)를 읽고,
일반 `wizard` 실행에서는 읽지 않습니다.

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
