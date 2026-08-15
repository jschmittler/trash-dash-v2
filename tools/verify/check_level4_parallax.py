#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import sys

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public/assets/backgrounds"
STAGES = [
    "hidden-service-entrance",
    "experimental-laboratory",
    "robotics-assembly-chamber",
    "zero-gravity-research-chamber",
    "rocket-hangar-finale",
]
LAYERS = ["far", "middle", "close"]
EXPECTED = {f"level4-{s}-{layer}.png" for s in STAGES for layer in LAYERS}


def fail(message):
    print(f"FAIL: {message}")
    return 1


def main():
    found = {p.name for p in PUBLIC.glob("level4-*.png")}
    if found != EXPECTED:
        return fail(f"runtime inventory differs: missing={sorted(EXPECTED-found)} extra={sorted(found-EXPECTED)}")
    for name in sorted(EXPECTED):
        image = Image.open(PUBLIC / name).convert("RGBA")
        if image.size != (1320, 540):
            return fail(f"{name} is {image.size}")
        hist = image.getchannel("A").histogram()
        partial = sum(hist[1:255])
        if partial:
            return fail(f"{name} contains {partial} partial-alpha pixels")
        if name.endswith("-far.png") and hist[0]:
            return fail(f"{name} contains {hist[0]} transparent pixels")
        if not name.endswith("-far.png") and (hist[0] == 0 or hist[255] == 0):
            return fail(f"{name} lacks meaningful object-shaped transparency")
        hot_magenta = 0
        for r, g, b, a in image.get_flattened_data():
            if a and r > 220 and b > 180 and g < 80:
                hot_magenta += 1
        if hot_magenta:
            return fail(f"{name} contains {hot_magenta} opaque hot-magenta pixels")
    print("PASS: 15 Level 4 parallax PNGs; 1320x540; far opaque; moving alpha binary and meaningful; no hot-magenta matte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
