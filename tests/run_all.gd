extends SceneTree

const PROJECT_CONTRACT_CASE: Script = preload("res://tests/unit/test_project_contract.gd")
const TEST_RUNNER_CASE: Script = preload("res://tests/unit/test_test_runner.gd")
const CORE_CONTRACT_CASE: Script = preload("res://tests/unit/test_core_contracts.gd")
const SERVICE_REGISTRY_CASE: Script = preload("res://tests/unit/test_service_registry.gd")
const STARTUP_VALIDATOR_CASE: Script = preload("res://tests/unit/test_startup_validator.gd")
const FIXED_STEP_CLOCK_CASE: Script = preload("res://tests/unit/test_fixed_step_clock.gd")
const LIVE_SCENE_TRANSITION_SERVICE_CASE: Script = preload(
	"res://tests/unit/test_live_scene_transition_service.gd"
)
const INPUT_REMAP_SERVICE_CASE: Script = preload("res://tests/unit/test_input_remap_service.gd")
const BOOTSTRAP_SCENE_CASE: Script = preload("res://tests/gameplay/test_bootstrap_scene.gd")
const VISUAL_CONTRACT_CASE: Script = preload("res://tests/visual/test_visual_contract.gd")
const RUNNER_PROBE_CASE: Script = preload("res://tests/support/runner_probe_case.gd")

var _usage_error: String = ""


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	await process_frame
	var failures := PackedStringArray()
	var test_count := 0
	for case_script: Script in _selected_scripts():
		var test_case: RefCounted = case_script.new()
		for method_name: StringName in _sorted_test_methods(test_case):
			test_count += 1
			await test_case.call(method_name)
		failures.append_array(test_case.call("failure_messages"))
		test_case = null
	if not _usage_error.is_empty():
		printerr(_usage_error)
		quit(2)
		return
	await process_frame
	for failure: String in failures:
		printerr(failure)
	print("Tests: %d, Failures: %d" % [test_count, failures.size()])
	quit(0 if failures.is_empty() else 1)


func _selected_scripts() -> Array[Script]:
	var all_cases: Array[Script] = [
		PROJECT_CONTRACT_CASE,
		TEST_RUNNER_CASE,
		CORE_CONTRACT_CASE,
		SERVICE_REGISTRY_CASE,
		STARTUP_VALIDATOR_CASE,
		FIXED_STEP_CLOCK_CASE,
		LIVE_SCENE_TRANSITION_SERVICE_CASE,
		INPUT_REMAP_SERVICE_CASE,
		BOOTSTRAP_SCENE_CASE,
		VISUAL_CONTRACT_CASE,
	]
	var suite_name := ""
	var probe_mode := ""
	for argument: String in OS.get_cmdline_args():
		if argument.begins_with("--suite="):
			if not suite_name.is_empty():
				_usage_error = "Usage: --suite=<file-stem> | --probe-pass | --probe-fail"
				return []
			suite_name = argument.trim_prefix("--suite=")
		elif argument == "--probe-pass" or argument == "--probe-fail":
			if not probe_mode.is_empty():
				_usage_error = "Usage: --suite=<file-stem> | --probe-pass | --probe-fail"
				return []
			probe_mode = argument
	if not suite_name.is_empty() and not probe_mode.is_empty():
		_usage_error = "Usage: --suite=<file-stem> | --probe-pass | --probe-fail"
		return []
	if not probe_mode.is_empty():
		return [RUNNER_PROBE_CASE]
	if suite_name.is_empty():
		return all_cases
	for case_script: Script in all_cases:
		if case_script.resource_path.get_file().get_basename() == suite_name:
			return [case_script]
	_usage_error = "Usage: --suite=<file-stem> | --probe-pass | --probe-fail"
	return []


func _sorted_test_methods(test_case: RefCounted) -> Array[StringName]:
	var names: Array[StringName] = []
	for method: Dictionary in test_case.get_method_list():
		var method_name := StringName(method["name"])
		if String(method_name).begins_with("test_"):
			names.append(method_name)
	names.sort()
	return names
