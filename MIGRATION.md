# TigerKit Issue 277 구조적 마이그레이션

TigerKit은 이제 `tk-drive`를 독립적으로 호출하는 workflow phase의 chain이 아니라
하나의 product-change controller로 다룹니다.

## 호출

명시적 source 하나로 변경을 시작합니다.

```text
$tk-drive <source>
```

Drive는 하나의 active run에서 `Prepare -> Execute -> Close gaps -> Finalize`를
수행합니다. 이전 standalone preparation, unit-slicing, implementation phase 호출을
대체하는 invocation은 없습니다. 작은 일반 수정은 여전히 Drive 없이 현재 대화에서
처리합니다.

## 하나의 승인

Prepare는 source와 repository evidence를 읽고 안전한 default를 정하며 material
assumptions와 alternatives를 기록하고 Ready R/AC와 dependency waves를 도출한 뒤
하나의 final approval surface를 표시합니다. `tk-grill-me`는 user-owned decision이
안전한 executable plan을 막을 때만 사용합니다.

승인은 표시된 snapshot만 승인합니다. Material source, scope, branch/head,
remote-state 또는 irreversible-decision drift가 발생하면 Prepare로 돌아갑니다.
변경되지 않은 plan에는 routine approval을 다시 받지 않습니다.

## Fresh-worker 변경

Drive는 product, test 또는 configuration 변경을 직접 작성하지 않습니다. 모든 primary
및 corrective candidate는 하나의 bounded unit을 맡은 fresh worker가 만듭니다. worker
dispatch가 없으면 controller-edit fallback이 아니라 `Blocked`입니다.

Worker selection은 dispatch마다 자동으로 결정됩니다.

- `cheapest`: evidence가 완전한 mechanical local work;
- `standard`: 일반적인 multi-file implementation 또는 debugging;
- `strongest`: design-heavy, unknown-cause, security/data-sensitive 또는 broad
  reasoning 작업;
- `host-default`: spawn별 selection을 사용할 수 없을 때.

user/repository model mapping이나 provider-name configuration surface는 없습니다.

## 검증 및 커밋

unit 순서는 다음과 같습니다.

```text
fresh worker candidate
-> required tests/checks/browser verifier
-> R/AC acceptance-gap closure
-> bounded fresh corrective worker when needed
-> one verified unit commit
```

필수 TigerKit review는 승인된 R/AC와 현재 evidence 사이의 gap으로 제한합니다. 더
넓은 style, architecture, optimization, security 및 performance review는 명시적인
acceptance 또는 repository policy가 아닌 한 이 workflow의 범위 밖에 둡니다.

## Headless 브라우저 검증

`tk-browser-verify`는 이제 read-only headless acceptance verifier입니다. Browser
scenario, target, auth mode 및 limitation은 top-level approval surface에 둡니다. 필수
authenticated scenario는 product worker가 실행되기 전에 다음 중 하나를 확립해야
합니다: no-auth access, verified run-owned headless session 또는 transient
repository/application-supported token/session bootstrap을 사용합니다.

Interactive login에는 browser 예외가 없습니다. OTP, MFA, SSO, CAPTCHA, passkey 또는
device approval에는 ephemeral secret-input channel을 통한 적절한 short-lived auth
material이 필요합니다. 이 방법으로 approved state를 확립할 수 없으면 product
mutation 전에 결과를 `Unverifiable`로 둡니다. Secret value는 echo하거나 persist하지
않습니다.

verifier는 Markdown lifecycle ledger를 만들지 않습니다. Nested run은 compact
criterion facts와 inspected binary evidence path를 top-level run을 소유하는
`drive.md`, `pr-respond.md` 또는 `pr-sweep.md`로 반환합니다.

## 상태 마이그레이션

Drive는 하나의 repo/worktree-local Markdown ledger를 사용합니다.

```text
.tigerkit/drive.md
```

split phase artifact를 parallel ledger로 마이그레이션하지 마세요. source와 repository
evidence에서 현재 task를 `drive.md`에 다시 만드세요. artifact가 존재한다는 사실만으로
authority를 부여하지 않습니다. Nested worker, reviewer 및 verifier는 lifecycle
Markdown을 쓰는 대신 compact evidence를 반환합니다.

## PR workflow 마이그레이션

`tk-pr-respond`는 이제 하나의 exact-PR resolution 및 publication plan을 준비하고
한 번 질문한 뒤 fresh-worker unit, acceptance verification, commit 및 이미 승인된
bounded remote action을 실행합니다. 이후 publication approval은 없습니다.
Standalone state는 `.tigerkit/pr-respond.md`입니다.

이전 PR-triage wrapper를 대체하는 skill은 없습니다. read-only inventory에는
`$tk-pr-sweep --report`를 사용하세요. interactive `$tk-pr-sweep`는 하나의 multi-PR
batch approval을 준비하고 이동된 deterministic triage script를 직접 호출합니다.
Top-level state는 `.tigerkit/pr-sweep.md`이며 nested Respond, Rebase, worker,
reviewer 및 verifier는 서로 경쟁하는 Markdown ledger를 쓰지 않습니다.

## 권한

Drive는 승인된 verified current-branch unit commit을 만들 수 있습니다. Push, PR,
merge, tag, release, publish 및 history rewriting에는 여전히 각각 별도의 명시적
owner와 authority가 필요합니다.

## 설치/갱신

```bash
npx skills update --global --yes
```

repository validation에서는 checkout에서 다시 설치하고 catalog가 현재 skill 구성만
열거하는지 확인하세요.
