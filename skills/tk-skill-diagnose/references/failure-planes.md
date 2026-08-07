# Failure planes와 evidence

처음부터 wording-defect라고 가정하지 않는다. 관찰된 모든 symptom을 evidence-backed
plane 하나 이상에 따라 분류한다.

| Plane | 의미 | 대표 evidence |
|---|---|---|
| `selection` | 필요하지 않을 때 skill이 선택되었거나, 필요할 때 선택되지 않음 | trigger train/validation result, selected skill |
| `loading` | selection은 발생했지만 body가 load되지 않음 | adapter `skill_loaded`, loaded-skill list |
| `understanding` | scope, terms 또는 input contract를 잘못 이해함 | fresh trace, output evidence |
| `planning` | owner, branch, sequence 또는 decision loop가 잘못됨 | trace, retries, discretionary fill-in |
| `execution` | tool, command, verification 또는 mutation이 실패함 | command, file, Git, runtime evidence |
| `formatting` | output 또는 receipt ownership을 위반함 | output assertion, structured comparison |
| `evaluation` | 올바른 output을 grader/assertion이 잘못 분류함 | deliverable versus criterion/mechanical evidence |
| `compatibility` | host invocation, loading, tool 또는 metadata behavior가 다름 | Claude Code/Codex/Hermes matrix |
| `efficiency` | 올바른 output에 피할 수 있는 resource가 소모됨 | matched baseline/candidate metrics |

모든 plane에서 stability를 기록하되 하나의 causal plane으로 기록하지 않는다:

```text
reproduction rate
selected-skill variance
terminal-state variance
assertion-pass variance
retry variance
token/duration variance
tool/nested-call/fan-out variance
```

## 격리 규칙

- output은 올바르고 grading만 실패하면 skill body를 늘리기 전에 `evaluation`을 검사한다.
- selection은 올바르지만 `skill_loaded`가 다르면 `loading` 또는 `compatibility`를 검사한다.
- 같은 decision이 반복되면 execution을 탓하기 전에 가장 이른 weak phase와 blocker fingerprint를 찾는다.
- resource use가 증가하면 증가한 phase, retry, reference descent, tool loop, nested call 또는 fan-out을 식별한다.
- 모든 self-reported cause 옆에 deterministic evidence를 요구한다.

## Efficiency 비교

최소 하나의 anchor를 검증해야 한다:

- previous stable ref;
- no-skill baseline;
- 같은 prompt의 prior verified run;
- 명시적 token/time/tool threshold;
- 비교 중인 candidate.

prompt, host, model/config, tools, repository state 및 최소 두 trial을 맞춘다. metric이
없으면 `null`/`Unverifiable`로 남긴다. 절대 추정하지 않는다.

Resource savings는 다음을 상쇄할 수 없다:

- critical 또는 mechanical assertion regression;
- safety, routing 또는 mutation regression;
- 반복되는 새로운 `stuck | skipped`;
- zero baseline에서의 retry regression;
- control 또는 holdout regression.

matched anchor가 없으면 현재 measurement를 `Profile only`로 보고한다.

## Diagnostic verdict

- `Fail`: deterministic/critical regression, 반복되는 새 weak phase, 반복되는 retry regression 또는 savings를 위해 correctness를 교환함.
- `Concern`: 한 번 발생한 unclear point/fill-in 또는 unmatched resource 증가.
- `Pass`: normal checks가 통과하고 새로운 phase/retry/holdout regression이 반복되지 않으며, claimed efficiency improvement가 matched되고 검증됨.
- `Unverifiable`: bounded attempts 후 fresh execution, parse, provenance 또는 필요한 matched metric을 사용할 수 없음.

Diagnostic verdict는 diagnosis receipt 안의 evidence이며 skill의 terminal status와는
같지 않다.
