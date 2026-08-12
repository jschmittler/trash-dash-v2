#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
temp_parent="${TMPDIR:-/tmp}"
temp_parent="${temp_parent%/}"
temp_dir="$(mktemp -d "$temp_parent/trash-dash-shell-contracts.XXXXXX")"
failures=0
fixture_repo=""
recorded_pids=()

is_valid_temp_dir() {
	[[ -n "$temp_dir" ]] \
		&& [[ -d "$temp_dir" ]] \
		&& [[ "$temp_dir" != "/" ]] \
		&& [[ "$temp_dir" != "$repo_root" ]] \
		&& [[ "$temp_dir" != "$repo_root/"* ]] \
		&& [[ "$(cd "$(dirname "$temp_dir")" && pwd -P)" == "$(cd "$temp_parent" && pwd -P)" ]] \
		&& [[ "$(basename "$temp_dir")" == trash-dash-shell-contracts.* ]]
}

cleanup() {
	set +u
	for recorded_pid in "${recorded_pids[@]}"; do
		if kill -0 "$recorded_pid" 2>/dev/null; then
			kill -TERM "$recorded_pid" 2>/dev/null || true
			sleep 0.1
		fi
		if kill -0 "$recorded_pid" 2>/dev/null; then
			kill -KILL "$recorded_pid" 2>/dev/null || true
		fi
	done
	set -u
	if is_valid_temp_dir; then
		find "$temp_dir" -depth -delete
	else
		echo "Refusing to clean an unvalidated shell-contract directory" >&2
	fi
}
trap cleanup EXIT INT TERM

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
			recorded_pids+=("$child_pid")
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
		recorded_pids+=("$normal_pid")
		assert_pid_absent "$normal_pid" "normal SIGINT" || true
	fi

	for signal_case in INT TERM; do
		local signal_output="$temp_dir/process-wrapper-${signal_case}.out"
		local signal_log="$temp_dir/process-wrapper-${signal_case}.log"
		LC_ALL=C LANG=C /usr/bin/perl -e \
			'$SIG{INT} = "DEFAULT"; $SIG{TERM} = "DEFAULT"; exec {$ARGV[0]} @ARGV or die "exec failed: $!\n"' \
			/bin/bash "$process_runner" "$signal_log" /bin/sleep 30 > "$signal_output" 2>&1 &
		local runner_pid=$!
		recorded_pids+=("$runner_pid")
		if ! wait_for_process_pid "$signal_output"; then
			record_failure "abnormal $signal_case exposes exact child PID"
			continue
		fi
		local child_pid="$observed_pid"
		recorded_pids+=("$child_pid")
		kill -"$signal_case" "$runner_pid"
		set +e
		wait "$runner_pid"
		local runner_status=$?
		set -e
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
		recorded_pids+=("$stubborn_pid")
		assert_pid_absent "$stubborn_pid" "nonresponsive child" || true
	fi
	if ! grep -F 'Forced process fallback: KILL' "$stubborn_output" >/dev/null; then
		record_failure "nonresponsive child reports KILL fallback"
	else
		record_success "nonresponsive child reports KILL fallback"
	fi
}

test_missing_rg_rejects
test_rg_error_rejects
test_legitimate_build_path_passes
test_forbidden_path_rejects "nested-exports" "docs/exports/app.zip"
test_forbidden_path_rejects "root-credentials" "credentials/key.txt"
test_forbidden_path_rejects "nested-secrets" "nested/secrets/token.txt"
test_forbidden_path_rejects "build-nested-exports" "src/core/build/exports/app.zip"
test_policy_self_inspection_rejects_executable_statement
run_process_contracts
test_post_kill_poll_failure_does_not_reap

printf 'Shell contract tests: %s failures\n' "$failures"
if [[ "$failures" -ne 0 ]]; then
	exit 1
fi
