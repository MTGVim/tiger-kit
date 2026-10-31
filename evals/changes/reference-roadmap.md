# 참조 구조 로드맵의 측정·인계·`renderer` 경계를 정리합니다

기준은 인증 수명주기 수정 `70da70d11d68036c2f38f9b09dd97eecdb7ba629`입니다. 사용자 승인 범위는 남은 구조 개선과 후속 테스트 정리의 로컬 구현·검증·독립 검토·커밋입니다. 원격 발행과 기존 사용자 산출물 변경은 포함하지 않습니다.

## 2. 예산 목록과 누락 검사

`tk-explain`의 페이지 선택·작성자 점검에서 명시적으로 읽는 `explanation-selection.md`, `clear-writing.md`, `reader-formatting.md`, `visual-grammar.md`가 정적 목록에서 빠져 있었습니다. 선언된 39,889바이트에 이를 포함하면 94,737바이트입니다. 기존 실행 지침을 줄이거나 새 읽기를 추가한 결과가 아니라 계상 범위를 바로잡은 결과입니다. 해당 한도만 77,000에서 96,000바이트로 조정하고 정당화 근거를 갱신합니다.

상시 참조 프로필에 `entrypoint`를 명시하고, 저장소 내부 `skills/tk-*/SKILL.md`의 명시적 `Read` 링크와 페이지 `renderer` 지시가 빠지면 검사 명령이 실패하도록 합니다. 코드 펜스 예시는 제외합니다. 조건부·전이 참조와 설치된 외부 스킬의 읽기는 자동 추론하지 않으며 의미 검토 대상으로 남깁니다. 정적 바이트는 모델 토큰이나 실행 전체의 실제 읽기량이 아닙니다.

실제 검사 명령이 누락된 프로필을 성공 처리하는 실패를 먼저 재현했습니다. 회귀 검사는 누락·정상 합산·새 직접 지시·조건부/코드 예시 제외·진입점 삭제/변경·경로 이탈·기존 바이트 한도를 보호합니다. 잘못된 프로필 자료형도 예외로 종료하지 않고 검증 오류를 반환합니다. 필수 경로의 두 번째 수기 목록이나 범용 자연어 실행 엔진은 도입하지 않습니다.

## 3-5. 분기별 참조 통합

- `Audit`: `executor-handoff.md`에 자기완결 맥락·비교 커밋·기대 결과·중단 조건·비밀 금지·권한 비확장을 합칩니다. `plan-template.md`와 본문의 상세 재요약만 제거합니다. 모든 일회성 감사에 저장 양식을 강제하지 않습니다. 기존 `shadcn/improve@03369ee6d7cafbfcecc4346539b05b3dc0a603bb` 출처와 `NOTICE`는 보존합니다.
- `Prep`: `task-evidence.md`에서 공통 `ui-evidence.md`를 직접 읽습니다. 구조 설명 대안·준비 단계 충돌 해결·텍스트 탐색기의 공백 정규화 차이는 해당 조건에 짧게 남기고 `ui-text.md`를 제거합니다. 공통 정본과 12개 패키지 사본은 변경하지 않습니다.
- `Browser`: 실행 준비의 독립 `wrapper`를 제거하고 `environment.md`로 직접 연결합니다. 고유한 새 `verifier`의 구문/`DOM`/신뢰 입력/정리 `smoke` 조건은 `Provider readiness`에 보존하고, 새 `adapter`/`hand-authored` `verifier`도 이 참조를 읽도록 명시합니다. `provider` 선택·`headless`·`attach` 사전 증명·소유 프로세스 정리·서버 식별·자동 설치 및 `fallback` 금지는 유지합니다. 고유한 인증 우선순위가 있는 `headless-auth.md`는 보존합니다.

`Audit`의 원 대화 없는 인계와 `Prep`의 `locator`/미검증 경로 경계를 보호하는 행동 평가를 각각 추가합니다. 기존 평가와 `migration`은 변경하지 않습니다. 평가 정의·정적 보존 검사와 실제 모델 `actor`/`grader`의 실행 성공을 구분합니다.

삭제한 `Prep` `wrapper`의 기존 증류 출처도 보존합니다. `microsoft/playwright@18205280b6112a4a08238195942c4fa30c199a62`의 `docs/src/locators.md`, `packages/playwright-core/src/client/locator.ts`, `tests/page/selectors-text.spec.ts`입니다. `keep`: 현재 `DOM`과 요소 범위 근거. `adapt`: 정확 탐색도 공백을 정규화하므로 원문 인용은 별도 입증. `omit`: 프레임워크 설치·런타임 권한 확장. 이 `revision`을 현재 `upstream` `HEAD`라고 주장하지 않습니다.

## 6-7. `Renderer` 조사와 선택한 최소 수정

현재 `research`는 `archify`를 사용하고 `explain`은 선택한 `archify` 또는 독립 `technique` `HTML`을 사용합니다. 반면 `QA`·`prototype`·`blind` `gallery`의 전용 생성기와 공용 테마, 기존 `report` 회귀 `fixture`는 여전히 `legacy` `shared` 파일을 사용합니다. `run_release_checklist.py`의 소비자 설치도 패키지의 모든 파일을 복사·대조하므로 배포 단계가 보존 파일을 자동 제거하지 않습니다.

