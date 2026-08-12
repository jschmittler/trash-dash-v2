#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
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
	if is_valid_temp_dir; then
		find "$temp_dir" -depth -delete
	else
		echo "Refusing to clean an unvalidated temporary directory" >&2
	fi
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
actual_version="$("$godot_bin" --version)"
if [[ "$actual_version" != "$expected_version" ]]; then
	printf 'Godot version mismatch: expected %s, got %s\n' \
		"$expected_version" \
		"$actual_version" >&2
	exit 1
fi
printf 'Godot version: %s\n' "$actual_version"
echo "Godot executable: Standard"
"$godot_bin" --headless --path "$repo_root" --editor --quit

echo "[3/6] Tests"
TRASH_DASH_GODOT_BIN="$godot_bin" "$script_dir/run_tests.sh"

echo "[4/6] Headless editor smoke"
"$godot_bin" --headless --path "$repo_root" --editor --quit

echo "[5/6] Fresh unsigned macOS export"
export_dir="$temp_dir/export"
TRASH_DASH_GODOT_BIN="$godot_bin" "$script_dir/export_macos.sh" "$export_dir"

echo "[6/6] Bounded package process"
executable="$export_dir/extracted/Trash Dash 2.0.app/Contents/MacOS/Trash Dash 2.0"
package_log="$temp_dir/package-smoke.log"
# Non-interactive shells start asynchronous children with SIGINT ignored. Reset
# it in a tiny exec wrapper so the recorded PID becomes Godot's PID and accepts
# the required interrupt instead of leaving an orphaned package process.
LC_ALL=C LANG=C /usr/bin/perl -e \
	'$SIG{INT} = "DEFAULT"; exec {$ARGV[0]} @ARGV or die "exec failed: $!\n"' \
	"$executable" --headless > "$package_log" 2>&1 &
package_pid=$!
printf 'Package PID: %s\n' "$package_pid"
sleep 2
if ! kill -0 "$package_pid" 2>/dev/null; then
	set +e
	wait "$package_pid"
	package_status=$?
	set -e
	printf 'Package exited before SIGINT with status %s\n' "$package_status" >&2
	exit 1
fi
kill -INT "$package_pid"
set +e
wait "$package_pid"
package_status=$?
set -e
if [[ "$package_status" -ne 130 ]]; then
	printf 'Package did not exit cleanly after SIGINT: %s\n' "$package_status" >&2
	exit 1
fi
if kill -0 "$package_pid" 2>/dev/null; then
	printf 'Package process is still present: %s\n' "$package_pid" >&2
	exit 1
fi
cat "$package_log"
if rg -n -i '(^|[[:space:]])(ERROR|WARNING):|leak|orphan|crash' "$package_log"; then
	echo "Package smoke log contains a failure diagnostic" >&2
	exit 1
fi
printf 'Process cleanup: PASS (PID %s absent, expected SIGINT exit 130)\n' "$package_pid"
echo "Local verification: PASS"
