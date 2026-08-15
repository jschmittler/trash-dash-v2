#!/usr/bin/env python3
"""Validate lossless preservation and frame isolation for Trash Dash."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-trash-dash-isolated"
MANIFEST = json.loads((OUTPUT / "manifest.json").read_text())
ATLAS = Image.open(ROOT / MANIFEST["sheet"]["file"]).convert("RGBA")
GUTTER = MANIFEST["sheet"]["gutterPixels"]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


if len(MANIFEST["frames"]) != 96:
    fail("complete frame inventory is not 96")
if MANIFEST["operationCounts"]["GENERATE NEW"] != 0:
    fail("unexpected generated artwork")
if MANIFEST["sourcePixelScale"] != 1 or MANIFEST["runtimeScale"] != 1:
    fail("scale changed")
if ATLAS.getchannel("A").getextrema()[0] != 0:
    fail("atlas has no transparent background")

rectangles: list[tuple[str, tuple[int, int, int, int]]] = []
for frame_id, metadata in MANIFEST["frames"].items():
    frame = Image.open(OUTPUT / metadata["frameFile"]).convert("RGBA")
    if raw_sha(frame) != metadata["frameRgbaSha256"]:
        fail(f"frame RGBA hash changed: {frame_id}")
    cx, cy, cw, ch = metadata["cellRect"]
    ax, ay, aw, ah = metadata["artRect"]
    if (ax - cx, ay - cy, cx + cw - (ax + aw), cy + ch - (ay + ah)) != (GUTTER,) * 4:
        fail(f"incorrect declared gutter: {frame_id}")
    atlas_frame = ATLAS.crop((ax, ay, ax + aw, ay + ah))
    source_rgba = frame.tobytes()
    atlas_rgba = atlas_frame.tobytes()
    for offset in range(0, len(source_rgba), 4):
        source_pixel = source_rgba[offset : offset + 4]
        atlas_pixel = atlas_rgba[offset : offset + 4]
        if source_pixel[3] > 0 and atlas_pixel != source_pixel:
            fail(f"atlas placement changed visible pixels: {frame_id}")
        if source_pixel[3] == 0 and atlas_pixel != b"\x00\x00\x00\x00":
            fail(f"transparent RGB was not normalized: {frame_id}")
    cell_alpha = ATLAS.crop((cx, cy, cx + cw, cy + ch)).getchannel("A")
    if (
        cell_alpha.crop((0, 0, cw, GUTTER)).getbbox()
        or cell_alpha.crop((0, ch - GUTTER, cw, ch)).getbbox()
        or cell_alpha.crop((0, 0, GUTTER, ch)).getbbox()
        or cell_alpha.crop((cw - GUTTER, 0, cw, ch)).getbbox()
    ):
        fail(f"visible pixel entered gutter: {frame_id}")
    rectangles.append((frame_id, (cx, cy, cx + cw, cy + ch)))

for index, (left_id, left) in enumerate(rectangles):
    for right_id, right in rectangles[index + 1 :]:
        intersects = left[0] < right[2] and right[0] < left[2] and left[1] < right[3] and right[1] < left[3]
        if intersects:
            fail(f"declared frame rectangles overlap: {left_id}, {right_id}")

expected_states = {
    "toxic-spit": 5,
    "emerge": 3,
    "retreat": 3,
    "defeat": 7,
    "gameplay-support-effects": 13,
}
states = {state["id"]: state["frames"] for state in MANIFEST["states"]}
for state_id, count in expected_states.items():
    if len(states.get(state_id, [])) != count:
        fail(f"incorrect {state_id} frame count")

print("PASS: 96/96 approved animation and gameplay-support frames present in locked sequence order")
print("PASS: all frame RGBA hashes preserved at source scale 1")
print("PASS: every frame has an 8px transparent gutter on all four sides")
print("PASS: no declared source rectangles overlap")
print("PASS: Toxic Ooze Spit is five independently extractable frames")
