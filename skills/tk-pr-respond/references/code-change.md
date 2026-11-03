<a id="code-change-execution"></a>
# 코드 변경 실행

코드 변경 경로를 선택한 뒤 승인 요청 전에 이 참조를 읽습니다. workspace와 Seed 처리를 계획하는 데 읽기 전용으로 사용합니다. 계획에 대한 현재 승인이 있기 전에는 변경하지 않습니다. 답글만 수행하는 작업은 이 참조를 읽지 않습니다.

<a id="workspace-isolation"></a>
## Workspace 격리

Sweep 아래에 중첩되어 있으면 Sweep이 제공한 setup 담당자, 준비 상태 근거와 실행 동시성 범위를 따릅니다. 초기화를 반복하지 말고 준비된 workspace를 재사용합니다. 계획하지 않은 무거운 setup이나 검사를 추가하기 전에 부모에게 돌아갑니다.

branch/HEAD, linked-worktree 상태, 무관한 작업과 submodule 상태를 조사합니다. `git rev-parse --show-superproject-working-tree`로 submodule을 제외한 뒤에만 `GIT_DIR != GIT_COMMON`을 linked-worktree 신호로 취급합니다. 이것은 checkout이 해당 PR 소유임을 입증하지 않습니다.

조건에 맞는 텍스트 전용 작업에서는 아래의 승인된 index-only 경로도 Sweep 아래를 포함하여 격리를 입증합니다.
새 workspace의 생성·초기화 경로를 선택하기 전에 [호스트 workspace와 setup 경계](../../tk-pr-guidance/references/workspace-setup.md)를 읽습니다. 호스트 경로를 쓸 수 없으면 setup hook을 직접 실행하지 말고 공통 폴백의 결정을 받습니다. Sweep 아래에서는 해당 행의 기존 결정을 재사용하며 누락된 결정만 부모에게 돌려보냅니다.
다른 작업에서 작고 직접적인 수정은 현재 checkout이 정확한 PR 브랜치이고, 깨끗하고 안전하며 무관한 작업이 없을 때만 재사용할 수 있습니다. 그 밖에는 기존 작업 격리를 탐지하고, `EnterWorktree`, `WorktreeCreate`, `/worktree` 또는 `--worktree`처럼 사용 가능한 에이전트 호출 네이티브 기능을 우선하며, 결과 경로, 브랜치 또는 detached 상태와 HEAD를 새로 읽습니다. 정확한 계획과 격리에 대한 현재 승인은 추가 질문 없이 해당 기능도 승인합니다.

안전한 네이티브 기능이 없을 때만 수동 `git worktree`를 사용합니다. 정확히 승인된 PR head에서 시작하고 충돌과 무관한 작업을 피하며 결과를 검증합니다. `.tigerkit/` 제외가 누락된 경우에만 담당 SKILL.md의 산출물 경로 설정을 사용합니다. 무관한 ignore 편집을 하거나 격리를 위한 setup commit을 만들지 않습니다.
격리를 입증할 수 없으면 변경 전에 `Blocked`를 반환합니다. 호스트가 관리하는 workspace lifecycle을 보존합니다. 완료 시 제거, prune, 이동 또는 정리를 하지 않습니다.

<a id="index-only-commit"></a>
### Index-only 커밋

문자열 리터럴을 제외한 일반 주석, 문서 또는 동작 보존을 입증할 수 있는 다른 텍스트이며 로컬 빌드/테스트나 런타임 검증이 필요하지 않을 때만 이 direct 경로를 사용합니다. 실행 가능한 문서, 에이전트 지침, compiler/linter 지시문, 설정, 동작 변경, 불확실한 영향, 여러 대응 commit과 rebase는 workspace 경로를 사용합니다. 해결 계획에 index-only 격리를 명시하고 정확히 그 경로를 포함하는 승인을 요구합니다. 일치하는 현재의 독립 작업 승인이나 부모 승인은 이미 이 요건을 충족합니다. worktree 계획을 설명한 뒤 조용히 전환하지 않습니다.

