#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "public/assets/backgrounds"
EVIDENCE = ROOT / "tools/visual-audit/evidence/level3-parallax"
STAGES = ("restaurant-alley", "rainy-downtown-avenue", "rooftop-run", "subway-maintenance-tunnels", "construction-site-finale")
SPEEDS = {"far": 0.018, "middle": 0.055, "close": 0.13}
VIEW = (960, 540)

def tiled(stage, layer, camera_x):
    source = Image.open(ASSETS / f"level3-{stage}-{layer}.png").convert("RGBA")
    canvas = Image.new("RGBA", VIEW)
    offset = -round((camera_x * SPEEDS[layer]) % source.width)
    for x in (offset-source.width, offset, offset+source.width, offset+source.width*2):
        canvas.alpha_composite(source, (x, 0))
    return canvas

def composite(stage, camera_x):
    frame = Image.new("RGBA", VIEW, (0, 0, 0, 255))
    for layer in ("far", "middle", "close"):
        frame.alpha_composite(tiled(stage, layer, camera_x))
    return frame.convert("RGB")

def smoothstep(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)

def blended(left, right, camera_x, blend):
    amount = smoothstep(blend)
    return Image.blend(composite(left, camera_x), composite(right, camera_x), amount)

EVIDENCE.mkdir(parents=True, exist_ok=True)
checkpoint = Image.new("RGB", (960, 540*len(STAGES)))
for index, stage in enumerate(STAGES):
    frame = composite(stage, index*1320+660)
    checkpoint.paste(frame, (0, index*540))
    frame.save(EVIDENCE / f"checkpoint-{index+1}-{stage}.png")
checkpoint.save(EVIDENCE / "checkpoint-contact-sheet.png")

boundary = Image.new("RGB", (960*3, 540*(len(STAGES)-1)))
for row, (left, right) in enumerate(zip(STAGES, STAGES[1:])):
    for column, amount in enumerate((0.25, 0.5, 0.75)):
        boundary.paste(blended(left, right, (row+1)*1320, amount), (column*960, row*540))
boundary.save(EVIDENCE / "boundary-contact-sheet.png")

frames = []
positions = list(range(0, 6601, 120)) + list(range(6600, -1, -120))
for camera_x in positions:
    stage_index = min(4, camera_x // 1320)
    local = camera_x % 1320
    if stage_index < 4 and local >= 1080:
        blend = (local-1080)/240
        frame = blended(STAGES[stage_index], STAGES[stage_index+1], camera_x, blend)
    else:
        frame = composite(STAGES[stage_index], camera_x)
    frames.append(frame.resize((480, 270), Image.Resampling.NEAREST))
frames[0].save(EVIDENCE / "forward-reverse-background-sweep.gif", save_all=True, append_images=frames[1:], duration=70, loop=0)
print(EVIDENCE)
