---
name: tk-pr-rebase
description: "[user/auto] 특정 PR의 기준 브랜치 변경이나 충돌에 rebase가 필요할 때 사용합니다. 활성 `tk-pr-sweep` 또는 `tk-pr-respond`가 정확한 PR/base/head와 승인된 rebase 범위를 넘기는 handoff도 받습니다. 일반 브랜치 작업과 rebase 근거가 확인되지 않은 리뷰 대응에는 자동 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "<pull request or repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

<a id="rebase-one-pr"></a>
# PR 하나의 rebase

<a id="shared-references"></a>
## 공통 참조

현재 설치된 담당 스킬에서 해당 분기의 기준을 읽습니다. 소유자나 자원이 없거나 일치하지 않으면 해당 작업을 중단합니다. 기억, 다른 설치본, 미승인 설치로 대체하지 않고 `tk-setup-skills`를 사용합니다. 참조 읽기는 실행이나 변경 권한을 부여하지 않습니다.

- 사용자 소유 결정, 누락된 승인이나 미충족 선행 조건을 질문 또는 질문 도구 입력으로 제시하기 직전에, 이번 작업에서 [질문 라운드](../tk-questioning/references/questions.md)를 읽었는지 확인하고 누락했으면 읽습니다. 독립적인 결정과 승인은 별도 질문으로 두고 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계나 여러 속성을 비교하는 대화 응답을 전달하기 전에 [대화 전달](../tk-writing/references/delivery.md)을 읽습니다. 작업별 출력 계약이 우선합니다.

<a id="approval-continuity"></a>
## 승인 연속성

같은 작업의 유효한 승인은 턴과 자식 단계(baseline/after 포함)에도 재사용합니다. 기존 담당자를 통해 승인된 작업만 계속하고 자식·baseline 근거를 반환한 뒤 승인된 담당 작업을 재개합니다. 단계 상태는 완료가 아니며, 호출과 복구된 산출물은 권한을 부여하지 않습니다. 새로운 중대한 결정, 범위·권한 변경이나 사용자만 제공할 입력이 누락된 경우에만 질문합니다. 원격 작업과 파괴적 작업에는 행동·대상의 명시적 승인이 필요하며 로컬 승인에서 추론하지 않습니다.

`/tk-pr-rebase`, `$tk-pr-rebase`, 호스트 스킬 선택기 또는 활성 `tk-pr-sweep`이나 `tk-pr-respond`의 정확히 승인된 rebase 인계를 통해서만 시작합니다.
일반적인 브랜치 `rebase`, 단순한 `conflict marker edit`나 일반 리뷰 대응에는 자동 적용하지 않습니다.

PR 하나의 정확한 `base/head rebase`, `conflict resolution`, `verification`과 범위가 제한된 `force-with-lease`를 담당합니다.
`merge`, `close`, `tag`, `release`나 무관한 피드백 구현은 수행하지 않습니다.

<a id="fresh-identity-and-workspace"></a>
## 최신 신원과 워크스페이스

로컬 rebase는 정확한 PR 작업을 위해 새로 마련한 전용 격리 워크스페이스에서 실행해야 합니다. “새로 마련한”은
의미에 따른 조건입니다. 호스트가 이 호출을 정확한 PR/head 전용의 새 외부 관리 워크스페이스에
이미 배치했다면 출처를 입증한 뒤 해당 경계를 재사용할 수 있습니다. 표현을 충족하려고
중첩된 수동 worktree를 만들지 않습니다.

무엇이든 만들기 전에 저장소 루트, 브랜치·HEAD, `GIT_DIR`, `GIT_COMMON`과
`git rev-parse --show-superproject-working-tree` 또는 동등한 정보를 확인합니다. `GIT_DIR != GIT_COMMON`은
submodule을 배제한 뒤에만 linked-worktree 신호이며, linked worktree라고 해서 자동으로 이 PR의 소유인 것은 아닙니다.

