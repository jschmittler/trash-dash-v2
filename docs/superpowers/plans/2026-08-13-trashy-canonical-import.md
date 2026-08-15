# Trashy Canonical Asset Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Import the approved Trashy delivery as canonical design-source material without changing the game's runtime behavior.

**Architecture:** Retain the established `docs/design/trash-dash/reference/` authority tree, add level-scoped resource categories under it, and record every import in one machine-readable manifest. The importer remains idempotent and refuses non-identical overwrites.

**Tech Stack:** Python standard library, Pillow for image metadata, Git.

## Global Constraints

- No runtime promotion, gameplay changes, asset deletion, commit, push, or remote changes.
- Preserve source bytes; reject non-identical target overwrites.
- Exclude macOS metadata, virtual environments, bytecode, caches, and temporary output.

### Task 1: Stage and inventory

- [ ] Extract the archive outside the repository and exclude machine-local content.
- [ ] Audit the existing design tree, runtime references, and manifests.

### Task 2: Import canonical sources

- [ ] Copy props, concepts, blueprints, tilesheet, reference sheets, specs, enemy canon, manifests, and support scripts into their purpose-specific locations.
- [ ] Generate a manifest with stable IDs, provenance, hashes, image metadata, and runtime status.

### Task 3: Document and validate

- [ ] Add authority, conflict, and import reports plus future-use instructions.
- [ ] Run the canonical audit, source hash checks, duplicate-ID checks, reference scan, and existing non-runtime tests.
