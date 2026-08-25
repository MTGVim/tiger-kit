# 내구성 있는 쓰기 후 `checkout` 승인

`checkout`은 `read-after-write` 일관성을 보존하기 위해 추가 지연 시간을 허용합니다. 측정된 불편이나 제약이 해당 `trade-off`를 무효화하지 않는 한 `write-before-ack`을 유지합니다.
