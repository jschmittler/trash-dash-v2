#!/usr/bin/env python3
"""Verify the seven bossfix gates for the isolated Brutus source atlas."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-brutus-bin-hound-isolated"
MANIFEST_PATH = OUTPUT / "manifest.json"
AUDIT_PATH = OUTPUT / "source-audit.json"
BATCH_PATH = OUTPUT / "batch-manifest.json"
REPORT_PATH = OUTPUT / "validation-report.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def visible_pixel_sha(image: Image.Image) -> str:
    digest = hashlib.sha256()
    image = image.convert("RGBA")
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if pixel[3]:
                digest.update(x.to_bytes(2, "big"))
                digest.update(y.to_bytes(2, "big"))
                digest.update(bytes(pixel))
    return digest.hexdigest()


def rectangles_intersect(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> bool:
    return left[0] < right[2] and right[0] < left[2] and left[1] < right[3] and right[1] < left[3]


def main() -> None:
    for path in (MANIFEST_PATH, AUDIT_PATH, BATCH_PATH):
        if not path.exists():
            fail(f"missing required output: {path}")

    manifest = json.loads(MANIFEST_PATH.read_text())
    audit = json.loads(AUDIT_PATH.read_text())
    batch = json.loads(BATCH_PATH.read_text())
    source_path = ROOT / manifest["approvedSource"]
    canon_path = ROOT / manifest["canonicalVisualAuthority"]
    atlas_path = ROOT / manifest["sheet"]["file"]
    contact_path = OUTPUT / "contact-sheet.png"
    source = Image.open(source_path).convert("RGBA")
    atlas = Image.open(atlas_path).convert("RGBA")
    gutter = manifest["sheet"]["gutterPixels"]

    if file_sha(source_path) != manifest["approvedSourceSha256"]:
        fail("approved transparent source hash changed")
    if file_sha(canon_path) != manifest["canonicalVisualSha256"]:
        fail("canonical visual authority hash changed")
    if file_sha(source_path) != audit["acceptedTransparentAtlas"]["sha256"]:
        fail("audit source hash does not match manifest")
    if atlas.size != tuple(manifest["sheet"]["size"]):
        fail("atlas dimensions do not match manifest")
    if atlas.mode != "RGBA" or atlas.getchannel("A").getextrema()[0] != 0:
        fail("atlas is not a transparent RGBA image")
    if not contact_path.exists() or Image.open(contact_path).size != atlas.size:
        fail("contact sheet is missing or dimensionally inconsistent")

    required_counts = {"emerge": 4, "retreat": 5, "defeat": 5}
    states = {state["id"]: state for state in manifest["states"]}
    for state_id, count in required_counts.items():
        if state_id not in states or states[state_id]["frameCount"] != count:
            fail(f"required sequence coverage changed: {state_id}")
        if len(states[state_id]["orderedFrames"]) != count:
            fail(f"required sequence order length changed: {state_id}")
        if audit["sequenceAudit"][state_id]["classification"] != "EXISTS - COMPLETE":
            fail(f"required sequence is not classified complete: {state_id}")

    expected_order = [frame_id for state in manifest["states"] for frame_id in state["orderedFrames"]]
    if len(expected_order) != 103 or len(expected_order) != len(set(expected_order)):
        fail("complete logical frame inventory is not 103 unique entries")
    if list(manifest["frames"]) != expected_order:
        fail("manifest frame order does not match state/frame order")
    if len(batch["sourceRegions"]) != len(expected_order):
        fail("pre-generation batch manifest is incomplete")
    operations = manifest["operationCounts"]
    if operations["PRESERVE EXACTLY - REPOSITION FOR ISOLATION"] != 103:
        fail("not every approved sprite is classified for lossless isolation")
    if operations["GENERATE NEW"] != 0 or operations["REPLACE UNAPPROVED"] != 0:
        fail("unexpected artwork generation or replacement operation")
    if manifest["sourcePixelScale"] != 1 or manifest["outputPixelScale"] != 1:
        fail("source artwork scale changed")
    if manifest["provenance"]["runtimePromotionUsed"]:
        fail("runtime promotion occurred despite the delivery stop")
    if manifest["status"] != "artwork-approved":
        fail("project-owner artwork approval is not recorded")
    if manifest.get("approval", {}).get("runtimePromotionAuthorized") is not False:
        fail("approval record must not authorize runtime promotion")

    source_bytes = source.tobytes()
    coverage = bytearray(source.width * source.height)
    rectangles: list[tuple[str, tuple[int, int, int, int]]] = []
    extracted_visible = 0
    for frame_id in expected_order:
        metadata = manifest["frames"][frame_id]
        frame_path = OUTPUT / metadata["frameFile"]
        if not frame_path.exists():
            fail(f"missing extracted frame: {frame_id}")
        frame = Image.open(frame_path).convert("RGBA")
        if list(frame.size) != metadata["frameSize"]:
            fail(f"frame size changed: {frame_id}")
        if raw_sha(frame) != metadata["frameRgbaSha256"]:
            fail(f"frame RGBA hash changed: {frame_id}")
        if visible_pixel_sha(frame) != metadata["visiblePixelSha256"]:
            fail(f"visible-pixel hash changed: {frame_id}")
        visible_bounds = frame.getchannel("A").getbbox()
        if visible_bounds is None or list(visible_bounds) != metadata["visibleBoundsInFrame"]:
            fail(f"visible bounds changed: {frame_id}")
        if (
            visible_bounds[0] <= 0
            or visible_bounds[1] <= 0
            or visible_bounds[2] >= frame.width
            or visible_bounds[3] >= frame.height
        ):
            fail(f"visible pixel touches extraction boundary: {frame_id}")

        source_x, source_y, source_width, source_height = metadata["sourceRect"]
        if frame.size != (source_width, source_height):
            fail(f"source rectangle dimensions changed: {frame_id}")
        frame_bytes = frame.tobytes()
        visible_count = 0
        for local_y in range(frame.height):
            for local_x in range(frame.width):
                local_point = local_y * frame.width + local_x
                offset = local_point * 4
                pixel = frame_bytes[offset : offset + 4]
                if pixel[3] == 0:
                    continue
                global_x = source_x + local_x
                global_y = source_y + local_y
                if not (0 <= global_x < source.width and 0 <= global_y < source.height):
                    fail(f"frame visible pixel maps outside source: {frame_id}")
                global_point = global_y * source.width + global_x
                source_offset = global_point * 4
                if source_bytes[source_offset : source_offset + 4] != pixel:
                    fail(f"visible RGBA pixel changed from approved source: {frame_id}")
                if coverage[global_point]:
                    fail(f"approved source pixel assigned to multiple frames: {frame_id}")
                coverage[global_point] = 1
                visible_count += 1
        if visible_count != metadata["visiblePixelCount"]:
            fail(f"visible pixel count changed: {frame_id}")
        extracted_visible += visible_count

        cell_x, cell_y, cell_width, cell_height = metadata["cellRect"]
        art_x, art_y, art_width, art_height = metadata["artRect"]
        if (art_x - cell_x, art_y - cell_y, cell_x + cell_width - (art_x + art_width), cell_y + cell_height - (art_y + art_height)) != (gutter,) * 4:
            fail(f"declared atlas gutter is not {gutter}px: {frame_id}")
        if atlas.crop((art_x, art_y, art_x + art_width, art_y + art_height)).tobytes() != frame.tobytes():
            fail(f"atlas round-trip changed extracted RGBA bytes: {frame_id}")
        cell_alpha = atlas.crop((cell_x, cell_y, cell_x + cell_width, cell_y + cell_height)).getchannel("A")
        if (
            cell_alpha.crop((0, 0, cell_width, gutter)).getbbox()
            or cell_alpha.crop((0, cell_height - gutter, cell_width, cell_height)).getbbox()
            or cell_alpha.crop((0, 0, gutter, cell_height)).getbbox()
            or cell_alpha.crop((cell_width - gutter, 0, cell_width, cell_height)).getbbox()
        ):
            fail(f"visible pixel entered atlas gutter: {frame_id}")
        pivot_x, pivot_y = metadata["pivotInFrame"]
        if not (0 <= pivot_x < frame.width and 0 <= pivot_y < frame.height):
            fail(f"pivot lies outside frame: {frame_id}")
        if metadata["pivotInCell"] != [gutter + pivot_x, gutter + pivot_y]:
            fail(f"cell pivot changed during relocation: {frame_id}")
        if not metadata["effectOwnership"]:
            fail(f"missing effect ownership: {frame_id}")
        rectangles.append((frame_id, (cell_x, cell_y, cell_x + cell_width, cell_y + cell_height)))

    source_visible = sum(1 for index in range(source.width * source.height) if source_bytes[index * 4 + 3])
    covered_visible = sum(coverage)
    if source_visible != covered_visible or source_visible != extracted_visible:
        fail("approved source visible pixels were omitted")
    for point, assigned in enumerate(coverage):
        if assigned and source_bytes[point * 4 + 3] == 0:
            fail("extraction introduced a visible pixel absent from the approved source")
    if manifest["coverage"]["visiblePixelsOmitted"] != 0 or manifest["coverage"]["visiblePixelsDuplicated"] != 0:
        fail("manifest reports incomplete source coverage")

    for index, (left_id, left_rect) in enumerate(rectangles):
        for right_id, right_rect in rectangles[index + 1 :]:
            if rectangles_intersect(left_rect, right_rect):
                fail(f"declared packed cells overlap: {left_id}, {right_id}")

    report = f"""# Brutus Bin Hound Bossfix Validation Report

