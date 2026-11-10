# Waza 대조와 적용 판단

2026-11-11에 `tw93/Waza@6095341ad46b063619f4d0a5afc1c6fa8f1b4696`의
`skills/hunt/SKILL.md`, `skills/check/SKILL.md`, `skills/health/SKILL.md`,
`skills/think/SKILL.md`, 루트 MIT 라이선스를 확인했습니다.
https://github.com/tw93/Waza/tree/6095341ad46b063619f4d0a5afc1c6fa8f1b4696

| 대조 | 판단과 차이 |
| --- | --- |
| hunt / diagnosis | adapt: 기존 red-capable 재현·TDD·권한 경계를 유지하고 원인 문장·실패 가설 상한·동일 증상 중단·같은 유형 조사·웹 함정을 보완합니다. tk-debug는 보고 전용 진입만 소유합니다. |
| check / review-protocol·finding-quality | adapt: 기존 Spec/AC·Quality/Standards와 독립 검토를 유지하고 범위 이탈·불필요한 추상화·세 라운드 뒤 접근 재검토를 추가합니다. |
| health / grooming | keep: 기존 범위 한정·런타임 기록·비밀·읽기 전용 경계를 유지합니다. adapt: MCP/훅 실제 연결과 설정 존재 구별, 공급망·권한 수단 점검을 보완합니다. archive 결정 대조는 사용자 피드백에서 추가합니다. |
| think / prep | keep: 기존 조건부 설계 비교·관찰 가능한 검증·복구·승인 연속성을 유지합니다. adapt: 새 설정/추상화의 최소안 대조와 핵심 전제 붕괴를 보완합니다. |

omit: Waza의 자동 리뷰/발행 통합, collector·runtime framework·memory 지속화,
IME·네이티브·PDF 전용 진단, 강제 표식·회귀 테스트 suite 복제는 도입하지 않습니다.
`tk-review`는 기존 명시 호출 전용 계약을 유지합니다. 일반 리뷰 요청에 특정 호스트의 `/code-review`
존재를 가정하거나 자동으로 호출하지 않습니다. 원본의 성능·호스트 라우팅 효과는 실행 검증하지 않았습니다.
각 독립 배포 패키지의 `LICENSE.txt`에 MIT 고지를 보존합니다.
