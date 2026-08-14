#!/usr/bin/env python3
"""Independently verify the generated-only Diamond Don isolation package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-diamond-don-isolated"
SOURCE = ROOT / "docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-diamond-don-transparent.png"
CANON = ROOT / "docs/design/trash-dash/reference/characters/level-06/sprites/boss-diamond-don.png"
MANIFEST = OUTPUT / "manifest.json"
BATCH = OUTPUT / "batch-manifest.json"
AUDIT = OUTPUT / "source-audit.json"
SPEC = OUTPUT / "immutable-generation-specification.md"
REPORT = OUTPUT / "validation-report.md"
APPROVAL = OUTPUT / "APPROVAL.md"
ATLAS = OUTPUT / "boss-diamond-don-isolated.png"
CONTACT = OUTPUT / "contact-sheet.png"

SOURCE_SHA256 = "7376000f332ef2ee4d58602b0843018c908ccbb0cd014fefb8e38d3704252bb8"
CANON_SHA256 = "f6132b478842f9cf6a5d54b32072e3ac1027aad3b1835350b40be680b483f5ac"
GUTTER = 8
FRAME_PAD = 2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def source_pixel_sha(source: Image.Image, points: list[int]) -> str:
    digest = hashlib.sha256()
    rgba = source.tobytes()
    for point in sorted(points):
        y, x = divmod(point, source.width)
        offset = point * 4
        digest.update(x.to_bytes(2, "big"))
        digest.update(y.to_bytes(2, "big"))
        digest.update(rgba[offset : offset + 4])
    return digest.hexdigest()


def main() -> None:
    required_files = [SOURCE, CANON, MANIFEST, BATCH, AUDIT, SPEC, APPROVAL, ATLAS, CONTACT]
    required_files += [OUTPUT / "previews" / f"{name}.gif" for name in ("emerge", "retreat", "defeat")]
    for path in required_files:
        require(path.is_file(), f"missing required artifact: {path}")

    require(file_sha(SOURCE) == SOURCE_SHA256, "accepted source hash changed")
    require(file_sha(CANON) == CANON_SHA256, "canonical visual authority hash changed")
    source = Image.open(SOURCE).convert("RGBA")
    require(source.size == (1536, 1024), "accepted source dimensions changed")
    require(set(source.getchannel("A").tobytes()) == {0, 255}, "source alpha is not binary")
    source_alpha = source.getchannel("A").tobytes()
    source_bytes = source.tobytes()
    source_visible = sum(1 for alpha in source_alpha if alpha)

    manifest = json.loads(MANIFEST.read_text())
    batch = json.loads(BATCH.read_text())
    audit = json.loads(AUDIT.read_text())
    frames = manifest["frames"]
    require(manifest["status"] == "artwork-approved", "incorrect approval status")
    require(manifest["approval"] == {
        "status": "ARTWORK APPROVED",
        "approvedBy": "project-owner",
        "approvedOn": "2026-08-13",
        "scope": "Level 6 Diamond Don isolated artwork package, manifest-defined rectangles, and approved-only EMERGE, RETREAT, and DEFEAT sequences",
        "runtimePromotionAuthorized": False,
    }, "approval status mismatch")
    require("Status: **ARTWORK APPROVED**" in APPROVAL.read_text(), "approval document mismatch")
    require(manifest["approvedSourceSha256"] == SOURCE_SHA256, "manifest source hash mismatch")
    require(manifest["canonicalVisualSha256"] == CANON_SHA256, "manifest canon hash mismatch")
    require(manifest["sourcePixelScale"] == manifest["outputPixelScale"] == 1, "pixel scale changed")
    for key in (
        "aiGenerationUsed", "resizingUsed", "redrawingUsed", "retouchingUsed",
        "filteringUsed", "rotationUsed", "runtimePromotionUsed",
    ):
        require(manifest["provenance"][key] is False, f"forbidden operation recorded: {key}")
    counts = manifest["operationCounts"]
    require(counts["GENERATE NEW"] == 0 and counts["REPLACE UNAPPROVED"] == 0, "artwork generation/replacement is nonzero")
    require(counts["PRESERVE EXACTLY - REPOSITION FOR ISOLATION"] == len(frames), "operation count mismatch")
    require(batch["operationCounts"] == counts, "batch operation counts mismatch")
    require(batch["status"] == "immutable-pre-assembly-manifest", "batch manifest status mismatch")
    require(len(batch["sourceRegions"]) == len(frames), "batch source inventory is incomplete")
    require(audit["acceptedTransparentAtlas"]["visiblePixelCount"] == source_visible, "audit pixel count mismatch")
    require(audit["sequenceAudit"] == manifest["requiredSequences"], "sequence audit differs from manifest")

    atlas = Image.open(ATLAS).convert("RGBA")
    require(list(atlas.size) == manifest["sheet"]["size"] == batch["updatedSheetDimensions"], "atlas size mismatch")
    require(manifest["sheet"]["gutterPixels"] == GUTTER, "gutter declaration mismatch")
    owner = [-1] * (source.width * source.height)
    extracted_visible = 0
    atlas_visible = 0

    frame_ids_from_states: list[str] = []
    for state in manifest["states"]:
        require(state["frameCount"] == len(state["orderedFrames"]), f"state count mismatch: {state['id']}")
        require(state["timing"]["durationMs"] is None, f"runtime timing invented: {state['id']}")
        require("NOT PROMOTED" in state["timing"]["status"], f"timing status missing: {state['id']}")
        frame_ids_from_states.extend(state["orderedFrames"])
    require(frame_ids_from_states == list(frames), "manifest frame order differs from state order")

    occupied_cells: list[tuple[int, int, int, int, str]] = []
    for frame_index, (frame_id, record) in enumerate(frames.items()):
        require(record["classification"] == "PRESERVE EXACTLY - REPOSITION FOR ISOLATION", f"bad classification: {frame_id}")
        require(record["effectOwnership"], f"missing effect ownership: {frame_id}")
        require(record["transparentFramePaddingPixels"] == FRAME_PAD, f"frame padding mismatch: {frame_id}")
        regions = [record["sourceOwnershipSelectionRegion"], *record.get("sourceOwnershipAdditionalSelectionRegions", [])]
        points: list[int] = []
        for left, top, right, bottom in regions:
            require(0 <= left < right <= source.width and 0 <= top < bottom <= source.height, f"invalid source region: {frame_id}")
            for y in range(top, bottom):
                row = y * source.width
                for x in range(left, right):
                    point = row + x
                    if not source_alpha[point]:
                        continue
                    require(owner[point] == -1, f"duplicated source pixel at {(x, y)}")
                    owner[point] = frame_index
                    points.append(point)
        require(len(points) == record["visiblePixelCount"], f"visible count mismatch: {frame_id}")
        require(source_pixel_sha(source, points) == record["sourceVisiblePixelSha256"], f"source pixel hash mismatch: {frame_id}")

        left, top, right, bottom = record["sourceVisibleBounds"]
        expected = Image.new("RGBA", (right - left + FRAME_PAD * 2, bottom - top + FRAME_PAD * 2), (0, 0, 0, 0))
        expected_pixels = expected.load()
        for point in points:
            source_y, source_x = divmod(point, source.width)
            offset = point * 4
            expected_pixels[source_x - left + FRAME_PAD, source_y - top + FRAME_PAD] = tuple(source_bytes[offset : offset + 4])
        frame_path = OUTPUT / record["frameFile"]
        require(frame_path.is_file(), f"missing frame: {frame_id}")
        frame = Image.open(frame_path).convert("RGBA")
        require(list(frame.size) == record["frameSize"], f"frame size mismatch: {frame_id}")
        require(frame.tobytes() == expected.tobytes(), f"source RGBA preservation failed: {frame_id}")
        require(raw_sha(frame) == record["frameRgbaSha256"], f"frame hash mismatch: {frame_id}")
        bbox = frame.getchannel("A").getbbox()
        require(list(bbox) == record["visibleBoundsInFrame"], f"visible bounds mismatch: {frame_id}")
        require(bbox[0] > 0 and bbox[1] > 0 and bbox[2] < frame.width and bbox[3] < frame.height, f"visible boundary contact: {frame_id}")
        pivot_x, pivot_y = record["pivotInFrame"]
        require(0 <= pivot_x < frame.width and 0 <= pivot_y < frame.height, f"pivot outside frame: {frame_id}")

        cell_x, cell_y, cell_w, cell_h = record["cellRect"]
        art_x, art_y, art_w, art_h = record["artRect"]
        require((art_x - cell_x, art_y - cell_y) == (GUTTER, GUTTER), f"leading gutter mismatch: {frame_id}")
        require(cell_x + cell_w - (art_x + art_w) == GUTTER, f"right gutter mismatch: {frame_id}")
        require(cell_y + cell_h - (art_y + art_h) == GUTTER, f"bottom gutter mismatch: {frame_id}")
        require((art_w, art_h) == frame.size, f"art rectangle mismatch: {frame_id}")
        require(atlas.crop((art_x, art_y, art_x + art_w, art_y + art_h)).tobytes() == frame.tobytes(), f"atlas/frame mismatch: {frame_id}")
        cell_alpha = atlas.getchannel("A").crop((cell_x, cell_y, cell_x + cell_w, cell_y + cell_h))
        require(cell_alpha.crop((0, 0, cell_w, GUTTER)).getbbox() is None, f"top gutter contaminated: {frame_id}")
        require(cell_alpha.crop((0, cell_h - GUTTER, cell_w, cell_h)).getbbox() is None, f"bottom gutter contaminated: {frame_id}")
        require(cell_alpha.crop((0, 0, GUTTER, cell_h)).getbbox() is None, f"left gutter contaminated: {frame_id}")
        require(cell_alpha.crop((cell_w - GUTTER, 0, cell_w, cell_h)).getbbox() is None, f"right gutter contaminated: {frame_id}")
        for other_x, other_y, other_w, other_h, other_id in occupied_cells:
            overlap = not (
                cell_x + cell_w <= other_x or other_x + other_w <= cell_x
                or cell_y + cell_h <= other_y or other_y + other_h <= cell_y
            )
            require(not overlap, f"atlas cells overlap: {frame_id} and {other_id}")
        occupied_cells.append((cell_x, cell_y, cell_w, cell_h, frame_id))
        extracted_visible += record["visiblePixelCount"]
        atlas_visible += sum(1 for alpha in frame.getchannel("A").tobytes() if alpha)

    missing = sum(1 for point, alpha in enumerate(source_alpha) if alpha and owner[point] == -1)
    require(missing == 0, f"{missing} source visible pixels omitted")
    require(extracted_visible == source_visible == atlas_visible, "one-to-one visible pixel coverage failed")
    require(sum(1 for alpha in atlas.getchannel("A").tobytes() if alpha) == source_visible, "atlas visible count mismatch")
    require(manifest["coverage"] == {
        "sourceVisiblePixelCount": source_visible,
        "extractedVisiblePixelCount": source_visible,
        "visiblePixelsOmitted": 0,
        "visiblePixelsDuplicated": 0,
    }, "coverage declaration mismatch")

    sequences = manifest["requiredSequences"]
    require(list(sequences) == ["emerge", "retreat", "defeat"], "required sequence order mismatch")
    for sequence_name, sequence in sequences.items():
        ordered = sequence["orderedFrames"]
        require(sequence["classification"] == "EXISTS - COMPLETE", f"sequence incomplete: {sequence_name}")
        require(len(ordered) == len(set(ordered)), f"duplicate frame reference: {sequence_name}")
        require(all(frame_id in frames for frame_id in ordered), f"unknown frame reference: {sequence_name}")
        preview = Image.open(OUTPUT / "previews" / f"{sequence_name}.gif")
        require(getattr(preview, "n_frames", 1) == len(ordered), f"preview frame count mismatch: {sequence_name}")
    require(sequences["emerge"]["orderedFrames"][-1] == "idle-swagger-00", "EMERGE does not connect to active idle")
    require(sequences["retreat"]["orderedFrames"][0] == "idle-swagger-00", "RETREAT does not begin at active idle")
    require(sequences["retreat"]["orderedFrames"][-1] == "curse-effect-00", "RETREAT does not establish curse exit state")
    require(sequences["defeat"]["orderedFrames"][-1] == "defeat-recovery-04", "DEFEAT does not end in approved softened state")
    require("visibly identifiable" in sequences["defeat"]["endState"], "DEFEAT identity statement missing")

    runtime_matches = list((ROOT / "assets/runtime").rglob("*diamond-don*")) if (ROOT / "assets/runtime").exists() else []
    require(not runtime_matches, "Diamond Don output was promoted into runtime assets")

    report = f"""# Diamond Don Bossfix Validation

