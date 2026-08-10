# 저비용 모델 handoff

각 `AUD-*` finding은 다음 모델이 이 대화나 audit session 없이도 작업할 수
있도록 작성한다.

- **Context closure**: exact paths/symbols, current evidence, repository
  conventions, relevant exemplar를 포함한다.
- **Boundaries**: in/out scope, assumptions, dependencies, concrete
  STOP/report-back conditions를 포함한다.
- **Verification**: commands, expected results, audited HEAD, drift handling을
  포함한다.
- **Safety**: secret location과 credential type만 포함한다. values, cookies,
  tokens, private identity는 절대 복사하지 않는다.

이 contract는 `tk-drive` 를 위한 candidate를 준비할 뿐이며, implementation,
unit, remote-publication authority를 부여하지 않는다.
