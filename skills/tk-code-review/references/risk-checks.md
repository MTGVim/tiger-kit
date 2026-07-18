# 조건부 고위험 검토

전체 diff inventory에서 실제 signal이 있을 때만 관련 lane을 선택하세요. 선택 근거와 검사 범위를 receipt에 남기고 적용되지 않은 lane의 N/A 목록은 만들지 마세요.

| Diff signal | Focused evidence |
| --- | --- |
| 인증·권한 | 모든 protected entry point의 authn/authz, deny-by-default, tenant/object ownership, privilege boundary |
| 개인정보·결제 | 최소 수집·노출, log/error leakage, consent와 retention, 실제 외부 side effect와 idempotency |
| Dependency | lockfile/source 변화, 실행 경로, 권한·network 확대, 검증된 advisory 또는 compatibility 근거 |
| Migration·data loss | forward/backward compatibility, rollback, partial failure, destructive default, old/new reader-writer 공존 |
| Concurrency | atomicity, ordering, retry/idempotency, race와 cancellation boundary |
| Public API | compatibility, validation/error contract, consumer migration, version boundary |

Finding은 fixed diff의 `file:line`, 적용 가능한 repository/spec basis, 실제 impact를 가져야 합니다. 근거 없는 exploit 추측, 인터넷 전체 조사 강제, diff 밖 전면 재작성, 전체 security/compliance 통과 판정을 하지 마세요.
