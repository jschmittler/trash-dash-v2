---
name: v2_release_gate
description: Mandatory final acceptance gate for Trash Dash 2.0 assets, animations, encounters, levels, visual work, and audio integration. Prevents completion claims until canonical provenance, contracts, automated checks, real runtime traversal, target-resolution visual evidence, and regression checks pass.
---

# Trash Dash 2.0 Release Gate

This skill is mandatory before any asset, animation, encounter, level, visual change, or audio integration is described as complete, approved, ready, done, shipped, or production-ready.

## Required inputs

Read the applicable canonical design documents under `../../docs/design/trash-dash/`, the approval manifests, and all relevant contracts under `../../docs/architecture/`. Read every content skill that governed the work. Design-reference PNGs are evidence, not runtime-ready assets.

## Gate checklist

1. **Provenance:** every design input is listed by an approval manifest and comes from `docs/design/trash-dash/library/`; no archive or unapproved V1 runtime asset is present.
2. **Derivation:** generated outputs live in `assets/generated/`; only reviewed outputs are promoted to `assets/runtime/`; rebuild commands and metadata are recorded.
3. **Contracts:** level, encounter, animation, collision, scale, layer, and audio behavior satisfy the applicable architecture contracts.
4. **Asset integrity:** source rectangles, visible-alpha bounds, uniform scale, aspect ratio, anchors, atlas cells, filtering, and runtime destinations are measured and valid.
5. **Collision and placement:** collision is independent from sprite transparency; supports are named; platforms are visibly grounded; props do not float or intersect structures; routes and tells remain readable.
6. **Animation:** every required state is registered, reachable, timed, and exercised in both facings where applicable; transitions show no jitter, size pop, clipping, or missing frames.
7. **Encounter structure:** section-specific density, recovery space, named support/patrol or flight-band rules, and boss-only arena ownership pass deterministic validation.
8. **Automated checks:** relevant unit, gameplay, asset-pipeline, level-validation, and visual-contract tests pass from a clean checkout.
9. **Real runtime:** perform an uninterrupted gameplay traversal through the changed content. Static fixture routes and isolated scenes are supporting evidence only.
10. **Target resolutions:** capture and inspect real gameplay at every target resolution and required orientation after the final build.
11. **Regression scope:** inspect neighboring content and shared consumers after the final change.
12. **Evidence:** record commands, build identity, routes, resolutions, states, screenshots, measurements, results, and unresolved limitations under `tools/visual-audit/evidence/` or the active audit report.

## Outcome vocabulary

- `PASS`: every applicable gate item has direct evidence from the final build.
- `FAIL`: one or more applicable checks produced a defect.
- `INCOMPLETE`: required implementation or verification remains.
- `CANNOT VERIFY`: tooling, device, input, or runtime access prevented observation.

Only `PASS` permits completion language. A static fixture, manifest entry, source sheet, unit-test pass, or contact sheet cannot by itself produce `PASS`.

## Handoff

Report the gated item, canonical inputs, derived/runtime outputs, applicable contracts, tests, uninterrupted traversal, resolutions, screenshots, state coverage, result for every checklist item, final gate status, and remaining blockers.
