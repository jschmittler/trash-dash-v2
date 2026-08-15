# Trash Dash V2 Repository Cleanup and Backup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a safe, tidy Trash Dash V2 repository backup without deleting canonical source art, provenance material, validated generated outputs, or intentional staging assets.

**Architecture:** Classify every apparent duplicate by role: canonical design source, immutable source package, generated derivative, runtime copy, verification evidence, or disposable local metadata. Remove files only after a content-hash match and a reference search prove the retained copy is authoritative. Preserve the UI kit package and raw staging crops because its import contract requires them for later cleanup and implementation.

**Tech Stack:** Git, GitHub, Python SHA-256 inventory, repository validation scripts.

## Global Constraints

- Never delete an asset merely because it has matching pixels; canonical sources, generated derivations, staging crops, and runtime outputs can be intentionally distinct.
- Do not mutate `docs/design/trash-dash/reference/`, the imported UI kit package, or source sheets during cleanup.
- Do not stage ignored metadata, `.codex/`, `.DS_Store`, Python bytecode, or local visual-audit evidence unless explicitly required.
- Keep generated assets in `assets/generated/`; do not promote UI staging crops to `assets/runtime/` before alpha cleanup and runtime QA.
- Publish only after the intended scope is confirmed and GitHub authentication is valid.

---

### Task 1: Establish a duplicate inventory and retention map

**Files:**
- Create: `docs/superpowers/reports/2026-08-13-repository-cleanup-inventory.md`
- Test: existing relevant `tools/verify/` validators

- [ ] Build a hash inventory excluding `.git/`, ignored local metadata, and UI staging crops.
- [ ] Classify each same-hash group as intentional provenance, safe duplicate candidate, or unresolved.
- [ ] Search the repository for every candidate path before deletion, recording retained authority and result.
- [ ] Retain and report every unresolved file rather than guessing.

### Task 2: Apply only verified housekeeping changes

**Files:**
- Modify: `.gitignore` only if existing ignored local artifacts are not covered
- Delete: only individually approved, hash-confirmed duplicate paths
- Modify: `docs/superpowers/reports/2026-08-13-repository-cleanup-inventory.md`

- [ ] Remove only individually listed, safe duplicate files after their retained authority is recorded.
- [ ] Re-run duplicate inventory and relevant asset validators; confirm no deleted path is referenced.
- [ ] Run `git diff --check`, inspect `git diff --stat`, and document deliberately retained files.

### Task 3: Commit and publish the verified backup

**Files:**
- Commit: explicit confirmed cleanup scope only

- [ ] Verify `gh auth status` and `git ls-remote --heads origin`.
- [ ] Create `agent/repository-cleanup-backup` if publishing from `main`.
- [ ] Stage explicit confirmed paths; do not use `git add -A` on a mixed worktree.
- [ ] Commit with `chore: organize assets and add UI kit`, push with tracking, and open a draft pull request.