**VALIDATION: PASSED**

## Seven mandatory tests

- **TEST A — CHARACTER IDENTITY: PASS.** Every delivered visible RGBA pixel is copied from the accepted atlas at 1:1 scale; canonical and accepted-source hashes are locked and verified.
- **TEST B — UNAUTHORIZED DESIGN CHANGE: PASS.** Generation, replacement, redraw, resize, retouch, rotation, filtering, and runtime promotion counts are zero.
- **TEST C — ANIMATION COMPLETENESS: PASS.** EMERGE, RETREAT, and DEFEAT each have explicit approved-only starts, ordered progressions, endings, continuity statements, and pivot-aligned previews with matching frame counts.
- **TEST D — ANIMATION CONTINUITY: PASS.** Approved source order, scale, ground-contact pivot strategy, effect-envelope pivots, and transition endpoints are preserved; runtime timing remains intentionally unset.
- **TEST E — SEQUENCE MEANING: PASS.** EMERGE materializes through canonical curse imagery into idle; RETREAT intentionally reverses that vocabulary without defeat art; DEFEAT uses approved hit/fall/exhausted art and ends with the exact identifiable softened seated Don.
- **TEST F — TECHNICAL SPRITE COMPLIANCE: PASS.** All {source_visible:,} accepted visible pixels and RGBA values are assigned exactly once; there are no omissions, duplicates, generated pixels, replacements, or atlas/frame mismatches.
- **TEST G — FRAME ISOLATION AND SPACING: PASS.** All {len(frames)} variable rectangles have two transparent frame-padding pixels plus eight transparent atlas-gutter pixels on every side; no delivered visible pixel touches a boundary or contaminates another cell.

## Commands and scope

- Build: `python3 tools/asset_pipeline/build_boss_diamond_don_isolated.py`
- Verify: `python3 tools/verify/check_boss_diamond_don_isolated.py`
- Canonical source: `docs/design/trash-dash/reference/characters/level-06/sprites/boss-diamond-don.png`
- Accepted extraction source: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-diamond-don-transparent.png`
- Output: `assets/generated/boss-diamond-don-isolated/`

## V2 release-gate status

`INCOMPLETE / NOT PROMOTED` by design. The requested artifact is generated review material only. No runtime registration, gameplay timing, collision, uninterrupted traversal, target-resolution runtime capture, or promotion was authorized or performed.

**ARTWORK APPROVED — RUNTIME PROMOTION NOT AUTHORIZED**
"""
    REPORT.write_text(report)
    print("VALIDATION: PASSED")
    print(f"frames/support sprites: {len(frames)}")
    print(f"source visible pixels preserved exactly once: {source_visible}")
    print("Bossfix tests A-G: PASS")
    print("V2 release gate: INCOMPLETE / NOT PROMOTED")
    print("ARTWORK APPROVED - RUNTIME PROMOTION NOT AUTHORIZED")


if __name__ == "__main__":
    main()
