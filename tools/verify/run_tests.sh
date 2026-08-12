#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
godot_bin="${TRASH_DASH_GODOT_BIN:-godot}"
expected_version="4.7.1.stable.official.a13da4feb"

if [[ "$godot_bin" == */* ]]; then
	if [[ ! -x "$godot_bin" ]]; then
		printf 'Godot executable is not executable: %s\n' "$godot_bin" >&2
		exit 1
	fi
elif ! command -v "$godot_bin" >/dev/null 2>&1; then
	printf 'Godot executable was not found: %s\n' "$godot_bin" >&2
	exit 1
fi

actual_version="$("$godot_bin" --version)"
if [[ "$actual_version" != "$expected_version" ]]; then
	printf 'Godot version mismatch: expected %s, got %s\n' \
		"$expected_version" \
		"$actual_version" >&2
	exit 1
fi

printf 'Godot version: %s\n' "$actual_version"
echo "Godot executable: Standard"
"$godot_bin" --headless --path "$repo_root" --script res://tests/run_all.gd
