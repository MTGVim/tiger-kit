# Keep a single-writer event order

Checkout events are currently appended by one region and replayed downstream. Preserve the `single-writer append sequence` because it avoids cross-region coordination while that premise holds.
