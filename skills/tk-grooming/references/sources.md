<a id="grooming-source-dispositions"></a>
# Grooming 출처별 판단

<a id="model-fit-audit"></a>
## 모델 적합성 감사

`anthropics/skills`의 `683bc88e56f3e09ba94f7055977f3d3aa499f202`에서
`skills/claude-api/shared/prompt-audit.md`, 그 안의 설계 이유와 검증 절차,
그리고 `skills/claude-api/shared/model-migration.md`의 대상 모델 절을 검토했습니다.
출처는 Apache-2.0이며 비교 자료입니다. 가져와 포함한 텍스트나 런타임 코드가 아닙니다.
prompt-audit의 별도 upstream 동작 평가 결과는 `unverified`입니다.

- `keep`: 대상에 따른 근거, 작성자 맥락과 순서 등에 민감한 계약의 보존, 확신도를 명시한 관찰과 유효한 문제없음·변경 없음 결과를 유지합니다.
- `adapt`: 압박, 출력 제한, 버전 상대적 문장, 런타임 이력, 오래된 사실, 충돌하는 지침, 정확한 문구 모드와 오래된 평가 기대를 기존 GR 발견 사항으로 전환합니다. 명시적인 사용자 형식은 계속 구속력을 가집니다. 모델별 주장에는 최신 1차 근거가 필요합니다. 기존 소유권과 기계적·의미적 권한 구분이 행동을 결정합니다.
- `adapt`: 출처는 조건부 유지보수 기록으로 두고, 동작 비교는 기존 지침 경제성 참조에서 계속 담당합니다. 충돌은 Git 최신성과 관계없이 보류합니다.
- `omit`: 애플리케이션·API 이전, 요청 builder, 도구 description 감사, 모델 라우팅, 자동 광범위 목록 조사, 필수 보고·diff 산출물과 upstream 구현·fixture를 제외합니다.

TigerKit의 구체적인 부족은 임의적인 출력 제한과 서로 다른 패키지 내부 계약이었습니다.
이 분기는 호출 종류, description, vendor 소유권이나 기존 적용 경계를 바꾸지 않고 대상 모델
분류를 추가합니다. 로컬 사례는 이전 동작과 후보 동작을 비교하며, 모든 대상 모델에서의 효과를
입증하지는 않습니다.

<a id="external-behavior-copies-and-usage-evidence"></a>
## 외부 동작 사본과 사용 근거

유지보수 보고서는 구체적이며 독립적으로 확인한 감사 결과 두 가지를 제공했습니다.
네이티브 실행 진단에서는 비활성 스킬을 찾았지만, 맥락이 없는 grooming 감사에서는 경로·lock·내용을
사용하여 새로운 비활성을 찾지 못했습니다. 현재 변경 전 Workflow,
`instruction-economy.md`와 `discovery.md`의
`26890b22bccb54a02f681ac621082a9930dff61c` 내용은 사용 근거 분기와 의도적인
외부 동작 사본의 기준판·설치판 비교가 없음을 확인해 줍니다. 이는 검증된 재사용 가능한 사고 사례이며,
새 upstream 구현 의존성이 아닙니다. 원래 호스트의 비공개 counter, plugin 내부와 진단 구현은
여기서 `unverified`로 남습니다. 호스트별 counter 경로나 schema를 단정하지 않습니다.

- `keep`: 조회 비용이 커서 의도적으로 만든 사본, 현재 호스트만의 탐색, 기존 보고 전용 호스트 설정·vendor 경계와 영속 TigerKit registry를 두지 않는 원칙을 유지합니다.
- `adapt`: 버전 출처와 설치 규칙 비교를 지침 경제성 안에 두고, 사용 의미와 관찰 범위는 범위별 참조 pointer 하나 뒤에 둡니다.
- `omit`: 모델 라우팅, 원시 세션 데이터, telemetry 수집, 자동 비활성화, 추측한 counter schema와 호스트 간 런타임을 제외합니다. 합성 평가 사례는 원래 환경의 세부사항을 공개하지 않고 결정 경계를 시험합니다.

<a id="copied-external-skill-provenance"></a>
## 복사 설치 외부 스킬의 출처와 변경

