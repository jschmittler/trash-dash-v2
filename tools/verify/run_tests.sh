#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
. "$script_dir/godot_diagnostics.sh"
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

actual_version="$(run_godot_stage \
	"$repo_root" \
	"Godot version check" \
	"run-tests-version" \
	"$godot_bin" \
	--headless \
	--version)"
if [[ "$actual_version" != "$expected_version" ]]; then
	printf 'Godot version mismatch: expected %s, got %s\n' \
		"$expected_version" "$actual_version" >&2
	exit 1
fi

printf 'Godot version: %s\n' "$actual_version"
echo "Godot executable: Standard"

set +e
run_godot_stage \
	"$repo_root" \
	"intentional failing runner probe" \
	"runner-probe" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--script res://tests/run_all.gd \
	--probe-fail
probe_status=$?
set -e
probe_output_log="$godot_log_output_file"
if [[ "$probe_status" -ne 1 ]]; then
	printf 'Runner probe expected exit 1, got %s\n' "$probe_status" >&2
	exit 1
fi
set +e
probe_message_count="$(rg -c -x -- 'intentional runner probe failure' "$probe_output_log")"
probe_message_status=$?
set -e
if [[ "$probe_message_status" -gt 1 ]]; then
	printf 'Runner probe message scan failed with status %s\n' "$probe_message_status" >&2
	exit 1
fi
if [[ "$probe_message_status" -ne 0 || "$probe_message_count" -ne 1 ]]; then
	echo "Runner probe did not emit its deterministic message exactly once" >&2
	exit 1
fi
echo "Runner failure probe: PASS (exit 1, deterministic message)"

run_godot_stage \
	"$repo_root" \
	"dependency-free GDScript suite" \
	"test-suite" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--script res://tests/run_all.gd
