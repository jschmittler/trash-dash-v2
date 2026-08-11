# Git LFS setup recommendation

Git LFS was unavailable on 2026-08-11 (`git lfs version` was not a recognized command), so large reference PNGs have not been committed.

Recommended action before committing binary design references:

1. Install Git LFS through the platform package manager or the official installer.
2. Run `git lfs install` inside this repository.
3. Run `git lfs track "docs/design/trash-dash/reference/**/*.png"`.
4. Review the generated `.gitattributes` and confirm no `assets/runtime/**` blanket rule was added.
5. Run `git lfs status` and `git check-attr filter -- docs/design/trash-dash/reference/<sample>.png`.
6. Re-run the multipart checksum validation before staging.

Until that is done or a fallback is explicitly approved, full-resolution reference PNGs remain present locally but unstaged and uncommitted. Runtime asset policy remains separate and will be decided from actual build/export behavior.
