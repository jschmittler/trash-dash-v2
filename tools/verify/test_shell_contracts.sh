#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
temp_parent="${TMPDIR:-/tmp}"
temp_parent="${temp_parent%/}"
temp_dir="$(mktemp -d "$temp_parent/trash-dash-shell-contracts.XXXXXX")"
failures=0
fixture_repo=""
owned_child_pids=()
requested_group="${1:-all}"
cleanup_grace_attempts=20
cleanup_poll_seconds=0.05

is_valid_temp_dir() {
	[[ -n "$temp_dir" ]] \
		&& [[ -d "$temp_dir" ]] \
		&& [[ "$temp_dir" != "/" ]] \
		&& [[ "$temp_dir" != "$repo_root" ]] \
		&& [[ "$temp_dir" != "$repo_root/"* ]] \
		&& [[ "$(cd "$(dirname "$temp_dir")" && pwd -P)" == "$(cd "$temp_parent" && pwd -P)" ]] \
		&& [[ "$(basename "$temp_dir")" == trash-dash-shell-contracts.* ]]
}

register_owned_child() {
	owned_child_pids+=("$1")
}

unregister_owned_child() {
	local removed_pid="$1"
	local retained_pids=()
	for owned_pid in "${owned_child_pids[@]}"; do
		if [[ "$owned_pid" != "$removed_pid" ]]; then
			retained_pids+=("$owned_pid")
		fi
	done
	if [[ -n "${retained_pids[*]-}" ]]; then
		owned_child_pids=("${retained_pids[@]}")
	else
		owned_child_pids=()
	fi
}

is_active_owned_job() {
	local expected_pid="$1"
	local active_jobs=""
	active_jobs="$(jobs -pr)"
	for active_pid in $active_jobs; do
		if [[ "$active_pid" == "$expected_pid" ]]; then
			return 0
		fi
	done
	return 1
}

poll_owned_child_absence() {
	local owned_pid="$1"
	if [[ "${TRASH_DASH_SHELL_CLEANUP_FORCE_POLL_FAILURE:-0}" == "1" ]]; then
		return 1
	fi
	local attempt=0
	while [[ "$attempt" -lt "$cleanup_grace_attempts" ]]; do
		if ! is_active_owned_job "$owned_pid" || ! kill -0 "$owned_pid" 2>/dev/null; then
			return 0
		fi
		sleep "$cleanup_poll_seconds"
		attempt=$((attempt + 1))
	done
	return 1
}

reap_owned_child() {
	local owned_pid="$1"
	local had_errexit=false
	case $- in
		*e*) had_errexit=true ;;
	esac
	set +e
	wait "$owned_pid"
	local wait_status=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	unregister_owned_child "$owned_pid"
	if [[ "$wait_status" -eq 127 ]]; then
		printf 'Refusing stale or non-child PID during shell cleanup: %s\n' "$owned_pid" >&2
		return 1
	fi
	if kill -0 "$owned_pid" 2>/dev/null; then
		printf 'Owned child PID remains after reap: %s\n' "$owned_pid" >&2
		return 1
	fi
	return 0
}

cleanup_owned_child() {
	local owned_pid="$1"
	if [[ ! "$owned_pid" =~ ^[1-9][0-9]*$ ]]; then
		printf 'Invalid owned child PID during shell cleanup: %s\n' "$owned_pid" >&2
		return 1
	fi
	if ! is_active_owned_job "$owned_pid"; then
		reap_owned_child "$owned_pid"
		return $?
	fi
	if kill -0 "$owned_pid" 2>/dev/null; then
		kill -TERM "$owned_pid" 2>/dev/null || true
		if ! poll_owned_child_absence "$owned_pid"; then
			kill -KILL "$owned_pid" 2>/dev/null || true
			if ! poll_owned_child_absence "$owned_pid"; then
				printf 'Owned child remains after bounded KILL poll: %s\n' "$owned_pid" >&2
				return 1
			fi
		fi
	fi
	reap_owned_child "$owned_pid"
}

cleanup_owned_children() {
	local cleanup_status=0
	local cleanup_snapshot=()
	if [[ -n "${owned_child_pids[*]-}" ]]; then
		cleanup_snapshot=("${owned_child_pids[@]}")
	fi
	if [[ -z "${cleanup_snapshot[*]-}" ]]; then
		return 0
	fi
	for owned_pid in "${cleanup_snapshot[@]}"; do
		cleanup_owned_child "$owned_pid" || cleanup_status=1
	done
	return "$cleanup_status"
}

exit_cleanup() {
	local original_status=$?
	trap - EXIT INT TERM
	set +e
	local cleanup_status=0
	cleanup_owned_children || cleanup_status=1
	if is_valid_temp_dir; then
		find "$temp_dir" -depth -delete || cleanup_status=1
	else
		echo "Refusing to clean an unvalidated shell-contract directory" >&2
		cleanup_status=1
	fi
	if [[ "$cleanup_status" -ne 0 ]]; then
		echo "Shell contract cleanup failed" >&2
		exit 1
	fi
	exit "$original_status"
}

