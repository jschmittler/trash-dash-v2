#!/usr/bin/env python3
"""Generate the canonical library catalog and complete migration map."""
from __future__ import annotations

import csv
import hashlib
import json
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs/design/trash-dash"
LIBRARY = DESIGN / "library"
MANIFESTS = DESIGN / "manifests"
PREFLIGHT = MANIFESTS / "LIBRARY_PRE_MIGRATION_INVENTORY.tsv"
CATALOG = MANIFESTS / "library-catalog.json"
MIGRATION = MANIFESTS / "LIBRARY_MIGRATION_MAP.tsv"
IMPORT_MANIFEST = MANIFESTS / "canonical-asset-manifest.json"

try:
    from PIL import Image
except ImportError:
    Image = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_preflight() -> list[dict[str, str]]:
    with PREFLIGHT.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    temporary.replace(path)


def resource_type(relative: Path) -> str:
    parts = relative.parts
    if parts[0] == "characters":
        if "animation-source" in parts:
            return "character-animation-source"
        if "concepts" in parts:
            return "character-concept"
        return "character-reference-sheet"
    if parts[0] == "environments":
        return {
            "backgrounds": "environment-background",
            "blueprints": "level-blueprint",
            "concepts": "environment-concept",
            "foreground": "foreground-reference",
            "props": "environment-prop",
            "tiles": "gameplay-tilesheet",
        }[parts[1]]
    if parts[0] == "gameplay":
        if "animation-source" in parts:
            return "gameplay-animation-source"
        return f"gameplay-{parts[1].rstrip('s')}-{parts[2].rstrip('s')}"
    if parts[0] == "interface":
        return f"interface-{parts[1].rstrip('s')}"
    if parts[0] == "branding":
        return f"branding-{parts[1].rstrip('s')}"
    return "design-source"


def identity(relative: Path) -> tuple[str | None, str | None]:
    parts = relative.parts
    level = next((part.removeprefix("level-") for part in parts if part.startswith("level-")), None)
    character = None
    if len(parts) >= 3 and parts[0] == "characters":
        if parts[1] == "heroes":
            character = parts[2]
        elif parts[1] == "bosses":
            character = parts[2]
        elif parts[1] == "enemies":
            character = relative.stem.removesuffix("-transparent").removesuffix("-approved")
    return level, character


def source_package(relative: Path, legacy_paths: list[str]) -> str:
    if "animation-source" in relative.parts and relative.parts[0] == "characters":
        return "character-animation/phase-05-codex-integration"
    if relative.parts[0] == "interface" and not any("ui-powerups" in old for old in legacy_paths):
        return "ui-kit/trash-dash-hd-remake-ui-kit-codex-handoff-v0.3"
    if relative.parts[:2] == ("gameplay", "powerups") and relative.name in {
        "taco-kite-powerups-clean-chroma.png",
        "taco-power-overlay-clean-8frame.png",
        "kite-power-overlay-clean-8frame.png",
        "powerups-branded-reference.png",
        "taco-power-overlay-branded-reference.png",
        "kite-power-overlay-branded-reference.png",
    }:
        return "powerups/trash-dash-hd-powerups-v1"
    if any("reference/levels/" in old for old in legacy_paths):
        return "Trashy.zip"
    return "trash-dash-codex-import-master-2026-08-11"


def stable_id(relative: Path) -> str:
    components = [part.replace("_", "-") for part in relative.with_suffix("").parts]
    return "library." + ".".join(components)


def character_aliases_by_hash() -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    inventory = DESIGN / "packages/character-animation/phase-05-codex-integration/CANONICAL_IMPORT_INVENTORY.json"
    if not inventory.is_file():
        return result
    for record in json.loads(inventory.read_text(encoding="utf-8")).get("assets", []):
        digest = record.get("approved_atlas_sha256")
        asset_id = record.get("asset_id")
        if digest and asset_id:
            result[digest].append(asset_id)
        alias = record.get("source_filename_alias")
        if digest and alias:
            result[digest].append(alias)
    return result


