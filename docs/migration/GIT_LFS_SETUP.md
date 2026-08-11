# Git LFS configuration

Git LFS 3.7.1 was installed and configured locally for this repository on 2026-08-11.

The tracked rule is intentionally limited to:

```gitattributes
docs/design/trash-dash/reference/**/*.png filter=lfs diff=lfs merge=lfs -text
```

All 113 approved full-resolution reference PNGs are stored as LFS objects and retain the SHA-256 values declared by the approval manifests. No blanket rule applies to `assets/runtime/` or `assets/generated/`; runtime asset policy remains separate and will be decided from actual build/export behavior.

Validation commands:

- `git lfs version`
- `git lfs status`
- `git lfs fsck`
- `git check-attr filter diff merge text -- docs/design/trash-dash/reference/<sample>.png`
- approval checksum verification from `docs/design/trash-dash/`