handle_int() {
	exit 130
}

handle_term() {
	exit 143
}

trap exit_cleanup EXIT
trap handle_int INT
trap handle_term TERM

run_cleanup_probe() {
	local child_pid_file="${TRASH_DASH_SHELL_CLEANUP_PID_FILE:?cleanup probe PID file required}"
	LC_ALL=C LANG=C /usr/bin/perl -e \
		'$SIG{INT} = "IGNORE"; $SIG{TERM} = "IGNORE"; sleep 1 while 1' &
	local child_pid=$!
	register_owned_child "$child_pid"
	printf '%s\n' "$child_pid" > "$child_pid_file"
	set +e
	wait "$child_pid"
	local child_status=$?
	set -e
	unregister_owned_child "$child_pid"
	return "$child_status"
}

if [[ "${TRASH_DASH_SHELL_CLEANUP_PROBE:-0}" == "1" ]]; then
	run_cleanup_probe
	exit 0
fi

record_failure() {
	printf 'not ok - %s\n' "$1" >&2
	failures=$((failures + 1))
}

record_success() {
	printf 'ok - %s\n' "$1"
}

create_policy_repo() {
	local case_name="$1"
	fixture_repo="$temp_dir/policy-$case_name"
	mkdir -p "$fixture_repo/tools/verify" "$fixture_repo/src/core/build"
	cp "$script_dir/check_policy.sh" "$fixture_repo/tools/verify/check_policy.sh"
	printf '%s\n' 'config_version=5' > "$fixture_repo/project.godot"
	printf '%s\n' '[preset.0]' 'name="macOS"' 'platform="macOS"' > "$fixture_repo/export_presets.cfg"
	printf '%s\n' 'class_name BuildIdentity' > "$fixture_repo/src/core/build/build_identity.gd"
	git -C "$fixture_repo" init -q
	git -C "$fixture_repo" add .
}

create_export_repo() {
	local case_name="$1"
	fixture_repo="$temp_dir/export-$case_name"
	mkdir -p "$fixture_repo/tools/verify"
	cp "$script_dir/export_macos.sh" "$fixture_repo/tools/verify/export_macos.sh"
	cp "$script_dir/godot_diagnostics.sh" "$fixture_repo/tools/verify/godot_diagnostics.sh"
	cp "$script_dir/godot_log_safety.sh" "$fixture_repo/tools/verify/godot_log_safety.sh"
	printf '%s\n' 'config_version=5' > "$fixture_repo/project.godot"
	git -C "$fixture_repo" init -q
	git -C "$fixture_repo" add .
	git -C "$fixture_repo" \
		-c user.name='Shell Contract Fixture' \
		-c user.email='fixture@example.invalid' \
		commit -q -m fixture
}

create_fake_godot() {
	local fake_godot="$1"
	local probe_status="${2:-1}"
	local probe_message="${3:-intentional runner probe failure}"
	printf '%s\n' \
		'#!/usr/bin/env bash' \
		'log_file=""' \
		'is_version=false' \
		'is_probe=false' \
		'while [[ "$#" -gt 0 ]]; do' \
		'  case "$1" in' \
		'    --log-file) log_file="$2"; shift 2 ;;' \
		'    --version) is_version=true; shift ;;' \
		'    --probe-fail) is_probe=true; shift ;;' \
		'    *) shift ;;' \
		'  esac' \
		'done' \
		'if [[ -z "$log_file" ]]; then echo "missing --log-file" >&2; exit 70; fi' \
		': > "$log_file"' \
		'if [[ -n "${TRASH_DASH_FAKE_GODOT_TEXT:-}" ]]; then printf "%s\n" "$TRASH_DASH_FAKE_GODOT_TEXT"; fi' \
		'if [[ "$is_version" == true ]]; then' \
		'  echo "4.7.1.stable.official.a13da4feb"' \
		'  exit 0' \
		'fi' \
		'if [[ "$is_probe" == true ]]; then' \
		"    printf '%s\\n' '$probe_message'" \
		"    exit $probe_status" \
		'fi' \
		'echo "Tests: 1, Failures: 0"' \
		'exit 0' > "$fake_godot"
	chmod +x "$fake_godot"
}

run_policy() {
	local policy_repo="$1"
	local output_file="$2"
	shift 2
	set +e
	(
		cd "$policy_repo"
		"$@" tools/verify/check_policy.sh
	) > "$output_file" 2>&1
	policy_status=$?
	set -e
}

test_missing_rg_rejects() {
	create_policy_repo "missing-rg"
	local output_file="$temp_dir/missing-rg.log"
	run_policy "$fixture_repo" "$output_file" env PATH=/usr/bin:/bin bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "missing rg exits nonzero"
		return
	fi
	if ! grep -F 'required command not found: rg' "$output_file" >/dev/null; then
		record_failure "missing rg reports its dependency"
		return
	fi
	record_success "missing rg exits nonzero"
}

