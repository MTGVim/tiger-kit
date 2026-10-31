# main 반영 전 확인

이 저장소는 Agent Skills와 실제 설치 도우미를 배포합니다. 저장소 전용 테스트 suite, eval catalog,
문구 잠금 검사와 릴리즈 비교 framework는 유지하지 않습니다. 제거한 파일과 과거 검증 근거는 Git 이력에서
확인할 수 있습니다. 이 정책은 스킬이 사용자의 다른 프로젝트에서 요구하는 TDD·리뷰·검증을 면제하지 않습니다.

## 기본 명령

저장소 루트에서 승인된 Python 환경을 사용합니다. 메타데이터 검사는 `Python 3.9+`와 `PyYAML`이 필요하며
없으면 자동 설치하지 않고 중단합니다.

```bash
python3 skills/tk-setup-skills/scripts/skill_dependencies.py validate \
  --root . --catalog skills/tk-setup-skills/references/install-catalog.json
PYTHONPYCACHEPREFIX=.tigerkit/tmp/compile-cache python3 -m compileall -q skills
for f in skills/*/scripts/*.mjs; do node --check "$f" || exit; done
git diff --check
```

`dependencies.json`을 바꿨으면 동일한 실제 설치 도우미로 bundled catalog를 갱신한 후 위 검사를 실행합니다.

```bash
python3 skills/tk-setup-skills/scripts/skill_dependencies.py build-catalog \
  --root . --output skills/tk-setup-skills/references/install-catalog.json
```

## 변경에 맞는 실행 확인

- 지침 변경: 바뀐 본문 전체와 참조 진입 조건을 읽고, 이전 동작·필요한 분기·건너뛸 분기·승인/실패 경계를 비교합니다.
- 설치·공통 자원 변경: 격리된 대상에 실제 dependency closure를 복사 설치하고 source checkout 없이 명령·자원 읽기를 확인합니다. 소유자 누락·식별 불일치·안전하지 않은 경로는 해당 작업을 중단해야 합니다. 사용자 설치본은 검증 대상으로 덮어쓰지 않습니다.
- 공통 자원 경로: `tk-writing`의 HTML assets/scripts와 `tk-verification-guidance`의 registry/설정 helper를 정확한 설치 소유자에서 읽고, 문서 링크·CLI 예제·직접 의존성·bundled catalog를 함께 확인합니다. 구 소비자 사본이나 wrapper로 누락을 가리지 않습니다.
- 라이선스 중복 정리: 파일별 고유 완전 고지, 저작권·attribution과 다른 법적 본문을 전후 비교합니다. 독립 배포 패키지 사이의 필요한 고지는 제거하지 않습니다.
- 실행 도우미 변경: 실제 CLI의 정상 출력·상태 변화와 바뀐 실패 조건을 재현합니다. HTML 등 표현 자원 이동은 이전/이후 출력 바이트를 비교하고, 표현 동작이 달라지면 해당 browser/app verifier를 사용합니다.
- 근거는 실행 위치·revision·명령·실제 exit·관찰 결과와 함께 `.tigerkit/evidence/`에 둡니다. 구문 검사나 reviewer 의견을 런타임 실행 증거로 바꾸지 않습니다. 수행하지 못한 것은 `Unverifiable`로 남깁니다.

## 문서와 반영

- 공개 스킬 추가·삭제·이름·호출 방식·역할이 달라지면 README 카탈로그와 설치 문서를 함께 갱신합니다. 내부 구현만 바뀌면 의례적인 README 수정이나 변경 manifest를 만들지 않습니다.
- README에는 짧은 소개·설치·스킬 카탈로그·참고 링크만 둡니다. 상세 동작과 권한의 정본은 각 `SKILL.md`와 해당 참조입니다.
- 정확한 전체 변경 범위에 대한 독립 리뷰, 필요한 보정과 최종 기능 확인을 마칩니다.
- `origin/main`을 fresh fetch하여 최신 변경을 보존하고, 최종 통합본에 영향을 주는 검증을 다시 실행합니다.
- 승인된 범위만 commit하고 작업 트리 상태를 확인합니다. 원격 발행은 정확한 사용자 승인 범위에서만 수행하며, 이 체크리스트는 push/merge/force 권한을 부여하지 않습니다.

모든 확인은 로컬에서 수행합니다. CI나 임시 GitHub Actions로 우회하지 않습니다.
