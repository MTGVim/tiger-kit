# TigerKit 저장소 지침

## 제품 경계

TigerKit은 워크플로 실행기, 플러그인, 공유 상태 프레임워크가 아니라 `Agent Skills`
저장소입니다.

- 각 `skills/tk-*` 패키지는 자체 완결형으로 유지합니다.
- `SKILL.md`가 실행 동작을 소유하고, 패키지 로컬 `references/`, `scripts/`,
  `agents/`, `evals/`가 조건부 세부사항과 실행 가능한 증거를 소유합니다.
- `.claude-plugin/`, `commands/`, 전역 TigerKit 상태, 호스트별 스킬 본문 복사본,
  GitHub Actions 검증을 복원하지 않습니다.
- 중복된 의식보다 삭제와 점진적 공개를 우선합니다.
- 정본 운영 문장과 사용자 노출 문장은 한국어로 작성합니다. 다만 정확한 상태, ID,
  명령, 경로, 리터럴과 필요한 기술 분류명은 안정성을 위해 원문을 유지합니다.

## Skill 존재 규율

Skill에는 독립적인 호출 또는 좁은 자동 trigger, 일반적인 모델 동작과 실질적으로 다른
절차, 객관적인 완료 기준, 그리고 소유하는 산출물·변경·승인 또는 안전 경계가
필요합니다.

Skill을 추가하거나 유지하기 전에 다음을 확인합니다.

1. 사용자 또는 문서화된 상위 기능이 이를 호출할 실제 이유가 있습니다.
2. 긍정·부정 trigger 사례가 인접 동작과 이를 구분합니다.
3. 성공·경계 평가 경로가 존재합니다.
4. 카탈로그 라우팅 또는 다른 문서화된 소비자가 이를 참조합니다.
5. 이를 제거하면 측정된 작업 품질이 낮아집니다.

약한 후보는 인라인 처리, 병합, 조건부 reference로 전환, 명시적인 사용자 호출 방식으로
변경하거나 삭제해야 합니다. `scripts/audit_catalog.py`는 정본 계약에서 이 증거를
도출합니다. `scripts/run_drive_experiment.py`가 측정된 `RemoveCandidate` 결과를
보고한 경우에만 `tk-drive`를 제거 검토 대상으로 표시할 수 있습니다.

## 핵심 경계

- `tk-drive`는 명시적인 제품 변경 조정자입니다. `tk-pr-sweep`는 다중 PR 유지보수만
  담당하는 좁은 두 번째 명시적 조정자입니다. 다른 단계 소유자는 형제 단계 소유자를
  호출하지 않습니다. 계속하기는 프롬프트가 지시하며 영속적인 일정 실행이 아닙니다.
- `tk-ask-repo`는 읽기 전용 조사만 수행하며 절대 구현하지 않습니다.
- `tk-drive`와 `tk-pr-respond` 제어기는 제품 변경을 직접 작성하지 않습니다. 새 작업자가
  한 번에 하나의 범위가 정해진 후보를 만듭니다.
- 필수 검증기와 R/AC 간극 해소를 거친 뒤 단위마다 검증된 커밋 하나를 만듭니다. 최상위
  소유자는 마지막 기계적 Git 장부 처리만 수행할 수 있습니다.
- `tk-drive`는 전체 추적성, 계보, 단위 간 검증, 마무리를 소유합니다.
- 사용자에게 보이는 동작을 위한 브라우저 도구는 `tk-browser-verify` 안에서 실행합니다.
- Push, PR, merge, tag, release, publish에는 별도의 명시적 권한이 필요합니다. 명시적
  `tk-pr-sweep`는 문서화된 범위의 PR 유지보수 권한만 제공합니다.
- 하나의 `workspace_backend`로 작업 트리 생성과 작업자 배정을 함께 선택하고 고정합니다.
  `git-native`는 이 저장소에서 확인된 fallback이며, `orca` 또는 `paseo`는 현재 호스트가
  작업 트리·배정·receipt를 모두 증명할 때만 선택합니다. 두 기능을 서로 다른 backend로
  조합하면 변경 전에 row를 `Blocked`로 둡니다.
- 기본 `tk-pr-sweep`는 원격 발행을 하지 않습니다. 이미 작업·검증·commit을 끝냈지만
  호스트 권한 판정이 마지막 원격 쓰기만 막은 row에 한해, 사용자가 정확히
  `--recover-publication`을 명시하고 별도 approval을 준 경우에만 고정된 refspec과
  원격 HEAD를 다시 확인한 뒤 한 번의 `git push --force-with-lease`를 수행할 수
  있습니다. 이 guard가 하나라도 없으면 direct fallback이 아니라 `Blocked`로 멈춥니다.
- 작은 작업과 일반적인 후속 feedback은 현재 대화에서 처리합니다.

## Eval 정본

다음 파일만 실행 가능한 평가 동작을 소유합니다.

```text
skills/<skill>/evals/triggers.json
skills/<skill>/evals/evals.json
evals/catalog-routing.json
evals/release-critical.json
evals/drive-ab.json
```

생성된 `test-prompts.json`, 루트 trigger/behavior 미러 fixture, Darwin projection,
또는 정본 case ID를 복제하는 Python 목록을 추가하지 않습니다. validator는
`skills/tk-*`를 자동 검색합니다. 정당한 skill을 추가하거나 삭제할 때 Python의
카탈로그 개수 수정이 필요해서는 안 됩니다.

eval을 변경할 때는 다음을 지킵니다.

- 사례는 정확한 `id`로 지정합니다.
- 기존 사례 ID를 보존하거나 명시적으로 migrate합니다.
- 동작 사례마다 적어도 하나의 기계적 assertion을 유지합니다.
- 문서화된 migration으로 대체하지 않는 한 안전성, 호스트 coverage, terminal strictness,
  nonterminal assertion을 보존합니다.
- release-critical reference가 정본 사례로 resolve될 수 있게 유지합니다.

## Host 품질

`scripts/adapters/tigerkit_host_adapter.py`는 기본 실시간 adapter입니다. 격리된 home에서
Codex, Claude Code, Hermes Agent 순서로 시도합니다. runtime이 없거나 사용할 수 없으면
결정적 성공 또는 실패가 아니라 quality `Advisory`입니다. 사용자 지정 adapter는 명령을
override할 수 있지만 동일한 JSON protocol을 반환해야 합니다.

adapter의 selected-skill 및 단계 event는 호스트 실행이 생성한 eval-envelope evidence입니다.
호스트가 해당 telemetry를 직접 노출하지 않는다면 이를 하위 runtime telemetry로
제시하지 않습니다.

## State와 문서

Runtime scratch는 저장소·작업 트리 로컬 `.tigerkit/`에 둡니다. 전역 archive, 현재 pointer
또는 자동 migration은 만들지 않습니다. branch 결정은 spec, tickets, commits, PRs, code,
tests에 남깁니다. 장기적인 저장소 제약에 대한 명시적인 요청이 있을 때만 ADR을 만듭니다.

## 필수 검사

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

패키징 변경에서는 임시 home에 지원되는 모든 호스트를 smoke-install합니다. release
quality를 확인할 때는 결정적 로컬 `scripts/run_release_gate.py`를 실행하고, drive 보존
증거를 확인할 때는 `scripts/run_drive_experiment.py`를 실행합니다. 모든 validation은
local-only로 유지합니다.
