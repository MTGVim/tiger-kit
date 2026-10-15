# 릴리즈 체크리스트

`main`에 변경을 반영하기 전에 이 문서의 필수 검사를 통과합니다. 모든 검사는 로컬에서 실행합니다.

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
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
python3 scripts/check_docs.py
node --check skills/tk-pr-sweep/scripts/triage.mjs
node --test skills/tk-pr-sweep/scripts/triage.test.mjs
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

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
- [ ] 기준 버전 비교 결과가 `Pass`이며 `blocking_reasons`, `contract_errors`, `Unverifiable` 상태가 없습니다.
- [ ] 검증 뒤 `origin/main`이 이동하면 새 기준으로 검사를 다시 실행합니다.
- [ ] 모든 항목을 만족한 뒤에만 `main`을 갱신합니다.