새 전용 워크스페이스가 여전히 필요하다면 현재 작업 승인이나 승인된 Sweep
인계가 워크스페이스 생성을 포함하는지 먼저 확인합니다. 명시적인 워크스페이스 동의를 요구하는 더 엄격한 사용자 규칙을
보존합니다. rebase 요청만으로 그 규칙을 무시하지 않습니다. 정확한 격리가 기존 승인에
포함되면 다시 질문하지 않고 재사용합니다. 그렇지 않으면 생성 전에 누락된 결정을 받습니다.
새 workspace의 생성·초기화 경로를 선택하기 전에 [호스트 workspace와 setup 경계](../tk-pr-guidance/references/workspace-setup.md)를 읽습니다. 호스트 경로를 쓸 수 없으면 setup hook을 직접 실행하지 말고 공통 폴백의 결정을 받습니다. Sweep에서 받은 해당 행의 기존 결정은 재사용합니다.
그다음 현재 도구 목록에서 `EnterWorktree`, `WorktreeCreate`, `/worktree`, `--worktree` 같은 구체적인
기본 진입점을 확인합니다. 이는 기능 예시이며 지속적인 제공자
경로 규칙이 아닙니다. 사용 가능한 에이전트 호출형 기본 worktree·워크스페이스 기능을 우선하고,
경로, 브랜치나 detached 상태와 HEAD를 새로 읽습니다.
안전한 기본 기능이 없을 때만 수동 `git worktree`를 사용합니다. 대체 경로는 정확한 `old_head`에서 시작하고,
경로·브랜치 충돌과 무관한 작업을 피하며 생성 후 새로 읽어야 합니다. `.tigerkit/` 제외 적용이 누락된 경우에만 산출물 경로 설정을 사용합니다.
대체 경로를 가능하게 하려고 무관한 Git 제외 항목을 수정하거나 설정 커밋을 만들지 않습니다.
전용 경계를 만들고 최신 상태임을 입증할 수 없다면 변경 전에 `Blocked`를 반환합니다.

호스트 관리 워크스페이스는 호스트 소유 수명주기를 유지합니다. 이 스킬은 rebase 완료의 일부로
외부 관리 워크스페이스를 제거, prune, 이동하거나 다른 방식으로 정리하지 않습니다.

시작할 때 다음을 새로 읽습니다.

- 저장소와 인증된 신원을 읽습니다.
- 열린 PR 번호를 읽습니다.
- head 저장소/ref/SHA를 읽습니다.
- base 저장소/ref/SHA를 읽습니다.
- 로컬 브랜치·HEAD·워크스페이스 출처를 읽습니다.
- 활성 Git 작업을 읽습니다.
- 리뷰·스레드·검사 상태를 읽습니다.

base 업데이트를 권고하거나 실행하기 전에 [PR base와 rebase 준비 상태](../tk-pr-guidance/references/rebase-readiness.md)를 적용합니다.

신원·소유권이 모호하거나 fork 발행 경계의 안전성을 입증할 수 없다면 변경 전에 `Blocked`를 반환합니다.

정확한 원격 head와 최신 base를 fetch한 뒤 다음을 고정합니다.

```text
old_head
base_sha
full head ref
remote
expected force-with-lease
```

로컬 `HEAD == old_head`, 원격 PR head `== old_head`와 깨끗한 전용 워크스페이스를 요구합니다.

<a id="rebase-and-conflict"></a>
## rebase와 충돌

정확한 `base_sha` 위로 rebase합니다.
충돌이 발생하면 `tk-merge-conflict`의 의도·index·마커·검증 계약을 적용합니다.
의미상 모호함이 있으면 임의로 선택하지 않습니다.

rebase 후 다음을 검증합니다.

- Git 작업이 완료되었는지 검증합니다.
- 워크스페이스·index가 깨끗한지 검증합니다.
- `base_sha`가 새 HEAD의 조상인지 검증합니다.
- 의도한 커밋·diff가 보존되었는지 검증합니다.
- 관련 테스트·검사가 통과하는지 검증합니다.

재작성이 필요하지 않으면 강제 push하지 않습니다.

<a id="standalone-publication"></a>
## 독립 실행의 발행

명시적인 독립 호출이 자동으로 허용하는 범위는 로컬 rebase뿐입니다.
원격 발행 전에 정확한 PR/base/head, 이전·새 SHA, 검증, 정확한 lease/refspec,
답글·스레드 행동과 제외 사항을 활성 승인 자료에 기록합니다. 같은 턴의 단순한 자료는
충실하게 유지하고 다시 읽을 수 있다면 대화에 보관합니다. 단일 파일 `.tigerkit/pr-rebase.md`는 명시적인 `save`,
여러 턴에 걸친 인계·복구, 복잡한 충돌 상태 또는 호스트가 정확한 자료를 유지할 수 없을 때만 사용합니다. 실행별
보관 파일은 만들지 않습니다. 파일을 사용하면 이 담당자의 오래된 완료 내용을 원자적으로 교체하고 다시 읽습니다.

<a id="-checkpoint---stop--standalone-publication-boundary"></a>
## 🔴 점검 지점 · 🛑 중단 · 독립 실행 발행 경계

사용자에게 단순히 산출물을 읽으라고만 하지 않습니다. 변경된 내용, 검증한 내용과
정확히 어떤 발행을 수행할지를 자연스럽게 요약합니다. 이 대상에 대한 rebase와 push를 명시적으로 허용한 사전 요청을 재사용하며, 발행 권한이 없을 때만 한 번 질문합니다.
원격 쓰기 직전에 저장소·신원·열림 상태·base·head·refspec·lease를 재확인할 수 없거나
중대한 변동으로 승인이 무효화되면 즉시 중단합니다.

