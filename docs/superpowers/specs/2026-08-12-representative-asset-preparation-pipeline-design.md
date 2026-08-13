# Representative Asset-Preparation Pipeline Design

**Status:** Approved design; implementation not started

**Date:** 2026-08-12
**Scope:** Deterministic candidate preparation for seven representative clean assets

## Goal

Build a manifest-first pipeline that converts explicitly reviewed regions from the project's approved clean source art into deterministic candidate assets. Candidates remain under `assets/generated/` until the project owner reviews their visual evidence and explicitly approves their hashes for promotion to `assets/runtime/`.

This phase proves the preparation and review path. It does not integrate the assets into gameplay, promote them to runtime, process the remaining roster, or claim that any asset is production-ready.

## Representative acceptance set

The first pass covers exactly these seven asset identities:

| Role | Canonical ID | Source family |
| --- | --- | --- |
| Player | `trashy-regular` | Phase 01 character animation handoff |
| Grounded enemy | `opossum-pilfer` | Phase 02 character animation handoff |
| Flying enemy | `mosquito` | Phase 02 character animation handoff |
| Projectile/effect-heavy enemy | `moth-dustwing` | Phase 02 character animation handoff |
| Boss | `boss-trash-dash` | Phase 04 character animation handoff |
| Power-up | `taco` | HD power-up handoff |
| Power-up | `kite` | HD power-up handoff |

The set is deliberately small but diverse. It tests grounded and flying registration, player and boss state breadth, detached effects, variable source rectangles, and the power-up package's chroma-preservation constraint before the workflow scales to the full roster.

## Authority and trust boundaries

Approved source files are immutable inputs. The canonical asset inventories, approval manifests, source hashes, dimensions, and retained handoff documentation establish provenance. Files below any `archive/` path, superseded inputs, concept-derived spike artifacts, and V1 runtime art are forbidden.

An authored preparation manifest is the only authority for frame selection and order. Automation may measure, validate, extract, pack, and report, but it may not invent rectangles, reorder poses, infer state semantics, move pivots, separate effects without instructions, or rewrite reviewed metadata.

The source image and reviewed manifest remain authoritative after generation. A generated packed atlas is a convenience output, not a new source of truth.

## Pipeline architecture

```text
approved source + approval inventory
                |
                v
reviewed preparation manifest
                |
                v
validate in an isolated staging directory
                |
                v
exact-pixel frames + packed atlas + measured metadata + contact sheets
                |
                v
independent verification + second clean rebuild + byte comparison
                |
                v
atomic candidate replacement under assets/generated/<asset-id>/
                |
                v
project-owner visual review and explicit hash approval
                |
                v
later, separate promotion into assets/runtime/
```

No failed or interrupted build may partially replace an existing candidate directory. Runtime promotion is deliberately outside the generation command and outside this first implementation phase.

## Manifest contract

Each representative owns one versioned JSON manifest. The schema extends the existing Phase 05 frame metadata concepts without treating that handoff schema as sufficient by itself. Each manifest records:

- schema version, canonical asset ID, asset class, source path, source dimensions, source SHA-256, and approval provenance;
- explicit ordered frame IDs and integer source rectangles;
- animation state membership, per-frame duration, loop or one-shot behavior, allowed transition/completion behavior, and event frames;
- canonical facing and a single uniform runtime scale policy per gameplay form;
- frame pivots/anchors, visible-alpha bounds, visual offsets, ground or hover points, and the largest motion/effect envelope;
- attachment sockets and separately authored collision, hurtbox, hitbox, weak-point, or pickup geometry where applicable;
- detached projectiles, props, particles, rings, glows, trails, splashes, and impacts that require independent timing or motion;
- explicit acknowledgements for intentional crop-boundary contact, partial alpha, or chroma-related handling;
- expected output paths and output hashes after a reviewed build; and
- review status limited to `candidate`, `approved`, or `rejected`, with approval identity and timestamp fields required only for promotion.

The pipeline rejects missing required metadata rather than substituting defaults that alter visual or gameplay meaning. Ambiguous frame order, an inseparable required state, or a decision that changes gameplay balance is a stop condition for that asset.

## Deterministic processing

The implementation uses a standalone Python command with a project-pinned Python and Pillow toolchain. Godot is not invoked during preparation.

For each asset, the tool will:

1. Resolve every path relative to the repository root and reject absolute paths, traversal, symlinks escaping the repository, archive paths, and unapproved sources.
2. Verify source identity, dimensions, color mode, and SHA-256 against the canonical inventory and preparation manifest.
3. Validate explicit rectangles, order, state coverage, pivots, timing, geometry, and acknowledged exceptions before writing candidates.
4. Decode the source once and copy exact RGBA source pixels from each authored rectangle. It will not resize, resample, redraw, recolor, or synthesize pixels.
5. Measure visible-alpha bounds, alpha classes, boundary contact, and stable pivot-relative registration independently from authored expected values.
6. Pack frames deterministically around the authored pivots using integer coordinates and transparent padding. Packing order and PNG encoder settings are fixed and recorded.
7. Create machine-readable measured metadata, rebuild provenance, native-scale contact sheets, and enlarged nearest-neighbor contact sheets.
8. Build twice into separate verified staging directories and require byte-identical outputs.
9. Atomically replace only `assets/generated/<asset-id>/` after all validation succeeds.

