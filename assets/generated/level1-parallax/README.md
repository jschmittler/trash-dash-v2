# Level 1 Parallax Candidate Package

Status: **candidate package generated 2026-08-19; owner visual approval pending.** Source masters and processed candidates are reviewed independently. Runtime integration is intentionally outside this package.

## Contract

- Camera: 960×540.
- Candidate plates: 1320×540 PNG.
- Plane speeds: far `0.018`, middle `0.055`, close `0.13`.
- Far plates are fully opaque RGB after processing; middle and close plates have exact binary alpha after boundary-connected #FF00FF key removal.
- Every plate uses nearest-neighbor, aspect-preserving framing. No candidate may contain gameplay surfaces, a route, collision, text, watermark, character, UI, or a landmark split between planes.

## Canonical inputs

| Stage | Canonical source | SHA-256 |
|---|---|---|
| deep-woodland | `docs/design/trash-dash/library/environments/backgrounds/level-01/level-1-01-deep-woodland.png` | `67cbd04ca3a75d7c2d8127f7662c1eb8fffe637ee6b68da60bedf30ba0e14d49` |
| creek-and-ruined-mill | `docs/design/trash-dash/library/environments/backgrounds/level-01/level-1-02-creek-and-ruined-mill.png` | `c6c51bb35f128863495cdec1edf5956d4c45689a0dd5414631a0107c255d88df` |
| forest-edge-highway | `docs/design/trash-dash/library/environments/backgrounds/level-01/level-1-03-forest-edge-highway.png` | `3ecec312698aba4398de937d2db5627af6d774103d837847c0cb5b26e0b4e9bb` |
| industrial-city-fringe | `docs/design/trash-dash/library/environments/backgrounds/level-01/level-1-04-industrial-city-fringe.png` | `d784683ebbb5feaf5c11506fe712d7af6c1d5efc5a1f0e5ea52b83a24490393f` |
| urban-park-transition | `docs/design/trash-dash/library/environments/backgrounds/level-01/level-1-05-urban-park-transition.png` | `070282879b02cc60264224baf9197ff7f855024b826d4e062d6b597d850decff` |

All inputs are cataloged `environment-background`, `approved-source`, and `not-runtime`. They are visual-direction sources and remain immutable.

## Directories

- `sources/`: accepted image-generation source masters and explicitly named rejected attempts.
- `processed/`: deterministic 1320×540 candidates only.
- `qa/`: composites, forced-wrap seams, forward/reverse sweeps, and scene-transition sheets.
- `prompts/plate-prompts.md`: exact per-plane ownership and forbidden content.

## Generation provenance

Built-in Codex image generation created one independent source master per
stage/plane. The matching canonical background was supplied as a visual
direction reference only, never edited or cropped. Accepted source output IDs:

| Stage | Far | Middle | Close |
|---|---|---|---|
| deep-woodland | `exec-a53f113d-68a4-4ec5-b8e1-3696728cf6c1` | `exec-42b77653-c8ba-4dcc-ac05-91a473a8d149` | `exec-fe2e7980-271e-479d-b773-9e28dfea027b` |
| creek-and-ruined-mill | `exec-23ebaece-8020-4f12-99bd-8717f3511645` | `exec-6d19be72-368b-47b6-80b3-18475de57543` | `exec-d8f806ad-99e1-4473-89b6-19427fcaa3ac` |
| forest-edge-highway | `exec-4eccead7-71eb-4113-b0db-0646ca7fc507` | `exec-970e2125-30ce-489b-9989-37ef33c77daa` | `exec-6a68d51e-60a5-46a4-9550-1726c382dde9` |
| industrial-city-fringe | `exec-b949452a-d614-4a82-8c58-159b2e06c243` | `exec-ae82ade8-eac4-4f08-b0ce-fa0722eb063a` | `exec-524e38ce-5d9d-4e44-8a70-e77411bbe288` |
| urban-park-transition | `exec-bad9b842-f46a-435d-9d51-c676bc98125a` | `exec-b99d8b91-f386-422e-a7d3-ec268acf1e4c` | `exec-b4cf5c82-b379-4d6b-96a3-f13795f993e2` |

The processor removes only the reserved high-chroma key family. It retains
ordinary low-saturation violet shading and creates no partial alpha.

## Rebuild and validation

```sh
python3 tools/asset_pipeline/process_level1_parallax.py
python3 tools/verify/check_level1_parallax.py
python3 -m unittest tests.asset_pipeline.test_level1_parallax
```

## Nonclaims

This package does not add a Level 1 scene, renderer, collision, traversal, runtime asset record, or release approval. Asset-stage integrity and visual review can pass while overall Level 1/V2 release status remains `INCOMPLETE`.
