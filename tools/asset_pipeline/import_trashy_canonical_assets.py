#!/usr/bin/env python3
"""Import an extracted Trashy delivery into the V2 canonical design tree.

This importer copies only whitelisted delivery sources, preserves image bytes,
and writes a provenance-rich registry. It never promotes assets to runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # The audit remains useful without image metadata.
    Image = None


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs/design/trash-dash"
LIBRARY = DESIGN / "library"
MANUALS = DESIGN / "manuals"
TRASHY_PACKAGE = DESIGN / "packages/imported-source/trashy"
MANIFEST = DESIGN / "manifests/canonical-asset-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_details(path: Path) -> dict:
    if Image is None or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        return {}
    with Image.open(path) as image:
        bands = image.getbands()
        return {"dimensions": [image.width, image.height], "colorMode": image.mode, "hasAlpha": "A" in bands or "transparency" in image.info}


def copied(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and sha256(source) != sha256(target):
        raise RuntimeError(f"refusing to overwrite non-identical file: {target}")
    if not target.exists():
        shutil.copy2(source, target)


def add(records: list[dict], source: Path, target: Path, level: str, category: str, status: str, use: str, original: str, related: list[str] | None = None) -> None:
    copied(source, target)
    stem = target.stem.replace("level-", "").replace("level", "").strip("-_")
    # Shared support filenames (for example README.md) are only stable when
    # qualified by their resource path; named art remains concise.
    if category == "enemy-canon" and stem.lower() in {"readme", "changelog", "asset_manifest", "enemy_master_contract", "enemy_index"}:
        authority_root = MANUALS / "enemies" if target.is_relative_to(MANUALS / "enemies") else TRASHY_PACKAGE / "enemy-canon"
        stem = target.relative_to(authority_root).with_suffix("").as_posix().replace("/", ".")
    asset_id = f"level-{level}.{category}.{stem}"
    record = {"id": asset_id, "level": level, "resourceCategory": category, "canonicalPath": target.relative_to(ROOT).as_posix(), "originalArchivePath": original, "sha256": sha256(source), "intendedUsage": use, "runtimeStatus": "not-runtime", "canonicalStatus": status, "supersedes": None, "derivedFrom": None, "related": related or [], "notes": "Imported byte-for-byte; runtime migration is intentionally out of scope."}
    record.update(image_details(source))
    records.append(record)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="Extracted directory containing Trashy/")
    args = parser.parse_args()
    package = args.source / "Trashy"
    if not package.is_dir():
        raise SystemExit(f"missing extracted Trashy directory: {package}")
    records: list[dict] = []
    for number in range(1, 7):
        level = f"{number:02d}"
        incoming = package / "output" / f"level{number}"
        for source in sorted((incoming / "sprites").glob("*.png")):
            target = LIBRARY / "environments/props" / f"level-{level}" / source.name.replace(f"level{number}_", "")
            add(records, source, target, level, "prop-source", "canonical-source", "isolated approved prop artwork", f"Trashy/output/level{number}/sprites/{source.name}")
        for source in sorted(incoming.glob("*foreground-gameplay-assets.png")):
            add(records, source, TRASHY_PACKAGE / "levels" / f"level-{level}" / "references/foreground-gameplay-assets.png", level, "foreground-reference", "reference-only", "composite cohesion and inventory reference", f"Trashy/output/level{number}/{source.name}")
        for source in sorted(incoming.glob("*.manifest.json")):
            add(records, source, TRASHY_PACKAGE / "levels" / f"level-{level}" / "generation" / source.name, level, "generation-source", "reference-only", "generation manifest and source provenance", f"Trashy/output/level{number}/{source.name}")
        for source in sorted(incoming.glob("*.png")):
            if "foreground-gameplay-assets" in source.name or source.parent.name == "sprites":
                continue
            category = "tilesheet-source" if "tiles" in source.stem else "concept-art"
            branch = "environments/tiles" if category == "tilesheet-source" else "environments/concepts"
            destination = LIBRARY / branch / f"level-{level}" / source.name.replace(f"level{number}_", "")
            add(records, source, destination, level, category, "canonical-source", "approved level visual reference" if category == "concept-art" else "approved source tilesheet", f"Trashy/output/level{number}/{source.name}")
    for kind, category, status, usage in (("blueprints", "blueprint", "canonical-source", "level composition and progression reference"), ("concepts", "concept-art", "canonical-source", "interactive environment reference"), ("specs", "level-spec", "canonical-source", "written level interpretation and usage requirements")):
        for source in sorted((package / "docs/level-design" / kind).glob("*")):
            if not source.is_file():
                continue
            level = next((f"{n:02d}" for n in range(1, 7) if f"level{n}" in source.name.lower() or f"level_{n}" in source.name.lower()), "00")
            if kind == "specs":
                destination = MANUALS / "levels" / f"level-{level}" / source.name
            else:
                destination = LIBRARY / "environments" / kind / f"level-{level}" / source.name
            add(records, source, destination, level, category, status, usage, f"Trashy/docs/level-design/{kind}/{source.name}")
    enemy_source = package / "docs/enemy-canon"
    for source in sorted(enemy_source.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(enemy_source)
        target = TRASHY_PACKAGE / "enemy-canon" / relative if relative.parts[0] == "reference-art" else MANUALS / "enemies" / relative
        level = next((f"{n:02d}" for n in range(1, 7) if f"{n:02d}" in source.name or f"level-{n:02d}" in relative.as_posix()), "00")
        add(records, source, target, level, "enemy-canon", "canonical-source", "approved enemy identity and implementation canon", f"Trashy/docs/enemy-canon/{relative.as_posix()}")
    for source in sorted((package / "scripts").glob("*.py")):
        add(records, source, ROOT / "tools/asset_pipeline/trashy-source" / source.name, "00", "generation-source", "reference-only", "imported reproduction/support script; not executed by this import", f"Trashy/scripts/{source.name}")
    for source in sorted((package / ".cursor/rules").glob("*.mdc")):
        add(records, source, ROOT / "docs/asset-management/reference-contracts" / source.name, "00", "generation-source", "reference-only", "imported editor reference contract; not activated as project configuration", f"Trashy/.cursor/rules/{source.name}")
    enemy_skill = package / ".agents/skills/enemy-canon/SKILL.md"
    if enemy_skill.is_file():
        add(records, enemy_skill, ROOT / ".skills/enemy-canon/SKILL.md", "00", "enemy-canon", "canonical-source", "imported project-local enemy canon workflow", "Trashy/.agents/skills/enemy-canon/SKILL.md")
    records.sort(key=lambda entry: entry["id"])
    ids = [entry["id"] for entry in records]
    if len(ids) != len(set(ids)):
        duplicates = sorted(identifier for identifier, count in defaultdict(int, ((identifier, ids.count(identifier)) for identifier in ids)).items() if count > 1)
        raise RuntimeError(f"duplicate generated asset IDs: {duplicates}")
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"schema": "trash-dash-v2-canonical-assets-v1", "import": "Trashy.zip", "assets": records}, indent=2) + "\n")
    print(f"IMPORTED {len(records)} records into {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
