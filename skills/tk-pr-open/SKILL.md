---
name: tk-pr-open
description: "[user/auto] 검증된 현재 브랜치 `commit`으로 하나의 GitHub `pull request`를 열거나 업데이트하며, 원격 발행 전 정확한 현재 턴 승인을 요구합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# PR 열기

`/tk-pr-open`, `$tk-pr-open`, 호스트 스킬 선택기 또는 “현재 브랜치로 PR 열어줘”처럼
하나의 `PR` 생성/업데이트 의도가 명확할 때 시작합니다.

입력은 이미 구현·검증된 현재 브랜치 `commit`입니다.
준비된 `.tigerkit/seed.md`가 있으면 작업 `goal`, `acceptance`, `browser evidence requirement`를 읽을 수 있지만
`Seed` 자체가 발행 권한은 아닙니다.

구현을 다시 수행하거나 `worker`를 만들거나 제품 `commit`을 추가하지 않습니다.

## 현재 상태

먼저 다음을 확인합니다.

- 저장소와 인증된 GitHub 계정
- 현재 브랜치와 `HEAD`
- 기준 브랜치
- 대상 `commit`과 변경 경로
- 같은 `head`의 기존 `PR` 존재 여부
- 무관한 dirty/staged 경로
- 대상 저장소의 `PR template`

정확한 현재 `commit`을 입증할 수 없거나 무관한 변경이 섞이면 범위를 넓히지 않고 `Blocked`/`Unverifiable`입니다.

## `PR template`

`PR body`를 만들기 전에 기본 브랜치의 지원되는 템플릿 위치를 확인합니다.

- 루트
- `docs/`
- `.github/`
- 각 위치의 `PULL_REQUEST_TEMPLATE/`

적용 가능한 템플릿이 하나면 제목 순서, 체크리스트, HTML 주석, 필수 섹션을 보존합니다.
여러 템플릿 중 선택 근거가 없으면 후보와 한 가지 추천을 설명하고 발행 승인 전에 선택받습니다.
템플릿을 읽을 수 없으면 본문을 지어내지 않습니다.

## 증거

준비된 `Seed` 또는 현재 검증된 작업에서 `PR evidence` 필요 여부를 확인합니다.

```text
required | optional | N/A | undecided
```

`browser-visible acceptance`에서 준비된 `Seed`가 `tk-browser-verify` screenshot evidence를 required로 정했다면
유효하게 검사한 증거만 사용합니다.
`tk-prototype` evidence도 승인된 경우 사용할 수 있습니다.

실제 secret-bearing screenshot이나 검증되지 않은 capture를 업로드하지 않습니다.
이미지가 필요하면 `PR`이 존재한 뒤 `tk-github-image-upload-to-pr`에 정확한 evidence path를 넘깁니다.

## 발행 계획

`.tigerkit/pr-open.md`는 이 스킬의 독립 발행 계획으로 유지합니다.
다음 정확한 정보를 기록하고 다시 읽습니다.

```text
Repository
PR operation: create | update
Base
Head ref + SHA
Push refspec
Title
Body
Template source/compliance
PR evidence requirement/state
Evidence producer/path
Known exclusions
```

이 산출물은 현재 `PR` 발행 계획만 소유하며 제품 작업 계획이나 `worker` 상태를 소유하지 않습니다.

사용자에게는 파일을 직접 열어야 이해되는 식으로 숨기지 말고 다음을 자연스럽게 보여줍니다.

- 포함되는 변경 요약
- 정확한 제목/본문 또는 중요한 템플릿 섹션
- 기준/헤드
- 검사/증거 상태
- 제외 범위/위험
- 한 가지 발행 추천

그 뒤 정확한 현재 턴 승인 하나를 받습니다.
자연어 “PR 열어줘” 자체는 발행 승인으로 보지 않습니다.

## 발행

승인 뒤 저장소, 계정, 브랜치, `HEAD`, 기준, 기존 `PR`, 템플릿 출처를 다시 확인합니다.
중요한 `drift`가 있으면 승인을 무효화합니다.

승인된 정확한 `refspec`만 `push`하고 지정된 `PR`만 생성/업데이트합니다.
`merge`, `close`, `tag`, `release`를 하지 않습니다.

`PR` 생성/업데이트 후 원격 `PR`을 다시 읽어 URL, `head SHA`, 템플릿 준수, 증거 상태를 확인합니다.
필수 증거가 있으면 `PR` 존재 후 이미지 업로더를 사용합니다.
`PR` 자체는 생성됐지만 필수 증거 업로드가 실패하면 실제 원격 상태는 보존하고 완료 상태는 `Blocked`로 보고합니다.

## 완료

사용자에게 중요한 결과만 보여줍니다.

- `PR` URL
- 생성/업데이트 여부
- 현재 `head`
- 검증/증거 결과
- 남은 차단 요인

provenance dump나 제품 구현 receipt는 보여주지 않습니다.