test_legitimate_build_path_passes() {
	create_policy_repo "legitimate-build"
	local output_file="$temp_dir/legitimate-build.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -ne 0 ]]; then
		sed -n '1,120p' "$output_file" >&2
		record_failure "src/core/build remains accepted"
		return
	fi
	record_success "src/core/build remains accepted"
}

test_rg_error_rejects() {
	create_policy_repo "rg-error"
	local fake_bin="$temp_dir/fake-rg-bin"
	mkdir -p "$fake_bin"
	printf '%s\n' '#!/usr/bin/env bash' 'exit 2' > "$fake_bin/rg"
	chmod +x "$fake_bin/rg"
	local output_file="$temp_dir/rg-error.log"
	run_policy "$fixture_repo" "$output_file" env PATH="$fake_bin:/usr/bin:/bin" bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "rg errors exit nonzero"
		return
	fi
	if ! grep -F 'policy dependency error: rg failed with status 2' "$output_file" >/dev/null; then
		record_failure "rg errors report status"
		return
	fi
	record_success "rg errors exit nonzero"
}

test_policy_self_inspection_rejects_executable_statement() {
	create_policy_repo "self-inspection"
	printf '%s\n' 'git clean -n' >> "$fixture_repo/tools/verify/check_policy.sh"
	git -C "$fixture_repo" add tools/verify/check_policy.sh
	local output_file="$temp_dir/self-inspection.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "check_policy executable statements are inspected"
		return
	fi
	if ! grep -F 'tools/verify/check_policy.sh' "$output_file" >/dev/null; then
		record_failure "check_policy self-inspection prints its file"
		return
	fi
	record_success "check_policy executable statements are inspected"
}

test_forbidden_path_rejects() {
	local case_name="$1"
	local forbidden_path="$2"
	create_policy_repo "$case_name"
	mkdir -p "$fixture_repo/$(dirname "$forbidden_path")"
	printf '%s\n' 'fixture' > "$fixture_repo/$forbidden_path"
	git -C "$fixture_repo" add "$forbidden_path"
	local output_file="$temp_dir/$case_name.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "$forbidden_path is rejected"
		return
	fi
	if ! grep -F "$forbidden_path" "$output_file" >/dev/null; then
		record_failure "$forbidden_path prints its matched file"
		return
	fi
	record_success "$forbidden_path is rejected"
}

test_export_dependency_failure() {
	local case_name="$1"
	local expected_message="$2"
	local fixture_path="$3"
	local fake_bin="$temp_dir/export-$case_name-bin"
	create_export_repo "$case_name"
	mkdir -p "$fake_bin"
	local fake_godot="$fake_bin/godot"
	create_fake_godot "$fake_godot"
	local output_dir="$temp_dir/export-$case_name-output"
	local output_file="$temp_dir/export-$case_name.log"
	set +e
	(
		cd "$fixture_repo"
		env \
			PATH="$fixture_path" \
			TRASH_DASH_GODOT_BIN="$fake_godot" \
			tools/verify/export_macos.sh "$output_dir"
	) > "$output_file" 2>&1
	local export_status=$?
	set -e
	if [[ "$export_status" -eq 0 ]]; then
		record_failure "exporter $case_name exits nonzero"
		return
	fi
	if ! grep -F "$expected_message" "$output_file" >/dev/null; then
		sed -n '1,100p' "$output_file" >&2
		record_failure "exporter $case_name reports dependency failure"
		return
	fi
	record_success "exporter $case_name fails closed"
}

test_export_dependencies_fail_closed() {
	local missing_tools_bin="$temp_dir/export-missing-tools-bin"
	mkdir -p "$missing_tools_bin"
	ln -s /bin/bash "$missing_tools_bin/bash"
	ln -s /usr/bin/dirname "$missing_tools_bin/dirname"
	ln -s /bin/pwd "$missing_tools_bin/pwd"
	ln -s /bin/mkdir "$missing_tools_bin/mkdir"
	ln -s /usr/bin/basename "$missing_tools_bin/basename"
	ln -s /usr/bin/find "$missing_tools_bin/find"
	test_export_dependency_failure \
		"missing-git" \
		"required command not found: git" \
		"$missing_tools_bin"
	test_export_dependency_failure \
		"missing-rg" \
		"required command not found: rg" \
		"/usr/bin:/bin"

	local fake_git_bin="$temp_dir/export-git-error-bin"
	mkdir -p "$fake_git_bin"
	printf '%s\n' \
		'#!/usr/bin/env bash' \
		'if [[ "${1:-}" == "diff" ]]; then exit 0; fi' \
		'if [[ "${1:-}" == "ls-files" ]]; then exit 2; fi' \
		'if [[ "${1:-}" == "rev-parse" ]]; then echo fixture-revision; exit 0; fi' \
		'exit 0' > "$fake_git_bin/git"
	chmod +x "$fake_git_bin/git"
	test_export_dependency_failure \
		"git-ls-files-error" \
		"git ls-files failed with status 2" \
		"$fake_git_bin:/opt/homebrew/bin:/usr/bin:/bin"

	local fake_rg_bin="$temp_dir/export-rg-error-bin"
	mkdir -p "$fake_rg_bin"
	printf '%s\n' '#!/usr/bin/env bash' 'exit 2' > "$fake_rg_bin/rg"
	chmod +x "$fake_rg_bin/rg"
	test_export_dependency_failure \
		"rg-error" \
		"rg failed with status 2" \
		"$fake_rg_bin:/opt/homebrew/bin:/usr/bin:/bin"
}

