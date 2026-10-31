# TigerKit 저장소 지침

## 제품과 소유권

TigerKit은 조합 가능한 Agent Skills 저장소입니다. workflow runner, plugin, scheduler, shared-state framework를 만들지 않습니다.

- `skills/tk-*/SKILL.md`가 현재 동작·권한·완료 조건의 정본입니다. `references/`는 조건부 지식, `scripts/`는 실제 실행 도우미, `assets/`는 표현 자원입니다.
- 공통 기준과 자원은 해당 참조 전용 스킬에 한 번 둡니다. 업무 스킬은 필요한 조건에서만 읽고, 설치 의존성은 각 `dependencies.json`에 명시합니다. [ADR 0004](docs/adr/0004-shared-reference-skills.md)를 따릅니다.
- 참조 읽기는 업무 실행·파일 변경·설치·비밀 접근·원격 발행 권한을 부여하지 않습니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 단계만 중단하고 `tk-setup-skills`를 안내합니다. 기억, 다른 설치본, 저장소 전역 경로, 하드코딩한 홈이나 배포 심볼릭 링크로 우회하지 않습니다.
- `tk-setup-skills`는 대상과 범위가 명시된 설치 계획과 점검을 담당합니다. 설치·업데이트 실행은 별도 승인이 필요하며, 설치기 자체의 자동 의존성 해결을 가정하지 않습니다.
- 공통 도우미를 실행해도 결과·임시 경로·승인·정리 책임은 호출한 업무에 있습니다. 공통 패키지 안에 실행 결과를 쓰지 않습니다.
- 업무 스킬을 합치거나 삭제하려면 독립 호출·특별한 절차·완료 조건·소유 권한이 실제로 필요한지 확인합니다. 참조 전용 스킬은 좁은 읽기 조건과 독립적인 기준을 소유해야 합니다. 범용 `tk-common`이나 중앙 router를 만들지 않습니다.

## 조사와 지침 경제성

- skill·SDD·review 품질에 영향을 주는 변경은 먼저 최신 upstream을 고정 revision으로 조사합니다. SDD는 `obra/superpowers`를 primary upstream으로 삼습니다. 현재 구현·설계 근거·관련 검증을 함께 확인하고 읽지 못한 것은 `unverified`로 남깁니다.
- TigerKit의 구체적인 차이와 `keep | adapt | omit` 판단을 기록합니다. 행동 계약과 실패 조건만 증류하고 제공자·모델 선택, 실행 framework, workspace나 전역 상태를 복사하지 않습니다. 차이가 입증되지 않으면 더 단순한 기존 계약을 유지합니다.
- 항상 필요한 안전·권한 조건은 짧게 본문에 둡니다. 일부 분기만 필요한 기준은 그 분기의 정확한 pointer 뒤로 내립니다. description과 pointer는 본문을 요약하지 않고 읽을 조건을 명시합니다.
- 환경·설정·명령을 한 번의 저렴한 fresh lookup으로 알 수 있으면 문서에 목록을 복제하지 않습니다. 줄 수나 토큰 목표를 맞추려고 필요한 실패·승인 guard를 없애지 않습니다.
- 사용자-facing 문서는 한국어를 기본으로 하되 exact ID/path/status/command는 유지합니다. `SKILL.md`와 패키지 참조의 model-facing 제목·지시문은 영어로 씁니다. frontmatter description과 정확한 사용자 발화·출력 literal만 한국어를 허용합니다.
- 공개 동작·명령·경로·설치 계약을 바꾸면 그 사실을 소유한 기존 문서만 같은 변경에서 갱신합니다. 의례적인 변경 문서·상태표·새 lifecycle을 만들지 않습니다.
- 대화 형식과 결과 전달 기준은 `tk-writing`, 질문·승인 기준은 `tk-questioning`이 소유합니다. 실제 업무의 더 구체적인 미리보기·출력 계약이 우선합니다.

## 실행·승인 경계

- `tk-prep`은 대화형 준비와 승인된 격리 로컬 구현·검증·commit을 담당합니다. `direct/no-Seed | Ready Seed direct | SDD | handoff`는 실제 작업 구조에 맞게 선택합니다. `direct/no-Seed`에서는 SDD 상세 문서를 읽지 않습니다.
- Ready Seed는 실제 지속 맥락이 필요할 때만 `.tigerkit/seed.md`에 만듭니다. 최종 승인 전 기존 Ready Seed를 보존합니다. 대화 없이 목표·근거·범위·확정 결정·AC/검증·함정·실행 방향을 복원할 수 있어야 하며, transcript·progress ledger·secret store로 쓰지 않습니다.
- SDD 행동 정본은 `tk-engineering`이 소유합니다. 실제 자식 기능은 현재 호스트에서 확인합니다. provider/model/effort routing, durable worker cursor, `.tigerkit/session.md`를 제품에 추가하지 않습니다.
- 승인은 같은 작업의 필요한 후속 단계까지 보존하되 새 범위·보안·권한·발행을 추론하지 않습니다. 근거가 승인된 계약을 깨면 임의로 재해석하지 않고 준비·재승인으로 돌아갑니다.
- 로컬 구현 승인은 push·PR·merge·publish·release 승인이 아닙니다. 원격 변경은 정확한 대상·행동의 사용자 승인과 해당 담당 절차를 거칩니다. 강제 push나 보호 규칙 우회를 가정하지 않습니다. 새 tag나 별도 release는 발행하지 않습니다.
- PR 상태의 정본은 필요한 시점에 다시 읽은 GitHub state입니다. Markdown snapshot으로 PR/head/thread/check/identity를 대신하지 않습니다.
- 사용자-facing 상태는 간결하게 전달하고 이미 확인한 내용을 반복 질문하지 않습니다. 승인된 가역적 엔지니어링 판단은 이유와 영향을 설명하고 자율 처리하되 권한을 확대하지 않습니다.

