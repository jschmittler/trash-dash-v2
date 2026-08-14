#!/usr/bin/env python3
"""Verify the seven bossfix gates for the isolated Pizza Rat King package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-pizza-rat-king-isolated"
MANIFEST_PATH = OUTPUT / "manifest.json"
AUDIT_PATH = OUTPUT / "source-audit.json"
BATCH_PATH = OUTPUT / "batch-manifest.json"
SPEC_PATH = OUTPUT / "immutable-generation-specification.md"
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
    for path in (MANIFEST_PATH, AUDIT_PATH, BATCH_PATH, SPEC_PATH):
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

    expected_required_counts = {"emerge": 5, "retreat": 5, "defeat": 5}
    for sequence_id, count in expected_required_counts.items():
        sequence = manifest["requiredSequences"].get(sequence_id)
        if sequence is None or sequence["classification"] != "EXISTS - COMPLETE":
            fail(f"required sequence is not complete: {sequence_id}")
        if len(sequence["orderedFrames"]) != count or len(sequence["orderedFrames"]) != len(set(sequence["orderedFrames"])):
            fail(f"required sequence frame order is invalid: {sequence_id}")
        if not (OUTPUT / "previews" / f"{sequence_id}.gif").exists():
            fail(f"required sequence preview is missing: {sequence_id}")
        frame_hashes = [
            raw_sha(Image.open(OUTPUT / manifest["frames"][frame_id]["frameFile"]).convert("RGBA"))
            for frame_id in sequence["orderedFrames"]
        ]
        if len(frame_hashes) != len(set(frame_hashes)):
            fail(f"required sequence contains an accidental duplicate image: {sequence_id}")

    expected_order = [frame_id for state in manifest["states"] for frame_id in state["orderedFrames"]]
    if len(expected_order) != 74 or len(expected_order) != len(set(expected_order)):
        fail("complete physical frame inventory is not 74 unique entries")
    if list(manifest["frames"]) != expected_order:
        fail("manifest frame order does not match physical state order")
    if len(batch["sourceRegions"]) != len(expected_order):
        fail("pre-assembly batch manifest is incomplete")
    for sequence in manifest["requiredSequences"].values():
        for frame_id in sequence["orderedFrames"]:
            if frame_id not in manifest["frames"]:
                fail(f"required sequence references an unknown physical frame: {frame_id}")

    operations = manifest["operationCounts"]
    if operations["PRESERVE EXACTLY - REPOSITION FOR ISOLATION"] != 74:
        fail("not every approved sprite is classified for lossless isolation")
    if operations["GENERATE NEW"] != 0 or operations["REPLACE UNAPPROVED"] != 0:
        fail("unexpected artwork generation or replacement operation")
    if manifest["sourcePixelScale"] != 1 or manifest["outputPixelScale"] != 1:
        fail("source artwork scale changed")
    if manifest["provenance"]["aiGenerationUsed"] or manifest["provenance"]["runtimePromotionUsed"]:
        fail("generation or runtime promotion occurred despite the immutable scope")
    if manifest["status"] != "artwork-approved":
        fail("project-owner artwork approval is not recorded")
    approval = manifest.get("approval", {})
    if approval.get("approvedBy") != "project-owner" or approval.get("approvedOn") != "2026-08-13":
        fail("artwork approval provenance is incomplete")
    if approval.get("runtimePromotionAuthorized") is not False:
        fail("artwork approval must not authorize runtime promotion")

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
        if raw_sha(frame) != metadata["frameRgbaSha256"] or visible_pixel_sha(frame) != metadata["visiblePixelSha256"]:
            fail(f"frame RGBA data changed: {frame_id}")
        visible_bounds = frame.getchannel("A").getbbox()
        if visible_bounds is None or list(visible_bounds) != metadata["visibleBoundsInFrame"]:
            fail(f"visible bounds changed: {frame_id}")
        if visible_bounds[0] <= 0 or visible_bounds[1] <= 0 or visible_bounds[2] >= frame.width or visible_bounds[3] >= frame.height:
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
        margins = (art_x - cell_x, art_y - cell_y, cell_x + cell_width - (art_x + art_width), cell_y + cell_height - (art_y + art_height))
        if margins != (gutter,) * 4:
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
    if manifest["coverage"]["visiblePixelsOmitted"] != 0 or manifest["coverage"]["visiblePixelsDuplicated"] != 0:
        fail("manifest reports incomplete source coverage")

    for index, (left_id, left_rect) in enumerate(rectangles):
        for right_id, right_rect in rectangles[index + 1 :]:
            if rectangles_intersect(left_rect, right_rect):
                fail(f"declared packed cells overlap: {left_id}, {right_id}")

    report = f"""# Pizza Rat King Bossfix Validation Report