test_godot_diagnostic_helper_contracts() {
	local helper="$script_dir/godot_diagnostics.sh"
	if [[ ! -f "$helper" ]]; then
		record_failure "Godot diagnostic helper exists"
		return
	fi
	# shellcheck source=/dev/null
	. "$helper"
	local fake_godot="$temp_dir/fake-godot-diagnostics"
	create_fake_godot "$fake_godot"
	for diagnostic_kind in warning error; do
		local diagnostic_text="WARNING: synthetic warning"
		if [[ "$diagnostic_kind" == "error" ]]; then
			diagnostic_text="ERROR: synthetic error"
		fi
		set +e
		TRASH_DASH_FAKE_GODOT_TEXT="$diagnostic_text" run_godot_stage \
			"$repo_root" \
			"zero-exit-$diagnostic_kind" \
			"contract-$diagnostic_kind" \
			"$fake_godot"
		local diagnostic_status=$?
		set -e
		if [[ "$diagnostic_status" -eq 0 ]]; then
			record_failure "zero-exit Godot $diagnostic_kind output fails"
		else
			record_success "zero-exit Godot $diagnostic_kind output fails"
		fi
	done
	set +e
	TRASH_DASH_FAKE_GODOT_TEXT=$'Godot Engine v4.7.1.stable.official.a13da4feb\nOpenGL API 4.1 Metal - 88.1 - Compatibility' run_godot_stage \
		"$repo_root" \
		"informational-renderer" \
		"contract-informational" \
		"$fake_godot"
	local informational_status=$?
	set -e
	if [[ "$informational_status" -ne 0 ]]; then
		record_failure "Godot banner and renderer information remain allowed"
	else
		record_success "Godot banner and renderer information remain allowed"
	fi
}

test_godot_log_safety_contracts() {
	local helper="$script_dir/godot_log_safety.sh"
	if [[ ! -f "$helper" ]]; then
		record_failure "Godot log safety helper exists"
		return
	fi
	# shellcheck source=/dev/null
	. "$helper"
	if ! prepare_godot_log_files "$repo_root" "safety-contract"; then
		record_failure "project-local Godot log directory is prepared"
		return
	fi
	local expected_directory="$repo_root/.codex/godot-logs"
	if [[ "$godot_log_directory" != "$expected_directory" \
		|| "$godot_log_engine_file" != "$expected_directory/safety-contract.log" \
		|| "$godot_log_output_file" != "$expected_directory/safety-contract.output.log" \
		|| ! -w "$godot_log_directory" ]]; then
		record_failure "Godot logs are writable and project-local"
	else
		record_success "Godot logs are writable and project-local"
	fi
	set +e
	prepare_godot_log_files "$temp_dir" "missing-project" >/dev/null 2>&1
	local missing_project_status=$?
	prepare_godot_log_files "$repo_root" "../escape" >/dev/null 2>&1
	local unsafe_purpose_status=$?
	set -e
	if [[ "$missing_project_status" -eq 0 || "$unsafe_purpose_status" -eq 0 ]]; then
		record_failure "unsafe Godot log targets are rejected before launch"
	else
		record_success "unsafe Godot log targets are rejected before launch"
	fi
	prepare_godot_log_files "$repo_root" "lock-contract"
	acquire_godot_process_lock
	set +e
	acquire_godot_process_lock >/dev/null 2>&1
	local duplicate_lock_status=$?
	set -e
	release_godot_process_lock
	if [[ "$duplicate_lock_status" -eq 0 ]]; then
		record_failure "concurrent Codex Godot process lock is rejected"
	else
		record_success "concurrent Codex Godot process lock is rejected"
	fi
	local fake_godot="$temp_dir/fake-godot-log-contract"
	local args_file="$temp_dir/fake-godot-log-contract.args"
	printf '%s\n' \
		'#!/usr/bin/env bash' \
		'printf "%s\n" "$@" > "${TRASH_DASH_FAKE_ARGS_FILE:?}"' \
		'while [[ "$#" -gt 0 ]]; do' \
		'  if [[ "$1" == "--log-file" ]]; then : > "$2"; shift 2; else shift; fi' \
		'done' \
		'exit 0' > "$fake_godot"
	chmod +x "$fake_godot"
	TRASH_DASH_FAKE_ARGS_FILE="$args_file" run_godot_stage \
		"$repo_root" "log argument contract" "argument-contract" "$fake_godot" --headless
	local expected_log="$repo_root/.codex/godot-logs/argument-contract.log"
	if ! grep -Fx -- '--log-file' "$args_file" >/dev/null \
		|| ! grep -Fx -- "$expected_log" "$args_file" >/dev/null; then
		record_failure "Godot launch receives explicit project-local --log-file"
	else
		record_success "Godot launch receives explicit project-local --log-file"
	fi
}

