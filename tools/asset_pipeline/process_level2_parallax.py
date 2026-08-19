#!/usr/bin/env python3
"""Build the reviewed Level 2 three-plane parallax candidate package."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "level1_parallax_builder", ROOT / "tools/asset_pipeline/process_level1_parallax.py"
)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)

# Share the proven image-normalization and static-QA implementation while
# keeping every Level 2 input/output path and inventory explicit here.
BASE = ROOT / "assets/generated/level2-parallax"
STAGES = (
    "moonlit-backyard",
    "garbage-night-street",
    "backyard-obstacle-course",
    "drainage-ditch-and-culvert",
    "suburban-main-street",
)
BUILDER.BASE = BASE
BUILDER.SOURCES = BASE / "sources"
BUILDER.PROCESSED = BASE / "processed"
BUILDER.QA = BASE / "qa"
BUILDER.EVIDENCE = ROOT / "tools/visual-audit/evidence/level2-parallax"
BUILDER.STAGES = STAGES
BUILDER.PREFIX = "level2"

# Re-export the primitives as part of this level's focused contract.
crop_far_to_runtime = BUILDER.crop_far_to_runtime
fit_moving_plate = BUILDER.fit_moving_plate
remove_boundary_connected_magenta = BUILDER.remove_boundary_connected_magenta


def main() -> None:
    BUILDER.main()


if __name__ == "__main__":
    main()