발행에는 정확한 `--force-with-lease=<full-head-ref>:<old_head>`만 허용합니다.
일반 `--force`는 금지합니다.

<a id="execution-under-a-parent-skill"></a>
## 상위 스킬 아래에서 실행

활성 `tk-pr-sweep`이나 `tk-pr-respond`가 정확한 저장소/PR/base/head, rebase 경로, 대상 브랜치와 범위가 제한된 이력 재작성 발행을 이미 승인받았다면 해당 승인 질문을 반복하지 않습니다.

상위 인계에는 정확한 PR, base 저장소/ref/SHA, head 저장소/ref/SHA, 승인된 발행 대상과 경로, 그리고 해당 워크스페이스가 이 PR에 속함을 입증하기에 충분한 출처를 갖춘 새 전용 워크스페이스 경로가 포함되어야 합니다. 워크스페이스는 호스트 기본 기능이나 안전한 수동 Git 대체 경로일 수 있습니다. 자식은 입증된 호스트 소유 워크스페이스를 중첩된 수동 워크스페이스로 교체해서는 안 됩니다. 승인, 경로, HEAD나 출처가 없거나 오래되었다면 변경 전에 `Blocked`를 반환합니다. 해당 워크스페이스에서 자식을 실행하며, 상위의 `main` 또는 `develop` checkout을 PR 브랜치로 전환하지 않습니다.

자식은 `.tigerkit/pr-sweep.md`, `.tigerkit/pr-respond.md`, `.tigerkit/pr-rebase.md`를 만들면 안 됩니다.
다음의 간결한 근거만 상위에 반환합니다.

- 저장소/PR을 반환합니다.
- 사용한 `base_sha` / `old_head`를 반환합니다.
- 검증된 `new_head`를 반환합니다.
- 테스트·검사를 반환합니다.
- 정확한 lease/refspec을 반환합니다.
- 남은 충돌·발견 사항을 반환합니다.
- 상태를 반환합니다.

자식 실행 직전에 정확한 PR/base/head를 다시 확인합니다.
head/base가 승인된 인계 밖에서 중대하게 바뀌었다면 해당 PR만 `Blocked`로 상위에 반환합니다.
상위가 `tk-pr-respond`라면 검증된 `new_head`를 예상 전이로 반환합니다. 상위는 계속하기 전에 PR을 새로 읽고 해당 head를 기준으로 피드백·스레드 근거를 다시 구성해야 합니다. 자식 rebase는 리뷰 발견 사항을 해결 처리하거나 답글을 달지 않습니다.

<a id="after-publication"></a>
## 발행 후

원격 PR head가 `new_head`인지 검증합니다.
독립 실행에서는 rebase로 실제 충족된 리뷰 스레드에만 답글을 달거나 해결 처리합니다. 상위 스킬 아래에서는 피드백에 답글을 달거나 해결 처리하지 않고 최신 상태를 상위에 반환합니다.
모든 스레드·리뷰·검사를 새로 읽고 해결되지 않은 발견 사항을 완료로 숨기지 않습니다.

필요하다면 작성자, 인증된 사용자, 봇과 여전히 유효한 승인자를 제외한 기존 인간 리뷰어에게 리뷰를 재요청합니다.
생성한 GitHub 댓글은 `_🤖 본 코멘트는 AI가 작성했습니다._`로 끝냅니다.

<a id="status"></a>
## 상태

| 상태 | 의미 |
| --- | --- |
| `Pass` | 최신 근거가 정확한 rebase와 필수 발행을 확인합니다. |
| `Pending` | 독립 실행의 발행 승인을 기다립니다. |
| `Blocked` | 신원, 권한, 의미상 충돌이나 최신성이 안전하게 해결되지 않았습니다. |
| `Unverifiable` | 필요한 Git·GitHub 근거를 읽을 수 없습니다. |
| `Fail` | 로컬이나 원격 작업이 실패했으며 정확하게 적용된 상태를 보고해야 합니다. |

관찰하지 않은 답글·해결 처리·리뷰·검사 상태에 대해 성공을 주장하지 않습니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 쓰기, checkout·전송·Git 제외 설정이나 임시 입력 소비 전에
[산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 파일에는 안전하고 소유권이 확인된 심볼릭 링크가 아닌 경로와
입증된 Git 제외를 사용합니다. 검사에 실패하면 해당 파일 분기를 중단합니다. 명시적인 최종 목적지와
담당자별 기본값을 보존합니다. 미리 채워진 입력은 완료된 입력이 아닙니다.
정리는 기록된 리터럴 형태의 해석 완료된 실행 소유 절대 경로만 대상으로 하며, cwd 상대 경로나 glob을 사용하지 않습니다.
