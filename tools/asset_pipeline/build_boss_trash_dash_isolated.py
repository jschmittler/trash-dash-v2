#!/usr/bin/env python3
"""Losslessly repack the approved Trash Dash frames with safe gutters."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
HISTORY = Path("/private/tmp/trash-dash-history/assets/generated/boss-trash-dash")
EXPANSION = ROOT / "assets/generated/boss-trash-dash-expansion"
OUTPUT = ROOT / "assets/generated/boss-trash-dash-isolated"
FRAMES_OUT = OUTPUT / "frames"
ATLAS_OUT = OUTPUT / "boss-trash-dash-isolated.png"
PREVIEW_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
SOURCE = ROOT / "docs/design/trash-dash/library/characters/bosses/trash-dash/sprites/animation-source/boss-trash-dash-transparent.png"
CANON = ROOT / "docs/design/trash-dash/library/characters/bosses/trash-dash/sprites/reference/boss-trash-dash.png"
GUTTER = 8
MAX_WIDTH = 2048

SUPPORT_FRAME_SPECS = [
    ("ooze-spit-small-0", (24, 943, 69, 966), (22, 23)),
    ("ooze-spit-small-1", (74, 939, 118, 967), (22, 28)),
    ("ooze-spit-large-0", (161, 933, 225, 975), (32, 42)),
    ("ooze-spit-large-1", (220, 934, 293, 975), (36, 41)),
    ("ooze-splash-impact-0", (309, 914, 415, 983), (53, 69)),
    ("ooze-splash-impact-1", (415, 916, 525, 984), (55, 68)),
    ("slam-impact-0", (544, 911, 625, 983), (40, 72)),
    ("slam-impact-1", (625, 926, 715, 983), (45, 57)),
    ("dust-debris-0", (752, 930, 837, 982), (42, 52)),
    ("dust-debris-1", (855, 933, 930, 981), (37, 48)),
    ("tossed-trash-clump-0", (958, 944, 1036, 986), (39, 42)),
    ("tossed-trash-clump-1", (1051, 947, 1110, 985), (29, 38)),
    ("ooze-puddles-various", (1139, 958, 1206, 990), (33, 32)),
]


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_inputs() -> tuple[list[dict], dict, dict]:
    history_manifest = json.loads(
        (Path("/private/tmp/trash-dash-history/tools/asset-pipeline/manifests/boss-trash-dash.json")).read_text()
    )
    history_measurements = json.loads((HISTORY / "measurements.json").read_text())
    expansion_manifest = json.loads((EXPANSION / "manifest.json").read_text())
    ordered: list[dict] = []
    for state in history_manifest["animations"]["states"]:
        ordered.append({"id": state["id"], "frames": list(state["frames"]), "source": "approved-transparent-sheet"})
    for state_id in ("emerge", "retreat", "defeat"):
        ordered.append(
            {
                "id": state_id,
                "frames": list(expansion_manifest["states"][state_id]["orderedFrames"]),
                "source": "approved-canonical-board",
                "fps": expansion_manifest["states"][state_id]["fps"],
                "loop": expansion_manifest["states"][state_id]["loop"],
            }
        )
    ordered.append(
        {
            "id": "gameplay-support-effects",
            "frames": [frame_id for frame_id, _rect, _pivot in SUPPORT_FRAME_SPECS],
            "source": "approved-transparent-sheet",
            "loop": False,
        }
    )
    return ordered, history_measurements, expansion_manifest


def frame_source(frame_id: str, history_measurements: dict, expansion_manifest: dict) -> tuple[Path, dict]:
    if frame_id in history_measurements["frames"]:
        metadata = history_measurements["frames"][frame_id]
        return HISTORY / metadata["file"], {
            "logicalPivot": metadata["pivot"],
            "sourceRect": metadata["source_rect"],
            "sourceAuthority": "approved-transparent-sheet",
            "ownershipMask": history_measurements.get("ownership_masks", {}).get(frame_id),
        }
    metadata = expansion_manifest["frames"][frame_id]
    return ROOT / metadata["derivedCell"], {
        "logicalPivot": {"x": 64, "y": metadata["groundBaselineInCell"]},
        "sourceRect": {
            "x": metadata["canonicalSourceRect"][0],
            "y": metadata["canonicalSourceRect"][1],
            "w": metadata["canonicalSourceRect"][2],
            "h": metadata["canonicalSourceRect"][3],
        },
        "sourceAuthority": "approved-canonical-board",
        "ownershipMask": None,
    }


def extract_support_frames() -> dict[str, tuple[Image.Image, dict]]:
    source = Image.open(SOURCE).convert("RGBA")
    extracted: dict[str, tuple[Image.Image, dict]] = {}
    for frame_id, (left, top, right, bottom), pivot in SUPPORT_FRAME_SPECS:
        image = source.crop((left, top, right, bottom))
        extracted[frame_id] = (
            image,
            {
                "logicalPivot": {"x": pivot[0], "y": pivot[1]},
                "sourceRect": {"x": left, "y": top, "w": right - left, "h": bottom - top},
                "sourceAuthority": "approved-transparent-sheet",
                "ownershipMask": None,
            },
        )
    return extracted


def plan_rows(frames: list[tuple[str, Image.Image, dict]]) -> tuple[list[dict], tuple[int, int]]:
    placements: list[dict] = []
    x = 0
    y = 0
    row_height = 0
    for frame_id, image, metadata in frames:
        cell_w = image.width + GUTTER * 2
        cell_h = image.height + GUTTER * 2
        if x and x + cell_w > MAX_WIDTH:
            x = 0
            y += row_height
            row_height = 0
        placements.append(
            {
                "id": frame_id,
                "cellRect": [x, y, cell_w, cell_h],
                "artRect": [x + GUTTER, y + GUTTER, image.width, image.height],
                "logicalPivotInCell": [GUTTER + metadata["logicalPivot"]["x"], GUTTER + metadata["logicalPivot"]["y"]],
                **metadata,
            }
        )
        x += cell_w
        row_height = max(row_height, cell_h)
    return placements, (MAX_WIDTH, y + row_height)


def main() -> None:
    if Image.open(SOURCE).size != (1536, 1024):
        raise RuntimeError("approved transparent source dimensions changed")
    ordered_states, history_measurements, expansion_manifest = load_inputs()
    frame_ids = [frame_id for state in ordered_states for frame_id in state["frames"]]
    if len(frame_ids) != 96 or len(frame_ids) != len(set(frame_ids)):
        raise RuntimeError("immutable batch frame inventory is not 96 unique frames")
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)
    loaded: list[tuple[str, Image.Image, dict]] = []
    support_frames = extract_support_frames()
    for frame_id in frame_ids:
        destination = FRAMES_OUT / f"{frame_id}.png"
        if frame_id in support_frames:
            image, metadata = support_frames[frame_id]
            image.save(destination, format="PNG", compress_level=9, optimize=False)
        else:
            source_path, metadata = frame_source(frame_id, history_measurements, expansion_manifest)
            image = Image.open(source_path).convert("RGBA")
            shutil.copyfile(source_path, destination)
            if Image.open(destination).convert("RGBA").tobytes() != image.tobytes():
                raise RuntimeError(f"frame copy changed RGBA bytes: {frame_id}")
        loaded.append((frame_id, image, metadata))

    placements, atlas_size = plan_rows(loaded)
    atlas = Image.new("RGBA", atlas_size, (0, 0, 0, 0))
    by_id = {frame_id: image for frame_id, image, _metadata in loaded}
    for placement in placements:
        frame_id = placement["id"]
        image = by_id[frame_id]
        x, y, _w, _h = placement["artRect"]
        # Alpha-composite onto a zeroed transparent canvas. This preserves every
        # visible approved RGBA pixel while preventing source-board RGB hidden
        # beneath alpha 0 from appearing in alpha-ignorant inspection tools.
        atlas.alpha_composite(image, (x, y))
        placement["frameRgbaSha256"] = raw_sha(image)
        placement["frameFile"] = f"frames/{frame_id}.png"
        placement["visibleBoundsInFrame"] = list(image.getchannel("A").getbbox())
    atlas.save(ATLAS_OUT, format="PNG", compress_level=9, optimize=False)

    preview = Image.new("RGBA", atlas.size, (40, 43, 46, 255))
    preview.alpha_composite(atlas)
    draw = ImageDraw.Draw(preview)
    for placement in placements:
        x, y, w, h = placement["cellRect"]
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=(92, 98, 103, 255))
    preview.save(PREVIEW_OUT, format="PNG", compress_level=9, optimize=False)

    frame_records = {placement.pop("id"): placement for placement in placements}
    manifest = {
        "assetName": "boss-trash-dash-isolated",
        "canonId": "boss.level-01.trash-dash",
        "status": "generated-awaiting-user-approval",
        "approvedSource": str(SOURCE.relative_to(ROOT)),
        "approvedSourceSha256": file_sha(SOURCE),
        "canonicalVisualAuthority": str(CANON.relative_to(ROOT)),
        "canonicalVisualSha256": file_sha(CANON),
        "sheet": {
            "file": str(ATLAS_OUT.relative_to(ROOT)),
            "size": list(atlas.size),
            "mode": "RGBA",
            "background": "transparent",
            "layout": "manifest-defined-variable-rectangles",
            "gutterPixels": GUTTER,
            "readingOrder": "states then ordered frames",
        },
        "canonicalFacing": "right",
        "sourcePixelScale": 1,
        "runtimeScale": 1,
        "states": ordered_states,
        "frames": frame_records,
        "operationCounts": {
            "PRESERVE EXACTLY - REPOSITION FOR ISOLATION": len(frame_records),
            "GENERATE NEW": 0,
            "REPLACE UNAPPROVED": 0,
        },
        "provenance": {
            "method": "lossless RGBA frame relocation with reviewed ownership masks for contaminated toxic-spit regions",
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "redrawingUsed": False,
            "filteringUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_trash_dash_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(ATLAS_OUT)
    print(MANIFEST_OUT)


if __name__ == "__main__":
    main()