1. 승인된 PR head를 `RESPONSE_BASE`로 고정합니다. 저장소/PR/브랜치/식별 정보를 새로 읽고 구성 전에 원격 head가 일치하도록 요구합니다. 부모 index를 새로 고치지 않은 채 부모의 HEAD/브랜치, 실제 index 바이트와 추적/미추적 작업 상태를 기록합니다. 기존 무관한 변경은 손대지 않고 이 commit의 입력으로 사용하지 않습니다.
2. 쓰기 전에 기존의 실제 적용 `.tigerkit/` 제외가 있어야 하며 산출물 경로 안전/소유권 검사를 통과해야 합니다.
   제외가 없으면 workspace 경로를 사용하거나 `Blocked`를 반환합니다. index-only에서 부모 ignore 설정을 실행하지 않습니다.
   후보 바이트와 처음에는 존재하지 않는 절대 경로 `GIT_INDEX_FILE`에 고유한 실행 소유 `.tigerkit/tmp/tk-pr-respond/<run-id>/`를 사용합니다. 변수 범위를 각 index 명령이나 subshell로 한정하고 이후 호출자 환경을 복원합니다. `-u` 없이 `git read-tree "$RESPONSE_BASE"`로 채웁니다. 부모 checkout이 아니라 정확한 해당 Git tree에서 소스 바이트와 파일 모드를 읽습니다. checkout, stage, reset, stash나 브랜치 전환을 하지 않으며 부모의 HEAD, 실제 index 또는 로컬 branch ref를 갱신하지 않습니다.
3. `commit-tree`는 commit hook(Husky/commitlint 포함)을 우회하므로 저장소의 commit 메시지 및 서명 요건을 명시적으로 검증합니다. `RESPONSE_BASE`를 기준으로 검증한 설정/의존성을 사용해 `--stdin-filepath <original-path>` 또는 지원되는 동등한 기능으로 후보 stdin에 저장소 formatter를 실행합니다. 포맷된 바이트를 비교하고 매핑된 변경만 유지합니다. 필수 포맷, 서명이나 다른 hook 의무를 checkout 없이 충족할 수 없으면 workspace 경로를 사용합니다. 무관한 부모 파일에 대해 빌드/테스트를 실행하지 않습니다.
4. `git hash-object -w`로 승인된 후보 바이트만 저장합니다. 정규 저장 blob 형식으로 편집했으면 `--no-filters`를 사용합니다. 작업 형식 바이트에는 `RESPONSE_BASE`를 기준으로 attributes/filters를 검증한 경우에만 `--path=<original-path>`를 사용합니다. 더러운 부모의 attributes를 적용하거나 이미 정규화된 blob을 두 번 clean 처리하지 않습니다. 임시 index를 사용해 `git update-index --cacheinfo <original-mode>,<blob>,<path>`로 항목을 교체합니다.
   `git write-tree`로 tree를 만듭니다. 정확한 name-status, diffstat, 전체 diff와 지적 매핑을 조사하고 기존 독립 검토 프로토콜을 적용합니다. `git commit-tree <tree> -p "$RESPONSE_BASE"`로 commit 하나를 만들기 전에 head 변경을 다시 확인합니다. SHA를 `COMMIT`으로 기록합니다. `RESPONSE_BASE..COMMIT`을 비교하고 push 전과 발행 후에 부모 상태가 바뀌지 않았는지 검증합니다. 소유한 무시된 실행 파일과 허용된 object store 쓰기만 제외합니다.
5. 검토 범위, 조상 관계, 발행과 현재 head 근거에는 무관한 부모의 `HEAD`가 아니라 `COMMIT`을 사용합니다.
   기존의 모든 발행 보호 조건을 다시 확인하고 원격 head가 여전히 `RESPONSE_BASE`와 같아야 합니다. `git push <remote> "${COMMIT}:refs/heads/<approved-branch>"`로 일반 fast-forward만 push합니다. 중괄호는 zsh의 `$C:r` modifier가 refspec을 손상하지 않도록 합니다. force, rebase 또는 변경된 상태의 덮어쓰기를 하지 않습니다. 상태 변경/거절 시에는 승인 없이 새 head를 대상으로 재시도하지 말고 후보를 보존하고 계획 변경을 위해 중단합니다.
