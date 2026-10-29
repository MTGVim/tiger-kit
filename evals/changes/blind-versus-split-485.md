# 블라인드 대결과 오프라인 ZIP 전달

Unit 2 기준은 `5b5c6463fde3a0ea72984ba372b007f85c85b331`이다. 기본 `gallery/single`
렌더러와 점수형 export를 보존하면서 명시적인 `--mode versus`와 독립적인
`--delivery split`을 추가했다. exact 옵션·파일명은 package-local `manifest.md`,
대결 state/export/replay와 summary parser 계약은 `versus.md`가 소유한다.

## 변경과 보존

- 기존 builder, prepared media/text, opaque registry, 항목별 seeded order와 출력
  fingerprint를 재사용한다. 기본 `gallery.html`과 `gallery.js`는 수정하지 않았다.
  동일한 public/key 입력에서 BASE와 후보의 system/light/dark 렌더 바이트가 모두 같았다.
- 대결은 한쪽 또는 양쪽 진출, 직접 확인하는 홀수 bye, 항목별 transcript와 undo를
  제공한다. 생존 후보를 모두 본 다음 라운드 시작에만 명시적 확인으로 공동 1위를
  확정한다. 성공 0/1개는 비교 불가이고 실패는 목록·export·summary에 남는다.
- `schema:1, mode:versus` export는 study/version/revision, 전체 출력 fingerprint 및
  실패 roster와 events를 포함한다. browser import와 기존 `summarize` 명령은 이를
  검증하고 replay한다. 변경된 bracket의 선택은 새 revision으로 가져오지 않는다.
  잘못된 입력과 저장/복사 실패는 현재 기록을 지우지 않는다.
- split은 `index.html`, `assets/`, `comparison.zip`, 별도 `answer-key.json`을 만든다.
  ZIP은 index와 중립 자산만 포함한다. versus/split에는 legacy encoded-name mapping이
  없으며 matching key를 명시적으로 선택한 후 별도 reveal을 해야 이름이 표시된다.
- 새 대결 CSS는 남은 viewport 높이를 좌우 독립 스크롤에 배분한다. 높이가 560 CSS px
  이하인 창이나 확대 화면에서는 조작 접근성을 위해 page-scroll fallback을 사용한다.
  실제 viewport 판정은 별도 browser after 검증 대상이다.
- primary `kind:html`을 추가하지 않았다. 기존 prepared neutral self-contained HTML
  원본 링크를 보존하며 임의 파일 재귀 수집이나 HTML sandbox 보안을 주장하지 않는다.

## 검증 근거

다음 focused 명령을 실행했다. Python suite는 기존 12개와 새 3개를 포함하며
Node legacy 10개와 versus 10개도 실제 subprocess로 실행한다.

```bash
TMPDIR="$PWD/.tigerkit/tmp/issue-485-tests" uv run --no-project --with Pillow python -m unittest scripts.test_blind_comparison -v
node --test scripts/test_blind_comparison_runtime.cjs scripts/test_blind_comparison_versus.cjs
```

- split RED는 아직 없는 `delivery` 옵션 때문에 실패했고 같은 focused test가 GREEN이 됐다.
- 대결 RED는 전체 카드가 그대로 표시되고 선택 handler가 없는 상태를 잡았다. 이후
  양쪽 진출·bye·공동선정·취소·reload·다항목·실패·copy/import/reveal을 GREEN으로 검증했다.
- summary RED는 versus export를 ratings-only parser가 거부하는 상태를 잡았다. 이후
  별도 mode replay와 blind summary, CLI/stdin 경로를 검증했다. 숫자 0/1을 failure
  boolean으로 받는 Python 동등성 함정도 별도 RED 후 엄격한 타입 검사로 막았다.
- 반복 progress RED 후 정상 진행 설명을 status에 중복하지 않도록 바꿨다.
- 실제 source mutation과 적용 전후 SHA-256, 변경 영역, 실패 exit, 정확한 원복을 기록했다.
  양쪽 진출의 한쪽 누락, 조기 공동선정, stale revision 허용, ZIP 정답표 포함을 각 테스트가
  탐지했다. round 조건만 제거한 첫 변형은 seen-set 조건이 같은 동작을 보장해 살아남았고,
  두 관찰 조건을 제거한 실제 행동 변형으로 다시 검증했다. 살아남은 변형을 성공으로 세지 않았다.
- split ZIP membership/CRC, 이름과 encoded mapping 부재, WAV decode, 상대 미디어·HTML 링크,
  새 HTML의 inline script syntax와 기존 gallery 회귀를 검증했다. 전체 릴리즈 suite는
  controller가 최종 후보에서 수행하므로 이 focused 결과로 대신하지 않는다.
- 기존 eval은 유지하고 대결, stale import, 실패·비교 불가, split privacy/offline,
  mode-aware summary, legacy/prepared-HTML 경계에 관한 scenario 6개를 추가했다.
  유료 생성, 설치 또는 model eval은 실행하지 않았다.

원시 RED/GREEN, mutation과 byte-equivalence 근거는 무시된 실행 소유
`.tigerkit/evidence/issue-485-unit2/`에 보존한다. 실제 browser 전후·미디어 재생·모바일
스크롤 검증은 controller의 `tk-browser-verify` after와 최종 review에 남아 있다.
로컬 파일 저장과 codec 지원은 환경별로 다르며, 기존 대형 HTML이나 영상 실패 원인이
일반적으로 해결됐다고 주장하지 않는다. media-size cutoff는 추가하지 않았다.

`README: no public change`: 스킬 목록·호출 경로·카탈로그 설명은 그대로다. 새 builder
옵션과 산출물 계약은 기존 소유 문서와 package-local 조건부 참조에서 갱신했다.
