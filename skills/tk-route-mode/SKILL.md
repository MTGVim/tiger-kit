---
name: tk-route-mode
description: "[user] 위임 능력 티어별 모델과 effort의 기본 및 절약 모드를 확인·전환하거나 사용자 모드를 추가·갱신하고, 현재 호스트의 사용자 수준 에이전트 설정을 승인받아 적용·검증·복원할 때 사용합니다. 개별 작업의 티어 선택이나 메인 세션 모델 변경에는 사용하지 않습니다."
disable-model-invocation: true
argument-hint: "[standard | economy | update]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---
<!-- tigerkit:universal-authoring-gate -->
## 공통 저작 품질 관문

이 스킬에서 질문·메시지·설명·보고서·Markdown·HTML·대본·자막·문서·스킬 본문 등 사람이 읽는 텍스트를 **새로 작성하거나 의미·표현을 수정하기 전에**, 설치된 `tk-writing`의 [모든 저작의 공통 관문](../tk-writing/references/authoring-gate.md)과 [명확한 글쓰기](../tk-writing/references/clear-writing.md)를 이번 작업에서 읽고 적용합니다. 최종 산출물을 인계하기 전에 같은 기준으로 원고를 검사하고 문제를 수정합니다. 이미 읽은 기준을 반복 로드하거나 별도 재작성 스킬·에이전트·승인 라운드를 추가하지 않습니다. 코드·명령·식별자·기계 판독 형식·인용과 고정 문구는 보호하며, 이 참조로 변경·전송·발행 권한이 생기지 않습니다. 이 스킬이 작성 작업을 수행하지 않는 경우에는 추가 읽기가 필요하지 않습니다.
<!-- /tigerkit:universal-authoring-gate -->

# 위임 모드 설정

명시적인 사용자 호출로만 시작합니다. 일반 SWE 실행이나 위임 도중 자동 호출하지 않습니다. 실제 작업의 티어 선택, 권한과 독립 평가의 정본은 [위임과 독립 평가](../tk-engineering/references/delegation.md)입니다. 이 스킬은 위임 대상의 사용자 수준 설정만 관리합니다. 중앙 라우터, 런타임 훅, 모델 자동 변경이나 새 실행 프레임워크를 추가하지 않습니다.

