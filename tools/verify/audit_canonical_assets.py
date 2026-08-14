#!/usr/bin/env python3
"""Validate the complete Trash Dash canonical design library."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = ImageOps = None

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/design/trash-dash/manifests/library-catalog.json"
LIBRARY = ROOT / "docs/design/trash-dash/library"


def digest(path: Path) -> str:
    data = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            data.update(chunk)
    return data.hexdigest()


def main() -> None:
    failures: list[str] = []
    if not MANIFEST.is_file():
        raise SystemExit(f"FAIL: missing manifest: {MANIFEST.relative_to(ROOT)}")
    payload = json.loads(MANIFEST.read_text())
    if payload.get("schema") != "trash-dash-v2-library-catalog-v1":
        raise SystemExit("FAIL: unsupported library catalog schema")
    assets = payload.get("assets", [])
    ids = [entry.get("id") for entry in assets]
    for asset_id, count in Counter(ids).items():
        if count > 1:
            failures.append(f"duplicate canonical ID: {asset_id}")
    canonical_claims = defaultdict(list)
    visual_hashes = defaultdict(list)
    registered = set()
    for entry in assets:
        path = ROOT / entry["canonicalPath"]
        registered.add(path.resolve())
        if not path.is_file():
            failures.append(f"missing canonical file: {entry['canonicalPath']}")
            continue
        if digest(path) != entry["sha256"]:
            failures.append(f"hash mismatch: {entry['canonicalPath']}")
        canonical_claims[(entry.get("level"), entry["resourceType"], path.parent.relative_to(ROOT).as_posix(), path.name)].append(entry["id"])
        if Image and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            with Image.open(path) as image:
                normalized = ImageOps.exif_transpose(image).convert("RGBA")
                visual_hashes[(normalized.size, hashlib.sha256(normalized.tobytes()).hexdigest())].append(entry["id"])
                expected = entry.get("dimensions")
                if expected and expected != [image.width, image.height]:
                    failures.append(f"dimension mismatch: {entry['canonicalPath']}")
    for claim, claim_ids in canonical_claims.items():
        if len(claim_ids) > 1:
            failures.append(f"multiple canonical claims for {claim}: {claim_ids}")
    for key, duplicate_ids in visual_hashes.items():
        if len(duplicate_ids) > 1:
            failures.append(f"visual duplicate canonical records: {duplicate_ids}")
    for path in LIBRARY.rglob("*"):
        if path.is_file() and path.name not in {"README.md", ".gdignore"} and path.resolve() not in registered:
            failures.append(f"unregistered canonical file: {path.relative_to(ROOT)}")
    if failures:
        print("CANONICAL ASSET AUDIT: FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        raise SystemExit(1)
    print(f"CANONICAL ASSET AUDIT: PASS ({len(assets)} registered files; {len(visual_hashes)} visual identities)")


if __name__ == "__main__":
    main()
