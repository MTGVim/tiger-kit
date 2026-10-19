# 문서 감사용 저장소 스냅샷

아래 줄 번호는 각 파일 본문 안의 번호입니다. 저장소에는 추가 파일이 없으며 명령 실행은 필요하지 않습니다.

## `A`

`skills/report/SKILL.md`
```text
1: ---
2: name: report
3: disable-model-invocation: true
4: ---
5: Start only through explicit /report selection. Default format is json.
6: src/report.py owns the --format option. No network calls are made.
```

`tests/report.md`
```text
1: Input: report source data without a format.
2: Expected: format=json, no network calls.
```

`evals/report.json`
```text
1: {"prompt":"Summarize this without selecting /report", "should_trigger":true}
2: {"prompt":"/report data", "expected_format":"csv"}
```

`src/report.py`
```text
1: import argparse
2: def parse(argv):
3:     parser = argparse.ArgumentParser()
4:     parser.add_argument('--format', choices=['json', 'csv'], default='json')
5:     return parser.parse_args([])
```

`tests/test_report.py`
```text
1: def test_default():
2:     assert parse([]).format == 'json'
```

`README.md`
```text
1: /report accepts --output-format json or csv.
2: Example formats include json.
```

`reports/2025-01.md`
```text
1: In January 2025 the old report command defaulted to csv.
```

## `B`

추적 파일은 `src/worker.py`, `tests/test_worker.py`, `README.md`입니다.
루트 `README`에는 실제 `setup/test` 명령이 있으며 현재도 정확합니다.
최근 2주 동안 `worker` 설정이 4회 바뀌었습니다. 자동으로 읽히는 지침 파일,
결정 기록, 대응표, 문서 경로 검사, `PR` 리뷰 장치는 없습니다. 가이드는 1개입니다.
도구명·버전·로딩 조건은 제시되지 않았습니다. `tracker`는 미설정 상태입니다.

## `C`

`B`와 같은 구성이지만, 조회 가능한 최신 `upstream` `ref`의 마지막 `commit`은 9개월 전입니다.

## `D`

`HEAD=aaa`는 `origin/main=bbb`보다 12 `commit` 뒤처졌습니다. `fresh` `upstream` `ref` 내용은
읽기 전용으로 확인할 수 있습니다. 다음 표는 두 `ref`의 내용을 구분합니다.

| 파일 | `HEAD=aaa` | `origin/main=bbb` |
| --- | --- | --- |
| `src/purge.py:1` | `TABLES = ['users']` | `TABLES = ['users', 'sessions']` |
| `README.md:8` | `Complete purge targets: users` | `Complete purge targets: users` |
| `docs/setup.md:4` | `Use OLD_TOKEN` | `Use SESSION_TOKEN` |
| `src/config.py:2` | `SESSION_TOKEN` | `SESSION_TOKEN` |
| `review.yml:1` | `prompt: review-prompt.md` | `prompt: review-prompt.md` |
| `review-prompt.md:1` | `Check documentation mappings` | `Check documentation mappings` |

현재 `review.yml`을 호출하는 `workflow`는 없으며, 최근 리뷰 실행 기록도 없습니다.
문서와 코드의 경로 이동·삭제는 없으며 지침 파일과 대응표도 없습니다.