def generate() -> tuple[int, int]:
    preflight = read_preflight()
    legacy_by_destination: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in preflight:
        if row["destination"]:
            legacy_by_destination[row["destination"]].append(row)

    import_ids: dict[str, list[str]] = defaultdict(list)
    if IMPORT_MANIFEST.is_file():
        payload = json.loads(IMPORT_MANIFEST.read_text(encoding="utf-8"))
        for record in payload.get("assets", []):
            original = record.get("canonicalPath", "")
            matched = next(
                (row for row in preflight if row["path"] == original or row["destination"] == original),
                None,
            )
            if matched and matched["destination"]:
                import_ids[matched["destination"]].append(record["id"])
                record["canonicalPath"] = matched["destination"]
                if not matched["destination"].startswith("docs/design/trash-dash/library/"):
                    record["canonicalStatus"] = "package-source" if "/packages/" in matched["destination"] else "canonical-manual"
        payload["supersededByCatalog"] = "docs/design/trash-dash/manifests/library-catalog.json"
        payload["scope"] = "Trashy.zip import provenance; not the complete canonical library"
        atomic_text(IMPORT_MANIFEST, json.dumps(payload, indent=2) + "\n")

    animation_aliases = character_aliases_by_hash()
    assets = []
    for path in sorted(LIBRARY.rglob("*")):
        if not path.is_file() or path.name in {"README.md", ".gdignore"}:
            continue
        repo_relative = path.relative_to(ROOT).as_posix()
        library_relative = path.relative_to(LIBRARY)
        digest = sha256(path)
        legacy_rows = legacy_by_destination.get(repo_relative, [])
        old_paths = [row["path"] for row in legacy_rows]
        aliases = old_paths + import_ids.get(repo_relative, []) + animation_aliases.get(digest, [])
        aliases.extend(alias for row in legacy_rows for alias in row["aliases"].split(",") if alias)
        level, character = identity(library_relative)
        record = {
            "id": stable_id(library_relative),
            "resourceType": resource_type(library_relative),
            "canonicalPath": repo_relative,
            "level": level,
            "character": character,
            "approvalStatus": "approved-source",
            "sourcePackage": source_package(library_relative, old_paths),
            "sha256": digest,
            "intendedUsage": "design and implementation source; requires runtime promotion gate",
            "runtimeStatus": "not-runtime",
            "aliases": sorted(set(aliases)),
        }
        if Image is not None and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            with Image.open(path) as image:
                record["dimensions"] = [image.width, image.height]
                record["colorMode"] = image.mode
                record["hasAlpha"] = "A" in image.getbands() or "transparency" in image.info
        assets.append(record)

    catalog_payload = {
        "schema": "trash-dash-v2-library-catalog-v1",
        "authority": "docs/design/trash-dash/library/",
        "generatedFrom": "LIBRARY_PRE_MIGRATION_INVENTORY.tsv plus preserved approved package manifests",
        "assets": assets,
    }
    atomic_text(CATALOG, json.dumps(catalog_payload, indent=2) + "\n")

    migration_fields = ["old_path", "new_path", "stable_id", "sha256", "disposition", "category", "aliases"]
    lines = []
    output = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=MANIFESTS, delete=False)
    with output as stream:
        writer = csv.DictWriter(stream, fieldnames=migration_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in preflight:
            writer.writerow({
                "old_path": row["path"],
                "new_path": row["destination"],
                "stable_id": row["stable_id"],
                "sha256": row["sha256"],
                "disposition": row["disposition"],
                "category": row["category"],
                "aliases": row["aliases"],
            })
    Path(output.name).replace(MIGRATION)
    return len(assets), len(preflight)


def main() -> None:
    asset_count, migration_count = generate()
    print(f"LIBRARY CATALOG: {asset_count} assets; MIGRATION MAP: {migration_count} paths")


if __name__ == "__main__":
    main()
