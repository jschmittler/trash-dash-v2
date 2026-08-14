#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import json
from collections import deque

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "assets/generated/level4-parallax"
SOURCES = BASE / "sources"
PROCESSED = BASE / "processed"
PUBLIC = ROOT / "public/assets/backgrounds"
QA = BASE / "qa"
SIZE = (1320, 540)
VIEW = (960, 540)

STAGES = [
    "hidden-service-entrance",
    "experimental-laboratory",
    "robotics-assembly-chamber",
    "zero-gravity-research-chamber",
    "rocket-hangar-finale",
]
LAYERS = ["far", "middle", "close"]


def center_crop_resize(image: Image.Image) -> Image.Image:
    sw, sh = image.size
    target_aspect = SIZE[0] / SIZE[1]
    source_aspect = sw / sh
    if source_aspect > target_aspect:
        crop_w = round(sh * target_aspect)
        left = (sw - crop_w) // 2
        image = image.crop((left, 0, left + crop_w, sh))
    else:
        crop_h = round(sw / target_aspect)
        top = (sh - crop_h) // 2
        image = image.crop((0, top, sw, top + crop_h))
    result = image.resize(SIZE, Image.Resampling.NEAREST)
    # Far plates must wrap without exposing a hard source boundary. Harmonize
    # the final edge columns with discrete nearest-neighbor pixels only; no
    # blur, gradient, antialiasing, or nonuniform scaling is introduced.
    for y in range(SIZE[1]):
        left = result.getpixel((0, y))
        right = result.getpixel((SIZE[0] - 1, y))
        seam_color = tuple((a + b) // 2 for a, b in zip(left, right))
        result.putpixel((0, y), seam_color)
        result.putpixel((SIZE[0] - 1, y), seam_color)
    return result


def fit_moving_plate(image: Image.Image) -> Image.Image:
    # Moving planes retain complete silhouettes. Aspect-preserving nearest-neighbor
    # fit is centered on the runtime canvas; chroma becomes transparent padding.
    sw, sh = image.size
    scale = min(SIZE[0] / sw, SIZE[1] / sh)
    nw, nh = max(1, round(sw * scale)), max(1, round(sh * scale))
    image = image.resize((nw, nh), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", SIZE, (255, 0, 255, 255))
    canvas.alpha_composite(image, ((SIZE[0] - nw) // 2, (SIZE[1] - nh) // 2))
    return canvas


def remove_magenta_binary(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = list(rgba.get_flattened_data())
    width, height = rgba.size
    # Flood only from the canvas boundary. The permissive fringe predicate can
    # therefore remove dark antialiased/key-matte pixels without deleting
    # isolated violet technology details inside retained objects.
    def is_strong_key(pixel):
        r, g, b, _ = pixel
        return r >= 175 and b >= 135 and g <= 145 and (r - g) >= 70 and (b - g) >= 45

    def is_fringe(pixel):
        r, g, b, _ = pixel
        return r >= 45 and b >= 45 and g <= 115 and (r - g) >= 28 and (b - g) >= 22

    removed = bytearray(width * height)
    queue = deque()
    for y in range(height):
        for x in range(width):
            i = y * width + x
            if is_strong_key(pixels[i]):
                removed[i] = 1
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                i = ny * width + nx
                if not removed[i] and is_fringe(pixels[i]):
                    removed[i] = 1
                    queue.append((nx, ny))
    out = []
    for i, (r, g, b, _) in enumerate(pixels):
        out.append((0, 0, 0, 0) if removed[i] else (r, g, b, 255))
    rgba.putdata(out)
    return rgba


def checker() -> Image.Image:
    img = Image.new("RGB", VIEW, "#18212d")
    draw = ImageDraw.Draw(img)
    step = 24
    for y in range(0, VIEW[1], step):
        for x in range(0, VIEW[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill="#243244")
    return img


def viewport(image: Image.Image, offset: int = 180) -> Image.Image:
    return image.crop((offset, 0, offset + VIEW[0], VIEW[1]))


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for folder in [QA / "composites", QA / "seams", QA / "transitions", QA / "sweeps"]:
        folder.mkdir(parents=True, exist_ok=True)

    report = {"size": list(SIZE), "plates": {}}
    stage_images = {}
    for stage in STAGES:
        stage_images[stage] = {}
        for layer in LAYERS:
            stem = f"level4-{stage}-{layer}"
            src = SOURCES / f"{stem}-source.png"
            image = Image.open(src).convert("RGBA")
            if layer == "far":
                result = center_crop_resize(image).convert("RGB").convert("RGBA")
                result.putalpha(255)
            else:
                result = remove_magenta_binary(fit_moving_plate(image))
            dst = PROCESSED / f"{stem}.png"
            result.save(dst, optimize=True)
            result.save(PUBLIC / dst.name, optimize=True)
            stage_images[stage][layer] = result
            alpha = result.getchannel("A")
            hist = alpha.histogram()
            report["plates"][dst.name] = {
                "source": str(src.relative_to(ROOT)),
                "sourceSize": list(image.size),
                "runtimeSize": list(result.size),
                "transparent": hist[0],
                "opaque": hist[255],
                "partialAlpha": sum(hist[1:255]),
            }

        composite = stage_images[stage]["far"].copy()
        composite.alpha_composite(stage_images[stage]["middle"])
        composite.alpha_composite(stage_images[stage]["close"])
        viewport(composite).convert("RGB").save(QA / "composites" / f"{stage}-960x540.png")

        # Forced wrap: right 480 px beside left 480 px for each plate.
        for layer in LAYERS:
            img = stage_images[stage][layer]
            seam = Image.new("RGBA", VIEW, (0, 0, 0, 0))
            seam.alpha_composite(img.crop((840, 0, 1320, 540)), (0, 0))
            seam.alpha_composite(img.crop((0, 0, 480, 540)), (480, 0))
            if layer != "far":
                bg = checker().convert("RGBA")
                bg.alpha_composite(seam)
                seam = bg
            seam.convert("RGB").save(QA / "seams" / f"{stage}-{layer}-forced-wrap.png")

        # Background-only forward/reverse sampling contact sheet.
        sweep = Image.new("RGB", (VIEW[0] * 3, VIEW[1] * 2), "black")
        offsets = [0, 180, 360]
        for row, sequence in enumerate((offsets, list(reversed(offsets)))):
            for col, off in enumerate(sequence):
                frame = viewport(stage_images[stage]["far"], off)
                mid = viewport(stage_images[stage]["middle"], min(360, round(off * .055 / .018)))
                close = viewport(stage_images[stage]["close"], min(360, round(off * .13 / .018)))
                frame.alpha_composite(mid)
                frame.alpha_composite(close)
                sweep.paste(frame.convert("RGB"), (col * VIEW[0], row * VIEW[1]))
        sweep.save(QA / "sweeps" / f"{stage}-forward-reverse.png")

    # Four monotonic smoothstep boundary contact sheets at t=0,.25,.5,.75,1.
    for a, b in zip(STAGES, STAGES[1:]):
        ca = viewport(stage_images[a]["far"]).copy()
        ca.alpha_composite(viewport(stage_images[a]["middle"]))
        ca.alpha_composite(viewport(stage_images[a]["close"]))
        cb = viewport(stage_images[b]["far"]).copy()
        cb.alpha_composite(viewport(stage_images[b]["middle"]))
        cb.alpha_composite(viewport(stage_images[b]["close"]))
        sheet = Image.new("RGB", (VIEW[0] * 5, VIEW[1]), "black")
        for i, t in enumerate((0, .25, .5, .75, 1)):
            smooth = t * t * (3 - 2 * t)
            sheet.paste(Image.blend(ca, cb, smooth).convert("RGB"), (i * VIEW[0], 0))
        sheet.save(QA / "transitions" / f"{a}-to-{b}.png")

    (BASE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