test_runner_probe_contracts() {
	local fake_godot="$temp_dir/fake-godot-wrong-exit"
	create_fake_godot "$fake_godot" 0 "intentional runner probe failure"
	local output_file="$temp_dir/run-tests-wrong-exit.log"
	set +e
	TRASH_DASH_GODOT_BIN="$fake_godot" "$script_dir/run_tests.sh" > "$output_file" 2>&1
	local runner_status=$?
	set -e
	if [[ "$runner_status" -eq 0 ]] || ! grep -F 'expected exit 1' "$output_file" >/dev/null; then
		sed -n '1,120p' "$output_file" >&2
		record_failure "runner rejects wrong intentional-probe exit"
	else
		record_success "runner rejects wrong intentional-probe exit"
	fi

	fake_godot="$temp_dir/fake-godot-wrong-message"
	create_fake_godot "$fake_godot" 1 "wrong runner probe message"
	output_file="$temp_dir/run-tests-wrong-message.log"
	set +e
	TRASH_DASH_GODOT_BIN="$fake_godot" "$script_dir/run_tests.sh" > "$output_file" 2>&1
	runner_status=$?
	set -e
	if [[ "$runner_status" -eq 0 ]] || ! grep -F 'deterministic message' "$output_file" >/dev/null; then
		sed -n '1,120p' "$output_file" >&2
		record_failure "runner rejects wrong intentional-probe message"
	else
		record_success "runner rejects wrong intentional-probe message"
	fi
}

test_forbidden_production_path_rejects() {
	local case_name="$1"
	local forbidden_path="$2"
	create_policy_repo "$case_name"
	mkdir -p "$fixture_repo/$(dirname "$forbidden_path")"
	printf '%s\n' 'fixture' > "$fixture_repo/$forbidden_path"
	git -C "$fixture_repo" add "$forbidden_path"
	local output_file="$temp_dir/$case_name.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "$forbidden_path is outside production allowlist"
		return
	fi
	if ! grep -F "$forbidden_path" "$output_file" >/dev/null; then
		record_failure "$forbidden_path allowlist rejection prints its file"
		return
	fi
	record_success "$forbidden_path is outside production allowlist"
}

test_current_production_allowlist_passes() {
	fixture_repo="$temp_dir/policy-current-production"
	mkdir -p "$fixture_repo/tools/verify"
	cp "$script_dir/check_policy.sh" "$fixture_repo/tools/verify/check_policy.sh"
	while IFS= read -r tracked_file; do
		mkdir -p "$fixture_repo/$(dirname "$tracked_file")"
		cp "$repo_root/$tracked_file" "$fixture_repo/$tracked_file"
	done < <(git -C "$repo_root" ls-files project.godot export_presets.cfg assets scenes src)
	git -C "$fixture_repo" init -q
	git -C "$fixture_repo" add .
	local output_file="$temp_dir/current-production.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -ne 0 ]]; then
		sed -n '1,140p' "$output_file" >&2
		record_failure "all approved production scaffold paths pass"
		return
	fi
	record_success "all approved production scaffold paths pass"
}

test_production_secret_rejects() {
	local case_name="$1"
	local production_file="$2"
	local secret_line="$3"
	create_policy_repo "$case_name"
	mkdir -p "$fixture_repo/$(dirname "$production_file")"
	printf '%s\n' "$secret_line" >> "$fixture_repo/$production_file"
	git -C "$fixture_repo" add "$production_file"
	local output_file="$temp_dir/$case_name.log"
	run_policy "$fixture_repo" "$output_file" bash
	if [[ "$policy_status" -eq 0 ]]; then
		record_failure "$case_name production secret is rejected"
		return
	fi
	if ! grep -F "$production_file" "$output_file" >/dev/null; then
		record_failure "$case_name secret rejection prints its file"
		return
	fi
	record_success "$case_name production secret is rejected"
}

