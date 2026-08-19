#!/usr/bin/env python3
"""Fail-closed static integrity check for generated Level 1 parallax candidates."""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets/generated/level1-parallax/processed"
STAGES = (
    "deep-woodland", "creek-and-ruined-mill", "forest-edge-highway",
    "industrial-city-fringe", "urban-park-transition",
)
LAYERS = ("far", "middle", "close")
EXPECTED = {f"level1-{stage}-{layer}.png" for stage in STAGES for layer in LAYERS}


def main() -> int:
    found = {path.name for path in ASSETS.glob("level1-*.png")}
    if found != EXPECTED:
        print(f"FAIL: inventory differs: missing={sorted(EXPECTED - found)} extra={sorted(found - EXPECTED)}")
        return 1
    errors: list[str] = []
    for name in sorted(EXPECTED):
        path = ASSETS / name
        try:
            with Image.open(path) as source:
                if source.format != "PNG":
                    errors.append(f"{name}: not PNG")
                image = source.convert("RGBA")
        except OSError as error:
            errors.append(f"{name}: unreadable PNG ({error})")
            continue
        if image.size != (1320, 540):
            errors.append(f"{name}: expected 1320x540, got {image.size}")
        hist = image.getchannel("A").histogram()
        if sum(hist[1:255]):
            errors.append(f"{name}: contains partial-alpha pixels")
        if name.endswith("-far.png"):
            if hist[0]:
                errors.append(f"{name}: far plane is not fully opaque")
        elif hist[0] == 0 or hist[255] == 0:
            errors.append(f"{name}: moving plane lacks meaningful binary alpha")
        hot_magenta = sum(1 for red, green, blue, alpha in image.get_flattened_data() if alpha and red >= 240 and blue >= 230 and green <= 25 and abs(red - blue) <= 20)
        if hot_magenta:
            errors.append(f"{name}: contains {hot_magenta} opaque hot-magenta pixels")
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        return 1
    print("PASS: 15 Level 1 parallax PNGs; 1320x540; far opaque; moving planes binary-alpha; no hot-magenta matte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
