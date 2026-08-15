#!/usr/bin/env python3
"""Capture the immutable baseline for the design-library reorganization."""
from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import tempfile
from pathlib import Path

from library_layout import build_mapping

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_states(root: Path) -> tuple[set[str], dict[str, str]]:
    tracked = set(subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    ).stdout.decode().rstrip("\0").split("\0"))
    porcelain = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"], cwd=root, check=True, capture_output=True
    ).stdout.decode().split("\0")
    changed: dict[str, str] = {}
    index = 0
    while index < len(porcelain):
        entry = porcelain[index]
        if not entry:
            break
        state, path = entry[:2], entry[3:]
        if state[0] in {"R", "C"} and index + 1 < len(porcelain):
            index += 1
            path = porcelain[index]
        changed[path] = state
        index += 1
    return tracked, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output_relative = output.relative_to(ROOT).as_posix()
    records = [record for record in build_mapping(ROOT) if record.old_path != output_relative]
    tracked, changed = git_states(ROOT)
    rows = []
    for record in records:
        source = ROOT / record.old_path
        state = changed.get(record.old_path, "tracked" if record.old_path in tracked else "untracked")
        rows.append({
            "path": record.old_path,
            "size": source.stat().st_size,
            "sha256": sha256(source),
            "git_state": state,
            "category": record.category,
            "destination": record.new_path or "",
            "disposition": record.disposition,
            "stable_id": record.stable_id or "",
            "aliases": ",".join(record.aliases),
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=output.parent, delete=False) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        temporary = Path(stream.name)
    temporary.replace(output)
    print(f"DESIGN LIBRARY SNAPSHOT: {len(rows)} files")


if __name__ == "__main__":
    main()