[Skill Constellations](https://github.com/FahdSeddik/Skill-Constellations/tree/97a1a46783f77d2dc9c63c33bb102e11b9ed36d1)의
고정 revision `97a1a46783f77d2dc9c63c33bb102e11b9ed36d1`에서 `README.md`, `LICENSE`와
`ui/skillnet_ui/pages/replay.py`를 읽었습니다. README는 Git 이력으로 복사 계보를 재구성한 데이터와 viewer를
설명합니다. replay는 미리 계산한 관찰·시뮬레이션을 보여 주며 개별 설치본의 revision 검증기는 아닙니다.
코드는 MIT, 파생 데이터는 CC BY 4.0입니다. 코드·데이터는 가져오지 않았으며 논문의 정량 결과와
upstream 시뮬레이션 재현은 `unverified`입니다. 이 자료로 보안 효과나 결함 확산 감소율을 주장하지 않습니다.

현재 `tk-grooming/references/discovery.md`는 marketplace plugin의 버전·commit 최신성을 비교하지만
일반 복사 설치본의 전체 파일 동일성과 로컬 변경을 구분하지 않습니다. `tk-setup-skills`는 식별·의존성
호환성만 검증하고 내용 최신성을 보장하지 않습니다. `tk-skill-vet`는 고정된 snapshot과 변경 동작의
정적 위험을 검토합니다. `tk-video/references/manim.md`는 이미 선택한 외부 스킬 tree의 경로·바이트를
비교하고 설치 commit이 없으면 `content_matches_revision`만 기록합니다.

- `keep`: Manim 절차의 선택한 스킬 tree 비교, 불변 revision과 내용 동일성의 구별, 수정본 보존과 자동 설치 금지를 유지합니다. Manim 런타임의 중단·오프라인 수용 조건은 그 소유자에게 남깁니다.
- `adapt`: `B`(설치 당시 기준판)·`L`(현재 설치본)·`U`(고정 원본)를 분리하는 조건부 읽기 전용 감사를 `tk-grooming`에 둡니다. 기준판이 없으면 일치하는 현재 내용만 입증하며, 차이의 원인은 미확인으로 남깁니다. 중요한 diff의 정적 검토 필요성은 기존 `tk-skill-vet` 대상으로 표시합니다.
- `omit`: 전역 복사 계보 수집, 시뮬레이터·viewer·데이터셋, 상시 감시·registry·자동 updater, 설치본 변경과 새 독립 스킬은 추가하지 않습니다. setup·vet·Manim의 절차를 재작성하거나 의존성을 추가하지 않습니다.

<a id="harness-stocktake-structural-evidence"></a>
## Harness-stocktake의 구조 근거와 의미 판단

[shimo4228/harness-stocktake](https://github.com/shimo4228/harness-stocktake/tree/3d676093ed3ceb58071b746c16bbf4484e87dc6d)의
고정 revision `3d676093ed3ceb58071b746c16bbf4484e87dc6d`에서 `skill-health/scripts/scan_refs.py`,
`harness-stocktake/scripts/render_report.py`, `rules-stocktake/scripts/transfer_probe.py`와 Skills·Rules·Agents·Hooks·
repo-asset 감사 지침을 검토했습니다. 경로는 저장소의 `skills/` 아래입니다. 라이선스는 MIT이며,
코드·문장·템플릿을 가져오지 않고 검증 책임의 구분만 독립적으로 작성했습니다.

- `keep`: 기존 GR 단위, vendor 보고 전용, 의미 변경의 담당자 인계와 안전 규칙 보존을 유지합니다. 중복·충돌과 no-op 비교는 이미 현행 grooming이 담당합니다.
- `adapt`: 실제 로컬 참조 열거와 설정의 소비자 연결을 먼저 확인하고, 의미·가치 판정과 구분합니다. 대상이 같은 제안의 충돌을 기존 GR 근거에 모읍니다. 제거 비교에는 로드/제외와 비교 환경 확인을 요구합니다.
- `omit`: 전체 harness 감사 확대, 파일 단위 점수·줄 수 비용 목표, 전용 보고 페이지·승인 저장소·ledger, 자동 삭제와 Claude 전용 child runner는 가져오지 않습니다. 반복 모델 호출은 기본 경로에 추가하지 않습니다.

업스트림 스캐너를 합성 사례에 실제 실행했을 때 Markdown 링크와 `bash` 호출의 누락은 잡았지만
`python scripts/direct_missing.py`는 지원하지 않아 놓쳤습니다. 따라서 스캐너의 성공이나 결과 없음이
전체 참조 건전성을 보장하지 않습니다. 보고 조립기는 구조적 충돌을 모으며 의미적 상충을 판정하지
않습니다. 제거 비교 도구는 실제 child 실행 코드가 있지만 이번 환경에는 Claude CLI가 없어 실행하지
못했습니다. 업스트림의 `pyproject.toml`에는 test 경로가 선언되어 있으나 이 revision에 test 파일은
포함되지 않았습니다. 모델별 불필요 규칙 검출률과 규칙 제거 효과는 `unverified`입니다.

## 런타임 근거와 기본 진단

이번 사용자 회고와 변경 전 `4e15fc700154de5c7036f5a02d8008b6b1162776`의 본문·참조를 대조했습니다.
정적 구조 검사에는 hook 실행 금지가 있었고 사용 근거에는 세션 대조가 일부 있었으나, hook 시간·
타임아웃, 연결된 외부 memory 진단과 주입량을 담을 조건부 조사·출력 계약은 없었습니다.
사용자가 보고한 지연·진단 수치와 원래 호스트 데이터는 여기서 재측정하지 않았으며 `unverified`입니다.
주입량과 일반 감사 비용 증가도 측정 사실이 아닌 가설로 보존합니다.

최신 upstream을 조회하여 고정한 `shimo4228/harness-stocktake`
`3d676093ed3ceb58071b746c16bbf4484e87dc6d`의 `skills/hook-stocktake/SKILL.md`,
`skills/skill-stocktake/scripts/usage_stats.py`, `skills/harness-stocktake/SKILL.md`의 네이티브 진단
경계와 `LICENSE`를 다시 읽었습니다. MIT이며 코드·문장은 가져오지 않았습니다.
hook 지침은 이벤트 횟수와 실제 hook 실행을 구별하고, 집계기는 실행·읽기·합성 표본 및 실제
보존 기간을 구분합니다. 전체 감사는 네이티브 진단을 안내하며 직접 실행하지 않습니다.
이번 transcript·외부 memory·주입량 분기는 해당 upstream의 구현 이식이 아닌 TigerKit 보강입니다.

- `keep`: 현재 호스트만의 탐색, hook·감사 코드 실행 금지, vendor 보고 전용,
  지속 백업, 항목별 승인과 다른 스킬 자동 호출 금지를 유지합니다.
- `adapt`: 명시적 grooming 실행·감사 요청에는 증상 제보가 없어도 최근 7일의 기본 진단을 수행합니다.
  hook·도구 호출·사용 불일치·주입량과 연결된 외부 memory를 확인하고 이상 항목에만 상세 조사를
  추가합니다. 정적 전용·사용자 제외를 존중하고 암묵적 호출은 관련 문제에 한정합니다. 검증된 읽기 전용
  명령, 같은 기간의 호출 대조, 가설의 창 확장·cwd별 반증과 측정값·한계 표를 유지합니다.
- `omit`: 호스트 간 조사, 추측한 schema·명령, 자체 backend, 자동 정리·설정 변경, 원시 transcript
  보관, 상시 수집과 설치 점검의 중복 구현은 추가하지 않습니다. 외부 저장소 쓰기는 승인과 일관된
  지속 백업·복원 검증을 요구하는 구현 담당자의 소관으로 남깁니다.

후속 설계 검토에서 증상 요청만 기다리면 사용자가 모르는 이상을 발견하지 못한다는 한계를 확인했습니다.
동일 upstream의 최신 ref는 위 고정 revision과 같음을 다시 확인하고 hook 평가와 사용 집계의 신호·판정
분리를 재검토했습니다. 최근 7일 기본 진단과 도구 오류·재시도·복구의 분류는 TigerKit 자체 보강입니다.
도구 계약상 정상인 부정 결과·거절·취소와 실제 실패를 구분하고, 호출 분모·관찰 공백을 보존합니다.
7일 표본으로 30일 비활성을 판정하지 않으며, 오류 수만으로 결함이나 제거를 확정하지 않습니다.
실제 호스트에서의 진단 비용·탐지 효과와 도구 오류 수치는 이번 유지보수에서 측정하지 않았습니다.

## 집계 누락·상주 색인과 승인된 합성 재현 (2026-11-06)

최신 upstream ref가 위 `3d676093ed3ceb58071b746c16bbf4484e87dc6d`와 같음을 조회하고
`skills/hook-stocktake/SKILL.md`, `skills/skill-stocktake/scripts/usage_stats.py`와 해당 패키지
`pyproject.toml`을 읽었습니다. hook의 wiring·중첩 동작·테스트 확인, 실행과 읽기·합성 표본의
구별, 미측정과 0의 구분을 대조했습니다. 집계기 docstring이 지시하는 `tests/test_usage_stats.py`는
tree에 없어서 검증 구현과 upstream 실행은 `unverified`입니다. 사용자 보고의 비용·호출·타임아웃·
생성 수는 원래 환경에서 재측정하지 않았습니다.

- `keep`: 현재 호스트·승인 범위, 기본 읽기 전용·vendor 보고 전용, 미관측≠0과 실제 호출 기준을 유지합니다.
- `adapt`: 실제 plugin 호출에 연결된 자식·백그라운드 세션의 모델별 token, 첫 프롬프트×입력 길이의 hook 지연, 겹친 matcher의 반환 계약, 도구 자체 계측 우선과 노출량 추정을 추가합니다. 상주 색인의 크기·규칙/사실 구성, 저장소별 auto memory의 사용자 규칙 대조, 재권고 전 제거 이력과 생성 대비 호출도 기존 참조에 둡니다. 원인 확인이 필요하고 별도 승인·강제 격리가 입증된 사본·합성 입력만 재현합니다.
- `adapt`: 기존 grooming 지속 백업의 일반 안전 기준을 `tk-artifacts`의 산출물 경로로 옮기고 T1/T2 변경 전 pointer로 적용합니다. 일치 검증·복원 메타데이터·지속성·정리 금지와 실패 중단은 유지합니다.
- `omit`: 실제 hook 자동 재실행, 외부 쓰기·운영 데이터·설정 변경, 수치 기반 자동 제거, 추측한 host schema·가격, 전용 집계 runtime·registry·상시 suite는 도입하지 않습니다.

이 보강은 upstream 코드 이식이 아닌 사용자 교정의 행동 계약입니다. 합성 시나리오 비교는
지침의 분기·집계 의미를 검토할 뿐 원래 plugin의 성능·절감률이나 사고 원인을 입증하지 않습니다.

## 스킬 실행의 관찰 경계

`hellogxp/skill-runtime-intelligence@0ac671f0ba8e08babffb5684906671fdd32c71ca`의 `README.md`,
`docs/runtime-event-model.md`, `docs/architecture.md`, `src/skill_runtime_intelligence/diagnosis_engine.py`,
`src/skill_runtime_intelligence/diagnostics.py`, `src/skill_runtime_intelligence/behavior_constraints.py`와
`tests/test_diagnosis_engine.py`, `tests/test_diagnostics.py`, `tests/test_behavior_constraints.py`를 읽었습니다.
Apache-2.0이며 코드·문장·fixture를 제품에 가져오지 않았습니다.
원본 tests·collector·hook·SQLite·UI 실행과 정량 효과는 `unverified`입니다.

- `keep`: 관련 범위만 조사하고 미관측과 실패를 구분하며 기존 hook/tool/usage 진단·RT 표·완료 상태를 유지합니다.
- `adapt`: 필요한 실행 단계의 관찰 근거를 연결하고 최초 관찰 실패와 최초 근거 공백, 주장·연결의 근거 등급을 구별합니다. 앞단 미확인이 뒤의 독립 관찰을 지우지 않게 합니다.
- `omit`: 새 SkillRun 모델·schema·registry·필수 단계별 표·원시 로그 수집기와 `Experimental` 기본 상태를 도입하지 않습니다. upstream engine에 독립 selection/verification stage가 있다고 주장하거나 resource 문자열 매칭을 실제 로드 성공으로 이식하지 않습니다.

## Waza 대조 출처

`tw93/Waza@6095341ad46b063619f4d0a5afc1c6fa8f1b4696`의 `skills/health/SKILL.md`와
`skills/think/SKILL.md`를 2026-11-11에 본문 대조했습니다. 기존 범위·읽기 전용 감사·조건부 설계
비교는 keep, 실제 MCP 상태/권한 수단 및 최소안/핵심 전제 검토는 adapt, collector·자동 실행·
새 프레임워크는 omit합니다. MIT 고지는 이 패키지의 `LICENSE.txt`에 보존합니다.
https://github.com/tw93/Waza/tree/6095341ad46b063619f4d0a5afc1c6fa8f1b4696
