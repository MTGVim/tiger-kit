<a id="retrospective-stack-split"></a>
# 구현 후 스택 분할

`tk-pr-open`에 이미 구현·검증된 작업이 한 브랜치에 있고, 리뷰 가능성 사전 점검에서 `stacked` 발행을 선택하거나 진지하게 검토하는 경우에만 읽습니다.

<a id="upstream-boundary"></a>
## upstream 경계

주요 upstream은 GitHub의 공식 `github/gh-stack` 스킬과 CLI 계약입니다.

유지합니다.

- 하위→상위의 선형 의존 계층을 유지합니다.
- 계층당 관심사 하나와 스택당 일관된 이야기 하나를 유지합니다.
- 비대화형 `gh stack init <branch>...`, `gh stack submit --auto`, `gh stack view --json` 사용을 유지합니다.
- ready PR에는 `submit --auto --open`, draft PR에는 `submit --auto`를 사용합니다.
- 정확한 명령 도움말을 런타임 정본으로 사용합니다.

적응합니다.

- upstream은 구현 전에 스택을 만들 것을 적절히 권고합니다.
- TigerKit은 `tk-pr-open`이 발행 전에 이미 구현·검증된 작업을 받기 때문에 좁은 범위의 사후 경로를 지원합니다.
- 이 경로는 소스 브랜치를 재작성하지 않고, 보존된 소스 브랜치 옆에 새 발행 브랜치를 재구성합니다.

제외합니다.

- 대화형 `gh stack modify`나 그 밖의 TUI 전용 재구성을 제외합니다.
- 확장 기능 자동 설치를 제외합니다.
- 공식 stacked PR을 사용할 수 없을 때 일반 PR을 임의로 연결하여 GitHub Stack인 것처럼 취급하는 방식을 제외합니다.

<a id="eligibility"></a>
## 적용 조건

다음 조건을 모두 충족할 때만 구현 후 스택 구성을 사용합니다.

- 소스 worktree가 깨끗하며 정확한 소스 브랜치, `HEAD`, 트리, base와 커밋 범위가 입증되어 있어야 합니다.
- 같은 head의 PR이 아직 없어야 합니다. 이미 리뷰되거나 발행된 PR을 알리지 않고 스택으로 이전하지 않습니다.
- 변경에는 하나의 기능·프로젝트에 속하면서 선형 의존 사슬을 구성할 수 있는, 독립적으로 리뷰 가능한 관심사가 둘 이상 있어야 합니다.
- 제안된 각 계층을 한 문장으로 설명할 수 있고, 저장소 요구사항에 맞게 충분히 빌드·테스트 가능한 상태를 유지할 것으로 예상되어야 합니다.
- 브랜치 이름이 로컬과 발행 원격에서 충돌하지 않아야 합니다.

원시 LOC가 크다는 이유만으로 스택을 구성하지 않습니다. 생성 파일, lockfile, 스냅샷, vendoring된 산출물과 기계적 대량 변경은 담당 관심사를 따르지만 그 자체로 계층을 만들지는 않습니다.

관심사가 서로 무관하면 하나의 스택에 억지로 넣지 말고 중단합니다. 의존 그래프가 선형이 아니라면 계층 수를 줄이거나 단일 PR을 유지합니다. 같은 파일에 여러 관심사의 분리할 수 없는 변경이 있다면 담당 계층 하나에 배정하거나 분할 단위를 크게 조정합니다. 목표 PR 크기에 맞추려고 취약한 hunk 분할을 만들어 내지 않습니다.

<a id="tool-provenance"></a>
## 도구 출처

승인 전에 확장 기능 자체를 실행하지 않고 `gh extension list`를 확인합니다.

적격 도구는 저장소가 정확히 `github/gh-stack`인, 모호하지 않은 설치된 확장 기능입니다. `gh stack` 설치가 없거나, 중복되거나, 모호하거나, 출처가 다르면 사용할 수 없는 것으로 취급합니다.

확장 기능을 자동으로 설치하거나 교체하지 않습니다. 공식 확장 기능이 없다면 발행 계획을 `Pending`으로 유지하고 사용자에게 공식 설치 경로나 단일 PR을 제안합니다.

승인 후 변경 전에 `gh stack <command> --help`를 옵션에 관한 최신 정본으로 사용합니다. 인자 없는 대화형 형태는 피합니다. 원격이 여러 개라면 `remote.pushDefault`를 요구하거나, 명령이 지원하는 모든 곳에 정확히 승인된 `--remote <name>`을 전달합니다.

<a id="preserve-the-source-snapshot"></a>
## 소스 스냅샷 보존

소스 브랜치는 복구 산출물입니다. 사후 분할의 일부로 reset, rebase, 이름 변경, 강제 push나 삭제를 하지 않습니다.

다음을 기록합니다.

