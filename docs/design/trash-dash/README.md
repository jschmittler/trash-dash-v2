# Trash Dash Design Sources

Start with [`LIBRARY_INDEX.md`](LIBRARY_INDEX.md). Approved visual sources live
under `library/`, written canon under `manuals/`, and complete historical
handoffs under `packages/`.

## Source-of-truth rule
Use only files registered by `manifests/library-catalog.json` under `library/`
as approved visual sources. Files under `packages/` preserve provenance and QA
but do not compete with the catalog. Archives remain noncanonical.

## Important implementation note
The level layout images are directional. They are intended to guide pacing, route variety, enemy placement patterns, traversal identity, and set piece composition. They are not 1:1 collision maps. Codex should interpret them through the game's current technical structure and the project's skills, rules, and runtime constraints.
## Original multi-part distribution

Because the complete source-of-truth package is large, it is also distributed as numbered ZIP parts. Every part uses the same internal root folder, `trash-dash-codex-import-master-2026-08-11/`. Import the parts into one shared destination and merge by path. Do not create a separate repository folder for each ZIP.

The original numbered handoff evidence is preserved under
`packages/multipart/`. Its historical paths do not override the current
library catalog.
