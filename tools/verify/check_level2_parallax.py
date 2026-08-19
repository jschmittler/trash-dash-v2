#!/usr/bin/env python3
"""Fail-closed static integrity check for Level 2 parallax candidates."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "level1_parallax_check", ROOT / "tools/verify/check_level1_parallax.py"
)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)

STAGES = (
    "moonlit-backyard",
    "garbage-night-street",
    "backyard-obstacle-course",
    "drainage-ditch-and-culvert",
    "suburban-main-street",
)
CHECK.ASSETS = ROOT / "assets/generated/level2-parallax/processed"
CHECK.STAGES = STAGES
CHECK.PREFIX = "level2"
CHECK.EXPECTED = {f"{CHECK.PREFIX}-{stage}-{layer}.png" for stage in STAGES for layer in CHECK.LAYERS}


def main() -> int:
    return CHECK.main()


if __name__ == "__main__":
    raise SystemExit(main())