run_policy_boundary_contracts() {
	test_missing_rg_rejects
	test_rg_error_rejects
	test_legitimate_build_path_passes
	test_forbidden_path_rejects "nested-exports" "docs/exports/app.zip"
	test_forbidden_path_rejects "root-credentials" "credentials/key.txt"
	test_forbidden_path_rejects "nested-secrets" "nested/secrets/token.txt"
	test_forbidden_path_rejects "build-nested-exports" "src/core/build/exports/app.zip"
	test_policy_self_inspection_rejects_executable_statement
	test_forbidden_production_path_rejects "audio-theme" "assets/audio/theme.ogg"
	test_forbidden_production_path_rejects "menu-scene" "scenes/menu/main.tscn"
	test_forbidden_production_path_rejects "level-scene" "scenes/levels/foo.tscn"
	test_forbidden_production_path_rejects "unexpected-module" "src/core/unexpected_module.gd"
	test_current_production_allowlist_passes
	test_production_secret_rejects "team-id" "project.godot" 'team_id="ABCDE12345"'
	test_production_secret_rejects "token" "export_presets.cfg" 'api_token="fixture-token"'
	test_production_secret_rejects "password" "scenes/bootstrap/bootstrap.tscn" 'metadata/password = "fixture-password"'
	test_production_secret_rejects "private-key" "src/core/build/build_identity.gd" 'const PRIVATE_KEY := "fixture-private-key"'
	test_production_secret_rejects "pem-material" "src/core/build/build_identity.gd" 'const PEM := "-----BEGIN PRIVATE KEY-----"'
	test_production_secret_rejects "pem-assignment" "src/core/build/build_identity.gd" 'const PEM_DATA := "fixture-pem-material"'
	test_production_secret_rejects "certificate" "project.godot" 'certificate="fixture-certificate"'
	test_production_secret_rejects "profile" "export_presets.cfg" 'provisioning_profile="fixture-profile"'
	test_production_secret_rejects "signing-identity" "scenes/bootstrap/bootstrap.tscn" 'metadata/signing_identity = "Developer ID Application: Fixture"'
}

process_pid_from() {
	awk '/^Package PID: / {print $3; exit}' "$1"
}

wait_for_process_pid() {
	local output_file="$1"
	for attempt in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
		observed_pid="$(process_pid_from "$output_file")"
		if [[ -n "$observed_pid" ]]; then
			return 0
		fi
		sleep 0.05
	done
	return 1
}

assert_pid_absent() {
	local process_pid="$1"
	local case_name="$2"
	if kill -0 "$process_pid" 2>/dev/null; then
		record_failure "$case_name exact PID is absent"
		return 1
	fi
	record_success "$case_name exact PID is absent"
}

wait_for_pid_absence() {
	local process_pid="$1"
	for attempt in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
		if ! kill -0 "$process_pid" 2>/dev/null; then
			return 0
		fi
		sleep 0.05
	done
	return 1
}

wait_for_owned_child_to_stop() {
	local process_pid="$1"
	for attempt in \
		1 2 3 4 5 6 7 8 9 10 \
		11 12 13 14 15 16 17 18 19 20 \
		21 22 23 24 25 26 27 28 29 30 \
		31 32 33 34 35 36 37 38 39 40 \
		41 42 43 44 45 46 47 48 49 50 \
		51 52 53 54 55 56 57 58 59 60; do
		if ! is_active_owned_job "$process_pid"; then
			return 0
		fi
		sleep 0.05
	done
	return 1
}

wait_for_file() {
	local expected_file="$1"
	for attempt in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
		if [[ -s "$expected_file" ]]; then
			return 0
		fi
		sleep 0.05
	done
	return 1
}

test_shell_cleanup_signal_case() {
	local signal_case="$1"
	local force_poll_failure="${2:-0}"
	local suffix="${signal_case}-normal"
	if [[ "$force_poll_failure" == "1" ]]; then
		suffix="${signal_case}-poll-failure"
	fi
	local output_file="$temp_dir/shell-cleanup-$suffix.out"
	local child_pid_file="$temp_dir/shell-cleanup-$suffix.pid"
	LC_ALL=C LANG=C /usr/bin/perl -e \
		'$SIG{INT} = "DEFAULT"; $SIG{TERM} = "DEFAULT"; exec {$ARGV[0]} @ARGV or die "exec failed: $!\n"' \
		env \
			TRASH_DASH_SHELL_CLEANUP_PROBE=1 \
			TRASH_DASH_SHELL_CLEANUP_PID_FILE="$child_pid_file" \
			TRASH_DASH_SHELL_CLEANUP_FORCE_POLL_FAILURE="$force_poll_failure" \
			/bin/bash "$script_dir/test_shell_contracts.sh" > "$output_file" 2>&1 &
	local runner_pid=$!
	register_owned_child "$runner_pid"
	if ! wait_for_file "$child_pid_file"; then
		record_failure "shell cleanup $suffix exposes owned child PID"
		cleanup_owned_child "$runner_pid" || true
		return
	fi
	local child_pid
	child_pid="$(sed -n '1p' "$child_pid_file")"
	kill -"$signal_case" "$runner_pid"
	if ! wait_for_owned_child_to_stop "$runner_pid"; then
		record_failure "shell cleanup $suffix returns within bound"
		kill -KILL "$runner_pid" 2>/dev/null || true
	fi
	set +e
	wait "$runner_pid"
	local runner_status=$?
	set -e
	unregister_owned_child "$runner_pid"
	if [[ "$force_poll_failure" == "1" ]]; then
		if [[ "$runner_status" -eq 0 || "$runner_status" -eq 130 || "$runner_status" -eq 143 ]]; then
			record_failure "shell cleanup poll failure overrides signal success"
		elif ! grep -F 'Shell contract cleanup failed' "$output_file" >/dev/null; then
			record_failure "shell cleanup poll failure is reported"
		else
			record_success "shell cleanup poll failure fails closed"
		fi
	else
		local expected_status=143
		if [[ "$signal_case" == "INT" ]]; then
			expected_status=130
		fi
		if [[ "$runner_status" -ne "$expected_status" ]]; then
			sed -n '1,100p' "$output_file" >&2
			record_failure "shell cleanup $signal_case returns $expected_status"
		else
			record_success "shell cleanup $signal_case returns $expected_status"
		fi
	fi
	if kill -0 "$child_pid" 2>/dev/null; then
		record_failure "shell cleanup $suffix owned child is absent"
		kill -KILL "$child_pid" 2>/dev/null || true
	else
		record_success "shell cleanup $suffix owned child is absent"
	fi
}

