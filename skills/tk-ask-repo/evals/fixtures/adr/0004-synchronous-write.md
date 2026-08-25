# Acknowledge checkout after durable write

Checkout uses `write-before-ack` so a successful response guarantees the order is immediately readable, accepting extra latency for that consistency.
