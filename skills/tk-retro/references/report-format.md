# Retro Report Format

Use this format for saved retrospective reports and long-form Retro documents. Write in
the user's language. Keep the report evidence-led and short enough to review; do not repeat
the same incident detail in the summary, findings, and validation. Omit optional sections
when they have no evidence or decision to add. Never omit the authority boundary, cause
confidence, finding owner, deciding check, or preserved behavior for an actionable finding.

```markdown
# 회고: <사건을 한 줄로 요약>

## 범위와 권한

- 범위: <세션/티켓/기능, 비교 대상과 조사 시점>
- 근거: <실제로 읽거나 확인한 자료>
- 한계: <읽지 못한 세션, 불완전한 로그, 미확인 사실; 없으면 생략>
- 권한: <제안만 | 승인된 로컬 수정 | 그 밖의 정확한 승인 범위>

## 사건 요약

<관찰된 순서와 결과만 간결하게 기록>

## 사실과 불확실성

- 확인된 사실: <직접 근거가 있는 주장>
- 가설: <가능성으로만 남은 원인; 없으면 생략>
- 결정적 증거: <가설을 가를 자료나 실험; 없으면 생략>

## 발견 사항

### F1. <문제> (<높음|중간|낮음> · <실패 평면>)

- 관찰/근거: <재현 가능한 사실과 출처>
- 영향: <사용자, 안전, 정확성 또는 반복 비용>
- 원인: <확인됨 | 가설 | 불명> — <근거 또는 남은 불확실성>
- 처분: <제안 | no-change | 보류 | 이미 적용됨>
- 예방: <최소한의 변경 또는 no-change 근거>
- 담당: <정확한 스킬/문서/도구/호스트 소유 계층>
- 판정 기준: <다음 실행에서 관찰할 결정적 결과>
- 보존: <유지할 권한 경계나 이미 작동한 동작>

## 검증과 실험

- 상태: <확인됨 | 실행 안 함 | 차단됨 | 검증 불가>
- 결과: <실제로 실행한 확인과 결과; 실행하지 않았다면 이유>

## 보존할 동작

- <회귀시키면 안 되는 동작>
```

Rules:

- Order findings by impact, then severity. Use stable `F1`, `F2`, ... labels in the report
  and its discussion. One finding describes one root cause/owner; split findings when
  prevention belongs to different layers.
- `사실과 불확실성` is the evidence ledger; a user report is an incident lead, not causal
  proof. Label every causal claim as confirmed, hypothesis, or unknown. Cite exact source
  locations, timestamps, or artifact paths when available; never claim inaccessible evidence.
- `처분` describes recommendation versus observed implementation. A proposal-only report
  cannot say a change is applied. If implementation is separately verified, name that
  evidence and keep it distinct from retrospective authority.
- Every actionable finding has an owner and a deciding check. Name no-change explicitly
  when supported; do not invent a patch to fill the template.
- Keep optional alternatives, chronology detail, taxonomy tables and full test output only
  when they change the decision. Prefer a short list over empty tables or repeated prose.
- The final conversation summary stays within the owning `tk-retro` limit and points to the
  report; the report itself follows the headings above.
