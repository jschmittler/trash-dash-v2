#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
. "$script_dir/godot_diagnostics.sh"
godot_bin="${TRASH_DASH_GODOT_BIN:-godot}"
expected_version="4.7.1.stable.official.a13da4feb"
temp_parent="${TMPDIR:-/tmp}"
temp_parent="${temp_parent%/}"
temp_dir="$(mktemp -d "$temp_parent/trash-dash-run-tests.XXXXXX")"

is_valid_temp_dir() {
	[[ -n "$temp_dir" ]] \
		&& [[ -d "$temp_dir" ]] \
		&& [[ "$temp_dir" != "/" ]] \
		&& [[ "$temp_dir" != "$repo_root" ]] \
		&& [[ "$temp_dir" != "$repo_root/"* ]] \
		&& [[ "$(cd "$(dirname "$temp_dir")" && pwd -P)" == "$(cd "$temp_parent" && pwd -P)" ]] \
		&& [[ "$(basename "$temp_dir")" == trash-dash-run-tests.* ]]
}

cleanup() {
	local original_status=$?
	trap - EXIT INT TERM
	local cleanup_status=0
	if is_valid_temp_dir; then
		find "$temp_dir" -depth -delete
	else
		echo "Refusing to clean an unvalidated test-runner directory" >&2
		cleanup_status=1
	fi
	if [[ "$cleanup_status" -ne 0 ]]; then
		exit "$cleanup_status"
	fi
	exit "$original_status"
}

handle_int() {
	exit 130
}

handle_term() {
	exit 143
}

trap cleanup EXIT
trap handle_int INT
trap handle_term TERM

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

probe_log="$temp_dir/runner-probe.log"
set +e
run_godot_stage \
	"intentional failing runner probe" \
	"$probe_log" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--script res://tests/run_all.gd \
	--probe-fail
probe_status=$?
set -e
if [[ "$probe_status" -ne 1 ]]; then
	printf 'Runner probe expected exit 1, got %s\n' "$probe_status" >&2
	exit 1
fi
set +e
probe_message_count="$(rg -c -x -- 'intentional runner probe failure' "$probe_log")"
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
	"dependency-free GDScript suite" \
	"$temp_dir/test-suite.log" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--script res://tests/run_all.gd
