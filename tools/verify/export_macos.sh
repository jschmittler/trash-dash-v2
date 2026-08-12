#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
godot_bin="${TRASH_DASH_GODOT_BIN:-godot}"
expected_version="4.7.1.stable.official.a13da4feb"

if [[ "$#" -ne 1 ]]; then
	echo "Usage: tools/verify/export_macos.sh <empty-output-directory>" >&2
	exit 2
fi

requested_output="$1"
if [[ "$requested_output" != /* ]]; then
	echo "Output directory must be an explicit absolute path" >&2
	exit 2
fi
if [[ "$requested_output" != "/" && "$requested_output" == */ ]]; then
	echo "Output directory must not end with a slash" >&2
	exit 2
fi
if [[ "$requested_output" == "/" || "$requested_output" == "$repo_root" ]]; then
	echo "Output directory cannot be the filesystem or repository root" >&2
	exit 2
fi
if [[ -L "$requested_output" ]]; then
	echo "Output directory cannot be a symbolic link" >&2
	exit 2
fi

output_parent="$(dirname "$requested_output")"
output_name="$(basename "$requested_output")"
if [[ ! -d "$output_parent" || -L "$output_parent" ]]; then
	echo "Output parent must be an existing, non-symlink directory" >&2
	exit 2
fi
canonical_parent="$(cd "$output_parent" && pwd -P)"
output_dir="$canonical_parent/$output_name"

if [[ "$output_dir" == "$repo_root" || "$output_dir" == "$repo_root/"* ]]; then
	echo "Output directory must be outside the repository" >&2
	exit 2
fi
if [[ -e "$output_dir" && ! -d "$output_dir" ]]; then
	echo "Output path exists and is not a directory" >&2
	exit 2
fi
if [[ -d "$output_dir" ]] && [[ -n "$(find "$output_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
	echo "Output directory must be empty" >&2
	exit 2
fi

cd "$repo_root"
if ! git diff --quiet || ! git diff --cached --quiet; then
	echo "Export requires tracked source to match HEAD" >&2
	exit 1
fi
unexpected_untracked="$(
	git ls-files --others --exclude-standard \
		| rg -v '\.(uid|import)$' \
		|| true
)"
if [[ -n "$unexpected_untracked" ]]; then
	while IFS= read -r untracked_file; do
		printf '%s: unexpected untracked source blocks export\n' "$untracked_file" >&2
	done <<< "$unexpected_untracked"
	exit 1
fi
revision="$(git rev-parse HEAD)"

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

if [[ ! -d "$output_dir" ]]; then
	mkdir -- "$output_dir"
fi
package="$output_dir/trash-dash-foundation-macos.zip"
extract_dir="$output_dir/extracted"

echo "Export: unsigned macOS development package"
"$godot_bin" \
	--headless \
	--path "$repo_root" \
	--export-debug "macOS" \
	"$package"

unzip -t "$package"
mkdir -- "$extract_dir"
unzip -q "$package" -d "$extract_dir"
executable="$extract_dir/Trash Dash 2.0.app/Contents/MacOS/Trash Dash 2.0"
architectures="$(lipo -archs "$executable")"
if [[ " $architectures " != *" arm64 "* || " $architectures " != *" x86_64 "* ]]; then
	printf 'Architecture verification failed: %s\n' "$architectures" >&2
	exit 1
fi
package_sha_line="$(shasum -a 256 "$package")"
package_sha="${package_sha_line%% *}"
package_size="$(stat -f '%z' "$package")"

printf '%s\n' "$package_sha_line"
printf 'Revision: %s\n' "$revision"
printf 'Package: %s\n' "$package"
printf 'Package bytes: %s\n' "$package_size"
printf 'Package SHA-256: %s\n' "$package_sha"
printf 'Architectures: arm64 x86_64 (lipo: %s)\n' "$architectures"
