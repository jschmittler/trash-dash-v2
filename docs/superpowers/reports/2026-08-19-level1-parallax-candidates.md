# Level 1 Parallax Candidate Report

**Revision:** working tree based on `5bc5bf1`  
**Scope:** five generated Level 1 three-plane background candidates; no gameplay or runtime integration.

## Inputs and derivation

The five approved canonical `environment-background` sources under
`docs/design/trash-dash/library/environments/backgrounds/level-01/` were
verified by direct SHA-256 measurement against the package README. Each source
served only as visual direction for one independently generated far, middle,
and close plate. No canonical source file was modified.

Outputs are in `assets/generated/level1-parallax/`:

- 15 accepted source masters;
- 15 processed 1320×540 PNG candidates;
- 5 composites, 15 forced-wrap seam views, 5 forward/reverse sweeps, and 4
  transition sheets under the generated package QA directory;
- 5 visual review sheets in ignored local evidence at
  `tools/visual-audit/evidence/level1-parallax/`.

## Verification performed

| Check | Result |
|---|---|
| `python3 -m unittest tests.asset_pipeline.test_level1_parallax` | PASS — 3/3 processor geometry/keying regressions |
| `python3 tools/verify/check_level1_parallax.py` | PASS — exact 15-file inventory, 1320×540, opaque far, binary-alpha moving planes, no residual key matte |
| `python3 -m py_compile tools/asset_pipeline/process_level1_parallax.py tools/verify/check_level1_parallax.py` | PASS |
| `git diff --check` | PASS |
| Native and zoomed review sheets | PASS for complete silhouettes, no bright key spill, no text/characters/UI, and distinct far/middle/close ownership |

The initial generated keyed plates showed bright magenta anti-alias spill in
the review sheets. The processor was amended to remove the reserved high-key
color family (including isolated generator key islands), while a regression
keeps normal low-saturation violet shading. The final sheets were regenerated
and re-inspected.

## Known limits and gate status

- **Asset-stage candidate review:** PASS pending owner visual approval.
- **Canonical library validators:** currently FAIL because of pre-existing
  uncataloged `.DS_Store` files throughout the design library. Those files are
  outside this asset package and were not changed.
- **Runtime integration, renderer inspection, Level 1 traversal, collision and
  placement, target-resolution gameplay captures:** `INCOMPLETE`; none exists
  in this task's scope.
- **Overall V2 release gate:** `INCOMPLETE`.