```text
SOURCE_BRANCH=<current branch>
ORIGINAL_HEAD=<exact approved HEAD>
ORIGINAL_TREE=<git rev-parse "$ORIGINAL_HEAD^{tree}">
BASE_REF=<approved base ref after fresh fetch>
BASE_TIP=<fresh base tip used to prove target drift>
BASE_ANCHOR=<git merge-base "$ORIGINAL_HEAD" "$BASE_REF">
```

재구성 직전에 이 값을 재검증합니다. 소스 `HEAD`, base ref나 base tip에 변동이 있으면 승인은 무효가 됩니다. 더 최신 base tip이 아니라 `BASE_ANCHOR`에서 재구성합니다. 이렇게 하면 기능 브랜치가 갈라진 뒤 대상 브랜치가 앞서 나갔더라도 이미 검증된 정확한 소스 트리를 보존합니다.

<a id="design-the-layers"></a>
## 계층 설계

전체 `BASE_ANCHOR...ORIGINAL_HEAD` diff와 커밋 이력에서 의미상 소유권을 분석합니다. 다음과 같은 경계를 우선합니다.

```text
foundation/types/schema
→ domain/API/core implementation
→ UI/integration
→ end-to-end or cross-layer acceptance
```

이 이름은 예시이며 기본값이 아닙니다. 저장소의 브랜치·제목 관례가 우선합니다.

기존 커밋이 의존성 순서대로 승인된 계층에 이미 명확하게 대응할 때만 온전한 커밋을 우선합니다. 그렇지 않으면 승인된 소스 스냅샷에서 경로 소유권에 따라 재구성합니다. 리뷰 가능성을 희생하면서 우연히 생긴 커밋 경계를 보존하지 않습니다.

승인 전에 각 계층에 대해 다음을 기록합니다.

- 다중 PR 계획이 있다면 계획된 PR 그룹과 Unit 전체의 소유권, 의존성, 공유 산출물의 단일 생성 주체, 보호 장치와 중간 상태 검사를 기록합니다. [다중 PR 전달의 안전](../../tk-pr-guidance/references/multi-pr-delivery.md)과 대조하고, 알리지 않고 그룹을 재구성하지 않습니다.
- 정확한 브랜치 이름과 부모를 기록합니다.
- 한 문장으로 된 리뷰 관심사를 기록합니다.
- 정확한 소유 경로나 온전한 소스 커밋을 기록합니다.
- 정확한 PR 제목·본문을 기록합니다.
- 템플릿과 근거의 소유권을 기록합니다.
- 계층이 의도적으로 고장 난 상태가 아님을 입증하는 최소한의 관련 검증을 기록합니다.

각 계층에서 파일은 하나의 확정적인 상태를 가져야 합니다. 새 제품 코드를 작성하지 않고는 경로 수준 재구성으로 의도한 중간 상태를 표현할 수 없다면, 표현할 수 있을 때까지 관심사를 합칩니다.

`.tigerkit/pr-open.md`의 스택 섹션을 다음의 정확한 필드로 기록합니다.

```text
Source branch: <preserved original branch>
Stack tooling/provenance: <verified github/gh-stack | unavailable>
Layers bottom → top:
- Branch
- Parent/base
- Reconstructed commit/tree
- Exact title/body
- Title convention basis
- Template/evidence ownership
- Layer verification
- Planned PR group/Units, dependencies, shared creators and merge-state safety checks (when supplied)
Expected stack-tip tree: <original tree>
```

승인 전에 정확한 하위→상위 사슬과 보존되는 원본 트리 불변 조건을 사용자에게 자연스럽게 제시합니다.

<a id="reconstruct-beside-the-source-branch"></a>
## 소스 브랜치 옆에 재구성

정확한 승인을 받은 뒤에만 소스 브랜치를 변경하지 않고 새 스택 브랜치를 만듭니다.

경로 소유 계층의 안전한 형태는 다음과 같습니다.

```text
BASE_ANCHOR
  └─ <topic>/<layer-1>
       └─ <topic>/<layer-2>
            └─ <topic>/<layer-3>

preserved separately:
SOURCE_BRANCH -> ORIGINAL_HEAD
```

첫 브랜치는 `BASE_ANCHOR`에서 만들고 이후 브랜치는 각각 앞선 계층에서 만듭니다. 승인된 소스 경로만 복원하거나 승인된 온전한 커밋만 재사용합니다. 재구성 커밋마다 그 전에 staged 경로를 확인하고 해당 계층 밖의 내용이 있으면 중단합니다.

경로 기반 복원은 소스 커밋을 내용의 정본으로 사용할 수 있습니다. 예를 들면 다음과 같습니다.

```bash
git restore --source "$ORIGINAL_HEAD" --staged --worktree -- <approved-paths...>
git diff --cached --name-status
git commit -m "<approved layer commit subject>"
```

