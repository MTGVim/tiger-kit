# 이슈 #398: `tk-autoresearch`

기준: `59d97faa4630b338d5f1cfd777bd39bbc0528b45`.

## 변경

- `tk-discover`의 현재 탐색 가능 항목·불명확 영역·의존성·출처 이력 계약을 `tk-autoresearch`로 이관하고 `renamed_from` 평가 계약으로 기존 필수 동작을 보존합니다.
- 승인된 연구 전용 작업 공간에 한해 사전 실험·벤치마크·시제품·본 실험의 로컬 변경을 허용하되 제품 작업 트리, 운영 데이터, `push`·PR·`merge`·`release` 권한은 확장하지 않습니다.
- 개별 연구 결과, 연구 방향, 연구 프로그램 세 수준의 수렴과 `NO-ACTION`·`NO-DELTA`를 추가합니다.
- 지속 상태는 `.tigerkit/autoresearch/state.md` 하나가 정본이며 필요한 실험 근거만 `experiments/<EXP-ID>/`에 둡니다. 예약 실행기, DB, 실행 위치 포인터, 실행별 대화 기록은 만들지 않습니다.
- `tk-research`는 1차 출처 추적과 출처 접근 가능성·주장 충실도 분리를 강화합니다.

## 상위 원본

- `Orchestra-Research/AI-Research-SKILLs` `773a52944ba4747a18bd4ae9ade53fff041adcbc`
- `uditgoenka/autoresearch` `050e30dc4ba0974b03f2873111b9901ec3211390`
- `Companion-Inc/feynman` `4d62d07a7e8eb1fba1b02d6547e6425e456715eb`
- `bryanshake/autoresearch` `0fa9a9336fc84a6b069111adb03ca21fabb5394b`
- `rohankgeorge/the-researcher` `1184d246c290a4ff772ea669ac6b9f9914d3f7da`

각 `keep`·`adapt`·`omit` 판단과 검증 한계는 스킬 내부 `references/sources.md`에 기록했습니다.

## 평가

- 기존 `tk-discover`의 동작·호출 평가 계약은 이름 변경으로 보존합니다.
- 카탈로그의 탐색 분기 계약은 명시적인 이관 기록을 통해 자동 연구 사례로 이동합니다.
- 소규모 사전 실험 우선, `NO-DELTA` 종료, 연구 변경 권한 경계, 전체 연구 수렴과 `tk-research` 출처 검증을 릴리스 필수 평가 대상으로 추가합니다.
