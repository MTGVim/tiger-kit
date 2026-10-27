# 릴리즈 체크리스트

`main`에 변경을 반영하기 전에 이 문서의 필수 검사를 통과합니다. 모든 검사는 로컬에서 실행합니다. 아래 명령은
릴리즈 검사기가 실행하는 내용을 보여 줍니다. 기준 버전 비교를 실행하면 이 명령들을
별도로 반복할 필요가 없습니다.

## README 기준

저장소 `README.md`에는 짧은 프로젝트 소개, 설치 방법, 간결한 스킬 카탈로그, 참고 링크만 둡니다.
스킬의 동작·권한·예외·사용 절차는 각 `SKILL.md`와 패키지 참조가 소유합니다. README에 상세 설명을 복제하지 않습니다.

- 스킬을 추가·삭제·이름 변경하거나 호출 방식·카탈로그 설명이 바뀌면 목록과 링크를 갱신합니다.
- 스킬 내부 동작이나 설명 자료만 바뀌면 README를 갱신하지 않습니다.
- 카탈로그 설명은 한 줄로 유지하고, 문서 검사에서 100자를 넘는 항목은 실패합니다.
- `scripts/check_docs.py`는 README 섹션, 간결한 소개, 스킬 호출 방식·링크·카탈로그 일치 여부를 검사합니다.

## 필수 검사

```bash
python3 scripts/sync_execution_protocol.py --check
python3 scripts/check_token_budget.py --check
python3 scripts/validate_skills.py
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
python3 scripts/check_docs.py
node --test skills/tk-pr-sweep/scripts/triage.test.mjs
git diff --check
```

`scripts/check_token_budget.py`는 스킬 본문의 글자 수(20,000자 미만), 문서 바이트 수, 설명 글자 수, 상시 참조 파일의 크기,
동기화 블록의 크기와 비율, 새로 중복된 문장을 측정합니다. 글자 수 제한은 유니코드 코드 포인트와 UTF-16 코드 단위를 모두 보수적으로 검사해
압축 후 재주입 시 잘림을 예방하는 별도 기준이며, 기존 36KB 제한은 바이트 부하를 검사합니다.
실제 호스트의 압축 동작을 실행했다는 증거는 아닙니다. 나머지 값은 컨텍스트 크기의 근사
지표이며 모델 토큰 수, 이미지 비용, 평가별 실행 비용을 직접 측정하지 않습니다.

실제 설치 검사는 기준 버전 비교에서 격리된 소비자 디렉터리에 패키지를 설치하고
설치 파일을 원본과 비교합니다. 전체 스킬 검사가 링크도 확인하고, `Node` 테스트가
대상 모듈을 불러오므로 링크 전용 검사와 구문 검사도 반복하지 않습니다.

## 기준 버전 비교

후보는 최신 `origin/main` 기준으로 비교합니다.

```bash
python3 scripts/run_seed_release_checklist.py \
  --baseline "$(git rev-parse origin/main)" \
  --candidate HEAD
```

## `main` 반영 전

- [ ] `origin/main`을 다시 확인하고 기준 버전이 최신인지 확인합니다.
- [ ] 후보 변경을 커밋하고 작업 트리가 깨끗한지 확인합니다.
- [ ] 위의 필수 검사를 모두 통과합니다.
- [ ] 문서 표·링크·스킬 목록·호출 방식·공유 정책을 검사하고, 공개 동작 설명은 독립 검수와 대조합니다.
- [ ] 새로 추가한 상시 참조 문장은 하나씩 삭제 전후로 동작을 비교합니다. 삭제해도 변화가 없는 문장은 추가하지 않습니다.
- [ ] 기준 버전 비교 결과가 `Pass`이며 `blocking_reasons`, `contract_errors`, `Unverifiable` 상태가 없습니다.
- [ ] 검증 뒤 `origin/main`이 이동하면 새 기준으로 검사를 다시 실행합니다.
- [ ] 모든 항목을 만족한 뒤에만 `main`을 갱신합니다.