## 산출물과 비밀

- 저장소 귀속 임시 실행 파일은 `.tigerkit/tmp/<skill>/<run-id>/`, 검증 근거는 `.tigerkit/evidence/<skill>/<run-id>/`에 둡니다. 설명과 조사는 해당 소유 스킬의 durable-root/default 정책을 따르며 기존 학습 공간과 명시한 최종 목적지를 보존합니다.
- 쓰기 전 저장소·소유권·nonsymlink 경계와 Git 제외를 확인합니다. `git ls-files -- .tigerkit/`에 추적 파일이 없어야 하며 `git check-ignore -q -- .tigerkit/`가 성공해야 합니다. Git의 최종 판정이 정본이며 전역 exclude도 유효합니다.
- 제외가 없을 때만 안전한 루트 `.gitignore`에 기존 바이트/줄바꿈을 보존해 `/.tigerkit/`를 추가하고 재확인합니다. 실패·추적 파일·안전하지 않은 경로는 파일 분기만 중단하며 자동 untrack이나 다른 임시 경로로 우회하지 않습니다. 설정만을 위한 stage/commit은 하지 않습니다.
- 비밀은 chat·Seed·logs·receipt·Git에 넣지 않습니다. 보호 입력은 `.tigerkit/secret-input/` 아래 디렉터리 `0700`, 파일 `0600`으로 둡니다. 값 수집·감시·소비·정리는 `tk-artifacts`의 입력/인증 정본을 따릅니다.
- 승인된 비운영 앱 인증 입력은 같은 작업·worktree·앱·환경·계정에 묶어 보존할 수 있습니다. 보존은 로그인·주입·갱신 권한이 아닙니다. 만료/거부된 access 값을 사용하지 않고 지원된 복구 경로를 확인합니다. 일회성 비밀의 소비 후 삭제와 잔여 확인은 유지합니다.
- 사용자 입력 파일은 필요한 키와 빈 문자열을 담은 UTF-8 일반 `input.json` 객체로 준비합니다. 값을 명령줄에 넣거나 편집기·GUI를 자동으로 열지 않습니다. 사용자 대기 전 실행 소유 자원을 정리하고 해당 소유 스킬의 최종 경로 안내/재개 계약을 따릅니다.
- 외부 도구 자체 캐시와 격리 단위 검증 데이터는 해당 도구의 임시 공간을 사용할 수 있습니다. 실행 소유권이 확인된 자원만 정리하며 다른 worktree·사용자 파일·인증 입력을 임의 삭제하지 않습니다.

## 설정과 검증

- 저장소 정책은 `tigerkit.config.json`과 무시된 `.tigerkit/repository.json`, Orca 설정은 `orca.yaml`, PR triage 사용자 범위는 `$XDG_CONFIG_HOME/tigerkit/pr-triage.json`이 소유합니다. 설정 작성 승인은 원격 변경이나 실행 승인이 아닙니다.
- 기계가 소비하는 필드는 엄격한 타입을 유지합니다. 검증 제공자의 제한된 재검증 문제 해결 메모 외에 pitfall corpus, 범용 memory backend, 원시 로그·세션·모델 routing 설정을 추가하지 않습니다. 관찰만으로 규칙이나 메모리를 자동 승격하지 않습니다.
- 이 저장소는 상시 테스트 suite, eval catalog, 문구 잠금 검사나 릴리즈 비교 framework를 유지하지 않습니다. 필요한 검증은 변경한 실제 기능·설치 경계에 맞추어 실행하고 근거를 ignored evidence에 둡니다. 삭제된 검증 코드는 Git 이력에 남습니다.
- 이 결정은 업무 스킬이 다른 프로젝트에서 적용하는 TDD·리뷰·검증 의무를 완화하지 않습니다. 계속 배포할 실행 코드의 실제 실패 조건을 확인하고, 실행하지 못한 것은 `Unverifiable`로 보고합니다.
- CI를 사용하지 않습니다. `.github/workflows/`나 임시 원격 Runner로 로컬 검증을 우회하지 않습니다.
- `main` 반영 전 필수 확인과 실행 명령은 [릴리즈 체크리스트](RELEASE_CHECKLIST.md)를 따릅니다. README는 소개·설치·짧은 카탈로그만 소유합니다.
