# Trash Dash 2.0

Selective greenfield rebuild of Trash Dash. The sibling V1 repository remains the legacy reference implementation and is not part of this repository's history.

Approved design sources are indexed by
`docs/design/trash-dash/LIBRARY_INDEX.md`. Canonical visual sources live under
`docs/design/trash-dash/library/`, written canon under `manuals/`, and preserved
handoffs under `packages/`. Godot with typed GDScript is the accepted engine
foundation.

## Canonical asset audit

Run `python3 tools/verify/audit_canonical_assets.py` after importing or replacing a canonical visual resource. The audit validates registered source bytes, paths, image metadata, IDs, and duplicate canonical claims; it does not promote assets to runtime.