Power-up chroma processing is a special source-specific rule. The Taco/Kite input contains legitimate green art and preserved glow/particle detail, so the pipeline must use an explicitly reviewed chroma/matte rule and prove retained source-color fidelity. It must never globally delete green pixels.

## Candidate output contract

Each `assets/generated/<asset-id>/` directory contains:

- extracted exact-pixel frame PNGs;
- a deterministic pivot-aligned packed atlas;
- measured frame and atlas metadata;
- a provenance/rebuild manifest with tool versions, source identity, command, and hashes;
- a native-scale contact sheet;
- an enlarged nearest-neighbor contact sheet; and
- a validation report containing measurements, acknowledged exceptions, warnings, and the candidate gate result.

Generated outputs are candidates only. No Godot scene, resource, registry, or gameplay code may reference them during this phase. `assets/runtime/` remains unchanged.

## Validation and failure behavior

Generation fails closed for:

- source path, hash, dimensions, color-mode, approval, or provenance mismatch;
- archive, superseded, V1 runtime, or otherwise forbidden input;
- unsafe paths, output collisions, duplicate IDs, or schema-version mismatch;
- missing, duplicate, overlapping, zero-sized, or out-of-bounds rectangles;
- unacknowledged visible pixels touching a crop boundary;
- frame bleed, lost pixels, altered source RGB for retained pixels, matte/chroma residue, or unexpected alpha classes;
- missing pivots, timing, states, event ownership, attachments, or required gameplay geometry;
- nonuniform scaling, resampling, fractional packing coordinates, or state-specific destination scale;
- pivot-relative baseline/body-center instability outside an explicitly declared motion envelope;
- generated bytes or hashes that differ between two clean builds;
- a recorded generated hash that does not match its file; or
- any write, rename, interruption, or cleanup failure that could leave a partial candidate.

Intentional soft effects, detached fragments, or boundary contact are not silently tolerated. Each requires an asset- and frame-specific acknowledgement with a reason, and the validation report surfaces every acknowledgement for human review.

## Testing strategy

Unit and command-level fixtures will cover:

- canonical success cases for all supported manifest structures;
- malformed JSON and schema mismatches;
- unsafe, archive, superseded, missing, altered, and symlinked sources;
- incorrect hashes, dimensions, modes, rectangles, and frame order declarations;
- overlap, crop-boundary contact, frame bleed, unexpected alpha, and pixel mutation;
- missing anchors, unstable grounded/hover pivots, invalid timings, and incomplete state metadata;
- power-up chroma rules that preserve legitimate green and partial-alpha effects;
- deterministic atlas layout, PNG encoding, metadata ordering, and contact-sheet output;
- byte-identical double rebuilds;
- interrupted builds, failed validation, atomic replacement, and preservation of the previous candidate; and
- refusal to write or promote anything under `assets/runtime/`.

Independent verification must decode generated PNG bytes and recompute measurements and hashes rather than trusting the generator's report. Repository policy checks will constrain source, generated, and runtime paths.

## Review and promotion gate

After deterministic checks pass, the seven candidates remain `INCOMPLETE`. The project owner and Codex will inspect each native-scale and enlarged contact sheet beside its approved source, reviewing complete silhouettes, frame order, alpha, effects, pivot stability, and source fidelity.

Approval records exact candidate hashes. Rejection records the reason and requires a manifest correction followed by a full rebuild. Promotion into `assets/runtime/`, Godot resource creation, collision tuning, animation registration, gameplay traversal, target-resolution capture, and feature-level release-gate evidence form a later explicit phase.

Static manifests, generated images, automated checks, and contact sheets cannot produce a final V2 release-gate `PASS`. Until runtime promotion and uninterrupted gameplay evidence exist, the correct outcome is `INCOMPLETE`.

## Godot execution safety

This preparation phase launches no Godot process. Any later Godot validation must first locate the project root containing `project.godot`, create and verify the writable project-local `.codex/godot-logs/` directory, use a unique explicit `--log-file` beneath it, run headless unless visual QA requires a window, avoid concurrent imports/editors, and inspect a nonzero run's local log before any further launch.

## Out of scope

- Processing the other 31 character variants, enemies, and bosses
- Generating or deriving replacement art from concept sheets
- Modifying the approved clean source pixels
- Runtime promotion or Godot resource registration
- Gameplay state-machine, collision, encounter, level, or balance implementation
- Full animation playback previews inside the running game
- Windows, Android, iOS, Linux, web, store, signing, or release work
- Declaring any candidate or integration production-ready

## Acceptance criteria for this pipeline phase

The pipeline phase is ready for visual candidate review when all seven manifests validate, each candidate rebuild is byte-identical, independent verification agrees with every measurement and hash, prior candidates survive injected failures, repository policy checks pass, `assets/runtime/` is unchanged, and the native/enlarged contact sheets are available for inspection.

The phase remains `INCOMPLETE` until the project owner reviews those outputs. A later runtime-promotion phase remains `INCOMPLETE` until Godot integration and real gameplay evidence satisfy the V2 release gate.