정확한 명령은 저장소 상태, 이름 변경, 삭제나 온전한 커밋 재사용에 따라 달라질 수 있습니다. 불변 조건은 달라지지 않습니다. 재구성은 이미 승인된 소스 내용을 선택하며 제품 내용을 수정하지 않습니다.

불명확한 계층을 보완하려고 `git add -A`를 사용하지 않습니다. 스택을 쉽게 만들려고 소스 브랜치를 재작성하지 않습니다.

<a id="verify-every-layer"></a>
## 모든 계층 검증

각 계층을 커밋한 뒤 다음을 수행합니다.

1. 브랜치 부모와 staged·커밋된 경로의 소유권을 확인합니다.
2. 검증된 작업·Seed·현재 저장소 계약에서 계층이 의도적으로 고장 난 상태가 아님을 입증하는 최소한의 관련 저장소 검사를 실행합니다.
3. 계층이 독립적으로 성립할 수 없다면 고장 난 중간 PR임을 알면서 발행하지 말고 인접한 관심사와 합칩니다.

원격 쓰기 전에 손실 없는 최종 불변 조건을 입증합니다.

```bash
STACK_TIP=<top reconstructed branch>
test "$(git rev-parse "$STACK_TIP^{tree}")" = "$ORIGINAL_TREE"
git diff --exit-code "$ORIGINAL_HEAD" "$STACK_TIP" --
```

두 검사 모두 통과해야 합니다. 트리 동일성이 주요 불변 조건이며 빈 diff는 읽기 쉬운 확인 수단입니다. 실패하면 `Blocked`로 중단하고 소스 브랜치를 그대로 둡니다.

<a id="adopt-and-submit-with-gh-stack"></a>
## `gh-stack`으로 편입하고 제출

로컬 검증 후 공식 확장 기능으로 이미 생성된 브랜치 사슬을 편입합니다. 기존 브랜치는 하위에서 상위 순서로 전달합니다.

```bash
git config rerere.enabled true
gh stack init <layer-1> <layer-2> <layer-3> [--base <non-default-base>]
```

선택적 옵션을 맹목적으로 복사하지 말고 현재의 정확한 `--help` 구문을 사용합니다. 첫 계층은 `BASE_ANCHOR`에서 시작하므로 현재 대상 tip보다 뒤처질 수 있습니다. 최초 발행 전에 최신 상태로 만들겠다는 이유만으로 `gh stack sync`나 자동 rebase를 실행하지 않습니다. rebase는 검증된 소스 스냅샷을 바꾸므로 실제로 필요하다면 새로운 정확한 계획이 필요합니다.

`gh stack view --json`이 예상 로컬 사슬을 입증한 뒤에만 제출합니다.

```text
ready -> gh stack submit --auto --open
 draft -> gh stack submit --auto
```

`submit`은 원자적이지 않습니다. 실패하기 전에 일부 브랜치를 push하거나 PR을 만들었다면 삭제하거나 닫거나, 알리지 않고 다른 발행 경로로 재시도하지 않습니다. 원격 스택·PR 상태를 다시 읽고 정확한 부분 결과를 보고합니다.

저장소에서 stacked PR을 사용할 수 없다면 알리지 않고 일반 연결 PR로 전환하지 않습니다. 실제 원격 상태를 보존하고 차단 요인을 보고하며 사용자에게 새로운 선택을 받아야 합니다.

<a id="restore-exact-pr-metadata"></a>
## 정확한 PR 메타데이터 복원

`gh stack submit --auto`는 브랜치나 커밋 메타데이터에서 PR 제목·본문을 도출할 수 있습니다. 제출 후 `gh stack view --json`으로 승인된 각 계층을 실제 PR에 대응시킨 뒤, 해당 PR만 정확히 승인된 제목·본문과 상태로 수정합니다.

모든 PR을 다시 읽고 다음을 확인합니다.

- 하위→상위 base/head 관계를 확인합니다.
- 정확한 제목·본문과 템플릿 준수를 확인합니다.
- 요청된 `draft | ready` 상태를 확인합니다.
- 근거 소유권·상태를 확인합니다.
- 재구성된 계층의 head SHA를 확인합니다.

스택을 merge하지 않습니다. 보존된 소스 브랜치를 삭제하거나 강제 push하지 않습니다.

<a id="failure-result"></a>
## 실패 결과

로컬 재구성 후 원격 발행 전에 실패하면 새 로컬 발행 브랜치만 남고 원본 소스 브랜치는 바뀌지 않습니다.

`submit`은 원자적이지 않으므로 `submit` 이후 실패하면 원격 브랜치·PR이 남을 수 있습니다. 해당 객체를 정확히 보고하고 상황에 따라 `Blocked`나 `Fail`을 반환합니다. 검증하지 않은 롤백을 주장하지 않습니다.
