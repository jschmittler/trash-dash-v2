#!/usr/bin/env python3
"""Extract staged UI crops from the Trash Dash UI Kit source sheets.

Raw mode makes exact region crops.
GrabCut mode attempts foreground extraction, but every output still requires visual review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-root', type=Path, default=Path('.'))
    parser.add_argument('--sheet', help='Optional sheet id from sprite-regions.json')
    parser.add_argument('--mode', choices=['raw', 'grabcut'], default='raw')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--padding', type=int, default=12)
    return parser.parse_args()


def add_padding(image: Image.Image, padding: int) -> Image.Image:
    out = Image.new('RGBA', (image.width + padding * 2, image.height + padding * 2), (0, 0, 0, 0))
    out.alpha_composite(image.convert('RGBA'), (padding, padding))
    return out


def grabcut_alpha(crop: Image.Image) -> Image.Image:
    try:
        import cv2
    except ImportError as exc:
        raise SystemExit('GrabCut mode requires opencv-python. Use --mode raw or install OpenCV.') from exc

    rgba = np.array(crop.convert('RGBA'))
    bgr = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    if w < 12 or h < 12:
        return crop.convert('RGBA')

    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    border = max(3, min(w, h) // 24)
    mask[:border, :] = cv2.GC_BGD
    mask[-border:, :] = cv2.GC_BGD
    mask[:, :border] = cv2.GC_BGD
    mask[:, -border:] = cv2.GC_BGD

    # Mark the central area as probable foreground. This is intentionally conservative.
    inset_x = max(border + 1, int(w * 0.08))
    inset_y = max(border + 1, int(h * 0.08))
    mask[inset_y:h-inset_y, inset_x:w-inset_x] = cv2.GC_PR_FGD

    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')

    # Preserve existing alpha where it is lower than the generated mask.
    original_alpha = rgba[:, :, 3]
    alpha = np.minimum(fg, np.where(original_alpha < 8, 0, 255).astype('uint8'))

    # Light morphological cleanup.
    kernel = np.ones((3, 3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel, iterations=1)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)

    out = rgba.copy()
    out[:, :, 3] = alpha
    result = Image.fromarray(out, 'RGBA')
    bbox = result.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    return result.crop(bbox) if bbox else result


def main() -> None:
    args = parse_args()
    root = args.package_root.resolve()
    region_file = root / 'manifests/sprite-regions.json'
    data = json.loads(region_file.read_text())
    args.output.mkdir(parents=True, exist_ok=True)

    selected = 0
    for sheet in data['sheets']:
        if args.sheet and sheet['id'] != args.sheet:
            continue
        source = root / sheet['path']
        image = Image.open(source).convert('RGBA')
        sheet_out = args.output / sheet['id']
        sheet_out.mkdir(parents=True, exist_ok=True)

        for asset in sheet['assets']:
            l, t, r, b = asset['region']
            crop = image.crop((l, t, r, b))
            if args.mode == 'grabcut':
                crop = grabcut_alpha(crop)
            crop = add_padding(crop, args.padding)
            crop.save(sheet_out / f"{asset['id']}.png")
            selected += 1

    if selected == 0:
        raise SystemExit('No assets matched the requested sheet id.')
    print(f'Extracted {selected} staged assets to {args.output}')
    if args.mode == 'grabcut':
        print('GrabCut output requires visual inspection and manual alpha cleanup before runtime use.')


if __name__ == '__main__':
    main()
