extends "res://tests/support/test_case.gd"

const BuildIdentityType := preload("res://src/core/build/build_identity.gd")
const FoundationStatusType := preload("res://src/core/bootstrap/foundation_status.gd")
const DisplayPolicyType := preload("res://src/core/display/display_policy.gd")
const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")

func test_content_rects_are_centered() -> void:
	assert_equal(DisplayPolicyType.content_rect(Vector2i(1280, 720)), Rect2i(0, 0, 1280, 720), "16:9")
	assert_equal(DisplayPolicyType.content_rect(Vector2i(1440, 900)), Rect2i(0, 45, 1440, 810), "1440x900")
	assert_equal(DisplayPolicyType.content_rect(Vector2i(1280, 800)), Rect2i(0, 40, 1280, 720), "1280x800")
	assert_equal(DisplayPolicyType.content_rect(Vector2i(390, 844)), Rect2i(0, 312, 390, 219), "portrait desktop")
	assert_equal(DisplayPolicyType.content_rect(Vector2i.ZERO), Rect2i(), "zero")

func test_content_rects_cover_small_and_odd_sizes() -> void:
	assert_equal(DisplayPolicyType.content_rect(Vector2i(1, 1)), Rect2i(0, 0, 1, 0), "one pixel")
	assert_equal(DisplayPolicyType.content_rect(Vector2i(1001, 600)), Rect2i(0, 18, 1001, 563), "odd wide")
	assert_equal(DisplayPolicyType.content_rect(Vector2i(599, 1001)), Rect2i(0, 332, 599, 336), "odd tall")

func test_desktop_policy_has_no_mobile_ui() -> void:
	assert_equal(DisplayPolicyType.is_mobile_ui_enabled(&"macOS", false), false, "macOS")
	assert_equal(DisplayPolicyType.is_mobile_ui_enabled(&"Android", false), false, "feature absent")
	assert_equal(DisplayPolicyType.is_mobile_ui_enabled(&"Android", true), true, "future query")

func test_identity_and_status_are_immutable_values() -> void:
	var identity := BuildIdentityType.development()
	assert_equal(identity.version(), "0.1.0-foundation", "version")
	assert_equal(identity.revision(), "development", "revision")
	assert_true(not identity.text().contains("/"), "identity text contains no absolute path")
	var source := PackedStringArray(["first"])
	var status := FoundationStatusType.error(identity, source)
	source.append("mutated")
	assert_equal(status.messages(), PackedStringArray(["first"]), "copy input")
	assert_equal(status.state(), FoundationStatusType.State.FOUNDATION_ERROR, "state")
	var copied_messages := status.messages()
	copied_messages.append("mutated output")
	assert_equal(status.messages(), PackedStringArray(["first"]), "copy output")

func test_ready_and_error_status_factories_are_exact() -> void:
	var identity := BuildIdentityType.development()
	var ready := FoundationStatusType.ready(identity)
	assert_equal(ready.state(), FoundationStatusType.State.FOUNDATION_READY, "ready state")
	assert_equal(ready.identity(), identity, "ready identity")
	assert_equal(ready.title(), "Trash Dash 2.0", "ready title")
	assert_equal(ready.subtitle(), "macOS prototype foundation", "ready subtitle")
	assert_equal(ready.logical_size(), Vector2i(960, 540), "ready logical size")
	assert_equal(ready.renderer(), "Compatibility", "ready renderer")
	assert_equal(ready.content(), "prototype content not loaded", "ready content")
	assert_equal(ready.messages(), PackedStringArray(), "ready messages")
	var error := FoundationStatusType.error(identity, PackedStringArray(["problem"]))
	assert_equal(error.state(), FoundationStatusType.State.FOUNDATION_ERROR, "error state")
	assert_equal(error.identity(), identity, "error identity")
	assert_equal(error.messages(), PackedStringArray(["problem"]), "error messages")

func test_current_input_map_is_valid() -> void:
	assert_equal(InputMapContractType.validate_current(), PackedStringArray(), "input map")

func test_input_validation_reports_ordered_missing_and_mismatched_actions() -> void:
	var actual := {
		&"move_left": [KEY_A, KEY_RIGHT],
		&"jump": [KEY_SPACE],
	}
	assert_equal(
		InputMapContractType.validate_actions(actual),
		PackedStringArray([
			"input defaults mismatch: move_left",
			"missing input action: move_right",
			"missing input action: dash",
			"missing input action: action",
			"missing input action: pause",
		]),
		"input validation messages"
	)