run_shell_cleanup_contracts() {
	local legacy_cleanup_pattern='^trap clean''up EXIT INT TERM$|recorded_''pids'
	if rg -n "$legacy_cleanup_pattern" "$script_dir/test_shell_contracts.sh" >/dev/null; then
		record_failure "shell cleanup uses separate status-preserving signal handlers and live ownership"
	else
		record_success "shell cleanup uses separate status-preserving signal handlers and live ownership"
	fi
	register_owned_child "$$"
	set +e
	cleanup_owned_child "$$" > "$temp_dir/stale-owned-pid.log" 2>&1
	local stale_cleanup_status=$?
	set -e
	if [[ "$stale_cleanup_status" -eq 0 ]] || ! kill -0 "$$" 2>/dev/null; then
		record_failure "stale non-child PID is refused without signaling"
	else
		record_success "stale non-child PID is refused without signaling"
	fi
	test_shell_cleanup_signal_case INT
	test_shell_cleanup_signal_case TERM
	test_shell_cleanup_signal_case TERM 1
}

test_post_kill_poll_failure_does_not_reap() {
	local process_runner="$script_dir/run_bounded_process.sh"
	for lifecycle_path in run cleanup; do
		local output_file="$temp_dir/post-kill-$lifecycle_path.out"
		local marker_file="$temp_dir/post-kill-$lifecycle_path.wait-called"
		local process_log="$temp_dir/post-kill-$lifecycle_path.log"
		local started_at="$(date +%s)"
		set +e
		/bin/bash -c '
			set -euo pipefail
			. "$1"
			lifecycle_path="$2"
			process_log="$3"
			marker_file="$4"
			bounded_process_startup_delay=0.1
			bounded_process_grace_attempts=1
			bounded_process_poll_seconds=0
			bounded_process_poll_until_absent() {
				return 1
			}
			bounded_process_reap() {
				printf "wait attempted\n" > "$marker_file"
				sleep 2
			}
			set +e
			if [[ "$lifecycle_path" == run ]]; then
				run_bounded_process "$process_log" /usr/bin/perl -e \
					'"'"'$SIG{INT} = "IGNORE"; $SIG{TERM} = "IGNORE"; sleep 1 while 1'"'"'
				contract_status=$?
			else
				LC_ALL=C LANG=C /usr/bin/perl -e \
					'"'"'$SIG{INT} = "IGNORE"; $SIG{TERM} = "IGNORE"; sleep 1 while 1'"'"' &
				bounded_process_pid=$!
				printf "Package PID: %s\n" "$bounded_process_pid"
				bounded_process_cleanup
				contract_status=$?
			fi
			set -e
			exit "$contract_status"
		' _ "$process_runner" "$lifecycle_path" "$process_log" "$marker_file" \
			> "$output_file" 2>&1
		local contract_status=$?
		set -e
		local elapsed_seconds=$(( $(date +%s) - started_at ))
		local child_pid="$(process_pid_from "$output_file")"
		if [[ -n "$child_pid" ]]; then
			wait_for_pid_absence "$child_pid" || true
		fi
		if [[ "$contract_status" -eq 0 ]]; then
			record_failure "post-KILL poll failure $lifecycle_path path returns failure"
		else
			record_success "post-KILL poll failure $lifecycle_path path returns failure"
		fi
		if [[ "$elapsed_seconds" -ge 2 ]]; then
			record_failure "post-KILL poll failure $lifecycle_path path returns within bound"
		else
			record_success "post-KILL poll failure $lifecycle_path path returns within bound"
		fi
		if [[ -e "$marker_file" ]]; then
			record_failure "post-KILL poll failure $lifecycle_path path skips blocking wait"
		else
			record_success "post-KILL poll failure $lifecycle_path path skips blocking wait"
		fi
		if ! grep -F 'Package process remains after bounded KILL poll' "$output_file" >/dev/null; then
			record_failure "post-KILL poll failure $lifecycle_path path reports failure"
		else
			record_success "post-KILL poll failure $lifecycle_path path reports failure"
		fi
		if [[ -z "$child_pid" ]]; then
			record_failure "post-KILL poll failure $lifecycle_path path records exact PID"
		elif kill -0 "$child_pid" 2>/dev/null; then
			record_failure "post-KILL poll failure $lifecycle_path child exact PID is absent"
		else
			record_success "post-KILL poll failure $lifecycle_path child exact PID is absent"
		fi
	done
}

