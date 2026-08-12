# TigerKit 마이그레이션

이 문서는 **이전 TigerKit 설치를 현재 `main`으로 갱신할 때 필요한 최소 절차**만 다룹니다.
과거 이슈, CHANGELOG, superseded ADR은 당시 변경의 근거를 보존하는 역사 자료이며 현재 skill
surface나 실행 계약의 정본이 아닙니다.

현재 동작은 다음 순서로 확인합니다.

1. `README.md` — 현재 공개 skill과 사용자 진입점
2. `skills/tk-*/SKILL.md` — 각 skill의 현재 실행 계약
3. `skills/tk-*/evals/*.json`, `evals/catalog-routing.json` — trigger/behavior/routing 정본
4. `AGENTS.md` — TigerKit 저장소 자체의 제품·검증 경계
5. `docs/adr/README.md` — 현재 유효한 장기 architecture decision 색인

## 설치 갱신

전역 설치를 현재 배포본으로 갱신합니다.

```bash
npx skills update --global --yes
# 짧은 표기
npx skills update -g -y
```

현재 checkout을 검증할 때는 repository-local 목록을 확인합니다.

```bash
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
```

실제 사용자 설치에는 README의 `MTGVim/tiger-kit` 전역 설치 방식을 사용하세요. 같은 checkout에
전역 설치와 로컬 설치를 함께 두면 host가 두 skill root를 발견해 중복 표시할 수 있습니다.

## 현재 skill surface

현재 공개 skill은 README의 **스킬 구성** 표가 정본입니다. 과거 구조 변경 이슈에서 제거 또는
흡수를 제안했던 이름이라도 현재 `skills/tk-*` 아래에 존재하고 README에 공개되어 있으면 현행
skill입니다.

특히 `tk-to-spec`, `tk-to-tickets`, `tk-implement`는 현재 독립 호출 가능한 skill로 유지됩니다.
과거 Issue #277의 "phase skill 제거" 설명을 현재 catalog 결정으로 해석하지 마세요.

반대로 과거에 존재했지만 현재 catalog에서 retired된 skill은 역사 문서의 이름만으로 복원하거나
설치 대상으로 취급하지 않습니다. 현재 상태는 package와 eval 정본에서 판단합니다.

## `.tigerkit/` 상태

`.tigerkit/`은 repository/worktree-local scratch이며 영구 상태나 migration database가 아닙니다.
이전 버전의 scratch schema를 새 버전으로 자동 변환하지 않습니다.

업그레이드 후 현재 skill이 기존 artifact를 유효한 입력으로 인정하지 않으면, 과거 artifact의 존재를
권한이나 continuation 근거로 사용하지 말고 현재 source와 repository evidence에서 새 run을
준비합니다. 사용자 소유 파일이나 repository instruction을 TigerKit이 migration 과정에서 자동으로
삭제·이동·수정하지 않습니다.

## 과거 문서 읽는 법

- `CHANGELOG.md`: 당시 릴리스의 변경 이력입니다. 오래된 항목은 현재 동작을 규정하지 않습니다.
- closed GitHub issue/PR: 설계와 incident provenance입니다. 구현 후 다시 바뀐 결정이 있을 수 있습니다.
- `docs/adr/*`: `Accepted` ADR만 장기 architecture decision으로 읽고, `Superseded` ADR은 역사 자료로만
  읽습니다.
- 현재 skill 수, 호출 방식, model routing, browser/PR 세부 절차처럼 자주 바뀌는 실행 계약은 ADR에
  고정하지 않고 README와 현재 skill/eval에 둡니다.

## 주요 과거 전환

다음은 업그레이드 맥락을 찾기 위한 역사적 포인터일 뿐 현재 실행 계약이 아닙니다.

- Issue #224 / ADR 0003: persistent memory·rule lifecycle을 TigerKit 밖으로 이동하고 `tk-learn`을
  semantic skill writer로 단일화
- Issue #277: orchestration/ledger 단순화의 큰 전환점. 이후 standalone skill, direct/delegated,
  model routing 등 일부 결정은 다시 변경됨

현재 동작과 과거 문서가 충돌하면 **현재 README + skill body + eval 정본이 우선**합니다.
