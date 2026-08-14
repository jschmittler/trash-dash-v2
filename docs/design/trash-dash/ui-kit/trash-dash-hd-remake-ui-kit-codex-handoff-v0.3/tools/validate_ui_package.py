#!/usr/bin/env python3
"""Validate paths, image dimensions, and SHA-256 hashes in the UI Kit package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-root', type=Path, default=Path('.'))
    args = parser.parse_args()
    root = args.package_root.resolve()
    manifest = json.loads((root / 'manifests/asset-manifest.json').read_text())
    errors = []

    for item in manifest['files']:
        path = root / item['path']
        if not path.exists():
            errors.append(f"MISSING {item['path']}")
            continue
        actual = sha256(path)
        if actual != item['sha256']:
            errors.append(f"HASH {item['path']} expected={item['sha256']} actual={actual}")
        if item.get('image'):
            with Image.open(path) as im:
                actual_size = [im.width, im.height]
                if actual_size != item['image']['size']:
                    errors.append(f"SIZE {item['path']} expected={item['image']['size']} actual={actual_size}")

    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f"Validated {len(manifest['files'])} files. All paths, hashes, and image dimensions match.")


if __name__ == '__main__':
    main()