run_process_contracts() {
	local process_runner="$script_dir/run_bounded_process.sh"
	if [[ ! -x "$process_runner" ]]; then
		record_failure "bounded process runner exists and is executable"
		return
	fi

	local normal_output="$temp_dir/process-normal.out"
	local normal_log="$temp_dir/process-normal.log"
	set +e
	TRASH_DASH_PROCESS_STARTUP_DELAY_SECONDS=0.1 \
	TRASH_DASH_PROCESS_GRACE_ATTEMPTS=5 \
	TRASH_DASH_PROCESS_POLL_SECONDS=0.05 \
		"$process_runner" "$normal_log" /bin/sleep 30 > "$normal_output" 2>&1
	local normal_status=$?
	set -e
	local normal_pid="$(process_pid_from "$normal_output")"
	if [[ "$normal_status" -ne 0 || -z "$normal_pid" ]]; then
		sed -n '1,160p' "$normal_output" >&2
		record_failure "normal SIGINT process contract"
	else
		record_success "normal SIGINT process contract"
		assert_pid_absent "$normal_pid" "normal SIGINT" || true
	fi

	for signal_case in INT TERM; do
		local signal_output="$temp_dir/process-wrapper-${signal_case}.out"
		local signal_log="$temp_dir/process-wrapper-${signal_case}.log"
		LC_ALL=C LANG=C /usr/bin/perl -e \
			'$SIG{INT} = "DEFAULT"; $SIG{TERM} = "DEFAULT"; exec {$ARGV[0]} @ARGV or die "exec failed: $!\n"' \
			/bin/bash "$process_runner" "$signal_log" /bin/sleep 30 > "$signal_output" 2>&1 &
		local runner_pid=$!
		register_owned_child "$runner_pid"
		if ! wait_for_process_pid "$signal_output"; then
			record_failure "abnormal $signal_case exposes exact child PID"
			cleanup_owned_child "$runner_pid" || true
			continue
		fi
		local child_pid="$observed_pid"
		kill -"$signal_case" "$runner_pid"
		set +e
		wait "$runner_pid"
		local runner_status=$?
		set -e
		unregister_owned_child "$runner_pid"
		local expected_status=143
		if [[ "$signal_case" == "INT" ]]; then
			expected_status=130
		fi
		if [[ "$runner_status" -ne "$expected_status" ]]; then
			record_failure "abnormal $signal_case returns $expected_status"
		else
			record_success "abnormal $signal_case returns $expected_status"
		fi
		assert_pid_absent "$child_pid" "abnormal $signal_case child" || true
	done

	local stubborn_output="$temp_dir/process-stubborn.out"
	local stubborn_log="$temp_dir/process-stubborn.log"
	set +e
	TRASH_DASH_PROCESS_STARTUP_DELAY_SECONDS=0.1 \
	TRASH_DASH_PROCESS_GRACE_ATTEMPTS=3 \
	TRASH_DASH_PROCESS_POLL_SECONDS=0.05 \
		"$process_runner" "$stubborn_log" /usr/bin/perl -e \
		'$SIG{INT} = "IGNORE"; $SIG{TERM} = "IGNORE"; sleep 1 while 1' \
		> "$stubborn_output" 2>&1
	local stubborn_status=$?
	set -e
	local stubborn_pid="$(process_pid_from "$stubborn_output")"
	if [[ "$stubborn_status" -eq 0 || -z "$stubborn_pid" ]]; then
		sed -n '1,160p' "$stubborn_output" >&2
		record_failure "nonresponsive child forces failing fallback"
	else
		record_success "nonresponsive child forces failing fallback"
		assert_pid_absent "$stubborn_pid" "nonresponsive child" || true
	fi
	if ! grep -F 'Forced process fallback: KILL' "$stubborn_output" >/dev/null; then
		record_failure "nonresponsive child reports KILL fallback"
	else
		record_success "nonresponsive child reports KILL fallback"
	fi
}

case "$requested_group" in
	all)
		run_policy_boundary_contracts
		test_export_dependencies_fail_closed
		test_godot_diagnostic_helper_contracts
		test_godot_log_safety_contracts
		test_runner_probe_contracts
		run_process_contracts
		test_post_kill_poll_failure_does_not_reap
		run_shell_cleanup_contracts
		;;
	policy)
		run_policy_boundary_contracts
		;;
	exporter)
		test_export_dependencies_fail_closed
		;;
	diagnostics)
		test_godot_diagnostic_helper_contracts
		test_godot_log_safety_contracts
		test_runner_probe_contracts
		;;
	process)
		run_process_contracts
		test_post_kill_poll_failure_does_not_reap
		;;
	cleanup)
		run_shell_cleanup_contracts
		;;
	*)
		printf 'Usage: tools/verify/test_shell_contracts.sh [all|policy|exporter|diagnostics|process|cleanup]\n' >&2
		exit 2
		;;
esac

printf 'Shell contract tests: %s failures\n' "$failures"
if [[ "$failures" -ne 0 ]]; then
	exit 1
fi
