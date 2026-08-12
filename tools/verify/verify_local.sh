#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
. "$script_dir/run_bounded_process.sh"
. "$script_dir/godot_diagnostics.sh"
godot_bin="${TRASH_DASH_GODOT_BIN:-godot}"
expected_version="4.7.1.stable.official.a13da4feb"
temp_parent="${TMPDIR:-/tmp}"
temp_parent="${temp_parent%/}"
temp_dir="$(mktemp -d "$temp_parent/trash-dash-foundation-verify.XXXXXX")"

is_valid_temp_dir() {
	[[ -n "$temp_dir" ]] \
		&& [[ -d "$temp_dir" ]] \
		&& [[ "$temp_dir" != "/" ]] \
		&& [[ "$temp_dir" != "$repo_root" ]] \
		&& [[ "$temp_dir" != "$repo_root/"* ]] \
		&& [[ "$(cd "$(dirname "$temp_dir")" && pwd -P)" == "$(cd "$temp_parent" && pwd -P)" ]] \
		&& [[ "$(basename "$temp_dir")" == trash-dash-foundation-verify.* ]]
}

cleanup() {
	local original_status=$?
	trap - EXIT INT TERM
	local cleanup_status=0
	bounded_process_cleanup || cleanup_status=$?
	release_godot_process_lock || cleanup_status=$?
	if is_valid_temp_dir; then
		find "$temp_dir" -depth -delete
	else
		echo "Refusing to clean an unvalidated temporary directory" >&2
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

echo "[1/6] Policy"
"$script_dir/check_policy.sh"
"$script_dir/test_shell_contracts.sh"

echo "[2/6] Exact Godot version and headless import"
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
	"verify-version" \
	"$godot_bin" \
	--headless \
	--version)"
if [[ "$actual_version" != "$expected_version" ]]; then
	printf 'Godot version mismatch: expected %s, got %s\n' \
		"$expected_version" \
		"$actual_version" >&2
	exit 1
fi
printf 'Godot version: %s\n' "$actual_version"
echo "Godot executable: Standard"
run_godot_stage \
	"$repo_root" \
	"headless import" \
	"headless-import" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--editor \
	--quit

echo "[3/6] Tests"
TRASH_DASH_GODOT_BIN="$godot_bin" "$script_dir/run_tests.sh"

echo "[4/6] Headless editor smoke"
run_godot_stage \
	"$repo_root" \
	"headless editor smoke" \
	"editor-smoke" \
	"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--editor \
	--quit

echo "[5/6] Fresh unsigned macOS export"
export_dir="$temp_dir/export"
TRASH_DASH_GODOT_BIN="$godot_bin" "$script_dir/export_macos.sh" "$export_dir"

echo "[6/6] Bounded package process"
executable="$export_dir/extracted/Trash Dash 2.0.app/Contents/MacOS/Trash Dash 2.0"
prepare_godot_log_files "$repo_root" "package-smoke"
package_engine_log="$godot_log_engine_file"
package_output_log="$godot_log_output_file"
acquire_godot_process_lock
set +e
run_bounded_process \
	"$package_output_log" \
	"$executable" \
	--log-file "$package_engine_log" \
	--headless
package_status=$?
set -e
release_godot_process_lock
cat "$package_output_log"
check_godot_diagnostics \
	"bounded package smoke" "$package_engine_log" "$package_output_log"
if [[ "$package_status" -ne 0 ]]; then
	print_godot_failure \
		"bounded package smoke" "$package_status" \
		"$executable" --log-file "$package_engine_log" --headless
	exit "$package_status"
fi
echo "Local verification: PASS"
