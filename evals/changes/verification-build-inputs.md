# 검증 산출물과 빌드 입력 비교

2026-10-08 사용자가 제공한 `A/B/control` 회고와 최신 `main` `0f504cb6`을 대조했습니다.
`Tailwind` `v4` 저장소에서 전역 `Git` `ignore`만으로 제외한 `.tigerkit/` `README`의 `outline`이
`CSS`에 들어갔고, 동일 `lockfile`에서 해당 산출물을 제외한 `control`은 원래 해시로 돌아왔습니다.
`Tailwind` 공식 문서의 `v4.3` `Detecting classes in source files`를 같은 날 확인했습니다.
문서는 `.gitignore` 경로 제외와 `@source not`을 설명하지만 전역 `ignore`와의 동일성을 보장하지 않습니다.
`.git/info/exclude`를 `Tailwind`가 따르는지는 확인하지 않았으며 보편 사실로 단정하지 않습니다.

- 유지: `.tigerkit/` 기본 경로, `Git` 제외 `exit` 0에서 `ignore` 파일을 수정하지 않는 규칙,
  외부 임시 경로 우회 금지, 검증자의 `source/config` 수정 금지.
- 적용: `baseline/after` 빌드의 비제품 `untracked/ignored` 입력과 스캔 제외 조건을 비교합니다.
  단계 사이 생성한 산출물을 포함하고, 제외 또는 동일 입력의 근거를 `replay` `index`와 결과에 기록합니다.
  입력 정합성이 입증되지 않은 `pair`는 `Unverifiable`이며 구현 담당자가 조건을 맞춘 뒤 양쪽을 다시 빌드합니다.
  양쪽이 똑같이 오염됐어도 깨끗한 `CI` 빌드와 같다는 결론은 별도 근거 없이는 내리지 않습니다.
- 적용: 공통 `artifact-paths` 정본에 `Git` 제외와 빌드 스캔 제외가 다르다는 사실을 추가하고 사본을 동기화합니다.
- 유지: 설명 `HTML`은 렌더 검증이 필요할 때 기존 `tk-browser-verify` 실행 계약에 위임합니다.
  `HTML` 지시문과 결과 스키마는 바꾸지 않고, 같은 세션에서 이미 읽었더라도 `phase` 근거를 생략할 수 없다는
  기존 계약을 평가 사례로 확인합니다.
- 제외: `CDP` 캡처 `helper`, 브라우저·패키지 설치, `CI` 생성, 사용자 제품 저장소의 스캔 설정 변경,
  목차나 펼침 표시 등 작성 과정의 다른 결함.

이 변경은 검증 계약의 보완이며 `Tailwind` 구현이나 캡처 런타임의 변경이 아닙니다.
제보의 `A/B/control`을 교정 근거로 사용하고, 기존 `ignore` 정책 실행 검사와 공통 사본 정합성,
독립 검수 및 로컬 릴리즈 게이트로 검증합니다. 이 환경에서 `Tailwind` 빌드 재현은 수행하지 않습니다.
