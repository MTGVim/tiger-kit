<a id="upstream-distillation"></a>
# Upstream 증류

2026-11-04에 `mattpocock/skills`의 최신 `main`을
[`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d)로
고정하고 `skills/engineering/wizard/SKILL.md`, `template.sh`, `docs/engineering/wizard.md`를 확인했습니다.
관계는 `adapted`이며 원본 MIT 고지는 [LICENSE.txt](../LICENSE.txt)에 보존합니다.

- **keep:** 근거 있는 단계, 값의 출처·목적지, 현재 행동과 진행 표시, 일반/비밀 입력 구분과 재실행입니다.
  짧은 절차에는 기존 대화를 유지합니다.
- **adapt:** 복잡한 사람 수행 절차에 검증한 일회성 Bash Wizard를 조건부로 제공합니다.
  [입력 틀](../assets/wizard.sh)은 원본 코드로 작성했으며 입력·진행 표시만 소유합니다.
  저장·대상별 원격 쓰기는 실제 파서·권한과 생성본의 실행 검증을 통과한 경우에만 추가합니다.
- **omit:** upstream 템플릿의 symlink 추종 쓰기, 셸 인용을 가정한 범용 dotenv 처리, cwd에서 추론하는
  GitHub 대상, 부분 실패 뒤 무조건 성공 요약, 값의 일괄 보존과 생성본의 구문 검사만으로 전달하는 방식은
  도입하지 않습니다. 운영·비가역 변경의 대상별 승인과 기존 보호 입력·정리 계약이 우선합니다.

실행·검증 조건은 [실행형 Wizard](executable-wizard.md)가 소유합니다. 설치된 Bash 3.2/macOS나
실제 제공자 쓰기를 확인하지 않았다면 해당 런타임의 성공을 주장하지 않습니다.

2026-11-06에 최신 `main`이 같은 revision임을 다시 확인하고 위 구현·설계 문서를 대조했습니다.
`keep`: 기존 값이 없는 일반/비밀 필드는 바로 값 입력으로 들어가는 upstream 동작입니다.
`adapt`: TigerKit의 `keep | skip | replace` 계약은 유지하되 실제 대안이 있을 때만 행동을 묻고,
입력 전 첫 PTY 화면·숨김 상태를 검사합니다. `omit`: 정적 추적만으로 생성본을 검증하는 방식입니다.
upstream 실행 검증은 수행하지 않았습니다.