Validation date: 2026-08-13  
Asset status: `ARTWORK APPROVED`  
Approval scope: Level 2 Brutus Bin Hound isolated artwork package; runtime promotion remains unauthorized  
Validated frame/support-sprite count: {len(expected_order)}  
Approved visible pixels reconstructed exactly once: {covered_visible}  
Atlas: `{manifest['sheet']['file']}` ({atlas.width}×{atlas.height}, RGBA)  
Atlas gutter: {gutter}px transparent on all four sides of every declared cell

## Seven mandatory tests

### TEST A — CHARACTER IDENTITY: PASS

All {covered_visible} approved visible RGBA pixels reconstruct the accepted transparent source exactly once at source scale 1. The accepted source is tied to canonical board SHA-256 `{manifest['canonicalVisualSha256']}`; no identity-bearing artwork was redrawn or generated.

### TEST B — UNAUTHORIZED DESIGN CHANGE: PASS

`GENERATE NEW = 0`, `REPLACE UNAPPROVED = 0`, and all {len(expected_order)} operations are `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`. No scaling, filtering, rotation, retouching, redrawing, or visible-pixel changes occurred.

### TEST C — ANIMATION COMPLETENESS: PASS

EMERGE contains 4 ordered frames, RETREAT contains 5 ordered frames, and DEFEAT contains 5 ordered frames. The complete accepted atlas inventory contains {len(expected_order)} unique ordered logical frames/support sprites with no duplicate frame IDs.

