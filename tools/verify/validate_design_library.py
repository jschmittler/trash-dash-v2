#!/usr/bin/env python3
"""Validate the canonical Trash Dash design-library structure."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

DESIGN_REL = Path("docs/design/trash-dash")
CATALOG_REL = DESIGN_REL / "manifests/library-catalog.json"
MIGRATION_REL = DESIGN_REL / "manifests/LIBRARY_MIGRATION_MAP.tsv"
PREFLIGHT_REL = DESIGN_REL / "manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".tsv", ".yaml", ".yml", ".py", ".sh", ".gd", ".ts", ".cfg"}
LEGACY_LITERAL = "docs/design/trash-dash/reference/"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def active_text_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    direct = [root / "AGENTS.md", root / "README.md", root / ".gitattributes", root / ".gitignore"]
    scan_roots = [
        root / ".skills",
        root / "tools",
        root / "src",
        root / "tests",
        root / "assets/generated",
        root / "docs/architecture",
        root / "docs/migration",
        root / "docs/design/trash-dash/library",
        root / "docs/design/trash-dash/manuals",
    ]
    candidates.extend(path for path in direct if path.is_file())
    for scan_root in scan_roots:
        if scan_root.is_dir():
            candidates.extend(path for path in scan_root.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)
    return sorted(set(candidates))


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    design = root / DESIGN_REL
    catalog_path = root / CATALOG_REL
    migration_path = root / MIGRATION_REL
    preflight_path = root / PREFLIGHT_REL

    catalog_records: list[dict] = []
    if not catalog_path.is_file():
        failures.append(f"missing library catalog: {CATALOG_REL.as_posix()}")
    else:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        if payload.get("schema") != "trash-dash-v2-library-catalog-v1":
            failures.append("library catalog schema must be trash-dash-v2-library-catalog-v1")
        catalog_records = payload.get("assets", [])
        ids = [record.get("id") for record in catalog_records]
        paths = [record.get("canonicalPath") for record in catalog_records]
        failures.extend(f"duplicate canonical ID: {key}" for key, count in Counter(ids).items() if count > 1)
        failures.extend(f"duplicate canonical path: {key}" for key, count in Counter(paths).items() if count > 1)
        for record in catalog_records:
            relative = record.get("canonicalPath", "")
            if not relative.startswith("docs/design/trash-dash/library/"):
                failures.append(f"canonical path outside library: {relative}")
                continue
            path = root / relative
            if not path.is_file():
                failures.append(f"missing catalog path: {relative}")
                continue
            if sha256(path) != record.get("sha256"):
                failures.append(f"catalog hash mismatch: {relative}")
            if record.get("runtimeStatus") not in {"not-runtime", "runtime-approved"}:
                failures.append(f"invalid runtime status: {relative}")

    library = design / "library"
    cataloged = {record.get("canonicalPath") for record in catalog_records}
    if library.is_dir():
        for path in sorted(library.rglob("*")):
            if not path.is_file() or path.name in {"README.md", ".gdignore"}:
                continue
            relative = path.relative_to(root).as_posix()
            if relative not in cataloged:
                failures.append(f"uncataloged library file: {relative}")

    if not preflight_path.is_file():
        failures.append(f"missing preflight inventory: {PREFLIGHT_REL.as_posix()}")
        preflight_rows: list[dict[str, str]] = []
    else:
        preflight_rows = read_tsv(preflight_path)
    if not migration_path.is_file():
        failures.append(f"missing migration map: {MIGRATION_REL.as_posix()}")
    else:
        migration_rows = read_tsv(migration_path)
        preflight_paths = {row["path"] for row in preflight_rows}
        migration_paths = {row["old_path"] for row in migration_rows}
        for missing in sorted(preflight_paths - migration_paths):
            failures.append(f"preflight path absent from migration map: {missing}")
        for extra in sorted(migration_paths - preflight_paths):
            failures.append(f"migration path absent from preflight inventory: {extra}")
        for row in migration_rows:
            destination = row.get("new_path", "")
            disposition = row.get("disposition", "")
            if disposition == "generated-metadata-removed":
                if destination:
                    failures.append(f"removed metadata has destination: {row['old_path']}")
            elif destination and not (root / destination).is_file():
                failures.append(f"missing migration destination: {destination}")
            if disposition not in {"canonical-moved", "package-preserved", "archive", "generated-metadata-removed"}:
                failures.append(f"invalid migration disposition: {row['old_path']}")

    if design.is_dir():
        for path in sorted(design.rglob("*")):
            if path.is_file() and (path.suffix == ".import" or path.name == ".DS_Store"):
                failures.append(f"design metadata present: {path.relative_to(root).as_posix()}")

    for path in active_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if LEGACY_LITERAL in text:
            failures.append(f"active legacy path: {path.relative_to(root).as_posix()}")

    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    failures = validate(args.root.resolve())
    if failures:
        print("DESIGN LIBRARY VALIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("DESIGN LIBRARY VALIDATION: PASS")


if __name__ == "__main__":
    main()
