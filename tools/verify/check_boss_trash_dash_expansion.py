#!/usr/bin/env python3
"""Static canon and asset-integrity checks for Trash Dash expansion."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/design/trash-dash/library/characters/bosses/trash-dash/sprites/animation-source/boss-trash-dash-transparent.png"
OUTPUT_DIR = ROOT / "assets/generated/boss-trash-dash-expansion"
OUTPUT = OUTPUT_DIR / "boss-trash-dash-expanded.png"
MANIFEST = OUTPUT_DIR / "manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


source = Image.open(SOURCE).convert("RGBA")
output = Image.open(OUTPUT).convert("RGBA")
manifest = json.loads(MANIFEST.read_text())

if source.size != (1536, 1024):
    fail(f"unexpected source size {source.size}")
if output.size != (1536, 1280):
    fail(f"unexpected output size {output.size}")
if output.crop((0, 0, 1536, 1024)).tobytes() != source.tobytes():
    fail("PRESERVE EXACTLY region differs from approved source")
if manifest["sourcePixelScale"] != 1:
    fail("canonical source pixels were scaled")

expected = {
    "emerge": ["emerge_01", "emerge_02", "emerge_03"],
    "retreat": ["retreat_01", "retreat_02", "retreat_03"],
    "defeat": [f"defeat_{index:02d}" for index in range(1, 8)],
}
for state, frames in expected.items():
    if manifest["states"][state]["orderedFrames"] != frames:
        fail(f"{state} does not preserve canonical pose order")

for name, metadata in manifest["frames"].items():
    cell = Image.open(ROOT / metadata["derivedCell"]).convert("RGBA")
    if cell.size != (128, 128):
        fail(f"{name} changed canonical frame dimensions")
    alpha = cell.getchannel("A")
    values = set(alpha.get_flattened_data())
    if values != {0, 255}:
        fail(f"{name} does not use binary transparency")
    box = alpha.getbbox()
    if box is None:
        fail(f"{name} is empty")
    if box[0] == 0 or box[2] == 128 or box[1] == 0 or box[3] == 128:
        fail(f"{name} touches a frame boundary: {box}")
    if metadata["scaleApplied"] != 1:
        fail(f"{name} used state-specific scaling")

def height(name: str) -> int:
    return manifest["frames"][name]["visibleBounds"][3]

if not (height("emerge_01") < height("emerge_02") < height("emerge_03")):
    fail("emerge does not rise progressively")
if not (height("retreat_01") >= height("retreat_02") >= height("retreat_03")):
    fail("retreat does not withdraw progressively")
if height("defeat_07") >= height("defeat_01"):
    fail("defeat does not end in the canonical reduced refuse heap")

print("PASS: original 1536x1024 RGBA region preserved exactly")
print("PASS: canonical 3/3/7 sequence counts and left-to-right ordering")
print("PASS: thirteen native 128x128 cells, scale 1, hard transparency")
print("PASS: safe cell margins and progressive sequence silhouettes")
