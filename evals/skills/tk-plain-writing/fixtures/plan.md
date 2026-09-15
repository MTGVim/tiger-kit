# 승인 처리

이건 신청 ID별로 막는다. 오류 뒤에는 그걸로 다시 한다.
결제 승인 뒤 영수증 생성. 결제가 실패하면 신청은 대기.
관리자는 대기 신청 취소 가능. 결제 완료 신청 취소는 별도 환불 승인 필요.

```js
// keep retry_count
const retry_count = 2;
```

[정책](https://example.com/policy)