6. push 후 정확한 원격 head와 CI 빌드/테스트 결과를 새로 읽습니다. 대기 중인 검사는 `Pending`, 실패한 검사는 `Fail`, 없거나 검증할 수 없는 필수 검증 범위는 `Unverifiable`입니다. 현재 head 빌드/테스트 성공과 기존의 모든 답글/스레드/요약/재검토 의무를 충족한 뒤에만 `Pass`를 주장합니다. 이 경로는 추가 발행 또는 정리 권한을 부여하지 않습니다. 미발행 후보 복구 데이터를 보존합니다. 성공 후에는 소유한 임시 파일만 제거합니다.

<a id="seed-selection"></a>
## Seed 선택

대화와 최신 PR 근거로 충분한 작고 명백한 직접 수정에는 Seed를 사용하지 않습니다. 새 자식 실행, 지속 맥락, 복잡한 검증 또는 여러 중요한 Unit이 있는 SDD에는 Ready Seed를 사용합니다. `pr-respond.md`를 만들지 않습니다.

승인 전에는 기존 Seed를 바이트 단위로 보존하고 `Status: Pending` 파일을 만들지 않습니다. 승인 후 필요한 Ready Seed를 원자적으로 쓰고 다시 읽으며 `<!-- tigerkit:seed -->`와 결정적인 PR/head/작업 식별 정보를 요구합니다.
TigerKit 소유임이 입증된 Seed만 교체합니다. 마커가 없거나, legacy이거나, 식별 정보가 모호한 파일은 보존하고 `Blocked`를 반환합니다.

Seed는 사용자에게 보이는 설명을 한국어로 작성하며 정확한 저장소/PR/head, 피드백과 요청 결과, 각 지적의 승인된 처리 분류와 근거, 목표, 범위와 제외 사항, 결정, 구현 근거, 중요한 Reuse/Simplicity/Tests/Security/Experience 공백 또는 예외, AC별 검증, 브라우저 계획, 발행 경계, 의미 중심 Review Plan과 역량이 더 낮은 실행자를 위한 지침을 포함합니다. Review Plan은 검토자 수나 provider/worker routing 없이 의도, 예상 시나리오/결과, `must-not-change` 영역, 변경 책임 범위의 위험 경계, 필수 근거와 알려진 불확실성을 기록합니다. 어떤 축이 준비되었거나 관련 없음을 나타내기 위한 준비 상태 행을 추가하지 않습니다. 정확히 일치하는 활성 Seed를 다시 쓰지 않습니다. 중요한 피드백이나 상태 변경이 있으면 원자적 교체 전에 변경 부분의 승인이 필요합니다. direct/no-Seed 경로는 Seed 형식 절차를 만들지 않고 현재 승인된 대화에 같은 의미 중심 Review Plan을 보존합니다. 승인된 검토자 의도, 테스트와 발행에 계속 구속됩니다.

<a id="response-delta-discipline"></a>
## 대응 변경분 규율

변경 전에 `RESPONSE_BASE`를 정확히 승인된 PR head로 기록합니다. `RESPONSE_BASE..HEAD`(index-only는 `RESPONSE_BASE..COMMIT`)의 모든 제품 코드 또는 테스트 hunk는 승인된 `fixed` 지적 하나 또는 그 수정에 필요한 최소 인수 조건 및 회귀 보호에 대응해야 합니다. 지원 변경은 매핑된 대응을 빌드, 테스트 또는 검증하는 데 필요한 경우에만 허용됩니다. 기회에 편승한 리팩터링, 정리, 포맷, 의존성 업데이트나 인접 수정을 포함하지 않습니다.

commit 전과 push 전에 다시 name-status, diffstat와 전체 대응 diff를 지적 매핑과 대조합니다.
workspace는 `RESPONSE_BASE..HEAD`, index-only commit 전에는 후보 tree, 이후에는 `RESPONSE_BASE..COMMIT`을 사용합니다. 실행이 소유한 매핑되지 않은 변경을 안전하게 제거합니다. 승인 범위나 무관한 작업을 바꾸지 않고 매핑되지 않은 변경을 분리할 수 없으면 발행하지 말고 계획 변경을 위해 중단합니다.

<a id="execution"></a>
## 실행

