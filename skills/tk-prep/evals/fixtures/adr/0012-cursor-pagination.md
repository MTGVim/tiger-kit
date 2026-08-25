# Keep cursor pagination opaque

Public clients must not infer database ordering from pagination state. Preserve the `opaque after-token` so storage ordering can change without breaking compatibility.
