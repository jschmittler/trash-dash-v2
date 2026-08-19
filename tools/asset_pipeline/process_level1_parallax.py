#!/usr/bin/env python3
"""Normalize reviewed Level 1 parallax source masters into candidate plates.

This builder deliberately has no gameplay or renderer dependency.  Its only
job is to preserve the authored three-plane package at the locked 1320x540
candidate size and create static review evidence.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "assets/generated/level1-parallax"
SOURCES = BASE / "sources"
PROCESSED = BASE / "processed"
QA = BASE / "qa"
EVIDENCE = ROOT / "tools/visual-audit/evidence/level1-parallax"
TARGET = (1320, 540)
VIEW = (960, 540)
STAGES = (
    "deep-woodland",
    "creek-and-ruined-mill",
    "forest-edge-highway",
    "industrial-city-fringe",
    "urban-park-transition",
)
LAYERS = ("far", "middle", "close")
KEY = (255, 0, 255, 255)


def crop_far_to_runtime(image: Image.Image) -> Image.Image:
    """Center-crop an opaque far plate without changing its aspect ratio."""
    source = image.convert("RGBA")
    width, height = source.size
    target_aspect = TARGET[0] / TARGET[1]
    source_aspect = width / height
    if source_aspect > target_aspect:
        crop_width = round(height * target_aspect)
        left = (width - crop_width) // 2
        source = source.crop((left, 0, left + crop_width, height))
    else:
        crop_height = round(width / target_aspect)
        top = (height - crop_height) // 2
        source = source.crop((0, top, width, top + crop_height))
    result = source.resize(TARGET, Image.Resampling.NEAREST)
    result.putalpha(255)
    return result


def fit_moving_plate(image: Image.Image) -> Image.Image:
    """Fit complete moving-plane silhouettes on an opaque magenta key canvas."""
    source = image.convert("RGBA")
    width, height = source.size
    scale = min(TARGET[0] / width, TARGET[1] / height)
    resized = source.resize(
        (max(1, round(width * scale)), max(1, round(height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new("RGBA", TARGET, KEY)
    canvas.alpha_composite(
        resized,
        ((TARGET[0] - resized.width) // 2, (TARGET[1] - resized.height) // 2),
    )
    return canvas


def _is_key_candidate(pixel: tuple[int, int, int, int]) -> bool:
    red, green, blue, _alpha = pixel
    # The generator antialiases the key boundary into a broad pink/violet
    # fringe.  We remove that fringe only when flood-reachable from the
    # exterior key field; a similarly colored enclosed art detail is retained.
    return red >= 115 and blue >= 95 and green <= 155 and red - green >= 35 and blue - green >= 25


def remove_boundary_connected_magenta(image: Image.Image) -> Image.Image:
    """Remove only #FF00FF-like pixels connected to a canvas boundary.

    An enclosed purple object is retained even when it resembles the external
    key. This is intentionally stricter than a global color delete.
    """
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = list(rgba.get_flattened_data())
    removed = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def enqueue(x: int, y: int) -> None:
        index = y * width + x
        if not removed[index] and _is_key_candidate(pixels[index]):
            removed[index] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(1, height - 1):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= next_x < width and 0 <= next_y < height:
                enqueue(next_x, next_y)

    output: list[tuple[int, int, int, int]] = []
    for index, pixel in enumerate(pixels):
        red, green, blue, _alpha = pixel
        # The prompt reserves this high-chroma family exclusively for keying;
        # remove isolated generator key islands too. Ordinary low-saturation
        # violet shading remains below _is_key_candidate's threshold.
        if removed[index] or _is_key_candidate(pixel):
            output.append((0, 0, 0, 0))
        else:
            output.append((red, green, blue, 255))
    rgba.putdata(output)
    return rgba


def _checker() -> Image.Image:
    image = Image.new("RGB", VIEW, "#27313d")
    for y in range(0, VIEW[1], 24):
        for x in range(0, VIEW[0], 24):
            if (x // 24 + y // 24) % 2:
                Image.Image.paste(image, "#1b2430", (x, y, x + 24, y + 24))
    return image


def _viewport(image: Image.Image, offset: int = 180) -> Image.Image:
    return image.crop((offset, 0, offset + VIEW[0], VIEW[1]))


def _save_evidence(stage_images: dict[str, dict[str, Image.Image]]) -> None:
    for folder in ("composites", "seams", "sweeps", "transitions"):
        (QA / folder).mkdir(parents=True, exist_ok=True)
    composites: dict[str, Image.Image] = {}
    for stage, planes in stage_images.items():
        composite = planes["far"].copy()
        composite.alpha_composite(planes["middle"])
        composite.alpha_composite(planes["close"])
        composites[stage] = _viewport(composite)
        composites[stage].convert("RGB").save(QA / "composites" / f"{stage}-960x540.png")
        review = Image.new("RGB", (VIEW[0] * 3, VIEW[1] * 2 + 72), "#101820")
        draw = ImageDraw.Draw(review)
        for column, layer in enumerate(LAYERS):
            plate = _viewport(planes[layer])
            if layer != "far":
                checker = _checker().convert("RGBA")
                checker.alpha_composite(plate)
                plate = checker
            review.paste(plate.convert("RGB"), (column * VIEW[0], 32))
            draw.text((column * VIEW[0] + 16, 8), layer.upper(), fill="#f2e8cf")
        review.paste(composites[stage].convert("RGB"), (VIEW[0], VIEW[1] + 72))
        draw.text((VIEW[0] + 16, VIEW[1] + 48), "COMPOSITE 960×540", fill="#f2e8cf")
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        review.save(EVIDENCE / f"level1-{stage}-review.png")
        for layer, image in planes.items():
            seam = Image.new("RGBA", VIEW, (0, 0, 0, 0))
            seam.alpha_composite(image.crop((840, 0, 1320, 540)), (0, 0))
            seam.alpha_composite(image.crop((0, 0, 480, 540)), (480, 0))
            if layer != "far":
                checker = _checker().convert("RGBA")
                checker.alpha_composite(seam)
                seam = checker
            seam.convert("RGB").save(QA / "seams" / f"{stage}-{layer}-forced-wrap.png")
        sweep = Image.new("RGB", (VIEW[0] * 3, VIEW[1] * 2), "black")
        for row, offsets in enumerate(((0, 180, 360), (360, 180, 0))):
            for column, offset in enumerate(offsets):
                frame = _viewport(planes["far"], offset)
                frame.alpha_composite(_viewport(planes["middle"], min(360, round(offset * 0.055 / 0.018))))
                frame.alpha_composite(_viewport(planes["close"], min(360, round(offset * 0.13 / 0.018))))
                sweep.paste(frame.convert("RGB"), (column * VIEW[0], row * VIEW[1]))
        sweep.save(QA / "sweeps" / f"{stage}-forward-reverse.png")
    for start, end in zip(STAGES, STAGES[1:]):
        sheet = Image.new("RGB", (VIEW[0] * 5, VIEW[1]), "black")
        for index, t in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
            smooth = t * t * (3.0 - 2.0 * t)
            sheet.paste(Image.blend(composites[start], composites[end], smooth).convert("RGB"), (index * VIEW[0], 0))
        sheet.save(QA / "transitions" / f"{start}-to-{end}.png")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"target": list(TARGET), "plates": {}}
    stage_images: dict[str, dict[str, Image.Image]] = {}
    for stage in STAGES:
        stage_images[stage] = {}
        for layer in LAYERS:
            stem = f"level1-{stage}-{layer}"
            source = SOURCES / f"{stem}-source.png"
            if not source.is_file():
                raise FileNotFoundError(source)
            with Image.open(source) as master:
                result = crop_far_to_runtime(master) if layer == "far" else remove_boundary_connected_magenta(fit_moving_plate(master))
                output = PROCESSED / f"{stem}.png"
                result.save(output, optimize=False)
                alpha = result.getchannel("A").histogram()
                report["plates"][output.name] = {
                    "source": str(source.relative_to(ROOT)),
                    "sourceSize": list(master.size),
                    "runtimeSize": list(result.size),
                    "transparent": alpha[0],
                    "opaque": alpha[255],
                    "partialAlpha": sum(alpha[1:255]),
                }
                stage_images[stage][layer] = result
    _save_evidence(stage_images)
    (BASE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
