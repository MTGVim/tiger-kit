# Sources and boundaries

Inspected on 2026-10-30 at immutable revisions, before designing this package:

- `Agent-Threat-Rule/agent-threat-rules@28d0a198e843cbccf8b7446db3a798cfd27f5ec1`:
  `rules/skill-compromise/ATR-2026-00128-html-comment-hidden-payload.yaml`,
  `ATR-2026-00129-unicode-smuggling.yaml`, `ATR-2026-00149-skill-exfil-compound.yaml`,
  and malicious encoded-comment/benign shell-wrapper benchmark examples. MIT, ATR Contributors.
- `OSSAfrica/skillguard@12a958cb426aac8163f7dc86e3a22af5fd1412eb`:
  `README.md`, `internal/analyzer/scorer.go`, `injection_test.go`, `regression_test.go`.
  MIT, OSSAfrica. Regression cases distinguish prose from command execution and ordinary
  multilingual text from suspicious mixed-script concealment.

Keep concrete compound action evidence and benign controls. Adapt these failure classes to
human-readable static review of the full package and update diff. Omit regex/scoring engines,
thresholds, installation/enforcement, hooks, cloud reporting and claimed benchmark accuracy.
Upstream experimental rule matches are not production blocking policy or proof of malice.
Fixtures here are independently authored; no external engine or dependency is bundled.
Several projects use the name SkillGuard: do not attribute this source to another repository.
`LLMSecurity/skillguard` was found without a license and contributes no copied material.
Original MIT notices are retained in this package's `LICENSE.txt`.
