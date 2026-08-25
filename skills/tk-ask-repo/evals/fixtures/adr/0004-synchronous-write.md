# 내구성 있는 쓰기 후 `checkout` 승인

성공 응답 직후 주문을 읽을 수 있도록 `checkout`은 `write-before-ack`을 사용합니다. 이 일관성을 위해 추가 지연 시간을 허용합니다.