- Index-only는 direct로 유지합니다. 동작하지 않는 텍스트임이 입증되면 테스트 `N/A`, 정확한 tree/범위 독립 검토와 push 후 현재 head CI에 위 보호 조건을 적용합니다. 아래 checkout/TDD/로컬 commit 단계는 workspace 경로에 적용합니다.
- `direct+TDD`: 하나의 일관된 변경 및 검토 범위입니다. 테스트 참조와 안전성이 입증된 checkout을 사용합니다.
- `SDD+TDD`: 여러 중요한 Unit이 있습니다. [비공개 SDD](../../tk-engineering/references/sdd.md)를 읽고 문법, 복구, 역할 관문, model 및 effort 계약, 수정 반복과 최종 검토를 따릅니다.

Direct 실행은 [동작 우선 테스트](../../tk-engineering/references/testing.md)를 따릅니다. 변경된 동작에는 RED → 검증된 실패 → 최소 GREEN이 필요합니다. 동작 보존 리팩터링에는 편집 전 GREEN → 리팩터링 → 대응 GREEN이 필요합니다. 필수 검사를 실행합니다.
SDD Unit 보고서는 해당 RED/GREEN 또는 전후 GREEN 근거를 유지합니다. fan-out을 사용할 수 없으면 같은 역할 및 범위 관문을 순차적으로 보존합니다. 검토 없는 direct 작업으로 낮추거나 provider routing을 영속화하지 않습니다.

구현 후 [독립 검토 프로토콜](../../tk-engineering/references/review-protocol.md)에서 요구하는 신뢰하지 않는 구현 회고를 구성합니다. direct의 정확한 변경 검토와 SDD Unit/전체 변경 검토에 해당 프로토콜을 적용합니다. 위험 기반 direct 검토 자리 수를 사용합니다. SDD 전체 변경 최종 검토는 여전히 맥락이 격리된 탐색 자리 두 개를 사용하고 각 SDD Unit은 새 자리 하나를 사용합니다. 모든 자리는 `Spec/AC`와 `Quality/Standards`를 모두 판단하고 두 점검을 모두 완료합니다. blind pass가 끝날 때까지 회고를 제공하지 않고, 후보 합집합을 모으며, 보고 가능한 모든 후보를 별도로 검증합니다. AC 검토, 필수 공백 수정, 검증된 로컬 commit과 브라우저에 보이는 변경의 `tk-browser-verify`로 마무리합니다. 검증 담당자에게 정확한 명령/cwd/URL/인증/준비 상태를 제공합니다. 서버 lifecycle은 검증 담당자가 소유합니다. SDD 전체 변경 검토를 또 다른 일반 검토로 반복하지 않습니다.

모든 코드 검토에 [지적 품질](../../tk-engineering/references/finding-quality.md)을 적용합니다. 검토 범위가 해당 참조의 조건에 맞을 때만 [TypeScript](../../tk-engineering/references/typescript.md), [React](../../tk-engineering/references/react.md), [보안](../../tk-engineering/references/security.md)을 읽습니다. 이 관점들은 지적의 처리 분류, 대응 변경분, 재검토 대상 또는 발행 순서를 바꾸지 않습니다.

Direct 검토 수정은 최대 다섯 라운드로 처리합니다. 편집할 때마다 광범위한 탐색을 다시 실행하지 말고, 원래 열린 지적, 정확한 수정 diff와 수정이 직접 영향을 줄 수 있는 변경되지 않은 호출자/피호출자 또는 생산자/소비자 계약만 사용합니다. 새 `Critical`/`Important` 지적은 근거가 직접 영향받는 변경되지 않은 경계에 있는 경우를 포함하여 수정에 인과적으로 귀속될 때만 추가합니다. 5라운드 후에는 `Fail` 또는 `Unverifiable`로 중단합니다. SDD도 같은 최대 횟수를 사용합니다.
중요한 Goal/Scope/Decision/AC/보안/필수 Verification 변경은 준비 담당자에게 돌려보냅니다. 되돌릴 수 있는 엔지니어링 모호성에는 명시적인 `Ruling:`을 내립니다. 어느 경로도 발행 권한을 확대하지 않습니다.
