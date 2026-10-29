# 설명 기법 선택과 외부 선호 저장 계약

기준은 `93314960a361cb6fd8a90602208d22ab3b937347`이다. 기존 설명 경로에는 기법별
이유·한계가 포함된 최대 5개 추천, 명시적 탐색의 최대 15개 시안, 네 원칙의 독립
선택지 및 외부 memory의 명시적 동의 계약이 없었다. 이번 Unit은 지시문과 eval만
변경하며 실행 코드나 새 backend를 추가하지 않는다.

`tk-explain`은 일반 요청에 하나만 생성한다. 설명 대상의 비교와 설명 기법의 비교를
구분하며, 명시적 기법 비교·탐색에만 여러 시안을 생성해 기존 평가 담당자에게 넘긴다.
새 package-local reference는 30개 공유 기법 정본을 수정하지 않고 추가 선택지를
소유한다. 네 출처의 정확한 revision, 읽은 구현·설계·평가 자료, `keep | adapt | omit`과
법적 고지는 `sources.md`와 `LICENSE.txt`에 기록했다. 원본 코드·표현 블록·에셋·폰트는
가져오지 않았다. 원본 실행이나 효능은 검증하지 않았다.

## 검증 근거

- 제품 변경 전 `sync_execution_protocol.py --check`, `validate_skills.py`,
  `check_docs.py`, `check_token_budget.py --check`가 모두 exit 0이었다.
- 변경 후 같은 네 검사가 모두 exit 0이었다. `validate_skills.py`는 30개 스킬과
  repository-owned trigger/behavior 계약을 오류 없이 검증했다. 기존 줄 수 경고는 남는다.
- `PYTHONPATH=scripts TMPDIR="$PWD/.tigerkit/tmp/issue-485-tests" python3 -B -m unittest scripts.test_validate_skills scripts.test_sync_execution_protocol scripts.test_check_docs scripts.test_explain_tools`
  결과는 68 tests, `OK (skipped=2)`였다. 두 Chrome 실행 검사는
  `TK_CHROMIUM_EXECUTABLE`이 지정되지 않아 생략됐다. 최초 실행은 `PYTHONPATH`가 없어
  세 모듈을 import하지 못했으며, 올바른 호출 경로로 다시 실행했다.
- 새 eval 13개가 일반 요청, 기법 비교, 15개 탐색, 적합 후보 부족, 현재 형식 우선,
  네 원칙, 시안별 근거 검사, 이미지 생성 불가, 저장 거절, provider 부재, 확인된
  이유와 맥락, 명시적 저장, 수정·삭제 한계와 저장 선호의 순서 영향을 다룬다.
  기존 eval을 삭제하거나 약화하지 않았다.
- 문구·지시문 변경이므로 인위적인 runtime RED를 만들지 않았다. 정적 검사와
  시나리오 계약 검토를 수행했으며 model eval이나 유료 생성은 실행하지 않았다.
  따라서 실제 모델 준수율이나 학습 효과가 입증되었다고 주장하지 않는다.

## 보존과 남은 검증

기존 Archify 설명 페이지·작성자 점검, PR/issue 기본 요약 PNG, 독립 정확성 리뷰,
접근성·오프라인·출처 조건을 유지한다. 새 표현 원칙은 그림과 구성의 선택지이며
별도 문서 renderer가 아니다. `tk-blind-comparison` package와 기존 30개 공유 참조는
변경하지 않았다. 갤러리 baseline은 controller가 확보했으며, 비교 런타임과 최종
browser after·전체 릴리즈 검사는 후속 Unit 및 controller가 수행한다.

`README: no public change`: 공개 호출 방식·스킬 목록·카탈로그 설명은 바뀌지 않았다.
추천·동의 절차는 소유 `SKILL.md`와 package-local reference에서 갱신했으며 README에
상세 동작을 중복하지 않는다.