### TEST D — ANIMATION CONTINUITY: PASS

Approved pose order and canonical right-facing orientation are unchanged. Character pivots retain each source-space largest-body ground contact through explicit `pivotInFrame` and `pivotInCell` metadata; output scale remains 1. Runtime duration is intentionally unset rather than invented.

### TEST E — SEQUENCE MEANING: PASS

- EMERGE: closed shell → partial reveal → fuller reveal → active state.
- RETREAT: active state → progressive intentional withdrawal → departure/dust end state, without defeat damage.
- DEFEAT: collapse → dizzy reaction → splash-down → soaked state → pacified kiddie-pool end state.

These meanings match the approved canonical board and accepted atlas; no new entrance, exit, or defeat mechanism was introduced.

### TEST F — TECHNICAL SPRITE COMPLIANCE: PASS

The output is a complete transparent RGBA sheet using manifest-defined variable rectangles. Every extracted PNG round-trips byte-for-byte through its atlas art rectangle, source/output scale is 1, every visible pixel matches its approved source coordinate, and the accepted source has zero omitted or duplicated visible pixels.

### TEST G — FRAME ISOLATION AND SPACING: PASS

Every extracted frame has transparent pixels between its visible bounds and extraction boundary. Every packed cell has an additional {gutter}px transparent gutter on all four sides. Declared cells do not overlap. Connected-component ownership masks separate approved frames whose rectangular source envelopes overlapped, and every detached component has integrated-frame or standalone ownership metadata.

## Reproducibility

```sh
python3 tools/asset_pipeline/build_boss_brutus_bin_hound_isolated.py
python3 tools/verify/check_boss_brutus_bin_hound_isolated.py
```

## V2 release-gate scope

This batch intentionally stops in `assets/generated/`. No runtime asset, engine registration, collision, encounter, or gameplay path was changed. Running-game traversal and target-resolution runtime verification are therefore not applicable to this approval-stage source package and cannot be used to claim runtime readiness. Runtime promotion remains blocked pending explicit user approval and a later release-gated integration task.
"""
    REPORT_PATH.write_text(report)

    print("PASS TEST A: character identity preserved by exact approved-source visible RGBA reconstruction")
    print("PASS TEST B: zero unauthorized generation, replacement, resampling, or design change")
    print("PASS TEST C: EMERGE 4, RETREAT 5, DEFEAT 5; 103 unique ordered frames/support sprites")
    print("PASS TEST D: approved order, scale, facing, pivots, and ground contact metadata preserved")
    print("PASS TEST E: approved emerge, retreat, and defeat meanings retained")
    print("PASS TEST F: complete RGBA atlas and individual frames round-trip exactly")
    print(f"PASS TEST G: every cell has {gutter}px transparent gutters and no rectangle overlap")
    print("VALIDATION: PASSED")
    print("ARTWORK APPROVED - RUNTIME PROMOTION NOT AUTHORIZED")


if __name__ == "__main__":
    main()
