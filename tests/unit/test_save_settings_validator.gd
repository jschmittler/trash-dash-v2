extends "res://tests/support/test_case.gd"

const SaveSettingsType := preload("res://src/core/schema/save_settings.gd")
const SaveSettingsValidatorType := preload("res://src/core/schema/save_settings_validator.gd")
const InputMapContractType := preload("res://src/core/input/input_map_contract.gd")


func _valid_settings() -> SaveSettingsType:
	var settings := SaveSettingsType.new()
	settings.master_volume = 0.8
	settings.music_volume = 0.6
	settings.sfx_volume = 1.0
	settings.reduced_motion = false
	settings.key_bindings = InputMapContractType.REQUIRED_ACTIONS.duplicate(true)
	return settings


func test_valid_settings_produce_no_errors() -> void:
	var errors := SaveSettingsValidatorType.validate(_valid_settings())
	assert_equal(errors.size(), 0, "valid settings errors")


func test_missing_key_binding_for_a_required_action_is_rejected() -> void:
	var settings := _valid_settings()
	settings.key_bindings.erase(&"jump")
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "missing key binding rejected")


func test_unknown_action_in_key_bindings_is_rejected() -> void:
	var settings := _valid_settings()
	settings.key_bindings[&"does_not_exist"] = [KEY_Z]
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "unknown action rejected")
	assert_true(
		errors[0].find("unknown action") != -1, "unknown action error message: %s" % errors[0]
	)


func test_empty_key_binding_is_rejected() -> void:
	var settings := _valid_settings()
	settings.key_bindings[&"jump"] = []
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "empty key binding rejected")


func test_conflicting_key_bindings_across_actions_are_rejected() -> void:
	var settings := _valid_settings()
	settings.key_bindings[&"dash"] = [KEY_SPACE]
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "conflicting key bindings rejected")
	assert_true(errors[0].find("conflict") != -1, "conflict error message: %s" % errors[0])


func test_master_volume_out_of_range_is_rejected() -> void:
	var settings := _valid_settings()
	settings.master_volume = 1.5
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "out of range master volume rejected")


func test_negative_music_volume_is_rejected() -> void:
	var settings := _valid_settings()
	settings.music_volume = -0.1
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "negative music volume rejected")


func test_sfx_volume_boundary_values_are_valid() -> void:
	var settings := _valid_settings()
	settings.sfx_volume = 0.0
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_equal(errors.size(), 0, "zero sfx volume errors")


func test_schema_version_mismatch_is_rejected() -> void:
	var settings := _valid_settings()
	settings.schema_version = SaveSettingsType.CURRENT_SCHEMA_VERSION + 1
	var errors := SaveSettingsValidatorType.validate(settings)
	assert_true(errors.size() > 0, "schema version mismatch rejected")