사용자 결정과 승인을 요청하기 전에 [질문 기준](../tk-questioning/references/questions.md)을 확인합니다. 설정 파일을 조사하기 전 [비밀 보호 조회](../tk-artifacts/references/artifact-paths.md#secret-safe-inspection), 원본 복구 사본을 만들기 전 [지속 백업 기준](../tk-artifacts/references/artifact-paths.md#persistent-recovery-backups)을 확인합니다. 필요한 설치 소유자가 없으면 해당 단계만 중단하고 tk-setup-skills를 안내합니다.

## 개념과 기본 모드

- 티어: light(좁은 사실 수집, 탐색과 분류, 기계적 검사), standard(구현과 독립 리뷰), top(아키텍처, 미지 문제 탐사와 연구). 모델명과 티어는 별개입니다. 메인 컨트롤러에는 top의 권장값만 안내하며 세션 모델을 바꾸지 않습니다.
- 공급자: 모드 대응표는 anthropic, openai 등 공급자별로 둡니다. Claude Code와 Codex는 호스트에 실제 설정된 공급자를 확인합니다. Hermes 등 복수 공급자 호스트도 현재 공급자를 확인합니다. 없는 공급자는 세 티어를 모두 사용자와 결정하고 add의 --set으로 추가합니다. 모델 별칭을 실제 호스트 모델 ID로 확인하기 전에는 적용하지 않습니다.
- 모드: standard와 economy를 기본으로 제공하고 extends로 사용자 모드를 추가합니다. economy는 구현과 리뷰의 standard 비용만 낮추고 light와 top을 유지합니다. 기본값은 [모드 대응표](references/default-modes.json)에 있으며 사용자 파일이 없을 때 읽기 전용으로 사용합니다.
- 대응표 위치: ROUTE_MODE_CONFIG, 없으면 XDG_CONFIG_HOME/route-mode/modes.json, XDG_CONFIG_HOME도 없으면 ~/.config/route-mode/modes.json. 사용자 벤치마크와 적용 기록, 복구 사본은 대응표와 같은 디렉터리에서 관리합니다. 설치 패키지나 저장소 안에 사용자 설정을 쓰지 않습니다.

## 도구

현재 설치 패키지에서 Python 3 표준 라이브러리 도우미를 실행합니다.

```bash
python3 scripts/route_mode.py path
python3 scripts/route_mode.py --help
python3 scripts/route_mode.py status
python3 scripts/route_mode.py list
python3 scripts/route_mode.py validate
python3 scripts/route_mode.py plan --provider anthropic --mode economy
python3 scripts/route_mode.py use economy
python3 scripts/route_mode.py add review-heavy --extends economy --set anthropic.standard=sonnet:high
python3 scripts/route_mode.py update economy --set anthropic.standard=sonnet:high
python3 scripts/route_mode.py derive
python3 scripts/route_mode.py derive --save
```

인자 없는 도우미 호출과 status, path, list, validate, plan, derive(저장 옵션 없음)는 읽기 전용입니다. use, add, update, derive --save와 rule on/off는 쓰기 명령이므로 정확한 목적지와 변경 계획에 대한 사용자 승인 후에만 실행합니다. 도우미는 호스트 설정을 자동 변경하지 않습니다. 검사가 실패하면 대응표를 저장하지 않습니다.

## 사용자 호출

| 호출 | 동작 |
| --- | --- |
| `tk-route-mode` | 현재 모드, 호스트별 목표, 프로필 파일과 로드 여부, 위임 선택 규칙, 티어별 실제 모델·effort의 확인 상태를 읽기 전용으로 보고합니다. |
| `tk-route-mode standard` | 기본 모드의 대응표·프로필·규칙을 함께 점검하고 승인된 변경을 적용한 뒤 실제 위임을 확인합니다. |
| `tk-route-mode economy` | 절약 모드를 같은 절차로 적용하고 검증합니다. |
| `tk-route-mode update` | 최신 원본 벤치마크를 조사하고 두 기본 모드의 후보를 비교합니다. 승인 후 대응표를 갱신하고 활성 모드를 적용·검증합니다. |

인자가 없으면 help가 아니라 상태 조회입니다. 호스트를 식별할 수 없으면 현재 대응표와 확인하지 못한 항목을 보여 주고 파일을 생성하지 않습니다. 상태 조회에서는 실제 위임을 새로 실행하지 않습니다. 기록된 증거가 현재 모드·대상·파일 지문과 일치하지 않거나 세션의 로드 상태를 알 수 없으면 unverified로 표시합니다.

모드 전환은 목표 대응표와 프로필, 기존 위임 규칙의 검사부터 시작합니다. 변경할 대응표·프로필·규칙과 복구·실행 검증을 한 계획으로 제시하고 한 번 승인받습니다. 같은 모드를 선택해도 실제 설정과 규칙을 확인하고 필요한 부분만 변경합니다. 검증 실패 또는 부분 적용은 성공으로 보고하지 않습니다.

이 네 가지가 사용자에게 안내하는 기본 인터페이스입니다. 기존 `status`, `use <mode>`, `apply`, `verify`, `derive`, `rule on/off/status`, `help` 및 `--`가 붙은 기존 옵션 표기는 호환 요청으로 처리합니다. 기존 사용자 모드 전환은 이름이나 `use <mode>`로 명시할 수 있습니다. 사용자 모드 추가, 특정 칸의 수동 override·해제, 복원은 명시적으로 요청하면 기존 승인·백업 절차와 내부 CLI를 사용합니다. `update <mode> --set/--unset/--description`은 이전 수동 편집의 호환 형식이며 인자 없는 update는 벤치마크 갱신입니다. 일반 모드 전환에서 별도 apply, rule on, verify 호출을 요구하지 않습니다.

## 벤치마크 갱신

1. 공급자마다 티어별 모델과 effort에 대응하는 작업당 비용(USD), 종합 점수를 같은 측정의 원본에서 수집합니다. 기본 조사처는 Artificial Analysis Intelligence Index입니다. 코딩 작업에는 Terminal-Bench 등 코드 벤치마크의 근거도 비교합니다.
2. 대응표와 같은 디렉터리의 benchmarks.json에 [번들 형식](references/benchmarks.json)을 사용해 출처 URL, 조회 날짜, 공급자별 모델 별칭과 값을 저장할 계획을 만듭니다. 원본에서 확인하지 못한 값은 추정하여 채우지 않습니다. 사용자 벤치마크를 덮어쓰기 전에 임시 후보 파일을 만들어 읽기 전용 도출을 수행합니다. 기존 벤치마크의 복구 사본을 포함합니다.
3. 도우미의 `--bench <후보 파일> derive`로 두 모드의 후보를 도출합니다. 조회 날짜와 원본 출처, 같은 측정의 비용·성능, 누락된 수치를 구분합니다. [선정 원칙](references/selection.md)의 규칙에 따라 현재 값과 차이, 비용 및 점수, 코딩 벤치마크와의 불일치를 보고합니다. 번들 데이터는 사용자 제공 세션의 재구성값이며 원본 수치 대조는 unverified입니다.
4. 후보 비교와 활성 모드의 프로필·규칙 변경 계획을 함께 승인받습니다. 승인 후 사용자 벤치마크를 백업·저장하고 `derive --save`로 대응표를 갱신합니다. 사용자 추가 모드와 기존 수동 override는 보존합니다. 활성 모드의 목표가 같아도 프로필·규칙을 검사하고 실제 위임을 검증합니다. 실패하면 부분 변경과 복원 가능성을 기록합니다.

## 호스트 적용

1. validate를 실행합니다. 실패하면 중단합니다. 현재 호스트, 공급자, 모델 별칭, 설정 위치와 실제 위임 API를 조사합니다. [호스트별 출발점](references/hosts.md)은 조사 참고용이며 현재 문서와 도구 스키마가 우선합니다.
2. 티어별 목표와 현재 모델 및 effort, 변경할 정확한 경로와 키, 비밀을 제외한 diff, 현재 세션 반영 여부, 복구 방법을 확인합니다. 사용자 수준 및 현재 작업의 유효한 위임 규칙이 티어 이름 선택을 실제로 요구하는지도 검사합니다. 동등한 규칙이 있으면 중복하지 않고 없거나 충돌하면 필요한 추가 또는 조정을 같은 변경 계획에 포함합니다. 대응표·프로필·규칙·실행 검증을 포함한 계획을 승인받습니다. 지원되지 않거나 확인하지 못한 축은 unverified로 표시합니다.
3. 승인된 범위만 씁니다. 필요한 위임 규칙은 프로필과 같은 적용 절차에서 기록·백업 후 반영합니다. 기존 규칙의 충돌을 임의로 덮어쓰지 않습니다. 기존 사용자 소유 에이전트나 설정을 덮어쓰지 않습니다. 충돌은 별도 승인을 받습니다. 공유 설정 파일에는 이 스킬 소유 부분을 구분하고 다른 내용을 유지합니다. 경로, 소유권, 심볼릭 링크 여부를 확인합니다. 변경 전에 대응표 디렉터리의 backups/<시각>/에 제한된 권한으로 지속 백업하고 복원 가능성을 확인합니다. 환경변수나 인증 설정의 원문과 값은 도구 출력에 노출하지 않습니다.
4. 대응표 디렉터리의 applied/<호스트>.json에 정확한 변경 파일과 키, 변경 전후 지문, 새 파일 여부, 백업 경로와 검증 상태만 남깁니다. 비밀 값이나 설정 전문은 기록하지 않습니다. 실패 또는 미완료 상태를 성공으로 바꾸지 않습니다.
5. 아래 실제 확인 기준을 실행하고 티어별 verified, mismatch, unverified를 보고합니다. 반영 시점과 복구 경로를 함께 전달합니다.
6. 파일 생성, 호스트 로드, 규칙 선택 및 실제 위임을 별도 상태로 기록합니다. 대응표와 파일 검사가 통과했더라도 실제 선택 또는 실효 모델·effort 근거가 없으면 unverified입니다. 현재 세션에서 검증을 완료하지 못하면 필요한 reload 또는 새 세션과 재검증 방법을 안내합니다.

## 위임 규칙 관리 도우미

호스트가 읽는 사용자 수준 지침 파일의 정확한 위치를 문서로 확인합니다. 저장소 지침 파일은 대상으로 삼지 않습니다. 프로필과 규칙의 저장 대상은 서로 다르지만 모드 전환에서는 함께 점검하고 적용합니다. rule off는 호환 복원 절차이며 티어 대상을 삭제하지 않습니다.

```bash
python3 scripts/route_mode.py rule status --file <지침 파일>
python3 scripts/route_mode.py rule on --file <지침 파일> --host <호스트>
python3 scripts/route_mode.py rule on --file <지침 파일> --host hermes --prefix ""
python3 scripts/route_mode.py rule off --file <지침 파일> --host <호스트>
```

on은 route-mode:begin/end 사이의 관리 블록을 추가하거나 교체하고 off는 블록만 제거합니다. 변경 전 백업과 applied 기록을 남깁니다. 같은 요청은 중복 블록을 만들지 않으며 잘못된 마커나 중복 마커, 안전하지 않은 경로, 기록 형식 오류는 차단합니다. on/off 전 정확한 변경을 승인받습니다.

## 실제 확인 기준

- 검증 요청에 포함된 각 티어를 해당 이름으로 선택하여 짧은 읽기 전용 작업을 실제 위임하고 호스트가 기록한 모델과 effort를 목표와 대조합니다. 도구 메타데이터나 세션 기록 등 호스트 근거를 사용합니다. 자식의 자기 보고만으로 verified라고 판정하지 않습니다.
- 호출 인자, 상위 환경변수, 플러그인 비활성 등 정의를 덮어쓰는 설정을 확인합니다. 환경변수 키 이름과 값의 유무만 반환하고 원시 값은 출력하지 않습니다.
- 파일 작성 직후 현재 세션이 설정을 다시 읽지 않았다면 이전 값과 달라도 unverified로 두고 새 세션 또는 확인된 호스트 reload 절차를 안내합니다. 다시 읽은 이후 실효값이 목표와 다르면 mismatch로 보고합니다.
- 대응표 유효성, 프로필 파일과 지문, 현재 호스트의 프로필 로드, 위임 규칙(동등한 규칙 포함), 실제 선택된 티어 이름, 실효 모델과 effort를 분리해 확인합니다. 세 티어의 호스트 기록을 대조하며 reload나 새 세션 전후를 구분합니다. 필요한 권한 또는 effort 축을 입증할 수 없으면 해당 티어는 unverified입니다. 메인 세션 모델이 바뀌었다고 주장하지 않습니다.

## 복원

applied/<호스트>.json에 기록된 항목만 승인된 복구 사본으로 되돌립니다. 변경 전후 지문, 현재 소유권과 백업의 일치를 확인합니다. 적용 후 사용자가 변경했거나 기록/백업이 없거나 안전한 경로인지 확인할 수 없으면 추측하여 복원하거나 삭제하지 않습니다. 이 스킬이 새로 만든 파일의 삭제도 별도 복원 계획에 포함해 승인받습니다. 복원 후 실제 위임 상태를 확인합니다.

## 위임 계약과 제한

위임하는 쪽은 tier-light, tier-standard, tier-top 또는 선택지형 호스트의 light, standard, top을 선택합니다. 이름으로 선택할 때 모델 및 effort 호출 인자를 따로 넘기지 않습니다. [공통 위임 계약](../tk-engineering/references/delegation.md)을 우선합니다. 공급자별 대응표는 명시적인 설정 작업에서만 읽으며 개별 업무에서 자동으로 설치하거나 적용하지 않습니다. 인증정보를 읽거나 쓰지 않고 호스트의 기존 인증 방식을 사용합니다. 원격 설치 스크립트를 내려받아 실행하지 않습니다.
