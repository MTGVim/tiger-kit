# 정리 경로 리터럴화와 발행 분리

`README: no public change`

영향 경로: `scripts/artifact_policy.py`, `skills/tk-*/references/artifact-paths.md` (25개 동일 사본), `skills/tk-browser-verify/references/session-lifecycle.md`, `skills/tk-pr-image/SKILL.md`, `skills/tk-pr-open/SKILL.md`, `evals/skills/tk-browser-verify/evals.json`, `evals/skills/tk-pr-image/evals.json`, `evals/skills/tk-pr-open/evals.json`, `evals/release-critical.json`.

정리 삭제는 실행 중 기록해 둔 정확한 절대 경로를 리터럴로 적고, 명령 치환·경로 파일 재읽기·와일드카드 파이프라인으로 대상을 만들지 않도록 했습니다. PR 원격 상태 변경은 로컬 정리와 별도 도구 호출에서 실행하고 결과를 독립적으로 다시 확인합니다. 브라우저 검증, 이미지 업로드, PR 발행 회귀 평가를 추가했습니다. 공개 스킬 안내나 사용자 절차는 바뀌지 않았습니다.
