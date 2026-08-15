extends "res://tests/support/test_case.gd"

const AssetRefType := preload("res://src/core/schema/asset_ref.gd")
const AssetRefValidatorType := preload("res://src/core/schema/asset_ref_validator.gd")


func _valid_reference() -> AssetRefType:
	var reference := AssetRefType.new()
	reference.asset_id = &"boss_galactogobbler_isolated"
	reference.source_path = "res://assets/generated/boss-galactogobbler-isolated/boss-galactogobbler-isolated.png"
	return reference


func test_valid_asset_ref_produces_no_errors() -> void:
	var errors := AssetRefValidatorType.validate(_valid_reference())
	assert_equal(errors.size(), 0, "valid asset ref errors")


func test_runtime_asset_root_is_also_approved() -> void:
	var reference := _valid_reference()
	reference.source_path = "res://assets/runtime/trashy/trashy.png"
	var errors := AssetRefValidatorType.validate(reference)
	assert_equal(errors.size(), 0, "assets/runtime is an approved root")


func test_missing_asset_id_is_rejected() -> void:
	var reference := _valid_reference()
	reference.asset_id = &""
	var errors := AssetRefValidatorType.validate(reference)
	assert_true(errors.size() > 0, "missing asset id rejected")


func test_archive_path_is_rejected() -> void:
	var reference := _valid_reference()
	reference.source_path = "res://docs/design/trash-dash/library/archive/legacy/old.png"
	var errors := AssetRefValidatorType.validate(reference)
	assert_true(errors.size() > 0, "archive path rejected")
	assert_true(errors[0].find("noncanonical") != -1, "archive error message: %s" % errors[0])


func test_unapproved_path_outside_runtime_roots_is_rejected() -> void:
	var reference := _valid_reference()
	reference.source_path = "res://docs/design/trash-dash/library/characters/trashy.png"
	var errors := AssetRefValidatorType.validate(reference)
	assert_true(errors.size() > 0, "unapproved path rejected")
	assert_true(errors[0].find("unapproved") != -1, "unapproved error message: %s" % errors[0])


func test_missing_source_path_is_rejected() -> void:
	var reference := _valid_reference()
	reference.source_path = ""
	var errors := AssetRefValidatorType.validate(reference)
	assert_true(errors.size() > 0, "missing source path rejected")


func test_schema_version_mismatch_is_rejected() -> void:
	var reference := _valid_reference()
	reference.schema_version = AssetRefType.CURRENT_SCHEMA_VERSION + 1
	var errors := AssetRefValidatorType.validate(reference)
	assert_true(errors.size() > 0, "schema version mismatch rejected")
