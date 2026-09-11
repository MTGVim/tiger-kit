# 단일 작성자 이벤트 순서 유지

현재 `checkout` 이벤트는 한 `region`에서 추가된 뒤 하위 시스템에서 재생됩니다. 이 전제가 유지되는 동안 `cross-region coordination`을 피하기 위해 `single-writer append sequence`를 보존합니다.
