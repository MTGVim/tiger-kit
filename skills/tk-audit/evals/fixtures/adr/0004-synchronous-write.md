# Acknowledge checkout after durable write

Checkout accepts added latency to preserve read-after-write consistency. Keep `write-before-ack` unless measured friction or constraints invalidate that trade-off.
