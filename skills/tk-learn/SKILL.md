---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료에서 재사용 가능한 repository 또는 user skill을 설계합니다. 명확한 skill-authoring intent가 있으면 draft와 approval checkpoint까지만 진행하며, approval 전에는 쓰지 않습니다."
disable-model-invocation: false
argument-hint: "<conversation, note, path, URL, workflow, or skill-evolution candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill learning

Apply this to an explicit `invocation` or clear intent to author a reusable `skill`.
Convert conversations, notes, paths, URLs, repeated workflows, or skill-evolution
candidates into `repo skill | user skill` candidates. Rules, one-off tips, and general
implementation are out of scope, and never invoke another user-invoked `skill`.

This is the sole TigerKit author for `skill` `create | improve | merge`, including new
`skill`s and semantic updates. Candidates or targets from other `skill`s must also pass
evidence, deduplication, evaluation, compatibility, and apply gates.

Draft and apply are separate.

- `draft gate`: Distinguish verified evidence from unverified user claims and design a
  `pending` candidate. Even when evidence remains `unverified`, record a clear design
  request in `learn.md` without printing the full text in chat.
- `apply gate`: Every checklist row must pass before writing to a `skill` path.

## Artifact-first draft checkpoint
candidate 또는 apply approval이 필요하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 approval packet을 plain chat으로 fallback하고 승인 전 canonical skill path를 쓰지 않습니다.

새 초안을 만들 때는 승인 전 최소 초안 전체를 채팅에 출력하지
않습니다. 먼저 저장소 루트의 `.tigerkit/learn.md` 에 `pending` 스크래치 장부를
원자적으로 작성하고 같은 경로를 다시 읽어 검증합니다. 이 파일은 정본
`skill` 경로도 아니고 `.tigerkit/skill-drafts/<skill-name>/` 도 아닙니다.

`learn.md` 는 다음 필드를 한 번씩 소유합니다: 작업 `Status` (`Pending | Blocked`),
`Disposition` (`reported | applied | pending`),
`Decision` (`proposed | merge | no-op | continue | pending`), `Candidate`,
`Evidence` (각 주장에 대한 ID/source/`verified | unverified`), `Checklist` (각
적용 검사의 `passed | pending | failed` 와 근거), `Target path` (정확한
계획 경로와 `not created`), `Not created` (두 정본 쓰기 경계),
`Next step` (하나의 실행 가능한 행동), `Updated` (작성 시각 또는 run ID).

원자적 쓰기와 재읽기가 현재 후보/실행과 일치하면 `Disposition: applied` 를
사용할 수 있지만, 적용 승인 전 작업 `Status: Pending` 은 유지합니다.
`Disposition` 은 장부 쓰기/재읽기 결과이고 `Status` 와 같은 의미가 아닙니다.

같은 디렉터리의 임시 파일을 만든 뒤 원자적으로 이름을 바꾸고 즉시 다시 읽습니다.
필수 필드가 없거나 장부가 오래됐거나 없거나 재읽기 내용이 작성 내용과
다르면 `Blocked` 로 중지하고 정본 경로에는 쓰지 않습니다. 기존 장부가
다른 후보/실행을 가리키면 덮어쓰지 말고 `Blocked` 로 보고합니다.

## Workflow

1. **Evidence ledger:** Assign each case/workflow an ID, claim, source, and
   `verified | unverified`. Keep two user-claimed cases with inaccessible artifacts
   as separate `unverified` rows and record `pending` status in `learn.md`. Promotion
   requires two independently verified repetitions or a reusable workflow supported
   by artifacts. `Unverified` rows cannot pass apply. End one-off mistakes, raw logs,
   and single unsourced claims as `no-op`.
2. **Promotion and deduplication:** Apply [Skill quality](references/skill-quality.md),
   then compare against existing repository/user `skill`s, default model capability,
   and a short rule. Choose one of `merge | no-op | continue | pending`. If the
   catalog cannot be read, remain `pending` and record that status and rationale in
   `learn.md`.
3. **Candidate proposal:** Present the target, action name, invocation kind, and
   positive/negative triggers. Use the user's domain/workflow language to choose a
   lowercase, hyphenated, verb-form name of at most 64 characters; check for
   collisions, then mark it `proposed`. Leave unsupported values as `TBD`.
4. **Minimal draft:** Record the minimal SKILL.md inputs, workflow, failure branches,
   approval boundaries, completion criteria, output contract, and prohibitions
   directly in `learn.md`. Also add train/validation triggers, success/boundary
   assertions, a no-skill or prior-skill baseline, and the
   portable-core/host-extension determination.