`keep`: `ADR` 0003의 패키지별 일반 파일 사본, 기존 전문 `UI` 생성기·테마·회귀 테스트, 기존 사용자 `HTML`, 설치·`offline`·접근성·`source`·`export` 계약.
`adapt`: `html-assembly.md`와 `html-reader.md`의 무조건적인 새 문서 `builder`/`shell` 강제를, 소유 `workflow`가 선택한 `shared-reader` 부분으로 한정하고 기존 동기화 도구로 사본을 생성합니다.
`omit`: `legacy` `report` 실행 경로 부활, 근거 없는 자산/테스트 일괄 삭제, 새 `renderer`/`framework` 도입, 자동 설치·의존 버전 갱신.

조사 `revision` `tt-a1i/archify@f325d86230553e1dd15d3464324f1fcd01f02352`에서 `authoring`·`renderer`·기본 `finalize` `CLI` 테스트를 대조했습니다. `raw` `HTML` 거부, `raster` `data` `URL`, `finalize`와 `browser` 실행의 분리 계약을 확인했습니다. `upstream` 코드·`runtime`은 복사하지 않고 현재 `TigerKit` 설치 최소 버전/`pin`은 바꾸지 않습니다. `upstream` 테스트를 읽은 것과 실제 실행한 것은 구분합니다.

## 후속 테스트 정리

`test_blind_comparison.py`에서 현재 동작을 보호하는 기존 17개 테스트는 유지합니다. 테스트 `PNG` 생성에만 필요했던 `Pillow` `import` 네 곳을 표준 라이브러리 `fixture`로 교체하고, `PNG` `CRC`·실제 캔버스 픽셀·메타데이터·출력 개수 검증을 보존/보강합니다. `Pillow` 제거를 저장소의 모든 선택적 이미지 기능 제거로 확대하지 않습니다.

통합 검사에서 기존 예산 증가 테스트 두 개가 보정된 전체 프로필 한도를 먼저 초과했습니다. 제품 한도는 유지하고, 해당 테스트가 원래 의도한 대로 상시 참조 프로필 밖의 `tk-audit` 본문에서 증가 근거의 유무를 검증하도록 입력만 고칩니다. 실제 저장소의 정적 한도 검사는 그대로 둡니다.

`test_probe_codex_isolation.py`는 0.2초 실행 제한 전에 `fixture`의 자식 시작이 끝나지 않는 기존 실패를 고칩니다. `SIGTERM` 무시 설정 후 자식이 `PID`를 게시하고, 테스트 소유의 유한 준비 대기 후 원래 `Popen.communicate`와 0.2초 제한을 사용합니다. 실제 `probe` 구현·`timeout`/완료/`interrupt` 판정·소유 `descendant` 종료 확인은 유지합니다. 의도적인 0.3초 시작 지연으로 준비/실행 시간을 구분합니다.

## 최종 검토에서 발견한 예외와 조치

독립 검토에서 명시적 `Read`의 두 번째 링크가 다음 줄에 있으면 누락을 놓치는 문제와, 유효한 들여쓰기·더 긴 닫는 코드 펜스를 예시로 제외하지 못하는 문제를 재현했습니다. 실제 `CLI` 회귀를 실패시킨 뒤 문단 단위의 연속 링크와 `Markdown` 펜스 상태 처리를 보완했습니다. 조건부·전이 읽기를 추론하는 범위로 확장하지 않습니다.

선택적 `HTML` `navigation` 검사에서는 설치된 `Playwright`/`Chrome`의 실행 환경 지정과 임시 폴더 준비가 필요했습니다. 준비 이후에도 `no-JS` 환경에서 의도적으로 숨긴 테마 컨트롤에 배치 단언을 적용해 실패했습니다. 인증 완료 기준 버전과 후보의 입력 파일이 동일함을 확인하고, 격리 복제본에서도 같은 실패를 재현했습니다. 제품 자산은 변경하지 않고, 검사에서 보이는 컨트롤에만 배치 단언을 적용하며 기존 `no-JS` 숨김·탐색·클리핑 검증을 유지합니다. 중첩 `fixture`의 부모 폴더는 검사가 직접 준비합니다. 과거 `TOC` 변경 전용 비교는 당시 `baseline`을 지정하지 않아 실행하지 않았으며 현재 변경의 전체 시각 비교로 보고하지 않습니다.

## `Upstream-first`와 검증 한계

`Anthropic` `skills@ca45fc496a3436251f191354091d557da31c15b5`, `skills/skill-creator/SKILL.md:86-109`의 단계별 로딩·정확한 조건 포인터를 현재 구현과 비교했습니다. `keep`: 조건부 참조와 안전 경계. `adapt`: 중복 `wrapper` 제거와 실제 로컬 읽기 계상. `omit`: 임의 줄 수를 정합성 관문으로 삼기, 제공자/`runtime` 복제. 이번 변경의 의미·경로·실제 명령 검증은 로컬 검사와 독립 리뷰를 사용하며, `upstream` `eval` 실행이나 실제 로그인/삭제·브라우저 화면 검증으로 포장하지 않습니다.

`README: no public change`: 변경 대상 `skills/tk-audit/SKILL.md`, `skills/tk-browser-verify/SKILL.md`의 이름·설명·호출 방식·카탈로그는 유지합니다. 나머지는 참조·저장소 검증·테스트 입력 정리입니다. 기존 공개 검사 설명의 소유자인 `RELEASE_CHECKLIST.md`만 함께 갱신합니다.