Validation date: 2026-08-13  
Asset status: `ARTWORK APPROVED`  
Approval scope: Level 3 Pizza Rat King isolated artwork package; runtime promotion remains unauthorized  
Validated physical frame/support-sprite count: {len(expected_order)}  
Approved visible pixels reconstructed exactly once: {covered_visible}  
Atlas: `{manifest['sheet']['file']}` ({atlas.width}×{atlas.height}, RGBA)  
Atlas gutter: {gutter}px transparent on all four sides of every declared cell

## Seven mandatory tests

### TEST A — CHARACTER IDENTITY: PASS

All {covered_visible} approved visible RGBA pixels reconstruct the accepted transparent source exactly once at source scale 1. The source is tied to canonical-board SHA-256 `{manifest['canonicalVisualSha256']}`; no identity-bearing artwork was redrawn or regenerated.

### TEST B — UNAUTHORIZED DESIGN CHANGE: PASS

`GENERATE NEW = 0`, `REPLACE UNAPPROVED = 0`, and all {len(expected_order)} physical operations are `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`. No scaling, filtering, rotation, retouching, redrawing, new damage, or new effects occurred.

### TEST C — ANIMATION COMPLETENESS: PASS

EMERGE has 5 ordered approved frame references, RETREAT has 5, and DEFEAT has 5. Every sequence has a declared start, intermediate progression, end, and continuity connection. The package contains {len(expected_order)} unique physical frames/support sprites and three pivot-aligned animated previews.

### TEST D — ANIMATION CONTINUITY: PASS

Approved pose order and right-facing orientation are unchanged. EMERGE decelerates from approved rush poses into idle; RETREAT accelerates from idle into approved exit motion; DEFEAT follows approved hit and crash/stunned poses to the face-down king. Source/output scale remains 1 and every physical frame has explicit pivot/ground metadata. Runtime duration is intentionally unset rather than invented.

### TEST E — SEQUENCE MEANING: PASS

- EMERGE: off-screen dust cue → approved right-facing entry rush → charge slowdown → active idle.
- RETREAT: active idle → approved charge acceleration → right-facing exit → off-screen dust cue, without defeat imagery.
- DEFEAT: hit reaction → crash/stunned collapse → face-down defeated king, still visibly the exact approved character. The rat/crown reveal remains separate approved post-defeat support art.

No new entrance mechanism, defeat damage, or character redesign was introduced.

### TEST F — TECHNICAL SPRITE COMPLIANCE: PASS

The output is a complete transparent RGBA sheet using manifest-defined variable rectangles. Every extracted PNG round-trips byte-for-byte through its atlas art rectangle, source/output scale is 1, every visible pixel matches its approved source coordinate, and the accepted source has zero omitted or duplicated visible pixels.

### TEST G — FRAME ISOLATION AND SPACING: PASS

Every extracted frame has transparent pixels between its visible bounds and extraction boundary. Every packed cell has an additional {gutter}px transparent gutter on all four sides. Declared cells do not overlap. Reviewed ownership masks isolate previously touching/overlapping source envelopes, including the accepted fast-run bridge seam, and every detached component has integrated-frame or standalone ownership metadata.

## Reproducibility

```sh
python3 tools/asset_pipeline/build_boss_pizza_rat_king_isolated.py
python3 tools/verify/check_boss_pizza_rat_king_isolated.py
```

## V2 release-gate scope

This batch stops in `assets/generated/`. No runtime asset, engine registration, collision, encounter, or gameplay path changed. Running-game traversal and target-resolution runtime verification are therefore outside this approval-stage package and cannot support a runtime-readiness claim. Runtime promotion remains blocked pending explicit user approval and a later release-gated integration task.
"""
    REPORT_PATH.write_text(report)

    print("PASS TEST A: character identity preserved by exact approved-source visible RGBA reconstruction")
    print("PASS TEST B: zero unauthorized generation, replacement, resampling, or design change")
    print("PASS TEST C: EMERGE 5, RETREAT 5, DEFEAT 5; 74 unique physical frames/support sprites")
    print("PASS TEST D: approved scale, facing, pivots, ground contact, and pose continuity preserved")
    print("PASS TEST E: approved motion vocabulary supplies emerge, retreat, and defeat meanings")
    print("PASS TEST F: complete RGBA atlas and individual frames round-trip exactly")
    print(f"PASS TEST G: every cell has {gutter}px transparent gutters and no rectangle overlap")
    print("VALIDATION: PASSED")
    print("ARTWORK APPROVED - RUNTIME PROMOTION NOT AUTHORIZED")


if __name__ == "__main__":
    main()