5. **Approval checkpoint:** After rereading `learn.md`, follow the checkpoint and
   output contract below, then stop.
6. **Write, verify, report:** After every checklist row and apply authority pass,
   preserve the pre-write contents, write with an atomic rename, then reread and
   verify frontmatter, links, evals, and target-host invocation.

### Apply gate checklist

| Check | Passing evidence | If not passed |
|---|---|---|
| Promotion threshold | Independent cases/common workflow meet the promotion threshold | `no-op | pending` |
| Deduplication | Differences from existing skill/default capability/short rule and rationale for `merge | continue` exist | `no-op | pending` |
| Candidate identity | Native target, name, kind, and positive/negative triggers are confirmed | `pending | Unverifiable` |
| Behavior validation | Train/validation triggers and success/boundary assertions pass | `pending | Blocked` |
| Baseline/compatibility | No-skill/prior baseline and portable-core/host-extension determination are verified | `pending | Unverifiable` |
| Apply authority | Current-turn approval names the exact candidate and target path | `pending`; do not write |

Use only the current host's native repo/user `skill` paths proven through actual path
or host discovery. An unknown host is `Unverifiable`. Do not invent locations, force
one host's paths onto another host, perform cross-host fan-out/sync, or use
`.tigerkit/` as a permanent `skill` registry/global state.

## Failure paths

| Trigger | Immediate action | What remains unresolved |
|---|---|---|
| 두 사례/workflow를 주장했지만 산출물을 읽을 수 없음 | 각각 `unverified` 로 기록하고 `learn.md` 를 `Blocked` 로 남김 | 정확한 산출물/검사를 요청함; 쓰지 않음 |
| 일회성 사례 하나 또는 원시 로그만 있음 | 기준/개인정보와 `Decision: no-op`, `Status: Pending` 을 기록함 | 후보/경로를 만들지 않음 |
| skill/기본 capability와 중복됨 | `merge | no-op` 과 근거를 보고함 | 새 디렉터리를 만들지 않음 |
| 대상/이름/trigger 일부를 알 수 없음 | 지원되는 값은 `proposed`, 나머지는 `TBD` 로 `learn.md` 에 기록함 | 후보 식별을 `pending` 으로 유지함; 쓰지 않음 |
| 증거/대상/승인이 충돌함 | 충돌과 하나의 결정을 제시함 | `Blocked` 로 중지 |
| 쓰기/쓰기 후 검사가 실패함 | 기존 대상과 실행 임시 파일을 보존하고, 실행 소유임이 입증된 경우에만 부분적으로 생성된 새 대상을 제거함 | 정확히 재현·검증할 수 있을 때만 복구함; 소유권/보존이 불확실하면 `Blocked | Unverifiable`, 그 외에는 실제 경로와 `Fail` 을 보고함 |

## 🔴 CHECKPOINT · 🛑 STOP (Approval and stop point)

Do not write to the canonical path or
`.tigerkit/skill-drafts/<skill-name>/` before explicit current-turn apply approval.
Past approval, implicit `invocation`, and a generic request to continue are
insufficient authority. Before approval, the candidate remains `pending`, and Target
path records the exact planned path and `not created`.

The approval checkpoint for a new draft occurs only after writing and rereading
`.tigerkit/learn.md`; a write or reread failure is `Blocked` and cannot request
approval. The failure table owns the one-off `no-op` status.

## Output contract

산출물 작성 후에는 절대 `learn.md` 경로와 `Decision`/`Status`/`Disposition` 를 먼저
보고하고, 핵심 결과를 1~3줄로만 요약합니다. 마지막에는 승인 질문을
정확히 하나만 둡니다. 장부가 소유하는 `Evidence`, `Dedupe`, `Candidate`,
`Target path`, `Verification`, `Remaining concerns` 의 전문을 채팅에 복사하지
않습니다. threshold 실패 또는 중복으로 인한 no-op도 같은 artifact-first 규칙을
따릅니다.

## Prohibitions / antipatterns

- Do not promote one-off cases, credentials, raw logs, or screenshots as reusable
  evidence or copy them into a draft.
- Do not omit a requested `pending` draft because evidence is `unverified`.
- Do not create duplicate `skill`s, verbose wrappers around default capability, or
  indistinguishable trigger pairs.
- Do not duplicate the name/kind/path/verification/concerns in the Receipt.
- Do not auto-archive, edit `.gitignore`, invoke another user `skill`, push, or
  publish.
